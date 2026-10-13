# Last-Mile Delivery: On-Time Performance and Route Efficiency

**Domain:** Logistics / last-mile delivery · **Focus:** Route planning, dispatch, and delivery promise management · **My role in this analysis:** Business Analyst (scenario case study)

## The problem (the business concern)

A regional courier is delivering late often enough that its two largest retail clients have put it on a performance improvement plan. Late deliveries are not random — they cluster by route, time of day, and neighborhood — but dispatch runs on habit and static route templates built two years ago.

Scenario baseline (assumption): ~12,000 stops per week across 26 routes. On-time performance (arrival within the promised window) is 81% against a 95% client target. Failed first delivery attempts are 9% of stops. Average route length is 92 stops, and cost per stop is about $6.40. Overtime is routine on the three longest routes.

Who feels it: end customers missing parcels, the retail clients whose brand absorbs the complaint, drivers pressured to speed, and the courier's account team facing penalty clauses.

## How I analyzed it

- **Data I'd pull:** Telematics/GPS actuals vs. planned route sequences, scan timestamps (depart depot, each stop, return), promised windows vs. actual arrival, failed-attempt reasons, and address-quality flags from the order feed.
- **Process mapping:** As-is map from order intake → sort → load → dispatch → delivery → exception handling, with handoff times between sort and dispatch.
- **Root-cause method:** Pareto of late stops by cause code, segmented by route, hour, and geography; a 5 Whys on the worst-performing route; comparison of planned vs. actual stop sequence adherence.
- **Stakeholder questions:** For dispatch — how are routes built and what can change daily? For drivers — where does the plan not match the street? For clients — which windows are hard promises vs. preferences?

## What the analysis found

1. **Routes ignore time windows.** Sequences were optimized for distance only. Drivers regularly arrived at business addresses before opening or after the promised window closed, then had to backtrack — backtracking showed up in GPS data on 7 of 26 routes.
2. **Late departure, not slow driving, starts the chain.** Sort finished on time, but loading was sequenced by route seniority, so the longest routes left last. Routes departing after 8:40 AM accounted for a disproportionate share of late first stops, and lateness compounded through the day.
3. **Address quality creates failed stops.** About 4% of orders arrived with missing apartment/unit numbers or wrong pin locations. Those stops took 3× longer and produced most "customer not available" failures — the customer was home; the driver was at the wrong door.
4. **No recovery mechanism.** When a driver fell behind, nothing rebalanced the route. One traffic incident converted into 20+ late stops because stops were never moved to a nearby driver with slack.

## The fix

**Must have (0–60 days):**
- Rebuild route plans with time-window-aware sequencing; re-plan quarterly and after any client mix change.
- Load and dispatch longest routes first; set a hard departure target per route with a visible board.
- Address validation at order intake (unit-number prompt, pin confirmation for new addresses) so bad addresses are fixed before sort, not at the door.

**Should have (60–120 days):**
- Customer notifications with a live window and safe-drop / neighbor / pickup-point options to cut failed first attempts.
- Dynamic re-routing: when a route runs 30+ minutes behind, the system proposes moving upcoming stops to an adjacent driver.

**Could have:** Photo-on-delivery and geofence check-in to clean up proof-of-delivery disputes.

## Expected impact & how I'd measure it

Projections, validated route-group by route-group (change half the routes first, keep half as control): OTP from 81% to 90–93% in one quarter; failed first attempts from 9% to under 6%; cost per stop down ~5% from fewer backtracks and less overtime.

Measurement plan: weekly OTP and cost-per-stop reporting by route against the 8-week baseline, using the unchanged routes as a comparison group for the first month. Guardrails: driver hours and safety incidents (OTP must not be bought with speeding), and customer complaint rate per 1,000 stops.

## Risks & assumptions

- Client order data quality varies; address validation depends on clients passing unit/pin fields through their checkout.
- Drivers may resist sequence changes; involving two senior drivers in the re-plan is built into the approach.
- Traffic patterns are seasonal; baselines should be re-struck after the first holiday peak.

## What I'd do in the first 30 days

- Join telematics, scan, and order data into one route-level dataset; verify late-stop cause codes with dispatch.
- Ride along on the worst and best routes for a day each to validate what the data says.
- Build the OTP Pareto by route/hour/cause and agree the top three causes with operations.
- Pilot time-window sequencing on four routes and set the comparison method before rollout.
