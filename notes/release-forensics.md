# Release-archive and build forensics (2008–09)

Status: working notes, 2026-09-26. Labels: **VERIFIED** (I checked the primary artefact myself), **REPORTED** (someone else says so), **INFERENCE** (my reasoning, with confidence). "Prior art" says whether I found it already published.

Scripts: `scripts/rar4_headers.py` (raw RAR 4 header dump, no time-zone conversion) and `scripts/pe_info.py` (PE/COFF header dump). Header dumps are in `data/releases/*.headers.json`.

## 1. The artefacts and their provenance

| File | SHA-256 | Provenance | Label |
|---|---|---|---|
| `bitcoin-nov08.rar` | f0327ebb…71abf | Satoshi's email attachment "bitcoin_src1.rar" (Nov 2008), sent to Ray Dillinger (Cryddit), Hal Finney and James A. Donald. Dillinger forwarded the original email and attachment to deepceleron in Dec 2013 (bitcointalk topic 382374, post #18). Mirrored by SNI. | VERIFIED chain as far as the forum posts go |
| `bitcoin-0.1.0.rar` | 8b17eb9a…55b56 | Hal Finney emailed it to Marc Bevand (mrb) in March 2012 (topic 68121). Its size, 2,132,686 bytes, exactly matches Satoshi's email to Hal of 10 Jan 2009: "The attached file: bitcoin-0.1.1.rar (filesize 2,132,686)". So it is almost certainly that attachment, i.e. **v0.1.1**. | VERIFIED (hashes match the 2012 post; size matches the email) |
| `bitcoin-0.1.0.tgz` | ce9da465…e756 | A repack by Hal: the tar headers say `hal/hal`, uid 500, and it was created on Linux. | VERIFIED |
| `bitcoin-0.1.3.rar` | 3d73b1a8…1756 | Mirrored by deepceleron in 2012 (topic 68121, post #14) and by SNI. | VERIFIED hash; origin chain REPORTED |

## 2. Findings

### F1. File timestamps were normalised to encode the version number (VERIFIED; already published)

Every *file* entry carries an artificial time of day that equals the version number:
- nov08: `2008-11-15 00:00:01` (0.0.1)
- 0.1.0: `2009-01-07 01:00:00`
- the 0.1.1 patch: `2009-01-10 01:01:00`
- 0.1.2: `2009-01-11 01:02:00`
- 0.1.3: `2009-01-12 01:03:00`

This mirrors an old Microsoft release-engineering habit (file time = version). **Prior art:** Georgi Stefanov, Chain Bulletin, 2020-11-19, "Satoshi Used Timestamps For Early Bitcoin Source Code Versioning" (`data/prior-research/forensics/chainbulletin-timestamps-versioning.html`). He also showed that "0.1.0.rar" is really 0.1.1. Nothing new here, except my note that the practice matches Microsoft's convention (INFERENCE, low value).

### F2. Directory entries were *not* normalised and carry genuine local timestamps (VERIFIED; noted but not exploited in prior art)

| Entry | Local time (Satoshi's clock) | Notes |
|---|---|---|
| `src\obj` | 2009-01-07 15:36:27.46875 | Packaging tree cleaned; `obj` emptied |
| `src\rc` | 2009-01-07 15:37:33.671875 | |
| `src` | 2009-01-10 23:15:06.703125 | Identical in the 0.1.1 and 0.1.3 archives |

The fractions are multiples of 1/64 s, the Windows timer tick, so these are genuine NTFS timestamps. RAR 3.x stores them as *local* time with no zone field. Chain Bulletin printed these values and said they "look untouched", but drew no time-zone conclusion from them.

### F3. PE link timestamps of the released binaries (VERIFIED; not found in prior art so far)

| Binary | COFF TimeDateStamp (UTC, by Satoshi's clock) |
|---|---|
| bitcoin.exe in the 0.1.1 archive | **2009-01-10 23:16:00** |
| bitcoin.exe in the 0.1.3 archive | **2009-01-12 05:20:24** |
| libeay32.dll (Satoshi's own OpenSSL build) | 2008-08-28 01:23:15 |
| mingwm10.dll (stock MinGW runtime) | 2007-08-03 23:08:17 (not Satoshi-specific) |

GNU ld (linker version 2.56, i.e. MinGW binutils) writes `time(0)`, which is UTC.

### F4. Satoshi's build machine was not on a US time zone in January 2009 (INFERENCE: hard bound high confidence; "exactly UTC" medium)

Anchors:
- **a.** The `src` dir event happened at 23:15:06 **local** on 10 Jan (F2).
- **b.** bitcoin.exe was linked at 23:16:00 **UTC** (F3).
- **c.** Satoshi's email attaching bitcoin-0.1.1.rar is shown in Hal's Gmail forward as "Sat, Jan 10, 2009 at 6:55 PM". The display zone is Pacific: Hal's crash report was sent at 19:13:18 UTC, and Satoshi's reply to it shows "11:52 AM", which is only possible at UTC−7h21m or further west. So 6:55 PM = 02:55 UTC on 11 Jan. Anonymousspeech's server clock ran fast in both raw headers we have (Date +26 and +34 min; MailEnable +37.5 min against Hal's server). That makes 02:55 UTC an *upper* bound on the true send time.
- **d.** Hal unpacked and repacked the archive at 02:34:07 UTC on 11 Jan by his own Linux clock (tar headers). His unpacker turned Satoshi's DOS 01:00 into 09:00Z, which independently confirms Hal's machine was on UTC−8.

Hard bound: the directory event must precede the archive being sent, so 23:15:06 local ≤ 02:55 UTC the next day. **Satoshi's displayed local time was at most 3 h 40 min behind UTC** (3 h 19 min if Hal's repack time is used instead). This rules out every North American zone (ET −5, CT −6, MT −7, PT −8, AT −4, NT −3:30) unless his PC clock was more than ~1.5 h wrong. Blocks from a node >2 h in the future would have been rejected by peers.

Pointer to exactly UTC: the directory event (23:15:06 local) and the link (23:16:00 UTC) are 54 s apart *if local = UTC*. Time zones shift whole hours, so the mm:ss closeness would be a ~1.5% coincidence otherwise. It is consistent with an edit/copy-and-build session on a machine showing UTC. The alternative, UTC−3 (e.g. Chile summer time, NE Brazil, Greenland), would put the event at ~02:15 UTC, just before the email. That is also a natural sequence, but those zones have little else going for them.

So in January 2009 the machine showed **GMT/UTC**: either Satoshi was in the GMT zone (UK, Ireland, Portugal, Iceland, W. Africa) or he had deliberately set the clock to UTC. That was a sensible opsec choice for someone who also scrubbed file times. **This contrasts with the white paper PDFs**, which carry US offsets (2008-10-03 −07'00' and 2009-03-24 −06'00'; REPORTED by Chain Bulletin 2020 and In Search of Satoshi 2018, and to re-verify). So either Satoshi used different machines/VMs with different settings, or he changed zones on purpose. Either way, **his machine time zones are not reliable location evidence**. That cuts against every "the metadata says he lived in X" argument, including the Mountain/Pacific PDF readings.

What would settle UK-time vs fixed-UTC: a Satoshi-built archive from summer (BST = UTC+1), e.g. 0.3.0-win32.zip (July 2010). A subagent is looking for surviving copies; Gavin Andresen deleted pre-0.3.24 binaries from SourceForge in March 2012 (topic 68121, post #16).

### F5. Build-environment timestamps (VERIFIED; not found in prior art so far)

- libeay32.dll is OpenSSL **0.9.8h**, built with the Mingw32 platform string. Compiled-in `DATE` = **"Thu Aug 28 01:18:38 2008"**. OpenSSL 0.9.8h's `util/mk1mf.pl` line 578 writes it with `scalar gmtime()`, so it is UTC. The link was 4 min 37 s later (01:23:15 UTC). The CFLAGS disable IDEA, AES, Camellia, SEED, RC2, RC4, RC5, MDC2, BF, CAST, DES, RSA, DH, SSL2, SSL3, TLSEXT, CMS and KRB5. That matches the "no-everything" OpenSSL recipe Satoshi later documented in build-msw.txt ("Bitcoin does not use any encryption"). So Satoshi was building his dependencies eight days after first emailing Adam Back (20 Aug 2008) and ten days after bitcoin.org was registered (18 Aug 2008).
- bitcoin.exe statically links wxWidgets (debug build) whose `__DATE__ __TIME__` reads **"Nov 28 2008 08:05:59"**. That is *local* time, with no UTC partner. It was the day after US Thanksgiving; if local = UTC, 08:05 UTC.
- Berkeley DB 4.7.25 (May 15, 2008); Boost at `/boost`. The build paths are drive-root MSYS-style (`/wxWidgets`, `/DB`, `/OpenSSL`), with **no user names or home directories** (negative result).
- Toolchain, per Satoshi to Hal on 24 Jan 2009: "My testing has been with MSVC 6.0 SP6 and GCC 3.4.5. GCC is the release build." MSVC 6.0 dates from 1998, so a long-time Windows C++ developer. He also wrote: "Normally I would keep the symbols in … increased the size of the EXE from 6.5MB to 50MB."

### F6. The claim that "SVN shows Satoshi's computer used BST" is an artefact (VERIFIED)

In Search Of Satoshi (Medium, 2018-02-14) argued that `svn log` showing `+0100` in summer and `+0000` in winter means "his computer used British Summer Time". But Subversion stores `svn:date` in UTC and `svn log` renders it in the **reader's** time zone. The same commit r15 prints `02:08:05 +0100` under TZ=Europe/London, `21:08:05 -0400` under America/New_York and `10:08:05 +0900` under Asia/Tokyo; the stored value is `2009-10-21T01:08:05.296300Z` (`data/svn/svn-log-timezone-demo.txt`). The commits carry no information about Satoshi's time zone.

### F7. Hal's debug.log: the Los Angeles node vs Satoshi's own words (VERIFIED quotes; interpretation INFERENCE)

Hal's debug.log (`data/satoshi-hal/hal-debug.log`, via lugaxker/nakamoto-archive) shows #bitcoin on freenode when Hal joined:
- Hal: `uCeSAaG6R9Qidrs`, 207.71.226.132
- `x93428606` via `gateway/tor`
- channel operator `@u4rfwoe8g3w5Tai` at `h-68-164-57-219.lsanca54.dynamic.covad.net` (Covad DSL, Los Angeles)

Hal connected *to* the LA node on port 8333. Its version message was stamped 2009-01-10 19:01:20 UTC, its clock offset was "−4 (+0 minutes)", and it saw Hal as `192.168.0.1:1531`, which suggests NAT/ICS or a VM at the LA end.

Prior art: Alex Waltz (@raw_avocado, June 2026; covered by TFTC and CryptoBriefing, July 2026) analysed this log and concluded that both other nodes were "almost certainly Satoshi". But on 12 Jan 2009 Satoshi wrote to Hal: *"Unfortunately, I can't receive incoming connections from where I am, which has made things more difficult. Your node receiving incoming connections was the main thing keeping the network going the first day or two."* The LA node **did** accept an incoming connection. So by Satoshi's own account the LA node was not his (or not at "where I am"). The Tor node fits his description. **INFERENCE (medium):** Satoshi most likely ran the Tor node, and the LA operator node was either another early user or a second Satoshi machine at a different location. Still to check: whether Waltz addressed this quote.

### F8. Clock-skew constraint (INFERENCE, low–medium confidence)

Pair (0.1.1 email "6:55 PM PST" vs Hal's repack 02:34:07Z) with (0.1.3 email "9:31 PM PST" = 05:31Z vs the 0.1.3 link at 05:20:24Z). Whatever Gmail displayed (receipt time or the fast Date header), both constraints hold only if **Satoshi's build PC clock ran ≥ ~10 min fast relative to Hal's Linux clock**. If the LA node's clock (within 4 s of Hal's Windows clock) is taken as Satoshi's, that is a mild tension. It weakly supports the LA node and the build PC being different machines, but it depends on Hal's Windows and Linux clocks agreeing.

## 3. What this means for the candidates (INFERENCE)

- **Hal Finney.** His own machine was on UTC−8 (F4d), while the build machine was ≥ UTC−3:40. In these emails Hal behaves as an outside tester: he reports crashes and receives builds and debug runtimes. A Finney-as-Satoshi or Finney-in-the-collective story needs this exchange to be theatre plus a second, differently configured machine. That is possible, but it adds assumptions. (Confidence the evidence *disfavours* Hal as the builder: medium.)
- **Adam Back** (British) and a UK Satoshi generally fit a GMT clock in January, but so does anyone who set their clock to UTC. **Len Sassaman** (Leuven, Belgium, UTC+1) is allowed by the hard bound and disfavoured only by the 54-second coincidence (weak).
- **General:** machine time-zone metadata points in different directions (PDFs: US Pacific/Mountain; build machine: UTC). The honest reading is that Satoshi's clocks can't locate him. The *activity-time* patterns (when he posted) are better location evidence than the *settings* of his clocks.
