#!/usr/bin/env python3
"""Scan Gmane NNTP archives (news.gmane.io) for articles From: Satoshi Nakamoto and save them raw.

Gmane keeps the full RFC822 message (all headers incl. Received:, Date:, Message-ID:), so
these are the most "raw" public copies of Satoshi's mailing-list posts.

Groups scanned:
  gmane.comp.encryption.general            = metzdowd "cryptography" list
  gmane.comp.peer-to-peer.p2p-foundation   = P2P Foundation lists (p2p-research?)
  gmane.comp.security.cypherpunks          = cypherpunks
  gmane.comp.bitcoin.user                  = bitcoin-list (only 2011+ in gmane)
  gmane.comp.bitcoin.devel                 = bitcoin-development (2011+)

Output: data/satoshi/raw/gmane/<group>/<artnum>.eml and data/satoshi/raw/gmane/scan.tsv
"""
import os
import sys
import warnings

warnings.filterwarnings("ignore")
import nntplib  # noqa: E402  (deprecated, removed in Python 3.13; run with <= 3.12)

nntplib._MAXLINE = 1 << 20

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
OUT = os.path.join(ROOT, "data", "satoshi", "raw", "gmane")
GROUPS = [
    "gmane.comp.encryption.general",
    "gmane.comp.peer-to-peer.p2p-foundation",
    "gmane.comp.security.cypherpunks",
    "gmane.comp.bitcoin.user",
    "gmane.comp.bitcoin.devel",
]
NEEDLES = ("satoshi", "vistomail", "anonymousspeech")


def main():
    os.makedirs(OUT, exist_ok=True)
    s = nntplib.NNTP("news.gmane.io", timeout=120)
    rows = []
    for g in GROUPS:
        resp, count, first, last, name = s.group(g)
        print(g, count, first, last, flush=True)
        step = 2000
        for a in range(first, last + 1, step):
            try:
                resp, ov = s.over((a, min(a + step - 1, last)))
            except Exception as e:  # pragma: no cover
                print("  over failed", a, e, flush=True)
                continue
            for num, o in ov:
                frm = o.get("from", "")
                if any(n in frm.lower() for n in NEEDLES):
                    rows.append((g, num, o.get("date"), frm, o.get("subject"), o.get("message-id")))
                    print("  ", num, o.get("date"), "|", frm, "|", o.get("subject"), flush=True)
    for g, num, date, *_ in rows:
        # Only download 2008-2011 articles; later "Satoshi" posts are well-known impostors
        # (listed in scan.tsv for completeness, never downloaded or used).
        if not any(str(y) in (date or "") for y in range(2008, 2012)):
            continue
        s.group(g)
        d = os.path.join(OUT, g)
        os.makedirs(d, exist_ok=True)
        p = os.path.join(d, f"{num}.eml")
        if os.path.exists(p):
            continue
        resp, info = s.article(str(num))
        with open(p, "wb") as f:
            f.write(b"\n".join(info.lines) + b"\n")
    with open(os.path.join(OUT, "scan.tsv"), "w") as f:
        f.write("group\tartnum\tdate\tfrom\tsubject\tmessage_id\n")
        for r in rows:
            f.write("\t".join(str(x).replace("\t", " ") for x in r) + "\n")
    s.quit()


if __name__ == "__main__":
    main()
