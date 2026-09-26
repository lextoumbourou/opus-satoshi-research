# Findings summary (working draft, 2026-09-26)

Labels: **VERIFIED** (I checked the primary source), **REPORTED** (someone else says so), **INFERENCE** (mine, with confidence). "New?" records whether I found it already published. Web search ran out mid-session (200-query cap, then Brave rate-limited), so "not found" means *not found in the prior-research survey plus targeted checks*, not a guarantee.

Detailed notes: `notes/timezone-evidence.md`, `notes/release-forensics.md`, `notes/prior-research.md`, `notes/article-claims-check.md`. Research log: `log.md`.

## 1. The main finding: Satoshi's working computers ran on UK time (2009–2010)

Every *machine-level* timestamp I could tie to Satoshi's own computers in 2009–2010 points to a clock set to **UK time (GMT in winter, BST in summer, switching on the EU dates)**. The data come from four independent mechanisms:

| # | Mechanism | Evidence | Reading | Label | New? |
|---|---|---|---|---|---|
| 1 | Thunderbird email headers | 8 GMX messages (Feb 2009 – Dec 2010) where Date-header local time minus offset equals the Thunderbird Message-ID's embedded UTC time **to the second**. 180+ more private emails to Malmi and Gavin show the same offsets. The switches fall exactly on the EU dates (+0100 on 21 and 24 Oct 2009, +0000 on 26 Oct 2009, and so on). | Thunderbird stamps the OS time zone. **UK/Irish/Portuguese rules** fit; CET, Iceland, Morocco and every US zone don't. His clock was accurate to about a minute. | VERIFIED data and mechanism; INFERENCE on meaning (high) | **Not found published.** The header offsets had been tabulated by others without identifying the mechanism. |
| 2 | Satoshi's own `diff -u` output | bitcointalk msg15116, posted 20:02:24 UTC on 3 Oct 2010 and never edited. His files show Windows-local mtimes of 20:57:54. | Dev machine ≥ UTC+0:55, so **not fixed UTC and not any American zone**. BST fits with the save 4.5 min before the post, and a +0100 Thunderbird email went out the same evening. | VERIFIED; INFERENCE (high for the exclusion, medium-high for BST) | **Not found published** |
| 3 | Release-archive folder times vs linker time | bitcoin-0.1.1 RAR: `src` dir modified 23:15:06 local on 10 Jan 2009; bitcoin.exe linked 23:16:00 UTC; the archive was emailed to Hal by ~02:55 UTC and repacked by him at 02:34 UTC on his UTC−8 machine. | Build machine ≥ UTC−3h40m (so not a US zone), and most likely **exactly GMT** (54-second match). | VERIFIED inputs; INFERENCE (bound high; GMT medium) | **The combination is not found published.** The ingredients were published separately: Chain Bulletin 2020, obxium Jan 2026, Fox Chapel May 2026. |

| 4 | Satoshi's own release ZIPs (Info-ZIP on Windows) storing local **and** UTC times for every file | 16 Windows releases, 0.2.0 (Dec 2009) to 0.3.19 (Dec 2010), recovered from Software Heritage and verified against SourceForge's 2010 SHA1+MD5 (0.3.10 also against Satoshi's own posted SHA1s). Offset = **+0:00 in Dec 2009, +1:00 on every file in Jul–Oct 2010, +0:00 in Nov–Dec 2010** (summer-dated files still +1, per-date DST). PE link times match the zip UTC times to the second. Linux tarballs show 00:01Z in summer and 01:01Z in winter. | The **build/packaging machine** followed the Western European rule (UK/Ireland/Portugal) across 16 Windows releases. That rules out CET, West Africa, Morocco and every American zone. | VERIFIED (high) | Not found published (the recovered binaries had been considered lost since 2012; Chain Bulletin asked for them in 2020) |

Supporting, weaker:
- The earliest client screenshot (taken 3 Jan 2009, published 4 Feb 2009) shows `03/01/2009 23:45`. The released 0.1.0/0.1.5 code would have printed `01/03/09` (C locale; I checked the wx 2.8.9 and Bitcoin sources). So the screenshot came from an earlier locale-aware or hard-coded day-first path, consistent with **UK regional defaults** (dd/MM/yyyy, 24-hour) and not US defaults. INFERENCE, medium. New? The dd/mm reading was noted before (deepceleron 2013); the C-locale argument appears new.
- White paper PDFs are tagged `/Lang (en-GB)` (VERIFIED; published by obxium).

**Control, and a serious caveat (added 2026-09-26 ~16:00).** Gavin Andresen (US Eastern; commits normally −0500/−0400) built the 0.3.20 Windows release on a box whose git commits were stamped **+0000** (`unknown <Administrator@.(none)>`, 14 Feb 2011). His 0.3.20.01, 0.3.20.2 and 0.3.21 Windows zips (7-Zip-style NTFS fields, no version-time normalisation, so not Satoshi's packaging) show **+0 in Feb–Mar 2011 and +1 in Apr 2011**, i.e. **London time**. So a Windows build box on London time does *not* reliably indicate the operator's location: it could be a rented UK server or a VM default, or (untestable) a machine Satoshi had set up. This **downgrades the build-machine leg** (#3, #4) as location evidence. The Thunderbird and diff legs (#1, #2) are separate machines or uses, but they would also be explained if Satoshi worked inside a remote UK-hosted Windows machine. Overall confidence in "UK time → UK residence": **medium-low**. Confidence that "Satoshi's working environment consistently ran on UK time": **high**.

**What it doesn't show.** It isn't proof of residence. A careful person can set a computer to London time. The exceptions are the two white paper PDFs (Oct 2008 −07'00', Mar 2009 −06'00'; VERIFIED; long published), which show US offsets. So at least once Satoshi's machine settings pointed away from the UK: a second machine or VM, a default, or deliberate misdirection. INFERENCE (medium): a UK-based person who used US time zones on the PDF machine is more economical than a non-UK person who kept his everyday mail and development machines on London time, with DST, for two years. That's because the latter would also have to match the British spellings, the day-first dates, the en-GB PDFs and the *Times* print headline.

## 2. What this means for the named candidates

The finding narrows the field to someone **UK-based or UK-connected**, or someone who deliberately kept London clocks. How the named candidates fare (all INFERENCE):
- **Adam Back: compatible, with one extra step.** He is British, and his Gmail was on UK time in Aug 2008. His own mail (mutt) Date headers track where he lived over 12 years: UK 2001–02, North American Eastern 2004–07, **CET +0100 Nov 2010 – Feb 2011** and CEST +0200 June 2011 (Malta; the NYT says he moved there in 2009), plus UK +0000 at Christmas 2010 (VERIFIED). On **1 Dec 2010** and **25 Jan 2011** Back's own emails are stamped +0100 while Satoshi's are +0000 (VERIFIED). So a Back-as-Satoshi theory needs two differently configured machines: his personal one following his location (possibly automatic, e.g. Mac OS X 10.6's location-based zone), and a Satoshi Windows machine set up on UK time and **never re-zoned after the move to Malta** (for 1–2 years). That's plausible for someone keeping identities separate, so it's a *constraint* on the Back theory, not a refutation. It also slightly favours a UK-connected person like Back over the other three.
- **Hal Finney.** California: his machines were on UTC−8 (tar headers, Gmail display). In the Jan 2009 emails he behaves as an outside tester receiving builds. For Finney to be the builder or mailer he'd have to keep deliberate London clocks for two years. It weighs against Finney (medium).
- **Len Sassaman** (Leuven, Belgium, CET) and **Nick Szabo** (US) are in the same position: they'd need a deliberate UK-time decoy, which is a bigger step than "never re-zoned".
- **Collective theory.** It isn't ruled out, but whoever operated the build and mail machines kept them on UK time with correct DST. Among the four, the only person that fits without a deliberate decoy is Back, and only if his Satoshi machine stayed on UK time after he moved to Malta.

## 3. Checking the NYT case against primary data

- **"Back went silent."**
  - On the metzdowd Cryptography list, Back's silence began in **Nov 2007**, nine months before Satoshi's first known email. He posted twice in Mar 2010, and the list itself was nearly dormant Nov 2010–2013. VERIFIED (`data/lists/metzdowd-adam-back-counts.txt`).
  - On the **randombit** Cryptography list, the successor list, Back posted **15 times between Mar 2010 and Feb 2011** while Satoshi was active. VERIFIED.
- **"First public comment on Bitcoin six weeks after Satoshi vanished" (June 2011).** Nobody on the randombit list mentioned Bitcoin at all until **9 June 2011**. Back's first mention was 12 June, in the week of the June 2011 price spike and Silk Road coverage, when the whole list started discussing it. In the Dec 2010 thread "current digital cash / anonymous payment projects?" nobody mentioned Bitcoin, including James A. Donald, who had reviewed Satoshi's code in 2008. So Back's silence matched the list's. VERIFIED data; INFERENCE that it weakens the NYT's timing argument (medium-high). New? I didn't find it in the critiques we collected.
- The NYT itself (VERIFIED) contains no time-zone or machine-metadata analysis and calls the "Southern California IP" a dead end.

## 4. Other results

- **Satoshi's build environment** (VERIFIED):
  - OpenSSL 0.9.8h "no-everything" build, `DATE` = Thu Aug 28 01:18:38 2008 (gmtime), linked 01:23:15 UTC, eight days after his first email to Back.
  - wxWidgets debug build compiled Nov 28 2008 08:05:59 (local).
  - Berkeley DB 4.7.25; MinGW GCC 3.4.5 plus MSVC 6.0 SP6 (per Satoshi).
  - No usernames or home paths in the binaries (negative result).
  - New? OpenSSL/wx dates not found published; the PE time is published (obxium).
- **The claim that "SVN commits show Satoshi used BST" (In Search Of Satoshi, 2018) is an artefact.** `svn log` prints UTC in the *reader's* zone (VERIFIED by running it in three zones). Ironically the conclusion (UK time) now has real support from the evidence above.
- **Hal's debug log (Jan 2009).**
  - The IRC channel operator at 68.164.57.219 (Covad DSL, Los Angeles) accepted Hal's incoming connection. On 12 Jan 2009 Satoshi told Hal: "I can't receive incoming connections from where I am … Your node receiving incoming connections was the main thing keeping the network going the first day or two." By Satoshi's own account the LA node wasn't his (or not at "where I am"). The Tor-connected node fits his description.
  - Alex Waltz (June 2026) assumes both nodes were Satoshi's. I couldn't access his full thread to see whether he addressed this. INFERENCE, medium.
- **Satoshi's release timestamps** encode the version number (01:00 = 0.1.0, and so on), a Microsoft-style release habit. Already published (Chain Bulletin 2020).
- **Activity rhythm: Back vs Satoshi** (`scripts/hour_compare.py`; VERIFIED data, INFERENCE weak). **30.1%** of Back's 156 randombit posts (2010–15) fall in 05:00–10:59 UTC, against **4.4%** of Satoshi's 919 timed items. Satoshi is essentially never active 07:00–12:00 UTC. During the overlap (Mar 2010 – Feb 2011), 4 of Back's 15 posts fall in Satoshi's dead zone (19–21 Nov 2010, 08:18–10:09 UTC). But there is **no direct conflict**: the closest pair is Back 21:19 / Satoshi 22:46 on 21 Nov 2010, and the 20 Nov sequence (Satoshi 02:12 → Back 10:03 → Satoshi 17:24) is compatible with one person sleeping in between. So the rhythms differ, but a single person who kept "Satoshi" to afternoons and nights can't be excluded. The NYT did no timing analysis; not found in prior art.
- **DST natural experiment** (did his activity shift on EU or US dates?): underpowered, 0–1 nights in the key windows. Inconclusive.

## 5. Claims in the article that need fixing

See `notes/article-claims-check.md`. None is flatly wrong; seven need nuance:
- the NYT co-author and headline;
- the Back-denial citation;
- the Reddit theory is a division of labour;
- Back was *the first* known correspondent;
- "only person *credited* by name" in the white paper;
- the bit gold date;
- Hatch overstated.

Also: the idea that the coins never moved *because* Sassaman died has a logic gap, since they didn't move while Satoshi was active either.

## 6. Added after the search cap was raised (2026-09-26, afternoon)

- **Prior-art sweep** (`notes/prior-art-search.md`): nothing found for any of the session's main findings (Thunderbird/UK-time headers, release-zip offsets, diff mtimes, the RAR+PE+Hal bound, the screenshot argument, the OpenSSL date, the NYT list-data checks, the DST analysis, the Gavin control).
- **NYT review** (`notes/nyt-review.md`): read the full article. It has no machine-metadata or timing analysis. Its "disappeared from the Cryptography list" claim is contradicted by Back's 15 randombit posts and 2 metzdowd posts during Satoshi's active period. Its "six weeks" timing coincides with everyone's first Bitcoin posts in June 2011. It relies on the 2015 vistomail email, whose headers show a genuine vistomail send but can't show who sent it.
- **Control that weakens the build-machine leg**: Gavin's Windows build box (2011) was also on London time. Build-box time zone is weak location evidence. Overall "UK residence" confidence is now medium-low; "UK-time working environment" confidence is high.
- **Behavioural DST test** (`notes/dst-behaviour.md`): Satoshi's activity follows a DST clock (robust; +12–20 log-lik over UTC). EU dates are favoured over US dates (+1.9–4.3), driven by one week in Oct 2009. Low-to-medium confidence. It addresses the operator's routine, not machine settings.
- **Packaging habits** (`notes/packaging-habits.md`): none of Back (hashcash/credlib), Dai (Crypto++), Sassaman (Mixmaster) or Finney shows Satoshi's Windows-native, version-number-timestamp release habit. Back and Sassaman packaged on Linux. Weak-moderate.
- **Sassaman at Black Hat 2010** (`notes/sassaman-blackhat-2010.md`): Satoshi was silent during the talk and active before and after. But that evening's Satoshi email (+0100) and the next day's 0.3.6 build (+1) were on London time while Sassaman was in Las Vegas (home: Belgium). Weak-moderate evidence against Sassaman as operator.
- **Filter strength** (`notes/uk-time-filter.md`): only ~7% of 2008–11 crypto-list regulars show a clean UK clock rule. A filter, not an identification.
- **Negative results**:
  - Patoshi miner ran continuously in early 2009 (no DST test possible).
  - Satoshi's difficulty table uses UTC dates (23/23).
  - Holiday test inconclusive after a local baseline.
  - SourceForge and forum profiles show no timezone (forum offset left at UTC; the 2021 "nakamoto2 / Japan" profile is a re-registration).
  - No raw GMX headers with client IP are public.
  - Satoshi never wrote "tonight", "this morning" or "weekend".

## 7. Final dig (2026-09-26, evening)

- **Ducrée (arXiv 2206.10257) read and citation-checked** (`notes/ducree-review.md`). His central "Benelux" argument is that white paper ref [2] was print-only, so Satoshi or someone close must have attended the 1999 Haasrode symposium. **That is false.**
  - The Massias paper was on UCL's public site: listed from 1999; PS download from 2002; file captured in 2003 and Aug 2007, byte-identical.
  - It was also indexed by CiteSeer (2004–2008). VERIFIED.
  - **New: bibliographic fingerprint.** White paper [2] reproduces the authors' own self-citation in their WETICE 1999 paper, as shown on CiteSeer, errors included: "X. S. Avila" (for Serret Avila) and plural "requirements". [3], [4] and [7] reproduce the reference list of [5], Haber & Stornetta's "Secure Names for Bit-Strings", on Haber's site from 2000. The Massias paper's own list doesn't match. INFERENCE (high): Satoshi built the timestamping bibliography from online sources available to anyone by 2007. Partly anticipated: Miller (Medium, 13 Apr 2026, citing Jeremy Clark) noted the plural "requirements" and missing pages, and proposed the 2005 Springer encyclopedia as the source. That is a weaker fit ("X. Serret Avila", "Twentieth", page numbers). The archival proof that the paper was online 2002–2007, the WETICE/CiteSeer string and the Haber-list match are not found published. This directly answers the April 2026 "print-only until 2020 → Sassaman" claim (Seroy/Carter on X).
  - **For the theory:** this removes Ducrée's grounds for excluding Finney and Szabo and his special KU Leuven route for Sassaman. It neither supports nor refutes the collective.
  - The Bank of Japan/IMES report (Quisquater lead) isn't the source: it shares only Haber & Stornetta 1991.
  - Ducrée errors: Feller 1957 is the 2nd edition; his PDF "CET" reading is his own viewer's zone; the P2P Foundation birthdate-based age was shown by Mar 2011 (not "2012"); Patterson's "according to its creator" tweet followed Satoshi's public 5 Dec 2010 post by 54 h; Mixmaster is C.
- **2011 time-of-day break** (`notes/2011-break.md`).
  - 4 of 11 items from 2011 fall in Satoshi's quietest 8 h window (06–14 UTC; 2.8% of 887 base events): p ≈ 2 × 10⁻⁴; window-free permutation test p ≈ 5 × 10⁻⁵.
  - Hearn's display zone, calibrated on his 2009–10 dumps, fits Zurich (UTC+1/+2) and rejects US displays.
  - Gavin's 26 Apr 2011 email is independently ≈08:29 UTC.
  - The farewell emails (20, 23, 26 Apr 2011) fall on weekday mornings in the UK Easter holiday: mundane for a UK person with daytime commitments, pre-dawn for a US one. Change of routine: medium-high. UK-favouring: low-medium. Hand-over to another writer: possible, not shown.
- **Back's "ruled out anyone in Europe" (24 Apr 2026)** (`notes/back-europe-claim.md`). It's the documentary's reasoning relayed against Sassaman.
  - Hours rule out a European with ordinary daytime hours, not a UK night owl.
  - The machine clocks (UK, not CET) cut against CET-based operators: Sassaman *and* Back himself.
  - The behavioural DST test weakly favours EU clock-change timing.
- **Extended Back rhythm test** (`notes/back-rhythm-extended.md`; subagent, rerun and reproduced by me). 1,455 Back posts: randombit 156, Bitcointalk 399, bitcoin-dev 197, cypherpunks 1996–98 703.
  - In Satoshi's quiet window (06–14 UTC; 3.0% of Satoshi's 902 items), Back has 28–49% per venue. In the UK era, 1996–98 in London time, Back is a late-evening poster (peak 21:00–01:00), but 18.5% of his posts fall at 09–13 against Satoshi's 0.3%. Watson U² p ≤ 0.0005 for every venue; weekends don't close the gap.
  - VERIFIED: Back's 1990s sendmail Message-ID times are GMT (43 Date-header matches), and his 1990s machine ran UK time with daylight saving.
  - During Nov 2008 – Apr 2011, 5 of his 15 randombit posts fall in Satoshi's quiet window; the closest pair is 87 min apart (no direct conflict).
  - Weak-to-moderate evidence against Back = Satoshi. A person could confine a pseudonym to evenings, so it can't exclude him. No published Back-vs-Satoshi timing comparison found (7 queries).
