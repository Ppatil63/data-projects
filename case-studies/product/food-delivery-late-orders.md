# Food Delivery App: Late Deliveries Are Killing Repeat Orders

**Domain:** Consumer product / food delivery · **Focus:** Delivery promise accuracy, dispatch logic, retention impact · **My role in this analysis:** Business Analyst (scenario case study)

## The problem (the business concern)

A food delivery platform's repeat order rate is sliding, and exit surveys keep naming the same reason: food arrives later than the app promised. The business initially treated this as a courier problem. The analysis question is where lateness is actually created — in the promise, the kitchen, the dispatch, or the road.

Scenario baseline (assumption): ~40,000 orders per week in one metro. Orders arrive within the promised window 74% of the time; 18% arrive more than 10 minutes late. Average quoted time is 32 minutes; average actual is 38. Customers who receive a 10+ minute late order reorder within 30 days at roughly half the rate of on-time customers. Refund/"late" credits cost about $26,000 per month.

Who feels it: customers whose dinner plans break, restaurants blamed for cold food they cooked on time, couriers pressured at the curb, and the growth team watching repeat rate — the cheapest revenue the business has — erode.

## How I analyzed it

- **Data I'd pull:** Full order timeline per order: placed, accepted by restaurant, prep started, ready, courier assigned, picked up, delivered — plus quoted vs. actual time, order value, distance, weather/time band, and the customer's reorder behavior over the next 60 days.
- **Process mapping:** As-is flow of an order across customer app, restaurant tablet, dispatch algorithm, and courier app, noting where time estimates are generated and where orders wait untouched.
- **Root-cause method:** Decompose total delivery time into its stages and measure which stage's variance explains lateness (a stage with a good average but wild variance creates most late orders); cohort comparison of repeat rates for on-time vs. late customers to size the business cost; Pareto of late orders by stage of delay.
- **Stakeholder questions:** For restaurant partners — when does the prep clock really start? For dispatch/engineering — what inputs does the promise time use today? For courier ops — where do couriers actually wait?

## What the analysis found

1. **The promise ignores prep variance.** Quoted times used each restaurant's *average* prep time. Restaurants with highly variable prep (same average, much wider spread) generated most late orders — the promise was "right on average" and wrong for a third of orders.
2. **Couriers wait at restaurants; food waits for couriers.** Stage data showed two opposite queues: couriers arriving before food was ready (wasted courier capacity at peak) and ready food sitting 6+ minutes waiting for a courier, arriving cold. Assignment happened at order placement, not relative to predicted ready time.
3. **Stacked orders compound delay.** To raise courier utilization, dispatch batched 2–3 orders per trip at peak. The second and third customers on a stack absorbed most of the lateness, and their repeat rate was the worst in the cohort data — utilization was being bought with the most loyal customers' experience.
4. **Peak radius was too wide.** At peak, the dispatch radius stayed at off-peak settings; long-distance orders accepted at 7 PM had almost no chance of meeting any promise, and they displaced courier capacity from nearby orders that could have been on time.

## The fix

**Must have:**
- Dynamic promise times: quote from predicted prep time (per restaurant, per hour band, using recent variance, not just the mean) plus live courier supply — show a slightly longer honest promise rather than a short false one.
- Just-in-time dispatch: assign the courier against predicted ready time so courier arrival and food readiness coincide.

**Should have:**
- Cap stacking: maximum 2 orders per trip, and never stack when the first order's remaining promise buffer is under 10 minutes. Measure courier utilization impact openly instead of hiding it.
- Peak zoning: shrink the active delivery radius at peak for the worst-performing zones, or add a transparent peak fee for long-distance orders.

**Could have:** Restaurant prep countdown display with a "running late" flag that re-times dispatch automatically; proactive customer notification with a revised time before the customer has to ask.

## Expected impact & how I'd measure it

Projections, tested zone-by-zone (roll to half the zones, hold half as control for 4 weeks): on-time within promised window 74% → 85%+; 10+ minute late orders 18% → under 10%; late-credit spend down ~40%; repeat order rate for previously-late cohorts recovering toward on-time cohort levels.

Measurement plan: weekly on-time %, average lateness, and 30-day repeat rate by cohort, plus refund cost per 1,000 orders. Guardrails: courier earnings per hour and orders per courier hour (on-time must not be bought by crashing courier income), restaurant order volume in shrunken zones, and average quoted time — if quotes balloon, conversion will fall, so quote time is tracked alongside promise accuracy.

## Risks & assumptions

- Restaurants may game prep-time inputs if they believe faster quotes bring more orders; the model should use observed timestamps, not self-reported prep times.
- Courier supply at peak is finite; zoning and stack caps shift scarcity rather than removing it — the plan assumes ops adjusts courier incentives at peak in parallel.
- Repeat-rate recovery is a projection from cohort correlation; the zone-controlled rollout exists precisely to test whether lateness *causes* the repeat drop or merely correlates with it.

## What I'd do in the first 30 days

- Build the order-timeline dataset and produce the stage-variance decomposition of lateness.
- Run the on-time vs. late cohort repeat analysis to put a revenue number on lateness.
- Interview 5 restaurant partners and 5 couriers to validate what timestamps say.
- Spec the dynamic-promise and just-in-time dispatch requirements with acceptance criteria and the zone-rollout measurement plan.
