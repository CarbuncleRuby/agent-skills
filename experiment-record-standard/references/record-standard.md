# Record standard for publication-candidate experiments

Why keep records in a fixed shape from the start, and what the shape is.
Derived from the cost of retrofitting this structure onto a finished project.

## Why from the start

Retrofitting is possible but expensive. In the project this standard was
distilled from:

- The status document mixed decisions with the work log, so recovering the
  decision timeline took a separate extraction pass.
- Terms multiplied and drifted during the project, so building the registry
  afterwards meant resolving dozens of issues (homonyms, definitions that no
  longer matched how the term was used).
- Numbers were scattered across documents, so cross-checking them against
  their sources was manual work every time.

Deciding the shape up front removes nearly all three costs.

## Scope

- Applies to experiments that may become a paper, thesis chapter, or report.
- Scratch trials and throwaway checks are out of scope.
- When an experiment becomes a publication candidate mid-flight, switch its
  records to this standard at that point.

## The five records

1. **Claims ledger** — one claim per row: claim / confirmation status
   (confirmatory, exploratory, retracted) / value / provenance / canonical
   reference / caveats. Prose numbers always come from the ledger.
   - Confirmatory = hypothesis and procedure frozen before a single
     evaluation on unseen data. Exploratory = found by looking at the data.
     The distinction is decided-first vs. seen-first, not result quality.
2. **Canonical JSON** — one machine-readable source of truth per run, holding
   at least: run ID, config or config hash, seed(s), data split, metric
   names, code commit. File names and JSON keys are identifiers and are
   never renamed.
3. **Term registry** — the main terms to start (method names, concepts,
   evaluation terms). Each term: stable ID, definition, aliases, and the
   corresponding code identifiers / JSON keys. Renames and concept changes
   are absorbed by versioning the registry; IDs and code identifiers never
   change.
4. **Decision log** — decisions only, in chronological order: date / what was
   decided / grounds / whose decision. Never mixed with the work log or
   progress notes.
5. **Retracted list** — retracted expressions are never deleted; they are
   kept as "old wording → correct form → grounds". If the records are later
   checked or queried automatically, this list serves as the blocklist of
   statements that must no longer be produced.

## Operating rules

- Frozen documents (preregistrations, freeze records) are never rewritten;
  corrections are new dated entries.
- Side experiments outside the main line carry an explicit "author's play"
  label; unlabeled, they cannot be told apart later.
- Third-party papers and materials are recorded as bibliography only.
- A periodic consistency check (weekly is enough) compares the working
  records against the registry and the canonical JSONs: unregistered terms,
  homonyms, definition drift, numbers that disagree with the canonical JSON.
  The check reports; it does not edit.

## What this buys later

- With the ledger, registry, and canonical JSONs in place, freezing a
  snapshot of the records (for release, audit, or reuse) is a copying step,
  not an archaeology project.
- With the decision log separated, the author's reasoning can be cited and
  reviewed without digging through work notes.
- With the retracted list, an automated checker can stop retracted claims
  from being reproduced.
