# The 2011 time-of-day break, and Hearn's display time zone

Script: `scripts/check_2011_break.py` → `data/satoshi/check-2011-break.txt`. Labels: **VERIFIED** (computation or source text), **REPORTED**, **INFERENCE** (with confidence).

## The observation (as put to me)

The user's version: "22 of 912 timed items in 2008-2010 fall between 07:03 and 14:37 UTC (2.4%), but 4 of the 11 in 2011 do … about 1e-4 by chance". The 07:03–14:37 window was drawn around the 2011 points, so I re-tested with a window fixed from the 2008–2010 data alone.

- **Base:** 887 events 2008–2010 whose UTC time is explicit or verified. The quietest 8-hour window is **06:00–14:00 UTC**, holding **25/887 (2.8%)**.
- **2011 (Jan–Apr):** 11 timed items; **4 fall in that window**: 7 Jan 12:00 (Hearn), 20 Apr 09:39 (Hearn), 23 Apr 13:40 (Hearn), 26 Apr 08:29 (Gavin). Binomial P(≥4 | 11, 0.028) = **1.8 × 10⁻⁴**.
- **Window-free check:** the mean KDE log-density of the 11 items under the base rhythm is −3.75. Only **5 in 100,000** random 11-item draws from the base (leave-one-out) are as low (**p ≈ 5 × 10⁻⁵**).
- VERIFIED computation. The anomaly isn't an artefact of the post-hoc window.

## Is it an artefact of Hearn's time zone? Mostly no

- Hearn's dumps (plan99.net and pastebins; Gmail "forwarded message" blocks) give naive times like "Wed, Apr 20, 2011 at 11:39 AM" with no zone. The corpus assumed Zurich. Hearn worked for Google in Zurich (REPORTED: LinkedIn location; COPA witness statement). The 2009 thread was forwarded on "Thu, May 2, 2013 at 10:02 AM".
- **Calibration:** 9 of Satoshi's 2009–2010 emails to Hearn sit in the same forwards. I scored their UTC times under Satoshi's independent base rhythm for every display offset from UTC−12 to +12.
  - Best fit: **UTC+2 / UTC+1** (Zurich summer/winter). Plateau: UTC−2 … +6.
  - **US displays are strongly rejected**: Eastern −4 scores 0.9 lower per item; Pacific −7/−8 scores 1.7–2.3 lower. VERIFIED computation. Zurich is supported; a US-Pacific Gmail default, the one plausible zone that would have moved the 2011 items into Satoshi's normal evening, is ruled out. (This assumes the 2011 threads were forwarded with the same display zone as the 2009 thread.)
  - Across the plausible offsets, 20 Apr lands at 05:39–13:39 UTC (always in or next to the quiet window). 7 Jan lands at 07:00–15:00. 23 Apr lands at 09:40–17:40 (in the window only for offsets ≥ +1).
- **Gavin's 26 Apr item is independent of Hearn.** His 2011 reply quotes "On Tue, Apr 26, 2011 at 4:29 AM"; his blog header shows "26 Apr 2011, 10:29". The six-hour gap fits EDT + CEST, giving **08:29 UTC**. If his Gmail had been left on a Pacific default it would be 11:29 UTC; still in the window. VERIFIED quotes; INFERENCE (high) that it's a morning-UTC email.
- **Caveats:**
  - Three of the four come from one correspondent's display-time dump (one shared assumption).
  - Only 3 of the 11 2011 items have an explicit zone (Malmi/Gavin, 6 Jan 18:31, 25 Jan 18:34, 22 Feb 19:49, all normal).
  - n = 11.

## What the base pattern looks like at those hours

- In 2008–2010 the deep quiet (**07:40–12:40 UTC**) has only **three** events:
  - 13 Jan 2009 07:39 (Tue);
  - 21 Nov 2009 07:02 (Sat);
  - **Sun 5 Dec 2010 09:08/09:29**: the WikiLeaks appeal ("No, don't 'bring it on'"), a special occasion on a Sunday.
- The other 07:00–15:00 events are 12:43–14:59 UTC, mostly **weekends and July–August 2010**. VERIFIED list in the output file.
- 2011's unprecedented items are **weekday mornings**: Wed 20 Apr 09:39 and Tue 26 Apr 08:29 UTC. They fall in the **UK Easter holiday**: Good Friday 22 Apr, Easter Sunday 24 Apr, Easter Monday 25 Apr 2011, with school and university vacations around them. 7 Jan (Fri) is before most UK university terms resumed. Sat 23 Apr 13:40 is a Saturday, like the base weekend events. VERIFIED dates.

## What it means (INFERENCE)

1. **Something changed in Satoshi's routine in April 2011**, exactly around the farewell emails: "I've moved on to other things" (Hearn, 23 Apr) and handing over the alert key (Gavin, 26 Apr). Medium-high confidence that it's real, given the independent Gavin anchor.
2. **Location reading.**
   - For a **UK-based** Satoshi these are 09:29–10:39 BST emails on holiday weekdays. That's mundane if his normal weekday daytime was occupied (job or studies), and consistent with the Sunday-morning WikiLeaks post and the summer-weekend afternoons.
   - For a **US-based** Satoshi they would be pre-dawn (04:29–05:39 EDT; 01:29–02:39 PDT), inside what the base pattern marks as his sleep.
   - So the break fits the UK reading more easily. Low-to-medium, and it depends on the "quiet window = working day" interpretation.
3. **For the collective theory.** A different person writing the final emails would also produce a timing break. It isn't required, and the content shows control of Satoshi's accounts and alert key. The break is compatible with a hand-over but doesn't show one. Low.
4. **Candidates.** None is directly implicated. Sassaman (Leuven, CET) would have been at 10:29–11:39 CEST, Back (Malta) likewise, Finney (California) at 01:29–02:39 PDT. The break doesn't discriminate between the Europeans. (Finney had ALS, diagnosed 2009; REPORTED.) The timing doesn't test him.

## Novelty

The posting-time pattern and the Mar–May gap were published before (Sean Thomas 2011; In Search of Satoshi 2018; Chain Bulletin 2020). I found no published analysis of the 2011 shift, the Hearn display-zone calibration, or the Easter-week timing of the farewell emails. Not found published (checked against my prior-research survey; no dedicated search beyond it). Treat as new but minor.
