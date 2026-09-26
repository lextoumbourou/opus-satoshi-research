#!/usr/bin/env python3
"""Extract Satoshi's SourceForge SVN commits from the bitcoin/bitcoin git history.

Clone (commits only, no trees/blobs; ~40 MB):
    git clone --bare --filter=tree:0 https://github.com/bitcoin/bitcoin.git data/satoshi/raw/bitcoin-git

The early history of bitcoin/bitcoin was imported from SourceForge SVN with git-svn. Satoshi's
SVN user name was `s_nakamoto`; git-svn records the SVN `svn:date` (server commit time, UTC) as
both author and committer date, and appends a `git-svn-id: ...trunk@REV` line to the message.

Some SVN commits appear twice on master (one copy with a git-svn-id, one without); we de-duplicate
on (author date, message) and keep the copy with the SVN revision.

Commits with author "Satoshi Nakamoto <satoshin@gmx.com>" (or the botched "--author=Satoshi
Nakamoto") were made in git by Gavin Andresen (committer) in Jul-Aug 2010 when he mirrored SVN
into git; their dates are Gavin's commit times, NOT Satoshi's, so they are written to a separate
file (svn_commits_git_mirror.jsonl) for reference and are not part of the corpus.

Output: data/satoshi/intermediate/svn_commits.jsonl, svn_commits_git_mirror.jsonl
         data/satoshi/raw/bitcoin-git-satoshi-log.txt (raw `git log` dump of the relevant commits)
"""
import json
import os
import re
import subprocess

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
REPO = os.path.join(ROOT, "data", "satoshi", "raw", "bitcoin-git")
OUT_DIR = os.path.join(ROOT, "data", "satoshi", "intermediate")
SEP = "\x1e"
FMT = SEP.join(["%H", "%an", "%ae", "%ad", "%aI", "%cn", "%ce", "%cd", "%cI", "%B"]) + "\x1d"


def git_log(*args):
    out = subprocess.run(
        ["git", "-C", REPO, "log", "master", "--date=raw", f"--format={FMT}", *args],
        check=True, capture_output=True,
    ).stdout.decode("utf-8", "replace")
    recs = []
    for chunk in out.split("\x1d"):
        chunk = chunk.lstrip("\n")
        if not chunk.strip():
            continue
        f = chunk.split(SEP)
        recs.append(dict(zip(["hash", "an", "ae", "ad_raw", "aI", "cn", "ce", "cd_raw", "cI", "body"], f)))
    return recs


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    svn = git_log("--author=s_nakamoto")
    mirror = git_log("--author=satoshin@gmx.com")
    # raw dump for provenance
    with open(os.path.join(ROOT, "data", "satoshi", "raw", "bitcoin-git-satoshi-log.txt"), "w") as f:
        f.write(subprocess.run(
            ["git", "-C", REPO, "log", "master", "--format=fuller", "--date=iso-strict",
             "--author=s_nakamoto", "--author=satoshin@gmx.com"],
            check=True, capture_output=True).stdout.decode("utf-8", "replace"))

    seen = {}
    for r in svn:
        m = re.search(r"git-svn-id: (\S+)@(\d+) ", r["body"])
        msg = re.sub(r"\n*git-svn-id: .*\n?", "", r["body"]).rstrip("\n")
        key = (r["aI"], msg)
        rec = seen.get(key)
        if rec is None or (m and not rec.get("svn_rev")):
            seen[key] = {"r": r, "msg": msg, "svn_rev": int(m.group(2)) if m else None,
                         "svn_url": m.group(1) if m else None, "dups": (rec or {}).get("dups", [])}
        seen[key]["dups"] = sorted(set(seen[key]["dups"] + [r["hash"]]))

    # The same SVN revision can appear with two different log messages (the SVN log message was
    # edited after the fact, e.g. r148). Merge on revision, keep the longest message, note the other.
    by_rev = {}
    for k, v in list(seen.items()):
        if v["svn_rev"] is None:
            continue
        if v["svn_rev"] in by_rev:
            other_k = by_rev[v["svn_rev"]]
            o = seen[other_k]
            keep, drop = (v, o) if len(v["msg"]) >= len(o["msg"]) else (o, v)
            keep["dups"] = sorted(set(keep["dups"] + drop["dups"]))
            keep["alt_msgs"] = keep.get("alt_msgs", []) + [drop["msg"]] + drop.get("alt_msgs", [])
            del seen[k if keep is o else other_k]
            by_rev[v["svn_rev"]] = other_k if keep is o else k
        else:
            by_rev[v["svn_rev"]] = k

    rows = []
    for (aI, msg), v in seen.items():
        r = v["r"]
        rev = v["svn_rev"]
        assert r["aI"].endswith("Z"), r["aI"]
        rows.append({
            "id": f"svn-r{rev}" if rev else f"svn-git-{r['hash'][:10]}",
            "source_type": "svn_commit",
            "venue": "bitcoin SourceForge SVN (trunk), via bitcoin/bitcoin git-svn import",
            "recipient": None,
            "thread": None,
            "timestamp_utc": r["aI"],
            "timestamp_raw": r["ad_raw"],
            "timestamp_precision": "second",
            "timestamp_source": "git author date (= SVN svn:date server commit time, recorded by git-svn in UTC; raw = unix epoch + offset)",
            "timestamp_tz_raw": r["ad_raw"].split()[-1],
            "url": f"https://github.com/bitcoin/bitcoin/commit/{r['hash']}",
            "raw_path": "data/satoshi/raw/bitcoin-git-satoshi-log.txt",
            "text": msg,
            "text_raw": r["body"].rstrip("\n"),
            "whitespace_preserved": True,
            "whitespace_notes": "git commit message as stored by git-svn (SVN log message verbatim, trailing newline normalised)",
            "svn_revision": rev,
            "git_hashes": v["dups"],
            "author": f"{r['an']} <{r['ae']}>",
            "committer": f"{r['cn']} <{r['ce']}>",
            "notes": "SVN commit by s_nakamoto. Timestamp is the SVN server commit time." + (
                "" if rev else " No git-svn-id on this copy; SVN revision unknown.") + (
                " Another git copy of this revision carries a different (earlier/edited) log message: "
                + json.dumps(v["alt_msgs"]) if v.get("alt_msgs") else ""),
        })
    rows.sort(key=lambda x: (x["timestamp_utc"], x["svn_revision"] or 0))
    with open(os.path.join(OUT_DIR, "svn_commits.jsonl"), "w") as f:
        for x in rows:
            f.write(json.dumps(x, ensure_ascii=False) + "\n")

    svn_msgs = {v["msg"].strip().lower(): k[0] for k, v in seen.items()}
    mrows = []
    for r in mirror:
        msg = r["body"].rstrip("\n")
        mrows.append({
            "git_hash": r["hash"], "author": f"{r['an']} <{r['ae']}>", "committer": f"{r['cn']} <{r['ce']}>",
            "author_date": r["aI"], "committer_date": r["cI"], "message": msg,
            "matching_svn_commit_date": svn_msgs.get(msg.strip().lower()),
            "notes": "git commit by Gavin Andresen attributing authorship to Satoshi; date is Gavin's commit time, not Satoshi's. Excluded from corpus.",
        })
    with open(os.path.join(OUT_DIR, "svn_commits_git_mirror.jsonl"), "w") as f:
        for x in mrows:
            f.write(json.dumps(x, ensure_ascii=False) + "\n")
    print(len(svn), "raw s_nakamoto commits ->", len(rows), "unique;", sum(1 for x in rows if x["svn_revision"]), "with SVN rev;",
          len(mrows), "git-mirror commits,", sum(1 for x in mrows if x["matching_svn_commit_date"]), "match an SVN message")


if __name__ == "__main__":
    main()
