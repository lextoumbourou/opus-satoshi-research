#!/usr/bin/env python3
"""Parse bitcointalk showPosts pages (fetched by fetch_bitcointalk.py) into normalised records.

Time zone: bitcointalk (SMF 1.1.19) renders times in the viewer's zone. For a guest (no login),
the forum header clock on every fetched page equals the HTTP `Date:` response header to the second
(checked for every page below), so guest display zone = UTC (+00:00, no DST). Timestamps shown on
posts are therefore UTC. SMF stores post times as unix epochs, so this conversion is exact.

Whitespace: SMF stores BBCode and renders it to HTML. It converts a run of two spaces to
" &nbsp;" / "&nbsp; " and a leading space after a line break to "&nbsp;", newlines to "<br />",
and wraps tabs in <span style="white-space: pre;">. So the HTML *does* preserve the number of
spaces: we reconstruct text by mapping <br /> -> "\\n" and &nbsp; -> " ". The exact served HTML of
each post is kept in `html_raw`.

Edit times ("Last Edit: ...") are not shown in showPosts; see fetch_bitcointalk_topics.py.

Output: data/satoshi/intermediate/bitcointalk.jsonl
"""
import email.utils
import glob
import html
import json
import os
import re
from datetime import datetime, timezone

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
RAW = os.path.join(ROOT, "data", "satoshi", "raw", "bitcointalk")
OUT = os.path.join(ROOT, "data", "satoshi", "intermediate", "bitcointalk.jsonl")
EDITS = os.path.join(ROOT, "data", "satoshi", "intermediate", "bitcointalk_edits.json")

SMILEYS = {"Smiley": ":)", "Wink": ";)", "Cheesy": ":D", "Grin": ";D", "Angry": ">:(", "Sad": ":(",
           "Shocked": ":o", "Cool": "8)", "Huh": "???", "Roll Eyes": "::)", "Tongue": ":P",
           "Embarrassed": ":-[", "Lips sealed": ":-X", "Undecided": ":-\\", "Kiss": ":-*", "Cry": ":'("}
DATE_FMT = "%B %d, %Y, %I:%M:%S %p"


def extract_div(s, start):
    """Given index of '<div', return (end_index_after_closing_div, inner_html)."""
    depth = 0
    i = start
    open_end = s.index(">", start) + 1
    for m in re.finditer(r"<div\b|</div>", s[start:]):
        tok = m.group(0)
        depth += 1 if tok.startswith("<div") else -1
        if depth == 0:
            end = start + m.end()
            return end, s[open_end:start + m.start()]
    raise ValueError("unbalanced div")


def html_to_text(h, keep_quotes=True):
    """Convert SMF post HTML to BBCode-ish plain text, preserving whitespace."""
    out = []
    pos = 0
    pending_quote_header = False
    while True:
        m = re.search(r'<div class="(quoteheader|quote|codeheader|code)">', h[pos:])
        if not m:
            out.append(inline(h[pos:]))
            break
        a = pos + m.start()
        out.append(inline(h[pos:a]))
        end, inner = extract_div(h, a)
        cls = m.group(1)
        if cls == "quoteheader":
            hdr = html.unescape(re.sub(r"<[^>]+>", "", inner)).replace("\xa0", " ")
            if keep_quotes:
                mm = re.match(r"Quote from: (.*) on (.*)$", hdr)
                if mm:
                    out.append(f"[quote author={mm.group(1)} date={mm.group(2)}]")
                else:
                    out.append(f"[quote {hdr}]" if hdr.strip() != "Quote" else "[quote]")
            pending_quote_header = True
        elif cls == "quote":
            if keep_quotes:
                # a quote without a preceding header (plain [quote])
                if not pending_quote_header:
                    out.append("[quote]")
                out.append(html_to_text(inner, keep_quotes=True))
                out.append("[/quote]")
        if cls != "quoteheader":
            pending_quote_header = False
        if cls == "codeheader":
            pass
        elif cls == "code":
            out.append("[code]" + inline(inner) + "[/code]")
        pos = end
    return "".join(out)


def inline(h):
    h = h.replace("\r", "")
    h = re.sub(r"<br\s*/?>", "\n", h)

    def img(m):
        tag = m.group(0)
        alt = re.search(r'alt="([^"]*)"', tag)
        src = re.search(r'src="([^"]*)"', tag)
        if alt and alt.group(1) in SMILEYS:
            return SMILEYS[alt.group(1)]
        return f"[img]{src.group(1) if src else ''}[/img]"

    h = re.sub(r"<img\b[^>]*>", img, h)

    def link(m):
        href = html.unescape(m.group(1))
        txt = html.unescape(re.sub(r"<[^>]+>", "", m.group(2)))
        if txt.replace("\xa0", " ").strip() == href.strip():
            return m.group(2)
        return f"[url={href}]" + m.group(2) + "[/url]"

    h = re.sub(r'<a\b[^>]*href="([^"]*)"[^>]*>(.*?)</a>', link, h, flags=re.S)
    h = re.sub(r"<li>", "[*]", h)
    h = re.sub(r"<[^>]+>", "", h)
    h = html.unescape(h).replace("\xa0", " ")
    return h


def check_display_zone():
    """Compare page-header clock with HTTP Date header for each fetched page."""
    res = []
    for p in sorted(glob.glob(os.path.join(RAW, "showposts", "start_*.html"))):
        s = open(p, encoding="latin-1").read()
        meta = json.load(open(p + ".meta.json"))
        m = re.search(r'<span class="smalltext">([A-Z][a-z]+ \d\d, \d{4}, \d\d:\d\d:\d\d [AP]M)</span>', s)
        shown = datetime.strptime(m.group(1), DATE_FMT)
        http = email.utils.parsedate_to_datetime(meta["http_date"]).astimezone(timezone.utc).replace(tzinfo=None)
        res.append((os.path.basename(p), m.group(1), meta["http_date"], (shown - http).total_seconds()))
    return res


def main():
    zone = check_display_zone()
    offsets = sorted(set(round(x[3] / 60) for x in zone))
    print("page-clock minus HTTP Date (minutes):", offsets)
    assert offsets == [0], zone

    edits = json.load(open(EDITS)) if os.path.exists(EDITS) else {}
    sni = json.load(open(os.path.join(ROOT, "data", "satoshi", "raw", "sni-repo", "server", "data", "forum_posts.json")))
    sni_by_msg = {}
    for x in sni:
        m = re.search(r"msg(\d+)", x["url"])
        if m and x.get("satoshi_id"):
            sni_by_msg[m.group(1)] = x

    rows = {}
    for p in sorted(glob.glob(os.path.join(RAW, "showposts", "start_*.html"))):
        s = open(p, encoding="latin-1").read()
        meta = json.load(open(p + ".meta.json"))
        for m in re.finditer(r'<tr class="titlebg2">(.*?)</tr>', s, re.S):
            hdr = m.group(1)
            links = re.findall(r'<a href="([^"]+)">(.*?)</a>', hdr)
            topic_link = [l for l in links if "topic=" in l[0]]
            if not topic_link:
                continue
            turl, subj = topic_link[-1]
            tm = re.search(r"topic=(\d+)\.msg(\d+)", turl)
            topic, msg = tm.group(1), tm.group(2)
            board = " / ".join(html.unescape(t) for u, t in links if "topic=" not in u)
            dm = re.search(r"on: ([A-Z][a-z]+ \d\d, \d{4}, \d\d:\d\d:\d\d [AP]M)", hdr)
            raw_ts = dm.group(1)
            utc = datetime.strptime(raw_ts, DATE_FMT).strftime("%Y-%m-%dT%H:%M:%SZ")
            dpos = s.index('<div class="post">', m.end())
            _, inner = extract_div(s, dpos)
            text_raw = html_to_text(inner, keep_quotes=True)
            text = html_to_text(inner, keep_quotes=False)
            text = re.sub(r"\n{3,}", "\n\n", text).strip("\n")
            sn = sni_by_msg.get(msg)
            notes = []
            others = []
            if sn:
                if sn["date"] != utc:
                    notes.append(f"SNI date {sn['date']} differs from bitcointalk display {utc}.")
                others.append({"label": "Satoshi Nakamoto Institute forum_posts.json date", "raw": sn["date"], "utc": sn["date"]})
            else:
                notes.append("Not in Satoshi Nakamoto Institute forum_posts.json.")
            e = edits.get(msg)
            if e and e.get("last_edit_raw"):
                others.append({"label": "bitcointalk 'Last Edit' (topic view; last edit only, display zone UTC)",
                               "raw": e["last_edit_raw"], "utc": e["last_edit_utc"], "edited_by": e.get("edited_by")})
            embedded = [
                {"kind": "diff -u file header (local mtime of the poster's file, zone not stated)",
                 "marker": mm.group(1), "file": mm.group(2), "raw": mm.group(3)}
                for mm in re.finditer(r"(---|\+\+\+) (\S+)[ \t]+(\w{3} \w{3} [ \d]\d \d\d:\d\d:\d\d \d{4})", text)]
            if embedded:
                notes.append("Post contains diff headers with local file modification times (see embedded_local_timestamps); "
                             "compare with the post time and any Last Edit time.")
            rows[msg] = {
                "id": f"bitcointalk-msg{msg}",
                "source_type": "forum",
                "venue": "bitcointalk.org" + (f" ({board})" if board else ""),
                "recipient": None,
                "thread": html.unescape(re.sub(r"^Re: ", "", subj)),
                "subject": html.unescape(subj),
                "timestamp_utc": utc,
                "timestamp_raw": raw_ts,
                "timestamp_precision": "second",
                "timestamp_source": "bitcointalk post time as displayed to a guest (display zone verified = UTC; SMF stores unix epoch)",
                "timestamp_tz_raw": None,
                "timestamps_other": others,
                "url": f"https://bitcointalk.org/index.php?topic={topic}.msg{msg}#msg{msg}",
                "raw_path": os.path.relpath(p, ROOT),
                "text": text,
                "text_raw": text_raw,
                "html_raw": inner,
                "whitespace_preserved": True,
                "whitespace_notes": "Reconstructed from SMF HTML: <br /> -> newline, &nbsp; -> space (SMF encodes each extra space as &nbsp;, so space runs survive). Quotes rendered as [quote author=.. date=..]..[/quote], code as [code]..[/code], links whose text differs from the URL as [url=..]..[/url]; smiley images mapped back to their codes. Original BBCode source is not available to guests.",
                "topic_id": int(topic),
                "msg_id": int(msg),
                "fetched_utc": meta["fetched_utc"],
                "sni_satoshi_id": sn.get("satoshi_id") if sn else None,
                "embedded_local_timestamps": embedded or None,
                "notes": " ".join(notes),
            }
    out = sorted(rows.values(), key=lambda r: (r["timestamp_utc"], r["msg_id"]))
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as f:
        for r in out:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    with open(os.path.join(RAW, "display_zone_check.tsv"), "w") as f:
        f.write("page\theader_clock_shown\thttp_date\tdiff_seconds\n")
        for z in zone:
            f.write("\t".join(map(str, z)) + "\n")
    n_diff = sum(1 for r in out if "differs" in r["notes"])
    n_missing = sum(1 for r in out if "Not in Satoshi" in r["notes"])
    sni_msgs = set(sni_by_msg) - set(rows)
    print(len(out), "posts;", n_diff, "date differs from SNI;", n_missing, "not in SNI;",
          len(sni_msgs), "SNI bitcointalk msgs not found in showPosts:", sorted(sni_msgs)[:20])


if __name__ == "__main__":
    main()
