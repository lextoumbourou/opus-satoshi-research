#!/usr/bin/env python3
"""Satoshi's activity on US-only vs UK-only public holidays (2009-11 .. 2010-12,
the period with dense forum/SVN/email data), compared with his typical
activity on the same weekday. Days are evaluated in each country's local
civil date. Also adds release-build events (PE link / zip pack times)."""
import json, datetime as dt, collections, statistics
from zoneinfo import ZoneInfo
ev = []
for l in open('data/satoshi/posts.jsonl'):
    r = json.loads(l)
    if r.get('source_type') in ('forum', 'svn_commit', 'email', 'mailing_list') and r.get('timestamp_utc') and r.get('timestamp_precision') in ('second', 'minute'):
        ev.append(dt.datetime.strptime(r['timestamp_utc'], '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=dt.timezone.utc))
start, end = dt.date(2009, 11, 22), dt.date(2010, 12, 13)
US_ONLY = {'Thanksgiving 2009': dt.date(2009, 11, 26), 'MLK Day 2010': dt.date(2010, 1, 18), "Presidents' Day 2010": dt.date(2010, 2, 15),
           'Independence Day 2010': dt.date(2010, 7, 4), 'Independence Day (obs) 2010': dt.date(2010, 7, 5), 'Labor Day 2010': dt.date(2010, 9, 6),
           'Columbus Day 2010': dt.date(2010, 10, 11), 'Veterans Day 2010': dt.date(2010, 11, 11), 'Thanksgiving 2010': dt.date(2010, 11, 25)}
UK_ONLY = {'Boxing Day (obs) 2009': dt.date(2009, 12, 28), 'Easter Monday 2010': dt.date(2010, 4, 5), 'Early May BH 2010': dt.date(2010, 5, 3),
           'Summer BH 2010': dt.date(2010, 8, 30), 'Good Friday 2010': dt.date(2010, 4, 2)}
BOTH = {'Christmas 2009': dt.date(2009, 12, 25), "New Year's Day 2010": dt.date(2010, 1, 1), 'Memorial Day / Spring BH 2010': dt.date(2010, 5, 31)}
def counts(tzname):
    tz = ZoneInfo(tzname); c = collections.Counter(t.astimezone(tz).date() for t in ev); return c
for label, hol, tzname in (('US-only holidays (US Eastern dates)', US_ONLY, 'America/New_York'), ('UK-only holidays (UK dates)', UK_ONLY, 'Europe/London'), ('Shared holidays (UK dates)', BOTH, 'Europe/London')):
    c = counts(tzname)
    days = [start + dt.timedelta(d) for d in range((end - start).days + 1)]
    wk = collections.defaultdict(list)
    for d in days: wk[d.weekday()].append(c[d])
    print(f'== {label}')
    tot_obs = tot_exp = 0
    for name, d in hol.items():
        if not (start <= d <= end): continue
        exp = statistics.mean(wk[d.weekday()]); active_frac = sum(1 for x in wk[d.weekday()] if x > 0) / len(wk[d.weekday()])
        tot_obs += c[d]; tot_exp += exp
        print(f'   {name:30s} {d} ({d:%a})  events={c[d]:3d}  typical {d:%a} mean={exp:4.1f}, active on {active_frac:.0%} of {d:%a}s')
    print(f'   TOTAL observed={tot_obs} expected~{tot_exp:.1f}  ratio={tot_obs / tot_exp:.2f}')
