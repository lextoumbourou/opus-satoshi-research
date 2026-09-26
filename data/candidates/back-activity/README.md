# Adam Back: timestamped public posts (for the posting-rhythm test)

Everything here was fetched on **2026-09-26** by `scripts/fetch_back_activity.py`. The analysis is in `scripts/back_rhythm_extended.py`, its output in `rhythm-extended.txt`, and the write-up in `notes/back-rhythm-extended.md`.

Privacy: only header fields are kept for the mailing lists. There are no message bodies, and To/Cc lines are dropped. The only addresses kept are Back's own (in From). Message-IDs in In-Reply-To are kept as they appear in the public archives. The bitcointalk files are public forum pages and API output.

## bitcointalk/ (user adam3us, uid 101601)

- `ninjastic-page-NN.json`: raw responses from `https://api.ninjastic.space/posts?author=adam3us&limit=200[&last=<post_id>]`. The API rejects `author_uid`; `author=adam3us` works, and every returned post has `author_uid` 101601. There are 399 posts dated 2013-04-17 to 2021-01-05. The profile says 404 posts, so 5 are missing from the index (probably deleted, or in boards it doesn't cover).
- `back-bitcointalk.jsonl`: one record per post with post_id, topic_id, title, board, `date_utc` and URL.
- `btt-topic-*.html`: bitcointalk.org guest-view pages for 4 posts spread across the range. All 4 displayed times equal ninjastic's `date` to the second.
- `btt-profile-101601-20260926.html`: the guest-view profile (Posts: 404; Location: Malta). Its "Local Time" (05:33:15 AM) matched `date -u` (05:33:21 UTC) at fetch time, so **guest view is UTC** (VERIFIED).

## bitcoin-dev/

- Source: the gnusha.org public-inbox mirror of bitcoin-dev (lists.linuxfoundation.org/pipermail/bitcoin-dev/ now redirects there). The query was `f:"adam back"`, downloaded as "results only" mbox.gz via `POST https://gnusha.org/pi/bitcoindev/?q=f:"adam back"&x=m`. That gives 197 messages, 2013-05-06 to 2021-04-06, including the 2013–15 bitcoin-development@sourceforge era. `f:adam.back` and `f:cypherspace.org` return the same set or a subset of it.
- `back-bitcoindev.jsonl`: message_id, subject, from, the raw `date_header`, `utc_offset`, `utc`, mailer, and the gnusha URL.
- `back-bitcoindev-headers.mbox`: header-only extract (Date, From, Subject, Message-ID, In-Reply-To, User-Agent/X-Mailer).

## cypherpunks/ (1996–1998)

- Source: the cryptoanarchy.wiki cypherpunks archive, i.e. GitHub `cryptoanarchywiki/mailing-list-archive-generator` at commit `5ee11c76b130aadf0ed74877107df5053ab0361b` (2022-02-21, HEAD when fetched), directories `_emails/1996..1998`. Each record's HTML copy is at `https://mailing-list-archive.cryptoanarchy.wiki/archive/YYYY/MM/<hash>`.
- `back-cypherpunks-1996-98.jsonl`: 747 messages whose From is Adam Back (aba@dcs.ex.ac.uk, aba@atlas.ex.ac.uk, A.Back@exeter.ac.uk…). Fields: from, subject, message_id, in_reply_to, archive_utc, archive_raw_date, message_hash, source_file and URL.
  - This archive's `Date:` headers are **not** Back's own. Most are list-server times labelled "+0800" (some wrongly); the rest are toad.com PST/PDT.
  - The analysis therefore uses the time inside Back's own sendmail Message-ID (`<YYYYMMDDhhmm.QAAnnnnn@server.test.net>` / `@server.eternity.org`), which is GMT; see the verification below. That leaves 703 unique posts. Excluded: 30 with toad.com-generated IDs, and 14 with Exeter/olib IDs in a different format whose zone was not verified.
- `venona-back-headers.jsonl`: header blocks (Subject, From name, **Date**, Sender; To/Cc dropped) for 43 of Back's posts. They come from Wayback copies of `cypherpunks.venona.com/date/YYYY/MM/msgNNNNN.html`, the MHonArc archive of the Algebra.COM CDR node, which keeps the sender's own Date header.
  - Months sampled: 1996-07/08/12, 1997-01/07/08, 1998-01/07. At most 8 per month, and only pages that Wayback holds. The live site returned HTTP 522 on 2026-09-26.
  - Result: Back's own Date header gives `+0100` in summer and `GMT` in winter, and its UTC value equals the Message-ID time to within 1 minute in all 43 posts (24 BST, 19 GMT). So the Message-ID time is UTC, and his machine was on Europe/London time.
