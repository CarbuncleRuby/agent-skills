---
name: bundled-data-sync
description: Keep one dataset consistent when it is copied into several bundles of an app or static site — a main app, workers, a replay engine — and archive each version under a content hash so saved replays and histories keep playing. Use when the same catalog, deck list, level data, or other records live in more than one file or bundle, when copies have drifted, or before changing data that saved replays depend on. Keywords — duplicated data, catalog, worker copy, replay, out of sync, content hash.
---

# Bundled data sync and archive

One dataset often ends up copied into several places: the main bundle, a
worker, a replay engine, a static export. The copies drift silently, and the
failure surfaces late — in one real case a rarity was added to one of five
copies of a card catalog, 21 cards went missing from the others, the copies'
version keys diverged, and a saved tournament replay broke. This skill is
the procedure that prevents that class of failure.

## Step 0: try to remove the duplication

Duplication is the problem; syncing is the workaround. Before maintaining
copies, check whether they can share one source:

- a build-time bundle step that generates each copy from the source;
- a shared module import (workers can `importScripts` or load an ES module —
  "workers cannot share memory" is true but does not force a hand-maintained
  copy);
- a generated file checked into each bundle by the build.

Only when a copy genuinely must be self-contained (an offline bundle, a
frozen export) do the sync steps below apply.

## Step 1: inventory every copy

- Search the whole project for the dataset before changing any value, and
  list every file that holds a copy.
- Record the full copy list in the delivery report, so the next edit starts
  from the same list.

## Step 2: change the single source and sync

- Pick one file as the single source for the dataset, and edit only that
  file. Never edit one copy by hand to fix a drift — a hand edit becomes
  the next drift.
- Sync with a script, not by hand. A skeleton is in
  [scripts/sync_data.py](scripts/sync_data.py); keep the adapted script
  beside the source file. The script must:
  - validate the data *before* writing anything (counts, unknown
    identifiers, per-item limits such as how many times one item may
    repeat);
  - back up every copy before applying a change, and roll back from the
    backup when any write or check fails;
  - rewrite every copy from the single source;
  - re-check the copies field by field after writing.

## Step 3: archive the old version before a change

- Archive the current version before you change any value, even when the
  change looks display-only.
- Store the archive under a key that identifies its contents: a hash of the
  canonical serialization of the data. Canonical means: object keys sorted,
  fixed separators, UTF-8 encoding, a stated number formatting, and a stated
  set of included fields (decide whether display-only fields change the
  key, and write the decision down). Without a canonical form, two
  "identical" copies produce different keys — which is exactly the symptom
  this skill exists to debug.
- Keep the archive reachable from the site itself (e.g. a `catalogs/`
  folder with one file per key) when saved replays must play without an
  external archive server.
- Playback uses the archived version when the recorded key differs from the
  current data; new replays use the current data.
- **Decide the missing-key case in advance.** If a replay asks for a key
  that is not in the archive, fail loudly and say which key is missing —
  silently substituting current data rewrites history. Record the decision
  with the archive layout.

Example layout:

```
data/catalog.json          <- single source
tools/sync_catalog.py      <- sync script (adapted from the skeleton)
catalogs/<hash>.json       <- one archived version per content hash
```

## Step 4: verify in the running app

- Compute the identifying key from each copy in the running app, and
  confirm that every copy reports the same key.
- Play a saved replay that used the old data, and start a new replay on the
  latest data, before you report the change complete.
- Report a copy that still differs as a failed item, and fix it through the
  single source and the sync script rather than by patching the copy.

## Alternatives

- Split a large dataset change into a small first change, and verify the
  sync and the archive on that change before applying the rest.
- Ask the user which version saved replays should keep when a change would
  alter old results, before you archive or replace the data.
