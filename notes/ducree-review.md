# Ducrée, "Satoshi Nakamoto and the Origins of Bitcoin" (arXiv 2206.10257v14, 9 Sep 2022): read and citation check

Read in full: main text, lines 1–3717 of `data/prior-research/theories-a/ducree-arxiv-2206.10257v14.txt`. The numerology/parameter chapters were skimmed. About 2,000 references; the ones behind claims that bear on candidates, location or the white paper were checked against primary sources. Labels: **VERIFIED**, **REPORTED**, **INFERENCE** (with confidence).

## Headline finding: Satoshi's bibliography can be traced to online sources, so the "Benelux attendance" inference fails

Ducrée's central, most distinctive argument is this (p. 19–22):
- Reference [2] of the white paper was printed only in the proceedings of a small regional symposium.
- Electronic copies "do not appear to have been available online … prior to the release of the Bitcoin whitepaper in 2008".
- So "Satoshi Nakamoto could not have just accidentally 'stumbled across' citation (2); either himself, or at least someone close to him, must have personally attended this symposium … in Haasrode".
- Also, (2) supposedly "provided (3–5)" (his "(2)&(6)-first" hypothesis).
- It feeds his Benelux/KU Leuven profile, his "hard fact" question #2, the Sassaman section, and his exclusion of Finney, Dai and Szabo ("it is thus hard to believe that Hal Finney, Wei Dai, or Nick Szabo would have found, and then included (2)").

What the archives show:

1. **The paper was freely downloadable from UCL's public web site before 2008.** VERIFIED (Wayback raw captures in `data/wayback/ucl-crypto/`):
   - UCL Crypto Group `publications.html` listed "Design of a secure timestamping service with minimal trust requirement … Proceedings of the 20th symposium on Information Theory in the Benelux, pp. 79-86, May 1999" from the **22 Sep 1999** capture onward.
   - A **[PS] download link** (`publications/1999/ITBenelux.ps`) appears from the **2 Aug 2002** capture onward.
   - The file itself was captured **10 Oct 2003** (`ITBenelux-1999-wb20031010.ps`).
   - After a site rebuild, the same paper was at `crypto/files/publications/ps113.ps`, captured **24 Aug 2007** (`ps113-wb20070824.ps`). Both files are byte-identical (sha256 `fa7587db…579a3d`): 8 pages, dvips of `/home/massias/TIMESEC/article/STA.ps`, TeX output 1999-04-09.
   - The 2012 and 2016 listings still link it (as `pdf113.pdf`).
2. **CiteSeer indexed it.** VERIFIED (`data/wayback/citeseer/`): `citeseer.ist.psu.edu/massias99design.html`, captured 1 Dec 2004, 20 May 2007 and 14 Feb 2008, with "View or download: dice.ucl.ac.be/crypto/pu…ITBenelux.ps" and cached PS/PDF copies.
3. **Satoshi's reference [2] is word for word the authors' own self-citation, not the paper's title page.** VERIFIED text comparison:

   | Source | Authors | Title ending | Venue |
   |---|---|---|---|
   | Paper title page (1999) | H. Massias, **X. Serret Avila**, J.-J. Quisquater | "minimal trust **requirement**" | – |
   | UCL publications page (1999–2006) | Henri Massias, Xavier Serret … | "requirement" | "Proceedings of the 20th symposium … pp. 79-86, May 1999" |
   | Massias et al., WETICE 1999 (Stanford), ref [4] (`WetICE-1999-wb20060118.pdf`, on UCL's site 2002–2006, also in IEEE's proceedings) | "H. Massias, **X. S. Avila**, and J.-J. Quisquater." | "minimal trust **requirements**." | "accepted at the 20th Symposium on Information Theory in the Benelux, May 1999." |
   | CiteSeer page, "BibTeX entry" line (2004–2008) | "H. Massias, **X. S. Avila**, and J.-J. Quisquater." | "**requirements**." | "accepted at the 20th Symposium on Information Theory in the Benelux, May 1999." |
   | **White paper [2]** (Oct 2008 draft and final) | "H. Massias, **X.S. Avila**, and J.-J. Quisquater," | "minimal trust **requirements**," | "In 20th Symposium on Information Theory in the Benelux, May 1999." |

   Satoshi's version carries both errors from the WETICE/CiteSeer string: "X.S. Avila" (treating the surname "Serret" as a middle initial) and the plural "requirements". It also shares the omission of page numbers and the exact venue wording. It differs only by "accepted at the" → "In" and his own quote/comma style.
4. **Satoshi's references [3], [4] and [7] match the reference list of his reference [5]**, Haber & Stornetta, "Secure Names for Bit-Strings" (1997). VERIFIED (`data/wayback/haber/wb20000815233629-HS-SureID.ps`, on Stuart Haber's web site `www.star-lab.com/haber/`, captured Aug 2000; also on CiteSeer):
   - [HS 91] "S. Haber and W.S. Stornetta. How to time-stamp a digital document. Journal of Cryptology, Vol. 3, No. 2, pp. 99–111 (1991)." Satoshi: "S. Haber, W.S. Stornetta, "How to time-stamp a digital document," In Journal of Cryptology, vol 3, no 2, pages 99-111, 1991."
   - [BHS 93] "D. Bayer, S. Haber, and W.S. Stornetta. Improving the efficiency and reliability of digital time-stamping. In Sequences II: Methods in Communication, Security, and Computer Science, … pp. 329–334, Springer-Verlag, New York (1993)." Satoshi: "…In Sequences II: Methods in Communication, Security and Computer Science, pages 329-334, 1993."
   - [Merk 80] "R.C. Merkle. Protocols for public key cryptosystems. In Proc. 1980 Symposium on Security and Privacy, IEEE Computer Society, pp. 122–133 (April 1980)." Satoshi's [7] is identical in content and word order.
   - By contrast, the Massias Benelux paper cites these works as "3(2):99–112", "Sequences'91 … 1992" and "timestamp(ing)" without the hyphen, and doesn't cite Merkle at all. So **[2] did not "provide (3–5)"**. Ducrée noticed the 111/112 and 1992/1993 differences but read them as Satoshi "taking a closer look". The simpler reading is that Satoshi took them from Haber & Stornetta's own list.
   - [5] itself matches CiteSeer's and Haber's rendering ("In Proceedings of the 4th ACM Conference on Computer and Communications Security, pages 28–35, April 1997"). Massias has "Communication Security … ACM Press".
5. **Reading of the evidence.** INFERENCE (high):
   - The white paper's timestamping references were assembled from online sources available to anyone by 2007: the Haber/Stornetta paper on Haber's site, and the Massias WETICE self-citation (UCL site, IEEE, or CiteSeer).
   - That is a natural trail for someone searching CiteSeer or Google Scholar for timestamping work in 2007–08. The CiteSeer page for [2] lists exactly [3], [4] and [5] as its citations, and links to Haber's copies.
   - Satoshi need not have read the printed proceedings, or even the Benelux paper itself.
   - Ducrée's geolocation inference ("Benelux", "KU Leuven library"), his "hard fact #2", and his use of it to exclude US-based candidates therefore have no support.
   - **For the user's theory:** this removes the argument Ducrée uses against Finney and Szabo, and the special KU Leuven route he proposes for Sassaman. Anyone with a web browser could have built this bibliography. (Side note: Back's own 2002 hashcash paper cites a CiteSeer URL, showing he used CiteSeer, which was normal for the field. Weak.)
6. **Competing source hypothesis: the Springer encyclopedia (Clark via Miller, Apr 2026).** Haber & Massias, "Time-stamping", *Encyclopedia of Cryptography and Security* (Springer 2005, ed. van Tilborg; `data/prior-research/citations/springer-ecs-2005-time-stamping.txt`) lists four of Satoshi's five timestamping refs ([2], [3], [4], [7]; not [5]). Feature check, VERIFIED text comparison:

   | Distinctive feature in Satoshi's list | WETICE/CiteSeer string | Haber & Stornetta 1997 list | Springer 2005 entry | Massias Benelux paper |
   |---|---|---|---|---|
   | [2] "X.S. Avila" | ✓ "X. S. Avila" | – | ✗ "X. Serret Avila" | ✗ "X. Serret Avila" |
   | [2] plural "requirements" | ✓ | – | ✓ | ✗ |
   | [2] "20th Symposium…", no page numbers | ✓ | – | ✗ "Twentieth…", pp. 79–86 | – |
   | [3] "vol 3, no 2, pages 99-111" | – | ✓ "Vol. 3, No. 2, pp. 99–111" | ~ "3 (2), 99–111" | ✗ "3(2):99–112" |
   | [3]/[4] hyphenated "time-stamp(ing)" | – | ✓ | ✓ | ✗ |
   | [4] "Sequences II … 1993" | – | ✓ | ✓ | ✗ "Sequences'91 … 1992" |
   | [7] "In Proc. 1980 Symposium on Security and Privacy, IEEE Computer Society, pages 122-133, April 1980" | – | ✓ (identical, incl. "April 1980") | ~ "Proceedings of the 1980 Symposium … IEEE Computer Society Press, Los Alamitos, CA, 122–133" (no month) | not cited |
   | [5] "…Computer and Communications Security, pages 28-35, April 1997" | ✓ (CiteSeer record) | (is [5]) | not cited | ✗ "Communication Security … ACM Press" |

   INFERENCE (medium-high): Haber & Stornetta 1997 for [3], [4], [7], plus the WETICE/CiteSeer string for [2] (and CiteSeer's record for [5]), fits every distinctive feature. The encyclopedia fits "requirements" and "Sequences II/1993" but misses "X.S.", "20th", the no-pages form, "vol/no" and "April 1980". Either way, every candidate source was online before 2008.
7. **Novelty.**
   - **Already published:**
     - Rosario (Medium, 1 Nov 2018) links the paper on UCL's current site.
     - Peter Miller (Medium, 13 Apr 2026; `data/prior-research/sassaman/miller-2026-04-13-…txt`) noted the plural "requirements" and the missing page numbers ("Maybe he did not have access to the paper, at all"). He relayed Jeremy Clark's suggestion that Satoshi took it from an online encyclopedia entry.
     - The opposite claim ("print-only … until 2020", a Sassaman/KU Leuven clue) was pushed on X by David Seroy and Nic Carter in April 2026 (REPORTED via `data/prior-research/sassaman/eventhorizoniq-…txt`).
   - **Not found published:**
     - That the Benelux paper itself was downloadable from UCL 2002–2007 and on CiteSeer 2004–2008, directly falsifying "print-only".
     - The exact WETICE/CiteSeer string match ("X. S. Avila", no pages, "20th").
     - The Haber & Stornetta 1997 list as the source of [3], [4], [7].
     - The feature comparison showing the Springer entry is a weaker fit.
   - Searches: 6 web queries plus the Miller/Substack threads, 2026-09-26.

## The Bank of Japan/IMES lead (Quisquater 2017, via Ducrée)

Ducrée reports that Quisquater's 2017 talk found a "stunning intersection" between the references of Une, "The Security Evaluation of Time Stamping Schemes" (IMES DP 2001-E-18) and the white paper's. VERIFIED (`data/prior-research/citations/01-E-18.pdf`, reference list pp. 33–34):
- The IMES paper does **not** cite the Massias Benelux paper, Bayer-Haber-Stornetta, "Secure names", Merkle 1980, Feller, Back or Dai.
- Its only overlap with the white paper is Haber & Stornetta 1991.
- It does cite the TIMESEC technical reports, with the co-author as "J. S. Avila", another instance of the same name mangling.
- INFERENCE (high): the IMES report was not Satoshi's source. (I haven't watched the 2017 video, so this checks Ducrée's summary against the document, not Quisquater's exact words.)

## Other claims checked

| Ducrée claim | Check | Label |
|---|---|---|
| Feller ref (8) is "the first, 1957-edition", an "antique" found only in a few libraries, perhaps a family heirloom | The 1957 printing is the **2nd edition**. Vol. I was first published in 1950 (Open Library; Internet Archive items `introductiontopr01fell` 1950, `introductiontopr0001fell_edi2` 1957). The 2nd edition was the current one until 1968 and is widely held. | VERIFIED error |
| PDF "Created: 24/03/2009 18:33:15" shows a 7-hour offset from −06:00, "suggest[ing] Central European Time" | 11:33:15 −06:00 = 17:33:15 UTC. A viewer displaying 18:33:15 is rendering in UTC+1, i.e. **the reader's own zone** (Dublin in summer = IST, when Ducrée wrote). The same artefact as the svn-log reader-timezone issue. | VERIFIED arithmetic; INFERENCE (high) |
| P2P Foundation profile (birthdate 5 Apr 1975) "populated … in 2012, i.e., after he disappeared" | Wayback: no age shown on 2 Jul and 15 Aug 2010; "**35, Male, Japan**" on 17–18 Mar 2011; "36" from 20 May 2011. So the 5-Apr-1975 birthdate was displayed **by 17 Mar 2011**, while Satoshi was still emailing developers. Whether he added it between Aug 2010 and Mar 2011 or Ning changed its template isn't established (no control profile found). | VERIFIED (`data/wayback/p2pfoundation/`) |
| Patterson tweet ("Bitcoin isn't ready for prime time yet, according to its creator") shows inside knowledge: "How would she have been able to 'know'…?" | Tweet ID 12163582133276672 decodes to **2010-12-07 15:16:38 UTC**. Satoshi's public forum post "No, don't 'bring it on'. The project needs to grow gradually … Bitcoin is a small beta community in its infancy" was **2010-12-05 09:08:08 UTC**, 54 h earlier, in a much-discussed WikiLeaks thread. | VERIFIED times; INFERENCE (high): public source |
| Satoshi "entirely disappeared from newsgroups on 07 December 2010" | Corpus has forum posts 8, 9 and 10–12 Dec 2010 and the 0.3.18 release (8 Dec). | VERIFIED error |
| Back's hashcash (2002) cites a personal communication with Hal Finney | "[6] Hal Finney. Personal communication, Mar 2002." (also Boschloo [7]), for the fixed-target improvement. | VERIFIED (`data/claims/B-hashcash-2002.txt`) |
| Mixmaster code shows "knowledge of C++ plus … Win32 API were the basis for the first Bitcoin version" (anonymous tip) | Mixmaster 3.0.0 source (`data/candidates/sassaman-mixmaster/mixmaster_3.0.0.orig.tar.gz`): 38 `.c`, 7 `.h`, **no C++ files**; it does ship 6 Visual Studio `.vcproj` files (Win32 builds). So C with Win32 build support, not C++. Win32/Visual Studio experience was common. | VERIFIED; "C++" part wrong |
| Sassaman published at the WIC Benelux symposium in 2007 (with Patterson) and 2008 (with Preneel, Leuven) | Plausible for a COSIC student; not independently verified (DBLP blocked by anti-bot page). Moot for the citation route after the finding above. | REPORTED |
| Genesis block 18:15 UTC 3 Jan 2009; block 1 02:54 UTC 9 Jan 2009 | Match the block headers (`data/blockchain/headers_0_60479.csv`). | VERIFIED |
| White paper posted 14:10 EDT, 31 Oct 2008 | pipermail server time; = 18:10 UTC. | VERIFIED |
| "Mountain Time zone in mid-March 2009" from PDF −06'00' | Offset VERIFIED (long published). −06:00 on 24 Mar 2009 is also CST in places without DST that day (Saskatchewan, most of Central America; Mexico didn't switch until 5 Apr 2009). "Mountain" isn't unique. | VERIFIED / INFERENCE |

## What Ducrée's paper does and doesn't add for the collective theory

- His candidate filter rests heavily on the Benelux-citation argument, which fails (above). His other filters are numerology (cross-sums equal to 21, 1957↔1975), speculation (biblical founding myth, Bobby Fischer), and style.
- His Sassaman case is mostly Evan Hatch (2021) plus the KU Leuven proximity. The genuinely checkable items are the hashcash Finney acknowledgement and Pynchon Gate/Black Hat 2007 citing Back. They show a connected cypherpunk network (Back ↔ Finney ↔ Sassaman), which is already well known and says nothing about authorship.
- He concedes that the Sassaman postings and tweets, and Patterson's denial, "substantially taint" the hypothesis. His only positive "inside knowledge" item (the Patterson tweet) is explained by a public post two days earlier.
- **Net effect on the user's theory:** it neither supports nor refutes the collective. It removes one supposed "Europe/Benelux" pointer (the citation) and leaves the UK-time machine settings as the main location evidence.
