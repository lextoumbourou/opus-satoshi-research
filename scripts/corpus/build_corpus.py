#!/usr/bin/env python3
"""Merge the per-source intermediate files into data/satoshi/posts.jsonl and print summary stats.

Pipeline (re-runnable; see data/satoshi/README.md):
  fetch_bitcointalk.py -> parse_bitcointalk.py -> fetch_bitcointalk_topics.py -> parse_bitcointalk.py
  fetch_gmane.py (+ metzdowd .txt.gz download) -> parse_metzdowd.py
  extract_svn_commits.py ; parse_code_comments.py ; parse_whitepaper.py
  fetch_/parse_ bitcoin_list, p2p_research, p2pfoundation_ning, private_emails (see README)
  build_corpus.py  (this script)  -> posts.jsonl + data/satoshi/summary.md

Only items written by Satoshi are included. Items flagged `exclude_from_corpus` in intermediates
are skipped.
"""
import collections
import glob
import hashlib
import json
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
INTER = os.path.join(ROOT, "data", "satoshi", "intermediate")
OUT = os.path.join(ROOT, "data", "satoshi", "posts.jsonl")
SUMMARY = os.path.join(ROOT, "data", "satoshi", "summary.md")

REQUIRED = ["id", "source_type", "venue", "recipient", "thread", "timestamp_utc", "timestamp_raw",
            "timestamp_precision", "url", "text", "text_raw", "notes"]
ORDER = REQUIRED[:7] + ["timestamp_precision", "timestamp_source", "timestamp_tz_raw", "timezone_basis", "authenticity", "timestamps_other",
                        "url", "raw_path", "whitespace_preserved", "whitespace_notes", "text", "text_raw", "notes"]
SOURCE_TYPES = {"email", "forum", "mailing_list", "p2pfoundation", "svn_commit", "code_comment", "whitepaper"}
ANNOTATIONS = {
    "p2pfoundation-ning-comment-52186": {
        "authenticity": "disputed",
        "authenticity_notes": "2014-03-07 'I am not Dorian Nakamoto' from Satoshi's P2P Foundation account, "
                              "3 years after the last accepted communication; account security questioned. "
                              "Excluded from the hour-of-day tables."},
}
# (kept, duplicate) pairs: the same e-mail distributed to two lists
SAME_MESSAGE = [("metzdowd-015014", "bitcoin-list-21356305")]
# files not part of the corpus proper
SKIP_FILES = {"svn_commits_git_mirror.jsonl"}


def norm(t):
    return re.sub(r"\W+", " ", (t or "").lower()).strip()


def main():
    items = []
    dup_skipped = []
    per_file = collections.Counter()
    for p in sorted(glob.glob(os.path.join(INTER, "*.jsonl"))):
        if os.path.basename(p) in SKIP_FILES:
            continue
        for ln, line in enumerate(open(p), 1):
            if not line.strip():
                continue
            r = json.loads(line)
            if r.get("exclude_from_corpus"):
                continue
            if r.get("duplicate_of_public"):
                # a private copy of a public list post (e.g. Malmi's copy of a bitcoin-list mail);
                # the public record is kept, this copy is only used as a cross-check there.
                dup_skipped.append(r["id"])
                continue
            r["_file"] = os.path.basename(p)
            items.append(r)
            per_file[os.path.basename(p)] += 1

    # normalise timezone_basis across sources:
    #   explicit  = offset/zone stated in the source itself (Date: header, epoch, PDF offset)
    #   verified  = zone not printed, but established empirically (bitcointalk guest display = UTC)
    #   inferred  = zone deduced indirectly (documented in timestamp_source/notes)
    #   assumed   = zone assumed without verification (documented)
    #   unknown   = local time known, zone unknown (timestamp_utc null)
    #   none      = no timestamp
    default_basis = {"forum": "verified", "svn_commit": "explicit", "whitepaper": "explicit",
                     "code_comment": "none"}
    for r in items:
        if not r.get("timezone_basis") and r.get("timestamp_utc"):
            f = r.get("_file")
            if f == "bitcoin_list.jsonl" and not r.get("timestamp_tz_raw"):
                r["timezone_basis"] = "verified"  # SourceForge archive time = UTC arrival (37 Gmane anchors)
            elif f == "p2pfoundation_ning.jsonl":
                r["timezone_basis"] = "verified"  # Ning display zone = UTC (Wayback relative-time anchors)
            elif f == "sourceforge_forums.jsonl":
                r["timezone_basis"] = "explicit"  # page shows "UTC"
        if not r.get("timezone_basis"):
            if r["source_type"] in default_basis and (r["source_type"] != "forum" or (r.get("venue") or "").startswith("bitcointalk")):
                r["timezone_basis"] = default_basis[r["source_type"]]
            elif r.get("timestamp_utc") is None:
                r["timezone_basis"] = "none" if not r.get("timestamp_raw") else "unknown"
            elif r.get("timestamp_tz_raw"):
                r["timezone_basis"] = "explicit"
            else:
                r["timezone_basis"] = "unspecified"

    # validation
    errors = []
    ids = collections.Counter(r["id"] for r in items)
    for i, n in ids.items():
        if n > 1:
            errors.append(f"duplicate id {i} x{n}")
    for r in items:
        for k in REQUIRED:
            if k not in r:
                r.setdefault(k, None)
        if r["source_type"] not in SOURCE_TYPES:
            errors.append(f"{r['id']}: bad source_type {r['source_type']}")
        t = r.get("timestamp_utc")
        if t is not None and not re.fullmatch(r"\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ", t):
            errors.append(f"{r['id']}: bad timestamp_utc {t}")
    if errors:
        print("\n".join(errors[:50]), file=sys.stderr)

    # annotations: authenticity and same-message duplicates across venues
    for r in items:
        r.setdefault("authenticity", ANNOTATIONS.get(r["id"], {}).get("authenticity", "accepted"))
        for k, v in ANNOTATIONS.get(r["id"], {}).items():
            r[k] = v
    # one e-mail Cc'd to two lists appears as two list posts: keep both, flag the second
    for a, b in SAME_MESSAGE:
        for r in items:
            if r["id"] == b:
                r["duplicate_message_of"] = a

    # near-duplicate text across items (same text posted to several venues)
    by_hash = collections.defaultdict(list)
    for r in items:
        n = norm(r.get("text"))
        if len(n) >= 200 and r["source_type"] != "code_comment":
            by_hash[hashlib.sha1(n[:400].encode()).hexdigest()].append(r["id"])
    for r in items:
        n = norm(r.get("text"))
        if len(n) >= 200 and r["source_type"] != "code_comment":
            others = [i for i in by_hash[hashlib.sha1(n[:400].encode()).hexdigest()] if i != r["id"]]
            if others:
                r["same_text_as"] = others

    items.sort(key=lambda r: (r.get("timestamp_utc") or "9999", r["source_type"], r["id"]))
    with open(OUT, "w") as f:
        for r in items:
            r.pop("_file", None)
            o = {k: r[k] for k in ORDER if k in r}
            o.update({k: v for k, v in r.items() if k not in o})
            f.write(json.dumps(o, ensure_ascii=False) + "\n")

    # ---- summary ----
    lines = []
    lines.append("| source_type | venue group | items | with UTC timestamp | earliest (UTC) | latest (UTC) |")
    lines.append("|---|---|---:|---:|---|---|")
    groups = collections.defaultdict(list)
    for r in items:
        v = r["venue"] or ""
        vg = ("bitcointalk.org" if v.startswith("bitcointalk") else
              "private email" if r["source_type"] == "email" else v.split(" (")[0])
        groups[(r["source_type"], vg)].append(r)
    for (st, vg), rs in sorted(groups.items()):
        ts = sorted(x["timestamp_utc"] for x in rs if x.get("timestamp_utc"))
        lines.append(f"| {st} | {vg} | {len(rs)} | {len(ts)} | {ts[0] if ts else '-'} | {ts[-1] if ts else '-'} |")
    ts = sorted(x["timestamp_utc"] for x in items if x.get("timestamp_utc"))
    lines.append(f"| **all** | | **{len(items)}** | **{len(ts)}** | {ts[0]} | {ts[-1]} |")
    lines.append("")
    prec = collections.Counter((r["source_type"], r.get("timestamp_precision")) for r in items)
    lines.append("Timestamp precision by source type: " + "; ".join(
        f"{st}/{p}: {n}" for (st, p), n in sorted(prec.items(), key=lambda x: (x[0][0], str(x[0][1])))))
    lines.append("")

    basis = collections.Counter((r["source_type"], r.get("timezone_basis")) for r in items)
    lines.append("Time-zone basis by source type (explicit = zone in source; verified = display zone checked; "
                 "inferred/assumed = see notes; unknown/none = no UTC): " + "; ".join(
                     f"{st}/{b}: {n}" for (st, b), n in sorted(basis.items(), key=lambda x: (x[0][0], str(x[0][1])))))
    lines.append("")
    ws = collections.Counter((r["source_type"], str(r.get("whitespace_preserved"))) for r in items)
    lines.append("whitespace_preserved by source type: " + "; ".join(
        f"{st}/{b}: {n}" for (st, b), n in sorted(ws.items())))
    lines.append("")
    if dup_skipped:
        lines.append(f"Private copies of public list posts not counted separately (duplicate_of_public): {len(dup_skipped)} "
                     f"({', '.join(dup_skipped)})")
        lines.append("")

    def hist_table(title, pred):
        sel = [r for r in items if r.get("timestamp_utc") and r.get("timestamp_precision") in ("second", "minute")
               and r.get("authenticity") != "disputed" and not r.get("duplicate_message_of") and pred(r)]
        types = sorted({r["source_type"] for r in sel})
        hist = {t: collections.Counter() for t in types}
        for r in sel:
            hist[r["source_type"]][int(r["timestamp_utc"][11:13])] += 1
        lines.append(title)
        lines.append("")
        lines.append("```")
        lines.append("hour  " + "  ".join(f"{t[:13]:>13}" for t in types) + "         all")
        for h in range(24):
            row = [hist[t][h] for t in types]
            lines.append(f"{h:02d}    " + "  ".join(f"{c:>13}" for c in row) + f"  {sum(row):>10}")
        lines.append("total " + "  ".join(f"{sum(hist[t].values()):>13}" for t in types) +
                     f"  {len(sel):>10}")
        lines.append("```")
        lines.append("")

    hist_table("UTC hour-of-day of Satoshi's items, A: only items whose time zone is explicit in the source or verified "
               "(second/minute precision; excludes authenticity=disputed and duplicate_message_of items):", lambda r: r.get("timezone_basis") in ("explicit", "verified"))
    hist_table("UTC hour-of-day, B: all items with a UTC timestamp incl. inferred/assumed zones (same exclusions):",
               lambda r: True)
    # whitespace sanity data (no interpretation): sentence boundaries followed by 1 vs 2+ spaces in `text`
    lines.append("Whitespace sanity data: count of sentence ends ('.', '?', '!' followed by spaces and a capital letter) "
                 "in `text`, by number of spaces, for items with whitespace_preserved == true (text inside [code] blocks "
                 "is not excluded):")
    lines.append("")
    lines.append("| source_type | venue group | items | 1 space | 2 spaces | 3+ spaces |")
    lines.append("|---|---|---:|---:|---:|---:|")
    for (st, vg), rs in sorted(groups.items()):
        rs = [r for r in rs if r.get("whitespace_preserved") is True]
        if not rs:
            continue
        c = collections.Counter()
        for r in rs:
            for m in re.finditer(r"[.?!]( +)[A-Z]", r.get("text") or ""):
                c[min(len(m.group(1)), 3)] += 1
        lines.append(f"| {st} | {vg} | {len(rs)} | {c[1]} | {c[2]} | {c[3]} |")
    lines.append("")

    # bitcointalk edit times (separate activity events)
    edits = collections.Counter()
    ne = 0
    for r in items:
        for o in r.get("timestamps_other") or []:
            if "Last Edit" in o.get("label", "") and o.get("utc") and (o.get("edited_by") in (None, "satoshi")):
                edits[int(o["utc"][11:13])] += 1
                ne += 1
    if ne:
        lines.append("")
        lines.append(f"bitcointalk 'Last Edit' times of Satoshi's posts (separate activity events, n={ne}; UTC hour):")
        lines.append("")
        lines.append("```")
        lines.append(" ".join(f"{h:02d}" for h in range(24)))
        lines.append(" ".join(f"{edits[h]:>2}" for h in range(24)))
        lines.append("```")
    open(SUMMARY, "w").write("\n".join(lines) + "\n")
    # splice into README between markers, if present
    readme = os.path.join(ROOT, "data", "satoshi", "README.md")
    if os.path.exists(readme):
        txt = open(readme).read()
        a, b = "<!-- BEGIN SUMMARY (generated by build_corpus.py) -->", "<!-- END SUMMARY -->"
        if a in txt and b in txt:
            txt = txt.split(a)[0] + a + "\n\n" + "\n".join(lines) + "\n\n" + b + txt.split(b)[1]
            open(readme, "w").write(txt)
    print("\n".join(lines))
    print("\nper intermediate file:", dict(per_file))
    print("wrote", OUT, len(items), "items;", len(errors), "validation errors")


if __name__ == "__main__":
    main()
