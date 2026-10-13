# Support Operations: Queue Redesign for a Growing SaaS Support Org

**Domain:** Technical support operations · **Focus:** Triage, routing, deflection, and problem management · **My role in this analysis:** Business Analyst (scenario case study)

## The problem (the business concern)

A B2B SaaS company's support queue has grown faster than the team. Customers wait too long for a first response, simple questions sit in the same queue as production outages, and the same issues come back week after week because nobody owns fixing the cause.

Scenario baseline (assumption): ~6,500 tickets per month across email, chat, and portal. First-response SLA breach rate is 28%. Open backlog is ~1,900 tickets and aging. Repeat contacts (same customer, same issue, within 14 days) are 24% of volume. CSAT is 84%. Agent attrition is rising, with exit interviews citing queue chaos and context switching.

Who feels it: customers whose work is blocked, agents burning out on avoidable volume, and the product/engineering teams who never see clean signal about what is actually broken.

## How I analyzed it

- **Data I'd pull:** 6 months of ticket data — created/resolved timestamps, priority, category, channel, first-response and resolution times, reopen and reassign counts, agent touches per ticket, CSAT per ticket, and text samples for theme analysis.
- **Process mapping:** As-is flow from intake to closure, including how tickets get assigned (round-robin), escalated, and reopened; map where tickets wait vs. where they are worked.
- **Root-cause method:** Pareto of volume by category and by root cause; separate "demand we can prevent" (product defects, confusing UX, missing docs) from "demand we can deflect" (how-to, status checks) from "demand we must serve well" (real incidents, complex cases).
- **Stakeholder questions:** For agents — which tickets waste your time, and which handoffs fail? For support leadership — what do SLAs actually promise per tier? For product/engineering — what ticket evidence would make you prioritize a fix?

## What the analysis found

1. **No real triage.** Everything entered one queue and was worked roughly in arrival order. A password reset could wait behind a data-sync investigation, while a P1 waited behind both. First-response breaches concentrated in low-complexity tickets that should never have waited at all.
2. **A third of volume is deflectable.** About 32% of tickets were how-to questions and status checks ("did my import run?") that a good help center, in-product status, or a macro-driven instant answer could resolve without an agent — but the help center covered only a fraction of the top 50 question themes.
3. **Reassignment churn.** Tickets averaged 1.8 reassignments because routing was round-robin, not skill-based. Every reassignment added wait time and a re-read of the ticket; complex billing and integration tickets suffered most.
4. **No problem management.** The top 10 recurring issues generated repeat tickets every week, but there was no problem-ticket process linking incidents to an underlying fix — agents re-solved the same issue hundreds of times, and engineering never saw the aggregated cost.

## The fix

**Must have (0–60 days):**
- Tiered triage: a rotating triage role (or rules-based auto-triage) tags every ticket within 30 minutes by severity and type; P1s jump the queue with a defined on-call path.
- Skill-based routing by product area and ticket type, ending round-robin for anything beyond simple requests.
- SLA clocks differentiated by tier (e.g., P1 first response 30 min, standard how-to 8 business hours) so the promise matches the work.

**Should have (60–120 days):**
- Deflection build-out: help-center articles and in-product guidance for the top 20 how-to themes, plus automation for status checks; measure deflection honestly (article → no ticket within 7 days), not by page views.
- Problem management: weekly review of top recurring categories, problem tickets linked to incidents, and a monthly evidence pack (volume × handling cost) to engineering.

**Could have:** AI-assisted draft replies and auto-summaries for agent review, piloted on the how-to queue only, with quality sampling.

## Expected impact & how I'd measure it

Projections, validated against a 4-week pilot on one product area: first-response SLA breaches 28% → under 10%; backlog down ~50% in 60 days from deflection plus triage throughput; repeat contacts 24% → ~16%; reassignment rate down from 1.8 to ~1.2 per ticket.

Measurement plan: weekly dashboard of volume, breach rate, backlog age profile, repeat-contact rate, and CSAT by category, vs. the 8-week pre-change baseline. Guardrails: CSAT must not fall as deflection rises (deflection that frustrates customers shows up in CSAT and repeat contacts), and resolution quality is sampled by QA review so speed isn't bought with sloppy closures.

## Risks & assumptions

- Ticket category data is only as good as agent tagging; a 2-week tagging cleanup and a simple taxonomy are prerequisites.
- Deflection targets assume the product team ships two small UX fixes for the top confusion points; support-side fixes alone cap the gain.
- Triage adds a coordination role; on a small team it must rotate so it doesn't become a burnout post itself.

## What I'd do in the first 30 days

- Build the ticket dataset and produce volume/SLA/repeat Pareto by category, validated with two senior agents.
- Map the as-is intake-to-closure flow and document the current (informal) triage reality.
- Draft the severity definitions and SLA table with support leadership and get sign-off.
- Stand up the top-10 recurring issue list as the first problem-management backlog with costed evidence.
