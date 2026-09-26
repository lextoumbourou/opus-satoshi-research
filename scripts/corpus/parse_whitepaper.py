#!/usr/bin/env python3
"""Whitepaper record for the corpus.

Download: curl -L -o data/satoshi/raw/whitepaper/bitcoin_org_current.pdf https://bitcoin.org/bitcoin.pdf
The file's SHA-1 (base32 RXRP3MCO3TTBE44OWUPBJ3GEEY4B7DWY) equals the Wayback Machine CDX digest of
http://www.bitcoin.org/bitcoin.pdf captured 2010-07-04, 2010-08-05 and 2010-11-05, i.e. it is the
version Satoshi served from bitcoin.org in 2010 (the revised March 2009 version). The original
October 2008 version linked from the metzdowd announcement was not found in the Wayback Machine
(earliest capture 2010).

Timestamp: PDF /CreationDate written by OpenOffice.org 2.4 from the author's system clock and zone.
Text: pdftotext -raw (PDF text extraction does not preserve inter-sentence spacing).
Output: data/satoshi/intermediate/whitepaper.jsonl
"""
import hashlib
import json
import os
import re
import subprocess
from datetime import datetime, timedelta, timezone

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
PDF = os.path.join(ROOT, "data", "satoshi", "raw", "whitepaper", "bitcoin_org_current.pdf")
OUT = os.path.join(ROOT, "data", "satoshi", "intermediate", "whitepaper.jsonl")


def main():
    b = open(PDF, "rb").read()
    raw = re.search(rb"/CreationDate\s*\(([^)]*)\)", b).group(1).decode()
    m = re.match(r"D:(\d{14})([+-])(\d\d)'(\d\d)'", raw)
    local = datetime.strptime(m.group(1), "%Y%m%d%H%M%S")
    off = timedelta(hours=int(m.group(3)), minutes=int(m.group(4))) * (1 if m.group(2) == "+" else -1)
    utc = (local - off).replace(tzinfo=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    txt = subprocess.run(["pdftotext", "-raw", PDF, "-"], capture_output=True).stdout.decode("utf-8", "replace")
    rec = {
        "id": "whitepaper-2009-03-24",
        "source_type": "whitepaper",
        "venue": "bitcoin.org/bitcoin.pdf",
        "recipient": None,
        "thread": "Bitcoin: A Peer-to-Peer Electronic Cash System",
        "timestamp_utc": utc,
        "timestamp_raw": raw,
        "timestamp_precision": "second",
        "timestamp_source": "PDF /CreationDate metadata (OpenOffice.org 2.4 Writer export; local time + UTC offset of the author's machine)",
        "timestamp_tz_raw": f"{m.group(2)}{m.group(3)}:{m.group(4)}",
        "url": "https://bitcoin.org/bitcoin.pdf",
        "raw_path": os.path.relpath(PDF, ROOT),
        "sha256": hashlib.sha256(b).hexdigest(),
        "text": txt.strip(),
        "text_raw": txt,
        "whitespace_preserved": False,
        "whitespace_notes": "pdftotext extraction; PDF glyph positioning does not reliably preserve the number of spaces between sentences. For whitespace analysis use the abstract as quoted in the 2008-10-31 metzdowd email instead.",
        "notes": "Revised version (PDF generated 2009-03-24) as served on bitcoin.org in 2010 (byte-identical to Wayback captures of July-Nov 2010). The original version was announced on the cryptography list 2008-10-31; a copy of that 2008 PDF was not retrieved here. The PDF time is when the PDF was generated, not when the text was written.",
    }
    with open(OUT, "w") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    print(rec["timestamp_raw"], "->", utc)


if __name__ == "__main__":
    main()
