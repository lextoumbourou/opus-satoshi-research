#!/usr/bin/env python3
"""Robustness checks for the DST-rule likelihood result.

1. Bandwidth sensitivity: London vs New York vs UTC log-lik across bandwidths.
2. Placebo rules: synthetic zones with a +1 h summer offset whose spring and
   autumn switch dates are moved by k weeks relative to the EU rule
   (k_spring, k_autumn in -6..+6). If Satoshi's routine followed EU clocks, the
   likelihood surface should peak near (0, 0). The US rule corresponds to
   roughly (-3, +1) weeks in 2009 and (-2, +1) weeks in 2010.
Only the relative shape matters (a constant offset doesn't change the KDE).
"""
import datetime as dt
import math
import sys

sys.path.insert(0, "scripts")
from dst_likelihood import load, circ_kernel, loo_ll, local_hours  # noqa: E402
import dst_likelihood as D  # noqa: E402

EU = {2008: (dt.date(2008, 3, 30), dt.date(2008, 10, 26)), 2009: (dt.date(2009, 3, 29), dt.date(2009, 10, 25)),
      2010: (dt.date(2010, 3, 28), dt.date(2010, 10, 31)), 2011: (dt.date(2011, 3, 27), dt.date(2011, 10, 30))}


def synth_hours(events, ks, ka):
    out = []
    for t in events:
        s, a = EU[t.year]
        s = s + dt.timedelta(weeks=ks)
        a = a + dt.timedelta(weeks=ka)
        # switch at 01:00 UTC on those dates
        st = dt.datetime.combine(s, dt.time(1), tzinfo=dt.timezone.utc)
        at = dt.datetime.combine(a, dt.time(1), tzinfo=dt.timezone.utc)
        off = 1 if st <= t < at else 0
        lt = t + dt.timedelta(hours=off)
        out.append(lt.hour + lt.minute / 60 + lt.second / 3600)
    return out


def main():
    ev = load("data/satoshi/posts.jsonl")
    print("1) bandwidth sensitivity (LOO log-lik relative to Europe/London)")
    for bw in (0.4, 0.6, 0.9, 1.3, 2.0):
        D.BW = bw
        l = loo_ll(local_hours(ev, "Europe/London"))
        n = loo_ll(local_hours(ev, "America/New_York"))
        u = loo_ll(local_hours(ev, "UTC"))
        print(f"   bw={bw:.1f}h  NewYork-London={n - l:+6.2f}  UTC-London={u - l:+6.2f}")
    D.BW = 0.9
    print("\n2) placebo grid: log-lik of +1h-summer rule with EU switch dates shifted (weeks), relative to EU rule")
    base = loo_ll(synth_hours(ev, 0, 0))
    ks_range = range(-6, 7)
    header = "   ks\\ka " + " ".join(f"{ka:+3d}" for ka in ks_range)
    print(header)
    best = (None, -1e9)
    for ks in ks_range:
        row = []
        for ka in ks_range:
            v = loo_ll(synth_hours(ev, ks, ka)) - base
            row.append(v)
            if v > best[1]:
                best = ((ks, ka), v)
        print(f"   {ks:+3d}    " + " ".join(f"{v:+5.1f}"[:5].rjust(5) for v in row))
    print(f"   best shift (spring, autumn weeks) = {best[0]}, delta = {best[1]:+.2f}")


if __name__ == "__main__":
    main()
