#!/usr/bin/env python3
"""Download the raw bitcoin-list articles that Gmane archived (gmane.comp.bitcoin.user, Nov 2011 -
2018; Gmane did not subscribe before then, so none of Satoshi's posts are there).

Purpose: TIME-ZONE ANCHOR for the SourceForge mailing-list archive. SourceForge's archive pages
show "YYYY-MM-DD HH:MM:SS" with no zone and (as found for Satoshi's CHILKAT-MID-30c0e5a0 message)
not the Date: header. Comparing SourceForge's displayed time for a message with the
`Received: ... by lists.sourceforge.net` / Date: headers of the same message in Gmane's raw copy
pins down what clock/zone SourceForge displays.

Output: data/satoshi/raw/sourceforge_bitcoin_list/gmane_bitcoin_user/<artnum>.eml
"""
import os
import warnings

warnings.filterwarnings("ignore")
import nntplib  # noqa: E402  (removed in Python 3.13; run with <= 3.12)

nntplib._MAXLINE = 1 << 20
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
OUT = os.path.join(ROOT, "data", "satoshi", "raw", "sourceforge_bitcoin_list", "gmane_bitcoin_user")


def main():
    os.makedirs(OUT, exist_ok=True)
    s = nntplib.NNTP("news.gmane.io", timeout=120)
    resp, count, first, last, name = s.group("gmane.comp.bitcoin.user")
    for num in range(first, last + 1):
        p = os.path.join(OUT, f"{num}.eml")
        if os.path.exists(p):
            continue
        try:
            resp, info = s.article(str(num))
        except nntplib.NNTPTemporaryError as e:
            print(num, e)
            continue
        with open(p, "wb") as f:
            f.write(b"\n".join(info.lines) + b"\n")
    s.quit()
    print("done", len(os.listdir(OUT)))


if __name__ == "__main__":
    main()
