#!/usr/bin/env python3
"""Summarise gzip + tar header metadata of release tarballs: gzip mtime/OS,
tar format, owner uname/gname/uid/gid, most common file mtimes (UTC)."""
import tarfile, glob, datetime as dt, struct, collections, re, sys
def vkey(p):
    m = re.search(r'bitcoin-([\d.]+)', p)
    return tuple(int(x) for x in m.group(1).strip('.').split('.')) if m else ()
for p in sorted(sys.argv[1:], key=vkey):
    raw = open(p, 'rb').read(10); mt = struct.unpack('<I', raw[4:8])[0]; osb = raw[9]
    t = tarfile.open(p); ms = t.getmembers()
    owners = collections.Counter((m.uname, m.gname, m.uid, m.gid) for m in ms)
    fmt = {tarfile.USTAR_FORMAT: 'ustar', tarfile.GNU_FORMAT: 'gnu', tarfile.PAX_FORMAT: 'pax'}.get(t.format, t.format)
    latest = max(ms, key=lambda m: m.mtime)
    times = collections.Counter(dt.datetime.fromtimestamp(m.mtime, dt.timezone.utc).strftime('%Y-%m-%d %H:%M:%S') for m in ms if m.isfile())
    print(f"{p.split('/')[-1]:30s} gzip_mtime={dt.datetime.fromtimestamp(mt, dt.timezone.utc):%Y-%m-%d %H:%M:%S}Z os={osb} fmt={fmt} owners={dict(owners)}")
    print(f"{'':30s} latest={dt.datetime.fromtimestamp(latest.mtime, dt.timezone.utc):%Y-%m-%d %H:%M:%S}Z {latest.name} | common file mtimes(UTC)={times.most_common(2)}")
