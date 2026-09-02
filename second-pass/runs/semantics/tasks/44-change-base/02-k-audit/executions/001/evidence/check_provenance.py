#!/usr/bin/env python3
"""Independent provenance and supplied-semantics integrity checks."""

from __future__ import annotations

import hashlib
import os
from pathlib import Path


CANDIDATE = Path("/candidate")
REFERENCE = Path("/reference")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def kind(path: Path) -> str:
    if path.is_symlink():
        return "symlink"
    if path.is_file():
        return "file"
    if path.is_dir():
        return "directory"
    return "other"


def compare_files(candidate: Path, trusted: Path) -> None:
    print(f"COMPARE_FILE candidate={candidate} trusted={trusted}")
    print(f"  candidate_kind={kind(candidate) if os.path.lexists(candidate) else 'missing'}")
    print(f"  trusted_kind={kind(trusted) if os.path.lexists(trusted) else 'missing'}")
    if candidate.is_file() and not candidate.is_symlink():
        print(f"  candidate_sha256={sha256(candidate)}")
    if trusted.is_file() and not trusted.is_symlink():
        print(f"  trusted_sha256={sha256(trusted)}")
    if (
        candidate.is_file()
        and trusted.is_file()
        and not candidate.is_symlink()
        and not trusted.is_symlink()
    ):
        print(f"  byte_identical={candidate.read_bytes() == trusted.read_bytes()}")


def tree_entries(root: Path) -> dict[str, Path]:
    result: dict[str, Path] = {}
    for current, directories, files in os.walk(root, followlinks=False):
        current_path = Path(current)
        for name in directories + files:
            path = current_path / name
            result[str(path.relative_to(root))] = path
    return result


def compare_trees(candidate_root: Path, trusted_root: Path) -> int:
    candidate_entries = tree_entries(candidate_root)
    trusted_entries = tree_entries(trusted_root)
    all_names = sorted(candidate_entries.keys() | trusted_entries.keys())
    failures = 0
    print(f"COMPARE_TREE candidate={candidate_root} trusted={trusted_root}")
    for name in all_names:
        candidate = candidate_entries.get(name)
        trusted = trusted_entries.get(name)
        candidate_kind = kind(candidate) if candidate is not None else "missing"
        trusted_kind = kind(trusted) if trusted is not None else "missing"
        status = "OK"
        details = ""
        if candidate_kind != trusted_kind:
            status = "FAIL"
            details = "type-or-presence mismatch"
        elif candidate_kind == "symlink":
            status = "FAIL"
            details = "candidate or trusted symlink"
        elif candidate_kind == "file":
            candidate_hash = sha256(candidate)
            trusted_hash = sha256(trusted)
            if candidate_hash != trusted_hash:
                status = "FAIL"
                details = f"content mismatch {candidate_hash} != {trusted_hash}"
        if status == "FAIL":
            failures += 1
        print(
            f"  {status} {name}: candidate={candidate_kind} trusted={trusted_kind}"
            + (f" ({details})" if details else "")
        )
    print(f"TREE_FAILURES={failures}")
    return failures


def main() -> int:
    required_untrusted = [
        "run-input.json",
        "metrics.json",
        "codex-last.txt",
        "codex-output.log",
    ]
    print("REQUIRED_UNTRUSTED_ARTIFACTS")
    for name in required_untrusted:
        path = CANDIDATE / name
        print(f"  {name}: {kind(path) if os.path.lexists(path) else 'missing'}")
    trace_candidates = sorted(
        path
        for path in CANDIDATE.iterdir()
        if "trace" in path.name.lower() or path.suffix.lower() in {".jsonl", ".trace"}
    )
    print("STRUCTURED_TRACE_CANDIDATES")
    if trace_candidates:
        for path in trace_candidates:
            print(f"  {path.name}: {kind(path)}")
    else:
        print("  none")

    compare_files(CANDIDATE / "prompt.py", REFERENCE / "prompt.py")
    compare_files(CANDIDATE / "py2mpy.py", REFERENCE / "py2mpy.py")

    candidate_semantics = CANDIDATE / "reference-semantics"
    trusted_semantics = REFERENCE / "reference-semantics"
    print(f"RENDERED_MODE=SUPPLIED_SEMANTICS")
    print(f"TRUSTED_SEMANTICS_PRESENT={trusted_semantics.is_dir()}")
    if not trusted_semantics.is_dir() or trusted_semantics.is_symlink():
        print("INFRASTRUCTURE_BREACH=trusted semantics missing, mistyped, or symlinked")
        return 2
    if not candidate_semantics.is_dir() or candidate_semantics.is_symlink():
        print("CANDIDATE_INTEGRITY_FAILURE=candidate semantics missing, mistyped, or symlinked")
        return 1

    failures = compare_trees(candidate_semantics, trusted_semantics)
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
