#!/usr/bin/env python3
"""Sync every bundled copy of a dataset from one single source.

Skeleton for the bundled-data-sync skill. Adapt the CONFIG section, the
validate() rules, and the list of copies to your project, then keep the
adapted script beside the source file.

Guarantees:
  - validation runs before anything is written;
  - every copy is backed up before it is rewritten, and all copies are
    rolled back if any write or check fails;
  - after writing, every copy is compared field by field with the source;
  - the canonical content hash of the source is printed, so the caller can
    archive the previous version under its key before syncing.
"""
import hashlib
import json
import shutil
import sys
from pathlib import Path

# --- CONFIG (adapt these) -------------------------------------------------
SOURCE = Path("data/catalog.json")
COPIES = [
    Path("app/catalog.json"),
    Path("worker/catalog.json"),
    Path("replay/catalog.json"),
]
BACKUP_SUFFIX = ".bak"


def canonical_bytes(data) -> bytes:
    """Canonical serialization for the content hash.

    Keys sorted, fixed separators, UTF-8, numbers as parsed by json.
    If your data carries display-only fields that must NOT change the key,
    strip them here — and write that decision down in the project docs.
    """
    return json.dumps(
        data, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")


def content_key(data) -> str:
    return hashlib.sha256(canonical_bytes(data)).hexdigest()[:12]


def validate(data) -> None:
    """Project-specific checks. Raise ValueError on the first problem."""
    if not isinstance(data, list):
        raise ValueError("dataset must be a list of records")
    ids = [rec.get("id") for rec in data]
    if any(i is None for i in ids):
        raise ValueError("a record is missing its id")
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate ids in dataset")
    # Add project rules here: unknown references, per-item repeat limits, ...


def main() -> int:
    source_data = json.loads(SOURCE.read_text(encoding="utf-8"))
    validate(source_data)
    key = content_key(source_data)
    print(f"source: {SOURCE}  records={len(source_data)}  key={key}")

    backups = {}
    try:
        for copy in COPIES:
            if copy.exists():
                bak = copy.with_suffix(copy.suffix + BACKUP_SUFFIX)
                shutil.copy2(copy, bak)
                backups[copy] = bak
            copy.parent.mkdir(parents=True, exist_ok=True)
            copy.write_bytes(canonical_bytes(source_data))
        # Post-sync check: every copy must equal the source, field by field.
        for copy in COPIES:
            got = json.loads(copy.read_text(encoding="utf-8"))
            if got != source_data:
                raise ValueError(f"post-sync mismatch: {copy}")
    except Exception as exc:  # roll everything back
        for copy, bak in backups.items():
            shutil.copy2(bak, copy)
        print(f"FAILED, rolled back: {exc}", file=sys.stderr)
        return 1
    print(f"synced {len(COPIES)} copies, all verified. key={key}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
