# Job-Matching Platform for Freshers: Applications Aren't Becoming Interviews

**Domain:** Marketplace product / hiring platform · **Focus:** Matching quality, two-sided trust signals, conversion funnel · **My role in this analysis:** Business Analyst (scenario case study)

## The problem (the business concern)

A job platform for fresh graduates has plenty of signups and job posts, but very few applications turn into interviews. Freshers respond by mass-applying, employers respond by ignoring the platform's applicants, and both sides conclude the platform doesn't work. It is a two-sided trust spiral, and analyzing only one side misses the cause.

Scenario baseline (assumption): ~25,000 active fresher job seekers and ~800 employers posting monthly. Average applications per user per month is 14 — high volume, low intent signal. Application-to-interview conversion is 4.1%. Employers view only 38% of applications within 7 days; the median employer response time is 11 days, and 46% of applications never receive any response at all. Only 46% of candidate profiles are complete (skills, project links, availability). Repeat monthly active employers fell 20% over two quarters.

Who feels it: freshers spending months applying into silence, employers wading through unqualified bulk applications, and the platform, whose only real product — successful matches — isn't visibly happening.

## How I analyzed it

- **Data I'd pull:** The full funnel per side: candidate (signup → profile complete → application → viewed → shortlisted → interview → outcome) and employer (post → applications received → viewed → responded → interviewed → hired), plus match attributes at application time (skills overlap, location, availability), response-time distributions, and profile completeness of the candidates who *did* get interviews.
- **Process mapping:** As-is flows for both sides — what a fresher sees when applying (in this scenario: one-click apply with no fit feedback) and what an employer sees when reviewing (a list sorted by recency, no quality signals).
- **Root-cause method:** Two-sided funnel analysis; outcome regression in plain terms — compare attributes of applications that produced interviews vs. those that didn't (skills match, profile completeness, application timing, employer responsiveness) to learn what actually drives conversion, instead of guessing.
- **Stakeholder questions:** For employers — how do you actually screen a fresher with no track record? For freshers — what do you do when you hear nothing for two weeks? For the business — is the platform paid for postings, applications, or hires? (The answer changes what "good" means.)

## What the analysis found

1. **Matching is keyword-based and it shows.** Jobs were matched on title/keyword overlap. Applications with high stated-keyword overlap but low *assessed* skill overlap flooded employers; interview-producing applications were distinguished less by keywords than by a complete profile with project evidence and a verified skill signal.
2. **One-click apply destroyed the intent signal.** With no cost to applying, users applied to anything; 14 applications/user/month at 4.1% conversion means employers learned that a platform application signals almost nothing. Employers who received 100+ bulk applications viewed the fewest — volume actively suppressed review.
3. **Silence is the product experience for most users.** 46% of applications got no response ever, and the median wait was 11 days. Fresher interviews and surveys (in this scenario) showed the same pattern: after ~2 weeks of silence, users stopped opening the app — churn of the supply side followed employer behavior, not candidate laziness.
4. **Freshers have no way to prove ability.** Employers screening freshers have no work history to read, and the platform gave them nothing else — no assessments, no project verification, no structured availability/location confirmation — so they defaulted to college brand as a proxy, which the platform's own outcome data showed was a weak predictor next to demonstrated skills.

## The fix

**Must have:**
- Skills-based matching: build a skills taxonomy for the top job families; extract skills from job posts and candidate projects; show both sides a transparent match view ("You match 7 of 9 skills; missing: SQL joins — here's a 2-hour path"). Rank employer inboxes by match quality, not recency.
- Verified skill signals: short, proctored-format skill assessments and verified project links (e.g., a live portfolio/repo link that is actually checked), displayed as badges employers can filter on.
- Employer response accountability: response-time displayed on job posts ("typically responds in 3 days"), automated nudges at day 3 and day 7, and auto-close with candidate notification at day 14 — no application ends in silence.

**Should have:**
- Application quality over quantity: light friction for low-match applications (a prompt showing the skill gap and asking for a 2-line note on fit), plus a soft cap that resets as employers respond — restoring the signal value of an application.
- Structured fresher profiles: guided completion (skills, one project with a link, availability date, location/mobility), with completeness visibly tied to response rates so users understand the payoff.

**Could have:** Interview-readiness nudges (mock questions for the specific role family) once an interview is booked, improving show rates and employer perception of platform candidates.

## Expected impact & how I'd measure it

Projections, rolled out by job family so measurement stays clean (start with the two largest families): application-to-interview conversion 4.1% → 7%+ within two quarters; applications receiving a response within 7 days from 38% to 65%; median employer response time 11 → 5 days; profile completeness 46% → 70%.

Measurement plan: funnel by side and job family, weekly for behavior metrics, monthly for employer retention. Guardrails: total application volume will *fall* by design — leadership must agree in advance that volume is not the success metric; match-ranked inboxes watched for bias (candidates from lesser-known colleges must not be systematically buried — audit interview rates by institution tier); assessment completion must not become a paywall-style barrier for low-income users.

## Risks & assumptions

- Employer behavior is the hardest variable: if employers won't respond even with better matches, nudges and transparency only go so far; the plan assumes at least anchor employers in each family cooperate during rollout.
- Assessments must be genuinely predictive; a bad test that filters out good candidates is worse than none — pilot validation against interview outcomes is built in before scaling.
- Baseline assumes outcome data (interview/hire) is captured on-platform; off-platform outcomes need an employer follow-up loop or conversion will be undercounted.

## What I'd do in the first 30 days

- Build the two-sided funnel dataset and the attributes-of-success comparison (what distinguishes applications that produced interviews).
- Interview 6 employers and 8 freshers to validate the silence and screening findings firsthand.
- Draft the skills taxonomy for the top two job families with sample job posts and profiles.
- Write requirements for response-accountability (nudges, response-time display, auto-close) as the first release — it needs no ML and attacks the trust problem directly — with the measurement plan attached.
