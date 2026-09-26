#!/usr/bin/env python3
"""Patoshi miner downtime: find gaps between consecutive Patoshi blocks
(leeschmalz list, extraNonce-derived) longer than a threshold, and report the
UTC hour distribution of gap starts/ends, plus a per-month summary."""
import csv, datetime as dt, collections, sys
TH = float(sys.argv[1]) if len(sys.argv) > 1 else 2.0  # hours
pat = set(int(x) for x in open('data/blockchain/patoshi/patoshi_heights.txt').read().split())
hdr = {int(r['height']): int(r['ntime']) for r in csv.DictReader(open('data/blockchain/headers_0_60479.csv'))}
ts = sorted((hdr[h], h) for h in pat if h in hdr)
print(f'Patoshi blocks: {len(ts)}  heights {min(pat)}..{max(pat)}  time {dt.datetime.utcfromtimestamp(ts[0][0]):%Y-%m-%d}..{dt.datetime.utcfromtimestamp(ts[-1][0]):%Y-%m-%d}')
gaps = []
for (t0, h0), (t1, h1) in zip(ts, ts[1:]):
    g = (t1 - t0) / 3600
    if g >= TH: gaps.append((t0, t1, g, h0, h1))
print(f'gaps >= {TH} h: {len(gaps)}')
st = collections.Counter(dt.datetime.utcfromtimestamp(a).hour for a, b, g, *_ in gaps if g < 24)
en = collections.Counter(dt.datetime.utcfromtimestamp(b).hour for a, b, g, *_ in gaps if g < 24)
print('UTC hour | gap starts (<24h gaps) | gap ends')
for h in range(24): print(f'  {h:02d}  {st[h]:4d} {"#"*st[h]:<30s} | {en[h]:4d} {"#"*en[h]}')
bym = collections.Counter(dt.datetime.utcfromtimestamp(a).strftime('%Y-%m') for a, *_ in gaps)
blocks_m = collections.Counter(dt.datetime.utcfromtimestamp(t).strftime('%Y-%m') for t, h in ts)
print('month  patoshi_blocks  gaps>=TH')
for m in sorted(blocks_m): print(f'  {m}  {blocks_m[m]:6d}  {bym[m]:4d}')
