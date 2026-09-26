#!/usr/bin/env python3
"""For each ZIP, compute (DOS local time - UT/NTFS UTC time) per entry, i.e.
the packing machine's UTC offset, and summarise. Also report the creator
system/version and the latest entry times."""
import collections, datetime as dt, struct, sys, zipfile, glob

def ut_mtime(extra):
    i = 0
    while i + 4 <= len(extra):
        hid, ln = struct.unpack_from("<HH", extra, i)
        d = extra[i + 4 : i + 4 + ln]
        if hid == 0x5455 and len(d) >= 5 and d[0] & 1:
            return dt.datetime.fromtimestamp(struct.unpack_from("<I", d, 1)[0], dt.timezone.utc).replace(tzinfo=None)
        if hid == 0x000A and len(d) >= 32 and struct.unpack_from("<H", d, 4)[0] == 1:
            m = struct.unpack_from("<Q", d, 8)[0]
            return dt.datetime(1601, 1, 1) + dt.timedelta(microseconds=m // 10)
        i += 4 + ln
    return None

for path in sorted(sys.argv[1:], key=lambda p: [int(x) if x.isdigit() else x for x in p.replace('-', '.').split('.')]):
    z = zipfile.ZipFile(path)
    offs = collections.Counter(); n = 0; latest = None; latest_utc = None; creators = set(); exe = None
    for i in z.infolist():
        creators.add((i.create_system, i.create_version))
        loc = dt.datetime(*i.date_time)
        u = ut_mtime(i.extra)
        if u:
            n += 1
            diff = (loc - u).total_seconds() / 3600
            offs[round(diff * 4) / 4] += 1
            if latest_utc is None or u > latest_utc: latest_utc, latest = u, (loc, i.filename)
        if i.filename.endswith("bitcoin.exe"): exe = (loc, u)
    oo = ", ".join(f"{k:+.2f}h x{v}" for k, v in sorted(offs.items()))
    print(f"{path.split('/')[-1]:32s} creators={sorted(creators)} utc-fields={n}/{len(z.infolist())} offsets: {oo}")
    if exe: print(f"{'':32s} bitcoin.exe local={exe[0]} utc={exe[1]}")
