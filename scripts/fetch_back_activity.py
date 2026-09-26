#!/usr/bin/env python3
"""Fetch and cache Adam Back's timestamped public posts for the extended
posting-rhythm test (see scripts/back_rhythm_extended.py).

Sub-commands (each caches under data/candidates/back-activity/):

  bitcointalk   ninjastic.space API, author=adam3us (bitcointalk uid 101601).
                Raw API pages -> bitcointalk/ninjastic-page-NN.json
                Extract       -> bitcointalk/back-bitcointalk.jsonl
                Also fetches a few bitcointalk.org guest-view topic pages
                (>= 3 s apart) to check ninjastic's dates against the forum.
  bitcoindev    gnusha.org public-inbox mirror of bitcoin-dev, query
                f:"adam back" (download as mbox.gz). Headers only are kept
                (Date, From, Subject, Message-ID, In-Reply-To, User-Agent,
                X-Mailer, X-Mailer-*), bodies and other people's addresses
                are dropped.  -> bitcoin-dev/back-bitcoindev-headers.mbox,
                bitcoin-dev/back-bitcoindev.jsonl
  cypherpunks   cryptoanarchy.wiki cypherpunks archive (GitHub repo
                cryptoanarchywiki/mailing-list-archive-generator, pinned
                commit), 1996-1998, messages whose From is Adam Back.
                Header fields only.  -> cypherpunks/back-cypherpunks-1996-98.jsonl
  venona        Wayback copies of cypherpunks.venona.com (MHonArc archive of
                the Algebra.COM CDR node, which keeps the sender's own Date
                header) for a sample of months, Back's messages only; header
                block only.  -> cypherpunks/venona-back-headers.jsonl

Usage: python3 scripts/fetch_back_activity.py [bitcointalk|bitcoindev|cypherpunks|venona|all]
"""
import datetime as dt
import email
import email.policy
import email.utils
import glob
import gzip
import html
import json
import os
import re
import subprocess
import sys
import tempfile
import time
import urllib.parse
import urllib.error
import urllib.request

OUT = "data/candidates/back-activity"
UA = "Mozilla/5.0 (satoshi-research timing study; polite single-threaded fetch)"
CP_REPO = "https://github.com/cryptoanarchywiki/mailing-list-archive-generator.git"
CP_COMMIT = "5ee11c76b130aadf0ed74877107df5053ab0361b"  # 2022-02-21, HEAD when fetched


def get(url, data=None, timeout=120, tries=4):
    for i in range(tries):
        try:
            req = urllib.request.Request(url, data=data, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.read()
        except urllib.error.HTTPError:
            raise
        except Exception as e:  # connection refused / reset: back off (Wayback rate limit)
            if i == tries - 1:
                raise
            print(f"  retry in {60 * (i + 1)} s after {e!r}")
            time.sleep(60 * (i + 1))


# ---------------------------------------------------------------- bitcointalk
def bitcointalk():
    d = f"{OUT}/bitcointalk"
    os.makedirs(d, exist_ok=True)
    posts, last, page = [], None, 0
    while True:
        q = {"author": "adam3us", "limit": 200}
        if last:
            q["last"] = last
        url = "https://api.ninjastic.space/posts?" + urllib.parse.urlencode(q)
        raw = get(url)
        page += 1
        with open(f"{d}/ninjastic-page-{page:02d}.json", "wb") as f:
            f.write(raw)
        js = json.loads(raw)
        batch = js["data"]["posts"]
        print(f"page {page}: {len(batch)} posts (total_results={js['data']['total_results']})")
        if not batch:
            break
        posts += batch
        last = batch[-1]["post_id"]
        time.sleep(2)
    seen = set()
    with open(f"{d}/back-bitcointalk.jsonl", "w") as f:
        for p in sorted(posts, key=lambda p: p["date"]):
            if p["post_id"] in seen or p["author_uid"] != 101601:
                continue
            seen.add(p["post_id"])
            f.write(json.dumps({
                "post_id": p["post_id"], "topic_id": p["topic_id"], "title": p["title"],
                "board": p.get("board_name"), "date_utc": p["date"],
                "url": f"https://bitcointalk.org/index.php?topic={p['topic_id']}.msg{p['post_id']}#msg{p['post_id']}",
            }) + "\n")
    print(f"wrote {len(seen)} posts")
    # spot-check a few posts on bitcointalk.org itself (guest view shows UTC)
    sample = sorted(posts, key=lambda p: p["date"])
    picks = [sample[0], sample[len(sample) // 3], sample[2 * len(sample) // 3], sample[-1]]
    for p in picks:
        url = f"https://bitcointalk.org/index.php?topic={p['topic_id']}.msg{p['post_id']}#msg{p['post_id']}"
        fn = f"{d}/btt-topic-{p['topic_id']}-msg{p['post_id']}.html"
        if not os.path.exists(fn):
            time.sleep(3)
            with open(fn, "wb") as f:
                f.write(get(url))
        print("cached", fn)


# ---------------------------------------------------------------- bitcoin-dev
KEEP = ("Date", "From", "Subject", "Message-ID", "In-Reply-To", "User-Agent", "X-Mailer")


def bitcoindev():
    d = f"{OUT}/bitcoin-dev"
    os.makedirs(d, exist_ok=True)
    url = "https://gnusha.org/pi/bitcoindev/?" + urllib.parse.urlencode({"q": 'f:"adam back"', "x": "m"})
    raw = gzip.decompress(get(url, data=b"z=results+only"))
    msgs = re.split(rb"\n(?=From [^\n]*\n)", b"\n" + raw)
    out, mb = [], []
    for m in msgs:
        m = m.lstrip(b"\n")
        if not m.startswith(b"From "):
            continue
        body = m.split(b"\n", 1)[1]
        msg = email.message_from_bytes(body, policy=email.policy.compat32)
        frm = str(msg.get("From", ""))
        if "adam back" not in frm.lower():
            continue
        hdr = {k: str(msg.get(k)) for k in KEEP if msg.get(k) is not None}
        date = hdr.get("Date", "")
        try:
            t = email.utils.parsedate_to_datetime(date)
        except Exception:
            t = None
        mo = re.search(r"([+-]\d{4})\s*(\(.*\))?\s*$", date)
        out.append({
            "message_id": hdr.get("Message-ID", "").strip(), "subject": " ".join(hdr.get("Subject", "").split()),
            "from": frm, "date_header": date, "utc_offset": mo.group(1) if mo else None,
            "utc": t.astimezone(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ") if t else None,
            "mailer": hdr.get("User-Agent") or hdr.get("X-Mailer"),
            "url": "https://gnusha.org/pi/bitcoindev/" + urllib.parse.quote(hdr.get("Message-ID", "").strip("<> ")) + "/",
        })
        mb.append("From back-rhythm-extract\n" + "".join(f"{k}: {' '.join(v.split())}\n" for k, v in hdr.items()) + "\n")
    out.sort(key=lambda r: r["utc"] or "")
    with open(f"{d}/back-bitcoindev.jsonl", "w") as f:
        for r in out:
            f.write(json.dumps(r) + "\n")
    with open(f"{d}/back-bitcoindev-headers.mbox", "w") as f:
        f.write("".join(mb))
    print(f"bitcoin-dev: {len(out)} messages from Adam Back")


# ---------------------------------------------------------------- cypherpunks
def parse_cp_md(path):
    t = open(path, errors="replace").read()
    m = re.search(r"## Header Data\s*\n(.*?)\n## ", t, re.S)
    if not m:
        return None
    hd = {}
    for line in m.group(1).split("\n"):
        line = re.sub(r"<br>$", "", line.strip())
        line = line.replace("<span>@</span>", "@").replace("\\<", "<").replace("\\>", ">")
        if ": " in line:
            k, v = line.split(": ", 1)
            hd[k] = v
    s = re.search(r"^# (\d{4}-\d\d-\d\d) - (.*)$", t, re.M)
    hd["Subject"] = s.group(2).strip() if s else ""
    return hd


def cypherpunks(clone_dir=None):
    d = f"{OUT}/cypherpunks"
    os.makedirs(d, exist_ok=True)
    tmp = None
    if clone_dir is None:
        tmp = tempfile.mkdtemp()
        clone_dir = f"{tmp}/cpgen"
        subprocess.check_call(["git", "clone", "-q", "--filter=blob:none", "--sparse", CP_REPO, clone_dir])
        subprocess.check_call(["git", "-C", clone_dir, "checkout", "-q", CP_COMMIT])
        subprocess.check_call(["git", "-C", clone_dir, "sparse-checkout", "set",
                               "_emails/1996", "_emails/1997", "_emails/1998"])
    rows = []
    for f in sorted(glob.glob(f"{clone_dir}/_emails/199[678]/*/*.md")):
        hd = parse_cp_md(f)
        if not hd or not re.search(r"Adam Back|aba@|a\.back@", hd.get("From", ""), re.I):
            continue
        rel = f.split("_emails/")[1]
        y, mth, h = rel[:4], rel[5:7], os.path.basename(rel)[:-3]
        rows.append({
            "from": hd.get("From"), "subject": hd.get("Subject"), "message_id": hd.get("Message ID"),
            "in_reply_to": hd.get("Reply To"), "archive_utc": hd.get("UTC Datetime"),
            "archive_raw_date": hd.get("Raw Date"), "message_hash": hd.get("Message Hash"),
            "source_file": "_emails/" + rel,
            "url": f"https://mailing-list-archive.cryptoanarchy.wiki/archive/{y}/{mth}/{h}",
        })
    rows.sort(key=lambda r: r["archive_utc"] or "")
    with open(f"{d}/back-cypherpunks-1996-98.jsonl", "w") as f:
        for r in rows:
            f.write(json.dumps(r) + "\n")
    print(f"cypherpunks: {len(rows)} messages from Adam Back 1996-98")


# ---------------------------------------------------------------- venona
VENONA_MONTHS = ["1996/07", "1996/08", "1996/12", "1997/01", "1997/07", "1997/08",
                 "1998/01", "1998/06", "1998/07"]


def wb(url, ts="2024"):
    """Fetch the raw (id_) Wayback capture of url nearest to timestamp ts."""
    return get(f"http://web.archive.org/web/{ts}id_/{url}").decode("latin-1")


def cdx_msgs(month):
    """Archived venona message pages for a month: {msgNNNNN.html: timestamp}."""
    q = urllib.parse.urlencode({"url": f"cypherpunks.venona.com/date/{month}/msg*", "filter": "statuscode:200",
                                "collapse": "urlkey", "fl": "original,timestamp"})
    rows = get(f"http://web.archive.org/cdx/search/cdx?{q}").decode().split("\n")
    out = {}
    for r in rows:
        if r.strip():
            u, ts = r.split()
            out[u.rsplit("/", 1)[1]] = ts
    return out


def venona(max_per_month=8):
    d = f"{OUT}/cypherpunks"
    os.makedirs(d, exist_ok=True)
    out_path = f"{d}/venona-back-headers.jsonl"
    done = set()
    if os.path.exists(out_path):
        done = {json.loads(l)["url"] for l in open(out_path)}
    with open(out_path, "a") as out:
        for m in VENONA_MONTHS:
            idx_url = f"https://cypherpunks.venona.com/date/{m}/"
            t = wb(idx_url)
            time.sleep(2)
            archived = cdx_msgs(m)
            time.sleep(2)
            ents = re.findall(r'<A NAME="\d+" HREF="(msg\d+\.html)">(.*?)</A>.*?<EM>From</EM>:(.*?)</LI>', t, re.S | re.I)
            back = [(h, s) for h, s, f in ents if "Adam Back" in f]
            avail = [(h, s) for h, s in back if h in archived][:max_per_month]
            print(f"{m}: {len(ents)} msgs in index, {len(back)} by Adam Back, {len(avail)} of those fetched (Wayback has {len(archived)} pages)")
            for h, s in avail:
                url = idx_url + h
                if url in done:
                    continue
                try:
                    p = wb(url.replace("https://", "http://"), archived[h])
                except Exception as e:
                    print("  fail", url, e)
                    time.sleep(2)
                    continue
                time.sleep(4)
                hb = re.search(r"<!--X-Head-of-Message-->(.*?)<!--X-Head-of-Message-End-->", p, re.S)
                block = hb.group(1) if hb else p
                fields = {}
                for k, v in re.findall(r"<em>([A-Za-z-]+)</em>:\s*(.*?)</li>", block, re.S | re.I):
                    v = html.unescape(re.sub(r"<[^>]+>", "", v)).strip()
                    if k.lower() in ("to", "cc"):
                        continue  # drop other people's addresses
                    if k.lower() == "from":
                        v = re.sub(r"<.*?>|\[email.*?protected\]", "", v).strip()
                    fields[k] = " ".join(v.split())
                rec = {"url": url, "wayback": f"http://web.archive.org/web/{archived[h]}/{url.replace('https://', 'http://')}", **fields}
                out.write(json.dumps(rec) + "\n")
                out.flush()
                print("  ", h, fields.get("Date"), "|", fields.get("Subject", "")[:60])


if __name__ == "__main__":
    what = sys.argv[1] if len(sys.argv) > 1 else "all"
    if what in ("bitcointalk", "all"):
        bitcointalk()
    if what in ("bitcoindev", "all"):
        bitcoindev()
    if what in ("cypherpunks", "all"):
        cypherpunks(sys.argv[2] if len(sys.argv) > 2 else None)
    if what in ("venona", "all"):
        venona()
