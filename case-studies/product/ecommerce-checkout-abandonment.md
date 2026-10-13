# E-Commerce Checkout Abandonment: Cart-to-Payment Friction

**Domain:** E-commerce product · **Focus:** Checkout funnel, friction audit, experimentation · **My role in this analysis:** Business Analyst (scenario case study)

## The problem (the business concern)

An online retailer gets healthy traffic and plenty of carts, but too few checkouts finish. Marketing keeps buying more traffic to compensate, which raises acquisition cost while the leak — between cart and payment — stays exactly where it was.

Scenario baseline (assumption): ~100,000 sessions per month. Add-to-cart rate 12% of sessions; checkout start rate 6.5% of sessions; completed purchase 2.4% of sessions. That means of shoppers who start checkout, only about 37% finish. Mobile is 68% of traffic but only 54% of orders. Average order value is $64. Cart abandonment surveys cite "unexpected costs" and "checkout took too long" as the top two reasons.

Who feels it: shoppers who wanted the product and gave up, the marketing team paying more per order every quarter, and customer support handling "I tried to pay" contacts that never become orders.

## How I analyzed it

- **Data I'd pull:** Step-level funnel events (cart view, checkout start, address, shipping method, payment, confirmation) with device, new vs. returning, and error codes; payment gateway decline/failure logs; session recordings sampled at the highest-exit steps.
- **Process mapping:** The as-is checkout as the user experiences it — count actual fields, steps, page loads, and decision points on mobile and desktop separately; include account creation, address entry, shipping selection, and payment as distinct friction sources.
- **Root-cause method:** Funnel analysis by step and segment to find where abandonment concentrates; error-rate analysis on the payment step (distinguishing user abandonment from technical failure — they need different fixes); an exit-survey and support-ticket theme review to cross-check the numbers with stated reasons.
- **Stakeholder questions:** For engineering — why is account creation mandatory before payment? For finance — which payment methods/fees are negotiable? For operations — can shipping cost be calculated at cart, not checkout?

## What the analysis found

1. **Shipping cost appears too late.** Shipping was revealed only at the payment step. The single largest exit was on that step, and exit-survey data matched: "unexpected costs" was the #1 stated reason. Users felt ambushed, and the funnel shape showed it.
2. **Forced account creation blocked first-time buyers.** Checkout required creating an account (password rules included) before payment. New visitors — the majority of mobile traffic — exited at account creation at roughly double the rate of returning users.
3. **The form was built for the database, not the human.** 24 fields across address and payment, no address autocomplete, no input formatting help, and errors shown only after submit, clearing the payment fields each time. Session recordings showed repeated error loops on mobile.
4. **Some "abandonment" was actually payment failure.** Gateway logs showed a meaningful slice of payment attempts failing on technical errors (timeouts, issuer soft declines with no retry guidance) while the user saw a generic "payment failed" message with no alternative offered. Those users were counted as abandoners; they were actually rejected customers.

## The fix

**Must have (each as a separate A/B test, not a big-bang relaunch):**
- Surface shipping cost and delivery estimate on the cart page ("free over $75" progress bar if that is the policy), so no cost is first revealed at payment.
- Guest checkout; offer account creation *after* purchase using the details already entered ("save these for next time?").
- Cut and assist the form: address autocomplete, card input formatting and inline validation, preserve all fields on error. Target: 24 fields → the practical minimum.

**Should have:**
- Express payment options (Apple Pay / Google Pay / PayPal) above the form on mobile, where the abandonment is worst.
- Payment failure recovery: specific error messages, one-tap retry, and an alternative-method prompt; alerting on gateway error-rate spikes so failures stop masquerading as abandonment.

**Could have:** One-page checkout consolidation once the step fixes are measured (it is often oversold; steps aren't the enemy — surprises and friction are).

## Expected impact & how I'd measure it

Projections, each validated by its own experiment at the observed traffic (~6,500 checkout starts/month gives readable tests in 2–4 weeks per change): checkout completion 37% → 46% of starters; overall session-to-purchase conversion 2.4% → ~3.0%; at $64 AOV that is roughly $38,000/month of recovered revenue at current traffic, before any AOV effects.

Measurement plan: pre-registered hypotheses per test with primary metric (step conversion), minimum detectable effect, and a fixed read date. Guardrails: AOV (free-shipping thresholds can distort baskets), payment fraud/chargeback rate on guest checkout, page performance on mobile, and refund rate — conversion bought by confusing users shows up in refunds and support contacts.

## Risks & assumptions

- Baseline assumes analytics events are trustworthy; the first task is reconciling funnel counts against order records, because a broken event makes every test read wrong.
- Guest checkout may complicate the retailer's loyalty program economics; finance must agree the trade-off explicitly.
- Results will differ by device segment; tests must be read mobile-first, not as blended averages that hide a mobile regression.

## What I'd do in the first 30 days

- Reconcile funnel analytics against order and gateway records; publish the corrected step-by-step baseline.
- Complete the field/step/error audit on mobile and desktop with session-recording evidence.
- Rank fixes by expected impact × effort with engineering and finance; write the first two experiment briefs (shipping transparency, guest checkout) with guardrails and read dates.
- Stand up a weekly checkout health report: step conversion by device, payment error rate, AOV.
