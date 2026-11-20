---
name: experiment-record-standard
description: Set up experiment records from day one so results stay traceable and reusable — a claims ledger with confirmation status (confirmatory / exploratory / retracted), canonical run JSONs, a term registry with stable IDs, a decision log kept separate from the work log, and a retracted-expressions list. Use when starting an experiment that may become a paper, thesis chapter, or technical report, or when an ongoing experiment becomes a publication candidate.
---

# Experiment Record Standard

Keep records from the start of any publication-candidate experiment, in a form
where every number in prose can be traced to one canonical source and every
claim carries its confirmation status. Retrofitting this structure is possible
but expensive: in the author's own project, retrofitting required a separate
extraction pass to recover the decision timeline from a mixed work log, and a
128-term registry with 31 terminology issues (homonyms, drifted definitions)
to clean up after the fact. Setting the shape up front makes most of that
cost disappear.

The full standard, with rationale, is in
[references/record-standard.md](references/record-standard.md). Templates for
the five records are in [templates/](templates/). This skill carries the
trigger, the scaffolding steps, and the operating rules.

## When this applies

- A new experiment that could plausibly become a paper, thesis chapter, or
  technical report.
- An ongoing experiment that has just become a publication candidate — switch
  its records to this standard at that point.
- Not for scratch trials or throwaway checks.

## Scaffolding (do this at the start, before results accumulate)

Create these five records in the project folder:

1. **Claims ledger** (`CLAIMS-LEDGER.md`): one claim per row. Columns:
   claim （主張） / confirmation status （確認度） / value （数値） /
   provenance （出自） / canonical reference （正本への参照） / caveats （留保）.
   Confirmation status is one of:
   - **confirmatory （確認的）** — hypothesis and procedure were frozen before
     a single evaluation on unseen data;
   - **exploratory （探索的）** — found by looking at the data;
   - **retracted （撤回）** — withdrawn; see the retracted list.
   The distinction is "decided first vs. seen first", not result quality.
   Rule: every number that appears in prose is taken from the ledger, never
   directly from a results file.
2. **Canonical JSON**: one machine-readable source of truth per experiment
   run. Ledger and prose numbers are drawn from it. File names and JSON keys
   are identifiers — never rename them later. Minimum schema per run:
   run ID, config (or its hash), seed(s), data split, metric names and
   definitions, and the code commit the run was produced with.
3. **Term registry**: start with the main terms only (method names, concepts,
   evaluation terms). Each term gets a stable ID, a definition, aliases, and
   the corresponding code identifiers / JSON keys. Renames and concept changes
   are absorbed by versioning the registry; IDs and code identifiers never
   change.
4. **Decision log**: decisions only, chronological — date / what was decided /
   grounds / whose decision. Never mix with the work log or progress notes.
5. **Retracted list**: never delete a retracted expression; keep it as
   "old wording → correct form → grounds". If the records are later used by
   an automated checker or a question-answering layer, this list becomes its
   blocklist verbatim.

## Operating rules

- Frozen documents (preregistrations, freeze records) are never edited after
  the fact. Corrections go in new dated entries.
- Side experiments outside the main line are recorded with an explicit
  "author's play" label — unlabeled, they become indistinguishable later.
- Other people's papers and materials enter the records as bibliography only
  (no full-text redistribution).
- Confirmation status is part of the claim: never let prose upgrade an
  exploratory result to confirmatory, or soften a retraction. Caveats (data
  fold, point estimate, single seed, evaluation scope) travel with the
  numbers wherever they are quoted.
- Periodically check the working records against the registry and the
  canonical JSONs: unregistered new terms, ambiguous homonyms, definition
  drift not propagated to the ledger, numbers disagreeing with the canonical
  JSONs. A weekly automated or manual pass is enough; the check reports
  problems and never edits the records itself.

## Later stages (pointers, not part of this skill)

- When writing up, bind each manuscript number back to its ledger row and
  canonical JSON key, so a reader (or a checker) can trace any printed value
  to its source.
- Freezing a corpus snapshot of the records (for release, audit, or reuse by
  other tools) is a separate step; the five records above are what make that
  step cheap when it comes.
