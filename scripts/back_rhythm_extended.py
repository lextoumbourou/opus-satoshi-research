#!/usr/bin/env python3
"""Adam Back's posting rhythm (four venues, 1996-2021) vs Satoshi's.

Extends scripts/hour_compare.py (which used only Back's 156 randombit posts).
Reads cached data only (fetch with scripts/fetch_back_activity.py):

  randombit    data/lists/randombit/back-randombit.json        Date header (UTC via offset)
  bitcointalk  data/candidates/back-activity/bitcointalk/back-bitcointalk.jsonl
               ninjastic.space 'date' (UTC; checked against bitcointalk.org guest view)
  bitcoin-dev  data/candidates/back-activity/bitcoin-dev/back-bitcoindev.jsonl
               Back's own Date header with its offset
  cypherpunks  data/candidates/back-activity/cypherpunks/back-cypherpunks-1996-98.jsonl
               time embedded in Back's own sendmail Message-ID (<YYYYMMDDhhmm.QAAnnnnn@host>),
               shown below to be GMT/UTC (checked against his own Date headers preserved
               in the venona archive, venona-back-headers.jsonl)

Satoshi reference sets (data/satoshi/posts.jsonl):
  'all timed'   hour_compare.py convention (forum/svn/email/list, second/minute precision)
  'KDE ref'     dst_likelihood.py convention (also excludes assumed/unknown zone basis,
                2008-01-01 .. 2011-05-01, de-duplicated) -- used for the KDE likelihood,
                quiet-window definition and the permutation tests.

Output: printed; redirect to data/candidates/back-activity/rhythm-extended.txt
"""
import collections
import datetime as dt
import email.utils
import json
import math
import re
from zoneinfo import ZoneInfo

import numpy as np

BW = 0.9          # circular KDE bandwidth, hours (as dst_likelihood.py)
NPERM = 2000      # permutations for two-sample tests
RNG = np.random.default_rng(20260926)
UTC = dt.timezone.utc
LON, MLT = ZoneInfo("Europe/London"), ZoneInfo("Europe/Malta")
SOURCES = {"forum", "svn_commit", "email", "mailing_list"}
D = "data/candidates/back-activity"


def ts(s):
    return dt.datetime.strptime(s[:19], "%Y-%m-%dT%H:%M:%S").replace(tzinfo=UTC)


# ------------------------------------------------------------------ Satoshi
def load_satoshi():
    all_timed, kde_ref = [], set()
    for l in open("data/satoshi/posts.jsonl"):
        r = json.loads(l)
        if r.get("source_type") not in SOURCES or not r.get("timestamp_utc"):
            continue
        if r.get("timestamp_precision") not in ("second", "minute"):
            continue
        t = ts(r["timestamp_utc"])
        all_timed.append(t)
        if r.get("timezone_basis") in ("assumed", "unknown", "none"):
            continue
        if t.year >= 2008 and t <= dt.datetime(2011, 5, 1, tzinfo=UTC):
            kde_ref.add(t)
    return sorted(all_timed), sorted(kde_ref)


# ------------------------------------------------------------------ Back
MID_RE = re.compile(r"<(\d{12})\.([A-Z])([A-Z]{2})(\d+)@(server\.test\.net|server\.eternity\.org|adam\.test\.net)>")


def load_back():
    ds = collections.OrderedDict()
    # randombit
    ev = []
    for x in json.load(open("data/lists/randombit/back-randombit.json")):
        try:
            d = email.utils.parsedate_to_datetime(x["date_header"]).astimezone(UTC)
        except Exception:
            continue
        ev.append({"t": d, "zone": MLT, "label": x["subject"][:60], "off": None})
    ds["randombit 2010-15"] = ev
    # bitcointalk
    ev = []
    for l in open(f"{D}/bitcointalk/back-bitcointalk.jsonl"):
        r = json.loads(l)
        ev.append({"t": ts(r["date_utc"]), "zone": MLT, "label": r["title"][:60], "off": None})
    ds["bitcointalk 2013-21"] = ev
    # bitcoin-dev
    ev = []
    for l in open(f"{D}/bitcoin-dev/back-bitcoindev.jsonl"):
        r = json.loads(l)
        ev.append({"t": ts(r["utc"]), "zone": MLT, "label": r["subject"][:60], "off": r["utc_offset"],
                   "mailer": "mutt" if (r.get("mailer") or "").startswith("Mutt") else ("gmail" if "mail.gmail.com" in r["message_id"] else "other")})
    ds["bitcoin-dev 2013-21"] = ev
    # cypherpunks 1996-98: Back's own sendmail Message-ID time (GMT)
    ev, seen, excl = [], set(), collections.Counter()
    for l in open(f"{D}/cypherpunks/back-cypherpunks-1996-98.jsonl"):
        r = json.loads(l)
        m = MID_RE.match(r["message_id"] or "")
        if not m:
            host = (r["message_id"] or "").split("@")[-1].rstrip(">")
            excl["toad.com (list-server id)" if host == "toad.com" else "Exeter/olib (non-sendmail id format, zone unverified)"] += 1
            continue
        if r["message_id"] in seen:
            excl["duplicate Message-ID"] += 1
            continue
        seen.add(r["message_id"])
        t = dt.datetime.strptime(m.group(1), "%Y%m%d%H%M").replace(tzinfo=UTC) + dt.timedelta(seconds=30)
        ev.append({"t": t, "zone": LON, "label": r["subject"][:60], "off": None,
                   "qletter": ord(m.group(2)) - 65, "mid": r["message_id"], "subject": r["subject"],
                   "archive_utc": r["archive_utc"]})
    ds["cypherpunks 1996-98"] = ev
    return ds, excl


# ------------------------------------------------------------------ stats helpers
def hrs(events, zone=UTC):
    out = []
    for t in events:
        lt = t.astimezone(zone)
        out.append(lt.hour + lt.minute / 60 + lt.second / 3600)
    return np.array(out)


def kde(ref, x):
    d = x[:, None] - ref[None, :]
    k = sum(np.exp(-0.5 * ((d + s) / BW) ** 2) for s in (-24, 0, 24))
    return k / (BW * math.sqrt(2 * math.pi))


def mean_ll(ref, x, loo=False):
    k = kde(ref, x)
    if loo:
        np.fill_diagonal(k, 0)
        dens = k.sum(1) / (len(ref) - 1)
    else:
        dens = k.mean(1)
    return float(np.mean(np.log(np.maximum(dens, 1e-9))))


def frac(h, a, b):
    return float(np.mean((h >= a) & (h < b)))


def wilson(p, n, z=1.96):
    den = 1 + z * z / n
    c = (p + z * z / (2 * n)) / den
    w = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return max(0, c - w), min(1, c + w)


def watson_u2(a, b):
    n1, n2 = len(a), len(b)
    allv = np.concatenate([a, b])
    order = np.argsort(allv, kind="mergesort")
    lab = np.concatenate([np.ones(n1), np.zeros(n2)])[order]
    d = np.cumsum(lab) / n1 - np.cumsum(1 - lab) / n2
    N = n1 + n2
    return n1 * n2 / N ** 2 * float(np.sum((d - d.mean()) ** 2))


def perm_test(a, b, stat):
    obs = stat(a, b)
    allv = np.concatenate([a, b])
    n1 = len(a)
    ge = 0
    for _ in range(NPERM):
        p = RNG.permutation(allv)
        if stat(p[:n1], p[n1:]) >= obs:
            ge += 1
    return obs, (ge + 1) / (NPERM + 1)


def quiet_stat(a, b):
    """difference in share inside Satoshi's quiet window [06,14) UTC"""
    return abs(frac(a, 6, 14) - frac(b, 6, 14))


def hist(h):
    c = np.bincount(np.floor(h).astype(int) % 24, minlength=24)
    return 100 * c / max(1, len(h))


def quietest(h, width=8):
    p = hist(h)
    best = min(range(24), key=lambda s: sum(p[(s + i) % 24] for i in range(width)))
    return best, sum(p[(best + i) % 24] for i in range(width))


def ovl(a, b):
    return float(np.sum(np.minimum(hist(a), hist(b))))


def best_shift(ref, x):
    """shift (hours, step 0.25) of x that maximises mean log-lik under ref's KDE"""
    grid = np.arange(-12, 12, 0.25)
    lls = [mean_ll(ref, (x + s) % 24) for s in grid]
    i = int(np.argmax(lls))
    return float(grid[i]), lls[i]


def bars(title, cols, names):
    print(title)
    print("  hour | " + " | ".join(f"{n[:22]:>22s}" for n in names))
    for h in range(24):
        cells = []
        for c in cols:
            v = c[h]
            cells.append(f"{v:5.1f} {'#' * int(round(v / 1.0)):<16s}"[:22])
        print(f"   {h:02d}  | " + " | ".join(f"{x:22s}" for x in cells))
    print()


# ------------------------------------------------------------------ main
def main():
    s_all, s_ref = load_satoshi()
    S = hrs(s_ref)
    S_lon = hrs(s_ref, LON)
    ds, excl = load_back()
    print("ADAM BACK POSTING RHYTHM, FOUR VENUES 1996-2021, VS SATOSHI")
    print("=" * 78)
    print(f"Satoshi 'all timed' (hour_compare.py convention): n={len(s_all)}, "
          f"share 05:00-10:59 UTC = {100 * frac(hrs(s_all), 5, 11):.1f}%")
    q0, qv = quietest(S)
    print(f"Satoshi KDE reference (dst_likelihood.py convention): n={len(s_ref)} "
          f"({s_ref[0]:%Y-%m-%d} .. {s_ref[-1]:%Y-%m-%d})")
    print(f"  quietest 8 h UTC window: {q0:02d}:00-{(q0 + 8) % 24:02d}:00 with {qv:.1f}% of events; "
          f"05:00-10:59 share {100 * frac(S, 5, 11):.1f}%; 06:00-13:59 share {100 * frac(S, 6, 14):.1f}%")
    s_self = mean_ll(S, S, loo=True)
    print(f"  Satoshi leave-one-out mean log-lik/event under own KDE (bw {BW} h): {s_self:.3f} "
          f"(uniform = {math.log(1 / 24):.3f})")
    print()

    # ---------------- Message-ID verification
    cp = ds["cypherpunks 1996-98"]
    print("1. CYPHERPUNKS 1996-98: IS BACK'S SENDMAIL MESSAGE-ID TIME GMT OR LOCAL?")
    print("-" * 78)
    print("Excluded from the cypherpunks set:", dict(excl))
    # (a) own Date headers preserved in venona (Algebra.COM node) vs Message-ID of the same post
    V = [json.loads(l) for l in open(f"{D}/cypherpunks/venona-back-headers.jsonl")]
    norm = lambda s: re.sub(r"\W+", " ", (s or "").lower()).strip()[:40]
    rows = []
    for v in V:
        vd = email.utils.parsedate_to_datetime(v["Date"])
        c = [(abs((e["t"] - dt.timedelta(seconds=30) - vd).total_seconds()), e) for e in cp
             if norm(e["subject"]) == norm(v.get("Subject")) and abs((e["t"] - vd).total_seconds()) < 2 * 86400]
        c.sort(key=lambda x: x[0])
        if not c:
            rows.append((v, None, None, 0))
            continue
        e = c[0][1]
        mid_t = e["t"] - dt.timedelta(seconds=30)
        rows.append((v, e, (vd.astimezone(UTC) - mid_t).total_seconds() / 60, len(c)))
    print("(a) Back's own Date header (venona copy, sender's header preserved) vs the Message-ID")
    print("    time of the same post (cryptoanarchy.wiki copy), matched by subject within 2 days.")
    print("    If the Message-ID were BST local time, summer diffs would be about -60 min.")
    for season in ("BST (+0100)", "GMT"):
        sel = [r for r in rows if r[1] and (("+0100" in r[0]["Date"]) == season.startswith("BST"))]
        d = [r[2] for r in sel]
        uniq = [r[2] for r in sel if r[3] == 1]
        print(f"    {season:12s}: {len(sel)} matched posts; Date(UTC) - MID time: min {min(d):+.1f}, "
              f"max {max(d):+.1f} min (unique-candidate matches only: n={len(uniq)}, max |diff| {max(map(abs, uniq)):.1f})")
    print(f"    unmatched: {sum(1 for r in rows if not r[1])}")
    print("    examples:")
    shown = 0
    for v, e, diff, nc in rows:
        if e and nc == 1 and shown < 8 and (("+0100" in v["Date"]) or shown >= 6):
            print(f"      Date: {v['Date']:32s}  Message-ID: {e['mid']:42s} diff {diff:+.1f} min")
            shown += 1
    # (b) sendmail queue-ID hour letter vs Message-ID hour
    c = collections.Counter()
    for e in cp:
        mid_t = e["t"] - dt.timedelta(seconds=30)
        c[(bool(mid_t.astimezone(LON).dst()), (e["qletter"] - mid_t.hour) % 24)] += 1
    print("(b) sendmail queue-ID first letter (A=00 ... X=23) minus Message-ID hour, all "
          f"{len(cp)} posts:")
    for (bst, dh), n in sorted(c.items()):
        print(f"      {'UK summer (BST)' if bst else 'UK winter (GMT)'}: letter - MID hour = {dh:+d} h  in {n} posts")
    print("    -> the queue letter follows UK civil time (BST in summer) while the Message-ID")
    print("       time stays on GMT; i.e. Message-ID time = UTC, and the machine's zone was Europe/London.")
    # (c) arrival lag at the list
    lag = []
    for e in cp:
        if e["archive_utc"]:
            a = dt.datetime.strptime(e["archive_utc"][:19], "%Y-%m-%d %H:%M:%S").replace(tzinfo=UTC)
            lag.append(((a - (e["t"] - dt.timedelta(seconds=30))).total_seconds() / 60,
                        bool(e["t"].astimezone(LON).dst())))
    for bst in (False, True):
        L = sorted(x for x, b in lag if b == bst)
        print(f"(c) archive date minus MID time, {'BST' if bst else 'GMT'} months: n={len(L)}, "
              f"10th pct {L[len(L) // 10]:.0f} min, median {L[len(L) // 2]:.0f} min, "
              f"negative: {sum(1 for x in L if x < 0)} (of which {sum(1 for x in L if -61 <= x < 0)} within -61..0 min)")
    print("    (archive dates come from list servers with mixed/odd zone labels, so (c) is only a sanity")
    print("     check: a BST-local Message-ID would push the summer lags ~60 min negative. The large")
    print("     negatives are Sep-Oct 1998 posts whose archive '+0800' dates are ~12-13 h early, i.e.")
    print("     mislabelled by the archive, plus one post filed under the wrong month.)")
    print()

    # ---------------- per-dataset table
    post10 = ["randombit 2010-15", "bitcointalk 2013-21", "bitcoin-dev 2013-21"]
    ds["POOLED 2010-21 (Malta era)"] = [e for k in post10 for e in ds[k]]
    ds["POOLED all venues"] = [e for k in list(ds)[:4] for e in ds[k]]
    print("2. SUMMARY TABLE (Satoshi KDE reference n=%d)" % len(s_ref))
    print("-" * 78)
    hdr = (f"{'dataset':28s} {'n':>4s} {'range':17s} {'05-11 UTC':>14s} {'06-14 UTC':>14s} "
           f"{'LL/ev':>6s} {'dLL':>6s} {'OVL%':>5s} {'U2':>6s} {'p(U2)':>7s}")
    print(hdr)
    summary = {}
    for name, ev in ds.items():
        t = [e["t"] for e in ev]
        h = hrs(t)
        f1, f2 = frac(h, 5, 11), frac(h, 6, 14)
        ll = mean_ll(S, h)
        own = mean_ll(h, h, loo=True)
        u2, p = perm_test(h, S, watson_u2)
        summary[name] = dict(n=len(h), f1=f1, f2=f2, ll=ll, own=own, u2=u2, p=p)
        lo1, hi1 = wilson(f1, len(h))
        lo2, hi2 = wilson(f2, len(h))
        print(f"{name:28s} {len(h):4d} {min(t):%Y-%m}..{max(t):%Y-%m}   "
              f"{100 * f1:4.1f} [{100 * lo1:2.0f}-{100 * hi1:2.0f}] {100 * f2:4.1f} [{100 * lo2:2.0f}-{100 * hi2:2.0f}] "
              f"{ll:6.2f} {ll - own:+6.2f} {ovl(h, S):5.1f} {u2:6.3f} {p:7.4f}")
    f1s, f2s = frac(S, 5, 11), frac(S, 6, 14)
    print(f"{'Satoshi KDE ref':28s} {len(S):4d} {s_ref[0]:%Y-%m}..{s_ref[-1]:%Y-%m}   "
          f"{100 * f1s:4.1f} {'':7s} {100 * f2s:4.1f} {'':7s} {s_self:6.2f}")
    print("Columns: share of posts in 05:00-10:59 and 06:00-13:59 UTC with Wilson 95% CI;")
    print("  LL/ev = mean log-likelihood per post of Back's UTC hour under Satoshi's circular KDE")
    print(f"  (bw {BW} h; Satoshi's own leave-one-out value {s_self:.2f}, uniform {math.log(1 / 24):.2f});")
    print("  dLL = LL/ev minus Back's own leave-one-out LL/ev (how much worse Satoshi's rhythm explains")
    print("  Back's posts than Back's own rhythm does; exp(dLL) = average likelihood ratio per post);")
    print("  OVL = overlap of the 24-bin hour histograms (100 = identical); U2 = two-sample Watson U^2")
    print(f"  (circular), p from {NPERM} label permutations (minimum attainable p = {1 / (NPERM + 1):.4f}).")
    print()

    # ---------------- histograms
    for group, zone, zname in ((["cypherpunks 1996-98"], LON, "Europe/London"),
                               (post10 + ["POOLED 2010-21 (Malta era)"], MLT, "Europe/Malta")):
        cols_u = [hist(hrs([e["t"] for e in ds[g]])) for g in group] + [hist(S)]
        bars(f"3. HOUR-OF-DAY HISTOGRAM, UTC (% of posts) -- {', '.join(group)}", cols_u, group + ["Satoshi (UTC)"])
        cols_l = [hist(hrs([e["t"] for e in ds[g]], zone)) for g in group] + [hist(S_lon)]
        bars(f"4. HOUR-OF-DAY HISTOGRAM, BACK'S LOCAL CIVIL TIME ({zname}); Satoshi shown in Europe/London "
             f"civil time (the zone his machine timestamps follow)", cols_l, group + ["Satoshi (London)"])

    # bitcoin-dev: header offset local time + offsets by year
    bd = ds["bitcoin-dev 2013-21"]
    print("5. BITCOIN-DEV DATE-HEADER OFFSETS (Back's machine / mail-account zone) by year and mailer")
    c = collections.Counter((e["t"].year, e["mailer"], e["off"]) for e in bd)
    for y in sorted({k[0] for k in c}):
        print(f"   {y}: " + ", ".join(f"{m} {o}: {n}" for (yy, m, o), n in sorted(c.items()) if yy == y))
    home = [e for e in bd if e["off"] in ("+0100", "+0200") and
            (e["off"] == ("+0200" if e["t"].astimezone(MLT).dst() else "+0100"))]
    print(f"   posts whose offset equals Malta civil time at that date: {len(home)} of {len(bd)}")
    hh = hrs([e["t"] for e in home])
    print(f"   Malta-consistent subset: 05-11 UTC {100 * frac(hh, 5, 11):.1f}%, 06-14 UTC {100 * frac(hh, 6, 14):.1f}%")
    loc = []
    for e in bd:
        o = int(e["off"][:3]) * 60 + (1 if e["off"][0] == "+" else -1) * int(e["off"][3:])
        lt = e["t"] + dt.timedelta(minutes=o)
        loc.append(lt.hour + lt.minute / 60)
    loc = np.array(loc)
    print(f"   in header-offset local time: share 00:00-07:59 {100 * frac(loc, 0, 8):.1f}%, "
          f"08:00-15:59 {100 * frac(loc, 8, 16):.1f}%, 16:00-23:59 {100 * frac(loc, 16, 24):.1f}%")
    print()

    # ---------------- local-time shape comparison
    print("6. SHAPE IN LOCAL CIVIL TIME (night-owl or daytime?)")
    print("-" * 78)
    rowsL = [("Satoshi, Europe/London time", S_lon)]
    for g, z in (("cypherpunks 1996-98", LON), ("randombit 2010-15", MLT), ("bitcointalk 2013-21", MLT),
                 ("bitcoin-dev 2013-21", MLT), ("POOLED 2010-21 (Malta era)", MLT)):
        rowsL.append((f"Back {g}, {'London' if z is LON else 'Malta'} time", hrs([e["t"] for e in ds[g]], z)))
    rowsL.insert(1, ("Satoshi, Europe/Malta time", hrs(s_ref, MLT)))
    print(f"   {'':44s} {'00-06':>6s} {'06-09':>6s} {'09-13':>6s} {'13-18':>6s} {'18-24':>6s}  quietest 8h (local)")
    for name, h in rowsL:
        q, qv = quietest(h)
        print(f"   {name:44s} " + " ".join(f"{100 * frac(h, a, b):6.1f}" for a, b in ((0, 6), (6, 9), (9, 13), (13, 18), (18, 24)))
              + f"  {q:02d}-{(q + 8) % 24:02d} ({qv:.1f}%)")
    print()
    print("   Best time-shift: shift Back's local hours by s to maximise LL/ev under Satoshi's London-time")
    print("   KDE (tests whether the SHAPES match up to a zone difference).")
    for g, z in (("cypherpunks 1996-98", LON), ("POOLED 2010-21 (Malta era)", MLT)):
        h = hrs([e["t"] for e in ds[g]], z)
        s, ll = best_shift(S_lon, h)
        sh = (h + s) % 24
        so = max(range(-12, 12), key=lambda k: ovl((h + k) % 24, S_lon))
        print(f"   {g:28s}: unshifted LL/ev {mean_ll(S_lon, h):.2f} OVL {ovl(h, S_lon):.1f}%; best-LL shift {s:+.2f} h "
              f"-> LL/ev {ll:.2f}, OVL {ovl(sh, S_lon):.1f}%; best-OVL shift {so:+d} h -> OVL {ovl((h + so) % 24, S_lon):.1f}%"
              f"  (Satoshi self LOO {mean_ll(S_lon, S_lon, loo=True):.2f})")
    # UK-era Back vs Satoshi, both in London time, permutation tests
    cph = hrs([e["t"] for e in cp], LON)
    u2, p = perm_test(cph, S_lon, watson_u2)
    qd, pq = perm_test(cph, S_lon, quiet_stat)
    print(f"   Back 1996-98 (London) vs Satoshi (London): Watson U2 = {u2:.3f}, permutation p = {p:.4f}")
    print(f"   share of posts in Satoshi's quiet window 06:00-13:59 UTC (07-15 BST / 06-14 GMT):"
          f" Back 1996-98 {100 * frac(hrs([e['t'] for e in cp]), 6, 14):.1f}% vs Satoshi {100 * f2s:.1f}% "
          f"(|diff| {100 * qd:.1f} pts, permutation p = {pq:.4f})")
    # weekday / weekend
    print()
    print("   Weekday vs weekend (day and hour in each person's local civil time; Satoshi in London time):")
    for name, tl, z in (("Satoshi", s_ref, LON), ("Back cypherpunks 1996-98", [e["t"] for e in cp], LON),
                        ("Back POOLED 2010-21", [e["t"] for e in ds["POOLED 2010-21 (Malta era)"]], MLT)):
        for lab, wk in (("Mon-Fri", range(0, 5)), ("Sat-Sun", range(5, 7))):
            sel = [t for t in tl if t.astimezone(z).weekday() in wk]
            h = hrs(sel, z)
            print(f"     {name:26s} {lab}: n={len(h):4d}  share at 07:00-14:59 local {100 * frac(h, 7, 15):5.1f}%  "
                  f"at 09:00-12:59 local {100 * frac(h, 9, 13):5.1f}%")
    # year-by-year
    print()
    print("7. BY YEAR (all venues pooled)")
    by = collections.defaultdict(list)
    for e in ds["POOLED all venues"]:
        by[e["t"].year].append(e["t"])
    for y in sorted(by):
        h = hrs(by[y])
        print(f"   {y}: n={len(h):4d}  05-11 UTC {100 * frac(h, 5, 11):5.1f}%  06-14 UTC {100 * frac(h, 6, 14):5.1f}%")
    print()

    # ---------------- overlap period
    print("8. SATOSHI'S ACTIVE PERIOD (Nov 2008 - Apr 2011): BACK ITEMS AND CLOSEST APPROACHES")
    print("-" * 78)
    a0, a1 = dt.datetime(2008, 11, 1, tzinfo=UTC), dt.datetime(2011, 5, 1, tzinfo=UTC)
    ov = sorted([e for e in ds["POOLED all venues"] if a0 <= e["t"] < a1], key=lambda e: e["t"])
    # Back's own replies to Satoshi, Aug 2008 (COPA exhibit AB1 'Sent:' lines, UTC+01:00 export)
    copa = [dt.datetime(2008, 8, 21, 12, 55, 59, tzinfo=UTC), dt.datetime(2008, 8, 21, 18, 17, 17, tzinfo=UTC)]
    s_arr = np.array([t.timestamp() for t in s_all])
    print(f"   Back posts in the four venues inside the period: {len(ov)} (all randombit; bitcointalk and")
    print("   bitcoin-dev activity starts 2013)")
    for e in ov:
        h = e["t"].hour + e["t"].minute / 60
        gap = np.min(np.abs(s_arr - e["t"].timestamp())) / 3600
        flag = "  <-- in Satoshi quiet window 06-14 UTC" if 6 <= h < 14 else ""
        print(f"     {e['t']:%Y-%m-%d %H:%M}Z  nearest Satoshi item {gap:6.1f} h away{flag}")
    print("   Back's own emails to Satoshi (COPA exhibit AB1, before the period):")
    for t in copa:
        gap = np.min(np.abs(s_arr - t.timestamp())) / 60
        print(f"     {t:%Y-%m-%d %H:%M:%S}Z  nearest Satoshi item {gap:6.1f} min away"
              f"{'  <-- in Satoshi quiet window' if 6 <= t.hour < 14 else ''}")
    pairs = []
    for e in ov:
        i = int(np.argmin(np.abs(s_arr - e["t"].timestamp())))
        pairs.append((abs(s_arr[i] - e["t"].timestamp()) / 60, e["t"], s_all[i]))
    pairs.sort()
    print("   closest Back-post / Satoshi-item pairs during the period:")
    for g, b, s in pairs[:5]:
        print(f"     Back {b:%Y-%m-%d %H:%M}Z  Satoshi {s:%Y-%m-%d %H:%M}Z  gap {g:.0f} min")
    print()
    print("Caveat: a single person can keep a pseudonym to chosen hours (e.g. evenings) and post under")
    print("his own name at other times, so a rhythm mismatch is weak evidence against identity, and a")
    print("match would be weak evidence for it.")


if __name__ == "__main__":
    main()
