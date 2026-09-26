#!/usr/bin/env python3
"""Compare UTC hour-of-day activity of Satoshi (corpus) with a candidate's
dated posts (JSON list with 'date_header' fields, e.g. mail-archive scrape)."""
import json, email.utils, collections, datetime as dt, sys
cand_path = sys.argv[1] if len(sys.argv) > 1 else "data/lists/randombit/back-randombit.json"
label = sys.argv[2] if len(sys.argv) > 2 else "Back (randombit)"
bh = collections.Counter()
for x in json.load(open(cand_path)):
    try:
        d = email.utils.parsedate_to_datetime(x.get("date_header")).astimezone(dt.timezone.utc)
    except Exception:
        continue
    bh[d.hour] += 1
sh = collections.Counter()
for l in open("data/satoshi/posts.jsonl"):
    r = json.loads(l)
    if r.get("source_type") in ("forum", "svn_commit", "email", "mailing_list") and r.get("timestamp_utc") and r.get("timestamp_precision") in ("second", "minute"):
        sh[int(r["timestamp_utc"][11:13])] += 1
bt, st = sum(bh.values()), sum(sh.values())
print(f"UTC hour | Satoshi % (n={st})          | {label} % (n={bt})")
for h in range(24):
    s, b = 100 * sh[h] / st, 100 * bh[h] / bt
    print(f"  {h:02d}  {s:5.1f} {'#' * int(s):<14} | {b:5.1f} {'#' * int(b)}")
dead = range(5, 11)
print(f"share in 05:00-10:59 UTC: Satoshi {100 * sum(sh[h] for h in dead) / st:.1f}%, {label} {100 * sum(bh[h] for h in dead) / bt:.1f}%")
