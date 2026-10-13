# Inventory: Stockouts and Overstock at the Same Time

**Domain:** Inventory management / distribution · **Focus:** Replenishment policy, EOQ and safety stock, SKU segmentation · **My role in this analysis:** Business Analyst (scenario case study)

## The problem (the business concern)

A multi-SKU distributor is losing sales to stockouts on its best-selling items while cash sits trapped in slow-moving stock. Buyers order by habit and vendor minimums, not by policy — so the business has too much of what doesn't sell and too little of what does.

Scenario baseline (assumption): ~4,200 active SKUs. Line fill rate is 91% against a 97% target the sales team quotes to key accounts. Inventory turns are 4.1 per year. Carrying cost is about 22% of inventory value per year (storage, insurance, shrinkage, cost of capital). Dead stock (no movement in 12 months) is 14% of inventory value. Emergency expediting from alternate suppliers runs about $9,000 per month.

Who feels it: key-account customers who get partial shipments, the sales team discounting to apologize, and finance watching working capital climb every quarter.

## How I analyzed it

- **Data I'd pull:** 24 months of SKU-level demand (units by week), supplier lead times (promised vs. actual), on-hand and on-order snapshots, purchase price and margin by SKU, and stockout/backorder logs.
- **Process mapping:** As-is replenishment flow — who decides order quantity, with what data, on what cycle — and the receiving/putaway path that determines when stock is actually sellable.
- **Root-cause method:** ABC/XYZ segmentation (value × demand variability) to show whether one ordering policy is being applied to very different SKU behaviors; demand and lead-time variability analysis to size safety stock properly.
- **Stakeholder questions:** For buyers — what triggers an order today? For sales — which stockouts actually cost orders vs. annoyance? For the warehouse — how accurate is on-hand data (cycle count results)?

## What the analysis found

1. **One policy for everything.** A items (top ~15% of SKUs, ~70% of margin) were reviewed on the same monthly cycle as C items. A items stocked out mid-cycle; C items were reordered "just in case."
2. **Reorder points ignore variability.** Order-up-to levels were based on average demand only. For SKUs with spiky demand (high XYZ variability), average-based stock guarantees stockouts in peak weeks — the math, not the buyer, was the problem.
3. **Lead times in the system were wrong.** System lead time said 14 days on the top supplier; actual receipts averaged 21 days with a standard deviation of 6. Safety stock computed off 14 days was structurally too low.
4. **Vendor minimums inflated C-item orders.** Minimum order quantities forced 6–9 months of cover on slow movers, which is exactly where the dead stock accumulated.

## The fix

**Must have (0–60 days):**
- Segment all SKUs ABC/XYZ and set a different review cycle and service target per segment (e.g., A: 98% fill, weekly review; C: 90%, monthly or make-to-order).
- Recalculate reorder points with real variability: Reorder point = average daily demand × lead time (days) + safety stock, where safety stock = z × σ_d × √L (z from target service level, σ_d = daily demand standard deviation, L = actual lead time). Use measured lead times, updated quarterly.
- Correct system lead times for the top 10 suppliers from receipt history.

**Should have (60–120 days):**
- Replace vendor-minimum-driven buys on C items with consolidated orders across SKUs from the same vendor, or delist the worst tail SKUs with sales sign-off.
- Monthly dead-stock review with a markdown/return-to-vendor path instead of silent write-offs.
- Cycle counting weighted to A items so on-hand accuracy supports the new policy.

**Could have:** Simple demand forecasting (moving average / exponential smoothing) for A items ahead of seasonal peaks.

## Expected impact & how I'd measure it

Projections, phased by segment so A items move first: line fill rate 91% → 96% within two quarters; inventory value down ~18% at equal or better fill rate, mostly from C-item cover reduction; expediting spend down by half. EOQ logic (EOQ = √(2DS/H)) applies to order sizing on stable A/B items to balance ordering cost against carrying cost instead of ordering by vendor pack size.

Measurement plan: monthly fill rate, turns, and weeks-of-cover by segment vs. the pre-change baseline; a stockout log tied to lost-order notes from sales. Guardrails: fill rate must not be "improved" by quietly raising total inventory — total value is reported next to fill rate every month — and A-item service is never traded for C-item savings.

## Risks & assumptions

- On-hand records must be trustworthy; if cycle-count accuracy is under ~95%, policy changes will misfire and counting fixes come first.
- Demand history includes two stockout-censored years, so true demand on A items is understated; use backorder-adjusted demand.
- Suppliers may resist smaller, more frequent orders; consolidation plan assumes at least the top vendors agree.

## What I'd do in the first 30 days

- Build the SKU-level dataset (demand, lead time actuals, margin) and validate on-hand accuracy with a sample cycle count.
- Produce the ABC/XYZ segmentation and the "policy vs. behavior" gap list.
- Recalculate reorder points for the top 100 A SKUs and quantify the stockout/cash impact.
- Agree segment service targets with sales and finance before any policy goes live.
