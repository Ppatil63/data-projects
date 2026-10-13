# Telemedicine Accessibility: Elderly and Low-Vision Patients Can't Complete Booking

**Domain:** Healthcare product / digital accessibility · **Focus:** WCAG-aware redesign, inclusive funnel analysis · **My role in this analysis:** Business Analyst (scenario case study)

## The problem (the business concern)

A telemedicine platform works well for its younger users and fails the patients who often need it most. Older and low-vision patients start booking appointments and abandon partway — many end up calling the clinic anyway, or not getting care. This is simultaneously an accessibility failure, a compliance exposure, and an operations cost, because every failed online booking becomes a phone call or a missed appointment.

Scenario baseline (assumption): Booking completion rate is 86% for patients under 50 but 58% for patients 65+. Average booking task time for 65+ users is 9 minutes vs. 3.5 minutes for younger users. Support calls tagged "help booking" run ~1,100 per month, disproportionately from older patients. A sample accessibility audit of the booking flow found text contrast as low as 3.2:1 on key screens (WCAG AA requires 4.5:1 for normal text), tap targets around 32px, form session timeouts at 10 minutes with no warning, and error messages conveyed by color alone.

Who feels it: patients who need care and can't book it independently, caregivers drafted into tech support, clinic phone staff absorbing avoidable calls, and the organization carrying legal and reputational risk under accessibility obligations.

## How I analyzed it

- **Data I'd pull:** Booking funnel by age band and device (start → provider select → time select → details → confirm → completed), step-level exit and error rates, session timeout duration, support-call tags linked to booking attempts, and the assistive-technology signals analytics can legitimately capture (e.g., OS text-size settings where the platform reports them).
- **Process mapping:** The as-is booking journey as experienced with a screen reader, at 200% text scaling, and by keyboard only — testing the actual experience, not the intended one.
- **Root-cause method:** Structured WCAG 2.2 audit of the booking flow (contrast, target size, focus order, error identification, timeout behavior) combined with moderated usability sessions with 6–8 older/low-vision patients, because analytics shows *where* users fail but only observation shows *why*.
- **Stakeholder questions:** For clinical ops — what is the fallback today when booking fails, and what does it cost? For engineering — is the flow built on a component library, and how old is it? For compliance — which standard are we formally committed to (WCAG 2.2 AA)?

## What the analysis found

1. **Basic visual accessibility failures at the exact steps that matter.** Low contrast on the time-slot grid and confirmation button, 32px tap targets on slot selection, and text that broke layout at 200% scaling — the steps with the highest 65+ exit rates were the steps with the worst audit scores. That alignment is the evidence this is design failure, not user failure.
2. **Timeouts punished slower users.** A 10-minute inactivity timeout with no warning or extension wiped completed form fields. Users who read carefully, use magnification, or get interrupted — precisely this population — were forced to restart, and funnel data showed a second-attempt abandonment cliff.
3. **Errors were incomprehensible.** Validation errors appeared as red borders only (color alone), with no text explanation and no summary; screen-reader users received no announcement at all. Error-recovery, not error occurrence, was where sessions died.
4. **No assisted path existed.** There was no "book by phone with a person" option surfaced in the flow, no caregiver/proxy booking, and no way to save progress — so a stuck patient had exactly one option: give up and call the general line.

## The fix

**Must have (accessibility fundamentals, WCAG 2.2 AA):**
- Raise all text and interactive-element contrast to at least 4.5:1 (3:1 for large text/UI components); minimum 44px tap targets; full layout integrity at 200% text scaling.
- Fix timeout behavior: warn before expiry, allow extension, and preserve entered data across a timeout so nobody restarts from zero.
- Real error handling: text-based error summaries, field-level messages in words, programmatic association for screen readers, and focus moved to the error summary on submit.
- Complete keyboard and screen-reader operability of the whole booking flow, verified with NVDA/JAWS/VoiceOver testing, not just automated scans.

**Should have:**
- Assisted booking paths: a prominent "Prefer to book by phone?" option with a dedicated line, caregiver proxy accounts (book on behalf of a patient with consent), and the option to have a confirmation read/sent via the patient's chosen channel (SMS, email, or automated voice call).
- Simplified booking mode: fewer choices per screen, larger defaults, plain-language labels ("Pick a day" not "Select appointment slot"), and a progress indicator.

**Could have:** Pre-visit tech check for video appointments (camera/mic test with a practice screen) so the accessibility problem isn't simply moved from booking to the visit itself.

## Expected impact & how I'd measure it

Projections, validated by staged rollout and segment-level measurement: 65+ booking completion 58% → 75%+; average 65+ task time 9 → under 6 minutes; "help booking" support calls down ~35%; zero critical WCAG failures in the booking flow on re-audit.

Measurement plan: funnel completion by age band and device reported monthly (never blended — the blended rate hid this problem), plus task-based usability re-testing with the same participant profile each release. Guardrails: completion and task time for under-50 users must not regress; phone-line wait times watched so shifting users to assisted booking doesn't just move the queue; and appointment no-show rates for proxy bookings monitored for consent/confirmation issues.

## Risks & assumptions

- Automated audits catch only part of accessibility issues; budget for manual assistive-technology testing and real user sessions is assumed, not optional.
- Age-band analytics must be handled within privacy policy; if age banding isn't available, recruited usability panels carry more of the evidence load.
- Component-library constraints may make some fixes (target size, scaling) platform-wide changes rather than booking-only — scoping that honestly with engineering is part of the plan.

## What I'd do in the first 30 days

- Produce the age-segmented booking funnel and pinpoint the failing steps.
- Commission/run the WCAG 2.2 audit of the booking flow and reconcile findings against funnel exits.
- Recruit and run 6–8 moderated sessions with older and low-vision patients; write up observed failure points with clips/quotes.
- Draft requirements (user stories + accessibility acceptance criteria per story) and the measurement plan for the fix backlog, sequenced Must/Should with clinical ops and compliance sign-off.
