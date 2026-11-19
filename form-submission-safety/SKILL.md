---
name: form-submission-safety
description: Submit a web form containing the user's personal data on their behalf — prize campaigns and sweepstakes, registrations, applications — without leaking data or entering through the wrong door. Use when asked to enter, apply, register, or submit anything that sends the user's name, address, phone, or email to a third party. Covers verifying the organizer and the official route, surveying the real form before collecting data, minimal-data collection, CAPTCHA and proxy-entry rules, per-submission confirmation, and entry records.
---

# Form submission safety

Submitting a form on the user's behalf sends their personal data to a third
party. The failures this skill prevents: entering through a phishing
lookalike, collecting more data than the form needs, submitting something
the user never saw, and losing track of what was sent where. Prize
campaigns （懸賞） are the worked example throughout; the protocol applies to
any consequential form.

Never write the user's personal details into this skill or any working
file. Personal values live only in the form itself and in the entry record
(field categories, not full values — see "Track each submission").

## 1. Verify the organizer and the official route

- Confirm the organizer is a real body or company, from its own official
  site plus one independent source (a press release, a news article, an
  official registry).
- Enter only through the link on the official site — never through an
  aggregator's redirect or a lookalike proxy page. Follow the form service
  to its actual host and check it matches what the official page describes.
- Take deadlines and conditions from the official announcement, not the
  aggregator. (Verified case: an aggregator showed Nov 26 while the
  official release said Nov 30 — the official source wins, and the
  correction is worth telling the user.)
- Read the terms before entering:
  - **If the terms prohibit automated or proxy entry, do not enter.** Tell
    the user, and offer to prepare everything (answers, field values) for
    them to submit manually.
  - How duplicate entries are treated (entries may be accepted while wins
    are capped at one per person).
  - How winners are announced (some campaigns substitute prize shipment for
    any notification).
- Stop signals at any step: the form asks for payment, asks for personal
  data beyond what the stated purpose needs, or sits on a host that does
  not match the official page. Stop and report what you verified and where
  it stopped, rather than switching to an unofficial route.

## 2. Survey the form before asking for anything

- Open the actual entry form first and enumerate every required field, any
  quiz or question and its confirmable answer, and whether an image CAPTCHA
  or reCAPTCHA is present.
- **CAPTCHA rule: never attempt to solve or bypass one.** Hand that step to
  the user and continue from where they leave off.
- Only then ask the user for the personal data that is missing, in one
  batch, naming exactly which fields are needed. Do not ask for anything
  the form does not require, and do not start filling before the required
  set is known.
- Leave optional survey questions empty unless the user wants them
  answered. For "how did you hear about us", answer honestly (for example,
  the aggregator site where the campaign was found).

## 3. Enter, confirm, submit

- Fill the form and advance to the confirmation screen. Show the user the
  complete contents exactly as they will be sent, including any display
  quirks worth a note (for example, spacing collapsed in an address line).
- Submit only after the user's explicit OK on that shown content. A general
  "try to automate entries" instruction does not replace the per-submission
  confirmation.
- After submitting, report the completion evidence exactly as shown: the
  completion message, and whether a receipt number or confirmation email
  exists. Some campaigns issue neither; say so plainly, with the announced
  results or prize-shipment timing.

## 4. Classify blockers when collecting candidates

- Plain web forms: fully completable with the flow above. Prioritize these.
- Entries tied to a messaging or social account the user must operate
  (follow-and-repost campaigns, app-based entries), entries that need the
  user's own account login, and entries that require an actual purchase
  (receipt campaigns) cannot be completed by the agent alone. Flag them
  when collecting candidates, prepare whatever can be prepared, and hand
  over at the point the user's own account or purchase is needed.

## 5. Track each submission

- Keep one entry record (a single file or table for all submissions, in a
  fixed place) with: campaign name, organizer, what was submitted (quiz
  answer and field categories, not full personal values), date submitted,
  deadline, and the expected announcement or shipment timing — so
  duplicates can be checked and follow-ups answered.
- If a submission cannot be completed or a campaign turns out unreachable
  or unsafe, record where it stopped as well; an unrecorded dead end gets
  retried next time.
