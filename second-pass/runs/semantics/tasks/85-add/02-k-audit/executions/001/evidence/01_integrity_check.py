#!/usr/bin/env python3
"""Independent stage-1 artifact and supplied-semantics integrity check."""

from __future__ import annotations

import filecmp
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


def tree_manifest(root: Path) -> dict[str, tuple[str, str]]:
    result: dict[str, tuple[str, str]] = {}
    for dirpath, dirnames, filenames in os.walk(root, followlinks=False):
        current = Path(dirpath)
        names = sorted(dirnames + filenames)
        for name in names:
            path = current / name
            rel = path.relative_to(root).as_posix()
            if path.is_symlink():
                result[rel] = ("symlink", os.readlink(path))
            elif path.is_dir():
                result[rel] = ("directory", "")
            elif path.is_file():
                result[rel] = ("file", digest(path))
            else:
                result[rel] = ("other", "")
    return result


def compare_file(label: str, trusted: Path, submitted: Path) -> bool:
    ok = (
        trusted.is_file()
        and not trusted.is_symlink()
        and submitted.is_file()
        and not submitted.is_symlink()
        and filecmp.cmp(trusted, submitted, shallow=False)
    )
    print(
        f"{label}: {'IDENTICAL' if ok else 'INTEGRITY FAILURE'} "
        f"trusted_sha256={digest(trusted) if trusted.is_file() else 'N/A'} "
        f"candidate_sha256={digest(submitted) if submitted.is_file() else 'N/A'}"
    )
    return ok


def main() -> int:
    required_claim_files = [
        "run-input.json",
        "metrics.json",
        "codex-last.txt",
        "codex-output.log",
    ]
    required_source_files = [
        "prompt.py",
        "py2mpy.py",
        "solution.py",
        "solution.mpy",
        "spec.k",
        "verification.k",
    ]
    failures = 0

    print("MODE=SUPPLIED_SEMANTICS")
    trusted_semantics = REFERENCE / "reference-semantics"
    print(
        "trusted_semantics_mount="
        + ("PRESENT" if trusted_semantics.is_dir() else "MISSING")
    )
    if not trusted_semantics.is_dir():
        return 2

    for name in required_claim_files:
        path = CANDIDATE / name
        state = "PRESENT" if path.exists() and not path.is_symlink() else "MISSING"
        print(f"untrusted_provenance_artifact {name}: {state}")

    for name in required_source_files:
        path = CANDIDATE / name
        ok = path.is_file() and not path.is_symlink()
        print(f"required_source_artifact {name}: {'REGULAR_FILE' if ok else 'FAIL'}")
        failures += int(not ok)

    failures += int(
        not compare_file(
            "prompt",
            REFERENCE / "prompt.py",
            CANDIDATE / "prompt.py",
        )
    )
    failures += int(
        not compare_file(
            "translator",
            REFERENCE / "py2mpy.py",
            CANDIDATE / "py2mpy.py",
        )
    )

    trusted_manifest = tree_manifest(trusted_semantics)
    candidate_manifest = tree_manifest(CANDIDATE / "reference-semantics")
    all_paths = sorted(set(trusted_manifest) | set(candidate_manifest))
    tree_failures = 0
    for rel in all_paths:
        trusted_entry = trusted_manifest.get(rel)
        candidate_entry = candidate_manifest.get(rel)
        if trusted_entry != candidate_entry:
            tree_failures += 1
            print(
                f"semantics_entry_mismatch {rel}: "
                f"trusted={trusted_entry!r} candidate={candidate_entry!r}"
            )
    print(
        f"semantics_tree: {'IDENTICAL' if tree_failures == 0 else 'INTEGRITY FAILURE'} "
        f"trusted_entries={len(trusted_manifest)} "
        f"candidate_entries={len(candidate_manifest)} "
        f"mismatches={tree_failures}"
    )
    failures += tree_failures

    symlinks = [
        str(path)
        for path in CANDIDATE.rglob("*")
        if path.is_symlink()
    ]
    print(f"candidate_symlinks={len(symlinks)}")
    for path in symlinks:
        print(f"candidate_symlink {path}")

    trace_candidates = sorted(
        str(path.relative_to(CANDIDATE))
        for path in CANDIDATE.iterdir()
        if path.is_file() and "trace" in path.name.lower()
    )
    print(f"structured_trace_candidates={trace_candidates!r}")
    print(f"INTEGRITY_FAILURE_COUNT={failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
