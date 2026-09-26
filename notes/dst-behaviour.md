# Did Satoshi's *behaviour* follow EU or US clock changes? (DST-rule likelihood)

Scripts: `scripts/dst_likelihood.py`, `scripts/dst_placebo.py`. Data: 902 timed Satoshi events 2008-08 → 2011-04 (forum, SVN, emails, list posts; zone explicit or verified).

Method: for each candidate civil zone, convert events to local hour (with that zone's DST rules), fit a wrapped-Gaussian KDE, and compute leave-one-out log-likelihood. A routine anchored to local clock time is best explained by the zone whose DST rules match it. Zones that differ by a constant offset differ in likelihood only through events in the weeks when their DST states differ.

Results (VERIFIED computation; INFERENCE on meaning):
- **DST-observing zones beat fixed UTC by 12–20 log-lik units** at every bandwidth (0.4–2.0 h). Satoshi's activity pattern shifted with DST. Fixed-offset regions are strongly disfavoured, including Japan and most of Asia.
- **EU rules (London/Lisbon/Paris identical) beat US rules by 1.9–4.3 units** depending on bandwidth (≈7:1 to 70:1). The signal comes from **12 events in 25 Oct – 1 Nov 2009**, when the UK had already changed clocks and the US hadn't. Spring windows carry almost no data (0–9 events).
- Placebo grid (EU dates shifted by k weeks): moving the autumn switch **later** than the EU date (US = +1 week) costs ≈3.5 units, and later still costs more. Moving it 1 week earlier is neutral or slightly better. Spring shifts barely matter. So the data say "his routine had switched to winter time by the last week of October 2009", which fits EU and not US timing, but the evidence is one autumn week.
- Confidence: DST-following, **high**; EU rather than US timing, **low-to-medium** (small n, one window, KDE model choice). It matters because it is **behavioural** rather than a machine setting, so it partly answers the Gavin control (a London-time build box says nothing about the operator; the operator's routine does).
