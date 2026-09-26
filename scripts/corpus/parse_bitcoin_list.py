#!/usr/bin/env python3
"""Build data/satoshi/intermediate/bitcoin_list.jsonl: Satoshi Nakamoto's posts to the
bitcoin-list mailing list (bitcoin-list@lists.sourceforge.net), Dec 2008 - Dec 2010.

Inputs (all under data/satoshi/raw/):
  sourceforge_bitcoin_list/allura_message/<ID>.html   Wayback raw captures of SourceForge's Allura
        archive page https://sourceforge.net/p/bitcoin/mailman/message/<ID>/ (fetch_bitcoin_list.py)
  sourceforge_bitcoin_list/lugaxker_bitcoin-list-archive.txt   text transcription of the Allura
        month listings made via Wayback in May 2022 by github.com/lugaxker/nakamoto-archive
        (fallback when no Allura page capture exists)
  sourceforge_bitcoin_list/gmane_bitcoin_user/*.eml   raw 2011+ bitcoin-list articles (TZ anchor)
  sni-repo/server/data/emails.json                    Nakamoto Institute (ids, dates, text)
  ../intermediate/private_emails.jsonl (read-only)    Date: headers of copies received privately
        (Malmi's published mailbox, Trammell's mbox)

TIMESTAMPS. SourceForge's archive shows "YYYY-MM-DD HH:MM:SS" without a zone. Using the 2011-2014
bitcoin-list messages that Gmane also archived raw, the SourceForge display equals, to the second,
the `Received: ... by sfs-ml-N.v29.ch3.sourceforge.com ...; <date> +0000` hop (arrival at the
SourceForge list server) in UTC in every matchable case (15/15), and NOT the Date: header (e.g.
Date 20:11:16Z vs SF 22:47:55Z; a sender with a fast clock: Date 03:39:34Z vs SF 03:37:03Z).
So `sf_display` = UTC time of arrival at SourceForge. Where the sender's Date: header is known from
another copy (Malmi's / Trammell's received copies, metzdowd/Gmane raw, or a Thunderbird
Message-ID hex timestamp), `timestamp_utc` uses that (it is Satoshi's own send time); otherwise
`timestamp_utc` = SourceForge arrival time. `timestamp_list_arrival_utc` always holds the SF value.
Observed arrival lag vs Date header for Satoshi's posts: 16 s .. 3 min typically (GMX), 28 min once
(0.3.6 alert), 2 h 32 min once (vistomail/anonymousspeech relay, Jan 2009).
"""
import html as htmlmod
import json
import os
import re
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
RAWD = os.path.join(ROOT, "data", "satoshi", "raw", "sourceforge_bitcoin_list")
SNI = os.path.join(ROOT, "data", "satoshi", "raw", "sni-repo", "server", "data", "emails.json")
PRIV = os.path.join(ROOT, "data", "satoshi", "intermediate", "private_emails.jsonl")
OUT = os.path.join(ROOT, "data", "satoshi", "intermediate", "bitcoin_list.jsonl")
LUG = os.path.join(RAWD, "lugaxker_bitcoin-list-archive.txt")
REL = lambda p: os.path.relpath(p, ROOT)  # noqa: E731
ISO = "%Y-%m-%dT%H:%M:%SZ"

FULL_ADDR = {"satoshi@vi...": "satoshi@vistomail.com", "satoshin@gm...": "satoshin@gmx.com"}


def iso(dt):
    return dt.astimezone(timezone.utc).strftime(ISO)


def sf_to_iso(s):
    return datetime.strptime(s, "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc).strftime(ISO)


def msgid_time(mid):
    m = re.match(r"<?([0-9A-F]{8})\.\d+@", mid or "")
    if not m:
        return None
    t = datetime.fromtimestamp(int(m.group(1), 16), timezone.utc)
    return iso(t) if 2008 <= t.year <= 2012 else None


def parse_allura(path, mid):
    s = open(path, encoding="utf-8", errors="replace").read()
    m = re.search(
        rf'<table id="msg{mid}">.*?<b><a href="[^"]*">(.*?)</a></b>.*?<small>From: (.*?) - '
        r'(\d{4}-\d\d-\d\d \d\d:\d\d:\d\d)</small>.*?<td class="email-body"><pre>(.*?)</pre>', s, re.S)
    if not m:
        return None
    body = m.group(4)
    body = re.sub(r"<a [^>]*>(.*?)</a>", r"\1", body, flags=re.S)
    body = htmlmod.unescape(body)
    return {"subject": htmlmod.unescape(m.group(1)).strip(), "from": htmlmod.unescape(m.group(2)).strip(),
            "sf_display": m.group(3), "body": body}


def parse_legacy():
    """Messages from legacy (pre-2013) SourceForge mailarchive pages captured by Wayback:
    thread pages (forum.php?thread_name=<Message-ID>) and month pages (style=nested).
    Returns {msg_id: {...}} and {msg_id: thread_name Message-ID} for thread roots by Satoshi."""
    import glob
    msgs, roots = {}, {}
    # thread_name (Message-ID of the thread's root post) <- saved filename (sanitised Message-ID)
    names = {}
    tnp = os.path.join(RAWD, "cdx_legacy_thread_names.txt")
    if os.path.exists(tnp):
        for tn in open(tnp).read().split():
            names[re.sub(r"[^A-Za-z0-9._-]+", "_", tn)] = tn
    meta_p = os.path.join(RAWD, "fetch_meta.json")
    meta = json.load(open(meta_p)) if os.path.exists(meta_p) else {}
    for sub in ("legacy_thread", "legacy_month"):
        for path in sorted(glob.glob(os.path.join(RAWD, sub, "*.html"))):
            s = open(path, encoding="utf-8", errors="replace").read()
            found = list(re.finditer(
                r'<a href="/mailarchive/message\.php\?msg_id=(\d+)">(.*?)</a>.*?<small>From: (.*?) -\s*'
                r'(\d{4}-\d\d-\d\d \d\d:\d\d)</small>.*?<pre>(.*?)</pre>', s, re.S))
            sat_in_page = [m.group(1) for m in found if "atoshi" in htmlmod.unescape(m.group(3))]
            for k, m in enumerate(found):
                body = re.sub(r"<a [^>]*>(.*?)</a>", r"\1", m.group(5), flags=re.S)
                rec = {"subject": htmlmod.unescape(m.group(2)).strip(), "from": htmlmod.unescape(m.group(3)).strip(),
                       "sf_minute": m.group(4), "body": htmlmod.unescape(body), "path": path,
                       "wayback": meta.get(os.path.relpath(path, RAWD), {}).get("wayback_ts")}
                msgs.setdefault(m.group(1), rec)
                # The legacy archive names each thread after ONE member message's Message-ID (not
                # necessarily the first). Attribute it to Satoshi's message only when unambiguous:
                # the ID has the form of Satoshi's mailer (CHILKAT-MID-...@server123 = vistomail,
                # <hex>.<n>@gmx.com = Thunderbird/GMX) and the page holds exactly one Satoshi post.
                tn = names.get(os.path.basename(path)[:-5]) if sub == "legacy_thread" else None
                if (tn and sat_in_page == [m.group(1)]
                        and re.match(r"(CHILKAT-MID-.*@server123|[0-9A-F]{8}\.\d+@gmx\.com)$", tn)):
                    roots[m.group(1)] = "<" + tn + ">"
    return msgs, roots


def parse_lugaxker():
    if not os.path.exists(LUG):
        return []
    s = open(LUG, encoding="utf-8").read()
    out = []
    for b in s.split("\n---\n")[1:]:
        lines = b.strip("\n").split("\n")
        if len(lines) < 2:
            continue
        m = re.match(r"From: (.*) - (\d{4}-\d\d-\d\d \d\d:\d\d:\d\d)$", lines[1])
        if not m:
            continue
        body = "\n".join(lines[3:] if len(lines) > 2 and lines[2] == "" else lines[2:])
        out.append({"subject": lines[0].strip(), "from": m.group(1), "sf_display": m.group(2), "body": body})
    return out


def strip_quotes(body):
    lines = body.split("\n")
    keep = []
    for i, ln in enumerate(lines):
        if re.match(r"^\s*>", ln):
            continue
        if re.search(r"(wrote|writes):\s*$", ln):
            j = i + 1
            while j < len(lines) and lines[j].strip() == "":
                j += 1
            if j < len(lines) and re.match(r"^\s*>", lines[j]):
                continue
        keep.append(ln)
    out = "\n".join(keep)
    return re.sub(r"\n{3,}", "\n\n", out).strip("\n") + "\n"


def norm(t):
    return re.sub(r"\s+", " ", t).strip()


def main():
    sni = [e for e in json.load(open(SNI)) if e["source"] == "bitcoin-list" and e["sent_from"] == "Satoshi Nakamoto"]
    lug = parse_lugaxker()
    priv = [json.loads(l) for l in open(PRIV)] if os.path.exists(PRIV) else []
    legacy, roots = parse_legacy()
    items = []
    for e in sorted(sni, key=lambda x: x["date"]):
        mid = e["source_id"]
        sf_iso = e["date"]
        allura_path = os.path.join(RAWD, "allura_message", f"{mid}.html")
        a = parse_allura(allura_path, mid) if os.path.exists(allura_path) else None
        lg = [x for x in lug if sf_to_iso(x["sf_display"]) == sf_iso and "atoshi" in x["from"]]
        lg = lg[0] if lg else None
        lgc = legacy.get(mid)
        src, raw_path, notes = None, None, []
        if a:
            src, raw_path, body, frm, subj, sfd = "allura", REL(allura_path), a["body"], a["from"], a["subject"], a["sf_display"]
            ws, wsn = True, ("Body taken from the <pre> block of SourceForge's archive page (Wayback raw capture); "
                              "spaces, double spaces after full stops and line breaks are as archived by SourceForge "
                              "(HTML entities unescaped, <a> tags removed).")
        elif lgc:
            src, raw_path, body, frm, subj = "sourceforge_legacy", REL(lgc["path"]), lgc["body"], lgc["from"], lgc["subject"]
            sfd = lg["sf_display"] if lg and lg["sf_display"][:16] == lgc["sf_minute"] else None
            ws, wsn = True, ("Body taken from the <pre> block of the legacy (pre-2013) SourceForge mail-archive page "
                              "(Wayback raw capture); spaces, double spaces and line breaks as archived by "
                              "SourceForge (identical to the Allura <pre> text where both exist, apart from trailing "
                              "newlines).")
            notes.append("No Wayback capture of the Allura message page; body from the legacy SourceForge archive "
                         "page (minute-precision time there; seconds from the lugaxker transcription of the Allura listing).")
            if sfd is None:
                sfd = lgc["sf_minute"] + ":00"
                notes.append("Seconds unknown (legacy page shows minutes only).")
        elif lg:
            src, raw_path, body, frm, subj, sfd = "lugaxker", REL(LUG), lg["body"], lg["from"], lg["subject"], lg["sf_display"]
            ws, wsn = "unknown", ("No Allura page capture available; body from lugaxker/nakamoto-archive's text "
                                   "transcription of the SourceForge month listing (via Wayback, May 2022). Double "
                                   "spaces after full stops appear preserved (they occur in the text), but trailing "
                                   "whitespace / exact line breaks are not verifiable.")
            notes.append("No Wayback capture of the Allura message page was retrievable; text and SF time from the lugaxker transcription.")
        else:
            src, raw_path, body, frm, subj, sfd = "sni", REL(SNI), e["text"], "Satoshi Nakamoto", e["subject"], None
            ws, wsn = "unknown", "Fallback: Nakamoto Institute emails.json text (derived from SourceForge HTML)."
            notes.append("No raw copy found; text from Nakamoto Institute only.")
        if not body.endswith("\n"):
            body += "\n"
        # cross-check text with SNI and lugaxker
        for lab, t in (("Nakamoto Institute", e["text"]), ("lugaxker transcription", lg["body"] if lg else None),
                       ("legacy SourceForge page", lgc["body"] if lgc else None)):
            if t is not None and norm(t) != norm(body):
                notes.append(f"Text differs from {lab} copy beyond whitespace (check).")
        if sfd and sf_to_iso(sfd) != sf_iso:
            notes.append(f"SF display {sfd} != SNI date {sf_iso}.")
        sf_arrival = sf_to_iso(sfd) if sfd else sf_iso
        others = [{"label": "SourceForge archive display time (= UTC arrival at SourceForge list server)",
                   "raw": sfd or sf_iso, "utc": sf_arrival},
                  {"label": "Nakamoto Institute emails.json date", "raw": e["date"], "utc": e["date"]}]
        if lg and src != "lugaxker":
            others.append({"label": "lugaxker transcription SF time", "raw": lg["sf_display"], "utc": sf_to_iso(lg["sf_display"])})
        if lgc:
            others.append({"label": "legacy SourceForge archive page time (minute precision, UTC arrival)",
                           "raw": lgc["sf_minute"], "utc": lgc["sf_minute"].replace(" ", "T") + ":00Z"})
            if sfd and sfd[:16] != lgc["sf_minute"]:
                notes.append(f"Legacy SF minute {lgc['sf_minute']} disagrees with {sfd}.")
        # sender Date: headers from privately received copies
        date_hdr, date_src = None, None
        subj_core = re.sub(r"^(Re: )?\[bitcoin-list\] ", "", e["subject"]).strip()
        for p in priv:
            if not p.get("duplicate_of_public") or "bitcoin-list" not in p["duplicate_of_public"]:
                continue
            psub = re.sub(r"^(Re: )?(\[bitcoin-list\] )?", "", p.get("subject") or "").strip()
            if psub[:30] != subj_core[:30] or not p.get("timestamp_utc"):
                continue
            pdt = datetime.strptime(p["timestamp_utc"], ISO).replace(tzinfo=timezone.utc)
            lag = (datetime.strptime(sf_arrival, ISO).replace(tzinfo=timezone.utc) - pdt).total_seconds()
            if not (0 <= lag <= 4 * 3600):
                continue
            who = "Malmi" if "malmi" in p["id"] else ("Trammell" if "trammell" in p["id"] else p["id"])
            others.append({"label": f"Date: header in {who}'s received copy ({p['id']})", "raw": p["timestamp_raw"], "utc": p["timestamp_utc"]})
            if date_hdr is None:
                date_hdr, date_src = p, who
            if p.get("message_id") and mid not in roots:
                roots[mid] = p["message_id"]
        msgid = roots.get(mid)
        msgid_src = ("SourceForge legacy archive thread_name (unambiguous: Satoshi's mailer ID format, single "
                     "Satoshi post in thread)") if msgid else None
        if date_hdr and date_hdr.get("message_id") and msgid == date_hdr["message_id"]:
            msgid_src = f"{date_src}'s received copy (and SourceForge thread_name)"
        if not msgid:
            # Thunderbird IDs listed as legacy thread_names whose hex send-time matches this post
            tnp = os.path.join(RAWD, "cdx_legacy_thread_names.txt")
            arr = datetime.strptime(sf_arrival, ISO).replace(tzinfo=timezone.utc)
            for tn in (open(tnp).read().split() if os.path.exists(tnp) else []):
                t = msgid_time(tn)
                if not t or not tn.endswith("@gmx.com") or "<" + tn + ">" in roots.values():
                    continue
                lag = (arr - datetime.strptime(t, ISO).replace(tzinfo=timezone.utc)).total_seconds()
                if 0 <= lag <= 600 and (not date_hdr or date_hdr["timestamp_utc"] == t):
                    msgid = "<" + tn + ">"
                    msgid_src = ("SourceForge legacy thread_name listed in Wayback CDX; matched by its Thunderbird "
                                 "hex send-time" + (" (= Date: header)" if date_hdr else "") + "; page itself not archived")
        mt = msgid_time(msgid)
        if mt:
            others.append({"label": "Thunderbird Message-ID hex timestamp (sender's clock)", "raw": msgid, "utc": mt})
        if date_hdr:
            ts_utc, ts_raw = date_hdr["timestamp_utc"], date_hdr["timestamp_raw"]
            ts_source = f"Date: header of the same message in {date_src}'s received copy (sender's clock)"
            tz_raw = ts_raw.split()[-1]
            lag = (datetime.strptime(sf_arrival, ISO) - datetime.strptime(ts_utc, ISO)).total_seconds()
            notes.append(f"SourceForge arrival {sf_arrival} is {lag:+.0f} s after the Date: header.")
        elif mt:
            ts_utc, ts_raw, tz_raw = mt, msgid, None
            ts_source = "Thunderbird Message-ID hex timestamp (sender's clock; equals Date: header in all checked cases)"
        else:
            ts_utc, ts_raw, tz_raw = sf_arrival, sfd or e["date"], None
            ts_source = ("SourceForge archive display time, no zone shown; established = UTC arrival time at "
                         "SourceForge (not the sender's Date: header)")
            if "vi..." in frm:
                notes.append("Sent via vistomail/anonymousspeech web mail: relay delays before reaching SourceForge "
                             "of up to 2 h 32 min are documented for this route (msg 21356305), so the send time may "
                             "be earlier than timestamp_utc.")
            else:
                notes.append("Timestamp is SourceForge arrival; for GMX-era posts with known Date: headers the lag was 16 s - 28 min.")
        fa = re.search(r"<(.*?)>", frm)
        disp_addr = fa.group(1) if fa else None
        items.append({
            "id": f"bitcoin-list-{mid}",
            "source_type": "mailing_list",
            "venue": "bitcoin-list@lists.sourceforge.net (SourceForge-hosted Mailman list)",
            "recipient": "bitcoin-list",
            "thread": re.sub(r"^(Re: )+", "", e["subject"]).strip(),
            "timestamp_utc": ts_utc,
            "timestamp_raw": ts_raw,
            "timestamp_precision": "second",
            "timestamp_source": ts_source,
            "timestamp_tz_raw": tz_raw,
            "timestamp_list_arrival_utc": sf_arrival,
            "timestamps_other": others,
            "url": f"https://sourceforge.net/p/bitcoin/mailman/message/{mid}/",
            "raw_path": raw_path,
            "text_source": src,
            "text": strip_quotes(body),
            "text_raw": body,
            "whitespace_preserved": ws,
            "whitespace_notes": wsn,
            "from_address": FULL_ADDR.get(disp_addr, disp_addr),
            "from_display": frm,
            "message_id": msgid,
            "message_id_source": msgid_src,
            "in_reply_to": None,
            "subject": subj,
            "notes": " ".join(notes) or None,
        })
    with open(OUT, "w") as f:
        for it in items:
            f.write(json.dumps(it, ensure_ascii=False) + "\n")
    print(f"wrote {len(items)} items to {REL(OUT)}")
    for it in items:
        print(it["id"], it["timestamp_utc"], it["timestamp_list_arrival_utc"], it["text_source"], "|", it["subject"][:50])


if __name__ == "__main__":
    main()
