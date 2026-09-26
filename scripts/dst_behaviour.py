#!/usr/bin/env python3
"""Did Satoshi's daily routine shift on EU or on US daylight-saving dates?

A person's routine is anchored to their *local* clock, so their activity,
measured in UTC, jumps by one hour when their local clocks change. The EU/UK
and the US change on different dates (1-3 weeks apart), which gives a natural
experiment:

  - UK/EU resident: the UTC activity pattern shifts on the EU dates only
  - US resident:    it shifts on the US dates only

Method: for each transition we take a window before the first switch, the gap
between the two switches, and a window after the second. For each day with
activity we find the longest quiet gap (the "night") and record when it
starts ("bedtime", last event before the gap) and ends ("wake", first event
after). We compare the medians across the three windows. The night is
located by looking for the largest gap in a 24 h period that starts at
12:00 UTC (Satoshi was rarely active 05:00-11:00 UTC, so this avoids cutting
nights in half).

Input: data/satoshi/posts.jsonl (only items with minute/second precision,
from forum/svn/email/mailing list sources).
"""
import datetime as dt
import json
import statistics
import sys
from collections import defaultdict

EU = {2009: (dt.date(2009, 3, 29), dt.date(2009, 10, 25)), 2010: (dt.date(2010, 3, 28), dt.date(2010, 10, 31))}
US = {2009: (dt.date(2009, 3, 8), dt.date(2009, 11, 1)), 2010: (dt.date(2010, 3, 14), dt.date(2010, 11, 7))}
SOURCES = {"forum", "svn_commit", "email", "mailing_list", "p2pfoundation"}


def load(path):
    out = []
    for line in open(path):
        r = json.loads(line)
        if r.get("source_type") not in SOURCES:
            continue
        if r.get("timestamp_precision") not in ("second", "minute"):
            continue
        ts = r.get("timestamp_utc")
        if not ts:
            continue
        out.append(dt.datetime.strptime(ts, "%Y-%m-%dT%H:%M:%SZ"))
    return sorted(set(out))


def nights(times):
    """Group events into 'days' that run 12:00 UTC -> 12:00 UTC and find the
    largest gap in each. Returns {day_label: (bed_utc_hours, wake_utc_hours, gap_h)}."""
    by = defaultdict(list)
    for t in times:
        anchor = (t - dt.timedelta(hours=12)).date()  # day containing the night
        by[anchor].append(t)
    res = {}
    for d, ev in by.items():
        ev.sort()
        start = dt.datetime.combine(d, dt.time(12))
        pts = [start] + ev + [start + dt.timedelta(hours=24)]
        best = max(range(len(pts) - 1), key=lambda i: pts[i + 1] - pts[i])
        a, b = pts[best], pts[best + 1]
        gap = (b - a).total_seconds() / 3600
        if gap < 4 or len(ev) < 2:
            continue
        # express times as hours after 12:00 UTC of the anchor day (so 01:00 next day = 13)
        res[d] = ((a - start).total_seconds() / 3600, (b - start).total_seconds() / 3600, gap)
    return res


def fmt(h):
    h = (h + 12) % 24
    return f"{int(h):02d}:{int(round((h % 1) * 60)) % 60:02d}"


def window_stats(nts, lo, hi):
    sel = [v for d, v in nts.items() if lo <= d < hi]
    if not sel:
        return None
    bed = statistics.median(v[0] for v in sel)
    wake = statistics.median(v[1] for v in sel)
    return len(sel), bed, wake


def main(path="data/satoshi/posts.jsonl", pad=21):
    times = load(path)
    nts = nights(times)
    print(f"events: {len(times)}  nights detected: {len(nts)}\n")
    for year in (2009, 2010):
        for idx, season in ((0, "spring"), (1, "autumn")):
            eu, us = EU[year][idx], US[year][idx]
            first, second = min(eu, us), max(eu, us)
            first_who = "US" if first == us else "EU"
            wins = [("before both", first - dt.timedelta(days=pad), first),
                    (f"between ({first_who} switched only)", first, second),
                    ("after both", second, second + dt.timedelta(days=pad))]
            print(f"== {year} {season}: EU {eu}, US {us}")
            for name, lo, hi in wins:
                s = window_stats(nts, lo, hi)
                if s:
                    n, bed, wake = s
                    print(f"   {name:34s} {lo}..{hi - dt.timedelta(days=1)}  n={n:2d}  median bedtime {fmt(bed)} UTC  median wake {fmt(wake)} UTC")
                else:
                    print(f"   {name:34s} {lo}..{hi - dt.timedelta(days=1)}  n= 0")
            print()
    # Seasonal comparison (summer vs winter), with a UK-time and a US-Eastern-time view
    def season_of(d, rules):
        y = d.year
        if y not in rules:
            return None
        return "summer" if rules[y][0] <= d < rules[y][1] else "winter"
    for label, rules in (("EU rules", EU), ("US rules", US)):
        by = defaultdict(list)
        for d, v in nts.items():
            s = season_of(d, rules)
            if s:
                by[s].append(v)
        line = []
        for s in ("summer", "winter"):
            if by[s]:
                line.append(f"{s}: n={len(by[s])} bed {fmt(statistics.median(v[0] for v in by[s]))} wake {fmt(statistics.median(v[1] for v in by[s]))} UTC")
        print(f"Seasonal split by {label}: " + " | ".join(line))


if __name__ == "__main__":
    main(*sys.argv[1:])
