# Subscription Churn: Users Leave at Month 2–3

**Domain:** Subscription product (streaming / fitness app) · **Focus:** Cohort retention analysis, voluntary vs. involuntary churn, save plays · **My role in this analysis:** Business Analyst (scenario case study)

## The problem (the business concern)

A subscription app (fitness content, in this scenario) grows steadily but leaks: a disproportionate share of subscribers cancel in months 2–3, right after the novelty and the introductory offer wear off. Leadership's first instinct is more acquisition and a bigger discount. The analysis question is who churns, why, and how much of it is actually preventable.

Scenario baseline (assumption): ~60,000 active subscribers. Blended monthly churn is 6.8%. Cohort view shows month-1 churn ~5%, spiking to ~11% in months 2 and 3, then settling near 4% for tenured users. Intro pricing converts to full price at month 3. About 18% of all churn is involuntary (failed payments), discovered only when dunning data was pulled. Average revenue per subscriber is $13/month.

Who feels it: subscribers who quietly stop getting value, the growth team whose acquisition spend evaporates at month 2, and finance, whose revenue forecasts keep missing on the same cohort pattern.

## How I analyzed it

- **Data I'd pull:** Cohort tables by signup month (retention by month of life), usage telemetry by week (sessions, minutes, features used), billing data (plan, price change points, payment failures and retries), cancellation survey responses, and win-back outcomes.
- **Process mapping:** The subscriber lifecycle as-is: signup → intro period → price step-up → renewal/cancellation, including every communication the user receives at each point (in this scenario, almost none between signup and the price increase).
- **Root-cause method:** Cohort and survival analysis to locate *when* churn happens; behavioral comparison — usage in the 2 weeks before churn vs. matched retained users — to find leading indicators; split churn into voluntary (user cancels) vs. involuntary (payment fails) before designing anything, because the fixes are entirely different.
- **Stakeholder questions:** For product — what is the core habit this app is supposed to build, and by when? For finance — what did the intro-offer terms actually promise? For engineering/payments — what happens today when a card fails?

## What the analysis found

1. **Usage decays before churn, visibly.** Subscribers who churned at month 2–3 showed a clear pattern: weekly sessions fell by more than half between weeks 3 and 6, well before cancelling. The churn decision happened weeks before the cancel click — the app had a warning window it wasn't using.
2. **The price step-up lands as a surprise.** The intro-to-full-price jump at month 3 coincided exactly with the churn spike. Users reported in cancellation surveys that they "didn't realize" the price would change — a communication and expectation failure as much as a price-sensitivity one.
3. **Nearly a fifth of churn is a payments problem, not a product problem.** 18% of churned accounts never chose to leave; their cards failed (expired, replaced, soft declines) and the existing flow sent one email and gave up. These users had usage patterns identical to retained users.
4. **One-size content bores the second segment.** Two user segments behaved differently: goal-driven users (e.g., training for an event) retained well; general "get fitter" users plateaued when the program stopped adapting around week 5, and their churn drove most of the spike.

## The fix

**Must have:**
- Fix involuntary churn first — it is the cheapest retained revenue available: smart retry logic on failed payments (retry timing based on failure type), pre-expiry card-update prompts, multiple notification channels, and a grace period where access continues while payment is recovered. Target: recover 30–40% of failed payments that are currently lost.
- Kill the price surprise: at signup, state the step-up date and amount plainly; remind at day 45 and day 75 with the actual upcoming charge. Measure cancellation-survey "price surprise" mentions to verify.

**Should have:**
- Early-warning intervention: when a subscriber's weekly sessions drop >50% from their own baseline before day 60, trigger a re-engagement sequence (a relevant new program, a shorter-session option, an email built around their original goal) — targeted, not a blanket discount blast.
- Week-5 program refresh for the general segment: new plan phase or challenge so the experience changes before the plateau does its damage.

**Could have:** A save flow on cancellation offering pause (1–2 months) instead of cancel for users citing time pressure; annual-plan offers targeted only at users past the month-3 danger zone with strong usage, not as a desperation discount.

## Expected impact & how I'd measure it

Projections, sequenced so each can be measured: involuntary churn recovery alone takes blended churn from 6.8% toward ~6.1%; price-transparency and early-warning plays target month 2–3 cohort churn from ~11% to ~8.5% within two cohort cycles; combined target blended churn ≈ 5.4% within two quarters. At 60,000 subscribers and $13/month, one point of monthly churn is roughly $7,800/month of recurring revenue preserved, compounding across cohorts.

Measurement plan: cohort retention curves reviewed monthly (never blended churn alone, which hides the month 2–3 pattern), involuntary churn tracked as its own line, and interventions A/B tested on eligible cohorts. Guardrails: dunning aggressiveness vs. complaints and issuer flags; discount depth (retention bought by training users to wait for offers shows up in full-price conversion); pause abuse rate; and unsubscribe/complaint rates on re-engagement emails.

## Risks & assumptions

- The usage-decay signal is predictive, not proven causal; the A/B design must confirm that intervening actually changes outcomes vs. just identifying users who were leaving anyway.
- Payment recovery rates depend on issuer behavior and card mix; the 30–40% recovery target is an industry-plausible projection, not a guarantee.
- Baseline assumes billing and product analytics can be joined on a common user ID; if not, identity resolution is the unglamorous first project.

## What I'd do in the first 30 days

- Build the cohort retention table and the voluntary/involuntary churn split; publish the month 2–3 evidence pack.
- Audit the dunning flow end-to-end (what actually happens on a failed payment today, hour by hour).
- Analyze pre-churn usage decay and propose the early-warning trigger with data.
- Draft the price-step-up communication fix and the dunning requirements with acceptance criteria and measurement plans.
