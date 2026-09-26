#!/usr/bin/env python3
"""Decide which tracked files can be published and which are third-party
copies that should be replaced by a pointer to the original source.

Policy (see data/SOURCES.md):
  REMOVE  published works: news and magazine articles, blog essays, academic
          papers, court filings, images and screenshots from articles, video
          transcripts, tweets, Wikipedia copies.
  KEEP    our own notes, scripts, logs and derived data; mailing-list and forum
          archives; Satoshi's writing and the emails his correspondents
          published; Wayback captures of profile and listing pages; the
          blockchain; open-source software (Bitcoin releases, hashcash,
          Crypto++, Mixmaster, wxWidgets, OpenSSL).

For every REMOVE file the script records its size, SHA-256 and the best
source URL it can find (a SOURCE: header, a canonical link, or a line in
our notes/logs that names the file next to a URL), so anyone can fetch the
original and check it against the hash.

Usage: classify_for_publication.py OUT_DIR
Writes OUT_DIR/remove-paths.txt and OUT_DIR/sources.csv.
"""
import csv
import hashlib
import json
import os
import re
import subprocess
import sys

# Policy: remove *published works* (articles, essays, papers, court filings,
# media, tweets, Wikipedia copies) and keep community archives (mailing lists,
# forums, emails published by their recipients), Satoshi's own writing,
# open-source software and our own work.
REMOVE_PREFIXES = [
    "data/prior-research/",                       # survey copies of articles, papers, videos, tweets
    "data/candidates/sassaman-alibi/",            # Black Hat's schedule page
]
REMOVE_EXACT_RE = [
    # data/claims: articles, essays, media, tweets, court filings, Wikipedia
    r"^data/claims/A-",                            # news/media items (NYT, Fortune, NPR, TechCrunch, Quanta, YouTube, ...)
    r"^data/claims/B-COPA-", r"^data/claims/B-opencrypto-",
    r"^data/claims/B-gwern-", r"^data/claims/B-hashcash-2002\.", r"^data/claims/B-rizzo-",
    r"^data/claims/C-andresen-", r"^data/claims/C-wikipedia-", r"^data/claims/C-finney-running-bitcoin-tweet",
    r"^data/claims/C-rpow-net-",
    r"^data/claims/D-(dlnews|hatch|lerner|monetaryfuture|morris|sassaman-ieet|sassaman-obit|szabo|wikipedia|tweet)",
    # published documents inside the Satoshi corpus sources
    r"^data/satoshi/raw/private_emails/hal_finney/(coindesk-.*\.html|coindesk_.*\.png|finneynakamotoemails\.pdf)$",
    r"^data/satoshi/raw/private_emails/hearn/First-Witness-Statement.*\.pdf$",
    r"^data/satoshi/raw/private_emails/adam_back/.*\.pdf$",
    r"^data/satoshi/raw/private_emails/andresen/",
    r"^data/satoshi/raw/private_emails/wei_dai/",
    r"^data/satoshi-hal/finneynakamotoemails\.pdf$",
    # academic papers captured from the Wayback Machine (keep the listing pages)
    r"^data/wayback/ucl-crypto/(ITBenelux|ps113|WetICE)",
    r"^data/wayback/haber/(wb\d+-.*\.ps|sureid\.)",
]
KEEP_EXCEPTIONS_RE = [
    r"^data/prior-research/metadata/satoshinakamoto-nakamotoinstitute\.asc$",   # Satoshi's public PGP key
]
URL_RE = re.compile(r"https?://[^\s\"'<>)\]`|,]+")
TEXT_EXT = {".txt", ".md", ".html", ".htm", ".json", ".eml", ".mbox", ".wikitext", ".hdr", ".tsv", ".csv", ".log", ".xml", ""}


def tracked():
    out = subprocess.run(["git", "ls-files", "-z"], capture_output=True, check=True).stdout
    return [p for p in out.decode().split("\0") if p]


def classify(p):
    if any(re.search(r, p) for r in KEEP_EXCEPTIONS_RE):
        return "keep"
    if any(p.startswith(x) for x in REMOVE_PREFIXES) or any(re.search(r, p) for r in REMOVE_EXACT_RE):
        return "remove"
    return "keep"


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def url_from_meta(p):
    for cand in (p + ".meta.json",):
        if os.path.exists(cand):
            try:
                u = json.load(open(cand)).get("url")
                if u:
                    return u
            except Exception:
                pass
    return None


WAYBACK_BASE = {
    "data/wayback/citeseer/": lambda b, ts: f"http://citeseer.ist.psu.edu:80/{b.split('-')[0]}.html",
    "data/wayback/p2pfoundation/": lambda b, ts: "http://p2pfoundation.ning.com/profile/SatoshiNakamoto",
    "data/wayback/forum-profile/": lambda b, ts: "https://bitcointalk.org/index.php?action=profile;u=3",
    "data/wayback/raw/bitcoin.org-": lambda b, ts: "http://bitcoin.org/",
}


def wayback_url(p):
    b = os.path.basename(p)
    m = re.search(r"(?<!\d)((?:19|20)\d{12})(?!\d)", b)
    if not m or not p.startswith("data/wayback/"):
        return None
    ts = m.group(1)
    for pre, fn in WAYBACK_BASE.items():
        if p.startswith(pre):
            return f"https://web.archive.org/web/{ts}/{fn(b, ts)}"
    return f"https://web.archive.org/web/{ts}/ (original URL: see the README in this folder)"


def url_from_file(p):
    ext = os.path.splitext(p)[1].lower()
    if ext not in TEXT_EXT or os.path.getsize(p) > 30_000_000:
        return None
    try:
        head = open(p, "rb").read(400_000).decode("utf-8", "replace")
    except OSError:
        return None
    m = re.search(r"(?im)^\s*\"?(?:SOURCE|Source|source|URL|url|Fetched from)\"?\s*[:=]\s*\"?(https?://[^\s\"]+)", head[:3000])
    if m:
        return m.group(1).rstrip(".,;)")
    for pat in (r'<link[^>]+rel="canonical"[^>]+href="([^"]+)"', r'<link[^>]+href="([^"]+)"[^>]+rel="canonical"',
                r'<meta[^>]+property="og:url"[^>]+content="([^"]+)"'):
        m = re.search(pat, head, re.I)
        if m and m.group(1).startswith("http"):
            return m.group(1)
    m = re.search(r"https?://web\.archive\.org/web/\d{8,14}(?:id_)?/(https?://[^\s\"'<>]+)", head)
    if m:
        return m.group(0)
    return None


def build_mention_index(keep_paths):
    """Map basename -> first URL on a line of our own notes/logs that mentions it."""
    idx = {}
    docs = [p for p in keep_paths if p.endswith((".md", ".json", ".txt", ".log")) and
            (p.startswith(("notes/", "data/")) or p in ("log.md", "README.md"))]
    for d in docs:
        try:
            text = open(d, encoding="utf-8", errors="replace").read()
        except OSError:
            continue
        if d.endswith("FETCH_LOG.json"):
            try:
                for k, v in json.load(open(d)).items():
                    urls = v.get("url_candidates") or []
                    if urls:
                        idx.setdefault(os.path.basename(k), urls[0])
            except Exception:
                pass
            continue
        lines = text.splitlines()
        for i, line in enumerate(lines):
            names = re.findall(r"[\w.\-]+\.(?:html|txt|json|pdf|PDF|eml|mbox|wikitext|ps|jpg|png|zip|tgz|gz|md|xml|asc|log)", line)
            if not names:
                continue
            urls = URL_RE.findall(line)
            if not urls:
                for j in (i - 1, i + 1, i - 2, i + 2):
                    if 0 <= j < len(lines) and URL_RE.findall(lines[j]):
                        urls = URL_RE.findall(lines[j])
                        break
            if urls:
                for name in names:
                    idx.setdefault(name, urls[0].rstrip(".,;"))
    return idx


def pattern_url(p):
    b = os.path.basename(p)
    m = re.match(r"^data/lists/metzdowd/(\d{4}-\w+)\.txt\.gz$", p)
    if m:
        return f"https://www.metzdowd.com/pipermail/cryptography/{m.group(1)}.txt.gz"
    m = re.match(r"^data/lists/randombit/pipermail/(\d{4}-\w+)\.txt$", p)
    if m:
        return f"https://lists.randombit.net/pipermail/cryptography/{m.group(1)}.txt (via Wayback)"
    if p.startswith("data/lists/cypherpunks-raw/"):
        return "https://github.com/cryptoanarchywiki/2000-to-2016-raw-cypherpunks-archive"
    m = re.match(r"^data/satoshi/raw/sourceforge_bitcoin_list/allura_message/(\d+)\.html$", p)
    if m:
        return f"https://sourceforge.net/p/bitcoin/mailman/message/{m.group(1)}/"
    m = re.match(r"^data/satoshi/raw/gmane/([\w.]+)/(\d+)\.eml$", p)
    if m:
        return f"gmane archive {m.group(1)} article {m.group(2)} (see data/satoshi/README.md)"
    m = re.search(r"(?:topic[_=-]?|bt-|btt-topic-)(\d{2,8})", b)
    if m and ("bitcointalk" in p or b.startswith(("bt-", "btt-"))):
        return f"https://bitcointalk.org/index.php?topic={m.group(1)}"
    if re.search(r"(^|[-_])(x|tweet|status)([-_]|$)|-x-|tweet", b):
        m = re.search(r"(?<!\d)(\d{15,20})(?!\d)", b)
        if m:
            return f"https://x.com/i/status/{m.group(1)}"
    if p.startswith("data/satoshi/raw/sni-repo/"):
        return "https://github.com/NakamotoInstitute/nakamotoinstitute.org (commit c412eb84)"
    if p.startswith("data/satoshi-hal/"):
        return "https://github.com/lugaxker/nakamoto-archive"
    if p.startswith("data/candidates/back-credlib/"):
        return "http://www.cypherspace.org/credlib/"
    if p.startswith("data/candidates/back-hashcash/"):
        return "http://www.hashcash.org/"
    return None


COLLECTIONS = [
    ("data/satoshi/raw/bitcointalk/", "https://bitcointalk.org/ (Satoshi is user 3; topics/tT_mM.html = index.php?topic=T.msgM)"),
    ("data/satoshi/raw/sourceforge_bitcoin_list/", "https://sourceforge.net/p/bitcoin/mailman/bitcoin-list/ and its gmane mirror (gmane.comp.bitcoin.user); legacy SourceForge forum pages via the Wayback Machine"),
    ("data/satoshi/raw/private_emails/trammell/", "https://www.dustintrammell.com/s/Satoshi_Nakamoto.zip"),
    ("data/satoshi/raw/private_emails/hal_finney/", "https://www.coindesk.com/markets/2020/11/26/previously-unpublished-emails-of-satoshi-nakamoto-present-a-new-puzzle/"),
    ("data/satoshi/raw/private_emails/secondary_lugaxker/", "https://github.com/lugaxker/nakamoto-archive (commit 8405b134)"),
    ("data/satoshi/raw/p2pfoundation/", "http://p2pfoundation.ning.com/ (via the Wayback Machine)"),
    ("data/satoshi/raw/p2p_research/", "p2presearch mailing-list archive (see data/satoshi/README.md)"),
    ("data/satoshi/raw/gmane/", "gmane.comp.encryption.general archive (see data/satoshi/README.md)"),
    ("data/satoshi/raw/metzdowd/", "https://www.metzdowd.com/pipermail/cryptography/"),
    ("data/satoshi/raw/whitepaper/", "https://bitcoin.org/bitcoin.pdf"),
    ("data/satoshi-hal/finneynakamotoemails.pdf", "https://online.wsj.com/public/resources/documents/finneynakamotoemails.pdf"),
    ("data/satoshi-hal/bitcoin-20081003.pdf", "https://gwern.net/doc/bitcoin/2008-10-03-nakamoto-bitcoindraft.pdf"),
    ("data/satoshi-hal/", "https://github.com/lugaxker/nakamoto-archive"),
    ("data/wayback/ucl-crypto/", "UCL Crypto Group pages via the Wayback Machine (see data/wayback/ucl-crypto/README.md)"),
    ("data/wayback/haber/", "Stuart Haber's papers on www.star-lab.com/haber/ via the Wayback Machine (see data/wayback/haber/README.md)"),
    ("data/wayback/", "Wayback Machine captures (see the README in this folder and data/wayback/SCREENSHOT-DATING.md)"),
    ("data/prior-research/nyt/", "https://www.nytimes.com/2026/04/08/business/bitcoin-satoshi-nakamoto-identity-adam-back.html"),
    ("data/prior-research/nyt-", "https://www.nytimes.com/2026/04/08/business/bitcoin-satoshi-nakamoto-identity-adam-back.html"),
    ("data/prior-research/citations/01-E-18", "https://www.imes.boj.or.jp/research/papers/english/01-E-18.pdf"),
    ("data/prior-research/", "see notes/prior-research.md (the survey lists the URL of each source)"),
    ("data/claims/B-COPA-", "https://www.opencrypto.org/2024-02-22-witnesses-satoshi-correspondence/"),
    ("data/claims/A-barely-sociable", "https://www.youtube.com/watch?v=XfcvX0P1b5g"),
    ("data/claims/bitcoin-current", "https://bitcoin.org/bitcoin.pdf"),
    ("data/claims/", "see notes/article-claims-check.md (each claim lists its source URL)"),
    ("data/candidates/sassaman-alibi/", "https://www.blackhat.com/html/bh-us-10/bh-us-10-schedule.html (via the Wayback Machine, 2010-07-25)"),
    ("data/candidates/back-activity/bitcointalk/ninjastic", "https://api.ninjastic.space/posts?author_uid=101601"),
    ("data/candidates/back-activity/bitcointalk/", "https://bitcointalk.org/index.php?action=profile;u=101601"),
    ("data/releases/later/sf-", "SourceForge download pages via the Wayback Machine (URLs in data/releases/later/sf-files-pages/_capture_urls.txt; see PROVENANCE.md)"),
    ("data/lists/randombit/", "https://www.mail-archive.com/cryptography@randombit.net/ and lists.randombit.net pipermail (via the Wayback Machine)"),
    ("data/releases/sni-code-page", "https://satoshi.nakamotoinstitute.org/code/"),
    ("data/blockchain/patoshi/ecash_README", "https://github.com/ecash-com/bitcoin"),
    ("data/releases/ninja/README", "bitcoin.ninja (the site these release binaries were downloaded from)"),
    ("data/lists/", "see the pattern in data/SOURCES.md"),
]


def collection_url(p):
    for pre, u in COLLECTIONS:
        if p.startswith(pre):
            return u
    return None


def sibling_url(p, resolved):
    stem = re.sub(r"(\.pdf)?\.(txt|html|json|xml|md)$", "", p)
    for q, u in resolved.items():
        if u and q != p and re.sub(r"(\.pdf)?\.(txt|html|json|xml|md|pdf)$", "", q) == stem:
            return u
    return None


def main(out_dir):
    os.makedirs(out_dir, exist_ok=True)
    paths = tracked()
    cls = {p: classify(p) for p in paths}
    keep = [p for p in paths if cls[p] == "keep"]
    remove = [p for p in paths if cls[p] == "remove"]
    idx = build_mention_index(keep)
    resolved = {}
    for p in remove:
        resolved[p] = (url_from_meta(p) or url_from_file(p) or idx.get(os.path.basename(p))
                       or pattern_url(p) or wayback_url(p))
    for p in remove:
        if not resolved[p]:
            resolved[p] = sibling_url(p, resolved)
    for p in remove:
        if not resolved[p]:
            resolved[p] = collection_url(p)
    rows = [{"path": p, "bytes": os.path.getsize(p), "sha256": sha256(p), "source": resolved[p] or ""} for p in remove]
    with open(os.path.join(out_dir, "remove-paths.txt"), "w") as f:
        f.write("\n".join(remove) + "\n")
    with open(os.path.join(out_dir, "sources.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["path", "bytes", "sha256", "source"])
        w.writeheader()
        w.writerows(rows)
    missing = [r["path"] for r in rows if not r["source"]]
    print(f"tracked {len(paths)}  keep {len(keep)}  remove {len(remove)}  "
          f"remove bytes {sum(r['bytes'] for r in rows)/1e6:.1f} MB  without source URL {len(missing)}")
    for m in missing[:80]:
        print("  no-url:", m)


if __name__ == "__main__":
    main(sys.argv[1])
