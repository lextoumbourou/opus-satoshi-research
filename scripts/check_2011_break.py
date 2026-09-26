#!/usr/bin/env python3
"""Is Satoshi's 2011 time-of-day pattern different from 2008-2010, and does the
answer depend on the assumed display time zone of Mike Hearn's email dumps?

1. Base rhythm: all timed Satoshi items (second/minute precision) 2008-11 .. 2010-12
   whose UTC time is explicit or verified (timezone_basis not assumed/inferred).
2. Quiet window chosen from the base data alone (the 8-hour circular window with
   the fewest base events), then a binomial test for the 2011 items.
3. A permutation test that doesn't need a window: mean log-density of the 2011
   items under the base KDE vs 100k random draws of the same size from the base.
4. Hearn display-zone calibration: Satoshi's 2009-2010 emails to Hearn appear in
   the same Gmail forwards with naive display times. For display offsets
   -12..+12 h, score their UTC times under the base KDE (which excludes them).
5. 2008-2010 daytime (07-15 UTC) events listed with weekday, to see whether
   daytime activity clusters on weekends/holidays.
"""
import datetime as dt
import json
import math
import random
import re
import sys

sys.path.insert(0, "scripts")
import dst_likelihood as D  # noqa: E402

D.BW = 0.9
rows = [json.loads(l) for l in open("data/satoshi/posts.jsonl")]
TIMED = ("second", "minute")


def t_utc(r):
    return dt.datetime.strptime(r["timestamp_utc"], "%Y-%m-%dT%H:%M:%SZ")


def hour(t):
    return t.hour + t.minute / 60 + t.second / 3600


def dens(h, base):
    return sum(D.circ_kernel(h - b) for b in base) / len(base)


def parse_gmail(raw):
    # "Fri, Jan 7, 2011 at 1:00 PM"
    return dt.datetime.strptime(raw.split(", ", 1)[1], "%b %d, %Y at %I:%M %p")


base_rows = [r for r in rows if r.get("timestamp_utc") and r.get("timestamp_precision") in TIMED
             and r.get("timezone_basis") not in ("assumed", "inferred", "unknown", "none")
             and "2008-01-01" <= r["timestamp_utc"] < "2011-01-01"]
base_ts = sorted({t_utc(r) for r in base_rows})
base = [hour(t) for t in base_ts]
y2011 = [r for r in rows if r.get("timestamp_utc") and r.get("timestamp_precision") in TIMED
         and "2011-01-01" <= r["timestamp_utc"] < "2011-05-01"]
print(f"base events (explicit/verified UTC, 2008-2010): {len(base)}")
print(f"2011 items (Jan-Apr, any basis): {len(y2011)}")

# 2. quiet window from base only
best = None
for start10 in range(0, 240):
    s = start10 / 10
    n = sum(1 for h in base if (h - s) % 24 < 8)
    if best is None or n < best[1]:
        best = (s, n)
s, n = best
p0 = n / len(base)
k = sum(1 for r in y2011 if (hour(t_utc(r)) - s) % 24 < 8)
pb = sum(math.comb(len(y2011), j) * p0**j * (1 - p0)**(len(y2011) - j) for j in range(k, len(y2011) + 1))
print(f"\nquietest 8h window in base: {s:04.1f}-{(s + 8) % 24:04.1f} UTC holds {n}/{len(base)} ({100 * p0:.1f}%)")
print(f"2011 items in that window: {k}/{len(y2011)}; binomial P(>= {k}) = {pb:.2e}")
for r in y2011:
    t = t_utc(r)
    flag = "IN " if (hour(t) - s) % 24 < 8 else "   "
    print(f"   {flag}{t:%Y-%m-%d %a %H:%M}Z  {r.get('correspondent') or r.get('recipient')}  basis={r.get('timezone_basis')}")

# 3. permutation test on mean log density
ld = lambda hs: sum(math.log(max(dens(h, base), 1e-9)) for h in hs) / len(hs)
obs = ld([hour(t_utc(r)) for r in y2011])
random.seed(1)
m = len(y2011)
# leave-one-out densities for base events so draws aren't favoured by self-inclusion
loo = []
for i, h in enumerate(base):
    d = (sum(D.circ_kernel(h - b) for b in base) - D.circ_kernel(0)) / (len(base) - 1)
    loo.append(math.log(max(d, 1e-9)))
N = 100000
le = sum(1 for _ in range(N) if sum(random.sample(loo, m)) / m <= obs)
print(f"\nmean log-density of 2011 items under base KDE = {obs:.3f}; random {m}-draws from base as low or lower: {le}/{N} (p = {le / N:.1e})")
explicit11 = [r for r in y2011 if r.get("timezone_basis") not in ("assumed", "inferred")]
print(f"   (2011 items with explicit zone only: {len(explicit11)}; mean log-density {ld([hour(t_utc(r)) for r in explicit11]):.3f})")

# 4. Hearn display-zone calibration
hearn = [r for r in rows if (r.get("correspondent") or r.get("recipient") or "").startswith("Mike Hearn")
         and r.get("timestamp_raw") and " at " in r["timestamp_raw"]]
cal = [r for r in hearn if r["timestamp_raw"] and parse_gmail(r["timestamp_raw"]).year < 2011]
print(f"\nHearn-thread Satoshi items: {len(hearn)} (calibration set pre-2011: {len(cal)})")
res = []
for off in range(-12, 13):
    hs = [hour(parse_gmail(r["timestamp_raw"]) - dt.timedelta(hours=off)) for r in cal]
    res.append((off, ld(hs)))
bestoff = max(res, key=lambda x: x[1])
for off, v in res:
    bar = "#" * max(0, int((v + 6) * 6))
    print(f"   display UTC{off:+3d}: mean log-dens {v:7.3f} {bar}{'  <- best' if off == bestoff[0] else ''}")
ok = [off for off, v in res if v >= bestoff[1] - 0.5]
print(f"   offsets within 0.5 of best: {ok}")
print("   2011 Hearn items under those offsets (UTC hours):")
for r in hearn:
    lt = parse_gmail(r["timestamp_raw"])
    if lt.year < 2011:
        continue
    print(f"     {r['timestamp_raw']:32s} -> " + ", ".join(f"{(lt - dt.timedelta(hours=o)):%H:%M}" for o in ok))

# 5. base daytime events
print("\n2008-2010 base events between 07:00 and 15:00 UTC:")
for t in base_ts:
    if 7 <= hour(t) < 15:
        print(f"   {t:%Y-%m-%d %a %H:%M}Z")
