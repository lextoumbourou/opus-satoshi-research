#!/usr/bin/env python3
"""Fetch the p2p-research mailing list (P2P Foundation) pipermail archives that contain
Satoshi Nakamoto's Feb-Mar 2009 posts, from the Internet Archive (Wayback Machine).

The original host (p2pfoundation.net/backups/p2p_research-archives/) now 404s, and the
diyhpl.us mirror used by the Nakamoto Institute is behind an anti-bot challenge, so we use
Wayback captures with the `id_` modifier (serves the original bytes, no Wayback toolbar).

Saved to data/satoshi/raw/p2p_research/:
  <YYYY-Month>.txt.gz           pipermail monthly "mbox-like" text archive (full From/Date/
                                Subject/In-Reply-To/References/Message-ID headers + body)
  <YYYY-Month>/<NNNNNN>.html    individual pipermail HTML pages (for URL/cross-check)
  <YYYY-Month>/date.html        month index
  fetch_meta.json               wayback timestamps actually served

Politeness: >= 3 s between requests. Re-runnable (skips existing files unless --force).
"""
import json
import os
import re
import sys
import time

import requests

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
OUT = os.path.join(ROOT, "data", "satoshi", "raw", "p2p_research")
BASE = "http://p2pfoundation.net/backups/p2p_research-archives/"
MONTHS = ["2009-February", "2009-March"]
DELAY = 3.0
UA = "Mozilla/5.0 (satoshi-research corpus builder; polite)"


def wb_get(sess, url, ts="2014"):
    """Fetch raw capture of url via Wayback id_ URL; returns (bytes, served_url)."""
    wb = f"https://web.archive.org/web/{ts}id_/{url}"
    for attempt in range(5):
        try:
            r = sess.get(wb, timeout=90, allow_redirects=True)
            if r.status_code == 200:
                return r.content, r.url
            print("  status", r.status_code, wb, flush=True)
            if r.status_code == 404:
                return None, r.url
        except requests.RequestException as e:
            print("  error", e, flush=True)
        time.sleep(DELAY * (attempt + 2))
    return None, None


def main():
    force = "--force" in sys.argv
    os.makedirs(OUT, exist_ok=True)
    s = requests.Session()
    s.headers["User-Agent"] = UA
    meta_path = os.path.join(OUT, "fetch_meta.json")
    meta = json.load(open(meta_path)) if os.path.exists(meta_path) else {}

    def fetch(rel, ts="2014"):
        path = os.path.join(OUT, rel)
        if os.path.exists(path) and not force:
            return open(path, "rb").read()
        os.makedirs(os.path.dirname(path), exist_ok=True)
        data, served = wb_get(s, BASE + rel, ts)
        time.sleep(DELAY)
        if data is None:
            meta[rel] = {"error": "not available", "served": served}
            return None
        with open(path, "wb") as f:
            f.write(data)
        meta[rel] = {"served": served, "bytes": len(data)}
        print("saved", rel, len(data), served, flush=True)
        return data

    for m in MONTHS:
        fetch(f"{m}.txt.gz")
        idx = fetch(f"{m}/date.html")
        if not idx:
            continue
        html = idx.decode("latin-1")
        # Individual message pages authored by Satoshi Nakamoto
        for num, who in re.findall(r'<LI><A HREF="(\d+)\.html">.*?</A><A NAME="\d+">&nbsp;</A>\s*<I>(.*?)\s*</I>', html, re.S):
            if "atoshi" in who:
                fetch(f"{m}/{num}.html")
    with open(meta_path, "w") as f:
        json.dump(meta, f, indent=1, sort_keys=True)


if __name__ == "__main__":
    main()
