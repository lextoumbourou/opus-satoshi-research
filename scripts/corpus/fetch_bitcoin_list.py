#!/usr/bin/env python3
"""Fetch archived copies of the bitcoin-list mailing list (lists.sourceforge.net) pages that
contain Satoshi Nakamoto's posts (Dec 2008 - Dec 2010).

sourceforge.net itself serves a Cloudflare JS challenge to non-browser clients (HTTP 403), which
we do NOT try to bypass. Instead we use Internet Archive (Wayback Machine) captures, fetched with
the `id_` modifier so the original bytes are returned (no Wayback banner / URL rewriting).

Pages fetched (all via Wayback):
  1. Allura message pages  https://sourceforge.net/p/bitcoin/mailman/message/<ID>/
     (the URLs the Nakamoto Institute cites). Show "From: Name <addr...> - YYYY-MM-DD HH:MM:SS"
     (no time zone shown) and the body in <pre> (whitespace preserved).
  2. Legacy (pre-2013) SourceForge mailarchive pages:
       sourceforge.net/mailarchive/message.php?msg_id=<ID>
       sourceforge.net/mailarchive/forum.php?forum_name=bitcoin-list&max_rows=25&style=nested&viewmonth=YYYYMM
       sourceforge.net/mailarchive/forum.php?forum_name=bitcoin-list&max_rows=25&style=ultimate&viewmonth=YYYYMM
     (used to enumerate every message in the months Satoshi was active, and cross-check dates)
  3. Allura list month listings sourceforge.net/p/bitcoin/mailman/bitcoin-list/?viewmonth=YYYYMM

Saved to data/satoshi/raw/sourceforge_bitcoin_list/ with fetch_meta.json recording, for each
file, the original URL and the Wayback capture timestamp actually served.

Politeness: >= 3 s between requests; exponential backoff on errors (IA is intermittently
"Temporarily Offline"). Re-runnable: existing files are skipped.

Usage: python3 scripts/corpus/fetch_bitcoin_list.py
"""
import json
import os
import re
import sys
import time
import urllib.parse

import requests

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
OUT = os.path.join(ROOT, "data", "satoshi", "raw", "sourceforge_bitcoin_list")
SNI = os.path.join(ROOT, "data", "satoshi", "raw", "sni-repo", "server", "data", "emails.json")
DELAY = 3.0
UA = "Mozilla/5.0 (satoshi-research corpus builder; polite)"

MONTHS = [f"{y}{m:02d}" for y in (2008, 2009, 2010, 2011) for m in range(1, 13)]
MONTHS = [m for m in MONTHS if "200811" < m < "201104"]

sess = requests.Session()
sess.headers["User-Agent"] = UA
_last = [0.0]


def polite_get(url, timeout=120):
    for attempt in range(8):
        wait = _last[0] + DELAY - time.time()
        if wait > 0:
            time.sleep(wait)
        try:
            r = sess.get(url, timeout=timeout, allow_redirects=True)
            _last[0] = time.time()
            if b"Temporarily Offline" in r.content[:3000] and "archive.org" in r.url:
                raise requests.RequestException("IA temporarily offline")
            return r
        except requests.RequestException as e:
            _last[0] = time.time()
            back = min(300, 10 * 2 ** attempt)
            print(f"    error {e!s:.80} -> sleep {back}s", flush=True)
            time.sleep(back)
    return None


def cdx(url, exact=True):
    q = {"url": url, "fl": "timestamp,original,statuscode", "limit": "200" if exact else "5000"}
    if not exact:
        q["matchType"] = "prefix"
    r = polite_get("https://web.archive.org/cdx/search/cdx?" + urllib.parse.urlencode(q), timeout=180)
    if r is None or r.status_code != 200:
        return None
    rows = [ln.split(" ") for ln in r.text.splitlines() if ln.strip()]
    return [row for row in rows if len(row) == 3]


def fetch_capture(original_variants, dest_rel, meta, prefer="earliest"):
    """Find a 200 capture of any of the URL variants and save its raw bytes."""
    dest = os.path.join(OUT, dest_rel)
    if os.path.exists(dest):
        return True
    caps = []
    for u in original_variants:
        rows = cdx(u)
        if rows is None:
            print("  cdx failed", u, flush=True)
            continue
        caps += [(ts, orig) for ts, orig, st in rows if st == "200"]
    if not caps:
        meta[dest_rel] = {"error": "no 200 capture", "tried": original_variants}
        print("  no capture", dest_rel, flush=True)
        return False
    caps.sort(reverse=(prefer == "latest"))
    for ts, orig in caps[:4]:
        r = polite_get(f"https://web.archive.org/web/{ts}id_/{orig}")
        if r is not None and r.status_code == 200 and len(r.content) > 500:
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            with open(dest, "wb") as f:
                f.write(r.content)
            meta[dest_rel] = {"original": orig, "wayback_ts": ts, "served": r.url, "bytes": len(r.content)}
            print("  saved", dest_rel, ts, len(r.content), flush=True)
            return True
    meta[dest_rel] = {"error": "captures failed to download", "captures": caps[:4]}
    return False


def repair_meta(meta):
    """Fill provenance for saved files lacking a fetch_meta.json entry (e.g. after an interrupted
    run) from fetch.log 'saved <rel> <wayback_ts>' lines and the legacy CDX listing."""
    log = os.path.join(OUT, "fetch.log")
    if os.path.exists(log):
        for m in re.finditer(r"saved (\S+) (\d{14}) (\d+)", open(log).read()):
            rel, ts, n = m.groups()
            if rel not in meta and os.path.exists(os.path.join(OUT, rel)):
                mid = re.search(r"(\d+)\.html$", rel).group(1)
                orig = (f"sourceforge.net/p/bitcoin/mailman/message/{mid}/" if rel.startswith("allura_message")
                        else f"sourceforge.net/mailarchive/message.php?msg_id={mid}")
                meta[rel] = {"original": orig, "wayback_ts": ts, "bytes": int(n), "note": "reconstructed from fetch.log"}
    rows_p = os.path.join(OUT, "cdx_legacy_forum_rows.txt")
    if os.path.exists(rows_p):
        for ln in open(rows_p):
            ts, orig, st = ln.split()
            if st != "200":
                continue
            q = urllib.parse.unquote(orig)
            tn = re.search(r"thread_name=([^&]+)", q)
            mo = re.search(r"style=(nested|ultimate)&viewmonth=(\d{6})$", q)
            rel = (f"legacy_thread/{re.sub(r'[^A-Za-z0-9._-]+', '_', tn.group(1))}.html" if tn else
                   (f"legacy_month/{mo.group(1)}_{mo.group(2)}.html" if mo and "max_rows=25" in q else None))
            if rel and rel not in meta and os.path.exists(os.path.join(OUT, rel)):
                meta[rel] = {"original": orig, "wayback_ts": ts, "note": "reconstructed from cdx_legacy_forum_rows.txt"}


def main():
    os.makedirs(OUT, exist_ok=True)
    meta_path = os.path.join(OUT, "fetch_meta.json")
    meta = json.load(open(meta_path)) if os.path.exists(meta_path) else {}
    repair_meta(meta)

    def save_meta():
        with open(meta_path, "w") as f:
            json.dump(meta, f, indent=1, sort_keys=True)

    emails = json.load(open(SNI))
    ids = sorted({e["source_id"] for e in emails if e["source"] == "bitcoin-list"})
    only = sys.argv[1:] if len(sys.argv) > 1 else None

    sat_ids = sorted({e["source_id"] for e in emails
                      if e["source"] == "bitcoin-list" and e["sent_from"] == "Satoshi Nakamoto"})
    sat_months = sorted({e["date"][:7].replace("-", "") for e in emails
                         if e["source"] == "bitcoin-list" and e["sent_from"] == "Satoshi Nakamoto"})
    default = ["cdxlegacy", "legacythreads", "allura", "months"]
    only = only or default

    # 1. Allura message pages for Satoshi's bitcoin-list messages
    if "allura" in only:
        for mid in sat_ids:
            print("allura", mid, flush=True)
            fetch_capture(
                [f"sourceforge.net/p/bitcoin/mailman/message/{mid}/"],
                f"allura_message/{mid}.html", meta)
            save_meta()

    # 2. Legacy message.php pages (not in the default run: the legacy thread pages below
    #    already contain the same <pre> bodies)
    if "legacy" in only:
        for mid in sat_ids:
            print("legacy", mid, flush=True)
            fetch_capture(
                [f"sourceforge.net/mailarchive/message.php?msg_id={mid}"],
                f"legacy_message/{mid}.html", meta)
            save_meta()

    # 3. Legacy month pages ("nested" style shows every message body) for the months in which
    #    Satoshi posted: an independent (2012-2013) enumeration of the list's messages, and the
    #    only SourceForge copy for posts whose own pages were never archived.
    if "months" in only:
        rows_p = os.path.join(OUT, "cdx_legacy_forum_rows.txt")
        caps = {}
        if os.path.exists(rows_p):
            for ln in open(rows_p):
                ts, orig, st = ln.split()
                m = re.search(r"style=(nested|ultimate)&viewmonth=(\d{6})$", urllib.parse.unquote(orig))
                if st == "200" and m and "max_rows=25" in orig:
                    caps.setdefault((m.group(2), m.group(1)), (ts, orig))
        for ym in sat_months:
            got = False
            for style in ("nested", "ultimate"):
                if (ym, style) in caps and not got:
                    ts, orig = caps[(ym, style)]
                    dest_rel = f"legacy_month/{style}_{ym}.html"
                    if os.path.exists(os.path.join(OUT, dest_rel)):
                        got = True
                        continue
                    r = polite_get(f"https://web.archive.org/web/{ts}id_/{orig}")
                    if r is not None and r.status_code == 200:
                        os.makedirs(os.path.join(OUT, "legacy_month"), exist_ok=True)
                        with open(os.path.join(OUT, dest_rel), "wb") as f:
                            f.write(r.content)
                        meta[dest_rel] = {"original": orig, "wayback_ts": ts, "served": r.url, "bytes": len(r.content)}
                        print("  saved", dest_rel, flush=True)
                        got = True
                        save_meta()
            if not got:
                print("  no legacy month capture", ym, flush=True)
                meta[f"legacy_month/{ym}"] = {"error": "no 200 capture in cdx_legacy_forum_rows.txt"}
    # 4. Legacy thread_name listing: SURT canonicalisation sorts query parameters, so a prefix
    #    query on "forum.php?forum_name=bitcoin-list" also returns "...&thread_name=<Message-ID>"
    #    URLs, which reveal Message-IDs of list posts (Thunderbird IDs encode the send time).
    if "cdxlegacy" in only and not os.path.exists(os.path.join(OUT, "cdx_legacy_forum_rows.txt")):
        rows = cdx("sourceforge.net/mailarchive/forum.php?forum_name=bitcoin-list", exact=False)
        if rows is not None:
            ids = sorted({urllib.parse.unquote(re.search(r"thread_name=([^&]+)", o).group(1))
                          for ts, o, st in rows if "thread_name=" in o})
            with open(os.path.join(OUT, "cdx_legacy_forum_rows.txt"), "w") as f:
                f.write("\n".join(" ".join(r) for r in rows) + "\n")
            with open(os.path.join(OUT, "cdx_legacy_thread_names.txt"), "w") as f:
                f.write("\n".join(ids) + "\n")
            print("legacy thread_names:", len(ids), flush=True)
    # 5. Legacy thread pages (2012-2013 captures) for threads rooted at Satoshi's / related
    #    Message-IDs: show each message with date and link Message-IDs to SourceForge msg_ids.
    if "legacythreads" in only:
        rows_p = os.path.join(OUT, "cdx_legacy_forum_rows.txt")
        if os.path.exists(rows_p):
            done = set()
            for ln in open(rows_p):
                ts, orig, st = ln.split()
                if st != "200" or "thread_name=" not in orig:
                    continue
                tn = urllib.parse.unquote(re.search(r"thread_name=([^&]+)", orig).group(1))
                if tn in done or not re.search(r"CHILKAT|gmx\.com|finney|ernest|2d8ebb050910230459", tn):
                    continue
                done.add(tn)
                safe = re.sub(r"[^A-Za-z0-9._-]+", "_", tn)
                dest_rel = f"legacy_thread/{safe}.html"
                if os.path.exists(os.path.join(OUT, dest_rel)):
                    continue
                r = polite_get(f"https://web.archive.org/web/{ts}id_/{orig}")
                if r is not None and r.status_code == 200:
                    os.makedirs(os.path.join(OUT, "legacy_thread"), exist_ok=True)
                    with open(os.path.join(OUT, dest_rel), "wb") as f:
                        f.write(r.content)
                    meta[dest_rel] = {"original": orig, "wayback_ts": ts, "served": r.url, "bytes": len(r.content)}
                    print("  saved", dest_rel, flush=True)
                    save_meta()
    repair_meta(meta)
    save_meta()


if __name__ == "__main__":
    main()
