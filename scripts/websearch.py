#!/usr/bin/env python3
"""Web search via Brave Search's HTML results page, used after the session's
built-in WebSearch budget ran out. Low volume only.

Usage: websearch.py "query" [max_results]
"""
import html
import re
import sys
import time
import urllib.parse
import urllib.request

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"


def strip(s):
    return html.unescape(re.sub(r"<[^>]+>", "", s or "")).strip()


def search(q, n=10):
    url = "https://search.brave.com/search?" + urllib.parse.urlencode({"q": q, "source": "web"})
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "en-US,en;q=0.9"})
    t = urllib.request.urlopen(req, timeout=40).read().decode("utf-8", "replace")
    blocks = t.split('data-type="web"')[1:]
    out = []
    for blk in blocks:
        blk = blk[:6000]
        u = re.search(r'<a href="(https?://[^"]+)"', blk)
        ti = re.search(r'class="title[^"]*"[^>]*>(.*?)</div>', blk, re.S)
        sn = re.search(r'class="(?:snippet-description|generic-snippet)[^"]*"[^>]*>(.*?)</(?:div|p)>', blk, re.S)
        if u:
            out.append((strip(ti.group(1)) if ti else "", u.group(1), strip(sn.group(1)) if sn else ""))
    return out[:n]


if __name__ == "__main__":
    q = sys.argv[1]
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    for t, u, s in search(q, n):
        print(f"- {t}\n  {u}\n  {s[:260]}")
    time.sleep(1.5)
