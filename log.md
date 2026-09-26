# Research log

Times are AEST (UTC+10) on the date shown, approximate.

## 2026-09-26

- ~11:45 Started. Read the article draft (`can-opus-5-5-find-satoshi-nakamoto.md`, a symlink into private notes, so it isn't committed). Set up the repo layout (data/, scripts/, notes/).
- ~11:50 Literature check: NYT (Carreyrou, 2026-04-08) named Adam Back. Its method was hyphenation stylometry (325 nonstandard hyphenations, 620 list writers, Back matched 67), plus Back's silence on the Cryptography list 2008-11. nytimes.com is blocked for fetching; a subagent is doing the full prior-research survey (notes/prior-research.md).
- ~11:52 Launched three subagents: prior-research survey, Satoshi primary-source corpus (data/satoshi), and a claim-by-claim check of the article (notes/article-claims-check.md).
- ~11:55 Release-archive forensics (my own angle). SourceForge downloads return 403 (Cloudflare). Got the original archives from the Satoshi Nakamoto Institute CDN: bitcoin-nov08.rar, bitcoin-0.1.0.rar/.tgz, bitcoin-0.1.3.rar. MD5/SHA1 match SNI's published values and mrb's March 2012 bitcointalk post (topic 68121).
- Provenance: 0.1.0 rar+tgz were emailed by Hal Finney to mrb in March 2012 (topic 68121). nov08 = "bitcoin_src1.rar", the attachment Satoshi emailed Ray Dillinger (Cryddit) in Nov 2008, forwarded to deepceleron in Dec 2013 (topic 382374, post #18).
- Wrote scripts/rar4_headers.py (raw RAR4 header parser, no time-zone conversion). RESULT: every *file* timestamp is artificially normalised, with time of day = version number (nov08: 00:00:01 = 0.0.1; 0.1.0: 01:00; patches 01:01, 01:02, 01:03). *Directory* entries were NOT normalised and carry genuine Windows timestamps (1/64 s granularity).
- Wrote scripts/pe_info.py. bitcoin.exe in "0.1.0" rar: PE link time 2009-01-10 23:16:00 UTC. Its archive's src dir mtime is 23:15:06.70 LOCAL, 54 s earlier if local = UTC. 0.1.3 exe linked 2009-01-12 05:20:24 UTC.
- Hal's 0.1.0.tgz is a repack by Hal (uname hal/hal, uid 500) at 2009-01-11 02:34:07 UTC. His unpacker mapped DOS 01:00 to 09:00Z, which means Hal's TZ was UTC-8 (California; a natural control). Hard bound: Satoshi's src dir time (local 23:15:06 Jan 10) must precede Hal's repack, so Satoshi's machine offset >= UTC-3h19m. No US zone fits (see notes/release-forensics.md).
