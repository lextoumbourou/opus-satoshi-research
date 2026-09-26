#!/usr/bin/env python3
"""Download publicly published PRIVATE email correspondence of Satoshi Nakamoto.

Saves raw copies under data/satoshi/raw/private_emails/<correspondent>/ and writes
data/satoshi/raw/private_emails/FETCH_LOG.json (url, local path, http status, sha256, fetch time).

Politeness: >= 2 s between requests. No anti-bot challenges are bypassed: sources that sit
behind Cloudflare / reddit bot walls are fetched from the Internet Archive (id_ raw mode) or,
failing that, from a secondary transcription (lugaxker/nakamoto-archive on GitHub), which is
clearly labelled as secondary.

Re-run safe: existing files are kept unless --force is given.
Usage: python3 scripts/corpus/fetch_private_emails.py [--force]
"""
import hashlib
import json
import os
import sys
import time
import zipfile
from datetime import datetime, timezone

import requests

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
OUT = os.path.join(ROOT, "data", "satoshi", "raw", "private_emails")
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/128.0 Safari/537.36 (satoshi-research corpus builder)")
DELAY = 2.0
LUGAXKER = "https://raw.githubusercontent.com/lugaxker/nakamoto-archive/8405b13482ae1a1bc55d6fe5bb3a5f2f46a58ffc/src/"

# (local path relative to OUT, [candidate URLs in order of preference], note)
SOURCES = [
    # Martti Malmi: published by Malmi himself, 2024-02-23 (GitHub Pages). Pin the commit too.
    ("malmi/index.html", ["https://mmalmi.github.io/satoshi/"], "Malmi's own publication (live)"),
    ("malmi/index.pinned-6e20611f.html",
     ["https://raw.githubusercontent.com/mmalmi/mmalmi.github.io/6e20611f204a9b9afd9e9f83e2ffe69754118465/satoshi/index.html"],
     "same page at the 2024-02-23 commit"),
    # Adam Back: COPA v Wright Exhibit AB1 (DocumentCloud is behind Cloudflare -> Wayback raw copy)
    ("adam_back/adam-back-exhibit-ab1-1.pdf",
     ["https://s3.documentcloud.org/documents/24439625/adam-back-exhibit-ab1-1.pdf",
      "https://web.archive.org/web/20260831145317id_/https://s3.documentcloud.org/documents/24439625/adam-back-exhibit-ab1-1.pdf"],
     "COPA v Wright exhibit AB1"),
    # Wei Dai: emails provided by Wei Dai, published on gwern.net
    ("wei_dai/gwern-2008-nakamoto.html", ["https://gwern.net/doc/bitcoin/2008-nakamoto"], "gwern.net page"),
    # Hal Finney: WSJ 2014 PDF (emails supplied by Finney) + CoinDesk 2020 raw-mbox screenshots (from Fran Finney)
    ("hal_finney/finneynakamotoemails.pdf",
     ["https://online.wsj.com/public/resources/documents/finneynakamotoemails.pdf"], "WSJ 2014"),
    ("hal_finney/coindesk-2020-11-26.html",
     ["https://www.coindesk.com/markets/2020/11/26/previously-unpublished-emails-of-satoshi-nakamoto-present-a-new-puzzle"],
     "CoinDesk article"),
    ("hal_finney/coindesk_c165ef7cffc1392f4ed4e166e814cb65d8feedce-1212x914.png",
     ["https://cdn.sanity.io/images/s3y3vcno/production/c165ef7cffc1392f4ed4e166e814cb65d8feedce-1212x914.png"],
     "Hal -> Satoshi 2008-11-19 (raw mbox screenshot)"),
    ("hal_finney/coindesk_a14c90a82690ccdd33ec98d0381c6f5e5cb78c66-1426x634.png",
     ["https://cdn.sanity.io/images/s3y3vcno/production/a14c90a82690ccdd33ec98d0381c6f5e5cb78c66-1426x634.png"],
     "Satoshi -> Hal 2009-01-09 'Bitcoin v0.1' (raw mbox screenshot)"),
    ("hal_finney/coindesk_049528492755b8dc909f2ea99364076cf0453884-1258x698.png",
     ["https://cdn.sanity.io/images/s3y3vcno/production/049528492755b8dc909f2ea99364076cf0453884-1258x698.png"],
     "Satoshi -> Hal 2009-01-09 'Re: Bitcoin v0.1' (raw mbox screenshot)"),
    # Dustin Trammell: raw mbox files published by Trammell (2013)
    ("trammell/Satoshi_Nakamoto.zip", ["https://www.dustintrammell.com/s/Satoshi_Nakamoto.zip"], "raw mbox zip"),
    # Mike Hearn: Gmail print views on plan99.net + the 2017 pastebin text dumps (CipherionX, from Hearn)
    ("hearn/index.html", ["https://plan99.net/~mike/"], "Hearn's page"),
    ("hearn/thread1.html", ["https://plan99.net/~mike/satoshi-emails/thread1.html"], "Gmail print view"),
    ("hearn/thread2.html", ["https://plan99.net/~mike/satoshi-emails/thread2.html"], "Gmail print view"),
    ("hearn/thread3.html", ["https://plan99.net/~mike/satoshi-emails/thread3.html"], "Gmail print view"),
    ("hearn/thread4.html", ["https://plan99.net/~mike/satoshi-emails/thread4.html"], "Gmail print view"),
    ("hearn/thread5.html", ["https://plan99.net/~mike/satoshi-emails/thread5.html"], "Gmail print view"),
    ("hearn/First-Witness-Statement-of-Michael-Christopher-Hearn.pdf",
     ["https://bitcoindefense.org/assets/documents/First-Witness-Statement-of-Michael-Christopher-Hearn.pdf"],
     "COPA witness statement (context; exhibits are screenshots)"),
    ("hearn/pastebin_Na5FwkQ4.txt",
     ["https://pastebin.com/raw/Na5FwkQ4",
      "https://web.archive.org/web/20230319170845id_/https://pastebin.com/raw/Na5FwkQ4"], "thread 1 text"),
    ("hearn/pastebin_wA9Jn100.txt", ["https://pastebin.com/raw/wA9Jn100"], "thread 3 text"),
    ("hearn/pastebin_JF3USKFT.txt",
     ["https://pastebin.com/raw/JF3USKFT",
      "https://web.archive.org/web/20230610115741id_/https://pastebin.com/raw/JF3USKFT"], "thread 4 text"),
    ("hearn/pastebin_syrmi3ET.txt", ["https://pastebin.com/raw/syrmi3ET"], "thread 5 text"),
    # Gavin Andresen: his 2022 blog post (MediaWiki raw wikitext + rendered page)
    ("andresen/eleven-years-ago-today.html", ["https://gavinandresen.ninja/eleven-years-ago-today"], "rendered"),
    ("andresen/eleven-years-ago-today.wikitext",
     ["https://riski.wiki/index.php?title=User:Gavinandresen/Blog/2022-04-26_Eleven_years_ago_today%E2%80%A6&action=raw"],
     "raw wikitext"),
    # Jon Matonis: Bitcoin Foundation forum post 2012-12-22 (site dead -> Wayback)
    ("matonis/bitcoinfoundation-forum-topic-54.html",
     ["https://web.archive.org/web/20140511100607id_/https://bitcoinfoundation.org/forum/index.php?/topic/54-my-first-message-to-satoshi/",
      "https://web.archive.org/web/20200516155319id_/https://bitcoinfoundation.org/forum/index.php?/topic/54-my-first-message-to-satoshi/"],
     "Matonis forum post"),
    # Laszlo Hanyecz: Nathaniel Popper's r/Bitcoin post 2015-05-22 (reddit blocks bots -> Wayback)
    ("hanyecz/reddit-36vnmr-wayback.html",
     ["https://web.archive.org/web/20250803142229id_/https://www.reddit.com/r/Bitcoin/comments/36vnmr/heres_what_satoshi_wrote_to_the_man_responsible/"],
     "Popper reddit post (archived)"),
    # Secondary transcriptions (lugaxker/nakamoto-archive), used only as fallbacks / cross-checks
    ("secondary_lugaxker/email-to-jon-matonis.txt", [LUGAXKER + "email-to-jon-matonis.txt"], "secondary"),
    ("secondary_lugaxker/email-to-laszlo-hanyecz.txt", [LUGAXKER + "email-to-laszlo-hanyecz.txt"], "secondary"),
    ("secondary_lugaxker/email-to-gavin-andresen.txt", [LUGAXKER + "email-to-gavin-andresen.txt"], "secondary"),
    ("secondary_lugaxker/nakamoto-dai-emails.txt", [LUGAXKER + "nakamoto-dai-emails.txt"], "secondary"),
    ("secondary_lugaxker/WQEY5CWEN5ASLKLCSGSL5ZNXLQ.txt", [LUGAXKER + "WQEY5CWEN5ASLKLCSGSL5ZNXLQ.txt"], "secondary"),
    ("secondary_lugaxker/66FEUFUEIVC3LOIOA6ESVKGGKM.txt", [LUGAXKER + "66FEUFUEIVC3LOIOA6ESVKGGKM.txt"], "secondary"),
    ("secondary_lugaxker/QEI3NJOWY5FXJOOR7CEMNT7O3U.txt", [LUGAXKER + "QEI3NJOWY5FXJOOR7CEMNT7O3U.txt"], "secondary"),
]

BLOCK_MARKERS = (b"Just a moment...", b"Attention Required! | Cloudflare", b"Checking you are not a bot",
                 b"Pastebin.com - Not Found")


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()


def main():
    force = "--force" in sys.argv
    s = requests.Session()
    s.headers["User-Agent"] = UA
    logp = os.path.join(OUT, "FETCH_LOG.json")
    log = json.load(open(logp)) if os.path.exists(logp) else {}
    for rel, urls, note in SOURCES:
        path = os.path.join(OUT, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        if os.path.exists(path) and os.path.getsize(path) > 0 and not force:
            log.setdefault(rel, {"note": note, "url_candidates": urls,
                                 "fetched_utc": "pre-existing file (downloaded 2026-09-26 from one of url_candidates)"})
            log[rel]["sha256"] = sha256(path)
            continue
        ok = False
        for url in urls:
            for attempt in range(3):
                try:
                    r = s.get(url, timeout=120)
                except Exception as e:  # network error / archive.org outage
                    print("ERR", url, e, flush=True)
                    time.sleep(DELAY * (attempt + 2))
                    continue
                time.sleep(DELAY)
                body = r.content
                blocked = any(m in body[:5000] for m in BLOCK_MARKERS)
                print(r.status_code, len(body), "BLOCKED" if blocked else "", url, flush=True)
                if r.status_code == 200 and not blocked:
                    with open(path, "wb") as f:
                        f.write(body)
                    log[rel] = {"url": url, "status": r.status_code, "note": note,
                                "fetched_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                                "http_last_modified": r.headers.get("Last-Modified"),
                                "sha256": sha256(path)}
                    ok = True
                break
            if ok:
                break
        if not ok:
            log[rel] = {"urls_tried": urls, "status": "UNAVAILABLE", "note": note,
                        "checked_utc": datetime.now(timezone.utc).isoformat(timespec="seconds")}
    # unpack Trammell zip
    z = os.path.join(OUT, "trammell", "Satoshi_Nakamoto.zip")
    if os.path.exists(z):
        with zipfile.ZipFile(z) as zf:
            zf.extractall(os.path.join(OUT, "trammell"))
    with open(logp, "w") as f:
        json.dump(log, f, indent=1, sort_keys=True)


if __name__ == "__main__":
    main()
