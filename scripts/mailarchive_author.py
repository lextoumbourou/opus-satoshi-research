#!/usr/bin/env python3
"""Collect all posts by an author on a mail-archive.com list via its search,
then fetch each message page to get the original Date header (with the
sender's time-zone offset). Polite: 1.5 s between requests.

Usage: mailarchive_author.py LIST_ADDRESS "Author Name" OUT.json
"""
import sys, re, html, json, time, urllib.parse, urllib.request
UA = {"User-Agent": "Mozilla/5.0 (research; low volume)"}
lst, author, out = sys.argv[1], sys.argv[2], sys.argv[3]
def get(url):
    for i in range(4):
        try:
            return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60).read().decode("utf-8", "replace")
        except Exception as e:
            time.sleep(5 * (i + 1))
    return ""
items, start = [], 0
while True:
    q = urllib.parse.urlencode({"l": lst, "q": f'from:"{author}"', "o": "oldest", "start": start})
    t = get("https://www.mail-archive.com/search?" + q)
    found = re.findall(r'<span class=subject><a href="([^"]+)">(.*?)</a></span>', t)
    if not found:
        break
    for href, subj in found:
        items.append({"href": "https://www.mail-archive.com" + href, "subject": html.unescape(subj)})
    start += 100
    time.sleep(1.5)
    if len(found) < 100:
        break
for it in items:
    t = get(it["href"])
    d = re.search(r'<span class="date"><a[^>]*>(.*?)</a>', t) or re.search(r'class="date"[^>]*>(.*?)<', t)
    raw = re.search(r"Date:\s*</?[^>]*>?\s*([A-Z][a-z]{2}, \d{1,2} [A-Z][a-z]{2} \d{4} [\d:]+ [+-]\d{4})", t)
    anyhdr = re.search(r"([A-Z][a-z]{2}, \d{1,2} [A-Z][a-z]{2} \d{4} \d\d:\d\d:\d\d [+-]\d{4})", t)
    it["date_display"] = html.unescape(re.sub("<[^>]+>", "", d.group(1))).strip() if d else None
    it["date_header"] = (raw or anyhdr).group(1) if (raw or anyhdr) else None
    time.sleep(1.5)
json.dump(items, open(out, "w"), indent=1)
for it in items:
    print(it["date_header"] or it["date_display"], "|", it["subject"][:80])
print(len(items), "items")
