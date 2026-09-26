#!/usr/bin/env python3
"""Print PE/COFF header fields relevant to build forensics.

The COFF TimeDateStamp is seconds since 1970-01-01 UTC, written by the linker
(GNU ld on MinGW writes time(NULL) at link time unless told otherwise).
Also prints linker version, subsystem, section names and any debug directory.

Usage: pe_info.py FILE.exe [FILE.dll ...]
"""
import datetime as dt
import struct
import sys


def info(path):
    b = open(path, "rb").read()
    (e_lfanew,) = struct.unpack_from("<I", b, 0x3C)
    assert b[e_lfanew : e_lfanew + 4] == b"PE\0\0", "not a PE file"
    coff = e_lfanew + 4
    machine, nsec, tds, symptr, nsym, optsz, chars = struct.unpack_from("<HHIIIHH", b, coff)
    opt = coff + 20
    magic, lmaj, lmin = struct.unpack_from("<HBB", b, opt)
    # PE32 optional header
    (image_base,) = struct.unpack_from("<I", b, opt + 28)
    os_maj, os_min, img_maj, img_min, sub_maj, sub_min = struct.unpack_from("<HHHHHH", b, opt + 40)
    (subsystem,) = struct.unpack_from("<H", b, opt + 68)
    (checksum,) = struct.unpack_from("<I", b, opt + 64)
    secs = []
    sh = opt + optsz
    for i in range(nsec):
        name = b[sh + 40 * i : sh + 40 * i + 8].rstrip(b"\0").decode("latin-1")
        vsize, vaddr, rawsize, rawptr = struct.unpack_from("<IIII", b, sh + 40 * i + 8)
        secs.append((name, vsize, rawsize))
    t = dt.datetime.fromtimestamp(tds, dt.timezone.utc)
    print(f"{path}")
    print(f"  COFF TimeDateStamp : {tds} = {t:%Y-%m-%d %H:%M:%S} UTC")
    print(f"  Machine 0x{machine:x}, sections {nsec}, symbols {nsym} @0x{symptr:x}, characteristics 0x{chars:x}")
    print(f"  Linker {lmaj}.{lmin}, OS {os_maj}.{os_min}, image {img_maj}.{img_min}, subsystem {subsystem} v{sub_maj}.{sub_min}, checksum 0x{checksum:x}")
    print(f"  Sections: " + ", ".join(f"{n}({r})" for n, v, r in secs))


if __name__ == "__main__":
    for p in sys.argv[1:]:
        info(p)
