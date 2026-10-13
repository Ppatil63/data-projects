# Warehouse Order Fulfillment Bottleneck: Same-Day Ship SLA Misses

**Domain:** E-commerce warehousing / fulfillment operations · **Focus:** Pick, pack, and ship process redesign · **My role in this analysis:** Business Analyst (scenario case study)

## The problem (the business concern)

A growing e-commerce warehouse is missing its same-day shipping promise. Orders placed before the 2:00 PM cutoff are supposed to leave the building the same day, but the miss rate keeps climbing as volume grows, and the operations team is compensating with overtime and expensive expedited freight.

Scenario baseline (assumption): 8,500 orders per day at peak, ~38,000 order lines per day. Same-day ship rate is 86% against a 95% target. Pick accuracy is 99.2%, so quality is not the main issue — speed and flow are. Expedited freight and overtime are costing roughly $38,000 per month. Customer support sees "where is my order" contacts spike on every missed-SLA day.

Who feels it: customers who paid for fast delivery, the support team absorbing the contacts, and warehouse associates working forced overtime at the end of every shift — which drives attrition and, eventually, more errors.

## How I analyzed it

- **Data I'd pull:** WMS order history with timestamps at each stage (release, pick start, pick complete, pack complete, label, carrier handoff), pick path and zone data per order, labor hours by function and hour of day, and carrier scan data to confirm true departure times.
- **Process mapping:** Walk the floor and build an as-is value stream map from order drop to carrier pickup, with wait times between steps, not just task times.
- **Root-cause method:** Pareto analysis of delay minutes by stage, plus a bottleneck (constraint) analysis by hour of day — a step that is fine on average can still be the constraint at 1:00–3:00 PM.
- **Stakeholder questions:** For the warehouse manager — where do orders queue, and when? For IT/WMS — how are waves released and can release logic change? For carriers — what is the real last pickup time vs. the contractual one?

## What the analysis found

1. **Slotting works against the pickers.** Pareto of picks showed ~20% of SKUs generate ~78% of pick lines, but fast movers were spread across all aisles because locations were assigned when the warehouse opened. Average travel time per pick was far above what the layout should produce.
2. **Wave release creates a dock surge.** Orders were released in two large waves. Packing and the dock were idle mid-morning, then swamped from 1:00 PM onward; pack was the hourly constraint during the exact window the cutoff orders arrived.
3. **Pack stations were the hidden bottleneck.** Four pack stations served the whole building; at peak, picked orders waited an average of 26 minutes for a pack bench. Picking got blamed because it is upstream and more visible.
4. **Cartonization errors caused rework.** System-suggested cartons were wrong often enough that packers re-boxed ~6% of orders, each rework costing about 4 minutes at the scarcest resource.

## The fix

**Must have (phase 1, 0–60 days):**
- Re-slot the top 500 SKUs by pick frequency into a forward pick zone near pack (ABC slotting), reviewed monthly.
- Replace two big waves with hourly mini-waves sized to pack capacity, so flow is level (heijunka-style) through the day.
- Add two pack stations for the 12:00–4:00 PM window using cross-trained pick associates as pick volume tapers.

**Should have (phase 2, 60–120 days):**
- Move single-line orders (about 45% of volume) to batch picking with a put-wall, cutting travel per line sharply.
- Fix cartonization rules with actual dimensional data for the top 2,000 SKUs.

**Could have:** Task interleaving in the WMS so pickers combine picks with putaway on return trips.

## Expected impact & how I'd measure it

These are projections, to be validated in a 4-week pilot on one shift: same-day ship rate from 86% to 94–96%; pick travel time per line down ~15%; overtime hours down ~20%; expedited freight spend down from ~$38,000 to under $15,000 per month.

Measurement plan: daily control chart of ship rate and stage-level cycle times, compared against the same-weekday baseline from the 8 weeks before the pilot. Guardrail metrics: pick accuracy (must stay ≥99.2%), associate injury/near-miss reports, and cost per order — a faster process that breaks accuracy or safety is not a win.

## Risks & assumptions

- Volume keeps growing ~15% quarter over quarter; gains could be absorbed by growth rather than showing as cost savings.
- Re-slotting assumes WMS location data is accurate; a cycle-count check has to come first.
- Labor agreement or shift rules may limit cross-training and staggered pack staffing.

## What I'd do in the first 30 days

- Pull 8 weeks of WMS timestamp data and build the stage-level delay Pareto.
- Walk the floor for two full shifts and validate the as-is map with associates and leads.
- Confirm carrier pickup reality vs. contract with the carrier rep.
- Run a cycle count on the top 500 SKUs so the re-slot is built on clean location data.
- Agree the pilot scope, baseline, and success thresholds with the warehouse manager before changing anything.
