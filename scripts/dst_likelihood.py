#!/usr/bin/env python3
"""Which civil time zone best explains Satoshi's daily rhythm, including DST?

For each candidate zone we convert every timed Satoshi event (UTC) to that
zone's *local civil time* (with its own DST rules), fit a circular kernel
density of local hour-of-day, and compute the leave-one-out log-likelihood of
all events. A person's routine is anchored to local clock time, so the zone
whose DST rules line up the activity pattern across clock changes should score
highest.

Zones that differ by a constant offset all year (e.g. Europe/London vs
America/New_York outside the spring/autumn gaps) give identical densities up
to a shift, so their likelihood difference comes only from events in the weeks
when one region has changed clocks and the other hasn't. Fixed UTC differs from
DST zones for the whole summer.

We also report a permutation-style check: how many events fall in the "gap"
windows, and the per-window contribution.

Input: data/satoshi/posts.jsonl
"""
import datetime as dt
import json
import math
import sys
from zoneinfo import ZoneInfo

ZONES = ["UTC", "Europe/London", "Europe/Lisbon", "Europe/Paris", "America/New_York",
         "America/Chicago", "America/Denver", "America/Los_Angeles", "Asia/Tokyo", "Australia/Sydney"]
SOURCES = {"forum", "svn_commit", "email", "mailing_list"}
BW = 0.9  # kernel bandwidth in hours (von Mises-like Gaussian on circle)


def load(path):
    ev = []
    for l in open(path):
        r = json.loads(l)
        if r.get("source_type") not in SOURCES:
            continue
        if r.get("timestamp_precision") not in ("second", "minute"):
            continue
        if r.get("timezone_basis") in ("assumed", "unknown", "none"):
            continue
        if not r.get("timestamp_utc"):
            continue
        t = dt.datetime.strptime(r["timestamp_utc"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=dt.timezone.utc)
        if t.year < 2008 or t > dt.datetime(2011, 5, 1, tzinfo=dt.timezone.utc):
            continue
        ev.append(t)
    return sorted(set(ev))


def circ_kernel(d):
    # wrapped Gaussian on a 24 h circle
    s = 0.0
    for k in (-24, 0, 24):
        s += math.exp(-0.5 * ((d + k) / BW) ** 2)
    return s / (BW * math.sqrt(2 * math.pi))


def loo_ll(hours):
    n = len(hours)
    total = 0.0
    for i, h in enumerate(hours):
        dens = sum(circ_kernel(h - hj) for j, hj in enumerate(hours) if j != i) / (n - 1)
        total += math.log(max(dens, 1e-9))
    return total


def local_hours(events, zone):
    z = ZoneInfo(zone)
    out = []
    for t in events:
        lt = t.astimezone(z)
        out.append(lt.hour + lt.minute / 60 + lt.second / 3600)
    return out


def gap_events(events):
    """Events that fall in periods where UK and US Eastern DST status differ."""
    L, N = ZoneInfo("Europe/London"), ZoneInfo("America/New_York")
    return [t for t in events if bool(t.astimezone(L).dst()) != bool(t.astimezone(N).dst())]


def main(path="data/satoshi/posts.jsonl"):
    ev = load(path)
    print(f"events used: {len(ev)} ({ev[0]:%Y-%m-%d} .. {ev[-1]:%Y-%m-%d}); kernel bw={BW} h")
    res = {}
    for z in ZONES:
        res[z] = loo_ll(local_hours(ev, z))
    base = res["Europe/London"]
    for z, v in sorted(res.items(), key=lambda kv: -kv[1]):
        print(f"  {z:22s} LOO log-lik = {v:9.2f}   (vs London {v - base:+7.2f})")
    g = gap_events(ev)
    print(f"\nevents in UK/US-Eastern DST-mismatch windows: {len(g)}")
    for t in g:
        print(f"   {t:%Y-%m-%d %H:%M}Z")
    # Contribution of gap events alone: compare each gap event's LOO density under both zones
    for za, zb in (("Europe/London", "America/New_York"), ("Europe/London", "UTC")):
        ha, hb = local_hours(ev, za), local_hours(ev, zb)
        idx = [i for i, t in enumerate(ev) if (t in g)] if zb == "America/New_York" else range(len(ev))
        s = 0.0
        for i in idx:
            da = sum(circ_kernel(ha[i] - ha[j]) for j in range(len(ev)) if j != i) / (len(ev) - 1)
            db = sum(circ_kernel(hb[i] - hb[j]) for j in range(len(ev)) if j != i) / (len(ev) - 1)
            s += math.log(da) - math.log(db)
        print(f"log-lik ratio {za} vs {zb} over {len(list(idx))} discriminating events: {s:+.2f}")


if __name__ == "__main__":
    main(*sys.argv[1:])
