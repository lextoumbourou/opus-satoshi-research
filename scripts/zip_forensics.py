#!/usr/bin/env python3
"""Dump ZIP central-directory metadata relevant to build/packaging forensics:
creator system/version, raw DOS (local) date/time, and any extra fields that
carry absolute (UTC) times:
  0x000a NTFS  -> Mtime/Atime/Ctime as Windows FILETIME (UTC)
  0x5455 UT    -> Unix mtime/atime/ctime (UTC seconds)
  0x5855 UX    -> old Info-ZIP Unix atime/mtime (UTC)
If both a DOS local time and a UTC time exist for the same entry, their
difference is the packing machine's UTC offset at packing time.

Usage: zip_forensics.py FILE.zip [--all]
"""
import datetime as dt
import struct
import sys
import zipfile

SYS = {0: "MS-DOS/FAT", 3: "Unix", 7: "Macintosh", 10: "NTFS(Win32)", 11: "MVS", 19: "OS X"}


def filetime(v):
    return dt.datetime(1601, 1, 1) + dt.timedelta(microseconds=v // 10)


def extras(b):
    out = {}
    i = 0
    while i + 4 <= len(b):
        hid, ln = struct.unpack_from("<HH", b, i)
        data = b[i + 4 : i + 4 + ln]
        if hid == 0x000A and len(data) >= 32:
            # reserved(4) then attribute tag 0x0001 size 24: mtime, atime, ctime
            tag, sz = struct.unpack_from("<HH", data, 4)
            if tag == 1:
                m, a, c = struct.unpack_from("<QQQ", data, 8)
                out["ntfs_mtime_utc"] = filetime(m).strftime("%Y-%m-%d %H:%M:%S.%f")
                out["ntfs_ctime_utc"] = filetime(c).strftime("%Y-%m-%d %H:%M:%S.%f")
        elif hid == 0x5455 and len(data) >= 5:
            flags = data[0]
            if flags & 1:
                (m,) = struct.unpack_from("<I", data, 1)
                out["ut_mtime_utc"] = dt.datetime.utcfromtimestamp(m).strftime("%Y-%m-%d %H:%M:%S")
        elif hid == 0x5855 and len(data) >= 8:
            a, m = struct.unpack_from("<II", data, 0)
            out["ux_mtime_utc"] = dt.datetime.utcfromtimestamp(m).strftime("%Y-%m-%d %H:%M:%S")
        else:
            out[f"extra_0x{hid:04x}"] = ln
        i += 4 + ln
    return out


def main(path, show_all=False):
    z = zipfile.ZipFile(path)
    infos = z.infolist()
    sysver = {(i.create_system, i.create_version, i.extract_version) for i in infos}
    print(f"== {path}: {len(infos)} entries; creator (system, version, extract_ver): "
          + ", ".join(f"({SYS.get(s, s)}, {v/10:.1f}, {e/10:.1f})" for s, v, e in sysver))
    if z.comment:
        print("   comment:", z.comment[:200])
    rows = infos if show_all else [i for i in infos if i.filename.endswith("/") or i.filename.lower().endswith(".exe") or "/" not in i.filename.rstrip("/")][:40]
    for i in rows:
        y, mo, d, h, mi, s = i.date_time
        ex = extras(i.extra)
        exs = " ".join(f"{k}={v}" for k, v in ex.items())
        print(f"   {y:04d}-{mo:02d}-{d:02d} {h:02d}:{mi:02d}:{s:02d} local  {i.file_size:>9}  attr=0x{i.external_attr:08x}  {i.filename}  {exs}")


if __name__ == "__main__":
    main(sys.argv[1], "--all" in sys.argv)
