#!/usr/bin/env python3
"""Read-only provenance and supplied-semantics integrity checks."""

from __future__ import annotations

import hashlib
import os
from pathlib import Path


CANDIDATE = Path("/candidate")
REFERENCE = Path("/reference")


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def tree_entries(root: Path):
    result = {}
    for directory, dirnames, filenames in os.walk(root, followlinks=False):
        directory_path = Path(directory)
        for name in sorted(dirnames + filenames):
            path = directory_path / name
            rel = path.relative_to(root).as_posix()
            if path.is_symlink():
                kind = "symlink"
            elif path.is_dir():
                kind = "directory"
            elif path.is_file():
                kind = "file"
            else:
                kind = "other"
            result[rel] = (kind, digest(path) if kind == "file" else None)
    return result


def compare_file(candidate: Path, reference: Path, label: str) -> None:
    if not candidate.exists() and not candidate.is_symlink():
        print(f"{label}: MISSING candidate={candidate}")
        return
    if candidate.is_symlink():
        print(f"{label}: INTEGRITY_FAILURE symlink={candidate}")
        return
    if not candidate.is_file():
        print(f"{label}: INTEGRITY_FAILURE mistyped={candidate}")
        return
    same = candidate.read_bytes() == reference.read_bytes()
    print(
        f"{label}: {'IDENTICAL' if same else 'CHANGED'} "
        f"candidate_sha256={digest(candidate)} reference_sha256={digest(reference)}"
    )


def main() -> int:
    print("rendered_semantics_mode=SUPPLIED_SEMANTICS")
    trusted_semantics = REFERENCE / "reference-semantics"
    print(
        "trusted_semantics_boundary="
        + ("PRESENT" if trusted_semantics.is_dir() and not trusted_semantics.is_symlink() else "BREACH")
    )

    for path in sorted(CANDIDATE.rglob("*")):
        if path.is_symlink():
            print(f"candidate_symlink=INTEGRITY_FAILURE path={path}")
    print(
        "candidate_symlink_count="
        + str(sum(1 for path in CANDIDATE.rglob("*") if path.is_symlink()))
    )

    compare_file(CANDIDATE / "prompt.py", REFERENCE / "prompt.py", "prompt")
    compare_file(CANDIDATE / "py2mpy.py", REFERENCE / "py2mpy.py", "translator")

    candidate_entries = tree_entries(CANDIDATE / "reference-semantics")
    reference_entries = tree_entries(trusted_semantics)
    all_names = sorted(set(candidate_entries) | set(reference_entries))
    differences = []
    for name in all_names:
        candidate_value = candidate_entries.get(name)
        reference_value = reference_entries.get(name)
        if candidate_value != reference_value:
            differences.append((name, candidate_value, reference_value))
    print(f"semantics_entry_count={len(candidate_entries)}")
    print(f"semantics_integrity_difference_count={len(differences)}")
    for name, candidate_value, reference_value in differences:
        print(
            "semantics_difference "
            f"path={name} candidate={candidate_value!r} reference={reference_value!r}"
        )

    named_records = [
        "run-input.json",
        "metrics.json",
        "codex-last.txt",
        "codex-output.log",
    ]
    for name in named_records:
        path = CANDIDATE / name
        if path.is_symlink():
            status = "SYMLINK_INTEGRITY_FAILURE"
        elif path.is_file():
            status = "PRESENT"
        elif path.exists():
            status = "MISTYPED"
        else:
            status = "MISSING"
        print(f"generation_record name={name} status={status}")

    trace_candidates = sorted(
        path.relative_to(CANDIDATE).as_posix()
        for path in CANDIDATE.rglob("*")
        if path.is_file()
        and (
            "trace" in path.name.lower()
            or path.suffix.lower() in {".jsonl", ".ndjson"}
        )
    )
    print(f"structured_trace_candidates={trace_candidates!r}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
