#!/usr/bin/env python3
"""Parse Satoshi's posts to the metzdowd.com "cryptography" mailing list (Oct 2008 - Jan 2009).

Primary raw source: Gmane NNTP copies (full RFC822 incl. Received: headers), fetched by
fetch_gmane.py into data/satoshi/raw/gmane/gmane.comp.encryption.general/*.eml.
Secondary: Mailman/pipermail monthly text archives (mbox-like) downloaded from
https://www.metzdowd.com/pipermail/cryptography/YYYY-Month.txt.gz into data/satoshi/raw/metzdowd/.
Pipermail HTML URLs (message numbers) are taken from the Satoshi Nakamoto Institute data
(emails.json source_id), matched on the Date: header.

Output: data/satoshi/intermediate/metzdowd.jsonl
"""
import email
import email.policy
import email.utils
import glob
import gzip
import json
import os
import re
from datetime import timezone

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
RAW = os.path.join(ROOT, "data", "satoshi", "raw")
OUT = os.path.join(ROOT, "data", "satoshi", "intermediate", "metzdowd.jsonl")
FOOTER_RE = re.compile(
    r"\n*-{50,}\nThe Cryptography Mailing List\nUnsubscribe by sending \"unsubscribe cryptography\" to majordomo(@| at )metzdowd\.com\n*$"
)


def to_utc(raw):
    dt = email.utils.parsedate_to_datetime(raw)
    return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def rel(p):
    return os.path.relpath(p, ROOT)


def strip_quotes(body):
    """Remove quoted lines ('>' prefixed) and the attribution line introducing them."""
    lines = body.split("\n")
    keep = []
    for i, ln in enumerate(lines):
        if ln.lstrip().startswith(">"):
            continue
        # attribution line: "X wrote:" followed (after optional blank) by a quoted line
        if re.search(r"wrote:\s*$", ln):
            nxt = [l for l in lines[i + 1:i + 3] if l.strip()]
            if nxt and nxt[0].lstrip().startswith(">"):
                continue
        keep.append(ln)
    text = "\n".join(keep)
    text = re.sub(r"\n{3,}", "\n\n", text).strip("\n")
    return text


def parse_received(msg):
    out = []
    for h in msg.get_all("Original-Received", []) + msg.get_all("Received", []):
        h1 = re.sub(r"\s+", " ", h)
        if ";" not in h1:
            continue
        d = h1.rsplit(";", 1)[1].strip()
        try:
            utc = to_utc(d)
        except Exception:
            utc = None
        out.append({"label": "Received: " + h1.rsplit(";", 1)[0][:140], "raw": d, "utc": utc})
    return out


def pipermail_index():
    """Map Message-ID -> (month file, envelope From_ line, body) from the .txt.gz archives."""
    idx = {}
    for p in sorted(glob.glob(os.path.join(RAW, "metzdowd", "*.txt.gz"))):
        data = gzip.open(p).read().decode("latin-1")
        parts = re.split(r"\n(?=From \S+ at \S+\s+\w{3} \w{3} [ \d]\d \d\d:\d\d:\d\d \d{4}\n)", "\n" + data)
        for part in parts:
            part = part.lstrip("\n")
            if not part.startswith("From "):
                continue
            head, _, body = part.partition("\n\n")
            m = re.search(r"^Message-ID: (<[^>]+>)", head, re.M)
            if m:
                idx[m.group(1)] = (rel(p), head.split("\n", 1)[0], body.rstrip("\n"), head)
    return idx


def main():
    sni = json.load(open(os.path.join(RAW, "sni-repo", "server", "data", "emails.json")))
    sni_by_date = {e["date"]: e for e in sni if e.get("source") == "cryptography"}
    pm = pipermail_index()
    rows = []
    for p in sorted(glob.glob(os.path.join(RAW, "gmane", "gmane.comp.encryption.general", "*.eml")),
                    key=lambda x: int(os.path.basename(x).split(".")[0])):
        rawbytes = open(p, "rb").read()
        msg = email.message_from_bytes(rawbytes, policy=email.policy.compat32)
        frm = msg["From"]
        if "vistomail" not in frm.lower():
            continue
        date_raw = msg["Date"]
        utc = to_utc(date_raw)
        body = msg.get_payload(decode=True).decode(msg.get_content_charset() or "latin-1")
        body = body.replace("\r\n", "\n")
        body_nofooter = FOOTER_RE.sub("", body).rstrip("\n")
        mid = msg["Message-ID"].strip()
        others = []
        pmrec = pm.get(mid)
        ws_note = ("Gmane copy is quoted-printable encoded (soft line breaks, =20 trailing spaces); decoded body "
                   "reproduced byte-for-byte. Satoshi's original lines were long (one paragraph per line) where the QP "
                   "encoder inserted soft breaks; hard line breaks are Satoshi's.")
        if pmrec:
            others.append({"label": "pipermail envelope From_ line (list server local time, US/Eastern)",
                           "raw": pmrec[1], "utc": None})
            pm_body = FOOTER_RE.sub("", pmrec[2]).rstrip("\n")
            obf = re.sub(r"(?<=[\w.+-])@(?=[\w-]+\.[\w.]+)", " at ", body_nofooter)  # pipermail address obfuscation
            same = re.sub(r"\s+", " ", pm_body).strip() == re.sub(r"\s+", " ", obf).strip()
            same_ws = pm_body == obf
            ws_note += (" Pipermail .txt archive body: " + ("identical incl. whitespace" if same_ws else (
                "same words, whitespace differs" if same else "differs in content (see raw)")) + " (after @->' at ' obfuscation).")
        nntp_date = msg["NNTP-Posting-Date"]
        if nntp_date:
            others.append({"label": "Gmane NNTP-Posting-Date (injection into Gmane after list distribution)",
                           "raw": nntp_date, "utc": to_utc(nntp_date)})
        rec_hops = parse_received(msg)
        others.extend(rec_hops)
        first_hop = [o for o in rec_hops if "by anonymousspeech.com" in o["label"]]
        s = sni_by_date.get(utc)
        url = s["url"].replace("http://", "https://") if s else None
        tz = date_raw.strip().split()[-1]
        rows.append({
            "id": f"metzdowd-{s['source_id']}" if s else f"metzdowd-gmane-{os.path.basename(p)[:-4]}",
            "source_type": "mailing_list",
            "venue": "cryptography@metzdowd.com",
            "recipient": "cryptography@metzdowd.com",
            "thread": re.sub(r"^Re:\s*", "", msg["Subject"]).strip(),
            "subject": msg["Subject"],
            "timestamp_utc": utc,
            "timestamp_raw": date_raw,
            "timestamp_precision": "second",
            "timestamp_source": "Date: header of the raw message (set by Satoshi's sending service, anonymousspeech.com / vistomail.com, Chilkat mailer)",
            "timestamp_tz_raw": tz,
            "timestamps_other": others,
            "timestamp_first_received_utc": first_hop[0]["utc"] if first_hop else None,
            "timestamp_first_received_raw": first_hop[0]["raw"] if first_hop else None,
            "url": url,
            "raw_path": rel(p),
            "raw_path_secondary": pmrec[0] if pmrec else None,
            "text": strip_quotes(body_nofooter),
            "text_raw": body_nofooter,
            "whitespace_preserved": True,
            "whitespace_notes": ws_note + " List footer (\"The Cryptography Mailing List / Unsubscribe...\") removed.",
            "from_address": frm,
            "to_address": msg["To"],
            "message_id": mid,
            "in_reply_to": msg["In-Reply-To"],
            "gmane_archived_at": msg["Archived-At"],
            "sni_satoshi_id": s.get("satoshi_id") if s else None,
            "notes": "The Date: header offset (+0800) is that of the sending service (anonymousspeech.com server, "
                     "124.217.253.42), not necessarily Satoshi's location. The first Received: hop "
                     "(server123 -> anonymousspeech.com, field timestamp_first_received_utc) is the service's own "
                     "timestamp when the message entered its mail server; it is 3-155 minutes AFTER the Date: header "
                     "across these 18 posts (Date: is probably when the message was composed/submitted in the web "
                     "interface; this is an inference). Timestamp_utc uses the Date: header.",
        })
    rows.sort(key=lambda r: r["timestamp_utc"])
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(len(rows), "metzdowd posts;", sum(1 for r in rows if r["raw_path_secondary"]), "matched in pipermail;",
          sum(1 for r in rows if r["url"]), "with SNI/pipermail URL")


if __name__ == "__main__":
    main()
