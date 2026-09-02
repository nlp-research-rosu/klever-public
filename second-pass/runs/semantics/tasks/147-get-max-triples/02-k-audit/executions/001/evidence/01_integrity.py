#!/usr/bin/env python3
"""Independent provenance and supplied-semantics integrity checks."""

from __future__ import annotations

import hashlib
import os
from pathlib import Path


CANDIDATE = Path("/candidate")
REFERENCE = Path("/reference")


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(65536), b""):
            value.update(block)
    return value.hexdigest()


def kind(path: Path) -> str:
    if path.is_symlink():
        return "symlink"
    if path.is_file():
        return "file"
    if path.is_dir():
        return "directory"
    return "other"


def inventory(root: Path) -> dict[str, tuple[str, str | None]]:
    result: dict[str, tuple[str, str | None]] = {}
    for current, directories, files in os.walk(root, followlinks=False):
        current_path = Path(current)
        for name in sorted(directories + files):
            path = current_path / name
            relative = path.relative_to(root).as_posix()
            path_kind = kind(path)
            result[relative] = (
                path_kind,
                digest(path) if path_kind == "file" else None,
            )
    return result


def compare_file(candidate: Path, reference: Path) -> None:
    print(f"COMPARE_FILE candidate={candidate} reference={reference}")
    if not candidate.exists() and not candidate.is_symlink():
        print("RESULT missing-candidate")
        return
    print(f"CANDIDATE_KIND {kind(candidate)}")
    print(f"REFERENCE_KIND {kind(reference)}")
    if kind(candidate) == "file" and kind(reference) == "file":
        print(f"CANDIDATE_SHA256 {digest(candidate)}")
        print(f"REFERENCE_SHA256 {digest(reference)}")
        print(f"BYTE_IDENTICAL {candidate.read_bytes() == reference.read_bytes()}")


def main() -> int:
    print("SEMANTICS_MODE SUPPLIED_SEMANTICS")
    trusted_semantics = REFERENCE / "reference-semantics"
    print(f"TRUSTED_SEMANTICS_PRESENT {trusted_semantics.is_dir()}")

    compare_file(CANDIDATE / "prompt.py", REFERENCE / "prompt.py")
    compare_file(CANDIDATE / "py2mpy.py", REFERENCE / "py2mpy.py")

    candidate_items = inventory(CANDIDATE / "reference-semantics")
    reference_items = inventory(trusted_semantics)
    all_names = sorted(set(candidate_items) | set(reference_items))
    differences = 0
    print(f"SEMANTICS_REFERENCE_ENTRY_COUNT {len(reference_items)}")
    print(f"SEMANTICS_CANDIDATE_ENTRY_COUNT {len(candidate_items)}")
    for name in all_names:
        left = candidate_items.get(name)
        right = reference_items.get(name)
        if left != right:
            differences += 1
            print(f"SEMANTICS_DIFFERENCE {name} candidate={left} reference={right}")
    print(f"SEMANTICS_DIFFERENCE_COUNT {differences}")

    for name in (
        "run-input.json",
        "metrics.json",
        "codex-last.txt",
        "codex-output.log",
    ):
        path = CANDIDATE / name
        print(f"GENERATION_METADATA {name} {kind(path) if path.exists() or path.is_symlink() else 'missing'}")

    trace_candidates = sorted(
        path
        for path in CANDIDATE.iterdir()
        if path.is_file()
        and ("trace" in path.name.lower() or path.suffix in {".json", ".jsonl"})
    )
    print(
        "STRUCTURED_TRACE_CANDIDATES "
        + (", ".join(str(path) for path in trace_candidates) if trace_candidates else "none")
    )

    required_sources = (
        "prompt.py",
        "py2mpy.py",
        "solution.py",
        "solution.mpy",
        "spec.k",
        "verification.k",
    )
    for name in required_sources:
        path = CANDIDATE / name
        print(f"REQUIRED_SOURCE {name} {kind(path) if path.exists() or path.is_symlink() else 'missing'}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
