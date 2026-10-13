# Portfolio Case Studies — Index

Scenario case studies written by Prathamesh Patil (Business Analyst). Each is an analysis exercise on a realistic industry scenario — not employment history. Every case follows the same structure: the problem, how I analyzed it, what the analysis found, the prioritized fix, expected impact and how I'd measure it, risks & assumptions, and my first 30 days. Scenario baseline numbers are labelled as assumptions inside each document, and projected impacts are labelled as projections.

## Operations Case Studies

| # | Case study | Domain | Core concern | Headline recommendation |
|---|-----------|--------|--------------|------------------------|
| 1 | [Warehouse Order Fulfillment Bottleneck](operations/warehouse-fulfillment-bottleneck.md) | E-commerce warehousing | Same-day ship rate stuck at 86% vs. a 95% promise as volume grows | Re-slot fast movers by ABC analysis and level the flow with hourly mini-waves matched to pack capacity |
| 2 | [Last-Mile Delivery On-Time Performance](operations/last-mile-delivery-otp.md) | Logistics / last-mile | On-time delivery at 81% vs. a 95% client target, with late stops clustered by route | Rebuild routes with time-window-aware sequencing, dispatch longest routes first, and validate addresses at intake |
| 3 | [Inventory Stockouts vs. Overstock](operations/inventory-stockouts-overstock.md) | Inventory / distribution | Fill rate of 91% on best sellers while 14% of inventory value is dead stock | Segment SKUs ABC/XYZ and set reorder points from real demand and lead-time variability (EOQ + safety stock) |
| 4 | [Support Operations Queue Redesign](operations/support-queue-redesign.md) | Technical support operations | 28% first-response SLA breaches, a 1,900-ticket backlog, and 24% repeat contacts | Tiered triage with skill-based routing, deflection of how-to/status volume, and problem management for recurring issues |
| 5 | [Manufacturing Downtime / OEE](operations/manufacturing-downtime-oee.md) | Manufacturing | OEE of 54% on the bottleneck line while the plant pays weekend overtime | SMED changeover reduction plus on-site spares for repeat failures — free capacity before buying a second line |
| 6 | [Hospital Outpatient Scheduling](operations/hospital-outpatient-scheduling.md) | Healthcare operations | 23% no-shows alongside 38-minute waits and only 74% schedule utilization | Standard reminder cadence, slot templates matched to real visit lengths, and segmented overbooking for high no-show groups |

## Product Case Studies

| # | Case study | Domain | Core concern | Headline recommendation |
|---|-----------|--------|--------------|------------------------|
| 1 | [Food Delivery: Late Deliveries](product/food-delivery-late-orders.md) | Consumer / food delivery | Only 74% of orders arrive within the promised window, and late customers stop reordering | Dynamic promise times from predicted prep variance plus just-in-time courier dispatch |
| 2 | [SaaS Onboarding Drop-Off](product/saas-onboarding-dropoff.md) | B2B SaaS | Only 24% of trial users reach activation; trial-to-paid conversion is 6% | Define activation from converter behavior and re-sequence onboarding: core action and team invite first, configuration later |
| 3 | [E-Commerce Checkout Abandonment](product/ecommerce-checkout-abandonment.md) | E-commerce | Only ~37% of checkout starters finish; mobile converts far worse than desktop | Show shipping costs at cart, add guest checkout and express wallets, and fix payment-failure recovery — each as its own A/B test |
| 4 | [Subscription Churn at Month 2–3](product/subscription-churn-month-2-3.md) | Subscription app | Cohort churn spikes to ~11% in months 2–3; 18% of churn is failed payments | Fix involuntary churn with proper dunning first, remove the price step-up surprise, and intervene on usage decay before day 60 |
| 5 | [Telemedicine Accessibility](product/telemedicine-accessibility-booking.md) | Healthcare product / accessibility | Booking completion is 58% for patients 65+ vs. 86% for younger users | WCAG 2.2 AA remediation of the booking flow (contrast, target size, timeouts, real error handling) plus assisted and caregiver booking paths |
| 6 | [Job-Matching Platform for Freshers](product/job-matching-freshers-conversion.md) | Marketplace / hiring | Application-to-interview conversion is 4.1% and 46% of applications get no response at all | Skills-based transparent matching with verified skill signals, and employer response accountability so no application ends in silence |

**Count:** 12 case studies (6 operations, 6 product), each ~600–900 words.
