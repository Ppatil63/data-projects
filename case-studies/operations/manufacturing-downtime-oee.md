# Manufacturing Downtime: Raising OEE on a Constrained Production Line

**Domain:** Manufacturing operations · **Focus:** OEE improvement, changeover reduction (SMED), planned maintenance · **My role in this analysis:** Business Analyst (scenario case study)

## The problem (the business concern)

A consumer-goods plant's bottleneck line cannot keep up with demand, so the plant runs weekend overtime while the line still loses hours every shift to unplanned stops and long changeovers. Management's first instinct is a second line; the analysis question is whether the existing line's losses justify that capital spend.

Scenario baseline (assumption): Line runs 3 shifts, 5 days, with ~120 hours of scheduled production time per week. OEE is 54%, decomposed as availability 78% × performance 82% × quality 84%. Changeovers average 95 minutes, 14 per week. Unplanned stops average 22 per shift. Weekend overtime costs about $14,000 per month and on-time delivery to the distribution network is slipping.

Who feels it: operators blamed for "slow" shifts, maintenance firefighting instead of preventing, planners padding schedules, and customers downstream getting late supply.

## How I analyzed it

- **Data I'd pull:** Downtime logs with reason codes (validated against PLC/machine data where available), changeover records by product pair, production counts vs. rated speed, scrap/rework counts by shift and SKU, and maintenance work orders.
- **Process mapping:** As-is changeover walk — every step, internal vs. external to the stopped line — and the shift-handover process, since losses cluster at shift boundaries.
- **Root-cause method:** Pareto of lost minutes by reason code; OEE loss waterfall (availability/performance/quality) to decide where the leverage actually is; 5 Whys on the top breakdown mode.
- **Stakeholder questions:** For operators — which stops don't get logged, and why? For maintenance — which failures repeat and what parts aren't on hand? For planning — how much of the schedule churn is order changes vs. line reality?

## What the analysis found

1. **Changeovers are the single biggest loss.** At 31% of lost minutes, 14 changeovers × 95 minutes consumed ~22 hours per week. Observation showed most steps were internal (done while the line was stopped) that could be external — pre-staging parts, pre-heating, preset tooling — and settings were re-dialed by trial each time instead of using recorded recipes.
2. **Minor stops are death by a thousand cuts.** Stops under 5 minutes were 24% of lost minutes but barely logged; operators cleared jams at one feeder station constantly. Machine data showed one misaligned guide rail behind most of them — a small fix invisible in manual logs.
3. **Repeat breakdowns share one root.** The top breakdown mode (18% of lost minutes) traced through 5 Whys to a wear part replaced only on failure, with no spare on site; each event cost the repair time plus an average 3-hour parts wait.
4. **Quality losses concentrate after changeovers.** First-hour scrap after a changeover ran 3× the steady-state rate — the quality component of OEE (84%) was largely a changeover problem too, not a separate one.

## The fix

**Must have (0–60 days):**
- SMED program on the top 5 changeover pairs: video the changeover, split internal/external work, pre-stage kits, convert adjustments to fixed settings/recipes. Target: 95 → 55 minutes.
- Fix the feeder guide rail and add the top repeat-failure parts to on-site spares with min/max levels.
- Standardize downtime reason codes (12 codes max) and log stops over 2 minutes — simple enough that logging actually happens.

**Should have (60–120 days):**
- Move the top wear parts from run-to-failure to time-based preventive replacement in planned windows (TPM), with autonomous maintenance checks (clean, inspect, lubricate) owned by operators.
- Sequence the schedule to group same-format products and cut changeovers per week from 14 toward 10, negotiated with planning.
- First-piece quality check + recorded settings sign-off after each changeover to cut post-changeover scrap.

**Could have:** Condition monitoring (vibration/temperature) on the two most failure-prone assets.

## Expected impact & how I'd measure it

Projections, built bottom-up from the loss Pareto, not top-down hope: OEE 54% → ~65% in two quarters (availability 78% → ~86% mainly from SMED and spares; quality 84% → ~90% from post-changeover controls). That frees roughly 13 hours of capacity per week — equivalent to most of the weekend overtime, deferred before any second-line capital decision.

Measurement plan: weekly OEE and loss-Pareto reporting from the standardized logs, with the baseline struck from 8 weeks of pre-change data; finance validates overtime spend monthly. Guardrails: safety incidents and near misses (SMED must never reward rushing lockout steps), and scrap rate — availability gains that ship bad product are not gains.

## Risks & assumptions

- Manual downtime data undercounts minor stops; the first month with clean codes may make OEE look worse before it looks better — stakeholders need that warning up front.
- SMED gains assume planning cooperates on sequencing; without it, changeover count stays high.
- The case for deferring a second line assumes demand growth stays within the freed capacity for ~12 months.

## What I'd do in the first 30 days

- Reconcile downtime logs against machine data for 2 weeks to size the logging gap.
- Build the loss Pareto and OEE waterfall; agree the top three losses with plant and maintenance leads.
- Video two changeovers and produce the internal/external step analysis.
- Cost the spares kit and the SMED pilot so the 60-day plan has real numbers attached.
