#!/usr/bin/env python3
"""Minimal web search via DuckDuckGo's HTML endpoint (used after the session's
WebSearch budget ran out). Usage: ddg.py "query" [max]"""
import sys, re, html, urllib.parse, urllib.request
q = sys.argv[1]; n = int(sys.argv[2]) if len(sys.argv) > 2 else 10
req = urllib.request.Request("https://html.duckduckgo.com/html/?" + urllib.parse.urlencode({"q": q}),
    headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/128 Safari/537.36"})
t = urllib.request.urlopen(req, timeout=30).read().decode("utf-8", "replace")
for m in list(re.finditer(r'<a rel="nofollow" class="result__a" href="([^"]+)">(.*?)</a>.*?<a class="result__snippet"[^>]*>(.*?)</a>', t, re.S))[:n]:
    url = m.group(1)
    if "uddg=" in url:
        url = urllib.parse.unquote(re.search(r"uddg=([^&]+)", url).group(1))
    strip = lambda s: html.unescape(re.sub(r"<[^>]+>", "", s)).strip()
    print(f"- {strip(m.group(2))}\n  {url}\n  {strip(m.group(3))[:220]}")
