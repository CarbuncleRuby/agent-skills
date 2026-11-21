---
name: branch-point-check
description: "At the start of a new task or project, before hands-on work begins, identify the important branch points — the places where the work should stop for the user's decision — and present them for confirmation alongside the plan. A branch point is a step that is expensive to get wrong: irreversible, outward-facing (sending, publishing, submitting, paying), a direction decision that shapes everything after it, or a large consumption of time, money or compute. Use this when a new multi-step piece of work begins. Do not use it for a continuation of work whose branch points were already agreed, for a single trivial step, or to manufacture checkpoints where none exist — if there are no branch points, say so in one line and proceed."
---

# Branch Point Check

Agreed with the user on 2026-11-14, in their words: 「どこで止まるべきかが一番大事」 — where to stop matters most. Naming the stop-points at the start is what makes everything between them safe to do autonomously: the user can correct the plan at the one moment correction is cheap, and never has to wonder whether an irreversible step is about to happen unannounced.

## Procedure

1. **Scan the planned work for branch points.** A step qualifies if it is:
   - **Irreversible**, or reversible only at real cost (deleting the only copy, overwriting a canonical file, sending something that cannot be unsent)
   - **Outward-facing** — it leaves the workspace: messages or mail sent, posts published, applications submitted, purchases made
   - **A direction decision** — a choice of approach, scope, or design that the rest of the work builds on
   - **A large resource consumption** — a long run, a big download, a heavy token spend. Rule of thumb: a step whose cost (time, money, compute, tokens) would be clearly wasted if the direction turned out wrong — more than it would cost to ask
2. **Present them with the kickoff report**: what will be done, the conditions, the time estimate — plus the branch points, each in one line: the step, and the decision the user will be asked for there. The kickoff report itself is not a stop unless the first step is a branch point: begin the reversible work immediately, and stop at the first listed branch point; if the user corrects the plan in the meantime, adjust.

   Kickoff report, three lines:
   ```
   Plan: … / Conditions: … / Estimate: ~40 min
   Branch points: (1) after the pilot run — choose the full grid or a reduced one; (2) before publishing the results page — final OK.
   ```
3. **Then proceed autonomously between branch points.** Work that is spec-fixed, reversible, and verifiable does not stop for confirmation; that is the other half of the agreement, and stopping there anyway breaks it.
4. **If a new branch point appears mid-task** that was not foreseeable at kickoff, stop there and check, even if it was not on the original list. Report direction changes as they happen, not at the end.

## Calibration

- The list should be short. A typical task has zero to three real branch points; a long list means criteria are being applied to ordinary steps.
- A branch point is a decision the **user** owns. Technical choices with a verifiable right answer are not branch points — make them, and report the reasoning.
- While waiting at a branch point, continue only work that does not depend on the decision and is reversible. Never take the branch-point step by default because no answer came.
- Do not re-litigate agreed branch points when work resumes after an interruption; the agreement stands until the plan itself changes.
