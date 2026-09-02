#!/usr/bin/env python3
"""Independent provenance and supplied-semantics integrity check."""

from __future__ import annotations

import hashlib
import json
import os
import stat
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
    mode = path.lstat().st_mode
    if stat.S_ISLNK(mode):
        return "symlink"
    if stat.S_ISDIR(mode):
        return "directory"
    if stat.S_ISREG(mode):
        return "file"
    return "other"


def manifest(root: Path) -> dict[str, dict[str, object]]:
    entries: dict[str, dict[str, object]] = {}
    for current, directories, files in os.walk(root, followlinks=False):
        current_path = Path(current)
        for name in sorted(directories + files):
            path = current_path / name
            relative = str(path.relative_to(root))
            entry_kind = kind(path)
            record: dict[str, object] = {"kind": entry_kind}
            if entry_kind == "file":
                record["size"] = path.lstat().st_size
                record["sha256"] = sha256(path)
            elif entry_kind == "symlink":
                record["target"] = os.readlink(path)
            entries[relative] = record
    return entries


def main() -> int:
    issues: list[str] = []
    facts: dict[str, object] = {}

    trusted_semantics = REFERENCE / "reference-semantics"
    candidate_semantics = CANDIDATE / "reference-semantics"
    facts["trusted_semantics_kind"] = (
        kind(trusted_semantics) if os.path.lexists(trusted_semantics) else "missing"
    )
    facts["candidate_semantics_kind"] = (
        kind(candidate_semantics) if os.path.lexists(candidate_semantics) else "missing"
    )
    if facts["trusted_semantics_kind"] != "directory":
        issues.append(
            "infrastructure: /reference/reference-semantics is not a real directory"
        )
    if facts["candidate_semantics_kind"] != "directory":
        issues.append(
            "candidate: /candidate/reference-semantics is not a real directory"
        )

    if (
        facts["trusted_semantics_kind"] == "directory"
        and facts["candidate_semantics_kind"] == "directory"
    ):
        trusted_manifest = manifest(trusted_semantics)
        candidate_manifest = manifest(candidate_semantics)
        facts["trusted_semantics_entry_count"] = len(trusted_manifest)
        facts["candidate_semantics_entry_count"] = len(candidate_manifest)
        for relative in sorted(trusted_manifest.keys() - candidate_manifest.keys()):
            issues.append(f"candidate semantics missing: {relative}")
        for relative in sorted(candidate_manifest.keys() - trusted_manifest.keys()):
            issues.append(f"candidate semantics additional: {relative}")
        for relative in sorted(trusted_manifest.keys() & candidate_manifest.keys()):
            expected = trusted_manifest[relative]
            actual = candidate_manifest[relative]
            if actual["kind"] == "symlink":
                issues.append(f"candidate semantics symlinked: {relative}")
            if expected != actual:
                issues.append(
                    "candidate semantics mismatch: "
                    f"{relative}: expected={expected!r} actual={actual!r}"
                )

    for name in ("prompt.py", "py2mpy.py"):
        trusted = REFERENCE / name
        submitted = CANDIDATE / name
        if not os.path.lexists(submitted):
            issues.append(f"candidate missing: {name}")
            continue
        if kind(submitted) != "file":
            issues.append(f"candidate mistyped: {name} is {kind(submitted)}")
            continue
        facts[f"{name}_trusted_sha256"] = sha256(trusted)
        facts[f"{name}_candidate_sha256"] = sha256(submitted)
        facts[f"{name}_byte_identical"] = trusted.read_bytes() == submitted.read_bytes()
        if not facts[f"{name}_byte_identical"]:
            issues.append(f"candidate changed: {name}")

    for name in ("solution.py", "solution.mpy", "spec.k", "verification.k"):
        path = CANDIDATE / name
        if not os.path.lexists(path):
            issues.append(f"candidate missing: {name}")
        elif kind(path) != "file":
            issues.append(f"candidate mistyped: {name} is {kind(path)}")
        else:
            facts[f"{name}_sha256"] = sha256(path)

    missing_generation_records = [
        name
        for name in (
            "run-input.json",
            "metrics.json",
            "codex-last.txt",
            "codex-output.log",
        )
        if not os.path.lexists(CANDIDATE / name)
    ]
    facts["missing_generation_records"] = missing_generation_records
    facts["structured_trace_candidates"] = sorted(
        str(path.relative_to(CANDIDATE))
        for path in CANDIDATE.rglob("*")
        if path.is_file()
        and (
            "trace" in path.name.lower()
            or path.suffix.lower() in {".jsonl", ".ndjson"}
        )
    )

    print(
        json.dumps(
            {
                "mode": "SUPPLIED_SEMANTICS",
                "facts": facts,
                "integrity_issues": issues,
                "generation_record_gap_count": len(missing_generation_records),
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 1 if issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
