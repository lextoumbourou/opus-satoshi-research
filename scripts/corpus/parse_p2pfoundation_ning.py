#!/usr/bin/env python3
"""Parse Satoshi Nakamoto's posts on the P2P Foundation Ning network from Wayback captures
(fetched by fetch_p2pfoundation_ning.py) into data/satoshi/intermediate/p2pfoundation_ning.jsonl.

Timestamps: Ning shows only a minute-precision local clock time with no zone label. The display
zone was established empirically as UTC (+00:00, see README / notes field) from captures that
show *relative* times ("N minutes/hours ago") next to posts whose absolute times are shown in
other captures:
  * capture 2009-02-21T02:48:57Z shows Sepp Hasslberger's reply as "17 hours ago"; the same reply
    is displayed as "February 20, 2009 at 8:53am" -> 17h56m earlier if the display is UTC (ok);
    UTC+1 would make it 18h56m, US Pacific 9h56m (both inconsistent);
  * capture 2014-03-07T02:12:21Z shows Satoshi's "I am not Dorian Nakamoto" reply as
    "54 minutes ago"; displayed elsewhere as "March 7, 2014 at 1:17" -> posted 01:17:22-01:17:59
    UTC if display is UTC (ok). Capture 2014-03-07T10:52:00Z shows "9 hours ago" for it and
    "7 hours ago"/"6 hours ago" for replies displayed at 3:36 / 4:34 (all consistent with UTC);
  * the first Ning post (22:27) was mailed by Satoshi to the p2p-research list with
    Date: Wed, 11 Feb 2009 22:30:54 +0000 (3-4 minutes later), again consistent with UTC.
All four posts fall outside northern-hemisphere DST, so UTC and Europe/London coincide.

Whitespace: Ning stored/rendered the text with single spaces after full stops (the email copy
of the same announcement has two), so Ning does NOT preserve Satoshi's spacing.
"""
import html as htmlmod
import json
import os
import re
from datetime import datetime, timedelta, timezone

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
RAW = os.path.join(ROOT, "data", "satoshi", "raw", "p2pfoundation")
SNI = os.path.join(ROOT, "data", "satoshi", "raw", "sni-repo", "server", "data", "forum_posts.json")
OUT = os.path.join(ROOT, "data", "satoshi", "intermediate", "p2pfoundation_ning.jsonl")
TOPIC_URL = "http://p2pfoundation.ning.com/forum/topics/bitcoin-open-source"
REL = lambda p: os.path.relpath(p, ROOT)  # noqa: E731


def html_to_text(frag):
    t = frag.strip()
    t = re.sub(r"<br\s*/?>\s*\n?", "\n", t)
    t = re.sub(r"</p>\s*<p[^>]*>", "\n\n", t)
    t = re.sub(r"</?p[^>]*>", "", t)
    t = re.sub(r"<a [^>]*>(.*?)</a>", r"\1", t, flags=re.S)
    t = re.sub(r"</?div[^>]*>", "", t)
    t = re.sub(r"<[^>]+>", "", t)
    t = htmlmod.unescape(t)
    return t.strip() + "\n"


def parse_ning_time(raw):
    raw = raw.strip()
    for fmt in ("%d %B %Y at %I:%M%p", "%B %d, %Y at %I:%M%p", "%B %d, %Y at %H:%M"):
        try:
            return datetime.strptime(raw, fmt).replace(tzinfo=timezone.utc)
        except ValueError:
            pass
    raise ValueError(raw)


def comment_block(s, cid):
    """Return (timestamp_text, body_html) for comment id cid in a Ning topic page."""
    i = s.find(f'name="2003008:Comment:{cid}"')
    if i < 0:
        return None, None
    seg = s[i:i + 20000]
    ts = re.search(r'<span class="timestamp">([^<]+)</span>', seg).group(1)
    m = re.search(rf'<div class="description" id="desc_2003008Comment{cid}">(.*?)</div>\s*</dd>', seg, re.S)
    body = m.group(1)
    body = re.sub(r'^\s*<div class="xg_user_generated">(.*)</div>\s*$', r"\1", body, flags=re.S)
    return ts, body


def main():
    sni = [p for p in json.load(open(SNI)) if "p2pfoundation" in p["url"] and p.get("satoshi_id")]
    sni_by_url = {p["url"]: p for p in sni}
    cap2009 = os.path.join(RAW, "topic", "main_20090221024857.html")
    cap2011 = os.path.join(RAW, "topic", "main_20110415095236.html")
    cap2024 = os.path.join(RAW, "topic", "main_20240701162653.html")
    capd1 = os.path.join(RAW, "topic", "comment52186_20140307021221.html")
    capd2 = os.path.join(RAW, "topic", "comment52186_20140307105200.html")
    capd3 = os.path.join(RAW, "topic", "comment52186_20140402054325.html")
    rd = lambda p: open(p, encoding="utf-8", errors="replace").read()  # noqa: E731
    s09, s11, s24 = rd(cap2009), rd(cap2011), rd(cap2024)
    ws_note = ("Ning stored/rendered the text with single spaces between sentences (0 occurrences of "
               "'.  ' in the raw HTML source; the p2p-research email copy of the 11 Feb 2009 "
               "announcement has double spaces), so Ning does NOT preserve Satoshi's original "
               "spacing. Line breaks are <br /> in the source and are converted to \\n here.")
    tz_note = ("Ning displays minute-precision local time without a zone label; display zone determined "
               "to be UTC from relative-time captures (see scripts/corpus/parse_p2pfoundation_ning.py "
               "docstring and README).")
    items = []

    # 1. Topic starter
    m = re.search(r'Posted by </a><a [^>]*>Satoshi Nakamoto</a><a class="nolink"> on ([^<]+)</a>', s09)
    ts09 = m.group(1).strip()
    body = re.search(r'<div class="discussion">\s*<div class="description">(.*?)</div>\s*</div>', s09, re.S).group(1)
    ts11 = re.search(r'Posted by </a><a [^>]*>Satoshi Nakamoto</a><a class="nolink"> on ([^<]+?)(?: in )?</a>', s11)
    ts24 = re.search(r'Posted by </a><a [^>]*>Satoshi Nakamoto</a><a class="nolink"> on ([^<]+?)(?: in )?</a>', s24)
    dt = parse_ning_time(ts09)
    p = sni_by_url.get(TOPIC_URL)
    items.append({
        "id": "p2pfoundation-ning-topic-9402",
        "comment_id": "2003008:Topic:9402",
        "raw": (cap2009, ts09, body),
        "others": [("Ning display in Wayback capture 2011-04-15", ts11.group(1) if ts11 else None),
                   ("Ning display in Wayback capture 2024-07-01", ts24.group(1) if ts24 else None)],
        "url": TOPIC_URL, "sni": p, "dt": dt,
        "notes": ("Same announcement text was emailed by Satoshi to the p2p-research list "
                  "(p2p-research-001347, Date: Wed, 11 Feb 2009 22:30:54 +0000), ~4 min after the "
                  "Ning timestamp."),
    })
    # 2/3. Replies of Feb 2009
    for cid in ("9493", "9562"):
        ts, body = comment_block(s09, cid)
        t11, _ = comment_block(s11, cid)
        t24, _ = comment_block(s24, cid)
        url = f"http://p2pfoundation.ning.com/xn/detail/2003008:Comment:{cid}"
        items.append({
            "id": f"p2pfoundation-ning-comment-{cid}", "comment_id": f"2003008:Comment:{cid}",
            "raw": (cap2009, ts, body),
            "others": [("Ning display in Wayback capture 2011-04-15", t11),
                       ("Ning display in Wayback capture 2024-07-01", t24)],
            "url": url, "sni": sni_by_url.get(url), "dt": parse_ning_time(ts), "notes": None,
        })
    # 4. 2014 "I am not Dorian Nakamoto"
    ts, body = comment_block(rd(capd3), "52186")
    rel1, _ = comment_block(rd(capd1), "52186")
    rel2, _ = comment_block(rd(capd2), "52186")
    url = "http://p2pfoundation.ning.com/xn/detail/2003008:Comment:52186"
    items.append({
        "id": "p2pfoundation-ning-comment-52186", "comment_id": "2003008:Comment:52186",
        "raw": (capd3, ts, body),
        "others": [("Ning relative time in Wayback capture 2014-03-07T02:12:21Z (=> posted 01:17:22-01:18:21Z)", rel1),
                   ("Ning relative time in Wayback capture 2014-03-07T10:52:00Z (=> posted 00:52-01:52Z)", rel2)],
        "url": url, "sni": sni_by_url.get(url), "dt": parse_ning_time(ts),
        "notes": ("Posted years after Satoshi's last generally-accepted communications (Apr 2011), the day "
                  "after Newsweek's 6 Mar 2014 'Dorian Nakamoto' article; authenticity disputed (the "
                  "account's email satoshin@gmx.com was later compromised, Sept 2014). Treat separately "
                  "from 2008-2011 material. Combining the absolute display ('1:17') with the 02:12:21Z "
                  "capture showing '54 minutes ago' narrows the posting time to 01:17:22-01:17:59 UTC."),
    })

    out = []
    for it in items:
        path, ts_raw, body_html = it["raw"]
        text = html_to_text(body_html)
        others = [{"label": lab, "raw": raw, "utc": None} for lab, raw in it["others"] if raw]
        sni = it["sni"]
        notes = [it["notes"]] if it["notes"] else []
        if sni:
            others.append({"label": "Nakamoto Institute forum_posts.json date", "raw": sni["date"], "utc": sni["date"]})
            if sni["date"] != it["dt"].strftime("%Y-%m-%dT%H:%M:%SZ"):
                notes.append(f"SNI date {sni['date']} differs from parsed Ning display.")
        out.append({
            "id": it["id"],
            "source_type": "p2pfoundation",
            "venue": "p2pfoundation.ning.com forum (P2P Foundation Ning network)",
            "recipient": None,
            "thread": "Bitcoin open source implementation of P2P currency",
            "timestamp_utc": it["dt"].strftime("%Y-%m-%dT%H:%M:%SZ"),
            "timestamp_raw": ts_raw.strip(),
            "timestamp_precision": "minute",
            "timestamp_source": "Ning page display (Wayback capture), zone determined = UTC",
            "timestamp_tz_raw": None,
            "timestamps_other": others,
            "url": it["url"],
            "raw_path": REL(path),
            "text": text,
            "text_raw": text,
            "html_raw": body_html.strip(),
            "whitespace_preserved": False,
            "whitespace_notes": ws_note,
            "from_address": None,
            "author_profile": "http://p2pfoundation.ning.com/profile/SatoshiNakamoto (Ning user id 0ye0gncqg772o)",
            "message_id": it["comment_id"],
            "in_reply_to": None if "Topic" in it["comment_id"] else "2003008:Topic:9402",
            "subject": "Bitcoin open source implementation of P2P currency",
            "notes": " ".join(notes + [tz_note]),
        })
    with open(OUT, "w") as f:
        for o in out:
            f.write(json.dumps(o, ensure_ascii=False) + "\n")
    print(f"wrote {len(out)} items to {REL(OUT)}")
    for o in out:
        print(o["id"], o["timestamp_utc"], "|", o["timestamp_raw"], "|", o["text"][:60].replace("\n", " "))


if __name__ == "__main__":
    main()
