#!/usr/bin/env python3
"""Classify cryptography-list posters (metzdowd 2008-01..2010-10, randombit
2010-11..2011-06) by the time-zone rule their mail clients' Date headers follow.
UK-rule = +0000 in winter AND +0100 in summer (EU DST dates), with at least one
of each. Reports counts per rule; names are NOT printed except for a supplied
list of already-public figures."""
import gzip, os, re, sys, collections, email.utils, datetime as dt
from zoneinfo import ZoneInfo
L = ZoneInfo('Europe/London')
def msgs(path):
    op = gzip.open if path.endswith('.gz') else open
    data = op(path, 'rb').read().decode('latin-1')
    for chunk in re.split(r'\n(?=From \S+ +(?:at \S+ +)?\w{3} \w{3} +\d+ [\d:]+ \d{4})', '\n' + data):
        hdr = chunk.split('\n\n', 1)[0]
        f = re.search(r'^From: (.*)', hdr, re.M); d = re.search(r'^Date: (.*)', hdr, re.M)
        if f and d: yield f.group(1), d.group(1)
files = [os.path.join('data/lists/metzdowd', x) for x in os.listdir('data/lists/metzdowd') if re.match(r'(2008|2009|2010)-', x)]
files += [os.path.join('data/lists/randombit/pipermail', x) for x in os.listdir('data/lists/randombit/pipermail')]
per = collections.defaultdict(lambda: {'s': collections.Counter(), 'w': collections.Counter(), 'n': 0})
for p in files:
    for frm, date in msgs(p):
        m = re.search(r'([+-]\d{4})\s*(\(|$)', date.strip())
        try: t = email.utils.parsedate_to_datetime(date)
        except Exception: continue
        if not m or t.tzinfo is None: continue
        who = re.sub(r'\s+', ' ', frm.lower()).strip()
        summer = bool(t.astimezone(L).dst())
        per[who]['s' if summer else 'w'][m.group(1)] += 1; per[who]['n'] += 1
def rule(v):
    s, w = set(v['s']), set(v['w'])
    if not s or not w: return 'one-season-only'
    if s == {'+0100'} and w == {'+0000'}: return 'UK/IE/PT rule (+0/+1)'
    if s == {'+0200'} and w == {'+0100'}: return 'CET/CEST (+1/+2)'
    if s == {'-0400'} and w == {'-0500'}: return 'US/CA Eastern'
    if s == {'-0700'} and w == {'-0800'}: return 'US/CA Pacific'
    if s == {'-0500'} and w == {'-0600'}: return 'US Central'
    if s == {'+0000'} and w == {'+0000'}: return 'UTC fixed'
    if len(s | w) == 1: return 'fixed ' + next(iter(s | w))
    return 'mixed/other'
act = {k: v for k, v in per.items() if v['n'] >= 5}
c = collections.Counter(rule(v) for v in act.values())
print(f'posters with >=5 dated posts 2008-2011: {len(act)}')
for k, n in c.most_common(): print(f'  {k:28s} {n:4d}  ({100*n/len(act):.0f}%)')
PUBLIC = [x.lower() for x in sys.argv[1:]]
for who, v in sorted(act.items()):
    if any(p in who for p in PUBLIC):
        print(f"  [public figure] {who[:60]}: {rule(v)}  summer={dict(v['s'])} winter={dict(v['w'])}")
