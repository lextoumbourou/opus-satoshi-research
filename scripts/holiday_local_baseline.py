#!/usr/bin/env python3
"""Holiday activity vs a LOCAL baseline: for each holiday, the share of days
active within +/-10 days (excluding the holiday itself). P(inactive by chance)
= 1 - that share. Combined probability for a set of holidays = product."""
import json, datetime as dt, collections
from zoneinfo import ZoneInfo
import importlib.util, sys
spec = importlib.util.spec_from_file_location('h', 'scripts/holiday_activity.py')
ev = []
for l in open('data/satoshi/posts.jsonl'):
    r = json.loads(l)
    if r.get('source_type') in ('forum', 'svn_commit', 'email', 'mailing_list') and r.get('timestamp_utc') and r.get('timestamp_precision') in ('second', 'minute'):
        ev.append(dt.datetime.strptime(r['timestamp_utc'], '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=dt.timezone.utc))
HOL = {
 'US': ('America/New_York', {'Thanksgiving 2009': (2009,11,26), 'MLK Day 2010': (2010,1,18), "Presidents' Day 2010": (2010,2,15), 'Independence Day 2010': (2010,7,4), 'Independence Day (obs)': (2010,7,5), 'Labor Day 2010': (2010,9,6), 'Columbus Day 2010': (2010,10,11), 'Veterans Day 2010': (2010,11,11), 'Thanksgiving 2010': (2010,11,25)}),
 'UK': ('Europe/London', {'Boxing Day (obs) 2009': (2009,12,28), 'Good Friday 2010': (2010,4,2), 'Easter Monday 2010': (2010,4,5), 'Early May BH 2010': (2010,5,3), 'Summer BH 2010 (Eng/Wal)': (2010,8,30)}),
}
for k, (tzn, hol) in HOL.items():
    tz = ZoneInfo(tzn); c = collections.Counter(t.astimezone(tz).date() for t in ev)
    print(f'== {k}-only holidays ({tzn} dates)'); p_all_inactive = 1.0; n_inactive = 0
    for name, ymd in hol.items():
        d = dt.date(*ymd)
        win = [d + dt.timedelta(i) for i in range(-10, 11) if i != 0]
        share = sum(1 for x in win if c[x] > 0) / len(win)
        near = ' '.join(f"{(d + dt.timedelta(i)).strftime('%d')}:{c[d + dt.timedelta(i)]}" for i in range(-3, 4))
        print(f'   {name:26s} {d} {d:%a} events={c[d]}  active share +/-10d={share:.0%}  P(inactive|chance)={1 - share:.2f}  [{near}]')
        if c[d] == 0: p_all_inactive *= (1 - share); n_inactive += 1
    print(f'   inactive on {n_inactive}/{len(hol)}; product of chance probabilities for the inactive ones = {p_all_inactive:.4f}')
