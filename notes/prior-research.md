# Prior research on Satoshi Nakamoto's identity (survey, as of 2026-09-26)

Purpose: record what has **already been published**, so nothing in this project is claimed as new when it isn't.

Labels (per README):
- **VERIFIED**: I read the primary source myself (local copy path given where saved).
- **REPORTED**: secondary coverage only; I did not read the primary.
- **INFERENCE**: my own reasoning (confidence given). Used sparingly; this file is meant to be a factual survey.

Local copies live under `data/prior-research/` (sub-folders: `timing/`, `metadata/`, `metadata/obxium/`, `llm-stylometry/`, `theories-a/`, `theories-b/`, `code-forensics/`, `nyt-freedman-thread-images/`). Items 2 to 7, 9(d) to 9(f), 10 and 11 were partly researched by helper agents; their saved files are in `theories-a/`, `theories-b/` and `code-forensics/`.

Search engine used: the WebSearch tool (US results). "Found nothing" below means nothing in those results plus follow-up fetches; it doesn't prove nothing exists.

---

## 1. New York Times: John Carreyrou (with Dylan Freedman), April 2026, naming Adam Back

### 1.1 The articles

| Piece | Date | URL | Label |
|---|---|---|---|
| "My Quest to Solve Bitcoin's Great Mystery" (SEO title "Who Is Satoshi Nakamoto? My Quest to Unmask Bitcoin's Creator"), by John Carreyrou, "With Dylan Freedman". About 11,200 words. | firstPublished 2026-04-08T04:00:25Z; lastModified 2026-04-13T00:56:32Z | https://www.nytimes.com/2026/04/08/business/bitcoin-satoshi-nakamoto-identity-adam-back.html | **VERIFIED**: full text pulled from the article JSON in the Wayback snapshot 20260415220650. Saved: `data/prior-research/nyt-carreyrou-2026-04-08.txt` (body), `…interactives.txt` (the embedded quote comparisons and the "562 → 1" scroller), `…wayback.html` (raw) |
| "4 Takeaways From Our Search for Bitcoin's Creator", by Carreyrou and Freedman | 2026-04-08 | https://www.nytimes.com/2026/04/08/business/takeaways-satoshi-nakamoto-bitcoin-adam-back.html | **VERIFIED** (Wayback 20260531044241). `data/prior-research/nyt-takeaways-2026-04-08.txt` |
| The Daily, "Unmasking the Creator of Bitcoin" (podcast) | 2026-04-09 | https://podcasts.apple.com/us/podcast/unmasking-the-creator-of-bitcoin/id1200361736?i=1000760438153 ; transcript: https://podcasts.happyscribe.com/the-daily/unmasking-the-creator-of-bitcoin | **REPORTED** (read via a fetch-and-summarise tool, not saved verbatim). Carreyrou: "Somewhere between 99.5% and 100%" (≈00:01:20) |
| Dylan Freedman's X thread, "three analyses we performed" | 2026-04-08 10:42 UTC | https://x.com/dylfreed/status/2041828936582119762 | **VERIFIED** (fxtwitter API). `freedman-x-thread-2041828936582119762.json`; images in `nyt-freedman-thread-images/` (they're article excerpts, not data) |

**Dylan Freedman** is the NYT's "A.I. Projects Editor" (his LinkedIn title; his X bio reads "A.I. @nytimes. Previously @washingtonpost, @documentcloud, @StanfordJourn, @GoogleAI, @Harvard"). The article calls him "a journalist on The New York Times's artificial-intelligence team who had experience with computational text analysis". **Published data or code? No.** The article, the takeaways piece and Freedman's thread don't link to any dataset, code or list of the 325 errors. GitHub searches ("satoshi hyphenation", "carreyrou satoshi", and the repos of user `dylfreed`) found nothing from the NYT. (VERIFIED negative, as of 2026-09-26.)

### 1.2 Method, in the article's own words (VERIFIED, `nyt-carreyrou-2026-04-08.txt`)

**Starting hunches.**
- He read the Satoshi corpus, "especially the emails released by Mr. Malmi" (the Martti Malmi emails released during COPA v Wright), and listed "more than a hundred words and phrases", e.g. "dang"; "backup," used as a verb in one word; "human friendly"; "on principle"; "burning the money"; "abandonware"; "hand tuned"; "partial pre-image"; "a menace to the network".
- He then ran X advanced search on "the dozen or so people most often suspected": "one person was a match for nearly all of my words and phrases: Mr. Back." He calls this step "wasn't meant to be scientific".
- British clues: he says he "never bought" the theory that Satoshi faked Britishisms, citing the genesis-block Times headline ("The headline in question appeared in The Times of London's British print edition").

**Corpus and mailing lists.** "We decided to collect archives of all three lists" (Cypherpunks, Cryptography, and the Hashcash list) "and merge them into one huge database". The numbers:
- "Between 1992 and Oct. 30, 2008 … more than 34,000 users had posted to the three lists."
- Removing anyone with fewer than 10 posts left **1,615**.
- Excluding users who had never discussed digital money left **620** candidates, with **134,308** posts between them (paraphrased).
- The article doesn't say how "discussed digital money" was defined, or how posters were deduplicated across addresses.

**Analysis 1: synonym-less words.** "identify all the words in the Satoshi corpus that didn't have synonyms, and measure which of our 620 suspects used the most of those words." Result: Back topped the list with 521 synonym-less words shared with Satoshi; a few others were close but had posted far more (paraphrased) No normalisation method is given.

**Analysis 2: hyphenation.** the NYT says it used its own stylebook's hyphenation rules with an AI model to list 325 distinct hyphenation errors in Satoshi's writing; Back shared 67 of them, and the next-highest candidate 38 (paraphrased)
- The model isn't named. Freedman's thread says only that A.I. was used "to assess 325 distinct errors … (beyond old-school grammar checkers' capabilities)".
- The runner-up (38) isn't named, and no per-author normalisation for post volume is described.
- Examples given in the text: "double-spending" hyphenated as a compound noun; compound adjectives left unhyphenated ("hand tuned," "full blown," "would be," "file sharing," "mint based model"); alternation between "e-mail"/"email", "built-in"/"built in", "off-line"/"offline", "pre-compiled"/"precompiled", "to-do list"/"to do list".

**Analysis 3: sequential "writing tics" filter** (from the embedded scroller, `…interactives.txt`):
1. Start from 620. Screening for two spaces between sentences "eliminated 58 people and left us with 562 suspects". The scroller lists "Notable people of interest" in the 562: Len Sassaman, Ian Grigg, Hal Finney, James Donald, Adam Back, Timothy May, Ben Laurie, Wei Dai, Nick Szabo.
2. British spellings: 434 left.
3. its/it's confusion: 114.
4. Sentences ending in "also": 56.
5. Eliminating those who wrote "bug fix" as two words and "halfway"/"downside" as one: 20.
6. Eliminating those who correctly hyphenated "noun-based"/"file-sharing" but not "double spending": 8.
7. Alternated "e-mail"/"email", "e-cash"/"electronic cash", "cheque"/"check", and the British and American forms of "optimize": "The answer was just one: Mr. Back."

The order of the filters and how they were chosen came from Carreyrou's reading of Satoshi and Back. The article says so itself: "we devised two additional approaches grounded in my reporting."

**Other linguistic markers claimed.**
- "proof-of-work" hyphenated as a noun: "only eight people had hyphenated it on the Cypherpunks or Cryptography lists". Of those eight, only Back was also among the four people who ever mentioned "WebMoney" on the lists.
- "partial pre-image": before Satoshi, only Finney (who wrote "preimage") and Back (who wrote "pre-image").
- "burning" an e-coin: only Back, April 1999.
- Five instances each of its/it's confusion and sentence-final "also" in Satoshi.
- "bloody": Back denied ever using it on X in Oct 2023 ("try google and see for yourself not a word i use"), but Carreyrou found a 1998 Cypherpunks post: "most of the bandwidth through my trusty 28.8k modem is bloody banners these days!"
- Robert Leonard (forensic linguist, Hofstra) called such quirks "markers of sociolinguistic variation".
- Double spacing "suggests Satoshi is older than 50".

**Conventional stylometry was inconclusive (the NYT says so itself).** Florian Cafiero (École nationale des chartes), who "had tried and failed to identify Satoshi for Mr. Wallace's book", re-ran function-word stylometry. He used Back's Hashcash paper and PhD thesis plus academic papers by 11 other suspects (incl. Finney, Szabo, Sassaman and Todd) against the white paper. Result: Back was closest, "but he said it wasn't a snug fit and that Mr. Finney was a very close second … he considered the overall result inconclusive". With a different distance measure, "Other candidates pulled ahead of Mr. Back." Carreyrou: "stylometry had failed."

**Timeline and behaviour claims.**
- Back "ignore[d] Bitcoin entirely until June 2011", six weeks after Satoshi's last message (Satoshi's last known message is dated 2011-04-26 in the article).
- In the Daily (REPORTED): "Adam Back disappeared from the cryptography mailing list before Satoshi posted his whitepaper there. And then he stayed away while Satoshi was active … He reappeared on the list before Satoshi disappeared, he never addressed Bitcoin."
- Back told "Let's Talk Bitcoin" (Dec 2013) that he had "participated" in the 2008 list discussion; Carreyrou "found no evidence of it".
- Back joined Bitcointalk on 2013-04-17, the day Sergio Lerner's blog revealed Satoshi's fortune.
- Similarities between the 2015 "Satoshi" bitcoin-dev email and Back's block-size posts ("dangerous", "very disappointing").

**Back's 1990s posts describing Bitcoin-like mechanisms.**
- 1997-04-30: e-cash "entirely disconnected" from banking, with privacy, distribution, "built-in scarcity" and no trust; two days later, "a publicly verifiable protocol".
- Aug 1997: "a distributed banking system … k of n of those nodes have to collude"; nodes that "come and go".
- 1998-12-06: the b-money + hashcash combination, with minting to "require more computational effort over time".
- April 1999: hash-tree timestamps published in NYT classified ads, and the claim that energy waste is fine "As long as the wastage is lower than the costs of fiat money".
- Back posting on "napster vs gnutella -- why distributed systems win" (2000-05-10), alongside Satoshi's 2008-11-06 Napster/Gnutella comment.

**Aug 2008 emails / "emails to himself" theory.**
- "Mr. Back could just as well have sent those emails to himself as a cover story."
- Argument: Back's Hashcash paper discusses b-money, so a Satoshi who read it would have known b-money. Back conceded that point in the El Salvador interview.
- Carreyrou asked Back for the emails' **metadata** ("The copies … made public during Mr. Wright's London trial hadn't included this information"). Back never replied to that request.

**Location, travel, time zones, code style.** The NYT article does **not** analyse Satoshi's posting times, time zones, travel alibis or code style. VERIFIED by keyword search of the full text: no "time zone", "a.m./p.m.", or posting-hour analysis. Related remarks it does make:
- Conventional wisdom's "leaked I.P. address that appeared to place him in Southern California" and the email hack: "not only were they dead ends, they probably weren't mistakes in the first place".
- Back's 1999 move to Montreal (Zero-Knowledge Systems / Freedom Network) and his 2009 move to Malta ("cost of living, weather and, yes, taxes").
- Code: only that Back's "thesis project focused on C++ — the same programming language Satoshi used".

**Confrontation (El Salvador, late Jan 2026).**
- Back's quotes: "Ultimately, it doesn't prove anything. And I will reassure you, it's really not me."; "It's not me, but I take what you're saying that this is what the A.I. said with the data. But it's still not me."; "Clearly I'm not Satoshi, that's my position … And it's true as well, for what it's worth."
- The alleged slip: "I did a lot of talking though for somebody, I mean … I'm not saying I'm good with words but I sure did a lot of yakking on these lists actually."
- Back's email explanation: "I was just responding conversationally to a general observation…"

### 1.3 Back's denials

- **X, 2026-04-08 09:34:16 UTC** (VERIFIED, `back-x-denial-2041811857732768148.json`), https://x.com/adam3us/status/2041811857732768148 : "i'm not satoshi, but I was early in laser focus on the positive societal implications of cryptography, online privacy and electronic cash, hence my ~1992 onwards active interest in applied research on ecash, privacy tech on cypherpunks list which led to hashcash and other ideas."
- Follow-up posts (REPORTED by CoinDesk, Helene Braun, 2026-04-08, https://www.coindesk.com/markets/2026/04/08/adam-back-denies-he-s-satoshi-nakamoto-after-nyt-report-claims-he-s-bitcoin-s-creator ; Decrypt https://decrypt.co/363649/): "The rest is a combination of coincidence and similar phrases from people with similar experience and interests". Back also called the "yakking" remark a case of confirmation bias.
- **Bloomberg podcast, 2026-04-10** (REPORTED via WuBlockchain X, 2026-04-13, `wublockchain-x-2043768683710034304.json`; CoinCentral 2026-04-13). Three technical arguments: "he would have used privacy technology from Sander and Ta-Shma's paper; second, early Bitcoin code contains cryptographic formatting mistakes he would never make; third, IRC logs still retain records of him asking other developers to explain Bitcoin's details."
- Yahoo Finance (David Hollerith, 2026-04-10), Back quoted: "You are inherently selecting people who are interested in similar things … So of course, they're going to sound similar." (REPORTED)
- Earlier denials: 2020 (after Barely Sociable), "I am not Satoshi despite recent video / reddit claiming so. some factors & timing may look suspicious in hindsight; coincidence & facts are untidy" (X, 2020-05-11 22:52 UTC, https://x.com/adam3us/status/1259979639092588551; VERIFIED by helper, `theories-a/back-x-2020-05-11-*.json`). In the HBO film (2024): "I thought you might think I'm Satoshi. And I don't want that to be on the record, really."

### 1.4 Critiques and rebuttals

| Critic | Date | Point | URL | Label |
|---|---|---|---|---|
| Jeff John Roberts, Fortune, "The New York Times says it found Satoshi Nakamoto… Not so fast" | 2026-04-08 | Confirmation bias. Cypherpunk traits are shared by "nearly everyone else in the early Bitcoin days". The "writing to himself" explanation is a stretch. Prefers Szabo. Back plays journalists ("the same behavior during the HBO documentary"). | https://fortune.com/2026/04/08/who-is-the-real-inventor-of-bitcoin-satoshi-nakamoto/ | VERIFIED (`fortune-not-so-fast-2026-04-08.txt`) |
| Robert Graham (C/C++ programmer), X | 2026-04-09 00:39 UTC | argues that Back's and Satoshi's published code look nothing alike (academic Unix style versus professional Windows style), with too little time between 2005 and 2009 for Back to have changed (paraphrased) | https://x.com/robertgraham/status/2042039637984596459 | VERIFIED (`graham-x-2042039637984596459.json`) |
| Unchained | 2026-04-09 | Round-up: Graham; Jameson Lopp (Satoshi "can't be caught with stylometric analysis"); Alex Thorn ("garbage"); Michael Saylor ("Until someone signs with Satoshi's keys, every theory is just narrative") | https://unchainedcrypto.com/nyt-names-adam-back-as-satoshi-nakamoto-he-denies-it-and-the-crypto-community-agrees-with-him-unchained/ | REPORTED (summarised by the fetch tool) |
| Joe Weisenthal (Bloomberg), X | 2026-04-08 | "The stylometry is interesting, but on content, ofc all the cypherpunks had similar thoughts on politics and privacy and the architecture of the internet." | https://x.com/TheStalwart/status/2041855409128890780 | REPORTED (quoted in search results / CoinDesk) |
| Alexander Muse, newsletter, "The New York Times Claims It Found Satoshi. It Didn't." | 2026-04-08 | Methodological: the filters were "reverse-engineered from a conclusion" (chosen and ordered after seeing Back's traits); base-rate neglect for prolific posters; the emails-as-decoys argument is unfalsifiable | https://newsletter.amuseonx.com/p/the-new-york-times-claims-it-found | REPORTED (fetch-tool summary) |
| Francis Tapon, Substack/podcast, "NYT is WRONG!" | 2026-04-16 | Relies on Benjamin Wallace's book: Amir Taaki says Back's code style ≠ Satoshi's (Back: C, Unix, conventional; Satoshi: erratic, C++, Windows); Jon Callas: "The primary argument against Adam Back is he couldn't keep his mouth shut." | https://ftapon.substack.com/p/why-adam-back-is-probably-not-satoshi | VERIFIED (`ftapon-substack-back-not-satoshi.txt`) |
| Brave New Coin, "…But the Evidence Falls Short" | 2026-04 | Includes the point that 67/325 means ~80% of Satoshi's hyphenation errors did not match Back | https://bravenewcoin.com/insights/new-york-times-names-adam-back-as-bitcoins-creator-but-the-evidence-falls-short | REPORTED (search snippet only; page is JS-rendered) |
| Bruce Schneier, blog | 2026-04-20 | "The article is convincing, but it's written to be convincing." No opinion. | https://www.schneier.com/blog/archives/2026/04/is-satoshi-nakamoto-really-adam-back.html | VERIFIED (`schneier-2026-04-is-satoshi-really-adam-back.txt`) |
| Fox Chapel Research (Substack) | 2026-05-21 | Calls the NYT article "what I believe to be an incorrect article". See 9(a)/9(b) for their forensic work. | https://foxchapelresearch.substack.com/p/how-you-probably-will-find-satoshi | VERIFIED |
| MatoTeziTanka, GitHub "satoshi-stylometry" | 2026-05-27 | Independent Burrows' Delta analysis. On the white paper, Back is closest (Δ 0.97). On forum posts and emails, Finney is closest (Δ ≈0.90). It also has a `forensics/nyt-april-2026-adam-back.md` discussing the NYT result. See §11. | https://github.com/MatoTeziTanka/satoshi-stylometry | VERIFIED (README) |

**Statisticians or linguists critiquing the hyphenation method specifically.** I searched for "linguist statistician critique NYT Carreyrou hyphenation", "Texas sharpshooter / forking paths Carreyrou", "Juola / Grieve / Cafiero comments", and "replicate NYT hyphenation analysis". I found **no** formal statistical or academic-linguistics critique or replication of the 325/67 analysis. Critiques are from commentators and programmers (above). The only credentialed linguists quoted are the NYT's own: Cafiero ("inconclusive") and Leonard (supportive of the method class). Hofstra published a news item on Leonard's role (2026-04-10, https://news.hofstra.edu/2026/04/10/unraveling-the-mystery-of-bitcoins-creator/ ; not read).

**Follow-ups May–Sept 2026.**
- No follow-up NYT article by Carreyrou found (searches: "Carreyrou Satoshi follow-up May/June/July/August 2026", "Carreyrou responds critics").
- What I did find:
  - "Finding Satoshi" documentary (released 2026-04-22; Finney + Sassaman), with Back calling its logic "self-contradictory" (CoinMarketCap Academy). See §4.
  - Fox Chapel Research (2026-05-21, §9).
  - MatoTeziTanka stylometry repo (2026-05-27).
  - jnathan9 "Satlock" classifier (2026-04-10, §11).
  - GNcrypto recap (2026-06-08).
  - AdvisorAnalyst "ICYMI" repost (2026-07-30).
  - Coverage linking the NYT story to Back's treasury company BSTR's SPAC deal (BeInCrypto, "Did Adam Back Use NYT Satoshi Story as Free BSTR Publicity?").

---

## 2. Barely Sociable (YouTube), 2020: Adam Back

(Helper agent; files in `theories-a/`. The video metadata and transcripts were obtained by the helper: Parts 1–2 from YouTube auto-captions, Part 3 from a local whisper.cpp transcription, so names may be misheard.)

| # | Title | URL | Published | Length |
|---|---|---|---|---|
| 1 | "The Most Elusive Identity On The Internet - Pt. 1 (Ft. Nexpo)" | https://www.youtube.com/watch?v=_Kav2K1DVWo | 2020-01-18 | 30:02 |
| 2 | "The Most Elusive Identity On The Internet - Pt. 2" | https://www.youtube.com/watch?v=fMWnaR5uJxQ | 2020-02-07 | 25:55 |
| 3 | "Bitcoin - Unmasking Satoshi Nakamoto" | https://www.youtube.com/watch?v=XfcvX0P1b5g | 2020-05-11 | 40:21 (~1.59M views) |

**Key arguments (helper: VERIFIED from transcripts).**
- **Parts 1–2** give the general profile: British spelling, "bloody difficult", the Times headline, two spaces after full stops (age estimate 55–64), and that the 2014 "I am not Dorian Nakamoto" post was genuine.
- **Part 3** names Back:
  - Only two of the accused are British, and one uses double spaces.
  - About 25 minutes on the 2015 block-size war and the 15 Aug 2015 vistomail "Satoshi" email opposing big blocks.
  - b-money + hashcash, and Back's 1998 cypherpunks post linking them ("hash cash would be a good candidate function for Wei's decentralized minting idea").
  - Back's side of the Satoshi–Back 2008 correspondence had not been produced at the time (2020). Back later produced the 5-email exchange (20 Aug 2008 → 10 Jan 2009) in COPA v Wright in Feb 2024; Pete Rizzo tweeted screenshots, and coverage includes Protos and Stacker News item 435610 (REPORTED).
  - Back's patent/paper/mailing-list gap about 2005/2007 to 2010; Malta 2009/2010; Wikipedia edits.
  - He joined Bitcointalk on 2013-04-17, the day of Lerner's "Well Deserved Fortune" post, and asked about an obscure ExtraNonce bug fix.
  - His Bitslog comment "…you might want to stop in Nakamoto's interests…". I VERIFIED this: it is in the comments of Lerner's **2013-04-24** follow-up "A more accurate figure", not the 04-17 post (`code-forensics/bitslog-2013-04-24-more-accurate-figure.txt`). The NYT's account matches.
  - The pastebin in the description (https://pastebin.com/kFLvgbsD, "Convo Gavin") is a 2015 #bitcoin-wizards log of adam3us vs gavinandresen.
- No later Barely Sociable update on Satoshi was found. NYT 2026 credits "a 2020 video by an anonymous YouTuber" and cites its b-money point (VERIFIED, NYT).
- **Does Barely Sociable do timing analysis?** No; nothing in the transcripts compares posting hours. (Helper: no such segment.)

**Back's response (2020).**
- Tweets 2020-05-11 (VERIFIED by helper):
  - "I am not Satoshi despite recent video / reddit claiming so. some factors & timing may look suspicious in hindsight; coincidence & facts are untidy."
  - "…I moved to Malta, an EU tax haven - in 2009. pure coincidence … I was born in London. i do use double-space and native spelling British. can code C++"
  - "…still not Satoshi tho".
- Bloomberg, Olga Kharif, 2020-06-02, "Latest Satoshi Nakamoto Candidate Buying Bitcoin No Matter What": "No, I am not."
- Reception: r/bitcoin banned the video; Tone Vays did a rebuttal stream (Chain Bulletin, 2020-05-18, VERIFIED by me, `timing/chainbulletin-unmasking-satoshi-aftermath.txt`).

## 3. HBO "Money Electric: The Bitcoin Mystery" (Cullen Hoback), Oct 2024: Peter Todd

- **Premiere:** HBO, 2024-10-08, 9 pm ET, 100 min (REPORTED, Wikipedia/press).
- **Key evidence, the 2010 forum reply** (VERIFIED by helper via a Wayback capture of 2014-04-20; `theories-a/bitcointalk-topic-2181-wayback-20140420092348.txt`). Bitcointalk topic 2181, "Fees in BitDNS confusion":
  - Satoshi, 2010-12-09 23:58:54: "…You intentionally write a double-spend. You write it with the same inputs and outputs, but this time with a fee … only strictly if the inputs and outputs match and the transaction fee is higher…"
  - Peter Todd ("retep"), 2010-12-10 01:27:59: "Of course, to be specific, the inputs and outputs can't match \*exactly\* if the second transaction has a transaction fee."
  - The film reads this as Satoshi "finishing Satoshi's sentences" from a mistakenly used second account.
- **Other film evidence** (REPORTED: New Yorker 2024-10-08/09, CNN, CoinDesk, Wired, Fortune):
  - Satoshi left days later; "John Dillon" as a Todd alter ego.
  - Canadian/British spellings ("colour", "cheque").
  - "Sacrifice" quote: "I'm probably the world leading expert on how to sacrifice your bitcoins … I've done exactly one such sacrifice, and I did it by hand." The original log was not found.
  - Todd's 2014 tweet: "Pro-tip: when starting a revolutionary cryptocurrency, find someone to frame for doing it first." (VERIFIED)
- **Treatment of Back:** first main suspect. "Well, I thought you might think I'm Satoshi. And I don't want that to be on the record, really…" Covers Malta, Wikipedia edits, 2013-04-17, and Blockstream as "corporate Satoshi". Final scene has Back beside Todd.
- **Todd's denials:**
  - X, 2024-10-08 23:05 UTC: "I'm not Satoshi." (VERIFIED)
  - CoinDesk: "…QAnon style coincidence-based conspiracy thinking…"
  - CNN: "I was simply pointing out a minor correction…"
  - Wired, 2024-10-08: "For the record, I am not Satoshi. It is a useless question, because Satoshi would simply deny it."
  - Wired, 2024-10-22 ("…Now He's in Hiding"): Todd gave Wired photos of himself "skiing and spelunking" that "a superficial look at the metadata would suggest were taken at roughly the same time that Satoshi was posting". Wired "has not had the images forensically analyzed". (VERIFIED article; the images themselves were not seen.)
  - Todd, X, 2024-10-23: the hiding report was "quite the exaggeration".
- **Polymarket** "Who will HBO doc identify as Satoshi?" (created 2024-10-03; ~$44.3M volume; resolved "Other/Multiple") (VERIFIED via API by helper).

## 4. Len Sassaman theory

- **Evan Hatch**, "Len Sassaman and Satoshi: a Cypherpunk History", Medium, 2021-02-22, https://evanhatch.medium.com/len-sassaman-and-satoshi-e483c85c2b10 (VERIFIED via Wayback by helper; HN front page item 26231674).
  - Arguments:
    - Satoshi went silent about 2 months before Sassaman's death (2011-07-03).
    - PGP/NAI with Finney; Mixmaster maintainer; collaborated with Back.
    - COSIC/KU Leuven PhD under Chaum.
    - An academic/European profile (British spelling, dd/mm/yyyy).
    - "Satoshi's post and commit times correspond closely to Len's own hours" on Twitter. This is an unquantified timing claim.
    - Lived with Bram Cohen.
  - The 2021 text has **no** Massias citation or travel-vs-commit analysis. A later revision (Medium dateModified 2024-10-10; Wayback 2026-06-14) adds a Quisquater section: the paper was "only distributed to 70 in-person academic attendees in Belgium". It cites HBVL, 2024-06-21. It also adds the "Senshi" GMX Mixmaster operator and Paul Marengo's Hashcash to-do in Mixmaster.
- **Meredith L. Patterson** (widow):
  - X, 2021-02-23: "It's a very well-researched and respectful article, but to the best of my knowledge, Len was not Satoshi." (VERIFIED)
  - X, 2022-01-17: "Len was a Mac user. He used FileVault…" (VERIFIED)
  - DL News, 2024-10-08: he "isn't Satoshi" … "The best case against him being Satoshi is some newbie mistakes in the design of the original protocol, like being able to send to an IP address." (VERIFIED)
  - Wired, 2024-10-22. (VERIFIED)
  - In *Finding Satoshi* (2026) she reportedly found the theory plausible. (REPORTED)
- **2024 coverage:**
  - Polymarket had Sassaman as favourite (CoinDesk: 35–55%, then 14% after the DL News interview).
  - CoinDesk pieces by Sam Reynolds (2024-10-04), Cheyenne Ligon (10-04), Shaurya Malwa (10-07), and Justin Newton's opinion piece "My Friend, Satoshi?" (10-07).
  - **David Z. Morris**'s piece is on his Substack *Dark Markets* (2024-10-08, "Why Len Sassaman Was Not Satoshi Nakamoto"), not CoinDesk. It concludes "no, Len Sassaman didn't invent Bitcoin".
  - Bart Preneel (Sassaman's advisor), HLN 2024-10-07: "Eerst zien en dan geloven" ("seeing is believing"). (REPORTED; paywalled)
- **Massias et al. white-paper citation ↔ Leuven: YES, already published.**
  - The citation: [2] H. Massias, X.S. Avila, J.-J. Quisquater, "Design of a secure timestamping service with minimal trust requirements", 20th Symposium on Information Theory in the Benelux, May 1999.
  - **Jens Ducrée, arXiv 2206.10257**, "Satoshi Nakamoto and the Origins of Bitcoin — The Profile of a 1-in-a-Billion Genius". v1 2022-06-21 argues Satoshi or someone close "must have personally attended" (Haasrode, 27–28 May 1999) and points to a KU Leuven cryptographer supervised by Chaum who died July 2011. v14 (2022-09-09) names Sassaman. Earliest found. (VERIFIED by helper)
  - HBVL 2024-06-21/24 (Preneel interview; paywalled).
  - David Michel, Global Security Mag, 2024-10-06 (Flickr shelf photo claim; "ChatGPT puts the probability over 99%").
  - DL News 2024-10-08 (deleted X posts; proceedings "likely accessible").
  - Jeremy Clark (Concordia), GitHub PulpSpy/Confluence draft, Oct 2024: mundane route via the *Encyclopedia of Cryptography and Security*.
  - Peter Miller, Medium, 2026-04-12 (sceptical; says Preneel attended, conflicting with Ducrée; Flickr shows a 2002 volume).
  - Event Horizon IQ, 2026-04-24 (David Seroy and Nic Carter amplification).
  - Conflicts to note: attendee-list claims (Ducrée: Quisquater and Preneel not attending; Miller: Preneel attended) and the Flickr claim.
- **July 2011 blockchain tribute** (VERIFIED on-chain by helper):
  - **Block 138725**, 2011-07-30 03:07:58 UTC, tx `930a2114…8e1d72`, 78 outputs encoding ASCII: "LEN "rabbi" SASSAMA[N] 1980-2011 … --Dan Kaminsky, Travis Goodspeed … ASCII BERNANKE".
  - Revealed in Kaminsky's Black Hat USA 2011 "Black Ops of TCP/IP" (slides "Len.", "BitLen"; "the cyber equivalent of pouring one out").
  - Note: the MatoTeziTanka README says block 167,956; the helper's on-chain check says 138725.
- **"Finding Satoshi"** (2026-04-22; director Matthew Miele, with Tucker Tooley also credited as director by Decrypt; EPs William D. Cohan and Tyler Maroney; 1h41m; findingsatoshi.com) (REPORTED):
  - Argues Finney wrote the code and Sassaman the prose.
  - Uses Alyssa Blackburn's ~6 am–10 pm Pacific activity window.
  - Doubts the 2015 "Satoshi" email.
  - Brian Armstrong: "the most thoughtful take on this subject I've seen out there" (VERIFIED tweet).
  - Back: the theory is "self-contradictory" (CoinMarketCap Academy; REPORTED).
- **Sceptical pieces:** Peter Miller (Medium, 2026-04-12, `timing/miller-sassaman-not-satoshi.txt`); Morris (above).

---

## 5. Hal Finney theory

(Helper agent's research; files in `theories-b/` unless noted. Labels are the helper's unless I say otherwise.)

- **Andy Greenberg, Forbes, 2014-03-25**, "Nakamoto's Neighbor: My Hunt For Bitcoin's Creator Led To A Paralyzed Crypto Genius". https://www.forbes.com/sites/andygreenberg/2014/03/25/satoshi-nakamotos-neighbor-the-bitcoin-ghostwriter-who-wasnt/ (VERIFIED, Wayback; `forbes-greenberg-2014-03-25.txt`)
  - Juola & Associates (John Noecker) on a 20,000-character Finney sample: "the best Nakamoto candidate whose writing the firm had ever analyzed".
  - But the Jan 2009 Finney–Satoshi emails "matched the style of the Bitcoin whitepaper more closely than Finney's writing".
  - Finney's denial: "I'm flattered but I deny categorically these allegations … my style is completely different from Satoshi's. I program in C … I don't understand the tricks that Satoshi used."
  - Greenberg concluded the links were "an illusion of a signal in random noise."
  - Finney lived a few blocks from Dorian Nakamoto in Temple City.
- **Jameson Lopp, "Hal Finney Was Not Satoshi Nakamoto"**, published 2023-10-21, modified 2026-05-07. https://blog.lopp.net/hal-finney-was-not-satoshi-nakamoto/ (VERIFIED)
  - **Race:** "On Saturday April 18, 2009 at 8 AM Pacific time Hal Finney … began a 10 mile race in Santa Barbara." Bib 591; results at archive.is/46t9A, which was unreachable, so the race is REPORTED.
  - "Satoshi sent the email to Mike [Hearn] at 9:16 AM Pacific time - 2 minutes before Hal crossed the finish line."
  - The Hearn printout shows "Sat, Apr 18, 2009 at 6:16 PM": "I sent back 32.51 and 50.00." Lopp assumes Swiss display time (CEST), so 16:16 UTC.
  - On-chain check: tx paying 32.51 BTC to Hearn's address confirmed in block 11408 at 15:55:19 UTC (miner-set timestamp).
  - Lopp credits Alyssa Blackburn / Erez Aiden with spotting the race overlap.
  - Other arguments: Finney's typing had slowed by Aug 2010 (Fran Finney's LessWrong comment, 2010-08-22: "from rapid-fire 120 WPM to a sluggish finger peck"); different IPs in the Jan 2009 debug log (Hal 207.71.226.132 vs 68.164.57.219); code-style differences.
- **Hal Finney, "Bitcoin and me (Hal Finney)"**, Bitcointalk topic 155054, 2013-03-19 (VERIFIED by helper; `data/claims/C-finney-bitcoin-and-me-topic155054.html`):
  - "I think I was the first person besides Satoshi to run bitcoin … I was the recipient of the first bitcoin transaction".
  - "at the time, I thought I was dealing with a young man of Japanese ancestry who was very smart and sincere."
  - "In August, 2009, I was given the diagnosis of ALS."
- **Dominic Frisby** (2014 book; Substack 2025-01-12): "If Satoshi is an individual, Hal Finney was not him." (VERIFIED)
- **"Finding Satoshi"** (2026-04-22), Finney + Sassaman (§4, 8.14c). Fran Finney: "Yes, I think he did help build it. The whitepaper itself, I didn't think he wrote." (REPORTED)
- NYT 2026 cites the race and notes Finney and Sassaman were dead before the Aug 2015 Satoshi email (VERIFIED).

## 6. Nick Szabo theory

- **Skye Grey**, "Satoshi Nakamoto is (probably) Nick Szabo", 2013-12-01, https://likeinamirror.wordpress.com/2013/12/01/satoshi-nakamoto-is-probably-nick-szabo/ ; follow-up 2014-03-11 "Occam's razor…" (VERIFIED by helper; the blog is **not** likestream.blogspot).
  - Method: "reverse textual analysis — searching the internet for highly unusual turns of phrase", plus Google Scholar frequencies of phrases like "it should be noted", "for our purposes", "can be characterized", "preclude".
  - 2014: character/word-length histograms rank Szabo closest.
  - TechCrunch interview 2013-12-05: "Nick is by far the number one candidate."
- **Aston University press release, 2014-04-16** (Dr Jack Grieve, 40 final-year forensic linguistics students; VERIFIED): "The number of linguistic similarities between Szabo's writing and the Bitcoin paper is uncanny". It wrongly says the paper "was drafted using Latex" (contradicted by COPA). No research output was published (David Gerard, 2018, opinion). The MatoTeziTanka repo (2026) argues the result was topic-contaminated.
- **Dominic Frisby**, *Bitcoin: The Future of Money?* (Unbound, 2014). Szabo's July 2014 email to Frisby: "Thanks for letting me know. I'm afraid you got it wrong doxing me as Satoshi, but I'm used to it." (REPORTED, via Wikipedia citing the book, p. 147)
- **Szabo denials:**
  - 2011 email to Adrian Chen: "I'm not going to comment any further on this…". A non-answer; screenshot tweeted 2013-12-02 (VERIFIED).
  - To Popper (NYT 2015): "As I've stated many times before, all this speculation is flattering, but wrong — I am not Satoshi." (VERIFIED)
  - 2011-05-28 "Bitcoin, what took ye so long?": "(assuming Nakamoto is not really Finney or Dai)". (VERIFIED)
- **Nathaniel Popper, NYT, 2015-05-15/17**, "Decoding the Enigma of Satoshi Nakamoto and the Birth of Bitcoin": "the most convincing evidence pointed to a reclusive American man of Hungarian descent named Nick Szabo." (VERIFIED) Fortune's 2026 critique still prefers Szabo.
- **Bit gold timestamp controversy** (VERIFIED by helper from Wayback and the Blogger feed):
  - The post at `/2005/12/bit-gold.html` showed "Thursday, December 29, 2005" in a 2006-03-29 capture, but "Saturday, December 27, 2008 … 4:16 PM" from 2009 onward. So an old post was **re-dated forward** to 57 days after the white paper, not backdated.
  - Explanation: Szabo's 2008-08-20 "Reruns" post ("Unenumerated is going into reruns season … reposting the best articles"). The feed shows many 2005–2006 posts re-dated between Aug 2008 and Jan 2009.
  - Who noticed: Skye Grey (2013-12-01, earliest found); Popper (NYT 2015); Deryk Makgill, news.bitcoin.com 2020-01-02 ("Why Nick Szabo Probably Isn't Satoshi"), who pointed to "Reruns".
  - Helper's INFERENCE, not checked for prior publication: the post's old-style Blogger ID 113588451301633208 begins with Unix time 1135884513 = 2005-12-29 19:28:33 UTC.
- **2025 Core v30 / OP_RETURN debate:**
  - Szabo's X posts of 2025-09-29 (VERIFIED), e.g. "The Core argument I've heard is that one can hide data in other ways that are not pruneable…". Cointelegraph (2025-09-29) reports "I strongly recommend not upgrading to Core v30."
  - "Exposed his ignorance of basic technical aspects" is **Carreyrou's characterization** (NYT 2026). The helper found no article itemising Szabo's specific technical errors.

## 7. Other theories (brief map)

| Candidate | Key source | Date | Status | Label |
|---|---|---|---|---|
| Wei Dai | Sunday Times, 2014-03-02 (Dai: Satoshi "just don't read like Nick's to me"); Dai's b-money cited in the white paper; Dai said in Wallace's book he didn't think Satoshi was anyone he knew | 2014; 2025 | Denied / not seriously pursued | VERIFIED (gwern page) / REPORTED |
| Dorian Nakamoto | Leah McGrath Goodman, Newsweek, online 2014-03-06: "I am no longer involved in that and I cannot discuss it…". P2P Foundation "I am not Dorian Nakamoto." ≈01:18 UTC 2014-03-07. Account later said hacked (Sep 2014). | 2014 | Discredited | VERIFIED (Wayback) |
| Craig Wright | COPA v Wright, oral ruling 14 Mar 2024 (judgment §7.1–7.4: not the author of the white paper, not Satoshi 2008–2011, didn't create Bitcoin, not author of initial software). Written judgment [2024] EWHC 1198 (Ch), 20 May 2024: "Dr Wright lied to the Court extensively and repeatedly … forged documents"; §10: "likely that a number of people contributed to the creation of Bitcoin, albeit that there may well have been one central individual." Contempt [2024] EWHC 3316 (Ch), 20 Dec 2024: 12 months suspended for 2 years. | 2024 | Adjudicated not Satoshi | VERIFIED (helper + my checks of §492, §636) |
| Paul Le Roux | Evan Ratliff, Wired, 2019-07-16: "What my narrative was lacking … was any single fact that couldn't be explained away by coincidence." | 2019 | Speculative | VERIFIED by helper |
| Gavin Andresen | Vice 2013 list; goldmonkey21/doxer names him | 2013, 2021 | Fringe | REPORTED/VERIFIED |
| Vili Lehdonvirta, Michael Clear | Joshua Davis, New Yorker, 2011-10-10 ("The Crypto-Currency"); both denied | 2011 | Denied | VERIFIED by helper |
| Neal King, Vladimir Oksman, Charles Bry | Adam Penenberg, Fast Company, Oct 2011 (patent US20100042841, "computationally impractical to reverse"); denials | 2011 | Denied | VERIFIED by helper |
| Ross Ulbricht | Ron & Shamir paper, Nov 2013; retracted after Dustin Trammell identified the address; Lerner rebuttal 2013-11-26 | 2013 | Retracted | VERIFIED by helper |
| Elon Musk | Sahil Gupta Medium post (2017); Musk, 2017-11-28: "Not true. A friend sent me part of a BTC a few years, but I don't know where it is." | 2017 | Denied | VERIFIED (tweet) |
| David Chaum | CoinMarketCap "Satoshi Files" 2023 | 2023 | Circumstantial | REPORTED |
| James A. Donald | Wallace's leading lead (NYMag excerpt 2025-03-17): rare shared words "hosed", "fencible"; Hungarian notation in his Crypto Kong code; Donald: "I have a very good idea of who it might be, but I don't actually, uh, no." | 2025 | Open | VERIFIED by helper |
| Ian Grigg | news.bitcoin.com "The Many Facts Pointing to Ian Grigg Being Satoshi"; Michael Chon's Medium stylometry | n.d. | Fringe | REPORTED (not fetched) |
| Ray Dillinger | ULC Legal Burrows' Delta top match (2026-03-24) | 2026 | Fringe | VERIFIED by helper |
| Jack Dorsey | 2025 social-media theory; Lopp rebuttal via timestamps (Feb 2025) | 2025 | Rebutted | VERIFIED |
| Stephen Mollah | Self-claim at a London event, 2024-10-31 (DL News) | 2024 | Self-claim | VERIFIED by helper |
| Phil Wilson ("Scronty") | "one third of Satoshi" self-claim, 2017/18; ranked first in ULC's 2024 Naive Bayes run | 2017–2024 | Self-claim | REPORTED |
| Michael Stokes (Shareaza) and other Windows P2P devs | whowrotebitcoin.com code-style "leads" | 2026 | Speculative | VERIFIED by helper |
| Shinichi Mochizuki (Ted Nelson 2013), Jed McCaleb, "European collective" | per Wikipedia | 2013 | Fringe | REPORTED |

---

## 8. Timing studies (posting-time histograms, time zones, weekends, SVN commits)

| # | Who / where | Date | Data | Claim | URL | Label |
|---|---|---|---|---|---|---|
| 8.1 | **Stefan Thomas**, Bitcointalk thread "Satoshi's Posting Times" (topic 37743) | 2011-08-17 | Satoshi's Bitcointalk posts (hourly counts, GMT; his data sums to 540 posts) | "the night dip is between 6-11am GMT, so assuming this person sleeps at night, he should live in GMT-5 to GMT-7 somewhere which is the Americas." Raw data: `[[0,32],[1,23],[2,15],[3,10],[4,9],[5,3],[6,3],[7,0],[8,0],[9,1],[10,0],[11,0],[12,3],[13,5],[14,14],[15,18],[16,46],[17,65],[18,65],[19,43],[20,42],[21,55],[22,46],[23,42]]`. He says he did it "a long time ago" (i.e. before Aug 2011). Replies raise the objection that he may have been at work/school, or working nights. | https://bitcointalk.org/index.php?topic=37743.0 | VERIFIED (`timing/bitcointalk-37743-stefan-thomas-posting-times.txt`) |
| 8.2 | **Benjamin Wallace, Wired**, "The Rise and Fall of Bitcoin" | 2011-11-23 | Reports Thomas's chart | Source of the Wikipedia wording: "steep decline to almost none between 5 a.m. and 11 a.m. GMT … this pattern held even on Saturdays and Sundays". | https://www.wired.com/2011/11/mf-bitcoin/ | REPORTED (via Wikipedia citation; not read) |
| 8.3 | **Michael Goetzman** blog | 2014-09-03 | Repeats Thomas | Says UTC−5/−6 (US East/Central) | https://goetzman.com/2014/09/03/who-is-satoshi-nakamoto/ | VERIFIED (`timing/goetzman-2014.txt`) |
| 8.4 | **"In Search Of Satoshi"** (Medium), "The Time Zones of Satoshi Nakamoto" | 2018-02-13 | White-paper PDF CreationDates; SVN log; Bitcointalk posts by hour | (a) Reads the PDF offsets as US Mountain time, noting the Oct 2008 −07'00' is anomalous for DST. (b) Claims SVN commit times show "British Summer Time" (+0100 until 2009-10-25 / 2010-10-30, then +0000). (c) Late-night activity clusters in Feb 2010 and summer 2010, with a gap Mar–May 2010 and at Christmas 2009, leading to a "student cramming for final university exams" hypothesis. (d) A post of 2010-02-15 06:28 UTC calls 14 Feb "yesterday" and uses DD/MM/YYYY. | https://medium.com/@insearchofsatoshi/the-time-zones-of-satoshi-nakamoto-aa40f035178f | VERIFIED (`timing/insearchofsatoshi-time-zones.txt`; article may be truncated after the DD/MM point) |
| 8.5 | **Jameson Lopp** charts, reported by AMBCrypto / cryptonews.net, "Wright is Wrong: Timestamps…" | 2019-04-25 | Satoshi posts and commits vs Craig Wright's blog posts | "If you assume standard sleeping patterns then it appears Satoshi resided in eastern North America or western South America while Wright's posts line up with eastern Australia." | https://cryptonews.net/news/other/138601/ | REPORTED |
| 8.6 | **Doncho Karaivanov, The Chain Bulletin**, "Satoshi Nakamoto Lived in London While Working on Bitcoin" | 2020-11-23 | 539 Bitcointalk posts + 169 SourceForge commits (s_nakamoto, 2009-10-21 → 2010-12-15, UTC) + 34 cryptography/bitcoin-list emails, i.e. 742 events on 206 days (2008-10-31 → 2010-12-13). Plus PDF metadata and the genesis block. | Scatter charts in London / US-Eastern / US-Pacific / Tokyo / Sydney time. All three of London, US-Eastern and US-Pacific are "plausible". Japan and Australia are excluded. London is favoured via the print-only Times headline and 2008 readership data. Discusses the PDF offsets (−07'00' PDT; −06'00' MDT) as likely VM or clock settings or a third party. The last-activity bulk is 1–3 AM London. Deliberately excludes private emails whose timestamps it couldn't confirm as UTC. | https://chainbulletin.com/satoshi-nakamoto-lived-in-london-while-working-on-bitcoin-heres-how-we-know | VERIFIED (`timing/chainbulletin-london.txt`) |
| 8.7 | **Prof Bill Buchanan** (Edinburgh Napier), Medium, "Meet Satoshi. From the UK? Bitcoin was a 5pm to 3am job?" | 2020-11-28 | Re-uses Chain Bulletin's data | If Bitcoin was a day job, then US Pacific; if a hobby after work, then UK (5pm–3am). Buchanan leans UK/hobby and mentions Adam Back. | https://medium.com/asecuritysite-when-bob-met-alice/meet-satoshi-from-the-uk-69a5f5722d00 | VERIFIED (`timing/buchanan-meet-satoshi-from-the-uk.txt`) |
| 8.8 | **CoinDesk, Michael Kapilkov**, "Previously Unpublished Emails of Satoshi Nakamoto Present a New Puzzle" | 2020-11-26 | Three Finney–Satoshi emails from Nathaniel Popper (Nov 2008–Jan 2009), with headers | Satoshi's Date headers show UTC+8. Finney's server appears to receive emails before Satoshi's sent time. Derek Atkins suggests a local-time system not set up for DST. Inconclusive. | https://www.coindesk.com/markets/2020/11/26/previously-unpublished-emails-of-satoshi-nakamoto-present-a-new-puzzle | REPORTED (fetch-tool summary) |
| 8.9 | **Chain Bulletin rebuttal**, "No, CoinDesk, Satoshi's Local Time Zone Wasn't UTC+8" | 2020-11-26 | Same headers | UTC+8 is the anonymousspeech.com webmail server's zone (Received: `mail.anonymousspeech.com [124.217.253.42]`; X-Mailer: Chilkat), so the Date header is irrelevant to Satoshi's location. | https://chainbulletin.com/no-coindesk-satoshis-local-time-zone-wasnt-utc8 | VERIFIED (`metadata/chainbulletin-no-coindesk-utc8.txt`) |
| 8.10 | **Blackburn, …, Erez Lieberman Aiden** (Baylor/Rice), "Cooperation among an anonymous group protected Bitcoin during failures of decentralization", Supplementary Fig S20 | preprint June 2022 (arXiv 2206.02871) | Satoshi's emails to Hearn, Finney, the Cryptography and Bitcoin lists, Bitcointalk posts, SourceForge commits, **plus prolonged Patoshi-miner outages** | the datasets suggest Satoshi was usually inactive for about 8 hours between 06:00 and 14:00 UTC, which the authors read as consistent with living in the Americas (paraphrased) This is the published analysis combining **Patoshi downtime with activity** (see 9(e)). Lopp (X, 2022-06-07) called the paper's "temporal analysis of Patoshi miner downtime vs Satoshi public activity" its interesting part. | https://aidenlab.org/bitcoin.pdf ; https://arxiv.org/abs/2206.02871 ; https://x.com/lopp/status/1534091662401720325 | VERIFIED (`timing/aidenlab-bitcoin.txt`, lines ~2146–2157; `timing/lopp-x-1534091662401720325.json`) |
| 8.11 | **Chainless.hk** (HK Chinese-language series), "Satoshi Nakamoto's residence and nationality" | 2023-01-23 | Re-reads Chain Bulletin's charts | Concludes US West Coast (Pacific), treating the Oct-2008 PDF offset as an unintended leak | https://chainless.hk/2023/01/23/4-satoshi-nakamotos-residence-and-nationality/ | VERIFIED (`timing/chainless-residence.txt`) |
| 8.12 | **Jameson Lopp**, "Jack Dorsey is not Satoshi Nakamoto" | 2025-02 | Lopp's own Satoshi activity dataset (Google Sheet), compared with 6,200 Dorsey tweets | "Satoshi held a pretty consistent schedule that would make sense for someone living in the Pacific time zone." Lists Satoshi's two long gaps: 2009-03-04 16:59:12 → 2009-10-21 01:08:05 UTC and 2010-03-24 18:02:55 → 2010-05-16 21:01:44 UTC. Event-by-event alibi method (same as his Finney race analysis). Raw data: https://docs.google.com/spreadsheets/d/16uyf7v9xcitr5zy1-WVYx7UiKnasHDcViK_udZyfExg | https://blog.lopp.net/jack-dorsey-is-not-satoshi-nakamoto/ | VERIFIED (`timing/lopp-jack-dorsey-is-not-satoshi.txt`) |
| 8.13 | **satoshinakamoto.me/stats** | undated | All platforms, per hour/day | Most active: "July 2010, mid-month Thursdays between 17:00-17:59 UTC" (page says "17:79"). Raw data downloadable. | http://satoshinakamoto.me/stats/ | VERIFIED (`timing/satoshinakamoto-me-stats.txt`) |
| 8.14a | **COPA v Wright**, judgment §636 | 2024-05-20 | COPA's scatter plot and bar graph of Satoshi emails, posts and check-ins, Aug 2008–Apr 2011 | In Sydney time, activity is "from midnight through to 5pm / 6pm … greatest concentrations … 2am to 11am (highest at 4-5am, Sydney time)". Used to rebut Wright. | https://caselaw.nationalarchives.gov.uk/ewhc/ch/2024/1198 | VERIFIED (`theories-b/copa-v-wright-2024-EWHC-1198-Ch.txt`) |
| 8.14b | **Jameson Lopp**, "Was Satoshi a Greedy Miner?" | 2022-09-16 | Patoshi block timestamps + Lopp's Satoshi activity sheet | "I strongly believe that Satoshi's machine slept." Reconstructs the Jan 2009 "double helix" in Pacific time: mined block 1386 at 4 PM Pacific on 22 Jan; restarted ~8 AM next day (two instances by accident); crashed after block 1916 at 10:30 PM on 25 Jan; resumed ~7 AM on 26 Jan. The helper agent found this the **only published link between Patoshi on/off events and a daily schedule**, besides Blackburn et al. (8.10). | https://blog.lopp.net/was-satoshi-a-greedy-miner/ | REPORTED by helper agent as VERIFIED (`code-forensics/lopp-was-satoshi-a-greedy-miner.*`); I didn't read it |
| 8.14c | **"Finding Satoshi"** documentary (dirs. Tucker Tooley and Matthew Miele; investigation by William D. Cohan and Tyler Maroney) | released 2026-04-22 | Alyssa Blackburn's timing data | Coverage says Blackburn put Satoshi's active hours at roughly 6 am–10 pm Pacific, calling Back, Szabo and Dai "inconceivable" on timing. The film concludes Finney (code) + Sassaman (prose). | Bitbo / The Block / Decrypt / Protos coverage (`theories-b/bitbo-finding-satoshi-documentary.*`, `…/protos-are-we-done-finding-satoshi.*`) | REPORTED |
| 8.15 | **GNcrypto** recap; cryptonews.net "25 Lesser-Known Facts…" | 2026-06-08 | Secondary compilation | Repeats the PDF Mountain-time anomaly, SVN "+0100/+0000 consistent with the UK", and the DD/MM format | https://www.gncrypto.news/news/emails-code-metadata-trace-satoshi-2010-bitcoin-actions/ | REPORTED |

Notes on the timing literature:
- **Conclusions conflict.** Different authors read the same inactive window (≈05/06–11/14 UTC) as UK night-owl, US-Eastern, or US-Pacific. The disagreement is about assumptions (day job vs hobby), not data.
- Lopp himself said "eastern North America" in 2019 but "Pacific" in 2025.
- **SVN "BST" claim (8.4), INFERENCE, high confidence.** `svn log` renders `svn:date` (stored in UTC) in the *viewer's* local time zone. The +0100/+0000 offsets in that article therefore most likely reflect the author's own machine (in the UK), not Satoshi's. Chain Bulletin (8.6) treats SVN times as UTC, consistent with this. I found no published correction of 8.4.
- **Weekend / holiday patterns.** Wired 2011 reports the gap "held even on Saturdays and Sundays". 8.4 notes a Christmas-2009 gap and a Mar–May 2010 gap (student hypothesis). A search for Thanksgiving/US-holiday or UK bank-holiday analyses found nothing.
- The **Malmi emails** (released Feb 2024) show Date headers such as `Sun, 03 May 2009, 23:32:26 +0100` (NYT interactive quoting a GMX email; VERIFIED in `nyt-carreyrou-2026-04-08.interactives.txt`). The helper agent tabulated all 144 and found the offsets flip +0100 ↔ +0000 on the **EU/UK** DST dates. It found **no published analysis** of this; see 9(d).
- bitcoin.com's "25 Lesser-Known Facts" (2026-06-07/08) states SVN commits show "+0100 (winter) and +0000 (summer)". That has the UK offsets backwards (and repeats the likely viewer-time-zone artifact from 8.4), so treat it as unreliable.

---

## 9. Metadata and forensic studies

### 9(a) White-paper PDF metadata

| Who | Date | Finding | URL | Label |
|---|---|---|---|---|
| Sergio Demian Lerner, Bitslog, "How you will not uncover Satoshi" | 2014-06-19 | Both 2008 and 2009 PDFs were made with **OpenOffice.org 2.4 Writer**. 2009 CreationDate is `D:20090324113315-06'00'`. `/ID [<CA1B0A44BD542453BEF918FFCD46DC04>…]` is an MD5 over metadata + system time (ms) + `m_aContext.URL` (the file path), so in principle a username could be brute-forced. Asserts "we know Satoshi's PC was a Windows XP". **gwern's comment (2014-06-19):** "Or you could try looking at the bitcoin-0.1.0.rar he released, with the metadata in it & the .exe he compiled for everyone." | https://bitslog.com/2014/06/19/how-you-will-not-uncover-satoshi/ | VERIFIED (`metadata/lerner-2014-how-you-will-not-uncover-satoshi.txt`) |
| In Search Of Satoshi, "The Time Zones of Satoshi Nakamoto" and "Leaking File URLs in the metadata of the Bitcoin whitepapers" | 2018-02-13 | Oct 2008 draft (gwern's copy `20081003-nakamoto-bitcoindraft.pdf`): `CreationDate(D:20081003134958-07'00')`, Producer "OpenOffice.org 2.4", Creator "Writer". bitcoin.pdf: `D:20090324113315-06'00'`. The hashed URL is a **temp file**, not the saved path (`PDFFilter::implExport()` uses `utl::TempFile`). | https://medium.com/@insearchofsatoshi/leaking-file-urls-in-the-metadata-of-the-bitcoin-whitepapers-742bd31c84b7 | VERIFIED (`metadata/insearchofsatoshi-leaking-file-urls.txt`) |
| Chain Bulletin (Karaivanov) | 2020-11-23 | −07'00' on 2008-10-03 is PDT. −06'00' on 2009-03-24 is "Mountain Time (MT)". Possible explanations: VM, manual time-zone change, or a third party exporting the PDF. | (8.6) | VERIFIED |
| obxium, "Nakamoto Research: The Bitcoin whitepaper" (v0.3.4, updated 2026-01-23) | 2026-01 | pdfid / pdf-parser / exiftool walk-through. Catalog has **`/Lang (en-GB)`**. A PDF comment reads `äüöß` (it's a standard binary-marker comment). "Nakamoto used a Windows XP PC". Discusses a LaTeX→OpenOffice workflow as possible misdirection. Carries the disclaimer "THIS CONTENT MAKES NO CLAIMS ABOUT THE IDENTITY OF SATOSHI NAKAMOTO". | https://nakamoto-research.obxium.com/whitepaper.html | VERIFIED (`metadata/obxium/whitepaper.txt`) |
| COPA v Wright, judgment and appendix ([2024] EWHC 1198 (Ch), Mellor J) | 2024-05-20 | See bullets below the table. | https://caselaw.nationalarchives.gov.uk/ewhc/ch/2024/1198 ; https://www.judiciary.uk/wp-content/uploads/2024/05/COPAv-Wright-Judgment-Appendix.pdf | VERIFIED (`theories-b/copa-v-wright-2024-EWHC-1198-Ch.txt`, `…-Appendix.txt`; paras quoted checked by me) |
| **Fox Chapel Research** (with X researcher **tmctmt**), "How you probably will find Satoshi" | **2026-05-21** | Extends Lerner (details below). | https://foxchapelresearch.substack.com/p/how-you-probably-will-find-satoshi | VERIFIED (`metadata/foxchapel-how-you-probably-will-find-satoshi.txt`) |

COPA v Wright, what the judgment and appendix say about the genuine PDFs:
- Appendix §59: "The Bitcoin White Paper was not written in LaTeX. It was written and produced in OpenOffice 2.4 … Examination by both parties' experts has led them both to conclude, and agree…" (Rosendahl for COPA, Lynch for Wright; joint report). Main judgment §303.1 says the same, adding "consistent with the metadata of the public Bitcoin White Paper versions".
- Control copies: {ID_000226}, creation date 3 Oct 2008; {ID_000865}, 24 Mar 2009, hash-identical to the SourceForge "Bitcoin.pdf" (§320). This is per the helper agent; I did not open §320.
- **Main judgment §492 does mention the time-zone offsets** (VERIFIED): "The CreateDate in the relevant version of the Bitcoin White Paper is 2009-03-24T11:33:15-06:00 … the October version of the Bitcoin White Paper used a -7 hours time zone". This comes up only because Wright's claimed LaTeX command used the wrong zone. The court did not interpret the offsets as evidence of Satoshi's location.
- §636 (VERIFIED): COPA plotted Satoshi's emails, posts and check-ins (Aug 2008–Apr 2011) in **Sydney time** to rebut Wright. Activity was "focused in the period from midnight through to 5pm / 6pm in Sydney time, with the greatest concentrations in the period from 2am to 11am (highest at 4-5am, Sydney time)". See §8.

Fox Chapel Research's findings:
- The PDF /ID hash uses the %TMP% path (`C:\DOCUME~1\<8.3 name>\LOCALS~1\Temp\svXXX.tmp\svYYY.tmp`, base-26 "0-p" names).
- Windows XP's 64-tick timer cuts the millisecond space to ~65 values.
- A modified Hashcat MD5 kernel was run on rented vast.ai GPUs. Result: **no match**. They say Satoshi's Windows username is not ≤4 characters and not a common name, and "Satoshi did not use Linux". They estimate ~60% of distinct English-speaking Windows usernames have been tried.
- They assume, but consider likely, that the PDFs weren't tampered with. They mention a pre-release draft sent to "Stealthmonger" "who later went on to share it".
- Code: https://github.com/foxchapelresearch/satoshi-solver (created 2026-05-21) and a WebGPU demo at https://foxchapelresearch.github.io/satoshi-solver/.

**PDF time-zone offsets: what's published vs not.**
- Published: both offsets (−07'00' Oct 2008; −06'00' Mar 2009), and their readings as PDT/MDT/"Mountain with DST anomaly".
- Searched but **found no** analysis of the specific idea that a Windows XP clock with **pre-2007 (unpatched) US DST rules** could explain the pair. Queries: "bitcoin whitepaper metadata -06'00' daylight saving 2007 DST change unpatched Windows". The nearest are In Search Of Satoshi's "bug in OpenOffice 2.4 or even Windows XP" remark and Derek Atkins's "not set up for DST" remark about emails (8.8).

### 9(b) Bitcoin v0.1.0 release archive / binary

| Who | Date | Finding | URL | Label |
|---|---|---|---|---|
| gwern (blog comment) | 2014-06-19 | Suggested looking at `bitcoin-0.1.0.rar` metadata and the .exe | (Lerner post above) | VERIFIED |
| **Georgi Stefanov, The Chain Bulletin**, "Satoshi Used Timestamps For Early Bitcoin Source Code Versioning" | **2020-11-19** | Details below. "This post will not focus on Satoshi's identity." | https://chainbulletin.com/satoshi-used-timestamps-for-early-bitcoin-source-code-versioning | VERIFIED (`metadata/chainbulletin-source-code-timestamps.txt`) |
| obxium, "Early Bitcoin binary analysis notes" (v0.3.4, updated 2026-01-23) | 2026-01 | Details below. | https://nakamoto-research.obxium.com/binary-analysis.html | VERIFIED (`metadata/obxium/binary-analysis.txt`) |
| **Fox Chapel Research** | **2026-05-21** | Details below. | (9(a) row) | VERIFIED |
| ANY.RUN malware-sandbox reports for `bitcoin-0.1.0.rar` (incl. the Nakamoto Institute S3 copy) | n.d. | Sandbox reports exist and normally display PE metadata. No identity analysis. | https://any.run/report/8b17eb9a5707f2519defda4cdf8d14fa1b8dee630e11e6ef85ff9f5547555b56/406b2a06-f351-4f3b-8965-918c56382173 | REPORTED (not opened) |

Chain Bulletin (Stefanov, 2020-11-19) findings:
- `unrar` listings of the **Nov 2008 preview** `bitcoin_src1.rar`: all files dated 15-11-08 00:00, later shown as 00:00:01.
- **bitcoin-0.1.0.rar**: MD5 91e2dfa2af043eabbb38964cbf368500. Files set to 07-01-09 01:00 or 10-01-09 01:01.
- **bitcoin-0.1.3.rar**: 11-01-09 01:02 and 12-01-09 01:03. Conclusion: **Satoshi encoded the version in the file time** (01:00 = 0.1.0, 01:01 = 0.1.1, …).
- The public "0.1.0" rar is **actually 0.1.1**: `VERSION = 101`, and SourceForge lists the release date as 2009-01-12.
- The RAR's **directory** entries keep untouched high-precision mtimes: `src/obj/` 2009-01-07T15:36:27.468750, `src/rc/` 2009-01-07T15:37:33.671875, `src/` 2009-01-10T23:15:06.703125. Host OS flag is WIN, so the RARs were created on Windows.
- **bitcoin-0.1.0.tgz** has uname/gname **hal/hal**: it was repacked by Hal Finney ("Finney extracted the files on 10 January at 18:34 local time … assuming … US/Pacific").
- Sources: for the 0.1.0 rar/tgz, copies Hal Finney sent to Marc Bevand ("mrb"), who posted them in Bitcointalk topic 68121 (March 2012; VERIFIED by me, `metadata/bitcointalk-68121-hal-finney-0.1.0-archives.txt`); diyhpl.us for 0.1.3; github.com/fernandonm/bitcoin/releases/tag/preview for the Nov 2008 preview.

obxium binary-analysis findings for `bitcoin.exe` 0.1.0:
- Size 6,440,960 bytes; MD5 307ad86c412c02abeb821afbb900355b; SHA-256 fbcac071d92e26d82ec917214e334bd43850c0691f113bab1d4741c9bdd30d2d.
- "Compiler: MinGW (gcc-3.4.5)", "Linker: GNU linker ld", "(stripped to external PDB)". wxWidgets.
- **"Compilation timestamp: 2009-01-10 23:16:00 UTC"**, and "Creation time: 2009-01-10 23:16:00 UTC".
- PE sections and imports; Ghidra stats.
- Disclaimer: "makes no claims about the identity".

Fox Chapel Research's archive findings:
- Satoshi's .rar files "could *only* have been produced by WinRAR versions older than WinRAR 3.62" (released 2006-12-04), found by recompressing with ~100 WinRAR versions.
- The folder mtimes (`15:36:27.4687500`, `15:37:33.6718750`, `23:15:06.7031250`) come from a 64-tick SYSTEMTIME timer, "exactly what you'd expect … on normal Windows XP hardware".
- **Footnote 2:** WinRAR stores local time without a zone, so the timestamp is what Satoshi's clock showed; the author remarks on the unusual midweek working hour (paraphrased)

**What I could not find published (negative results, important).**
- **Time zone from archive timestamps.** Searched: "bitcoin.exe 2009-01-10 23:16 compile Satoshi time zone GMT rar local time"; "\"23:15:06\" bitcoin src rar Satoshi"; "Satoshi compile time bitcoin.exe 0.1 reveals time zone UTC GMT"; "Satoshi was in GMT January 2009 evidence bitcoin release archive folder timestamp matches exe compile time"; "\"bitcoin-0.1.0.rar\" metadata timestamps time zone Satoshi analysis". Result: **no published analysis derives Satoshi's time zone by comparing the RAR folder times (local wall-clock, per Fox Chapel) with the PE compile timestamp (UTC, per obxium)**. The ingredients are all published separately: Chain Bulletin 2020 (`src/` 23:15:06 local), obxium 2026 (PE 23:16:00 UTC), and Fox Chapel 2026 ("WinRAR does not normalize to UTC"). Nobody I found put them side by side, and Fox Chapel explicitly treats the times as local without converting to a zone.
- **INFERENCE (for the coordinator, not a finding here).** If both values are right, they sit ~1 minute apart, which would imply a UTC+0 clock on 2009-01-10. This must be checked against the actual files before anyone relies on it. In particular, PE TimeDateStamp is UTC by convention for MinGW ld, and the RAR 2.9 EXTTIME fields are local time.
- **Tar uname/gname in later Linux tarballs** (0.2/0.3.x). Searched: "bitcoin 0.3 linux tar.gz Satoshi tarball owner uname gname". Found nothing. The only published tar-owner analysis is the Hal-made 0.1.0 tgz ("hal/hal").
- **Embedded build paths / PDB paths in bitcoin.exe.** Only obxium's "stripped to external PDB" note. I found no published extraction of a PDB/build path string.

### 9(c) Satoshi's PGP key

- The key served by the Satoshi Nakamoto Institute, https://satoshi.nakamotoinstitute.org/satoshinakamoto.asc (VERIFIED, `metadata/satoshinakamoto-nakamotoinstitute.asc`; inspected with `gpg --list-packets`, not imported):
  - Armor header `Version: GnuPG v1.4.7 (MingW32)`.
  - Primary DSA-1024 key ID **18C09E865EC948A1**, created 1225390759 = **2008-10-30 18:19:19 UTC**.
  - UID "Satoshi Nakamoto <satoshin@gmx.com>".
  - pref-sym-algos 9 8 7 3 2; **pref-hash-algos 2 8 3**; pref-zip 2 3 1.
  - Elgamal-2048 subkey CF1857E6D6AAA69F, same creation time.
- **Sarah Jeong, Motherboard/Vice**, "Satoshi's PGP Keys Are Probably Backdated and Point to a Hoax" (2015-12-09), https://www.vice.com/en/article/satoshis-pgp-keys-are-probably-backdated-and-point-to-a-hoax/ (REPORTED via fetch-tool summary):
  - "The Original Key appears to have been generated on a Windows version of GnuPG that was already outdated at the time"; DSA-1024 was the GnuPG default; hash prefs "2,8,3".
  - By contrast, the Wired/Gizmodo (Craig Wright) keys used RSA-3072 and hash prefs "8,2,9,10,11", "added to the GnuPG code tree … on July 9, 2009", so they were backdated.
- Gwern Branwen & Andy Greenberg (Wired, 2015-12-08) and CoinDesk (2015-12-10, https://www.coindesk.com/markets/2015/12/10/satoshi-denies-being-wright-amid-doubts-over-pgp-data) covered Wright's keys, including Google Reader caches showing a key inserted into a 2008 blog post after 2013 (REPORTED).
- A Scribd rebuttal ("Appeal to Authority: a Failure of Trust") argues GnuPG 1.4.7 could produce those preferences (REPORTED).
- **Not found:** any published analysis tying the key's 18:19 UTC creation time to a time zone (a key creation time alone can't give one), or a software fingerprint beyond "GnuPG 1.4.7 MingW32 / outdated Windows build".

### 9(d) Email header analysis

Mostly from the helper agent (files in `code-forensics/`). Its labels are carried through; where I also read the source myself I say so.

- **Whitepaper announcement, full headers.** Derek Atkins and Sidney Markowitz posted them in a metzdowd thread in Nov 2020 (helper: VERIFIED primary; `code-forensics/metzdowd-2020-11-satoshi-email-timestamps-thread.txt`):
  - `Received: from server123 ([124.217.253.42]) by anonymousspeech.com with MailEnable ESMTP; Sat, 01 Nov 2008 02:20:18 +0800`
  - `Date: Sat, 01 Nov 2008 02:10:00 +0800`
  - `X-Mailer: Chilkat Software Inc`
  - `Message-ID: <CHILKAT-MID-…@server123>`
  - About a 29-hour moderation delay.
  - **No client IP and no X-Originating-IP.**
- **CoinDesk/Kapilkov (2020-11-26), and the Chain Bulletin rebuttal the same day.** The +0800 comes from AnonymousSpeech's server (Tokyo; Chilkat/.NET webmail), not Satoshi's PC. See 8.8 and 8.9; the rebuttal is VERIFIED by me.
- **Dustin Trammell's Jan 2009 mbox files** (helper's own check of `data/satoshi/raw/private_emails/trammell`, not a publication). Same chain: `server123 [124.217.253.42]` → anonymousspeech.
- **Malmi GMX emails (Feb 2024, https://mmalmi.github.io/satoshi).** The helper tabulated all 144 of Satoshi's `satoshin@gmx.com` Date headers:
  - +0100 in May–Oct 2009 and May–Oct 2010; +0000 from 26 Oct 2009 to Mar 2010 and from Dec 2010 to Feb 2011.
  - The switch falls between #41 "Sat, 24 Oct 2009 00:55:06 +0100" and #42 "Mon, 26 Oct 2009 17:50:10 +0000", i.e. the **EU/UK DST change (25 Oct 2009), not the US one (1 Nov)**.
  - These are not German local time (+0100/+0200), and Malmi's own replies are +0200/+0300.
  - **No published analysis of this pattern found.** Queries: "Satoshi Malmi emails Date header +0100 +0000 GMX British Summer Time"; "Satoshi GMX email timestamps daylight saving October 25 2009".
  - This is the helper's own tabulation, **not yet verified by me**. What sets the Date header in GMX webmail (the account's time-zone setting vs the client clock) also still needs checking.
- **Hearn emails.** Gmail printouts, no raw headers. Lopp's Finney analysis assumes the printout was displayed in Swiss time (§5).
- **2014 GMX hack.** theymos, Bitcointalk topic 775174 (2014-09-08): "The email was not spoofed in any way…". The hacker's claim "your IP leaked when you used your email account sometime in 2010" was never substantiated (helper: VERIFIED thread).
- **The "leaked IP" in Southern California** (REPORTED). whoissatoshi.wordpress.com ("Bounty Hunter"), 2016-02-20:
  - Quotes Hal Finney's 2009-01-10 debug.log (bitcoin-list msg 21295694).
  - IRC nick `u4rfwoe8g3w5Tai` on host `h-68-164-57-219.lsanca54.dynamic.covad.net` (68.164.57.219, Covad, LA area); another nick via `gateway/tor`; Finney at 207.71.226.132.
  - That 68.164.57.219 was Satoshi is the blogger's own inference.
  - Also used by Lopp (2023) and Cryptobriefing (2026-07-06, "Satoshi ran two nodes").
  - Carreyrou calls it a dead end and "probably weren't mistakes" (VERIFIED, NYT).
- **"Russian proxy" claim.** Cointelegraph/Kapilkov, 2020-06-03: an IP decoded from the irc.cpp example comment (87.251.146.x). Rebutted (REPORTED).
- **Not found:** any published analysis of Received headers, Tor exit IPs or X-Originating-IP in Satoshi's **GMX** mail. Only the anonymousspeech/vistomail headers have been published and analysed.

### 9(e) Patoshi pattern and on/off times

From the helper agent (files `code-forensics/bitslog-*`, etc.). I verified Back's comment on the 2013-04-24 post, and Blackburn et al., myself.

- **Sergio Demian Lerner, Bitslog:**
  - 2013-04-17, "The Well Deserved Fortune of Satoshi Nakamoto". ExtraNonce slopes; "Satoshi fortune is around 1M Bitcoins"; restarts "approximately every 100 hours, probably to backup the wallet".
  - 2013-04-24, ~980K BTC.
  - 2013-09-03/04: nonce LSB restricted to [0–9] and [19–58]; "Satoshi's Machine".
  - 2014-04-03, "Chain-Archeology": "double helix" = two miner instances; "probably quad-core".
  - 2014-06-23, "July 2009 Mystery Solved": stop/start of Satoshi's mining.
  - 2019-04-16, "The Return of the Deniers and the Revenge of Patoshi": ~22k blocks, ~1.1M BTC. Longest pause 10 days; full-day stop 2009-07-18. **Zero Patoshi→Patoshi timestamp inversions**, hence "There is a single PC clock whose time is stamped in the Patoshi blocks."
  - 2020-06-22, "A New Mystery in Patoshi Timestamps": consecutive-Patoshi gaps cluster at ~312 s.
  - 2020-08-22, "The Patoshi Mining Machine": 5 nonce sub-ranges, decrementing nonce, 5 threads on a high-end CPU (credits Kim Nilsson).
  - 2020-09-03, "Re-mining Patoshi Blocks for Dummies".
- **Others:**
  - OrganOfCorti (Aug 2014): hashrate changed 4 times; "turned his miners off for extended periods in August and September 2009".
  - BitMEX Research (2018-08-19): "Perhaps 600,000 to 700,000 bitcoin".
  - Whale Alert (2020-07-20): 1,125,150 BTC, 22,503 blocks to block 54,316.
  - TechMiX "The Mysterious 19" (2020-06-02).
  - Lopp, "Was Satoshi a Greedy Miner?" (2022-09-16): Pacific-time narrative of Jan 2009 restarts; "Satoshi's machine slept" (8.14b).
  - Wicked Bitcoin on X (2024-09-29) and Bitcoin Magazine (2024-10-01): May 2009 missing blocks, possibly testing 51% attacks.
  - Bitquery reconstruction via Cryptobriefing (2026-09-22): 1,023,352 BTC unspent (REPORTED).
  - **Blackburn et al. 2022, Fig S20 (VERIFIED):** Patoshi outages plotted with activity; inactive 06–14 UTC (8.10).
- **Not found:**
  - A systematic study correlating each Patoshi pause/restart with Satoshi's post/email/commit times.
  - A sleep schedule derived from Patoshi on/off events beyond Blackburn's Fig S20 and Lopp's Jan 2009 narrative.
  - Any "clock-skew reveals time zone" analysis. Block nTime is Unix time, so a machine's time-zone setting isn't recorded in it.

### 9(f) Code stylometry (Bitcoin 0.1 vs candidates)

| Who | Date | Compared | Result | URL | Label |
|---|---|---|---|---|---|
| Caliskan-Islam et al., "De-anonymizing Programmers via Code Stylometry" (USENIX Security) | 2015 | none | Mentions Satoshi only hypothetically | — | VERIFIED by helper |
| Tindell, Mitchell, Sprague & Wang (JMU), "An empirical study of two Bitcoin artifacts through deep learning", FC 2022 workshops | 2022 | 16 authors/libraries c.2008. Finney is represented by one file (`bc_key`, 2011). **Back and Sassaman are not included.** | 89.1% validation accuracy; v0.1 "likely produced by multiple authors and Hal Finney is not one of them" | https://fc22.ifca.ai/preproceedings/31.pdf | VERIFIED by helper |
| Adebayo & Yampolskiy, "Estimating the Identity of Satoshi Nakamoto using Multimodal Stylometry", IEEE BigData 2024 | 2024-12-15 | unknown | abstract not accessible | DOI 10.1109/bigdata62323.2024.10826132 | REPORTED |
| Amir Taaki, X post | 2024-10-09 | Impressions | "Satoshi is not a programmer" … Hungarian notation, locks, Windows, "indicate an older person … We can find him by comparing his code with others, but no one did that yet." | https://x.com/.../1844017533336142025 | VERIFIED by helper |
| Taaki to Benjamin Wallace (book, 2025, p. 27 per Tapon) | 2025 | Back vs Satoshi | "Adam has a consistent style across his projects. His style does not match Satoshi's." | (book) | REPORTED |
| Wallace, *The Mysterious Mr. Nakamoto* | 2025-03-18 | "text and code stylometry" per reviews | Who did the code stylometry and the results: **not found** | — | REPORTED |
| **Robert Graham**, X thread | 2026-04-09 | Hashcash source vs Bitcoin 0.1 (0xMagnuz repo) | "don't look remotely similar" (§1.4). Also "Satoshi's code … exactly the sort of code I wrote, down to using 'printf' instead of 'cout'"; the brace/space style is "non-distinctive" | x.com/robertgraham/status/2042039637984596459 (+ 2042039825058984138, 2042041533986435172, 2042042800938570173) | VERIFIED (root by me; replies by helper) |
| **whowrotebitcoin.com** (Adam Fisk) | 2026-04 | 12 code traits vs Bitcoin 0.1 | Michael Stokes (Shareaza) 11/12; Falco 9/11; Wei Dai (Crypto++) 8.5/11; Andresen 8.5/12; Le Roux (E4M) 5.5; McCaleb 4.5/11; Sassaman (Mixmaster) 4.5/9; Finney (RPOW) 2/10; **Back (hashcash) 1/10**. "Zero cypherpunk mailing list participants match Satoshi's Windows MFC C++ coding style." The site names living developers as "leads", which is speculation. | https://whowrotebitcoin.com | VERIFIED by helper |
| **MatoTeziTanka/satoshi-stylometry** (GitHub) | 2026-05-27 | Code axis: Bitcoin nov2008/0.1.0/0.1.3 vs Hashcash, RPOW, Crypto++ 5.2.1, Mixmaster, TrueCrypt 7.1a, PGP 6.5.1i, E4M 2.01, BSV | "mosaicked". Code-identifier function words: closest Back (Δ 0.78–0.80). Braces: Allman 45%, like TrueCrypt/Finney/Dai. **100% spaces, no candidate matches.** 105 line-comments/KLOC. **MFC C-prefix class names 6.4% of identifiers vs ≤0.8% for every candidate** (PGP 6.5 highest). | https://github.com/MatoTeziTanka/satoshi-stylometry | VERIFIED (README, `llm-stylometry/github-MatoTeziTanka_satoshi-stylometry-README.md`) |
| obxium, "Early Bitcoin source code characteristics" | 2026-01 | Comments | Unusual `////`, `///` comment styles; "MSVC 2005 SP1 specifically mentioned in source comment" | https://nakamoto-research.obxium.com/code-characteristics.html | VERIFIED (`metadata/obxium/code-characteristics.txt`) |
| Lopp, "Hal Finney Was Not Satoshi Nakamoto" | 2023-10-21 | RPOW vs Bitcoin | tabs vs spaces, snake_case vs camelCase, block vs line comments | https://blog.lopp.net/hal-finney-was-not-satoshi-nakamoto/ | VERIFIED by helper |

- Other remarks from people who read the code:
  - Kaminsky (New Yorker 2011): "world-class programmer".
  - Andresen (MIT TR 2014): "brilliant coder, but it was quirky".
  - Finney (Forbes 2014): "my style is completely different from Satoshi's. I program in C … I don't understand the tricks that Satoshi used."
- **Not found:**
  - A code-stylometry study commissioned by a journalist with published results (Wallace's is unpublished/unknown; the NYT did none).
  - Peer-reviewed comparisons including Back's or Sassaman's code.

---

## 10. The November 2008 pre-release source code

From the helper agent (`code-forensics/`), except where I note otherwise.

- **Satoshi's own mention** (metzdowd, Mon Nov 17 12:24:43 EST 2008, replying to James A. Donald): "the sourcecode is coming soon. I sent you the main files. (available by request at the moment, full release soon)". https://www.metzdowd.com/pipermail/cryptography/2008-November/014863.html (helper: VERIFIED)
- **Published by Ray Dillinger ("Cryddit")** on Bitcointalk, 2013-12-23, topic 382374, "Bitcoin source from November 2008": "This is the Bitcoin sources from November 16, 2008 … It is four source code files." How he got it: "Satoshi posted asking for professional crypto geeks to review his project. Hal Finney and I were two of those who answered, and he sent the archive to several of us." Also "the genesis block in this code has a different hash". https://bitcointalk.org/index.php?topic=382374.0 (helper: VERIFIED)
- **In the same thread:**
  - deepceleron quotes Satoshi's covering email ("here's the core source files attached (bitcoin_src1.rar) … main.h and main.cpp are the bitcoin system node.h and node.cpp are the peer network communications infrastructure") and hosted the rar at `we.lovebitco.in/bitcoin_src1.rar` (now Wayback only).
  - Sergio Lerner says he also had the files "sent to me by one of the early reviewers" and lists changes made after this draft.
  - Mike Hearn on the marketplace/"user reviews" code; Peter Todd on OP_CODESEPARATOR, `getmywtxes`, "atoms".
- **Where to download:**
  - Satoshi Nakamoto Institute, https://cdn.nakamotoinstitute.org/code/ (`bitcoin-nov08.rar` MD5 1de1b45c425c1cebb2b3280baffe7f25; the helper confirmed the local copy `data/releases/bitcoin-nov08.rar` matches).
  - github.com/fernandonm/bitcoin release "preview" (`bitcoin_src1.rar`, 33,657 bytes, 2019-03-19).
  - github.com/XertroV/bitcoin_src1; github.com/benjiqq/bitcoinArchive `nov08/` (2014); lugaxker/nakamoto-archive (hashes).
  - Note: trottier/original-bitcoin is 0.1.0, not the pre-release.
- **Provenance of the 0.1.0 archives (VERIFIED by me):** Hal Finney sent `bitcoin-0.1.0.rar` and `.tgz` to Marc Bevand ("mrb"), who posted them in March 2012 (Bitcointalk topic 68121; rar MD5 91e2dfa2af043eabbb38964cbf368500, SHA-256 8b17eb9a…5b56). File: `metadata/bitcointalk-68121-hal-finney-0.1.0-archives.txt`.
- **Published analyses of the pre-release:**
  - Chain Bulletin 2020 (all files 15-11-08 00:00:01; "version 0.0.0.1" under the time-as-version scheme; VERIFIED by me).
  - Jamie Redman, bitcoin.com 2019-03-14 ("timechain", coin/cent units, poker "added April 16, 2008", which the helper shows is a misreading of the wxFormBuilder version string).
  - Fiach_Dubh, Medium/Stacker News, ~2024: claims of 10,000 BTC reward and 1.99 billion coins. The helper's check of `main.h` gives ~20M coins with 6 decimal places.
  - Jason Chavannes, "Satoshi's Poker" (2026-06-25): poker UI empty; marketplace code substantive.
  - Ray Dillinger interview, ofnumbers.com (2018-10-01): he says he "freaked out" at floating point in the proof-chain code.
- **Not found:** a style/stylometry analysis aimed specifically at the Nov 2008 files, or archive-metadata work beyond Chain Bulletin's (Fox Chapel's WinRAR-version test covers "Satoshi's bitcoin .rar files" generally).

## 11. LLM / AI / modern stylometry studies, 2024–2026

| Who | Date | Method | Result | URL | Label |
|---|---|---|---|---|---|
| NYT (Carreyrou, Freedman) | 2026-04-08 | Unnamed AI model given the NYT stylebook hyphens section → 325 Satoshi hyphen errors; Cafiero function-word stylometry | Back 67 vs 38; Cafiero "inconclusive" | §1 | VERIFIED |
| Benjamin Wallace, *The Mysterious Mr. Nakamoto* (Crown) | 2025-03-18 | Home-made "Satoshitizer" (>200 "Nakamoto-isms"); "recruited a machine-learning expert and a stylometry specialist" | "we will likely never know beyond a reasonable doubt who he was". Leading lead in the NYMag excerpt: James A. Donald ("hosed", "fencible"). CoinDesk says his favourites were Finney, Szabo, Sassaman, Donald and Ben Laurie. | NYMag excerpt 2025-03-17 | VERIFIED by helper (excerpt) / REPORTED (book) |
| obxium, "Claude LLM Profile" and "Grok LLM Profile" | 2025–2026 (site v0.3.4, 2026-01-23) | Claude 3.7 Sonnet and Grok asked to profile a de-identified Satoshi corpus | Claude: late 30s–early 40s, CS background, etc. Grok leans UK/London, citing Chain Bulletin and the In Search Of Satoshi time analyses. | https://nakamoto-research.obxium.com/claude-profile.html ; /grok-profile.html | VERIFIED (`metadata/obxium/claude-profile.txt`, `grok-profile.txt`) |
| jnathan9, "Satlock" (GitHub `jnathan9/satoshi-stylometry`) | created 2026-04-10 | SVM on 126 hand-crafted features; 565 Satoshi texts vs 2,873 texts from the same 258 Bitcointalk threads | Candidate mean "Satoshi-likeness": Dai 20.4%, Finney 16.3%, Andresen 14.4%, Szabo 9.2% (Back not scored). HF demo `huggingface.co/spaces/thestalwart/satlock` ("thestalwart" is also Joe Weisenthal's X handle; ownership not verified). | https://github.com/jnathan9/satoshi-stylometry | VERIFIED (README) |
| MatoTeziTanka, `satoshi-stylometry` | 2026-05-27 | Burrows' Delta (201 function words) + code-style axes | Forum/emails → Finney (Δ≈0.90); white paper → Back (Δ 0.97, after dropping a multi-author Sassaman corpus); argues Aston 2014's Szabo result was topic-contaminated | https://github.com/MatoTeziTanka/satoshi-stylometry | VERIFIED (README) |
| ULC Legal (JUDr. Ján Čarnogurský) | 2026-03-24 | Burrows' Delta, ~13k authors | Top match Ray Dillinger (Δ 0.77); Back 0.91 but writes "can not" 17×, whereas Satoshi always writes "cannot"; Szabo 24th of 29. Oct 2024 Naive-Bayes version ranked Phil Wilson first. No LLM. | https://www.ulclegal.com/en/satoshi-nakamoto-found-cypherpunk-bitcoin/ | VERIFIED by helper |
| basvandorst/where-is-satoshi (GitHub) | 2024-04-13 | Satoshi corpus + 500k list posts, Burrows' Delta etc. | names no one | GitHub | VERIFIED by helper |
| goldmonkey21/doxer | 2021 (upd. 2024) | Random forest + unique words | "Gavin Andresen is Satoshi!" | GitHub | VERIFIED |
| Adebayo & Yampolskiy (IEEE BigData 2024) | 2024-12 | "multimodal stylometry" | not accessible | DOI above | REPORTED |
| Jamie Redman, bitcoin.com | 2026-07-14 | Asked Grok 4.3, Claude Fable 5, ChatGPT 5.6 Sol, Gemini Pro and Kimi K26 for Bayesian solo-vs-group estimates | opinion poll, not stylometry | (`theories-b/bitcoincom-chatgpt-grok-claude-satoshi.*`) | VERIFIED by helper |
| Kelsey Piper, The Argument (2026-04-21); Techdirt (2026-04-27) | 2026-04 | Claude Opus 4.7 de-anonymised Piper from 125 words | does not test Satoshi | — | VERIFIED by helper |

- **Not found:** any dedicated LLM, embedding or transformer authorship-attribution study on the Satoshi corpus with candidate comparison. arXiv API queries (`abs:Satoshi AND abs:stylometry`, `abs:Nakamoto AND abs:stylometry`, `abs:Satoshi AND abs:authorship`, `abs:"Satoshi Nakamoto" AND abs:language AND abs:model`) returned 0 results. Web queries found only the items above.
- Earlier academic work: Tindell et al. FC 2022 (code, deep learning, §9(f)); Ducrée arXiv 2206.10257 (profile, not stylometry).

---

## Checklist: has this angle already been published?

| Angle | Already published? | By whom | URL |
|---|---|---|---|
| Hyphenation-error matching (Satoshi vs mailing-list posters) | Yes (325 errors; Back 67 vs 38). **No data or code released.** | Carreyrou & Freedman, NYT, 2026-04-08 | https://www.nytimes.com/2026/04/08/business/bitcoin-satoshi-nakamoto-identity-adam-back.html |
| Synonym-less shared vocabulary | Yes (Back 521) | NYT 2026 | same |
| Sequential writing-tic filter (double space, British spelling, its/it's, "also", bugfix, e-mail/email…) | Yes (620 → 1) | NYT 2026 | same |
| its/it's confusion, sentence-final "also", "bloody", "partial pre-image", "burning", WebMoney, "proof-of-work" hyphenation | Yes | NYT 2026 | same |
| "cannot" vs "can not" as a marker against Back | Yes | ULC Legal, 2026-03-24 | https://www.ulclegal.com/en/satoshi-nakamoto-found-cypherpunk-bitcoin/ |
| Function-word stylometry (Burrows' Delta etc.) on candidates | Yes, many; results conflict | Juola/Greenberg 2014 (Finney); Aston 2014 (Szabo); Cafiero for NYT 2026 (Back ≈ Finney, inconclusive); ULC 2026 (Dillinger); MatoTeziTanka 2026 (Finney on posts, Back on white paper); basvandorst 2024 | see §§5, 6, 11 |
| LLM/transformer authorship attribution with a candidate ranking | **Not found** (only LLM "profiles" and opinion polls; one SVM "Satlock") | obxium (Claude/Grok profiles); bitcoin.com 2026-07-14 poll; jnathan9 Satlock 2026-04 | §11 |
| Back's silence on lists during Satoshi's tenure / first Bitcoin comment ~6 weeks after Satoshi left | Yes | NYT 2026 (also partly Barely Sociable 2020) | NYT; https://www.youtube.com/watch?v=XfcvX0P1b5g |
| Back's 1997–1999 posts prefiguring Bitcoin (b-money + hashcash, difficulty increase, energy argument) | Yes | Barely Sociable 2020; NYT 2026 | same |
| Back joining Bitcointalk the day of Lerner's post; the "stop in Nakamoto's interests" comment | Yes | Barely Sociable 2020; HBO 2024; NYT 2026 | https://bitslog.com/2013/04/24/ (comment) |
| "Emails to himself" theory about the Aug 2008 Back–Satoshi emails; request for their metadata | Yes (metadata never provided) | NYT 2026 | NYT |
| Back's code vs Satoshi's code | Yes (says they don't match) | Robert Graham (X, 2026-04-09); whowrotebitcoin.com (Back 1/10); Taaki via Wallace 2025; MatoTeziTanka 2026 (identifier-level closest = Back) | §9(f) |
| Satoshi's MFC/Windows-C++ fingerprint (C-prefix classes, Hungarian notation) | Yes | whowrotebitcoin.com 2026; MatoTeziTanka 2026; Taaki 2024; Graham 2026 | §9(f) |
| Posting-hour histogram of Bitcointalk posts | Yes | Stefan Thomas 2011; Wired 2011; many since | https://bitcointalk.org/index.php?topic=37743.0 |
| Combined posts + commits + emails time-zone scatter charts | Yes | Chain Bulletin 2020-11-23; Lopp 2019 and 2025; COPA (Sydney time) 2024 | §8 |
| Weekend pattern | Yes (gap holds on weekends) | Stefan Thomas / Wired 2011 | https://www.wired.com/2011/11/mf-bitcoin/ |
| Seasonal/term-time pattern (student hypothesis), Christmas-2009 gap | Yes | In Search Of Satoshi, 2018-02-13 | https://medium.com/@insearchofsatoshi/the-time-zones-of-satoshi-nakamoto-aa40f035178f |
| US or UK holiday (Thanksgiving, bank holidays) activity analysis | **Not found** | — | — |
| SVN commit times as time-zone evidence | Yes. The "BST offsets" claim is likely a viewer-TZ artifact (my inference); Chain Bulletin used UTC. | In Search Of Satoshi 2018; Chain Bulletin 2020; bitcoin.com 2026 (reversed) | §8 |
| Patoshi downtime combined with Satoshi activity to find a sleep window | Yes (inactive 06–14 UTC; "North or South America") | Blackburn … Lieberman Aiden, arXiv 2206.02871 (2022), Fig S20; Lopp 2022 (Jan 2009 Pacific narrative); Finding Satoshi 2026 (6am–10pm Pacific) | https://arxiv.org/abs/2206.02871 |
| Systematic correlation of every Patoshi pause/restart with Satoshi's posts | **Not found** (only partial) | — | — |
| Patoshi pattern / single machine / 5 threads / ~1.1M BTC | Yes | Lerner 2013–2020; Whale Alert 2020; BitMEX 2018; Lopp 2022 | https://bitslog.com |
| White-paper PDF metadata (OpenOffice 2.4, CreationDate −07'00' Oct 2008 / −06'00' Mar 2009) | Yes | Lerner 2014; In Search Of Satoshi 2018; Chain Bulletin 2020; obxium 2026; COPA judgment §492 (2024) | §9(a) |
| PDF `/Lang (en-GB)` | Yes | obxium 2026 | https://nakamoto-research.obxium.com/whitepaper.html |
| Brute-forcing the PDF /ID MD5 for a Windows username | Yes (proposed 2014; attempted at scale 2026; no hit) | Lerner 2014; Fox Chapel Research + tmctmt 2026-05-21 (code published) | https://foxchapelresearch.substack.com/p/how-you-probably-will-find-satoshi |
| Unpatched pre-2007 US-DST rules as the explanation for the PDF offsets | **Not found** | — | — |
| Release-archive file timestamps as a version scheme (01:00 = 0.1.0 …); "0.1.0" is really 0.1.1 | Yes | Chain Bulletin (Stefanov) 2020-11-19 | https://chainbulletin.com/satoshi-used-timestamps-for-early-bitcoin-source-code-versioning |
| RAR folder mtimes (untouched, 64-tick Windows XP timer); WinRAR < 3.62 | Yes | Chain Bulletin 2020 (values); Fox Chapel 2026 (timer, WinRAR version; notes times are local, no UTC normalisation) | as above |
| PE compile timestamp of bitcoin.exe 0.1.0 (2009-01-10 23:16:00 UTC), MinGW gcc 3.4.5 | Yes (as a data point) | obxium, "Early Bitcoin binary analysis notes", 2026-01 | https://nakamoto-research.obxium.com/binary-analysis.html |
| **Deriving Satoshi's time zone by comparing RAR local folder times with the PE UTC timestamp** | **Not found** (ingredients published separately; nobody combined them) | — | — |
| Tar uname/gname in release tarballs | Only for the Hal-made 0.1.0 tgz ("hal/hal"); nothing for later Satoshi-built tarballs | Chain Bulletin 2020 | as above |
| Embedded build/PDB paths in bitcoin.exe | **Not found** (only "stripped to external PDB") | obxium | as above |
| Satoshi PGP key (DSA-1024, 2008-10-30, GnuPG 1.4.7 MingW32, hash prefs 2,8,3) | Yes (as contrast to Wright's backdated keys) | Sarah Jeong, Motherboard, 2015-12-09; Gwern & Greenberg, Wired 2015 | https://www.vice.com/en/article/satoshis-pgp-keys-are-probably-backdated-and-point-to-a-hoax/ |
| anonymousspeech/vistomail headers (Received 124.217.253.42, Chilkat, +0800) | Yes | metzdowd thread Nov 2020 (Atkins, Markowitz); CoinDesk/Kapilkov 2020; Chain Bulletin 2020 | §9(d) |
| **GMX (Malmi) Date-header offsets switching on EU/UK DST dates** | **Not found** (helper's own tabulation; needs verification) | — | https://mmalmi.github.io/satoshi |
| GMX Received headers / Tor exits | **Not found** | — | — |
| Southern-California IP (68.164.57.219, Covad) from Finney's Jan 2009 debug log | Yes (disputed; NYT calls it a dead end) | whoissatoshi.wordpress.com 2016; Lopp 2023; Cryptobriefing 2026 | §9(d) |
| Finney 10-mile race alibi (2009-04-18) | Yes | Lopp 2023 (credits Blackburn/Aiden) | https://blog.lopp.net/hal-finney-was-not-satoshi-nakamoto/ |
| Jack Dorsey timestamp alibis | Yes | Lopp 2025 | https://blog.lopp.net/jack-dorsey-is-not-satoshi-nakamoto/ |
| Peter Todd alibi photos | Yes (photos not public; not forensically checked) | Wired 2024-10-22 | Wired |
| Szabo bit-gold re-dating (2005 post re-dated to Dec 2008 as a "rerun") | Yes | Skye Grey 2013; Popper NYT 2015; Makgill/bitcoin.com 2020 | §6 |
| Massias/Quisquater citation → Leuven → Sassaman | Yes | Ducrée arXiv 2206.10257 (2022); Hatch update 2024; Global Security Mag 2024; Clark 2024; Miller 2026 | §4 |
| Sassaman blockchain tribute (block 138725, Kaminsky/Goodspeed) | Yes | Kaminsky, Black Hat 2011 | §4 |
| Finney + Sassaman two-person theory | Yes | "Finding Satoshi" film 2026-04-22 (earlier floated by others) | https://findingsatoshi.com |
| Nov 2008 pre-release code: provenance and download | Yes | Ray Dillinger, Bitcointalk topic 382374 (2013-12-23); SNI; fernandonm GitHub | §10 |
| Style or metadata analysis specific to the Nov 2008 code | Minimal (Chain Bulletin timestamps; bitcoin.com 2019; Fiach_Dubh 2024, partly wrong) | — | §10 |
| Aug 2015 "Satoshi" email vs Back's block-size language | Yes | Barely Sociable 2020; NYT 2026 | — |

### Notes for whoever uses this
- The richest prior work on **timestamps and metadata** is: Chain Bulletin (Nov 2020, three articles), In Search Of Satoshi (Feb 2018, two articles), Lerner's Bitslog (2013–2020), Blackburn et al. (2022), obxium Nakamoto Research (2026), and Fox Chapel Research (May 2026). Anything about RAR/PE/PDF timing must be checked against these before being called new.
- Beware duplicated or garbled claims in secondary compilations. Examples: the bitcoin.com / cryptonews "25 facts" (reversed SVN offsets), the Aston release saying the paper was LaTeX, and Fiach_Dubh's "1.99 billion".
- Another agent's folder `data/prior-research/forensics/` (not created by me) contains overlapping HTML copies.
