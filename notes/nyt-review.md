# What the NYT investigation (Carreyrou & Freedman, 8 Apr 2026) missed, or got wrong

Source read in full: `data/prior-research/nyt/nyt-carreyrou-2026-04-08.pdf` (user-supplied PDF, 14 pp.; same text as the Wayback copy). Labels: **VERIFIED**, **REPORTED**, **INFERENCE** (with confidence).

## Summary

Carreyrou's case is textual: shared vocabulary, hyphenation errors, a filter of writing tics, and Back's 1997–99 posts describing Bitcoin-like mechanisms. There are also two behavioural claims: Back "disappeared" from the Cryptography list while Satoshi was active, and he "ignored Bitcoin entirely until June 2011". The article contains **no machine-metadata or time-zone analysis at all**. It asks Back for email metadata but never looks at the metadata already public. My work bears on the case in five places.

## 1. Satoshi's computers ran on UK time; Back's own machine was on Malta time (not in the NYT)

- **What I found** (`notes/timezone-evidence.md`; VERIFIED data):
  - Satoshi's Thunderbird mail machine (Feb 2009 – Feb 2011) stamped UK offsets (+0000 in winter, +0100 in summer, switching on EU dates), confirmed to the second against Message-ID times.
  - His Windows development machine was ≥ UTC+0:55 on 3 Oct 2010 (his own posted `diff` output), which fits BST.
  - His release-packing machine showed +0 in Dec 2009, +1 on every file Jul–Oct 2010, and +0 in Nov–Dec 2010 (16 original Windows releases).
- **Why it matters to the NYT case.**
  - It supports Carreyrou's premise that "Satoshi really was British", with machine-level evidence rather than spelling.
  - But the NYT itself reports that Back **moved to Malta in 2009**. Back's own mutt-sent emails are stamped **+0100 (CET) from Nov 2010 to Feb 2011** and +0200 in June 2011 (VERIFIED, raw randombit archives). On **1 Dec 2010** and **25 Jan 2011** Back's emails carry +0100 while Satoshi's carry +0000 (VERIFIED).
  - If Back is Satoshi, he ran a separate Satoshi machine that stayed on UK time for over a year after he moved. That's possible, and it fits a UK-born person who set the machine up before moving, but the article never considers it. INFERENCE: this is a constraint on the Back theory, not a refutation (medium).
- **Important caveat, found while checking a control.** Gavin Andresen (Massachusetts, whose commits are normally −0500/−0400) built the 0.3.20 Windows release on a machine whose git commits were stamped **+0000** ("unknown <Administrator@.(none)>", 14 Feb 2011). His 0.3.20.x and 0.3.21 Windows zips show **+0 (Feb/Mar 2011) and +1 (Apr 2011)**, i.e. London time, on a box created 11 Feb 2011 (NTFS folder creation times). So a *Windows build box* on London time doesn't prove where its operator lived: it could be a rented UK server or a VM default. That weakens the build-machine leg of the UK-time evidence. The mail-client and dev-machine legs are separate, but they would also be explained if Satoshi worked on a remote UK-hosted machine. INFERENCE: overall "UK time → UK residence" is downgraded to **medium-low**. (Alternative I can't test: Gavin inherited or used a build machine that Satoshi had set up.)

## 2. "Mr. Back … disappeared from the Cryptography list during the period Satoshi was active" (NYT, confrontation section): inaccurate

- Back's silence on the **metzdowd** list began in **Nov 2007** (last post 5 Nov 2007), nine months before Satoshi's first known email. The list stayed busy through 2008–09 (50–235 posts a month). VERIFIED (`data/lists/metzdowd-adam-back-counts.txt`).
- Back **posted twice on metzdowd on 24 Mar 2010**, during Satoshi's active period. VERIFIED.
- The metzdowd list itself went almost silent from **Nov 2010 to mid-2013**. VERIFIED.
- On the **randombit Cryptography list**, which replaced it, Back posted **15 times between Mar 2010 and Feb 2011**, while Satoshi was active: Nov 2010 (patents, short signatures), 1 Dec 2010 (digital cash), Jan–Feb 2011. VERIFIED (`data/lists/randombit/`).
- So Back didn't disappear from cryptographic discussion while Satoshi was active. He was absent from metzdowd from late 2007 and silent about *Bitcoin*. The first is not tied to Satoshi's timeline; the second is point 3.

## 3. "Ignored Bitcoin entirely until June 2011 … six weeks after Satoshi vanished": the timing has a simpler explanation

- **Nobody** on the randombit Cryptography list mentioned Bitcoin at all until **9 June 2011**. Back's first mention was 12 June. That was the week of Bitcoin's first mainstream media wave: Gawker's Silk Road story on 1 June and the price spike around 8 June 2011. VERIFIED (mail-archive search, oldest first).
- In the list's **30 Nov – 2 Dec 2010** thread "current digital cash / anonymous payment projects?", **no one** mentioned Bitcoin. That includes Back (who plugged his own credlib), **James A. Donald**, who had reviewed Satoshi's code in Nov 2008 and debated him on metzdowd, and Ian Grigg. VERIFIED (full text of 11 messages).
- INFERENCE (medium-high): Back's Bitcoin silence matched his list's, and his first comment coincided with everyone else's. The "six weeks after Satoshi vanished" framing picks one anchor from several that fit.

## 4. No timing or alibi analysis in the NYT

- Carreyrou ran no posting-hour analysis. Comparing Back's 156 randombit posts (2010–15) with Satoshi's 919 timed items, **30.1%** of Back's posts fall at 05:00–10:59 UTC against **4.4%** of Satoshi's. Satoshi is essentially never active 07:00–12:00 UTC.
- During the overlap (Mar 2010 – Feb 2011) there is **no direct conflict**: the closest pair is 1.4 h apart. One person could keep "Satoshi" to evenings, so this is weak evidence. VERIFIED data; INFERENCE weak. (`scripts/hour_compare.py`)
- Back's documented mail tool was **mutt** throughout 2004–2013 (User-Agent headers; VERIFIED). Satoshi used **Thunderbird** (VERIFIED). That's compatible with deliberate separation of identities, and not otherwise informative.

## 5. Points where the NYT's premises are weaker than stated

- **The 2015 "Satoshi" email** is used to rule out Finney and Sassaman ("both dead when Satoshi made his final appearance in August 2015").
  - Its raw headers show it really was sent through vistomail's MailEnable server (`Received: from DS04 ([190.97.163.93]) by vistomail.com with MailEnable ESMTP; Sat, 15 Aug 2015 13:51:14 -0500`). VERIFIED (`data/claims/2015-08-15-vistomail-raw.eml`).
  - It is *not* in the 2008–09 format (`CHILKAT-MID-…@server123`, +0800), because the service had changed software and zone.
  - The headers can't show *who* controlled the account in 2015. Using it as proof of life makes the Finney and Sassaman exclusions only as strong as that authenticity. INFERENCE.
- **"A leaked I.P. address that appeared to place him in Southern California … dead ends."** Hal Finney's Jan 2009 debug log shows the Los Angeles node (68.164.57.219, Covad) accepting Hal's incoming connection. But Satoshi wrote to Hal on 12 Jan 2009: "I can't receive incoming connections from where I am." By Satoshi's own account the LA node wasn't his (or not at "where I am"). So Carreyrou's "not a mistake" conclusion is probably right, for a reason he doesn't give. VERIFIED quotes; INFERENCE medium.
- **Email metadata.** Carreyrou asked Back for the Aug 2008 emails' metadata. Every other anonymousspeech message of that era we have shows the same signature: X-Mailer Chilkat, `server123`, +0800, and a Date header 3–155 min before the service's relay stamp. Genuine headers would share it. But if Back were Satoshi he'd have used the same service, so the metadata **couldn't distinguish** "Satoshi wrote to Back" from "Back wrote to himself". The one useful thing it would show is recipient-side receipt times and Back's own server path. INFERENCE.
- Back's own replies in COPA exhibit AB1 use Gmail's attribution format ("On Wed, Aug 20, 2008 at 6:30 PM"), which matches the exhibit's UK-time rendering. That's consistent with Back being on UK time in Aug 2008, before Malta. VERIFIED quotes; INFERENCE medium.

## Things the NYT got right that my data supports

- A British/UK-connected Satoshi: the machine settings, the en-GB PDF language, day-first dates and the Times print headline all point that way.
- The Finney 10-mile-race alibi, and Satoshi's use of anonymousspeech/vistomail.
- "Satoshi was a master at … leaving few, if any, digital footprints" is *not* right at the machine level. Satoshi left consistent clock-setting footprints in his email headers, archives and diffs, and the NYT didn't use them.
