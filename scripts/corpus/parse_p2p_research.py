#!/usr/bin/env python3
"""Parse Satoshi Nakamoto's posts to the P2P Foundation "p2p-research" mailing list from the
pipermail monthly text archives (fetched by fetch_p2p_research.py) into
data/satoshi/intermediate/p2p_research.jsonl.

Source format: Mailman/pipermail `YYYY-Month.txt.gz`. Each message starts with an mbox-style
envelope line `From <addr> <asctime in list-server local time>`, followed by the headers
pipermail keeps (From, Date, Subject, In-Reply-To, References, Message-ID) and the decoded
plain-text body. The `Date:` header is the sender's original header (incl. its UTC offset);
pipermail does not rewrite it (cf. the metzdowd archive, which keeps Satoshi's "+0800").
Body whitespace is preserved byte-for-byte as archived (double spaces, trailing spaces from
format=flowed, space-stuffing). Non-ASCII characters were replaced by "?" by pipermail.
"""
import gzip
import json
import os
import re
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
RAW = os.path.join(ROOT, "data", "satoshi", "raw", "p2p_research")
SNI = os.path.join(ROOT, "data", "satoshi", "raw", "sni-repo", "server", "data", "emails.json")
OUT = os.path.join(ROOT, "data", "satoshi", "intermediate", "p2p_research.jsonl")
BASE_URL = "http://p2pfoundation.net/backups/p2p_research-archives/"
MONTHS = ["2009-February", "2009-March"]

ENVELOPE = re.compile(r"^From (\S+ at \S+)  ([A-Z][a-z]{2} [A-Z][a-z]{2} [ \d]\d \d\d:\d\d:\d\d \d{4})$")


def split_messages(text):
    lines = text.split("\n")
    starts = [i for i, ln in enumerate(lines) if ENVELOPE.match(ln)]
    msgs = []
    for k, st in enumerate(starts):
        end = starts[k + 1] if k + 1 < len(starts) else len(lines)
        block = lines[st:end]
        env = ENVELOPE.match(block[0])
        # headers until first blank line; continuation lines start with whitespace
        hdr_lines, i = [], 1
        while i < len(block) and block[i] != "":
            hdr_lines.append(block[i])
            i += 1
        headers, raw_headers = {}, "\n".join(hdr_lines)
        cur = None
        for hl in hdr_lines:
            if hl[:1] in (" ", "\t") and cur:
                headers[cur] += "\n" + hl
            elif ":" in hl:
                cur, v = hl.split(":", 1)
                cur = cur.strip()
                headers[cur] = v.lstrip(" ")
        body_lines = block[i + 1:]
        # pipermail separates messages with a blank line before the next envelope; drop the
        # trailing empty lines (they are archive framing, not message content).
        while body_lines and body_lines[-1] == "":
            body_lines.pop()
        msgs.append({
            "envelope_from": env.group(1), "envelope_date": env.group(2),
            "headers": headers, "raw_headers": raw_headers,
            "body": "\n".join(body_lines) + "\n",
        })
    return msgs


def strip_quotes(body):
    """Remove quoted text ('>' lines, incl. Thunderbird's ' > ' form) and the attribution line
    ('X wrote:') that introduces a quote block. Keeps Satoshi's own lines verbatim."""
    lines = body.split("\n")
    keep = []
    n = len(lines)
    for i, ln in enumerate(lines):
        if re.match(r"^\s*>", ln):
            continue
        if re.search(r"wrote:\s*$", ln):
            # attribution if the next non-empty line is a quote
            j = i + 1
            while j < n and lines[j].strip() == "":
                j += 1
            if j < n and re.match(r"^\s*>", lines[j]):
                continue
        keep.append(ln)
    while keep and not keep[0].strip():
        keep.pop(0)
    while keep and not keep[-1].strip():
        keep.pop()
    out = "\n".join(keep)
    out = re.sub(r"\n{3,}", "\n\n", out).strip("\n") + "\n"
    return out


def msgid_time(mid):
    """Mozilla/Thunderbird Message-IDs look like <4993519E.8080300@gmx.com>: the first field is the
    send time as hex Unix seconds (same clock as the Date: header). Returns ISO UTC or None."""
    m = re.match(r"<?([0-9A-F]{8})\.\d+@", mid or "")
    if not m:
        return None
    t = datetime.fromtimestamp(int(m.group(1), 16), timezone.utc)
    return t.strftime("%Y-%m-%dT%H:%M:%SZ") if 2008 <= t.year <= 2012 else None


def unmunge(addr):
    return addr.replace(" at ", "@")


def main():
    sni = {e["source_id"]: e for e in json.load(open(SNI)) if e["source"] == "p2p-research"}
    sni_satoshi = sorted((e for e in sni.values() if e["sent_from"] == "Satoshi Nakamoto"), key=lambda e: e["source_id"])
    items = []
    for m in MONTHS:
        gz = os.path.join(RAW, f"{m}.txt.gz")
        if not os.path.exists(gz):
            continue
        text = gzip.open(gz).read().decode("latin-1")
        # pipermail message numbers for Satoshi's posts, from the month's date index
        idx_path = os.path.join(RAW, m, "date.html")
        idx_nums = []
        if os.path.exists(idx_path):
            idx = open(idx_path, encoding="latin-1").read()
            for num, who in re.findall(r'<LI><A HREF="(\d+)\.html">.*?<I>(.*?)\s*</I>', idx, re.S):
                if "atoshi" in who:
                    idx_nums.append(num)
        sat = [x for x in split_messages(text) if "atoshi" in x["headers"].get("From", "")]
        for k, msg in enumerate(sat):
            h = msg["headers"]
            date_raw = h.get("Date", "").strip()
            dt = parsedate_to_datetime(date_raw).astimezone(timezone.utc)
            # envelope date is list-server local time; Feb 2009 => CET (UTC+1), no DST
            env_naive = datetime.strptime(re.sub(r"\s+", " ", msg["envelope_date"]), "%a %b %d %H:%M:%S %Y")
            env_utc = (env_naive - timedelta(hours=1)).replace(tzinfo=timezone.utc)
            num = idx_nums[k] if k < len(idx_nums) else None
            s = sni.get(num) if num else None
            others = [
                {"label": "pipermail envelope date (list server local time, CET=UTC+1 in Feb 2009)",
                 "raw": msg["envelope_date"], "utc": env_utc.strftime("%Y-%m-%dT%H:%M:%SZ")},
            ]
            notes = []
            mt = msgid_time(h.get("Message-ID"))
            if mt:
                others.append({"label": "Thunderbird Message-ID hex timestamp (sender's clock, Unix seconds)",
                               "raw": h.get("Message-ID"), "utc": mt})
            if s:
                others.append({"label": "Nakamoto Institute emails.json original_date", "raw": s.get("original_date"), "utc": None})
                others.append({"label": "Nakamoto Institute emails.json date", "raw": s["date"], "utc": s["date"]})
                sni_dt = datetime.strptime(s["date"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
                diff = (sni_dt - dt).total_seconds()
                if diff:
                    notes.append(
                        f"SNI 'date' ({s['date']}) differs from the raw Date header by {diff:+.0f} s. SNI's "
                        f"original_date '{s.get('original_date')}' is the pipermail list-server time in CET "
                        f"(=UTC+1); SNI appears to have converted it with the Europe/Berlin LMT offset (+0:53) "
                        f"instead of CET (+1:00), giving a systematic +7 min error. The raw Date header and "
                        f"the envelope time agree; use them.")
            body = msg["body"]
            items.append({
                "id": f"p2p-research-{num}" if num else f"p2p-research-{m}-{k}",
                "source_type": "mailing_list",
                "venue": "p2p-research mailing list (P2P Foundation; archive p2pfoundation.net/backups/p2p_research-archives)",
                "recipient": "p2p-research",
                "thread": re.sub(r"\s+", " ", h.get("Subject", "")).strip(),
                "timestamp_utc": dt.strftime("%Y-%m-%dT%H:%M:%SZ"),
                "timestamp_raw": date_raw,
                "timestamp_precision": "second",
                "timestamp_source": "Date: header (sender's original, preserved in pipermail .txt archive)",
                "timestamp_tz_raw": date_raw.split()[-1],
                "timestamps_other": others,
                "url": f"{BASE_URL}{m}/{num}.html" if num else f"{BASE_URL}{m}.txt.gz",
                "raw_path": os.path.relpath(gz, ROOT),
                "text": strip_quotes(body),
                "text_raw": body,
                "whitespace_preserved": True,
                "whitespace_notes": ("pipermail .txt archive body is verbatim plain text: double spaces after "
                                     "full stops preserved; lines end with a trailing space where Thunderbird "
                                     "format=flowed soft-wrapped; a line starting with an extra space is "
                                     "format=flowed space-stuffing (e.g. '  Their' = soft break after "
                                     "'accounts. ' + ' Their', i.e. a double space across the wrap). Non-ASCII "
                                     "chars were replaced with '?' by pipermail. text_raw is exactly the archived "
                                     "body; no un-flowing applied."),
                "from_address": unmunge(re.sub(r"\s*\(.*\)", "", h.get("From", "")).strip()),
                "from_raw": h.get("From"),
                "message_id": h.get("Message-ID"),
                "in_reply_to": h.get("In-Reply-To"),
                "references": re.sub(r"\s+", " ", h.get("References", "")).strip() or None,
                "subject": re.sub(r"\s+", " ", h.get("Subject", "")).strip(),
                "raw_headers": msg["raw_headers"],
                "envelope": f"From {msg['envelope_from']}  {msg['envelope_date']}",
                "notes": " ".join(notes) or None,
            })
    # coverage check against SNI
    got = {it["id"].split("-")[-1] for it in items}
    missing = [e["source_id"] for e in sni_satoshi if e["source_id"] not in got]
    if missing:
        print("WARNING: SNI Satoshi p2p-research items not found in raw archive:", missing)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as f:
        for it in items:
            f.write(json.dumps(it, ensure_ascii=False) + "\n")
    print(f"wrote {len(items)} items to {os.path.relpath(OUT, ROOT)}")
    for it in items:
        print(it["id"], it["timestamp_utc"], it["timestamp_raw"], "|", it["subject"][:60])


if __name__ == "__main__":
    main()
