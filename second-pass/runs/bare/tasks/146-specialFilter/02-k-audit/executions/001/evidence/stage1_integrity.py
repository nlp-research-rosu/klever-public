#!/usr/bin/env python3
"""Independent source/type/provenance checks for audit stage 1."""

from __future__ import annotations

import hashlib
from pathlib import Path


CANDIDATE = Path("/candidate")
REFERENCE = Path("/reference")

REQUIRED = [
    "run-input.json",
    "metrics.json",
    "codex-last.txt",
    "codex-output.log",
    "prompt.py",
    "py2mpy.py",
    "solution.py",
    "solution.mpy",
    "semantic.k",
    "spec.k",
    "verification.k",
]


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def kind(path: Path) -> str:
    if path.is_symlink():
        return "symlink"
    if path.is_file():
        return "regular-file"
    if path.is_dir():
        return "directory"
    if path.exists():
        return "other"
    return "missing"


def main() -> int:
    print("mode=GENERATED_SEMANTICS")
    print(f"reference-semantics={kind(REFERENCE / 'reference-semantics')}")
    for rel in REQUIRED:
        path = CANDIDATE / rel
        label = kind(path)
        suffix = f" sha256={digest(path)}" if label == "regular-file" else ""
        print(f"required {rel}: {label}{suffix}")

    traces = sorted(CANDIDATE.glob("codex-trace/**/*.jsonl"))
    print(f"structured-trace-count={len(traces)}")
    for path in traces:
        print(f"trace {path.relative_to(CANDIDATE)}: {kind(path)} sha256={digest(path)}")

    for name in ("prompt.py", "py2mpy.py"):
        candidate = CANDIDATE / name
        trusted = REFERENCE / name
        same = candidate.is_file() and trusted.is_file() and candidate.read_bytes() == trusted.read_bytes()
        print(
            f"trusted-compare {name}: byte_identical={str(same).lower()} "
            f"candidate_sha256={digest(candidate)} trusted_sha256={digest(trusted)}"
        )

    print("top-level-entry-inventory:")
    for path in sorted(CANDIDATE.iterdir(), key=lambda item: item.name):
        print(f"  {path.name}: {kind(path)}")

    source_symlinks = []
    for path in CANDIDATE.rglob("*"):
        if "semantic-kompiled" in path.parts or "verification-kompiled" in path.parts:
            continue
        if path.is_symlink():
            source_symlinks.append(path.relative_to(CANDIDATE))
    print(f"source-symlink-count={len(source_symlinks)}")
    for rel in source_symlinks:
        print(f"  source-symlink={rel}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
