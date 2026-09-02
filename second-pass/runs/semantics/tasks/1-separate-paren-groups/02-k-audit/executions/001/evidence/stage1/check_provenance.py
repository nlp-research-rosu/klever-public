#!/usr/bin/env python3
"""Reviewer-authored provenance and supplied-semantics integrity check."""

from __future__ import annotations

import hashlib
import os
from pathlib import Path


CANDIDATE = Path("/candidate")
REFERENCE = Path("/reference")
REQUIRED_CLAIMS = (
    "run-input.json",
    "metrics.json",
    "codex-last.txt",
    "codex-output.log",
)


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def tree(root: Path) -> dict[str, tuple[str, str | None]]:
    entries: dict[str, tuple[str, str | None]] = {}
    for directory, dirnames, filenames in os.walk(root, followlinks=False):
        base = Path(directory)
        for name in sorted(dirnames + filenames):
            path = base / name
            relative = str(path.relative_to(root))
            if path.is_symlink():
                entries[relative] = ("symlink", os.readlink(path))
            elif path.is_dir():
                entries[relative] = ("directory", None)
            elif path.is_file():
                entries[relative] = ("file", digest(path))
            else:
                entries[relative] = ("other", None)
    return entries


def main() -> int:
    print("rendered_mode=SUPPLIED_SEMANTICS")
    trusted_semantics = REFERENCE / "reference-semantics"
    print(f"trusted_semantics_present={trusted_semantics.is_dir()}")

    candidate_manifest = tree(CANDIDATE)
    for relative, entry in sorted(candidate_manifest.items()):
        print(f"candidate_manifest {relative}: {entry!r}")

    for relative in REQUIRED_CLAIMS:
        path = CANDIDATE / relative
        print(f"required_claim_artifact {relative}: present={path.exists()} symlink={path.is_symlink()}")

    for relative in (
        "prompt.py",
        "py2mpy.py",
        "solution.py",
        "solution.mpy",
        "spec.k",
        "verification.k",
    ):
        entry = candidate_manifest.get(relative)
        print(f"required_source_artifact {relative}: entry={entry!r}")

    traces = sorted(
        path.name
        for path in CANDIDATE.iterdir()
        if "trace" in path.name.lower()
    )
    print(f"structured_trace_candidates={traces!r}")

    failures: list[str] = []
    for relative in ("prompt.py", "py2mpy.py"):
        trusted = REFERENCE / relative
        submitted = CANDIDATE / relative
        if not submitted.exists():
            failures.append(f"missing candidate {relative}")
        elif submitted.is_symlink():
            failures.append(f"symlinked candidate {relative}")
        elif submitted.read_bytes() != trusted.read_bytes():
            failures.append(f"changed candidate {relative}")
        print(
            f"{relative}: trusted_sha256={digest(trusted)} "
            f"candidate_sha256={digest(submitted) if submitted.is_file() else 'N/A'}"
        )

    trusted_tree = tree(trusted_semantics)
    submitted_tree = tree(CANDIDATE / "reference-semantics")
    all_paths = sorted(set(trusted_tree) | set(submitted_tree))
    for relative in all_paths:
        trusted_entry = trusted_tree.get(relative)
        submitted_entry = submitted_tree.get(relative)
        if trusted_entry != submitted_entry:
            failures.append(
                f"semantics mismatch {relative}: trusted={trusted_entry!r} "
                f"candidate={submitted_entry!r}"
            )

    print(f"trusted_semantics_entries={len(trusted_tree)}")
    print(f"candidate_semantics_entries={len(submitted_tree)}")
    print(f"integrity_failure_count={len(failures)}")
    for failure in failures:
        print(f"INTEGRITY_FAILURE: {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
