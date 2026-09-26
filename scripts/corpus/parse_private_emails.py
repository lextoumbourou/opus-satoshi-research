#!/usr/bin/env python3
"""Normalise Satoshi's published PRIVATE emails into data/satoshi/intermediate/private_emails.jsonl.

Run scripts/corpus/fetch_private_emails.py first. Only messages WRITTEN BY SATOSHI are emitted.

Sources (see README / the report for provenance):
  malmi       Martti Malmi's 2024 publication (HTML <pre>, Date: headers with offsets)
  trammell    Dustin Trammell's raw .mbox files (full headers incl. Received:)
  hal_finney  CoinDesk 2020 raw-mbox screenshots (manually transcribed) + WSJ 2014 PDF (Gmail forwards)
  adam_back   COPA v Wright exhibit AB1 (Outlook print, explicit UTC offsets)
  wei_dai     gwern.net code blocks (Outlook Express "Sent:" lines, zone not stated)
  hearn       2017 pastebin text dumps (Gmail forward format) + plan99.net Gmail print views
  andresen    Gavin Andresen's 2022 blog post (MediaWiki wikitext)
  matonis     Jon Matonis' 2012 forum post (Wayback) or secondary transcription
  hanyecz     Nathaniel Popper's 2015 r/Bitcoin post (Wayback)

Timestamp policy
  timestamp_utc is filled when the zone is stated in the source (timezone_basis="explicit") or can be
  inferred from cross-checks (timezone_basis="inferred"; evidence in timestamp_source). When only the
  publisher's likely zone is known (timezone_basis="assumed") timestamp_utc is filled under that
  assumption and flagged; when nothing is known (timezone_basis="unknown") timestamp_utc is null and
  the naive local value is kept in timestamp_local_naive.
"""
import email
import email.utils
import glob
import html
import json
import mailbox
import os
import quopri
import re
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

import fitz  # PyMuPDF

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
RAW = os.path.join(ROOT, "data", "satoshi", "raw", "private_emails")
OUT_DIR = os.path.join(ROOT, "data", "satoshi", "intermediate")
OUT = os.path.join(OUT_DIR, "private_emails.jsonl")

FIELDS = [
    "id", "source_type", "venue", "correspondent", "recipient", "thread", "subject",
    "timestamp_utc", "timestamp_raw", "timestamp_precision", "timestamp_source", "timestamp_tz_raw",
    "timezone_basis", "timestamp_local_naive", "timestamps_other",
    "url", "raw_path", "from_address", "to_address", "cc_address", "message_id", "in_reply_to",
    "text", "text_raw", "whitespace_preserved", "whitespace_notes",
    "duplicate_of_public", "also_published_at", "notes",
]


def rel(p):
    return os.path.relpath(p, ROOT)


def iso(dt):
    return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def offset_str(dt):
    off = dt.utcoffset()
    if off is None:
        return None
    mins = int(off.total_seconds() // 60)
    sign = "+" if mins >= 0 else "-"
    mins = abs(mins)
    return f"{sign}{mins // 60:02d}{mins % 60:02d}"


def rfc_dt(s):
    """Parse an RFC 2822 date string; returns aware datetime or None."""
    try:
        dt = email.utils.parsedate_to_datetime(s.strip())
    except Exception:
        return None
    if dt is not None and dt.tzinfo is None:
        # RFC 2822 "-0000" = UTC time, local zone unknown (qmail writes this); Python returns it naive
        if re.search(r"-0000\s*$", s.strip()):
            return dt.replace(tzinfo=timezone.utc)
        return None
    return dt


def received_hops(msg):
    """List of {label, raw, utc} for Received: headers (top = last hop) and the mbox From_ line."""
    out = []
    for h in msg.get_all("Received", []) or []:
        h1 = " ".join(str(h).split())
        m = re.search(r";\s*(.+)$", h1)
        raw = m.group(1).strip() if m else None
        dt = rfc_dt(re.sub(r"\s*\(.*?\)\s*$", "", raw)) if raw else None
        by = re.search(r"\bby\s+([\w.-]+)", h1)
        label = "Received by " + by.group(1) if by else "Received: " + h1.split(";")[0][:40]
        out.append({"label": label, "raw": raw,
                    "utc": iso(dt) if dt else None, "header": h1})
    return out


ATTRIB = re.compile(r"(wrote|writes):\s*$|^\s*Quoting .*:\s*$")


FWD = re.compile(r"^\s*-{3,}\s*(Original Message|Forwarded message)\s*-{3,}\s*$", re.I)
PGP = re.compile(r"-----BEGIN PGP [A-Z ]+-----.*?-----END PGP [A-Z ]+-----\n?", re.S)


def strip_quotes(text, extra_quote_pred=None, cut_at_first_quote=False):
    """Remove quoted material ('>' and '| ' prefixed lines, attribution lines introducing them),
    forwarded messages ('-------- Original Message --------' to the end) and PGP armour blocks."""
    text = PGP.sub("", text)
    lines = text.split("\n")
    # forwarded message -> drop everything from the separator on
    for i, l in enumerate(lines):
        if FWD.match(l):
            lines = lines[:i]
            break
    # attribution immediately followed by another attribution = nested forward of someone else's reply
    for i, l in enumerate(lines):
        if ATTRIB.search(l):
            j = i + 1
            while j < len(lines) and lines[j].strip() == "":
                j += 1
            if j < len(lines) and ATTRIB.search(lines[j]) and not lines[j].lstrip().startswith(">"):
                lines = lines[:i]
                break
    if cut_at_first_quote:
        for i, l in enumerate(lines):
            if l.startswith(">"):
                lines = lines[:i]
                break
    keep = [True] * len(lines)

    def is_q(i):
        l = lines[i]
        if re.match(r"^\s*>", l) or re.match(r"^\|( |$)", l):
            return True
        return bool(extra_quote_pred and extra_quote_pred(l))

    for i, l in enumerate(lines):
        if is_q(i):
            keep[i] = False
    for i, l in enumerate(lines):
        if keep[i] and ATTRIB.search(l):
            j = i + 1
            while j < len(lines) and lines[j].strip() == "":
                j += 1
            if j >= len(lines) or not keep[j]:
                keep[i] = False
                # two-line Gmail attributions: "On ..., Name\n<addr> wrote:"
                if i > 0 and keep[i - 1] and re.match(r"^On .*\d", lines[i - 1]):
                    keep[i - 1] = False
    out = [l for l, k in zip(lines, keep) if k]
    t = "\n".join(out)
    t = re.sub(r"\n{3,}", "\n\n", t)  # quote removal leaves gaps; collapse (text only, not text_raw)
    return t.strip("\n")


def base_record(**kw):
    r = {k: None for k in FIELDS}
    r.update(source_type="email", venue="private email", timestamps_other=[], duplicate_of_public=None,
             also_published_at=[])
    r.update(kw)
    return r


# --------------------------------------------------------------------------- Malmi
def parse_malmi():
    p = os.path.join(RAW, "malmi", "index.html")
    s = open(p, encoding="utf-8").read()
    parts = re.split(r'(?=<div class="message )', s)[1:]
    recs = []
    for part in parts:
        n = int(re.search(r'id="email-(\d+)"', part).group(1))
        hdr = {k: html.unescape(v) for k, v in re.findall(r"<div><strong>([\w-]+)</strong>: (.*?)</div>", part)}
        if "satoshi" not in hdr.get("From", "").lower():
            continue
        m = re.search(r"<pre>(.*?)</pre>", part, flags=re.S)
        body = html.unescape(m.group(1))
        dt = rfc_dt(hdr["Date"])
        recip = re.sub(r"\s*<.*?>", "", hdr.get("To", "")).strip() or hdr.get("To")
        r = base_record(
            id=f"email-malmi-{n:04d}", correspondent="Martti Malmi", recipient=recip,
            thread=hdr.get("Subject"), subject=hdr.get("Subject"),
            timestamp_utc=iso(dt) if dt else None, timestamp_raw=hdr["Date"],
            timestamp_precision="second" if dt else "unknown",
            timestamp_source="Date: header as reproduced by Martti Malmi (HTML page shows Date/From/Subject/To/Cc only)",
            timestamp_tz_raw=offset_str(dt) if dt else None, timezone_basis="explicit" if dt else "unknown",
            url=f"https://mmalmi.github.io/satoshi/#email-{n}", raw_path=rel(p),
            from_address=hdr.get("From"), to_address=hdr.get("To"), cc_address=hdr.get("Cc"),
            text_raw=body, text=strip_quotes(body), whitespace_preserved=True,
            whitespace_notes="Body is inside <pre>; runs of spaces, trailing spaces (format=flowed) and line breaks "
                             "are preserved in the HTML source (html.unescape applied).",
            notes="Published by Martti Malmi 2024-02-23 (github.com/mmalmi/mmalmi.github.io commit 134c4a97); only his "
                  "@cc.hut.fi mailbox (2009-05-02..2011-02); Message-ID/Received headers not published. "
                  "Also exhibited in COPA v Wright.",
        )
        if "bitcoin-list@lists.sourceforge.net" in (hdr.get("Cc") or "") + (hdr.get("To") or ""):
            r["duplicate_of_public"] = "bitcoin-list (SourceForge) post; Malmi's copy gives the sender's Date: header"
        recs.append(r)
    return recs


# --------------------------------------------------------------------------- Trammell
PUBLIC_MIDS = {
    # Message-IDs also archived on public lists (metzdowd cryptography / bitcoin-list)
    "<CHILKAT-MID-30c0e5a0-3435-5411-3f7b-3fe798efbe86@server123>":
        "cryptography@metzdowd.com 2009-January/015014 and bitcoin-list (Cc'd to both lists)",
    "<CHILKAT-MID-e622b093-c26b-ab6c-9b35-00003814eb59@server123>":
        "cryptography@metzdowd.com 2009-January/015041 (identical Date: and body; Trammell got a separate "
        "copy with its own Message-ID, both relayed by anonymousspeech at Mon, 26 Jan 2009 00:03:11 +0800)",
}


def parse_trammell():
    d = os.path.join(RAW, "trammell", "Satoshi_Nakamoto", "Email")
    recs, seen = [], {}
    files = sorted(f for f in glob.glob(os.path.join(d, "*.mbox")) if "- Satoshi -" in os.path.basename(f))
    for f in files:
        mb = mailbox.mbox(f)
        for msg in mb:
            mid = msg["Message-ID"]
            rawb = open(f, "rb").read()
            payload = msg.get_payload(decode=True)
            body = payload.decode("latin-1")
            dt = rfc_dt(msg["Date"])
            hops = received_hops(msg)
            fromline = msg.get_from()
            other = hops + [{"label": "mbox From_ line (delivery time at Trammell's server, UTC)",
                             "raw": fromline, "utc": None}]
            if mid in seen:
                seen[mid]["also_published_at"].append(
                    f"second delivered copy: {rel(f)} (From_ line '{fromline}')")
                seen[mid]["timestamps_other"].extend(
                    [dict(h, label=h["label"] + " [2nd copy]") for h in hops])
                continue
            r = base_record(
                id=f"email-trammell-{len(recs) + 1:04d}", correspondent="Dustin D. Trammell",
                recipient="Dustin D. Trammell", thread=msg["Subject"], subject=msg["Subject"],
                timestamp_utc=iso(dt), timestamp_raw=msg["Date"], timestamp_precision="second",
                timestamp_source="Date: header in raw mbox published by Trammell. NB anonymousspeech/vistomail "
                                 "Date: headers can precede the MailEnable Received: time by minutes to hours "
                                 "(see timestamps_other).",
                timestamp_tz_raw=offset_str(dt), timezone_basis="explicit", timestamps_other=other,
                url="https://www.dustintrammell.com/s/Satoshi_Nakamoto.zip", raw_path=rel(f),
                from_address=msg["From"], to_address=msg["To"], cc_address=msg["Cc"], message_id=mid,
                in_reply_to=msg["In-Reply-To"], text_raw=body, text=strip_quotes(body),
                whitespace_preserved=True, whitespace_notes="Raw RFC822 message in mbox (8bit text/plain).",
                notes="Published by Dustin Trammell, 2013-11 (blog.dustintrammell.com/i-am-not-satoshi). "
                      "Individual .mbox per message plus Archive.mbox (identical content).",
            )
            if mid in PUBLIC_MIDS:
                r["duplicate_of_public"] = PUBLIC_MIDS[mid]
            seen[mid] = r
            recs.append(r)
    return recs


# --------------------------------------------------------------------------- Hal Finney
def parse_coindesk_hal():
    recs = []
    items = [("coindesk_a14c90a8_transcription.mbox.txt", "coindesk_a14c90a82690ccdd33ec98d0381c6f5e5cb78c66-1426x634.png"),
             ("coindesk_04952849_transcription.mbox.txt", "coindesk_049528492755b8dc909f2ea99364076cf0453884-1258x698.png")]
    for tx, png in items:
        p = os.path.join(RAW, "hal_finney", tx)
        msg = email.message_from_bytes(open(p, "rb").read().split(b"\n", 1)[1])
        rawbody = msg.get_payload()
        body = quopri.decodestring(rawbody.encode("latin-1")).decode("latin-1")
        dt = rfc_dt(msg["Date"])
        fromline = open(p).readline().strip()
        other = received_hops(msg) + [{"label": "mbox From_ line (finney.org delivery, local PST)",
                                       "raw": fromline, "utc": None}]
        recs.append(base_record(
            id=f"email-finney-coindesk-{len(recs) + 1:04d}", correspondent="Hal Finney", recipient="Hal Finney",
            thread=msg["Subject"], subject=msg["Subject"], timestamp_utc=iso(dt), timestamp_raw=msg["Date"],
            timestamp_precision="second",
            timestamp_source="Date: header visible in raw-mbox screenshot published by CoinDesk (manually transcribed)",
            timestamp_tz_raw=offset_str(dt), timezone_basis="explicit", timestamps_other=other,
            url="https://www.coindesk.com/markets/2020/11/26/previously-unpublished-emails-of-satoshi-nakamoto-present-a-new-puzzle",
            raw_path=rel(os.path.join(RAW, "hal_finney", png)),
            from_address=msg["From"], to_address=msg["To"], message_id=msg["Message-ID"],
            text_raw=body, text=strip_quotes(body), whitespace_preserved=True,
            whitespace_notes="Screenshot of raw mbox in a monospace font; spaces counted from glyph columns during "
                             "manual transcription (" + rel(p) + "). Body quoted-printable-decoded (soft breaks removed).",
            notes="Emails supplied by Fran Finney via Nathaniel Popper; published as images by CoinDesk 2020-11-26. "
                  "finney.org's Received: time is ~26-37 min EARLIER than the anonymousspeech Date:/Received: "
                  "times, i.e. the two servers' clocks disagreed (or a relay delay was mis-stamped); treat "
                  "sub-hour precision with care.",
        ))
    return recs


def pdf_text_with_blank_lines(path):
    """PyMuPDF text preserving in-line spaces; blank lines reconstructed from vertical gaps; rows joined."""
    doc = fitz.open(path)
    pages = []
    for pg in doc:
        rows = {}
        for b in pg.get_text("dict")["blocks"]:
            for l in b.get("lines", []):
                t = "".join(sp["text"] for sp in l["spans"])
                y = round(l["bbox"][1], 1)
                rows.setdefault(y, []).append((l["bbox"][0], t))
        ys = sorted(rows)
        out, prev = [], None
        for y in ys:
            cells = [t for x, t in sorted(rows[y])]
            line = cells[0] if len(cells) == 1 else cells[0] + " " + " ".join(c.strip() for c in cells[1:])
            if prev is not None:
                gap = y - prev
                nblank = int(round(gap / 11.5)) - 1
                out.extend([""] * max(0, nblank))
            out.append(line)
            prev = y
        pages.append("\n".join(out))
    return pages


def parse_wsj_hal():
    p = os.path.join(RAW, "hal_finney", "finneynakamotoemails.pdf")
    doc = fitz.open(p)
    t = "".join(pg.get_text("text") for pg in doc)
    # split at each "From: Satoshi" header block
    chunks = re.split(r"(?m)^(?=From: Satoshi Nakamoto <satoshi@vistomail\.com> ?$)", t)[1:]
    recs = []
    pacific = ZoneInfo("America/Los_Angeles")
    for c in chunks:
        c = re.sub(r"(?m)^-{5,} Forwarded message -{5,} ?\n?\Z", "", c)
        c = re.sub(r"\n-{5,} Forwarded message -{5,} ?\s*\Z", "\n", c)
        hm = re.match(r"From: (.*?) ?\nDate: (.*?) ?\nSubject: (.*?) ?\nTo: (.*?) ?\n", c)
        frm, date_raw, subj, to = hm.groups()
        body = c[hm.end():]
        body = re.sub(r"\A( ?\n)+", "", body)
        body = body.rstrip() + "\n"
        naive = datetime.strptime(date_raw.strip(), "%a, %b %d, %Y at %I:%M %p")
        local = naive.replace(tzinfo=pacific)
        recs.append(base_record(
            id=f"email-finney-wsj-{len(recs) + 1:04d}", correspondent="Hal Finney", recipient="Hal Finney",
            thread=subj.strip(), subject=subj.strip(), timestamp_utc=iso(local), timestamp_raw=date_raw.strip(),
            timestamp_precision="minute",
            timestamp_source="Gmail forward 'Date:' line (Hal Finney forwarded to WSJ, 2014); zone not shown. "
                             "Inferred US/Pacific (PST, UTC-8): Finney lived in California; Finney's Gmail quote "
                             "header of Satoshi's bitcoin-list post of 2009-02-22 reads '9:35 AM' while SourceForge "
                             "archives it at 17:47:52Z (UTC-8 +12 min list delay); Satoshi's 'RE:Crash in bitcoin "
                             "0.1.0' at 11:52 AM answers Finney's crash report whose Gmail Message-ID encodes "
                             "0901101113 (Pacific).",
            timestamp_tz_raw=None, timezone_basis="inferred", timestamp_local_naive=naive.isoformat(timespec="minutes"),
            url="https://online.wsj.com/public/resources/documents/finneynakamotoemails.pdf", raw_path=rel(p),
            from_address=frm.strip(), to_address=to.strip(),
            text_raw=body, text=strip_quotes(body), whitespace_preserved=False,
            whitespace_notes="WSJ Word-2010 PDF: spaces inside lines survive in the PDF text layer (PyMuPDF; pdftotext "
                             "collapses them), but LINE BREAKS are Word's page-width re-wrapping, not the original "
                             "(each line ends with the inter-word space at the wrap); blank lines are ' ' lines.",
            notes="Emails supplied by Hal Finney to the Wall Street Journal (spring 2014), published 2014-08-29 with "
                  "https://www.wsj.com/articles/BL-MBB-26228. Satoshi-to-Finney messages only (Finney's text quoted "
                  "with '>'). Gmail forward times are minute precision and derive from the sender's Date: header.",
        ))
    return recs


# --------------------------------------------------------------------------- Adam Back
def parse_back():
    p = os.path.join(RAW, "adam_back", "adam-back-exhibit-ab1-1.pdf")
    pages = pdf_text_with_blank_lines(p)
    # each email starts with "From: ..." at the top of a page; join continuation pages
    emails, cur = [], None
    for pg in pages:
        if pg.startswith("From:"):
            cur = pg
            emails.append(cur)
        else:
            emails[-1] = emails[-1] + "\n" + pg
    recs = []
    for e in emails:
        hm = re.match(r"From: (.*)\nSent: (.*)\nTo: (.*)\n(?:Cc: (.*)\n)?Subject: (.*)\n", e)
        frm, sent, to, cc, subj = [x.strip() if x else x for x in hm.groups()]
        if "satoshi" not in frm.lower():
            continue
        body = e[hm.end():].lstrip("\n")
        m = re.match(r"\w+ (\d+)/(\d+)/(\d{4}) (\d+):(\d\d):(\d\d) ([AP]M) \(UTC([+-]\d\d:\d\d)?\)", sent)
        mo, dd, yy, hh, mi, ss, ap, off = m.groups()
        h = int(hh) % 12 + (12 if ap == "PM" else 0)
        sign = 1
        tzd = timedelta(0)
        if off:
            sign = 1 if off[0] == "+" else -1
            tzd = sign * timedelta(hours=int(off[1:3]), minutes=int(off[4:6]))
        dt = datetime(int(yy), int(mo), int(dd), h, int(mi), int(ss), tzinfo=timezone(tzd))
        recs.append(base_record(
            id=f"email-back-{len(recs) + 1:04d}", correspondent="Adam Back", recipient="Adam Back",
            thread="Citation of your Hashcash paper", subject=subj, timestamp_utc=iso(dt), timestamp_raw=sent,
            timestamp_precision="second",
            timestamp_source="'Sent:' line of the COPA exhibit AB1 print-out, which states the offset "
                             "(UTC in Jan 2009, UTC+01:00 in Aug 2008, i.e. UK local time of the export).",
            timestamp_tz_raw="UTC" + (off or ""), timezone_basis="explicit",
            url="https://s3.documentcloud.org/documents/24439625/adam-back-exhibit-ab1-1.pdf", raw_path=rel(p),
            from_address=frm, to_address=to, cc_address=cc, text_raw=body,
            text=strip_quotes(body, cut_at_first_quote=True),
            whitespace_preserved=False,
            whitespace_notes="PDF (iText) text layer: spaces inside lines preserved (PyMuPDF), but long lines are "
                             "wrapped at page width by the exporter; blank lines reconstructed from line spacing.",
            notes="COPA v Wright Exhibit AB1 (Adam Back), filed Feb 2024; fetched via Wayback copy of DocumentCloud "
                  "(sha256 aa30732a...). Adam Back's Gmail quote header 'On Wed, Aug 20, 2008 at 6:30 PM' agrees "
                  "with the exhibit's 6:30:39 PM (UTC+01:00).",
        ))
    for r in recs:
        if "Third PartyAbstract" in (r["text_raw"] or ""):
            r["notes"] += (" The exhibit itself prints 'Title: ... Third PartyAbstract: ...' on one line (line break "
                           "lost in the exhibit, not by this parser).")
    return recs


# --------------------------------------------------------------------------- Wei Dai
def parse_dai():
    p = os.path.join(RAW, "wei_dai", "gwern-2008-nakamoto.html")
    s = open(p, encoding="utf-8").read()
    pres = [html.unescape(re.sub(r"<[^>]+>", "", x)) for x in re.findall(r"<pre[^>]*>(.*?)</pre>", s, flags=re.S)]
    recs = []
    for pre in pres:
        if not pre.startswith("From:") or "Satoshi" not in pre.split("\n", 1)[0]:
            continue
        hdr_txt, body = pre.split("\n\n", 1)
        hdr = dict(re.findall(r"^(\w+): (.*)$", hdr_txt, flags=re.M))
        naive = datetime.strptime(hdr["Sent"].strip(), "%A, %B %d, %Y %I:%M %p")
        cands = []
        for zname in ("America/Los_Angeles", "America/New_York", "UTC"):
            cands.append({"label": f"hypothesis only: 'Sent:' rendered in {zname}", "raw": hdr["Sent"],
                          "utc": iso(naive.replace(tzinfo=ZoneInfo(zname)))})
        recs.append(base_record(
            id=f"email-dai-{len(recs) + 1:04d}", correspondent="Wei Dai", recipient="Wei Dai",
            thread="Citation of your b-money page", subject=hdr.get("Subject"),
            timestamp_utc=None, timestamp_raw=hdr["Sent"], timestamp_precision="minute",
            timestamp_source="Outlook-style 'Sent:' line in the copy Wei Dai forwarded to Gwern; rendered in Wei "
                             "Dai's client time zone, which is not stated. No independent anchor found.",
            timestamp_tz_raw=None, timezone_basis="unknown", timestamp_local_naive=naive.isoformat(timespec="minutes"),
            timestamps_other=cands,
            url="https://gwern.net/doc/bitcoin/2008-nakamoto", raw_path=rel(p),
            from_address=hdr.get("From"), to_address=hdr.get("To"), cc_address=hdr.get("Cc"),
            text_raw=body.rstrip("\n") + "\n", text=strip_quotes(body), whitespace_preserved=True,
            whitespace_notes="gwern.net reproduces the emails 'as a code block to preserve whitespace' (HTML <pre>).",
            notes="Provided publicly by Wei Dai (2014) via Gwern Branwen. The Satoshi -> Dai emails of 2008-08-22 and "
                  "2009-01-10; Dai's reply is not Satoshi's and is omitted.",
        ))
    return recs


# --------------------------------------------------------------------------- Mike Hearn
ZURICH = ZoneInfo("Europe/Zurich")


def gmail_naive(s):
    return datetime.strptime(s.strip(), "%a, %b %d, %Y at %I:%M %p")


def hearn_record(n, thread, frm, to, date_raw, body, mike_text, src_path, url, ws_note, extra_notes=""):
    naive = gmail_naive(date_raw)
    loc = naive.replace(tzinfo=ZURICH)
    mike_norm = " ".join(mike_text.split())

    def quoted(line):
        if not line.startswith("    "):
            return False
        norm = " ".join(line.split())
        return bool(norm) and norm in mike_norm

    text = strip_quotes(body, extra_quote_pred=quoted)
    text = "\n".join(l for l in text.split("\n") if not re.match(r"^\s*Mike Hearn wrote:\s*$", l))
    text = re.sub(r"\n{3,}", "\n\n", text).strip("\n")
    return base_record(
        id=f"email-hearn-{n:04d}", correspondent="Mike Hearn", recipient="Mike Hearn", thread=thread,
        subject=thread, timestamp_utc=iso(loc), timestamp_raw=date_raw, timestamp_precision="minute",
        timestamp_source="Gmail 'Date:' line (2013/2017 export of Hearn's Gmail); zone not shown. ASSUMED "
                         "Europe/Zurich (CET/CEST) because Hearn was Zurich/Switzerland-based (Google Zurich, 2009-14; "
                         "Switzerland-based per his LinkedIn) when the thread was exported; the 2013 forward and the "
                         "2017 print view agree. Not independently verified: if his Gmail displayed UK time instead, "
                         "every true UTC value would be 1 hour LATER than given here.",
        timestamp_tz_raw=None, timezone_basis="assumed", timestamp_local_naive=naive.isoformat(timespec="minutes"),
        url=url, raw_path=rel(src_path), from_address=frm, to_address=to,
        text_raw=body, text=text, whitespace_preserved=True, whitespace_notes=ws_note,
        notes="Mike Hearn's emails with Satoshi, first released via CipherionX (bitcointalk topic 2080206, "
              "2017-08-07, pastebin) and then on plan99.net/~mike; Hearn confirms in his COPA witness statement "
              "(10 Nov 2023). Satoshi's GMX messages to Hearn were HTML; quoted text appears as 4-space-indented "
              "blocks in the text export." + extra_notes,
    )


def split_gmail_text(t):
    """Split a Gmail text export into (from, date, to, body) using '----------' separators."""
    t = t.replace("\r\n", "\n")
    msgs = []
    for block in re.split(r"(?m)^-{10,}\n", t):
        m = re.match(r"(?:\n*)From: (.*)\nDate: (.*)\nTo: (.*)\n(?:Cc: .*\n)?", block)
        if not m:
            continue
        body = block[m.end():]
        msgs.append((m.group(1).strip(), m.group(2).strip(), m.group(3).strip(), body))
    return msgs


def parse_hearn():
    recs, n = [], 0
    threads = [
        ("Questions about BitCoin", "pastebin_Na5FwkQ4.txt", "thread1.html", "https://pastebin.com/raw/Na5FwkQ4"),
        ("Lack of chargeback support", None, "thread2.html", None),
        ("More BitCoin questions", "pastebin_wA9Jn100.txt", "thread3.html", "https://pastebin.com/raw/wA9Jn100"),
        ("Open sourced my Java SPV impl", "pastebin_JF3USKFT.txt", "thread4.html", "https://pastebin.com/raw/JF3USKFT"),
        ("Holding coins in an unspendable state for a rolling time window", "pastebin_syrmi3ET.txt", "thread5.html",
         "https://pastebin.com/raw/syrmi3ET"),
    ]
    for title, pb, pv, pburl in threads:
        pv_path = os.path.join(RAW, "hearn", pv)
        pv_url = "https://plan99.net/~mike/satoshi-emails/" + pv
        if pb:
            path = os.path.join(RAW, "hearn", pb)
            msgs = split_gmail_text(open(path, encoding="utf-8", errors="replace").read())
            seen = set()
            mike_text = ""
            for frm, date_raw, to, body in msgs:
                key = (frm, date_raw)
                if key in seen:
                    continue
                seen.add(key)
                if "satoshin@gmx.com" not in frm:
                    mike_text += "\n" + body
                    continue
                n += 1
                body = re.sub(r"\A\n+", "", body).rstrip("\n") + "\n"
                r = hearn_record(n, title, frm, to, date_raw, body, mike_text, path, pburl,
                                 "Plain-text Gmail export pasted to pastebin (CRLF normalised to LF): double spaces "
                                 "after full stops are preserved; paragraphs are unwrapped because the originals were "
                                 "HTML mail.")
                r["also_published_at"] = [pv_url]
                recs.append(r)
        else:
            s = open(pv_path, encoding="utf-8").read()
            blocks = re.split(r'<table width=100% cellpadding=0 cellspacing=0 border=0 class="message">', s)[1:]
            mike_text = ""
            for b in blocks:
                m = re.search(r"<b>(.*?)</b>\s*&lt;(.*?)&gt;</font></td><td align=right><font size=-1>(.*?)</font>", b)
                name, addr, date_raw = m.group(1).strip(), m.group(2), m.group(3)
                tom = re.search(r'class="recipient"><div>To: (.*?)</div>', b)
                bm = re.search(r'<div style="overflow: hidden;"><font size=-1>(.*)', b, flags=re.S)
                h = bm.group(1)
                h = re.split(r"</font></div></table>|</body>", h)[0]
                h = re.sub(r"<br\s*/?>\n?", "\n", h)
                h = re.sub(r"<wbr\s*/?>", "", h)
                h = re.sub(r"<[^>]+>", "", h)
                body = html.unescape(h).replace("\u00a0", " ").rstrip("\n") + "\n"
                if addr != "satoshin@gmx.com":
                    mike_text += "\n" + body
                    continue
                n += 1
                r = hearn_record(n, title, f"{name} <{addr}>", html.unescape(tom.group(1)) if tom else None, date_raw,
                                 body, mike_text, pv_path, pv_url,
                                 "Gmail print-view HTML: Gmail encodes each double space as U+00A0+space, converted "
                                 "back to two spaces here; <br> -> newline. No plain-text copy of this thread survives "
                                 "(pastebin cKZPC1rF deleted; not in Wayback as raw).")
                recs.append(r)
    return recs


# --------------------------------------------------------------------------- Gavin Andresen
def parse_andresen():
    p = os.path.join(RAW, "andresen", "eleven-years-ago-today.wikitext")
    s = open(p, encoding="utf-8").read()
    m = re.search(r"'''Subject: (.*?)'''<br />\n(.*?)<br />\n(.*?)\n\n(.*?)\n\n\n-----", s, flags=re.S)
    subj, frm, date_raw, body_w = m.groups()
    body = body_w.replace("<br />\n", "\n").replace("<br />", "\n") + "\n"
    frm_clean = re.sub(r"\[mailto:(\S+) \S+\]", r"<\1>", frm)
    return [base_record(
        id="email-andresen-0001", correspondent="Gavin Andresen", recipient="Gavin Andresen", thread=subj,
        subject=subj, timestamp_utc="2011-04-26T08:29:00Z", timestamp_raw=date_raw.strip(),
        timestamp_precision="minute",
        timestamp_source="Blog header shows '26 Apr 2011, 10:29' (zone not stated) and Gavin's own reply quotes "
                         "'On Tue, Apr 26, 2011 at 4:29 AM'. Gavin lived in Amherst, Massachusetts (EDT, UTC-4) in "
                         "2011 -> 08:29 UTC; the 10:29 header is then consistent with a UTC+2 display. Inference, "
                         "not stated by the source.",
        timestamp_tz_raw=None, timezone_basis="inferred", timestamp_local_naive="2011-04-26T10:29",
        timestamps_other=[{"label": "Gavin's reply attribution (Gmail, his 2011 zone, presumably EDT)",
                           "raw": "On Tue, Apr 26, 2011 at 4:29 AM", "utc": "2011-04-26T08:29:00Z"}],
        url="https://gavinandresen.ninja/eleven-years-ago-today", raw_path=rel(p),
        from_address=frm_clean.strip(), to_address="Gavin Andresen <gavinandresen@gmail.com>",
        text_raw=body, text=body.strip("\n"), whitespace_preserved=False,
        whitespace_notes="Blog (MediaWiki) copy: apostrophes converted to typographic quotes and single spaces after "
                         "full stops, i.e. retyped/normalised by the publisher; original line breaks kept as <br />.",
        notes="Gavin Andresen's blog post of 2022-04-26 ('Eleven years ago today...'), riski.wiki MediaWiki page. "
              "Also quoted by The Atlantic (2014). Satoshi's last known email to Andresen.",
    )]


# --------------------------------------------------------------------------- Jon Matonis
def parse_matonis():
    prim = os.path.join(RAW, "matonis", "bitcoinfoundation-forum-topic-54.html")
    sec = os.path.join(RAW, "secondary_lugaxker", "email-to-jon-matonis.txt")
    if os.path.exists(prim) and os.path.getsize(prim) > 1000:
        s = open(prim, encoding="utf-8", errors="replace").read()
        i = s.find("Date: Thursday, March 4, 2010")
        j = s.find("interested in?", i) + len("interested in?")
        seg = s[i:j]
        seg = re.sub(r"<a [^>]*href='([^']+)'[^>]*>.*?</a>", r"\1", seg)  # IP.Board truncates link text; use href
        seg = re.sub(r"<br\s*/?>\n?", "\n", seg)
        seg = re.sub(r"<[^>]+>", "", seg)
        txt = html.unescape(seg).replace("\u00a0", " ")
        src, ws = prim, True
        wsn = ("IP.Board forum HTML (Wayback 2014-05-11 raw copy): each space in a run is written as &nbsp; "
               "(e.g. 'blog.&nbsp;&nbsp;That'), converted back to spaces; <br /> -> newline; the displayed URL is "
               "truncated by the forum, so the href is used.")
        url = "https://web.archive.org/web/20140511100607/https://bitcoinfoundation.org/forum/index.php?/topic/54-my-first-message-to-satoshi/"
    else:
        txt = open(sec, encoding="utf-8").read()
        src, ws = sec, "unknown"
        wsn = ("SECONDARY transcription (lugaxker/nakamoto-archive, 'retrieved from' the Wayback copy of the forum "
               "post); primary HTML could not be fetched, so fidelity is unverified.")
        url = "https://web.archive.org/web/20140511100607/https://bitcoinfoundation.org/forum/index.php?/topic/54-my-first-message-to-satoshi/"
    m = re.search(r"Date: (Thursday, March 4, 2010, 9:55 PM)[ \t]*\n\n(.*?interested in\?)", txt, flags=re.S)
    date_raw, body = m.group(1), m.group(2) + "\n"
    return [base_record(
        id="email-matonis-0001", correspondent="Jon Matonis", recipient="Jon Matonis", thread="Introduction",
        subject="Re: Introduction", timestamp_utc=None, timestamp_raw=date_raw, timestamp_precision="minute",
        timestamp_source="Yahoo Mail forward header ('--- On Thu, 3/4/10, Satoshi Nakamoto <satoshin@gmx.com> wrote:' "
                         "/ 'Date: Thursday, March 4, 2010, 9:55 PM'); rendered in Matonis' Yahoo account zone, not "
                         "stated. UTC not determinable (date could be 2010-03-04 or -05 UTC).",
        timestamp_tz_raw=None, timezone_basis="unknown", timestamp_local_naive="2010-03-04T21:55",
        url=url, raw_path=rel(src), from_address="Satoshi Nakamoto <satoshin@gmx.com>",
        to_address='"Jon Matonis" <matonis@yahoo.com>', text_raw=body, text=body.strip("\n"),
        whitespace_preserved=ws, whitespace_notes=wsn,
        notes="Posted by Jon Matonis on the Bitcoin Foundation forum, 22 Dec 2012 ('my last email from Satoshi on 4th "
              "March 2010'); earlier correspondence purged. Forum is offline; only Wayback copies exist.",
    )]


# --------------------------------------------------------------------------- Laszlo Hanyecz
def parse_hanyecz():
    p = os.path.join(RAW, "hanyecz", "reddit-36vnmr-wayback.html")
    s = open(p, encoding="utf-8", errors="replace").read()
    i = s.find("A big attraction")
    j = s.find("</p>", i)
    seg = s[i:j]
    body = html.unescape(re.sub(r"<br\s*/?>", "\n", seg)).strip() + "\n"
    return [base_record(
        id="email-hanyecz-0001", correspondent="Laszlo Hanyecz", recipient="Laszlo Hanyecz", thread=None,
        subject=None, timestamp_utc=None, timestamp_raw=None, timestamp_precision="unknown",
        timestamp_source="No date given by the publisher. Context: Popper says Laszlo first emailed Satoshi about GPU "
                         "mining in April 2010 (so ~April-May 2010).",
        timestamp_tz_raw=None, timezone_basis="unknown",
        url="https://www.reddit.com/r/Bitcoin/comments/36vnmr/heres_what_satoshi_wrote_to_the_man_responsible/",
        raw_path=rel(p), from_address=None, to_address=None, text_raw=body, text=body.strip("\n"),
        whitespace_preserved=False,
        whitespace_notes="Reddit markdown rendering (Wayback copy of 2025-08-03): runs of spaces collapsed; "
                         "paragraph breaks shown as <br>. Possibly an excerpt; no headers.",
        notes="Posted by Nathaniel Popper (u/nathanielpopper) on r/Bitcoin, 2015-05-22 14:11 UTC, as an excerpt "
              "shared by Laszlo Hanyecz for 'Digital Gold'. Not a verbatim raw email.",
    )]


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    recs = []
    for fn in (parse_malmi, parse_trammell, parse_coindesk_hal, parse_wsj_hal, parse_back, parse_dai, parse_hearn,
               parse_andresen, parse_matonis, parse_hanyecz):
        got = fn()
        print(f"{fn.__name__:22s} {len(got)}")
        recs.extend(got)
    recs.sort(key=lambda r: (r["timestamp_utc"] or r["timestamp_local_naive"] or "9999", r["id"]))
    # chronological ids per source (Malmi keeps his own email numbers, which match the page anchors)
    counters = {}
    for r in recs:
        if r["id"].startswith("email-malmi-"):
            continue
        prefix = r["id"].rsplit("-", 1)[0]
        counters[prefix] = counters.get(prefix, 0) + 1
        r["id"] = f"{prefix}-{counters[prefix]:04d}"
    for r in recs:
        extra = []
        if "-----BEGIN PGP" in (r["text_raw"] or ""):
            extra.append("PGP armour block(s) removed from `text`.")
        if re.search(r"(?m)^\s*-{3,}\s*(Original Message|Forwarded message)", r["text_raw"] or "", re.I):
            extra.append("Forwarded third-party message removed from `text`.")
        if not (r["text"] or "").strip():
            extra.append("No words of Satoshi's own in this message (pure forward/attachment); `text` is empty.")
        if extra:
            r["notes"] = (r["notes"] or "") + " " + " ".join(extra)
    with open(OUT, "w", encoding="utf-8") as f:
        for r in recs:
            f.write(json.dumps({k: r.get(k) for k in FIELDS}, ensure_ascii=False) + "\n")
    print("wrote", rel(OUT), len(recs))


if __name__ == "__main__":
    main()
