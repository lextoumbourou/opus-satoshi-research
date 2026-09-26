#!/usr/bin/env python3
"""Fetch Satoshi Nakamoto's posts on the P2P Foundation Ning social network
(p2pfoundation.ning.com) from the Internet Archive (Wayback Machine, `id_` raw captures).

Targets:
  - the forum topic "Bitcoin open source implementation of P2P currency"
      http://p2pfoundation.ning.com/forum/topics/bitcoin-open-source  (all captures listed, several
      eras fetched so the displayed timestamp format / zone can be compared across Ning versions)
  - its feed (Atom/RSS) variants if archived: ...?feed=yes&xn_auth=no  (machine timestamps)
  - Satoshi's reply permalinks  http://p2pfoundation.ning.com/xn/detail/2003008:Comment:<N>
  - Satoshi's profile page and "listForContributor" page (to check for posts SNI lacks)

Saved to data/satoshi/raw/p2pfoundation/ with fetch_meta.json (original URL + capture ts).
Politeness: >= 3 s between requests, exponential backoff when IA is "Temporarily Offline".
"""
import json
import os
import re
import sys
import time
import urllib.parse

import requests

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
OUT = os.path.join(ROOT, "data", "satoshi", "raw", "p2pfoundation")
DELAY = 3.0
sess = requests.Session()
sess.headers["User-Agent"] = "Mozilla/5.0 (satoshi-research corpus builder; polite)"
_last = [0.0]


def polite_get(url, timeout=120):
    for attempt in range(8):
        wait = _last[0] + DELAY - time.time()
        if wait > 0:
            time.sleep(wait)
        try:
            r = sess.get(url, timeout=timeout, allow_redirects=True)
            _last[0] = time.time()
            if b"Temporarily Offline" in r.content[:3000] and "archive.org" in r.url:
                raise requests.RequestException("IA temporarily offline")
            return r
        except requests.RequestException as e:
            _last[0] = time.time()
            back = min(300, 10 * 2 ** attempt)
            print(f"    error {e!s:.80} -> sleep {back}s", flush=True)
            time.sleep(back)
    return None


def cdx(url, prefix=False, limit=500):
    q = {"url": url, "fl": "timestamp,original,statuscode,mimetype", "limit": str(limit)}
    if prefix:
        q["matchType"] = "prefix"
    r = polite_get("https://web.archive.org/cdx/search/cdx?" + urllib.parse.urlencode(q), timeout=180)
    if r is None or r.status_code != 200:
        return []
    return [ln.split(" ") for ln in r.text.splitlines() if len(ln.split(" ")) == 4]


def save_capture(ts, orig, dest_rel, meta):
    dest = os.path.join(OUT, dest_rel)
    if os.path.exists(dest):
        return True
    r = polite_get(f"https://web.archive.org/web/{ts}id_/{orig}")
    if r is None or r.status_code != 200:
        meta[dest_rel] = {"error": f"status {getattr(r, 'status_code', None)}", "original": orig, "wayback_ts": ts}
        return False
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    with open(dest, "wb") as f:
        f.write(r.content)
    meta[dest_rel] = {"original": orig, "wayback_ts": ts, "served": r.url, "bytes": len(r.content)}
    print("  saved", dest_rel, len(r.content), flush=True)
    return True


def main():
    os.makedirs(OUT, exist_ok=True)
    meta_path = os.path.join(OUT, "fetch_meta.json")
    meta = json.load(open(meta_path)) if os.path.exists(meta_path) else {}
    listing = {}

    queries = [
        ("topic", "p2pfoundation.ning.com/forum/topics/bitcoin-open-source", True),
        ("comments", "p2pfoundation.ning.com/xn/detail/2003008:Comment:", True),
        ("topicdetail", "p2pfoundation.ning.com/xn/detail/2003008:Topic:", True),
        ("profile", "p2pfoundation.ning.com/profile/SatoshiNakamoto", True),
        ("contrib", "p2pfoundation.ning.com/forum/topic/listForContributor?user=0ye0gncqg772o", True),
    ]
    lp = os.path.join(OUT, "cdx_listing.json")
    if os.path.exists(lp) and "--relist" not in sys.argv:
        listing = json.load(open(lp))
        queries = []
    for key, url, prefix in queries:
        rows = cdx(url, prefix=prefix)
        listing[key] = rows
        print(key, len(rows), flush=True)
    if queries:
        with open(lp, "w") as f:
            json.dump(listing, f, indent=0)

    if "--list-only" in sys.argv:
        return
    # Explicit targets chosen from cdx_listing.json (status 200, distinct eras of the Ning
    # templates). The Feb 2009 capture is the contemporaneous rendering; 2011 and 2024 show later
    # Ning versions; the 2010 profile + "listForContributor" pages list all of Satoshi's forum
    # activity (to check for posts the Nakamoto Institute lacks).
    targets = [
        ("20090221024857", "http://p2pfoundation.ning.com:80/forum/topics/bitcoin-open-source", "topic/main_20090221024857.html"),
        ("20110415095236", "http://p2pfoundation.ning.com:80/forum/topics/bitcoin-open-source?", "topic/main_20110415095236.html"),
        ("20240701162653", "http://p2pfoundation.ning.com/forum/topics/bitcoin-open-source/", "topic/main_20240701162653.html"),
        ("20100702211420", "http://p2pfoundation.ning.com:80/profile/SatoshiNakamoto", "profile/SatoshiNakamoto_20100702211420.html"),
        ("20110526192730", "http://p2pfoundation.ning.com:80/profile/SatoshiNakamoto?", "profile/SatoshiNakamoto_20110526192730.html"),
        ("20210924154548", "https://p2pfoundation.ning.com/profile/SatoshiNakamoto/", "profile/SatoshiNakamoto_20210924154548.html"),
        ("20100704054812", "http://p2pfoundation.ning.com:80/forum/topic/listForContributor?user=0ye0gncqg772o", "contrib/listForContributor_20100704054812.html"),
        # "I am not Dorian Nakamoto" reply (Comment:52186, 2014-03-07): earliest captures of its
        # permalink (found via an exact CDX query; the prefix listing is capped at 500 rows).
        ("20140307021221", "http://p2pfoundation.ning.com/forum/topics/bitcoin-open-source%3FcommentId=2003008%253AComment%253A52186", "topic/comment52186_20140307021221.html"),
        ("20140307105200", "http://p2pfoundation.ning.com/forum/topics/bitcoin-open-source?commentId=2003008%3AComment%3A52186", "topic/comment52186_20140307105200.html"),
        # a later capture, once Ning shows the absolute date instead of "N hours ago"
        ("20140402054325", "http://p2pfoundation.ning.com/forum/topics/bitcoin-open-source?commentId=2003008%3AComment%3A52186", "topic/comment52186_20140402054325.html"),
    ]
    for ts, orig, rel in targets:
        save_capture(ts, orig, rel, meta)
        with open(meta_path, "w") as f:
            json.dump(meta, f, indent=1, sort_keys=True)
    with open(meta_path, "w") as f:
        json.dump(meta, f, indent=1, sort_keys=True)


if __name__ == "__main__":
    main()
