# SaaS Onboarding Drop-Off: Trial Users Never Reach Activation

**Domain:** B2B SaaS product · **Focus:** Funnel analysis, activation definition, onboarding redesign · **My role in this analysis:** Business Analyst (scenario case study)

## The problem (the business concern)

A B2B SaaS tool (team project/workspace software) spends heavily to acquire trial signups, but most trials never convert — and the drop happens early, before users have seen the product do anything valuable. The team had been treating this as a pricing problem and discounting trials, which did not move conversion.

Scenario baseline (assumption): ~10,000 trial signups per month. Funnel: 78% verify email and log in; 61% create a workspace; only 24% complete the product's core action (the activation event — e.g., creating a project and completing one real workflow in it) within 7 days; 15% are still active at day 7; trial-to-paid conversion is 6%. Support tickets from trial users cluster on "how do I get started" themes.

Who feels it: the growth team buying signups that evaporate, users who signed up with a real job to do and bounced off setup, and sales, who get handed "trials" that were never actually trials of anything.

## How I analyzed it

- **Data I'd pull:** Product analytics event stream keyed by user/workspace — signup, verification, each onboarding step, first core action, invites sent/accepted, day 1/3/7 activity — plus trial outcome (converted/expired), company size, and acquisition channel.
- **Process mapping:** The as-is onboarding journey step by step with time-on-step and exit points; compare the intended happy path against the paths users actually take (most users do not follow the designed path).
- **Root-cause method:** Funnel analysis with segment cuts (company size, channel, invited vs. creator); define activation by working backwards — compare feature usage of users who converted vs. those who churned to find the behavior that actually predicts conversion, rather than assuming the designed "aha moment" is the real one.
- **Stakeholder questions:** For customer success — what do converted users do in week 1 that others don't? For engineering — which setup steps are technically mandatory vs. historical habit? For sales — what job did the buyer think they were hiring the product for?

## What the analysis found

1. **Activation is team-based, but onboarding is solo.** Users who invited at least one teammate in the first 3 days converted at roughly 3× the rate of solo users — yet the invite step sat at the *end* of setup, after configuration steps most users never finished.
2. **Setup asks for decisions users can't make yet.** The wizard demanded workspace structure, naming conventions, and integrations before the user had done any real work. Median time to first core action was 2.5 days; users who hit the core action on day 0 converted at several times the rate of those who didn't.
3. **Empty states teach nothing.** New workspaces opened onto blank screens. Users stared at an empty project list with no example data, no template, and no next step — session recordings (in this scenario) showed users clicking around for under 2 minutes and leaving.
4. **The "how do I start" support load confirmed it.** 41% of trial support tickets were setup confusion, not product defects — the funnel leak and the support cost were the same root cause.

## The fix

**Must have:**
- Redefine activation explicitly: "workspace created + first core action completed + ≥1 teammate invited within 7 days" — instrument it, report it weekly, and make it the onboarding team's north-star metric.
- Re-sequence onboarding: core action first (with a template that creates a realistic starter project in one click), invite teammates immediately after the first success, defer all configuration until it becomes relevant.

**Should have:**
- A 4-step progress checklist anchored to the activation milestones, persistent in-product, dismissible but resumable.
- Empty states replaced with guided first actions and sample data that can be deleted in one click.
- Lifecycle emails tied to behavior, not time: if no core action by day 1, send the template link; if core action done but no invite by day 3, send the invite prompt — each with one clear action.

**Could have:** Role-based starting templates (the job the user picked at signup changes the starter project); concierge onboarding calls reserved for accounts above a size threshold where economics justify it.

## Expected impact & how I'd measure it

Projections, A/B tested (new onboarding to 50% of new signups for one month, pre-registered success criteria): activation rate 24% → 35%; day-7 retention 15% → 22%; trial-to-paid conversion 6% → 8–9% over the following quarter as activated cohorts mature.

Measurement plan: funnel conversion by step and segment, weekly, with the experiment read on activation first (it leads), conversion second (it lags). Guardrails: time-to-first-action must fall, not just completion of a checklist; support tickets per trial should fall; and paid conversion quality — refund/early-churn rate of converted accounts — must not worsen, because activating the *wrong* users faster is not a win.

## Risks & assumptions

- The activation definition is correlational until tested; the A/B rollout exists to verify that pushing users through these milestones *causes* conversion rather than just selecting motivated users.
- Templates assume 2–3 dominant use cases cover most trials; if the user base is more fragmented, template coverage becomes its own workstream.
- Sales-led accounts may need a different path; the redesign targets self-serve trials and shouldn't be forced onto enterprise pilots.

## What I'd do in the first 30 days

- Instrument and backfill the funnel; validate event data quality with two days of manual session tracing.
- Run the converter vs. churner behavior comparison and propose the activation definition with evidence.
- Map as-is onboarding with exit rates per step; cut the three highest-friction steps on paper with product and engineering.
- Write the experiment plan: hypothesis, segments, sample size, success and guardrail metrics, decision date.
