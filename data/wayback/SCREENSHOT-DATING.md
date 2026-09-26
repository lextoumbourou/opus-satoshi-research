# Dating bitcoin.org `screen3.png` ("03/01/2009 22:18 / 23:45", 213 blocks)

Question: was screen3.png (640x300, two transactions dated `03/01/2009 22:18` and
`03/01/2009 23:45`, "3 connections", "213 blocks", address
19CncWdnU57yq4QHBNVPdScFB54JkPGu28) public before 1 March 2009? If it was,
`03/01/2009` can't be 1 March in mm/dd/yyyy order, so it must be 3 January 2009
(dd/mm/yyyy), assuming the machine clock was correct.

Researched 2026-09-26. The raw captures are in `data/wayback/raw/`. They were
fetched with `id_` (unmodified) Wayback URLs, and the response headers are saved
alongside as `*.hdr`.

## Answer

**Yes. screen3.png was public before 1 March 2009, so the date reads as
3 January 2009 (dd/mm/yyyy).** Two independent lines of evidence show this:

1. **SourceForge, 18 Feb 2009 (VERIFIED capture; content match INFERRED to hold
   in 2009).** The Bitcoin project's screenshots page
   was captured on **2009-02-18 17:17:04 UTC**. It showed a full-size
   "Main Window" screenshot `dbimage.php?id=203604` at **640x300**, plus thumbnails
   203603 (100x46, "Main Window") and 203601 (100x45, "Send Coins"). The earliest
   capture of the image bytes for id 203604 is from 2011-07-22. That file is a
   640x300 JPEG, and pixel-for-pixel it is screen3.png re-encoded as JPEG. The
   mean absolute difference is 1.7/255 per channel, and only 0.17% of pixels
   differ by more than 40, all of it JPEG ringing around text. The link to 2009
   rests on SourceForge dbimage ids pointing at fixed stored images: a replaced
   screenshot gets a new id. The Feb 2009 HTML fits this, because its
   dimensions (640x300, and thumbnails with the 640x300 and 625x286 aspect
   ratios) match screen3/screen4.
   - https://web.archive.org/web/20090218171704id_/http://sourceforge.net:80/project/screenshots.php?group_id=244765
   - https://web.archive.org/web/20110722190112id_/http://sourceforge.net/dbimage.php?id=203604

2. **The bitcoin.org server's own file timestamp: 4 Feb 2009 (VERIFIED header,
   captured 2011).** The earliest Wayback captures of
   `http://www.bitcoin.org/screen3.png` (2011-04-10 and 2011-05-04) carry the
   original Apache headers:
   - screen3.png: `Last-Modified: Wed, 04 Feb 2009 22:57:10 GMT`, ETag `"cc728-35f7-4621fb52d5d80"`
   - screen4.png: `Last-Modified: Wed, 04 Feb 2009 23:00:31 GMT`, ETag `"cc729-2b40-4621fc12861c0"`
   - something.png: `Last-Modified: Mon, 23 Nov 2009 02:35:43 GMT`, ETag `"cc72a-217-47900ae97fdc0"`

   The ETags follow Apache's inode-size-mtime format. Decoding their mtime
   fields gives exactly the Last-Modified times above. The size field 0x35f7
   (13815) matches the bytes served. The three files have consecutive inodes
   (cc728, cc729, cc72a) but mtimes nine months apart, and the 2011-05-04 capture
   shows a different inode (15857c) with the same mtime. So the files were
   copied between servers with their mtimes preserved: 4 Feb 2009 is a carried-over
   original mtime, not the date of some later copy. 4 Feb 2009 is also the
   SourceForge release date of bitcoin-0.1.5.rar (VERIFIED on the SF project page,
   "Release Date: 2009-02-04", and on the files pages in
   `data/releases/later/sf-files-pages/`). An mtime can be set by hand, so this
   line on its own is strong but not conclusive.

Both lines agree: **screen3.png existed and was very probably posted with the
0.1.5 release on about 4 Feb 2009. It was certainly on SourceForge's public
screenshots page by 18 Feb 2009**, 11 days before 1 March.

## January 31 2009 bitcoin.org used different screenshots

Raw capture: https://web.archive.org/web/20090131115053id_/http://bitcoin.org:80/
(`raw/bitcoin.org-20090131115053.html`, 5272 bytes, sha256 `525f977a…f244`,
orig-date Sat, 31 Jan 2009 11:50:53 GMT). VERIFIED:

| page capture | title | images | download |
|---|---|---|---|
| 2009-01-31 11:50:53 | "Bitcoin.org - Research Paper on Peer-to-Peer Electronic Cash" | `screen1.png` 683x343, `screen2.png` 636x327, `something.png` 120x19 | bitcoin-0.1.3.rar |
| 2009-03-03 19:59:36 | "Bitcoin.org - Open Source P2P Electronic Cash" | `screen3.png` 640x300, `screen4.png` 625x286, `something.png` 120x19 | bitcoin-0.1.5.rar |
| 2009-07-22 01:18:38 | (same as March) | screen3 / screen4 / something | bitcoin-0.1.5.rar |

The download link on both 2009 pages is
`http://sourceforge.net/project/showfiles.php?group_id=244765&package_id=298441`.
The Jan 31 page text ("…a new electronic cash system that uses a peer-to-peer
network to prevent double-spending. It's completely decentralized with no server
or trusted parties.") is almost word for word the 9 Jan 2009 v0.1 announcement,
which said "See bitcoin.org for screenshots." So the screenshots Satoshi pointed
Hal and the list to in early January were most likely screen1/screen2, not
screen3 (INFERRED).

**screen1.png and screen2.png can't be recovered from the Wayback Machine.** CDX
has no capture of either before 2011-04-10, and every capture of them is a
301/404. So I couldn't download them or read any dates they show. (archive.today
only dates from 2012. The Memento aggregator didn't resolve from here.)

Note on `data/satoshi-hal/bitcoin-org-20090303/files/`: its screen3.png,
screen4.png and something.png are **byte-identical** to the 2011 Wayback
captures (sha256 `03e47245…613c`, `08a146d6…11c7`, `c0517cb9…d4d3`). The Wayback
UI fills page images from the nearest capture, which is 2011, so that "March
2009" copy's images are really 2011 captures. They say nothing about 2009 bytes
on their own.

## Wayback CDX summary (VERIFIED)

- `bitcoin.org` prefix, 2008–2009: the only captures are the root page
  (20090131115053, 20090303195936, 20090722011820, 20090822060833,
  20090823095446), byzantine.html (20090309175840), and Dec 2009 node/smf pages.
  **There are no image captures at all in 2008–2009.**
- `bitcoin.org/screen3.png`: earliest is **20110410024734** (www., image/png,
  200). The last 200 is 20110504201020, and it has been 404 since 20110523.
  Same bytes throughout (13815 B, sha256
  `03e47245b9b1a6c0612a50fde32252a85a91468df4378b2770aa7ad75e6e613c`).
- `bitcoin.org/screen4.png`: earliest 20110410024736 (11072 B, `08a146d6…11c7`).
- `bitcoin.org/something.png`: earliest 20110410024735 (535 B, `c0517cb9…d4d3`).
- `bitcoin.org/screen1.png` and `screen2.png`: never captured with content
  (earliest 20110410, 301 → 404).
- `bitcoin.org/files/*`: no captures. The `./files/` paths in the March copy
  come from a browser "Save As", not the live site. The live site used bare
  `screen3.png`.
- SourceForge dbimage 203604 (Main Window, 640x300): earliest image capture
  20110722190112 (sha256 `c757a9e0…df6f`, the same hash the satoshi-hal README
  gives for `screenshot-main-window.jpg`). 203602 (Send Coins, 625x286):
  20120319165716 (`2e24f316…d57`). Thumbnails 203603/203601: 20100612.

## SourceForge project pages (VERIFIED)

- `sourceforge.net/projects/bitcoin/`, captured **2009-01-06 20:13:47 UTC**:
  "Last Update: Oct 31 2008". The only file was bitcoin.pdf, with no software
  release yet. The status was Pre-Alpha. The activity feed listed only
  registration, the bitcoin.pdf upload, and s_nakamoto/hal being added. It had a
  generic "Screenshots" nav link but no screenshot images or screenshot events.
  (Whether screenshots already existed on SF that day can't be settled from this
  page.)
- `project/screenshots.php?group_id=244765`, captured **2009-02-18 17:17:04 UTC**
  (SF build `release_20090210.01`): shows 203604 "Main Window" (640x300) and
  "Send Coins". This is the earliest dated public appearance of the screen3 image
  I verified. The page shows no upload dates.
- `projects/bitcoin/`, captured 2009-09-16: "Release Date: 2009-02-04". The
  screenshot gallery is "Main Window" (203604/203603) and "Send Coins"
  (203602/203601), the only two Bitcoin screenshots.
- I tried to bracket when id 203604 was created from captures of nearby dbimage
  ids, but there are too few captures (none in 2036xx; 199123 first seen
  2009-03-28), so that gave nothing.

## bitcointalk topic 382374, post #18 (deepceleron)

VERIFIED from `raw/bitcointalk-382374.0.html`: the post is msg4109944, posted
December 23, 2013, 08:52:32 PM and last edited December 24, 2013, 02:29:50 PM.
It says "Thanks to robots.txt, there's no source code to recover off sourceforge
through the Internet Archive, but here's a screenshot from Jan 3 2009 (same date
as genesis), with an unreleased blockchain at block 213 and three other
connections." The embedded image is
`<img class="userimg" src="https://ip.bitcointalk.org/?u=http%3A%2F%2Fwe.lovebitco.in%2Fimg%2Fbitcoinss-Jan-03-2009.jpg&t=690&c=sqTocvNdSkqY4w">`,
which points to **http://we.lovebitco.in/img/bitcoinss-Jan-03-2009.jpg**.

- The live host doesn't resolve. The bitcointalk image proxy now returns an
  "Invalid image" placeholder (saved as `raw/deepceleron-proxy-placeholder.png`).
  The file is not in Wayback: CDX for `we.lovebitco.in/*` has 973 rows and none
  match it.
- INFERRED: his sentence puts the screenshot next to "sourceforge through the
  Internet Archive", and it was a `.jpg` (SF re-encoded screenshots as JPEG).
  So it was very likely the SF dbimage 203604 copy of screen3. His "Jan 3 2009"
  is his own dd/mm reading of the on-screen date, not independent evidence.

## Verified vs inferred

VERIFIED:
- The Jan 31 2009 page used screen1/screen2 (683x343, 636x327) with 0.1.3. The
  Mar 3 2009 page used screen3/screen4 with 0.1.5.
- SF screenshots page, 2009-02-18 17:17:04 UTC: 640x300 "Main Window" dbimage 203604.
- dbimage 203604 as captured in 2011 is screen3.png re-encoded as JPEG.
- The bitcoin.org server reported screen3.png mtime 2009-02-04 22:57:10 GMT
  (Last-Modified and ETag agree), captured 2011. bitcoin-0.1.5.rar is dated
  2009-02-04 on SourceForge.
- deepceleron's image URL, as above. The image itself is lost.

INFERRED:
- dbimage 203604 held the same image on 2009-02-18 as it did in 2011. This
  follows from immutable dbimage ids and the matching dimensions and thumbnail
  aspect ratios.
- screen3/screen4 were made or uploaded with the 0.1.5 release on about
  4 Feb 2009. That rests on the preserved mtime, which could in principle have
  been altered by hand.
- So `03/01/2009` = 3 January 2009 in dd/mm/yyyy. The only alternative is a
  deliberately or wrongly set clock on the machine that took the screenshot.
  Nothing here tells us which time zone 22:18/23:45 is in.
- Open oddity: the image wasn't on bitcoin.org on 31 Jan, even though its
  on-screen date is 3 Jan. So Satoshi either took it on 3 Jan and only published
  it on about 4 Feb (swapping out screen1/screen2 when 0.1.5 shipped), or the
  demo client's clock or date was staged. The 213-block chain, LAN peer
  192.168.0.12 and the Alice/Bob "Order #12345" data show it was a private test
  network. Mainnet had only the genesis block until 9 Jan 2009.

## Files (data/wayback/raw/)

- `bitcoin.org-20090131115053.html` (+ `hdr-20090131115053.txt`), `bitcoin.org-20090303195936.html`, `bitcoin.org-20090722011820.html`, `byzantine-20090309175840.html`
- `screen3-20110410024734.png`, `screen3-20110504201020.png`, `screen4-20110410024736.png`, `something-20110410024735.png` (+ `.hdr` with the Last-Modified/ETag)
- `sf-screenshots-20090218171704.html`, `sf-screenshots-20100416093819.html`, `sf-projects-bitcoin-20090106201347.html`, `sf-projects-bitcoin-20090916201827.html`
- `sf-dbimage-203604-20110722190112.jpg` (Main Window = screen3), `sf-dbimage-203602-20120319165716.jpg` (Send Coins = screen4), thumbnails 203603/203601
- `bitcointalk-382374.0.html`, `deepceleron-proxy-placeholder.png`
- CDX listings: `cdx-bitcoin.org-prefix-2008-2010.txt`, `cdx-screenshots-specific.txt`, `cdx-sf-targeted.txt`, `cdx-sf-projects-bitcoin.txt`, `cdx-sf-bitcoin-sourceforge-net.txt`, `cdx-sf-dbimage-*.txt`, `cdx-we.lovebitco.in.txt`
