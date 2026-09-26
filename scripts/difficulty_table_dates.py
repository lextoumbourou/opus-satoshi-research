#!/usr/bin/env python3
"""Compare Satoshi's own date labels in his difficulty table (bitcointalk
msg249, updated through Aug 2010) with the UTC timestamps of the retarget
blocks, and test which calendar (UTC, UK civil, US Eastern, US Pacific, CET)
reproduces every label."""
import json, re, time, urllib.request, datetime as dt
from zoneinfo import ZoneInfo
def get(u):
    for i in range(4):
        try: return urllib.request.urlopen(urllib.request.Request(u, headers={'User-Agent': 'research'}), timeout=60).read().decode()
        except Exception: time.sleep(3 * (i + 1))
    raise SystemExit('fetch failed ' + u)
text = next(json.loads(l)['text'] for l in open('data/satoshi/posts.jsonl') if json.loads(l)['id'] == 'bitcointalk-msg249')
labels = sorted({dt.datetime.strptime(m, '%d/%m/%Y').date() for m in re.findall(r'\b(\d{2}/\d{2}/20\d{2})\b', text)})
print('labels in table:', [d.isoformat() for d in labels])
retargets = []
cache = 'data/blockchain/retargets.json'
try: retargets = json.load(open(cache))
except Exception: pass
have = {r['height'] for r in retargets}
h = 32256
while h <= 84672:
    if h not in have:
        bh = get(f'https://blockstream.info/api/block-height/{h}').strip()
        b = json.loads(get(f'https://blockstream.info/api/block/{bh}'))
        retargets.append({'height': h, 'hash': bh, 'timestamp': b['timestamp'], 'bits': b['bits']}); time.sleep(0.5)
    h += 2016
retargets.sort(key=lambda r: r['height']); json.dump(retargets, open(cache, 'w'), indent=1)
zones = {'UTC': dt.timezone.utc, 'Europe/London': ZoneInfo('Europe/London'), 'Europe/Paris (CET)': ZoneInfo('Europe/Paris'),
         'America/New_York': ZoneInfo('America/New_York'), 'America/Chicago': ZoneInfo('America/Chicago'), 'America/Los_Angeles': ZoneInfo('America/Los_Angeles')}
print(f"\n{'height':>6} {'UTC time':19s} " + ' '.join(f'{z[:12]:>12s}' for z in zones))
score = {z: [0, 0] for z in zones}
for r in retargets:
    t = dt.datetime.fromtimestamp(r['timestamp'], dt.timezone.utc)
    row = []
    for z, tz in zones.items():
        d = t.astimezone(tz).date()
        ok = d in labels
        near = any(abs((d - L).days) <= 1 for L in labels)
        if near:
            score[z][1] += 1; score[z][0] += ok
        row.append(f"{d.strftime('%d/%m')}{'*' if ok else ' '}".rjust(12))
    print(f"{r['height']:>6} {t:%Y-%m-%d %H:%M:%S} " + ' '.join(row))
print('\n(* = matches one of Satoshi\'s labels)')
for z, (ok, n) in score.items(): print(f'  {z:20s} matches {ok}/{n} relevant retargets')
