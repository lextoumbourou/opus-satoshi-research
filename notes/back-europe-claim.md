# Back (Apr 2026): "the documentary ruled out very early anyone in europe given the time of forum posts". Reconciling it with the UK-time machine finding

## What Back actually said (VERIFIED)
- Tweet by @adam3us, **2026-04-24 10:57:32 UTC**, id 2047631019612795092 (`data/claims/A-back-tweet-2047631019612795092.json`), replying to @WillPrice:
  > "the documentary ruled out very early anyone in europe given the time of forum posts. and len was ... in europe, at KU Leuven, Belgium doing a PhD from 2004 until he died in 2011. so how does it make sense for that last minute "patch" if Len was doing the writing."
- U.Today (Fri 24 Apr 2026 13:48) paraphrases this as "the timing of Satoshi's forum posts does not align with Sassaman's European daily schedule" (`data/claims/A-utoday-back-timezone-2026-04.txt`).
- It's Back relaying the *Finding Satoshi* documentary's reasoning and using it against a Sassaman role, not an analysis of his own. The documentary's method is REPORTED (I haven't seen it).

## The two findings measure different things
| | What it measures | Result |
|---|---|---|
| Forum/email **activity hours** | When the person was at the keyboard | Active ~15:00–03:00 UTC; quiet **06:00–14:00 UTC** (2.8% of 887 events) |
| **Machine clock settings** (Thunderbird Date vs Message-ID, `diff` output, release archives) | How the computers were configured | UK civil time with EU DST switching, 2009–2010 |

They are compatible. They constrain the person differently:
- **In UK time** Satoshi was active ~16:00–04:00 (summer) and never 07:00–15:00. That's a night-owl, or "busy all day, online evenings and nights", schedule. Unusual, but ordinary for students, freelancers and programmers. His exceptions fit it: weekend/summer-holiday afternoons from ~13:00 UTC, a Sunday-morning post (5 Dec 2010, 09:08 GMT), and the Easter-week morning emails of April 2011 (`notes/2011-break.md`).
- **In Belgian/Maltese time (CET/CEST)** the same pattern is active until ~05:00 local and silent 08:00–16:00. That's a harder fit, and the machines weren't on CET anyway.
- **In US time** the pattern looks like normal waking hours (Pacific: ~08:00–20:00). That's why timing analysts, and apparently the documentary, lean American.

## Reconciliation (INFERENCE)
1. **"Ruled out anyone in Europe" is too strong.** Hours can rule out a European keeping *ordinary daytime* hours, not Europeans in general. A UK night owl fits both the hours and the clock settings. A US resident fits the hours but needs an extra assumption for the clocks: a deliberately UK-set mail machine, or a remote UK box (cf. the Gavin control, which shows London-time build boxes exist).
2. **Behavioural DST evidence** (`notes/dst-behaviour.md`) tips slightly toward Europe. Satoshi's *routine* had shifted to winter time in the last week of October 2009, when the UK had changed clocks and the US hadn't. EU beats US rules by 1.9–4.3 log-lik units, but on one autumn week. Low-to-medium. A US-resident Satoshi would have to keep his routine on UK clock-change dates as well as his machines.
3. **Where Back's argument does bite:** against **CET-based** candidates as the day-to-day operator, which means Sassaman (Leuven) *and Back himself* (Malta from 2009). Satoshi's machines ran UK time, not CET. On 1 Dec 2010 and 25 Jan 2011 Back's own emails carry +0100 while Satoshi's carry +0000 (VERIFIED, `notes/timezone-evidence.md`). Back's argument against Sassaman applies equally to himself.
4. **Back's own rhythm:** 30.1% of his 2010–15 randombit posts fall at 05:00–10:59 UTC vs 4.4% for Satoshi (`scripts/hour_compare.py`). An extended test (Bitcointalk, bitcoin-dev, 1996–98 cypherpunks) is in progress.
5. **For the collective theory:** Back is right that a Belgium-based Sassaman as the *main online operator* sits badly with the hours. He'd be posting until 04:00–05:00 local and never before ~16:00. It also sits badly with the clocks (UK, not CET). A UK-based or US-based operator, possibly with others contributing text or code offline, is not addressed by his point.

## Novelty
Back's statement is public; the reconciliation (hours vs clock settings, and applying CET to Back himself) is mine. The UK-time machine finding is not found published (`notes/prior-art-search.md`).
