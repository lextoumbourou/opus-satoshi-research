#!/usr/bin/env python3
"""Check a Hacker News commenter's claim (April 2026) about Adam Back's writing
habits against Satoshi's: bracketed full sentences with the full stop outside,
"(ie"/"(eg" without dots, and the word "nor".

Back: his own text in the randombit Cryptography-list monthly archives we hold
(Nov 2010 - Jun 2011, while Satoshi was active), with quoted lines ("> ...")
and signatures removed.
Satoshi: the `text` field of forum posts, emails and mailing-list items in
data/satoshi/posts.jsonl.

Small sample on Back's side (a few thousand words), so treat rates as rough.
Output: data/candidates/back-activity/writing-habits.txt
"""
import glob
import json
import re

PATTERNS = {
    'bracketed full sentence, full stop outside  "(Xxx ...)."': r"\([A-Z][^()]{15,}\)\.",
    '"(ie" / "(eg" without dots': r"\((ie|eg)[ ,]",
    '"i.e." / "e.g." with dots': r"\b(i\.e\.|e\.g\.)",
    '"nor" as a word': r"\bnor\b",
}


def back_texts():
    out = []
    for p in sorted(glob.glob("data/lists/randombit/pipermail/*.txt")):
        raw = open(p, encoding="latin-1").read()
        for m in re.split(r"\n(?=From [^\n]*\d{4}\n)", raw):
            hdr, _, body = m.partition("\n\n")
            if not re.search(r"(?im)^From:.*(adam at cypherspace|Adam Back)", hdr):
                continue
            body = "\n".join(l for l in body.split("\n") if not l.startswith(">"))
            body = body.split("\n-- \n")[0].split("_______________________________________________")[0]
            out.append(body)
    return out


def satoshi_texts():
    rows = [json.loads(l) for l in open("data/satoshi/posts.jsonl")]
    return [r.get("text") or "" for r in rows if r.get("source_type") in ("forum", "email", "mailing_list")]


def report(label, texts):
    words = sum(len(t.split()) for t in texts)
    lines = [f"{label}: {len(texts)} items, {words} words"]
    for name, pat in PATTERNS.items():
        n = sum(len(re.findall(pat, t)) for t in texts)
        lines.append(f"   {name:55s} {n:5d}   ({1e4 * n / max(words, 1):5.1f} per 10,000 words)")
    return lines, words


def main():
    b, bw = report("Adam Back, randombit Cryptography list (Nov 2010 - Jun 2011)", back_texts())
    s, sw = report("Satoshi, forum posts + emails + list messages", satoshi_texts())
    out = b + [""] + s
    out += ["", "Expected Satoshi counts at Back's rates, for Satoshi's word count:"]
    bt = back_texts()
    st = satoshi_texts()
    for name, pat in PATTERNS.items():
        rate = sum(len(re.findall(pat, t)) for t in bt) / max(bw, 1)
        obs = sum(len(re.findall(pat, t)) for t in st)
        out.append(f"   {name:55s} expected {rate * sw:6.0f}   observed {obs:4d}")
    text = "\n".join(out) + "\n"
    open("data/candidates/back-activity/writing-habits.txt", "w").write(text)
    print(text)


if __name__ == "__main__":
    main()
