#!/usr/bin/env python3
"""Parse Satoshi's posts found in the Bitcoin SourceForge project forums / project news
(Wayback captures fetched by fetch_bitcoin_list_sfforums.py) into
data/satoshi/intermediate/sourceforge_forums.jsonl.

Findings (Wayback captures, 2010-2013):
  * Project forums "Open Discussion" (forum 885783) and "Help" (885784) only ever contained the
    automatic "Welcome to ..." topics by user "nobody" (2008-11-09 18:58:15 UTC) as of July 2010:
    no Satoshi forum posts.
  * Project news: one item by SourceForge user s_nakamoto, "Bitcoin v0.1 released - P2P e-cash".
    Its timestamp is shown explicitly with a zone: "2009-01-13 20:46:54 UTC" (2010 capture),
    "2009-01-13 12:46:54 PST" (2012 capture), Atom <published>2009-01-13T20:46:54Z</published>
    (2013 capture; after SourceForge's Allura migration the feed attributes it to "Gavin
    Andresen" and the page to "Anonymous" - a migration artefact).
"""
import html as htmlmod
import json
import os
import re

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
RAW = os.path.join(ROOT, "data", "satoshi", "raw", "sourceforge_bitcoin_list", "forums")
OUT = os.path.join(ROOT, "data", "satoshi", "intermediate", "sourceforge_forums.jsonl")
REL = lambda p: os.path.relpath(p, ROOT)  # noqa: E731


def main():
    p2010 = os.path.join(RAW, "http_sourceforge.net_80_news_group_id_244765_20100716175339.html")
    p2012 = os.path.join(RAW, "news_group_id_244765_id_258322_20120612075923.html")
    patom = os.path.join(RAW, "http_sourceforge.net_80_p_bitcoin_news_feed.atom_20130419104742.html")
    s = open(p2010, encoding="utf-8", errors="replace").read()
    m = re.search(r'<h4 class="icon news-icon">(.*?)</h4>\s*<p>(.*?)</p>\s*<p class="meta">(.*?) by <a href="/users/s_nakamoto/"', s, re.S)
    title, body_html, ts_raw = htmlmod.unescape(m.group(1)), m.group(2), m.group(3).strip()
    text = re.sub(r"<br />\n", "\n", body_html)
    text = re.sub(r"<a [^>]*>(.*?)</a>", r"\1", text, flags=re.S)
    text = htmlmod.unescape(re.sub(r"<[^>]+>", "", text))
    if not text.endswith("\n"):
        text += "\n"
    others = []
    if os.path.exists(p2012):
        m2 = re.search(r"(\d{4}-\d\d-\d\d \d\d:\d\d:\d\d [A-Z]{3}) by", open(p2012, encoding="utf-8", errors="replace").read())
        if m2:
            others.append({"label": "SourceForge legacy news page, 2012 capture", "raw": m2.group(1), "utc": "2009-01-13T20:46:54Z"})
    if os.path.exists(patom):
        a = open(patom, encoding="utf-8", errors="replace").read()
        m3 = re.search(r"<title>Bitcoin v0.1 released - P2P e-cash</title>.*?<published>(.*?)</published>", a, re.S)
        if m3:
            others.append({"label": "SourceForge Allura news Atom feed <published>, 2013 capture", "raw": m3.group(1), "utc": m3.group(1)})
    item = {
        "id": "sourceforge-news-bitcoin-v01-released",
        "source_type": "forum",
        "venue": "SourceForge project news (sourceforge.net/projects/bitcoin, news item by user s_nakamoto)",
        "recipient": None,
        "thread": title,
        "timestamp_utc": "2009-01-13T20:46:54Z",
        "timestamp_raw": ts_raw,
        "timestamp_precision": "second",
        "timestamp_source": "SourceForge news page 'meta' line (explicit UTC), 2010 Wayback capture",
        "timestamp_tz_raw": "UTC",
        "timestamps_other": others,
        "url": "http://sourceforge.net/news/?group_id=244765",
        "url_allura": "https://sourceforge.net/p/bitcoin/news/2009/01/bitcoin-v01-released---p2p-e-cash/",
        "raw_path": REL(p2010),
        "text": text,
        "text_raw": text,
        "html_raw": body_html,
        "whitespace_preserved": "partial",
        "whitespace_notes": ("HTML source keeps the double spaces after full stops (browsers collapse them on "
                             "display) and line breaks as <br />; every line in the source ends with ' <br />' "
                             "so most lines of text_raw end with a trailing space (SourceForge nl2br artefact or "
                             "original trailing spaces - cannot tell)."),
        "from_address": None,
        "author_account": "s_nakamoto (SourceForge; display name 'Satoshi Nakamoto')",
        "message_id": "sourceforge news id 258322 (legacy)",
        "in_reply_to": None,
        "subject": title,
        "notes": ("Project news post on SourceForge. Text is essentially the 'Bitcoin v0.1 released' announcement "
                  "Satoshi mailed to the cryptography list on 2009-01-08, re-posted as SF news on 2009-01-13. "
                  "After SourceForge's 2013 Allura migration the same item is attributed to 'Anonymous' (page) "
                  "/ 'Gavin Andresen' (feed) - migration artefact, the 2010/2012 legacy pages show s_nakamoto. "
                  "No Satoshi posts exist in the project's SF forums (only auto-created welcome topics)."),
    }
    with open(OUT, "w") as f:
        f.write(json.dumps(item, ensure_ascii=False) + "\n")
    print("wrote 1 item to", REL(OUT), item["timestamp_utc"], "|", ts_raw)


if __name__ == "__main__":
    main()
