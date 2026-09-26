#!/usr/bin/env python3
"""Count posts per month (all authors vs selected authors) in pipermail
monthly archives (.txt / .txt.gz, mbox-like with 'From ' separators).

Usage: list_author_counts.py DIR PATTERN[,PATTERN...]
PATTERN is a case-insensitive regex matched against the From: header.
"""
import gzip, os, re, sys, collections, email.utils, datetime as dt

MONTHS = {m: i for i, m in enumerate(["January","February","March","April","May","June","July","August","September","October","November","December"], 1)}

def messages(path):
    op = gzip.open if path.endswith(".gz") else open
    with op(path, "rb") as f:
        data = f.read().decode("latin-1")
    for chunk in re.split(r"\n(?=From \S+ +(?:at \S+ +)?\w{3} \w{3} +\d+ [\d:]+ \d{4})", "\n" + data):
        if not chunk.strip():
            continue
        hdr = chunk.split("\n\n", 1)[0]
        frm = re.search(r"^From: (.*(?:\n[ \t].*)*)", hdr, re.M)
        date = re.search(r"^Date: (.*)", hdr, re.M)
        subj = re.search(r"^Subject: (.*(?:\n[ \t].*)*)", hdr, re.M)
        yield (frm.group(1).replace("\n", " ") if frm else "", date.group(1).strip() if date else "", subj.group(1).replace("\n"," ") if subj else "")

def main():
    d, pats = sys.argv[1], [re.compile(p, re.I) for p in sys.argv[2].split(",")]
    rows = []
    for fn in os.listdir(d):
        m = re.match(r"(\d{4})-(\w+)\.txt", fn)
        if not m or m.group(2) not in MONTHS:
            continue
        ym = (int(m.group(1)), MONTHS[m.group(2)])
        tot = 0; hits = []
        for frm, date, subj in messages(os.path.join(d, fn)):
            tot += 1
            if any(p.search(frm) for p in pats):
                hits.append((date, frm, subj))
        rows.append((ym, tot, hits))
    rows.sort()
    for (y, mo), tot, hits in rows:
        print(f"{y}-{mo:02d}  total={tot:5d}  match={len(hits):3d}")
    print("\n# matching posts")
    for (y, mo), tot, hits in rows:
        for date, frm, subj in hits:
            print(f"{y}-{mo:02d} | {date} | {frm[:50]} | {subj[:70]}")

main()
