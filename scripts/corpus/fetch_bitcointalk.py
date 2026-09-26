#!/usr/bin/env python3
"""Fetch all posts by bitcointalk user `satoshi` (u=3) via the profile showPosts view.

Politeness: one request every >= 3 seconds (bitcointalk blocks aggressive scraping).

Raw HTML pages are saved to data/satoshi/raw/bitcointalk/showposts/start_XXXX.html together
with a sidecar .meta.json recording the fetch time and the HTTP `Date` header. The page header
of every bitcointalk page shows the current time in the viewer's display zone; for a guest
this is compared against the HTTP Date header to establish the display zone (see README).

Usage: python3 scripts/corpus/fetch_bitcointalk.py [--force]
"""
import json
import os
import re
import sys
import time
from datetime import datetime, timezone

import requests

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
OUT = os.path.join(ROOT, "data", "satoshi", "raw", "bitcointalk", "showposts")
BASE = "https://bitcointalk.org/index.php?action=profile;u=3;sa=showPosts;start={}"
UA = "Mozilla/5.0 (satoshi-research corpus builder; polite, 1 req/3s)"
DELAY = 3.0


def main():
    force = "--force" in sys.argv
    os.makedirs(OUT, exist_ok=True)
    s = requests.Session()
    s.headers["User-Agent"] = UA
    start = 0
    last_start = None
    while True:
        path = os.path.join(OUT, f"start_{start:04d}.html")
        if os.path.exists(path) and not force:
            html = open(path, encoding="latin-1").read()
        else:
            url = BASE.format(start)
            r = s.get(url, timeout=60)
            r.raise_for_status()
            html = r.content.decode("latin-1")
            with open(path, "wb") as f:
                f.write(r.content)
            meta = {
                "url": url,
                "fetched_utc": datetime.now(timezone.utc).isoformat(),
                "http_date": r.headers.get("Date"),
                "status": r.status_code,
            }
            with open(path + ".meta.json", "w") as f:
                json.dump(meta, f, indent=1)
            print("fetched", url, len(r.content), flush=True)
            time.sleep(DELAY)
        if last_start is None:
            starts = [int(x) for x in re.findall(r"sa=showPosts;start=(\d+)", html)]
            last_start = max(starts) if starts else 0
        if start >= last_start:
            break
        start += 20


if __name__ == "__main__":
    main()
