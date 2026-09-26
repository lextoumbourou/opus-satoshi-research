#!/usr/bin/env python3
"""From Info-ZIP local headers (UT extra with mtime/atime/ctime), report for
each release: the top package folder's creation time, the earliest creation
time of any entry, and the packing time (max atime). Times are UTC."""
import zipfile, struct, datetime as dt, sys, re
def ut_local(f, info):
    f.seek(info.header_offset); h = f.read(30); n, e = struct.unpack_from('<HH', h, 26); f.read(n); ex = f.read(e)
    j = 0
    while j + 4 <= len(ex):
        hid, ln = struct.unpack_from('<HH', ex, j); d = ex[j + 4:j + 4 + ln]
        if hid == 0x5455:
            flags = d[0]; vals = [struct.unpack_from('<I', d, 1 + 4 * k)[0] for k in range((ln - 1) // 4)]
            keys = [k for k, b in (('m', 1), ('a', 2), ('c', 4)) if flags & b]
            return {k: dt.datetime.fromtimestamp(v, dt.timezone.utc).replace(tzinfo=None) for k, v in zip(keys, vals)}
        j += 4 + ln
    return {}
def vkey(p):
    m = re.search(r'bitcoin-([\d.]+)-win', p); return tuple(int(x) for x in m.group(1).split('.'))
for p in sorted(sys.argv[1:], key=vkey):
    z = zipfile.ZipFile(p); f = open(p, 'rb'); top = None; cmin = None; amax = None
    for i in z.infolist():
        t = ut_local(f, i)
        if not t: continue
        if i.filename.count('/') == 1 and i.filename.endswith('/'): top = t.get('c')
        if 'c' in t: cmin = min(cmin, t['c']) if cmin else t['c']
        if 'a' in t: amax = max(amax, t['a']) if amax else t['a']
    print(f"{p.split('/')[-1]:26s} top-folder ctime={top}  earliest ctime={cmin}  packed(max atime)={amax}")
