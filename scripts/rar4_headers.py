#!/usr/bin/env python3
"""Dump raw RAR 4.x block headers, including file timestamps, without any
time-zone conversion.

RAR 2.x/3.x/4.x store FTIME as an MS-DOS date/time, which is the *local* wall
clock time of the machine that created the archive (there is no time-zone
field). Optional EXT_TIME records add sub-second precision (100 ns units) and
optional ctime/atime/arctime values, also in local time.

Reference: RAR 3.x/4.x technote.txt (block types 0x72 marker, 0x73 archive,
0x74 file, 0x75 comment, 0x7a subblock/new-sub, 0x7b end).

Usage: rar4_headers.py ARCHIVE.rar [--json]
"""
import json
import struct
import sys
import zlib

HOST_OS = {0: "MS-DOS", 1: "OS/2", 2: "Win32", 3: "Unix", 4: "Mac OS", 5: "BeOS"}


def dos_time(v):
    """Decode a 32-bit DOS date/time into a naive (local) tuple string."""
    sec = (v & 0x1F) * 2
    minute = (v >> 5) & 0x3F
    hour = (v >> 11) & 0x1F
    day = (v >> 16) & 0x1F
    month = (v >> 21) & 0x0F
    year = ((v >> 25) & 0x7F) + 1980
    return year, month, day, hour, minute, sec


def fmt(t, frac=None, plus1=False):
    y, mo, d, h, mi, s = t
    if plus1:
        s += 1
    out = f"{y:04d}-{mo:02d}-{d:02d} {h:02d}:{mi:02d}:{s:02d}"
    if frac is not None:
        out += f".{frac:07d}"
    return out


def parse_ext_time(buf, pos, ftime):
    """Parse the EXT_TIME structure. Returns (dict, new_pos)."""
    (flags,) = struct.unpack_from("<H", buf, pos)
    pos += 2
    names = ["mtime", "ctime", "atime", "arctime"]
    out = {}
    for i, name in enumerate(names):
        rmode = (flags >> ((3 - i) * 4)) & 0xF
        if not (rmode & 8):
            continue
        if i == 0:
            base = ftime
        else:
            (base,) = struct.unpack_from("<I", buf, pos)
            pos += 4
        count = rmode & 3
        rem = 0
        for j in range(count):
            rem |= buf[pos] << ((j + 3 - count) * 8)
            pos += 1
        # rem is in 100ns units, stored in the top `count` bytes of a 24-bit value
        out[name] = fmt(dos_time(base), frac=rem, plus1=bool(rmode & 4))
    return out, pos


def parse(path):
    buf = open(path, "rb").read()
    if buf[:7] != b"Rar!\x1a\x07\x00":
        raise SystemExit("not a RAR 4.x archive")
    pos = 7
    blocks = []
    while pos + 7 <= len(buf):
        crc, htype, hflags, hsize = struct.unpack_from("<HBHH", buf, pos)
        if hsize < 7:
            break
        block = {"offset": pos, "type": hex(htype), "flags": hex(hflags), "head_size": hsize}
        add_size = 0
        if htype == 0x73:  # archive header
            block["kind"] = "archive"
            block["solid"] = bool(hflags & 0x0008)
            block["has_comment"] = bool(hflags & 0x0002)
            block["locked"] = bool(hflags & 0x0004)
            block["authenticity_info"] = bool(hflags & 0x0020)
            block["recovery_record"] = bool(hflags & 0x0040)
        elif htype in (0x74, 0x7A):  # file header / new sub-block
            (pack_size, unp_size, host_os, file_crc, ftime, unp_ver, method, name_size, attr) = struct.unpack_from(
                "<IIBIIBBHI", buf, pos + 7
            )
            p = pos + 7 + 25
            if hflags & 0x0100:
                hi_pack, hi_unp = struct.unpack_from("<II", buf, p)
                p += 8
                pack_size |= hi_pack << 32
                unp_size |= hi_unp << 32
            name = buf[p : p + name_size]
            p += name_size
            if hflags & 0x0400:
                p += 8  # salt
            ext = {}
            if hflags & 0x1000:
                ext, p = parse_ext_time(buf, p, ftime)
            if b"\x00" in name:  # unicode name follows a NUL
                name = name.split(b"\x00")[0]
            block.update(
                {
                    "kind": "file" if htype == 0x74 else "subblock",
                    "name": name.decode("latin-1"),
                    "packed": pack_size,
                    "size": unp_size,
                    "host_os": HOST_OS.get(host_os, host_os),
                    "crc32": f"{file_crc:08x}",
                    "unp_ver": unp_ver,
                    "method": method,
                    "attr": hex(attr),
                    "is_dir": (hflags & 0x00E0) == 0x00E0,
                    "dos_time_raw": hex(ftime),
                    "mtime_local": ext.get("mtime", fmt(dos_time(ftime))),
                    "ext_times_local": ext,
                }
            )
            add_size = pack_size
        elif htype == 0x75:
            block["kind"] = "comment"
        elif htype == 0x7B:
            block["kind"] = "end"
        else:
            block["kind"] = "other"
            if hflags & 0x8000:
                (add_size,) = struct.unpack_from("<I", buf, pos + 7)
        blocks.append(block)
        if htype == 0x7B:
            break
        pos += hsize + add_size
    return blocks


if __name__ == "__main__":
    blocks = parse(sys.argv[1])
    if "--json" in sys.argv:
        print(json.dumps(blocks, indent=1))
    else:
        for b in blocks:
            if b["kind"] in ("file", "subblock"):
                ext = b["ext_times_local"]
                extra = " ".join(f"{k}={v}" for k, v in ext.items() if k != "mtime")
                print(
                    f"{b['mtime_local']:<27} {b['size']:>9} {b['host_os']:<6} {b['attr']:<6} "
                    f"{'D' if b['is_dir'] else ' '} {b['name']}  {extra}"
                )
            else:
                print(f"[{b['kind']}] " + " ".join(f"{k}={v}" for k, v in b.items() if k not in ("kind",)))
