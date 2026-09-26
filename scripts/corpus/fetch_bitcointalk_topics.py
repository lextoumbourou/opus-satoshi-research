#!/usr/bin/env python3
"""Fetch the bitcointalk topic pages containing Satoshi's posts, to capture "Last edit" times
(not shown in the showPosts view) and to cross-check post times shown in topic view.

For each topic, request index.php?topic=T.msgM for the earliest not-yet-seen Satoshi msg M
(SMF serves the page containing M); every Satoshi post found on that page is marked done.
Politeness: one request every >= 3 s.

Input : data/satoshi/intermediate/bitcointalk.jsonl (from parse_bitcointalk.py)
Output: data/satoshi/raw/bitcointalk/topics/t<T>_m<M>.html (+ .meta.json)
        data/satoshi/intermediate/bitcointalk_edits.json  {msg_id: {...}}
Re-run parse_bitcointalk.py afterwards to merge edit times into bitcointalk.jsonl.
"""
import json
import os
import re
import sys
import time
from collections import defaultdict
from datetime import datetime, timezone

import requests

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
RAW = os.path.join(ROOT, "data", "satoshi", "raw", "bitcointalk", "topics")
INP = os.path.join(ROOT, "data", "satoshi", "intermediate", "bitcointalk.jsonl")
OUT = os.path.join(ROOT, "data", "satoshi", "intermediate", "bitcointalk_edits.json")
UA = "Mozilla/5.0 (satoshi-research corpus builder; polite, 1 req/3s)"
DELAY = 3.0
DATE_RE = r"[A-Z][a-z]+ \d\d, \d{4}, \d\d:\d\d:\d\d [AP]M"
DATE_FMT = "%B %d, %Y, %I:%M:%S %p"


def parse_page(s):
    """Yield dicts for every post on a topic page."""
    for m in re.finditer(r'id="subject_(\d+)"', s):
        msg = m.group(1)
        before = s[max(0, m.start() - 6000):m.start()]
        posters = re.findall(r'title="View the profile of ([^"]+)"', before)
        after = s[m.end():m.end() + 3000]
        dm = re.search(r'<div class="smalltext">(.*?)</div>', after, re.S)
        block = dm.group(1) if dm else ""
        edit = re.search(r'title="Last edit: (' + DATE_RE + r') by ([^"]+)"', block)
        shown = re.search(DATE_RE, re.sub(r'title="[^"]*"', "", block))
        yield {
            "msg_id": msg,
            "poster": posters[-1] if posters else None,
            "post_time_raw": shown.group(0) if shown else None,
            "last_edit_raw": edit.group(1) if edit else None,
            "last_edit_utc": datetime.strptime(edit.group(1), DATE_FMT).strftime("%Y-%m-%dT%H:%M:%SZ") if edit else None,
            "edited_by": edit.group(2) if edit else None,
        }


def main():
    os.makedirs(RAW, exist_ok=True)
    posts = [json.loads(l) for l in open(INP)]
    by_topic = defaultdict(set)
    for p in posts:
        by_topic[p["topic_id"]].add(p["msg_id"])
    result = json.load(open(OUT)) if os.path.exists(OUT) else {}
    s = requests.Session()
    s.headers["User-Agent"] = UA
    n_req = 0
    for topic in sorted(by_topic):
        pending = sorted(m for m in by_topic[topic] if str(m) not in result)
        tries = 0
        while pending and tries < 50:
            tries += 1
            msg = pending[0]
            path = os.path.join(RAW, f"t{topic}_m{msg}.html")
            if os.path.exists(path):
                html = open(path, encoding="latin-1").read()
            else:
                url = f"https://bitcointalk.org/index.php?topic={topic}.msg{msg}"
                r = s.get(url, timeout=60)
                n_req += 1
                if r.status_code != 200:
                    print("HTTP", r.status_code, url, file=sys.stderr, flush=True)
                    time.sleep(30)
                    continue
                with open(path, "wb") as f:
                    f.write(r.content)
                with open(path + ".meta.json", "w") as f:
                    json.dump({"url": url, "fetched_utc": datetime.now(timezone.utc).isoformat(),
                               "http_date": r.headers.get("Date")}, f)
                html = r.content.decode("latin-1")
                time.sleep(DELAY)
            found = False
            for rec in parse_page(html):
                if int(rec["msg_id"]) in by_topic[topic] and rec["poster"] == "satoshi":
                    rec["page"] = os.path.relpath(path, ROOT)
                    result[rec["msg_id"]] = rec
                    found = found or int(rec["msg_id"]) == msg
            if not found:
                result[str(msg)] = {"msg_id": str(msg), "error": "msg not found on page", "page": os.path.relpath(path, ROOT)}
            pending = sorted(m for m in by_topic[topic] if str(m) not in result)
            if n_req % 20 == 0:
                json.dump(result, open(OUT, "w"), indent=1)
                print(n_req, "requests,", len(result), "msgs done", flush=True)
    json.dump(result, open(OUT, "w"), indent=1)
    print("done:", n_req, "requests,", len(result), "msgs,", sum(1 for v in result.values() if v.get("last_edit_raw")), "edited")


if __name__ == "__main__":
    main()
