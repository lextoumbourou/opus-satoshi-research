# Fact-check: "Can Opus 5.5 Find Satoshi Nakamoto?" (draft)

Checked 2026-09-26. Article: `can-opus-5-5-find-satoshi-nakamoto.md` (symlink, not modified).
Primary sources saved under `data/claims/`.

Every citation key and factual claim is listed below. The **Label** says whether I read the primary source myself (VERIFIED) or am relying on someone else's account (REPORTED). Opinions and speculation in the article (e.g. "I think Sassaman had the keys") are not fact-checked, except where they rest on a factual premise.

## Summary table

| # | Claim (short) | Verdict | Label | Fix needed |
|---|---|---|---|---|
| 1 | Barely Sociable video argues Adam Back | ACCURATE | VERIFIED (video metadata) / REPORTED (argument) | Optional: title "Bitcoin - Unmasking Satoshi Nakamoto", May 2020 |
| 2 | NYT investigation "by John Carreyrou himself" concluded Back "most likely" | ACCURATE BUT NEEDS NUANCE | VERIFIED (headline, byline, date); body paywalled | Co-byline Dylan Freedman; the piece names Back outright and Carreyrou told NPR "between 99 and 100% certain"; the evidence is circumstantial |
| 3 | Back denies it [@robertsNewYorkTimes2026] | ACCURATE (weak citation) | VERIFIED | Fortune (Roberts) is an opinion piece that doesn't quote the denial; cite Back's X post of 8 Apr 2026: "i'm not satoshi" |
| 4 | Reddit comment: Szabo + Sassaman collaboration | ACCURATE BUT NEEDS NUANCE | VERIFIED (archived copy) | It's a two-person split: Szabo wrote the paper, Sassaman coded the client |
| 5 | Hashcash first proposed in 1997 [@backHashcash...2002] | ACCURATE | VERIFIED | Optional: announced 28 Mar 1997 on cypherpunks (the 2002 paper says "May 1997") |
| 6 | Back "one of the first people Satoshi emailed, in August 2008, to check the citation" [@rizzoReadAdamBacks2024] | ACCURATE BUT NEEDS NUANCE | VERIFIED | He's the *first* known (20 Aug 2008; Wei Dai followed on 22 Aug at Back's suggestion). Rizzo's piece is in **Bitcoin Magazine**, not CoinDesk |
| 7 | Back "literally the only person named in the body" of the white paper; quote | ACCURATE BUT NEEDS NUANCE | VERIFIED (Oct 2008 and 2009 PDFs) | Quote is exact. But Merkle ("Merkle Tree"), Moore ("Moore's Law") and Poisson also appear as eponyms. Say "the only person credited by name" |
| 8 | Szabo's Bit gold post [@szaboBitGold2008] | ACCURATE (link); citation date NEEDS NUANCE | VERIFIED | Post first published 29 Dec 2005; its display date was later changed to 27 Dec 2008; the idea dates from 1998 |
| 9 | White paper doesn't cite Szabo | ACCURATE | VERIFIED | None |
| 10 | 2010 Satoshi quote "an implementation of Wei Dai's b-money proposal [...] and Nick Szabo's Bitgold proposal" | ACCURATE | VERIFIED | None (bitcointalk, 20 Jul 2010, "They want to delete the Wikipedia article") |
| 11 | Finney built RPOW | ACCURATE | VERIFIED (rpow.net archive) | None |
| 12 | Finney first person besides Satoshi to run Bitcoin; received the first transaction | ACCURATE BUT NEEDS NUANCE | VERIFIED | Finney said "I think I was the first..."; it was the first person-to-person tx (block 170, 12 Jan 2009) |
| 13 | Satoshi to Malmi: Finney "helped me a lot" | ACCURATE | VERIFIED | Optional: 21 Jul 2009; "helped me a lot defending the design on the Cryptography list, and with initial testing" |
| 14 | Hatch argues Sassaman "may have written the original Bitcoin client" | ACCURATE BUT NEEDS NUANCE (overstated) | VERIFIED | Hatch says "a real possibility that Len was a direct contributor to Bitcoin"; he never claims Sassaman wrote the client |
| 15 | Satoshi's last known email April 2011 | ACCURATE | VERIFIED | Optional: 26 Apr 2011 to Gavin Andresen |
| 16 | Sassaman died July 2011 | ACCURATE | VERIFIED | Optional: 3 July 2011 |
| 17 | ~1.1M Satoshi bitcoins never spent [@lernerWellDeservedFortune2013] | ACCURATE BUT NEEDS NUANCE | VERIFIED | Lerner 2013 said ~1M; 1.1M is Lerner 2019; ~99.9% unspent, not literally all (e.g. block-9 coins went to Finney) |
| 18 | Widow denied it; he criticised Bitcoin's lack of anonymity [@morrisWhyLenSassaman2024] | ACCURATE | VERIFIED (primaries) / REPORTED (Morris is paywalled) | Cite Patterson's 2021 tweet and Sassaman's 15 Jun 2011 tweet ("no strong anonymity") |
| 19 | Malmi "founder of the first Bitcoin community forum" | ACCURATE BUT NEEDS NUANCE | VERIFIED | He set up the first forum (SourceForge, 2009) and hosted the SMF forum; Satoshi co-founded and announced it (22 Nov 2009) |
| 20 | OpenAI Navier–Stokes claim, Lean-checked, not independently verified [@kakaesAIHasSolved2026] | ACCURATE BUT NEEDS NUANCE | REPORTED | Quanta (Kakaes, 8 Sep 2026); the result is a blow-up/singularity; OpenAI's page returned 403 to me |
| 21 | Jacobian conjecture counterexample found with Claude Fable 5 [@leeHelloThereJacobian2026] | ACCURATE | REPORTED | Optional: by Levent Alpöge (Anthropic); holds for dimensions > 2 only |
| 22 | Latent Space Engineering article | ACCURATE | VERIFIED | None |

**Biggest fixes:** #2 (co-author, and the confidence level is understated), #6 (Back was *the first* known correspondent; citation venue is Bitcoin Magazine), #7 (eponyms), #8 (Bit gold date is the reverse of what the key implies), #14 (Hatch overstated), #17 (1M vs 1.1M, and "never" should be "almost never").

**Logic note on the Sassaman keys argument:** the Patoshi coins were also essentially unmoved *before* July 2011, while Satoshi was active. So "it has never moved since his passing" isn't specific evidence for Sassaman (INFERENCE, high confidence).


## Barely Sociable documentary

- **Claim as written:** "I've watched the [Barely Sociable](https://www.youtube.com/watch?v=XfcvX0P1b5g) documentary, which makes a very strong claim that it's Adam Back."
- **Primary source:** YouTube oEmbed and watch page (`data/claims/A-barely-sociable-oembed.json`, `A-barely-sociable-watch.html`).
  - Title "Bitcoin - Unmasking Satoshi Nakamoto", channel Barely Sociable (@BarelySociable).
  - Uploaded 2020-05-11T07:29:07-07:00, 2421 s (~40 min).
  - The description opens: "Bitcoin's creator satoshi Nakamoto has remained a mystery, until today."
  - I couldn't get a transcript (YouTube HTTP 429).
- **Secondary:** Decrypt, "New theory claims Adam Back is Satoshi Nakamoto", 2020-05-12, https://decrypt.co/28542/new-theory-claims-adam-back-is-satoshi-nakamoto: "The video draws comparisons between Adam Back and Satoshi… writing style, coding ability, and constructs a timeline…" (`data/claims/A-decrypt-barely-sociable-2020.txt`). Back's tweet at the time, quoted there: "I am not Satoshi despite recent video / reddit claiming so. some factors & timing may look suspicious in hindsight; coincidence & facts are untidy."
- **Verdict:** ACCURATE.
- **Label:** VERIFIED for the video's existence, title and date. REPORTED for its argument (Decrypt; I didn't watch it).
- **Suggested wording (optional):** "the Barely Sociable documentary *Bitcoin - Unmasking Satoshi Nakamoto* (May 2020)".

## NYT investigation by John Carreyrou

- **Claim as written:** "a [New York Times investigation](https://www.nytimes.com/2026/04/08/business/bitcoin-satoshi-nakamoto-identity-adam-back.html) by John Carreyrou himself concluded that Back is most likely Satoshi."
- **Primary source:** NYT oEmbed and page meta tags (`data/claims/A-nyt-carreyrou-oembed.json`, `A-nyt-carreyrou-meta.txt`).
  - Headline "My Quest to Solve Bitcoin's Great Mystery". Byline "By John Carreyrou and Dylan Freedman". Published 2026-04-08T04:00:25Z. The URL matches.
  - Summary: the summary says "a trail of clues" led to "a 55-year-old computer scientist named Adam Back"
  - The body is paywalled and I didn't read it.
- **Carreyrou's stated confidence:** NPR All Things Considered, 2026-04-13, https://www.npr.org/2026/04/13/nx-s1-5778501/after-years-of-speculation-a-reporter-claims-to-have-uncovered-the-founder-of-bitcoin (`data/claims/A-npr-carreyrou-2026-04-13.txt`): "I'm pretty certain. Might say somewhere between 99 and 100% certain." And: "And now we know it's Adam Back."
- **Secondary:** Fortune (Roberts, below) says the piece "doesn't produce any smoking guns" and that the case is circumstantial.
- **Verdict:** ACCURATE BUT NEEDS NUANCE.
  - It is co-bylined with Dylan Freedman, so "by John Carreyrou himself" omits him.
  - "Most likely" understates the piece's position: it names Back, and Carreyrou says he is 99–100% certain. The evidence is circumstantial.
- **Label:** VERIFIED for headline, byline, date and summary. Carreyrou's confidence is VERIFIED via the NPR interview transcript. The full body is not read.
- **Suggested wording:** "a New York Times investigation by John Carreyrou (with Dylan Freedman), "My Quest to Solve Bitcoin's Great Mystery" (8 April 2026), named Back as Satoshi; Carreyrou later told NPR he was 'between 99 and 100% certain', though the evidence is circumstantial."

## Back's denial [@robertsNewYorkTimes2026]

- **Claim as written:** "Back denies it [@robertsNewYorkTimes2026]."
- **Primary source:** Back's X thread, 2026-04-08 (Twitter embed API JSON, `data/claims/A-back-tweet-*.json`):
  - https://x.com/adam3us/status/2041811857732768148 (09:34:16 UTC): "i'm not satoshi, but I was early in laser focus on the positive societal implications of cryptography, online privacy and electronic cash, hence my ~1992 onwards active interest in applied research on ecash, privacy tech on cypherpunks list which led to hashcash and other ideas."
  - https://x.com/adam3us/status/2041814565747409082 (09:45:02 UTC, reply to @JohnCarreyrou @AaronvanW): "the rest is a combination of coincidence and similar phrases from people with similar experience and interests - inference satoshi needed specific skills and experience to discover bitcoin, where myself and others got "so close yet so far" in design discussions the decade before."
  - https://x.com/adam3us/status/2041816020776611935 (09:50:49 UTC): "I also don't know who satoshi is, and i think it is good for bitcoin that this is the case, as it helps bitcoin be viewed a new asset class, the mathematically scarce digital commodity."
- **Citation key:** Jeff John Roberts, "The New York Times says it found Satoshi Nakamoto, the inventor of Bitcoin. Not so fast", Fortune, 2026-04-08T17:02:43Z (updated 2026-04-29), https://fortune.com/2026/04/08/who-is-the-real-inventor-of-bitcoin-satoshi-nakamoto/ (`data/claims/A-fortune-roberts-2026-04-08.txt`).
  - It's an opinion/analysis piece arguing that Carreyrou fell for confirmation bias and that Szabo is a better suspect.
  - On the denial it says only: Back "again denied he is Satoshi on Wednesday", and suggests he has used past encounters to steer journalists away (paraphrased). It doesn't quote Back.
- **Also:** TechCrunch (Amanda Silberling, 2026-04-08), https://techcrunch.com/2026/04/08/british-cryptographer-adam-back-denies-nyt-report-that-he-is-bitcoin-creator-satoshi-nakamoto/, embeds the X post. Back also denied it to Carreyrou in person, on camera (REPORTED via NPR/Carreyrou).
- **Verdict:** ACCURATE, but the citation is weak. The Fortune piece is secondary opinion and doesn't quote the denial. Cite Back's X post (or TechCrunch) for the denial, and use Fortune for the sceptical take.
- **Label:** VERIFIED (read Back's posts via the embed API).
- **Suggested wording:** "Back denies it: "i'm not satoshi," he posted on X the day the story ran, putting the rest down to "a combination of coincidence and similar phrases from people with similar experience and interests"."

## Reddit comment: Szabo + Sassaman collaboration

- **Claim as written:** "I also have [this Reddit comment](https://www.reddit.com/r/CryptoCurrency/comments/1b12azf/comment/ksc328o) bookmarked that offers a plausible theory that it was a collaboration between Nick Szabo and Len Sassaman."
- **Primary source:** Reddit blocked scripted fetches, so I used the verbatim copy in the Arctic Shift archive API (`arctic-shift.photon-reddit.com/api/comments/ids?ids=ksc328o`; `data/claims/D-reddit-ksc328o-arcticshift.json`, parent post `D-reddit-1b12azf-post-arcticshift.json`).
  - Author u/ThatInternetGuy. Posted 2024-02-27 05:19:11 UTC, edited 07:53:43 UTC, score ~1230.
  - Parent thread (u/Ilovekittens345): "Satoshi Nakamoto was John Nash (the inventor of game theory from A Beautifull Mind), it's literally spelled out in Satoshi Nakamoto."
  - Key text:
    > "Satoshi Nakamoto is made of two persons. The Satoshi Nakamoto who submitted the Bitcoin whitepaper was **N**ick **S**zabo. Japanese name is written in reverse so it's **N**akamoto **S**atoshi. He picked this name as to get the same initials **NS** on the whitepaper while not having to reveal his full name.
    > Then who's the Satoshi Nakamoto the coder? He's not Nick Szabo. He committed suicide back in 2010/2011. He's Len Sassaman. He's not the visionary who came up with Bitcoin whitepaper but he's the vessel to code the first bitcoin client. The Bitcoin second man was Martti Malmi (alive). He got to test bitcoin client and mined thousands of Bitcoin on his laptop. Martti Malmi was the one who register Bitcoin.org and ran the forum."
- **Summary:** "Satoshi" was two people. Szabo wrote the white paper (evidence offered: the NS initials). Sassaman coded the first client. It also names Malmi as "the Bitcoin second man".
- **Errors in the comment itself:** Sassaman died in July 2011, not "2010/2011". bitcoin.org was registered on 18 Aug 2008, before Malmi was involved, and is attributed to Satoshi (REPORTED).
- **Verdict:** ACCURATE BUT NEEDS NUANCE. It's a division-of-labour theory (Szabo wrote the paper, Sassaman wrote the code), supported only by the initials.
- **Label:** VERIFIED (archived verbatim copy).
- **Suggested wording:** "...a theory that 'Satoshi' was two people: Nick Szabo wrote the white paper and Len Sassaman coded the first client."

## Hashcash "first proposed in 1997" [@backHashcashDenialService2002]

- **Claim as written:** "Adam was the creator of Hashcash, which he first proposed in 1997 [@backHashcashDenialService2002]"
- **Primary sources:**
  - Adam Back, "[ANNOUNCE] hash cash postage implementation", cypherpunks@toad.com, Fri 28 Mar 1997 (16:52:26 GMT in hashcash.org's copy; 16:57:18 UTC in the list archive). http://www.hashcash.org/papers/announce.txt and https://mailing-list-archive.cryptoanarchy.wiki/archive/1997/03/1fea96e9a08fb74d7f1fdeca362f943dcb2ca70017b092359eb8f931e11004cf (`data/claims/B-hashcash-announce.txt`, `B-cypherpunks-1997-03-28-hashcash-announce.html`):
    > "I've been talking about a partial hash collision based postage scheme on the crypto lists for the last few days. The idea of using partial hashes is that they can be made arbitrarily expensive to compute ... and yet can be verified instantly."
  - Adam Back, "Hashcash - A Denial of Service Counter-Measure", dated "1st August 2002", http://www.hashcash.org/papers/hashcash.pdf (`data/claims/B-hashcash-2002.pdf`). It says Hashcash "was originally proposed ... in May 1997" (the dated announcement is 28 March). It also acknowledges prior proof-of-work by Dwork & Naor (1992): "At the time of publication of [1] the author was not aware of the prior work by Dwork and Naor".
- **Verdict:** ACCURATE. The year is right. The cited 2002 paper supports "1997", though it says "May" while the announcement is dated March.
- **Label:** VERIFIED.
- **Suggested wording:** "Adam created Hashcash, which he announced on the cypherpunks list on 28 March 1997 and wrote up in a 2002 paper". Cite the 1997 post as well as the paper.
- **Supporting context for "clearly a foundation for Bitcoin":** Satoshi's 31 Oct 2008 cryptography-list announcement (https://www.metzdowd.com/pipermail/cryptography/2008-October/014810.html): "New coins are made from Hashcash style proof-of-work."

## Satoshi emailed Back in August 2008 to check the citation [@rizzoReadAdamBacks2024]

- **Claim as written:** "and one of the first people Satoshi emailed, in August 2008, to check the citation [@rizzoReadAdamBacks2024]"
- **Primary source:** COPA v Wright (claim IL-2021-000019), Adam Back Exhibit AB1 plus his First Witness Statement (signed 17 July 2023) and Second Witness Statement. Published via COPA, https://www.opencrypto.org/2024-02-22-witnesses-satoshi-correspondence/ (`data/claims/B-COPA-Adam-Back-Exhibit-AB1.pdf/.txt`, `B-COPA-First-Witness-Statement-Adam-Back.*`, `B-COPA-Second-Witness-Statement-Adam-Back.*`). The emails:
  1. "Sent: Wed 8/20/2008 6:30:39 PM (UTC+01:00)", from satoshi@anonymousspeech.com to adam@cypherspace.org, Subject "Citation of your Hashcash paper":
     > "I'm getting ready to release a paper that references your Hashcash paper and I wanted to make sure I have the citation right. Here's what I have: [5] A. Back, "Hashcash - a denial of service counter-measure," http://www.hashcash.org/papers/hashcash.pdf, 2002."
     It offers a pre-release draft, "Electronic Cash Without a Trusted Third Party", and says "I'm also nearly finished with a C++ implementation to release as open source." (Back's witness statement gives the time as 19:38; the date is the same.)
  2. Thu 21 Aug 2008 1:55:59 PM, Back: "Yes citation looks fine, I'll take a look at your paper. You maybe aware of the "B-money" proposal ... by Wei Dai which sounds to be somewhat related to your paper."
  3. Thu 21 Aug 2008 6:59:49 PM, Satoshi: "Thanks, I wasn't aware of the b-money page, but my ideas start from exactly that point. I'll e-mail him to confirm the year of publication so I can credit him."
  4. Thu 21 Aug 2008 7:17:17 PM, Back points to Rivest et al.'s MicroMint.
  5. Sat 10 Jan 2009, from satoshi@vistomail.com: "Thanks for the pointers you gave me to Wei Dai's b-money paper and others. I just released the open source implementation of my paper, Bitcoin v0.1."
- **Wei Dai comparison:** Satoshi to Wei Dai, "Sent: Friday, August 22, 2008 4:38 PM", Subject "Citation of your b-money page", https://gwern.net/doc/bitcoin/2008-nakamoto (`data/claims/B-gwern-2008-nakamoto-weidai.txt`): "Adam Back (hashcash.org) noticed the similarities and pointed me to your site." So Dai was emailed two days after Back, because of Back.
- **Citation key:** Pete Rizzo, "Read Adam Back's Complete Emails with Bitcoin Creator Satoshi Nakamoto", **Bitcoin Magazine** (not CoinDesk), 23 Feb 2024, https://bitcoinmagazine.com/technical/bitcoin-adam-backs-complete-emails-satoshi-nakamoto (`data/claims/B-rizzo-bitcoinmagazine-2024-adam-back-emails.*`; the emails appear there as screenshots).
- **Verdict:** ACCURATE BUT NEEDS NUANCE. "One of the first" undersells it: Back is the first person Satoshi is known to have emailed (20 Aug 2008). No earlier authenticated Satoshi email has been published (INFERENCE, high confidence).
- **Label:** VERIFIED (read Exhibit AB1 and the Wei Dai emails).
- **Suggested wording:** "and the first person Satoshi is known to have emailed: on 20 August 2008 Satoshi wrote to check the Hashcash citation, and Back replied pointing him to Wei Dai's b-money." Cite Exhibit AB1 (COPA v Wright) and/or Rizzo, Bitcoin Magazine, 2024.

## Whitepaper: "the only person named in the body"

- **Claim as written:** "he's literally the only person named in the body of the original Bitcoin white paper: "a proof-of-work system similar to Adam Back's Hashcash" [@nakamotoBitcoinPeertoPeerElectronic2008]"
- **Primary sources:**
  - Current https://bitcoin.org/bitcoin.pdf (downloaded 2026-09-26, `data/claims/bitcoin-current.pdf`, sha256 `b1674191a88ec5cdd733e4240a81803105dc412d6c6708d53ab94fc248f4f553`). 9 pages, PDF CreationDate 2009-03-24 UTC, so this is the March 2009 revision, not the original. Text in `data/claims/bitcoin-current.txt`.
  - The original 2008 PDF: `data/claims/B-whitepaper-2008-10-03-draft-gwern.pdf` (from https://gwern.net/doc/bitcoin/2008-10-03-nakamoto-bitcoindraft.pdf). 8 pages, CreationDate 2008-10-03 ~20:50 UTC, author email satoshi@vistomail.com. Its sha256 `427c63b364c6db914cf23072a09ffd53ee078397b7c6ab2d604e12865a982faa` matches the hash that a cryptography-list member posted in 2015 for their saved copy of the 2008 bitcoin.pdf (https://www.metzdowd.com/pipermail/cryptography/2015-January/024453.html). That this is exactly the 31 Oct 2008 file is REPORTED (hash match via a third party); the Internet Archive was offline, so I couldn't cross-check.
- **Exact sentence (section 4, Proof-of-Work; identical in both versions):** "To implement a distributed timestamp server on a peer-to-peer basis, we will need to use a proof-of-work system similar to Adam Back's Hashcash [6], rather than newspaper or Usenet posts."
- **Other names in the body text (not the reference list), present in both versions:**
  - "transactions are hashed in a Merkle Tree [7][2][5]" (section 7), plus "Merkle Root" / "Merkle Branch" in figures and section 8. Eponym of Ralph Merkle, who is cited as [7].
  - "Moore's Law predicting current growth of 1.2GB per year" (section 7). Eponym of Gordon Moore.
  - "the attacker's potential progress will be a Poisson distribution" (section 11). Eponym of Simeon Denis Poisson.
  - No other person (Wei Dai, Szabo, Finney, Haber, Stornetta, Feller) is named in the body. Dai, Haber etc. appear only in the references list. Szabo and Finney appear nowhere, which confirms the article's "The white paper doesn't cite him".
- **Verdict:** ACCURATE BUT NEEDS NUANCE. Back is the only person named directly, as a person credited for their work, in the body. But "literally the only person named" is loose: Merkle, Moore and Poisson appear through eponymous terms.
- **Label:** VERIFIED (read both PDFs).
- **Suggested wording:** "he's the only person the white paper credits by name in its main text (others, like Wei Dai, appear only in the references): "a proof-of-work system similar to Adam Back's Hashcash"."

## Nick Szabo's Bit gold post [@szaboBitGold2008]

- **Claim as written:** "Nick Szabo (author of the [Bit gold](https://unenumerated.blogspot.com/2005/12/bit-gold.html) proposal [@szaboBitGold2008]) was also a clear influence from the early days."
- **Primary source:** https://unenumerated.blogspot.com/2005/12/bit-gold.html, fetched 2026-09-26 (`data/claims/D-szabo-bitgold-blogspot.html`, `D-szabo-bitgold-blogger-feed.json`).
  - The page header reads "Saturday, December 27, 2008". Published metadata: 2008-12-27T16:16:00-08:00.
  - But the post was first published in December 2005:
    - The URL path is /2005/12/. Blogger fixes the path at first publication.
    - Blogger post ID 113588451301633208: the legacy ID's millisecond timestamp 1135884513016 decodes to 2005-12-29 19:28:33 UTC.
    - The first comments are dated before the displayed date: showComment=1135894560000 (2005-12-29 22:16 UTC, Kay Bell), 1135896240000 (2005-12-29 22:44 UTC, Szabo replying as author), 1135984380000 (2005-12-30), and 1216783080000 (2008-07-23).
    - Satoshi linked this same /2005/12/ URL on 20 July 2010.
  - So the "backdating" controversy runs the other way from how it's often described: the 2005 post was re-dated forward to 27 Dec 2008, after the white paper (31 Oct 2008). (Wayback evidence was unavailable because the Internet Archive was offline.)
  - Szabo, "Bitcoin, what took ye so long?", 28 May 2011 (`data/claims/D-szabo-what-took-ye-so-long-2011.html`): "the bit gold ideas, which although I came up with them in 1998 (at the same time and on the same private mailing list where Dai was coming up with b-money...) were mostly not described in public until 2005".
- **Verdict:** ACCURATE (link and authorship). The citation year NEEDS NUANCE: the key says 2008 because of the re-dated display, but the post dates from Dec 2005 and the idea from 1998.
- **Label:** VERIFIED.
- **Suggested citation:** Szabo, N., "Bit gold", *Unenumerated* blog, first posted 29 Dec 2005 (display date later changed to 27 Dec 2008); idea from 1998. Consider renaming the key `szaboBitGold2005`.
- **Related:** "The white paper doesn't cite him": VERIFIED. Szabo appears nowhere in either the Oct 2008 or the current white paper (see the whitepaper section).

## Satoshi's 2010 post: "an implementation of Wei Dai's b-money proposal ... and Nick Szabo's Bitgold proposal" [@nakamotoTheyWantDelete2010]

- **Claim as written:** "in a 2010 forum post Satoshi described Bitcoin as "an implementation of Wei Dai's b-money proposal [...] and Nick Szabo's Bitgold proposal""
- **Primary source:** bitcointalk, thread "They want to delete the Wikipedia article", post by satoshi, July 20, 2010, 18:38:28 UTC (last edited July 22, 2010, 03:02:48), https://bitcointalk.org/index.php?topic=342.msg4508#msg4508 (`data/claims/D-bitcointalk-topic342.html`; the Nakamoto Institute copy `D-sni-bitcointalk-249.html` has the same time). Full sentence:
  > "Bitcoin is an implementation of Wei Dai's b-money proposal http://weidai.com/bmoney.txt on Cypherpunks http://en.wikipedia.org/wiki/Cypherpunks in 1998 and Nick Szabo's Bitgold proposal http://unenumerated.blogspot.com/2005/12/bit-gold.html"
- **Context:** Satoshi was suggesting how the Wikipedia article could describe Bitcoin during a deletion debate.
- **Verdict:** ACCURATE. The ellipsis only drops the URLs and "on Cypherpunks ... in 1998".
- **Label:** VERIFIED.

## Hal Finney: first to run Bitcoin, first transaction

- **Claim as written:** "Hal Finney, who built RPOW (a reusable proof-of-work system), was also closely involved from the very early days: he was the first person besides Satoshi to run Bitcoin, and received the first bitcoin transaction [@finneyBitcoinMe2013]."
- **Primary sources:**
  - Hal Finney, "Bitcoin and me (Hal Finney)", bitcointalk, 19 March 2013, https://bitcointalk.org/index.php?topic=155054.0 (`data/claims/C-finney-bitcoin-and-me-topic155054.html`): "I think I was the first person besides Satoshi to run bitcoin. I mined block 70-something, and I was the recipient of the first bitcoin transaction, when Satoshi sent ten coins to me as a test."
  - Blockchain: tx `f4184fc596403b9d638783cf57adfe4c75c605f6356fbc91338530e9831e9e16`, block 170, 2009-01-12 03:30:25 UTC. It spends the block-9 coinbase (50 BTC): 10 BTC to Finney, 40 BTC change back (`data/claims/C-block170-tx-f4184fc5.json`, `C-block170-header.json`).
  - Finney's tweet "Running bitcoin", 2009-01-11 03:33:52 UTC (`data/claims/C-finney-running-bitcoin-tweet.json`).
  - RPOW: archived rpow.net (2005 capture): "Reusable Proofs of Work by Hal Finney" (`data/claims/C-rpow-net-archive.html`). Its 2004 launch date is REPORTED.
- **Verdict:** ACCURATE BUT NEEDS NUANCE. Finney himself hedged ("I think"). "First bitcoin transaction" means the first person-to-person transfer; coinbase (mining reward) transactions came before it.
- **Label:** VERIFIED.
- **Suggested wording:** "he was, in his words, probably 'the first person besides Satoshi to run bitcoin', and received the first person-to-person bitcoin transaction (10 BTC, block 170, 12 January 2009)."

## "Helped me a lot" (Satoshi to Martti Malmi)

- **Claim as written:** "Satoshi mentioned him in the third person, in an email to Martti Malmi, as someone who "helped me a lot" [@malmiSatoshiSiriusEmails2024]."
- **Primary source:** Martti Malmi, "Satoshi - Sirius emails 2009-2011", published 2024, https://mmalmi.github.io/satoshi/ (260 emails; `data/claims/C-malmi-satoshi-index.html`, `C-malmi-satoshi-emails.txt`). Email #24, https://mmalmi.github.io/satoshi/#email-24, Satoshi Nakamoto <satoshin@gmx.com> to mmalmi@cc.hut.fi, "Date: Tue, 21 Jul 2009 04:14:43 +0100", Subject "Re: Bitcoin":
  > "Hal isn't currently actively involved.  He helped me a lot defending the design on the Cryptography list, and with initial testing when it was first released.  He carried this torch years ago with his Reusable Proof Of Work (RPOW)."
- **Verdict:** ACCURATE. The citation key matches Malmi's page title.
- **Label:** VERIFIED.
- **Optional nuance:** the help was specifically "defending the design on the Cryptography list, and with initial testing". The same email also says Satoshi needed "a break from it after 18 months development". Note: some emails in that archive contain old passwords, so don't quote those parts.
- **Suggested wording (optional):** "...as someone who 'helped me a lot defending the design on the Cryptography list, and with initial testing' (21 July 2009)."

## Satoshi's last known email: April 2011

- **Claim as written:** "Satoshi's last known email was in April 2011 [@wikipediaSatoshiNakamoto]"
- **Primary sources:**
  - To Mike Hearn, 23 April 2011: "I've moved on to other things. It's in good hands with Gavin and everyone." Published by Hearn: https://plan99.net/~mike/satoshi-emails/thread5.html (`data/claims/C-hearn-satoshi-emails-thread5.html`).
  - To Gavin Andresen, 26 April 2011, subject "alert key". Published by Andresen in his 26 April 2022 blog post "Eleven years ago today…", now at https://riski.wiki/wiki/User:Gavinandresen/Blog/2022-04-26_Eleven_years_ago_today%E2%80%A6 (`data/claims/C-andresen-eleven-years-ago-today.html`):
    > "I wish you wouldn't keep talking about me as a mysterious shadowy figure, the press just turns that into a pirate currency angle. [...] I've moved on to other things and will probably be unavailable. Here's the CAlert key and broadcast code in case you need it."
  - Wikipedia "Satoshi Nakamoto" (revision of 13 Sept 2026, `data/claims/C-wikipedia-satoshi-nakamoto.wikitext`): the lead gives 26 April 2011 and cites Andresen. The body's "never heard from again" line after the Hearn email is slightly misleading, because Andresen's is the later email.
  - Later messages, none authenticated: the P2P Foundation post of 7 March 2014, "I am not Dorian Nakamoto." (account widely believed compromised; REPORTED; `data/claims/C-p2pfoundation-2014-03-07-archive.html`), and the 15 Aug 2015 bitcoin-dev "Bitcoin XT Fork" email from satoshi@vistomail.com (widely regarded as fake; REPORTED; `data/claims/C-bitcoin-dev-2015-08-15-vistomail-xt-fork.html`). The last email in Malmi's archive is 22 Feb 2011, but Malmi says that archive is incomplete for early 2011.
- **Verdict:** ACCURATE.
- **Label:** VERIFIED (read Hearn's and Andresen's publications).
- **Suggested wording (more precise):** "Satoshi's last known email was on 26 April 2011, to Gavin Andresen: 'I've moved on to other things and will probably be unavailable'." Consider citing Andresen's post directly rather than Wikipedia.

## Evan Hatch on Sassaman [@hatchLenSassamanSatoshi2021]

- **Claim as written:** "as Evan Hatch argues [@hatchLenSassamanSatoshi2021], Len Sassaman may have written the original Bitcoin client"
- **Primary source:** Evan Hatch, "Len Sassaman and Satoshi: a Cypherpunk History", Medium, 2021-02-22 03:41:37 UTC, https://evanhatch.medium.com/len-sassaman-and-satoshi-e483c85c2b10 (text from Medium's RSS feed: `data/claims/D-hatch-medium-2021.txt`, `D-hatch-medium-2021-feed.xml`). Key lines:
  - "I hesitate to speculate about Satoshi's identity..."
  - Len was "unequivocally an indirect contributor", and asks who actually wrote the code and ran the first node
  - "I think there is a real possibility that Len was a direct contributor to Bitcoin."
  - On the Byzantine-fault-tolerant protocol Sassaman was working on: the work was never released under his real name, implying it was either abandoned or released as Satoshi (paraphrased)
  - His case is circumstantial: remailer/Mixmaster work; links to Finney, Back, Chaum/COSIC and Bram Cohen; British spelling; living in Belgium; posting times; a Hashcash to-do in Mixmaster; Sassaman's death about two months after Satoshi's last message. He says nothing about keys or wallets.
- **Verdict:** ACCURATE BUT NEEDS NUANCE (slightly overstated). Hatch never says Sassaman "may have written the original Bitcoin client". He says there is "a real possibility that Len was a direct contributor", and he raises "who actually wrote the code" as an open question.
- **Label:** VERIFIED.
- **Suggested wording:** "as Evan Hatch argues, Len Sassaman may have been 'a direct contributor to Bitcoin', possibly one of the people behind the Satoshi pseudonym". The keys/wallet idea is the author's own and should read that way (it already does: "I think").

## Sassaman died July 2011 [@wikipediaLenSassaman]

- **Claim as written:** "and Sassaman died in July 2011 [@wikipediaLenSassaman]"
- **Primary sources:**
  - IEET notice, 5 July 2011: "Len ended his own life on July 3, 2011." (`data/claims/D-sassaman-ieet-20110703.html`)
  - SF Chronicle obituary via Legacy.com (published 18–24 July 2011): "laid to rest on July 9th, 2011 at De Jacht cemetery, Heverlee, Belgium… survived by his wife, Meredith L. Patterson" (`data/claims/D-sassaman-obit-legacy.html`)
  - Wikipedia (revision of 2026-09-10): "(April 9, 1980 – July 3, 2011)" (`data/claims/D-wikipedia-len-sassaman.json`)
- **Verdict:** ACCURATE. You could give the exact date: 3 July 2011, aged 31.
- **Label:** VERIFIED.
- **Note:** 26 April 2011 (last email) to 3 July 2011 is about 10 weeks.

## ~1.1 million bitcoins, never spent [@lernerWellDeservedFortune2013]

- **Claim as written:** "The roughly 1.1 million bitcoins thought to be Satoshi's have never been spent [@lernerWellDeservedFortune2013]."
- **Primary sources:**
  - Sergio Lerner, "The Well Deserved Fortune of Satoshi Nakamoto, Bitcoin creator, Visionary and Genius", bitslog.com, 17 April 2013 (`data/claims/D-lerner-well-deserved-fortune-2013.*`): "I estimate at eyesight that Satoshi fortune is around 1M Bitcoins, or 100M USD at current exchange rate". He also says it "hasn't spend any coins (as last as the eye can see)."
  - Sergio Lerner, "The Return of the Deniers and the Revenge of Patoshi", bitslog.com, 16 April 2019 (`data/claims/D-lerner-the-return-of-the-deniers-and-the-revenge-of-patoshi.html`): "Satoshi mined close to 1.1M coins (even more than the initial 1M I discovered)" and "99.9% of all Patoshi blocks are unspent".
  - On-chain: the first transaction to Finney (block 170) spent Satoshi's block-9 coinbase, so a few early coins attributed to Satoshi did move (`data/claims/D-tx-block170-f4184fc5.json`, `C-block170-tx-f4184fc5.json`).
- **Verdict:** ACCURATE BUT NEEDS NUANCE.
  - The 2013 source says ~1M. The 1.1M figure is from Lerner's 2019 post.
  - "Never been spent" should be "almost entirely unspent": about 99.9% by Lerner's count, and a handful of early coins (e.g. block 9) did move.
  - REPORTED: Bitquery (Sept 2026) says ~99.86% of Patoshi coins have never moved, that the 600 BTC moved on 17 May 2010 weren't Patoshi coins, and Arkham debunked a claimed 10,000 BTC "Satoshi" movement.
- **Label:** VERIFIED (Lerner's posts, on-chain block 170). REPORTED (Bitquery/Arkham).
- **Suggested wording:** "The roughly 1.1 million bitcoins attributed to Satoshi through the 'Patoshi' mining pattern have almost entirely (about 99.9%) never moved [Lerner 2019]." Or keep the 2013 cite and say "about 1 million".
- **Logic note (INFERENCE, high confidence):** the article says the coins have "never moved since his passing". But the Patoshi coins were essentially unmoved before July 2011 too, while Satoshi was active. So their stillness after Sassaman's death isn't specific evidence for him. It fits any Satoshi who chose not to spend.

## Sassaman's widow denied it; he criticised Bitcoin's lack of anonymity [@morrisWhyLenSassaman2024]

- **Claim as written:** "Not everyone buys the Sassaman theory, though: his widow has denied it, and he publicly criticised Bitcoin's lack of anonymity [@morrisWhyLenSassaman2024]."
- **Citation key:** David Z. Morris, "Why Len Sassaman Was Not Satoshi Nakamoto", *Dark Markets* (Substack), 2024-10-08, https://davidzmorris.substack.com/p/why-len-sassaman-was-not-satoshi (`data/claims/D-morris-why-sassaman-not-satoshi-2024.*`). The Sassaman section is paywalled, so its contents are REPORTED only.
- **Widow's denial (primary):**
  - Meredith L. Patterson (@maradydd) on X, 2021-02-23 21:24:07 UTC, status 1364325186372304904, quoting Hatch's article (`data/claims/D-tweet-1364325186372304904.json`): "It's a very well-researched and respectful article, but to the best of my knowledge, Len was not Satoshi. Worth reading for the history and the conclusions about mental health, though."
  - DL News (Ekin Genç, 2024-10-08) quotes her: "The best case against him being Satoshi is some newbie mistakes in the design of the original protocol, like being able to send to an IP address." (`data/claims/D-dlnews-patterson-2024.*`; REPORTED)
- **Sassaman's own public criticism (primary, his tweets via the Twitter syndication API):**
  - 2011-06-15 19:43:30 UTC, status 81084436518674433: "This big Bitcoin heist shows Bitcoin suffers from the worst of both worlds: no strong anonymity, yet no fraud reversal protection."
  - 2011-06-05, status 77358901774917632: "Bitcoin pretty much fails as a cypherpunk protocol."
  - 2010-12-07, status 12213554224562176: "I haven't analyzed BitCoin, but the impression of multiple digital cash experts I've talked to is that it's bunk."
  - A private exchange from 25 June 2011, published by Jon Matonis ("Len Sassaman on Bitcoin", *The Monetary Future*, 5 July 2011): "Bitcoin is less anonymous than physical cash… Bitcoin lacks unlinkability as a property…" (`data/claims/D-monetaryfuture-sassaman-on-bitcoin-2011.html`)
- **Caution:** the line "allows pseudonymity but not anonymity", sometimes attributed to Sassaman in search summaries, is CoinGeek's own sentence, not his.
- **Verdict:** ACCURATE.
- **Label:** VERIFIED (Patterson's tweet, Sassaman's tweets). REPORTED (the Morris article body, DL News quote).
- **Suggestion:** cite primaries alongside Morris, e.g. "his widow, Meredith Patterson, has said 'to the best of my knowledge, Len was not Satoshi', and weeks before his death he tweeted that Bitcoin had 'no strong anonymity'."

## Martti Malmi: "founder of the first Bitcoin community forum"

- **Claim as written:** "Martti Malmi, founder of the first Bitcoin community forum [@bitcoinwikiSirius]"
- **Primary sources:**
  - Bitcoin Wiki "Sirius" (revision 55738, `data/claims/C-bitcoinwiki-Sirius.json`): "the second Bitcoin developer after Satoshi and the founder of the [[Bitcoin Forum]]."
  - Malmi–Satoshi emails (https://mmalmi.github.io/satoshi/):
    - 9 June 2009 (#17): Malmi set up bitcoin.sourceforge.net with forums: "New users can register to the site and write to the wiki and the forums."
    - 5 Nov 2009 (#59), Satoshi: "Now that the forum on bitcoin.sourceforge.net is catching on, we really should look for somewhere that freehosts full blown forum software."
    - 14 Nov 2009 (#80), Satoshi: "I created a forum on Zetaboards".
    - 18 Nov 2009 (#93), Malmi: "I installed both phpBB3 and Simple Machines Forum".
    - 20 Nov 2009 (#99), Satoshi: "I've been configuring the SMF forum".
  - bitcointalk topic 5, Satoshi, 22 Nov 2009: "Welcome to the new Bitcoin forum!" ... "The old forum can still be reached here" (`data/claims/C-bitcointalk-topic5.html`).
- **Verdict:** ACCURATE BUT NEEDS NUANCE. Malmi set up the first forum (the SourceForge one, June 2009) and hosted the SMF forum that became Bitcointalk. Satoshi pushed for it, configured it and announced it, so it was a joint effort.
- **Label:** VERIFIED.
- **Suggested wording:** "Martti Malmi, who set up the first Bitcoin community forum and co-founded, with Satoshi, the forum that became Bitcointalk".

## LLM claims (2026 news)

### OpenAI Navier–Stokes [@kakaesAIHasSolved2026]

- **Claim as written:** "OpenAI's claimed solution to the [Navier-Stokes Millennium Prize Problem](https://openai.com/index/navier-stokes-solution/) (checked in Lean, but not yet independently verified) [@kakaesAIHasSolved2026]"
- **Sources:**
  - https://openai.com/index/navier-stokes-solution/ returns HTTP 403 to curl and WebFetch. Search results show it exists, titled "On the Navier–Stokes Millennium Prize Problem | OpenAI".
  - OpenAI on X, 2026-09-08T17:20:56Z, https://x.com/OpenAI/status/2097374640582668336 (`data/claims/A-openai-tweet-2097374640582668336.json`): "We're sharing a solution to the Navier-Stokes Millennium Prize Problem… The proof was produced by a group of agents, using an OpenAI next-generation model significantly more capable than GPT-6 Astra."
  - Citation key: Konstantin Kakaes, "AI Has Solved One of Math's $1 Million Millennium Prize Problems", Quanta Magazine, 2026-09-08, https://www.quantamagazine.org/ai-has-solved-one-of-maths-1-million-millennium-prize-problems-20260908/ (`data/claims/A-quanta-kakaes-2026-09-08.txt`). It says the result shows a singularity (blow-up) in the 3D equations and: the result "has been formally checked" in Lean, pending further scrutiny. It calls the result "not without controversy".
- **Verdict:** ACCURATE BUT NEEDS NUANCE. The link and citation match, and "checked in Lean, but not yet independently verified" fairly reflects Quanta. You could add that the result is a blow-up (singularity), i.e. it resolves the problem in the negative.
- **Label:** REPORTED. (I couldn't load OpenAI's page. I read OpenAI's X post and the Quanta article.)

### Jacobian conjecture counterexample with Claude Fable 5 [@leeHelloThereJacobian2026]

- **Claim as written:** "a [counterexample to the Jacobian conjecture](https://theconversation.com/...-283883) found with Claude Fable 5 [@leeHelloThereJacobian2026]"
- **Source:** Melissa Lee (Monash), "'hello there the jacobian conjecture is false thanx': why a tiny social media post has mathematicians rethinking AI", The Conversation, 22 July 2026 (`data/claims/A-conversation-jacobian.txt`):
  - "Levent Alpöge, a mathematician working at … Anthropic, made a very casual announcement on X that he had found a counterexample to the Jacobian conjecture… He had done this using Anthropic's large language model Claude Fable 5."
  - "the conjecture is false for every dimension larger than 2, with the original conjecture in two dimensions remaining open."
- **Verdict:** ACCURATE. You could credit Levent Alpöge and note "in dimensions above 2".
- **Label:** REPORTED.

### Latent Space Engineering article

- **Claim as written:** "the technique from this [Latent Space Engineering](https://blog.fsck.com/2026/01/30/Latent-Space-Engineering/) article about gassing up the agent to put it in a good "frame of mind""
- **Source:** "Latent Space Engineering — Massively Parallel Procrastination", 30 Jan 2026 (`data/claims/A-fsck-latent-space-engineering.txt`). The site says "I'm Jesse"; that this is Jesse Vincent is REPORTED. It advocates prompts that put the model in a "frame of mind where it's going to excel" (e.g. "You've totally got this. Take your time.").
- **Verdict:** ACCURATE.
- **Label:** VERIFIED (read the page).

## Caveats and gaps

- The Internet Archive (web.archive.org) was "Temporarily Offline" all session, so there is no Wayback cross-check for the 2008 bitcoin.pdf or for the Szabo blog's 2008 state.
- Not read in full: the NYT article body (paywalled; metadata only), OpenAI's Navier–Stokes page (HTTP 403), and the Sassaman section of Morris's Substack piece (paywalled).
- I didn't watch the Barely Sociable video; its argument is taken from Decrypt's contemporaneous summary.
- The COPA v Wright Dropbox bundle (232 MB, which includes the Hearn and Malmi witness statements) is only in the session scratchpad, not in `data/`. The Back exhibit and statements are saved as `data/claims/B-COPA-*`.
- Some emails in Malmi's archive (`data/claims/C-malmi-satoshi-emails.txt`) contain old passwords. Don't quote those parts.
