#!/usr/bin/env python3
"""Independent lstat/hash comparison for audit stage 1."""

from __future__ import annotations

import hashlib
import os
from pathlib import Path


CANDIDATE = Path("/candidate")
REFERENCE = Path("/reference")


def kind(path: Path) -> str:
    if path.is_symlink():
        return "symlink"
    if path.is_file():
        return "file"
    if path.is_dir():
        return "directory"
    if path.exists():
        return "other"
    return "missing"


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def manifest(root: Path) -> dict[str, tuple[str, str | None]]:
    result: dict[str, tuple[str, str | None]] = {}
    for current, directories, files in os.walk(root, followlinks=False):
        current_path = Path(current)
        for name in sorted(directories + files):
            path = current_path / name
            relative = path.relative_to(root).as_posix()
            entry_kind = kind(path)
            entry_hash = digest(path) if entry_kind == "file" else None
            result[relative] = (entry_kind, entry_hash)
    return result


def compare_file(candidate_name: str, reference_name: str) -> bool:
    candidate = CANDIDATE / candidate_name
    reference = REFERENCE / reference_name
    candidate_kind = kind(candidate)
    reference_kind = kind(reference)
    print(
        f"FILE {candidate_name}: candidate_kind={candidate_kind} "
        f"reference_kind={reference_kind}"
    )
    if candidate_kind != "file" or reference_kind != "file":
        print("  RESULT=FAIL_TYPE")
        return False
    candidate_hash = digest(candidate)
    reference_hash = digest(reference)
    print(f"  candidate_sha256={candidate_hash}")
    print(f"  reference_sha256={reference_hash}")
    identical = candidate_hash == reference_hash
    print(f"  byte_identical={str(identical).lower()}")
    return identical


def main() -> int:
    ok = True
    trusted_semantics = REFERENCE / "reference-semantics"
    candidate_semantics = CANDIDATE / "reference-semantics"
    print("RENDERED_MODE=SUPPLIED_SEMANTICS")
    print(f"trusted_semantics_kind={kind(trusted_semantics)}")
    print(f"candidate_semantics_kind={kind(candidate_semantics)}")
    if kind(trusted_semantics) != "directory":
        print("INFRASTRUCTURE_BREACH=trusted semantics missing or mistyped")
        return 2
    if kind(candidate_semantics) != "directory":
        print("CANDIDATE_INTEGRITY_FAILURE=candidate semantics missing or mistyped")
        ok = False
    else:
        trusted_manifest = manifest(trusted_semantics)
        candidate_manifest = manifest(candidate_semantics)
        all_names = sorted(set(trusted_manifest) | set(candidate_manifest))
        differences = 0
        for name in all_names:
            trusted_entry = trusted_manifest.get(name)
            candidate_entry = candidate_manifest.get(name)
            if trusted_entry != candidate_entry:
                differences += 1
                print(
                    f"SEMANTICS_DIFF {name}: "
                    f"trusted={trusted_entry} candidate={candidate_entry}"
                )
            if candidate_entry is not None and candidate_entry[0] == "symlink":
                print(f"SEMANTICS_SYMLINK {name}")
        print(f"trusted_semantics_entries={len(trusted_manifest)}")
        print(f"candidate_semantics_entries={len(candidate_manifest)}")
        print(f"semantics_differences={differences}")
        ok &= differences == 0

    ok &= compare_file("prompt.py", "prompt.py")
    ok &= compare_file("py2mpy.py", "py2mpy.py")

    required_regular = [
        "run-input.json",
        "metrics.json",
        "codex-last.txt",
        "codex-output.log",
        "solution.py",
        "solution.mpy",
        "spec.k",
        "verification.k",
        "prove.sh",
    ]
    for name in required_regular:
        entry_kind = kind(CANDIDATE / name)
        print(f"REQUIRED {name}: kind={entry_kind}")
        if entry_kind != "file":
            ok = False

    traces = sorted((CANDIDATE / "codex-trace").glob("**/*.jsonl"))
    print(f"structured_trace_count={len(traces)}")
    for trace in traces:
        trace_kind = kind(trace)
        print(
            f"TRACE {trace.relative_to(CANDIDATE)}: "
            f"kind={trace_kind} bytes={trace.stat().st_size if trace_kind == 'file' else 'NA'}"
        )
        if trace_kind != "file":
            ok = False
    if not traces:
        ok = False

    print(f"INTEGRITY_RESULT={'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
