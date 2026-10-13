# Hospital Outpatient Scheduling: No-Shows and Long Waits

**Domain:** Healthcare operations · **Focus:** Appointment scheduling, reminder systems, and clinic flow · **My role in this analysis:** Business Analyst (scenario case study)

## The problem (the business concern)

A hospital's outpatient clinics run a frustrating paradox: patients wait weeks for an appointment and then wait again in the lobby, while roughly one in four booked slots goes unused because the patient never shows up. Providers end days late, front-desk staff absorb patient anger, and unused slots mean other patients wait longer for care.

Scenario baseline (assumption): ~420 appointments per day across 6 clinics. No-show rate is 23%. Average in-clinic wait is 38 minutes past appointment time. Schedule utilization is 74% of provider time actually spent with patients. Clinics run an average of 45 minutes late by end of day, and staff overtime is a recurring budget problem.

Who feels it: patients (especially those traveling far or taking unpaid time off), providers whose days overrun, front-desk teams managing the fallout, and the patients still on the waitlist for the wasted slots.

## How I analyzed it

- **Data I'd pull:** 12 months of appointment data — booked lead time, appointment type and duration booked vs. actual, no-show and late-cancel flags, arrival vs. appointment vs. rooming timestamps, reminder sends, and patient segment attributes the data governance allows (clinic, visit type, lead time band, prior no-show history).
- **Process mapping:** As-is patient flow: referral → booking → reminders → check-in → waiting → consult → checkout/rebook, with the paperwork steps that delay rooming.
- **Root-cause method:** Segmentation analysis of no-show rate (by lead time, visit type, day/time, prior behavior) to find where no-shows concentrate — an average of 23% usually hides segments at 5% and segments at 45%; logistic reasoning on the pattern plus front-desk interviews.
- **Stakeholder questions:** For clinic managers — which sessions chronically overrun and why? For front desk — what do patients actually say when they no-show or arrive late? For providers — which visit types genuinely need longer slots?

## What the analysis found

1. **Lead time drives no-shows.** Appointments booked 30+ days out no-showed at ~34%, vs. ~11% for appointments within a week. The schedule was filled far ahead, which guaranteed a high no-show mix — a booking-policy problem, not a patient-behavior problem.
2. **Reminders were inconsistent.** Two clinics sent no reminders at all; others sent one reminder 7 days out — too early to act on. Where a 48-hour reminder existed, no-shows ran several points lower, but there was no confirmation step, so clinics couldn't backfill slots patients already knew they'd miss.
3. **One slot length for every visit type.** New-patient consults, follow-ups, and quick reviews were all booked into identical 20-minute slots, but actual consult times averaged 31, 17, and 9 minutes respectively. New-patient-heavy sessions structurally overran, producing the 38-minute waits and end-of-day cascade.
4. **Front-end delays stack at check-in.** Insurance/referral paperwork was verified at arrival rather than before the visit; a minority of patients with missing paperwork created a queue that delayed everyone behind them.

## The fix

**Must have (0–60 days):**
- Standard reminder cadence for all clinics: confirmation request at 72 hours and a reminder at 24 hours (SMS first, call for patients who don't use SMS), with one-tap cancel/reschedule so freed slots surface early.
- Slot templates by visit type: 30-minute new consults, 20-minute follow-ups, 10-minute reviews, based on measured consult times — stop booking fiction.
- Pre-visit paperwork and insurance verification 48 hours ahead, with a phone queue to fix exceptions before arrival day.

**Should have (60–120 days):**
- Segmented overbooking: overbook only the segments with proven high no-show rates (long lead time, prior no-show history), capped so a full-show day creates manageable waits, never blanket double-booking.
- Waitlist backfill: when a slot frees via cancellation, auto-offer it to waitlisted patients in the same visit type, shortest lead time first.
- Release a portion of follow-up slots only 7–14 days out, shortening lead time for the highest no-show segment.

**Could have:** Same-day open slots held for urgent referrals, managed by the clinic coordinator.

## Expected impact & how I'd measure it

Projections, piloted in two clinics first with the other four as comparison: no-show rate 23% → ~14%; provider utilization 74% → ~85%; average wait 38 → ~20 minutes; end-of-day overrun largely eliminated on templated sessions.

Measurement plan: weekly clinic-level dashboard of no-show rate, utilization, and wait times vs. the 12-week baseline, reported by segment so averages can't hide harm to one group. Guardrails: patient complaints and wait times on full-show days (overbooking's cost), provider overtime (utilization must not be bought with longer days), and equity checks — reminder and overbooking policies must not systematically disadvantage elderly or non-English-speaking patients; phone-based confirmation stays available.

## Risks & assumptions

- SMS reminder gains assume most patients have a mobile number on file; data cleanup on contact details is a prerequisite.
- Overbooking is politically sensitive; clinical leadership must own the cap and the full-show-day protocol, not the scheduling team alone.
- Consult-time data assumes timestamps are recorded honestly; a short time-study validates before templates change.

## What I'd do in the first 30 days

- Build the 12-month appointment dataset and produce no-show segmentation by lead time, visit type, and clinic.
- Run a 1-week time study in two clinics to measure true consult durations by visit type.
- Map the reminder reality clinic-by-clinic against policy.
- Draft the slot-template and reminder-cadence pilot with clinic managers, including guardrail metrics and a go/no-go date.
