#!/usr/bin/env python3
"""Look for Satoshi Nakamoto posts in the Bitcoin SourceForge project's *forums* and *news*
(2009-2010), via Internet Archive CDX listings + raw (`id_`) captures. sourceforge.net itself is
behind a Cloudflare challenge, which we do not bypass.

URL families checked (CDX prefix queries):
  sourceforge.net/projects/bitcoin/forums/        (legacy project forums, 2009-2012)
  sourceforge.net/p/bitcoin/discussion/           (Allura discussion tool)
  sourceforge.net/p/bitcoin/news/                 (Allura project news / blog)
  sourceforge.net/news/?group_id=244765           (legacy project news; bitcoin group_id 244765)
  sourceforge.net/forum/forum.php?forum_id=...    (legacy forums; only via links found above)

Output: data/satoshi/raw/sourceforge_bitcoin_list/forums/ (cdx listings + fetched pages +
fetch_meta.json). Parse step: parse_sourceforge_forums.py.
"""
import json
import os
import re
import time
import urllib.parse

import requests

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
OUT = os.path.join(ROOT, "data", "satoshi", "raw", "sourceforge_bitcoin_list", "forums")
DELAY = 3.0
sess = requests.Session()
sess.headers["User-Agent"] = "Mozilla/5.0 (satoshi-research corpus builder; polite)"
_last = [0.0]

PREFIXES = [
    "sourceforge.net/projects/bitcoin/forums/",
    "sourceforge.net/p/bitcoin/discussion/",
    "sourceforge.net/p/bitcoin/news/",
    "sourceforge.net/news/?group_id=244765",
    "sourceforge.net/forum/?group_id=244765",
    "sourceforge.net/projects/bitcoin/news",
]


def polite_get(url, timeout=180):
    for attempt in range(7):
        wait = _last[0] + DELAY - time.time()
        if wait > 0:
            time.sleep(wait)
        try:
            r = sess.get(url, timeout=timeout)
            _last[0] = time.time()
            if b"Temporarily Offline" in r.content[:3000] and "archive.org" in r.url:
                raise requests.RequestException("IA temporarily offline")
            if r.status_code in (502, 503, 504):
                raise requests.RequestException(f"HTTP {r.status_code}")
            return r
        except requests.RequestException as e:
            _last[0] = time.time()
            back = min(300, 10 * 2 ** attempt)
            print(f"    error {e!s:.80} -> sleep {back}s", flush=True)
            time.sleep(back)
    return None


def cdx_prefix(prefix):
    q = {"url": prefix, "matchType": "prefix", "fl": "timestamp,original,statuscode,mimetype",
         "collapse": "urlkey", "limit": "3000"}
    r = polite_get("https://web.archive.org/cdx/search/cdx?" + urllib.parse.urlencode(q))
    if r is None or r.status_code != 200:
        return None
    return [ln.split(" ") for ln in r.text.splitlines() if len(ln.split(" ")) == 4]


def main():
    os.makedirs(OUT, exist_ok=True)
    meta_p = os.path.join(OUT, "fetch_meta.json")
    meta = json.load(open(meta_p)) if os.path.exists(meta_p) else {}
    listing_p = os.path.join(OUT, "cdx_listing.json")
    listing = json.load(open(listing_p)) if os.path.exists(listing_p) else {}
    for pre in PREFIXES:
        if pre in listing and listing[pre] is not None:
            continue
        rows = cdx_prefix(pre)
        listing[pre] = rows
        print(pre, None if rows is None else len(rows), flush=True)
        with open(listing_p, "w") as f:
            json.dump(listing, f, indent=0)
    if "--list-only" in __import__("sys").argv:
        return
    # fetch every distinct 200 text/html page (earliest capture) from the forum/news families,
    # skipping obvious non-content (RSS/stats/login) pages; cap to keep IA load small
    todo = []
    for pre, rows in listing.items():
        for ts, orig, st, mime in rows or []:
            if st != "200" or not ("html" in mime or "xml" in mime):
                continue
            if re.search(r"(login|stats|subscribe|monitor|search|tags|sf\.js|sf\.php|\.css|\.png|\.gif|\.webp)", orig, re.I):
                continue
            todo.append((ts, orig))
    todo = sorted(set(todo))[:120]
    for ts, orig in todo:
        safe = re.sub(r"[^A-Za-z0-9._-]+", "_", orig.split("sourceforge.net/", 1)[-1])[:120]
        rel = f"{safe}_{ts}.html"
        if os.path.exists(os.path.join(OUT, rel)):
            continue
        r = polite_get(f"https://web.archive.org/web/{ts}id_/{orig}")
        if r is None or r.status_code != 200:
            meta[rel] = {"error": f"status {getattr(r, 'status_code', None)}", "original": orig}
            continue
        with open(os.path.join(OUT, rel), "wb") as f:
            f.write(r.content)
        meta[rel] = {"original": orig, "wayback_ts": ts, "bytes": len(r.content)}
        print("  saved", rel, flush=True)
        with open(meta_p, "w") as f:
            json.dump(meta, f, indent=1, sort_keys=True)
    with open(meta_p, "w") as f:
        json.dump(meta, f, indent=1, sort_keys=True)


if __name__ == "__main__":
    main()
