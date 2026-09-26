#!/usr/bin/env python3
"""Extract Satoshi's code comments (and readme prose) from the earliest Bitcoin source releases.

Sources (downloaded from the Satoshi Nakamoto Institute CDN; hashes match those published at
https://satoshi.nakamotoinstitute.org/code/):
  https://cdn.nakamotoinstitute.org/code/bitcoin-nov08.rar   (pre-release sent to early testers, Nov 2008)
  https://cdn.nakamotoinstitute.org/code/bitcoin-0.1.0.rar   (v0.1.0, released 2009-01-09)
Download + extract:
  curl -O https://cdn.nakamotoinstitute.org/code/bitcoin-0.1.0.rar ; unar bitcoin-0.1.0.rar  (etc.)

Third-party / generated files are excluded: sha.cpp/sha.h (Crypto++), uibase.cpp/uibase.h and
uiproject.fbp (wxFormBuilder-generated).

One record per file. Comments carry NO reliable timestamp: the archive member mtimes are
normalised (e.g. "2009-01-07 01:00") and are local times of the archiving machine with an unknown
zone, so timestamp_utc is null and the archive mtime is kept in timestamp_raw for reference.

Output: data/satoshi/intermediate/code_comments.jsonl
"""
import json
import os
import re
import subprocess

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
RAW = os.path.join(ROOT, "data", "satoshi", "raw", "code")
OUT = os.path.join(ROOT, "data", "satoshi", "intermediate", "code_comments.jsonl")
EXCLUDE = {"sha.cpp", "sha.h", "uibase.cpp", "uibase.h", "uiproject.fbp", "license.txt"}
RELEASES = [
    ("bitcoin-nov08", "bitcoin-nov08.rar", "Bitcoin pre-release source (Nov 2008)", "2008-11"),
    ("bitcoin-0.1.0", "bitcoin-0.1.0.rar", "Bitcoin v0.1.0 source (released 2009-01-09)", "2009-01-09"),
]


def comments(src):
    """Return list of comment strings (verbatim incl. markers), respecting string/char literals."""
    out = []
    i, n = 0, len(src)
    while i < n:
        c = src[i]
        if c in "\"'":
            q = c
            i += 1
            while i < n and src[i] != q:
                if src[i] == "\\":
                    i += 1
                if src[i] == "\n":
                    break
                i += 1
            i += 1
        elif src.startswith("//", i):
            j = src.find("\n", i)
            j = n if j < 0 else j
            out.append(src[i:j])
            i = j
        elif src.startswith("/*", i):
            j = src.find("*/", i + 2)
            j = n if j < 0 else j + 2
            out.append(src[i:j])
            i = j
        else:
            i += 1
    return out


def strip_marker(c):
    if c.startswith("//"):
        return c[2:]
    body = c[2:-2] if c.endswith("*/") else c[2:]
    return "\n".join(re.sub(r"^\s*\* ?", "", l) for l in body.split("\n"))


def archive_mtimes(rar):
    out = subprocess.run(["lsar", "-l", rar], capture_output=True, text=True).stdout
    res = {}
    for m in re.finditer(r"^\s*\d+\.\s+\S+\s+\d+\s+\S+\s+\S+\s+(\d{4}-\d\d-\d\d \d\d:\d\d)\s+(.+)$", out, re.M):
        res[os.path.basename(m.group(2).strip())] = m.group(1)
    return res


def main():
    rows = []
    for d, rar, label, rel_date in RELEASES:
        base = os.path.join(RAW, d, d)
        mt = archive_mtimes(os.path.join(RAW, rar))
        for dirpath, _, files in os.walk(base):
            for fn in sorted(files):
                if fn in EXCLUDE or not re.search(r"\.(cpp|h|txt|rc)$|^makefile", fn):
                    continue
                p = os.path.join(dirpath, fn)
                src = open(p, "rb").read().decode("latin-1")
                if fn.endswith(".txt"):
                    raw = src
                    text = src.replace("\r\n", "\n")
                    kind = "readme/documentation text"
                else:
                    cs = comments(src)
                    if fn.startswith("makefile"):
                        cs = [l for l in src.split("\n") if l.lstrip().startswith("#")]
                    # drop the boilerplate copyright header lines
                    cs = [c for c in cs if not re.search(r"Copyright \(c\)|Distributed under the MIT|file license.txt or http", c)]
                    if not cs:
                        continue
                    raw = "\n".join(cs)
                    text = "\n".join(strip_marker(c) if not fn.startswith("makefile") else c.lstrip()[1:] for c in cs)
                    text = text.replace("\r", "")
                    kind = "source comments"
                relp = os.path.relpath(p, ROOT)
                rows.append({
                    "id": f"code-{d}-" + os.path.relpath(p, base).replace(os.sep, "_"),
                    "source_type": "code_comment",
                    "venue": label,
                    "recipient": None,
                    "thread": os.path.relpath(p, base),
                    "timestamp_utc": None,
                    "timestamp_raw": f"archive member mtime {mt.get(fn, '?')} (zone unknown)",
                    "timestamp_precision": "none",
                    "timestamp_source": f"none; release date {rel_date}. Archive mtimes are normalised local times with unknown zone, not usable as UTC.",
                    "timestamp_tz_raw": None,
                    "url": f"https://cdn.nakamotoinstitute.org/code/{rar}",
                    "raw_path": relp,
                    "text": text.strip("\n"),
                    "text_raw": raw.replace("\r\n", "\n"),
                    "whitespace_preserved": True,
                    "whitespace_notes": f"{kind} extracted verbatim from the release archive (CRLF normalised to LF). One record per file; comments joined with newlines.",
                    "release_date": rel_date,
                    "notes": "Code comments are Satoshi's words but carry no per-comment timestamp; excluded from time-of-day statistics.",
                })
    with open(OUT, "w") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(len(rows), "code/readme records")


if __name__ == "__main__":
    main()
