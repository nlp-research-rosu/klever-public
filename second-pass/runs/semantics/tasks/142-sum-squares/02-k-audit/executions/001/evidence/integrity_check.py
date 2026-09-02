#!/usr/bin/env python3
"""Independent byte/type/symlink integrity checks for audit stage 1."""

from __future__ import annotations

import hashlib
import os
from pathlib import Path


CANDIDATE = Path("/candidate")
REFERENCE = Path("/reference")


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def tree(root: Path) -> dict[str, tuple[str, str | None]]:
    result: dict[str, tuple[str, str | None]] = {}
    for dirpath, dirnames, filenames in os.walk(root, followlinks=False):
        base = Path(dirpath)
        for name in sorted(dirnames + filenames):
            path = base / name
            rel = str(path.relative_to(root))
            if path.is_symlink():
                result[rel] = ("symlink", os.readlink(path))
            elif path.is_dir():
                result[rel] = ("directory", None)
            elif path.is_file():
                result[rel] = ("file", digest(path))
            else:
                result[rel] = ("other", None)
    return result


def compare_file(candidate: Path, reference: Path, label: str) -> int:
    errors = 0
    if not candidate.exists():
        print(f"FAIL {label}: missing {candidate}")
        return 1
    if candidate.is_symlink() or not candidate.is_file():
        print(f"FAIL {label}: candidate is {candidate.stat().st_mode:o}, not regular file")
        return 1
    same = candidate.read_bytes() == reference.read_bytes()
    print(
        f"{'PASS' if same else 'FAIL'} {label}: "
        f"candidate_sha256={digest(candidate)} reference_sha256={digest(reference)}"
    )
    return 0 if same else 1


def main() -> int:
    errors = 0
    reference_semantics = REFERENCE / "reference-semantics"
    print(
        "MODE_CHECK "
        f"reference_semantics_exists={reference_semantics.is_dir()} "
        f"is_symlink={reference_semantics.is_symlink()}"
    )
    if not reference_semantics.is_dir() or reference_semantics.is_symlink():
        print("INFRASTRUCTURE_BREACH supplied-semantics trusted tree is absent or symlinked")
        return 2

    errors += compare_file(
        CANDIDATE / "prompt.py", REFERENCE / "prompt.py", "prompt_byte_identity"
    )
    errors += compare_file(
        CANDIDATE / "py2mpy.py", REFERENCE / "py2mpy.py", "translator_byte_identity"
    )

    candidate_tree = tree(CANDIDATE / "reference-semantics")
    reference_tree = tree(reference_semantics)
    all_paths = sorted(set(candidate_tree) | set(reference_tree))
    for rel in all_paths:
        got = candidate_tree.get(rel)
        expected = reference_tree.get(rel)
        if got != expected:
            errors += 1
            print(f"FAIL semantics_entry {rel}: candidate={got!r} reference={expected!r}")
    print(
        f"{'PASS' if candidate_tree == reference_tree else 'FAIL'} "
        f"semantics_tree entries_candidate={len(candidate_tree)} "
        f"entries_reference={len(reference_tree)}"
    )

    for name in (
        "run-input.json",
        "metrics.json",
        "codex-last.txt",
        "codex-output.log",
    ):
        path = CANDIDATE / name
        if path.is_symlink():
            errors += 1
            print(f"FAIL generation_artifact {name}: symlink")
        elif not path.exists():
            errors += 1
            print(f"MISSING generation_artifact {name}")
        elif not path.is_file():
            errors += 1
            print(f"FAIL generation_artifact {name}: not a regular file")
        else:
            print(f"PRESENT generation_artifact {name}: sha256={digest(path)}")

    traces = sorted(
        p
        for p in CANDIDATE.iterdir()
        if "trace" in p.name.lower() or p.suffix == ".jsonl"
    )
    print("structured_generation_traces=" + ",".join(map(str, traces)))
    print(f"integrity_errors={errors}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
