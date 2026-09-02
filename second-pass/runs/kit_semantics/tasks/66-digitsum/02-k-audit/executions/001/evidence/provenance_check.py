#!/usr/bin/env python3
"""Independent launcher-input and supplied-semantics integrity checks."""

from __future__ import annotations

import hashlib
import json
import os
import stat
import sys
from pathlib import Path


AUDIT = Path("/audit-input.json")
LOCK = Path("/audit-campaign-lock.json")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def kind(path: Path) -> str:
    mode = path.lstat().st_mode
    if stat.S_ISREG(mode):
        return "file"
    if stat.S_ISDIR(mode):
        return "dir"
    if stat.S_ISLNK(mode):
        return "symlink"
    return f"other:{stat.S_IFMT(mode):o}"


def tree_entries(root: Path) -> dict[str, tuple[str, str | None]]:
    entries: dict[str, tuple[str, str | None]] = {}
    for directory, dir_names, file_names in os.walk(root, followlinks=False):
        base = Path(directory)
        for name in sorted(dir_names + file_names):
            path = base / name
            rel = path.relative_to(root).as_posix()
            entry_kind = kind(path)
            entries[rel] = (
                entry_kind,
                sha256_file(path) if entry_kind == "file" else None,
            )
    return entries


def report_hash(label: str, path: Path, expected: str | None = None) -> bool:
    actual = sha256_file(path)
    status = expected is None or actual == expected
    print(
        f"HASH {label}: actual={actual}"
        + (f" expected={expected} match={status}" if expected else "")
    )
    return status


def main() -> int:
    problems: list[str] = []
    audit = json.loads(AUDIT.read_text())
    lock = json.loads(LOCK.read_text())

    lock_equal = lock == audit["audit_campaign"]
    print(f"CAMPAIGN_BLOCK_EQUALS_LOCK: {lock_equal}")
    if not lock_equal:
        problems.append("campaign lock content differs from audit_campaign block")

    hash_checks = [
        ("audit_campaign_lock", LOCK, audit["hashes"]["audit_campaign_lock_sha256"]),
        ("canonical", Path("/reference/canonical.py"), audit["hashes"]["canonical_sha256"]),
        ("candidate_prompt", Path("/candidate/prompt.py"), audit["hashes"]["candidate_prompt_sha256"]),
        ("trusted_prompt", Path("/reference/prompt.py"), audit["hashes"]["trusted_prompt_sha256"]),
        ("candidate_translator", Path("/candidate/py2mpy.py"), audit["hashes"]["candidate_translator_sha256"]),
        ("trusted_translator", Path("/reference/py2mpy.py"), audit["hashes"]["trusted_translator_sha256"]),
        ("run_manifest", Path("/run.json"), audit["hashes"]["run_manifest_sha256"]),
        ("task_manifest", Path("/task.json"), audit["hashes"]["task_manifest_sha256"]),
        ("generation_result", Path("/generation-result.json"), audit["hashes"]["stage1_result_sha256"]),
        ("invocation", Path("/generation-evidence/invocation.json"), audit["hashes"]["stage1_invocation_sha256"]),
        ("metrics", Path("/generation-evidence/metrics.json"), audit["hashes"]["generation_metrics_sha256"]),
        ("runtime_metrics", Path("/generation-evidence/runtime-metrics.json"), audit["hashes"]["generation_runtime_metrics_sha256"]),
        ("usage", Path("/generation-evidence/usage.json"), audit["hashes"]["generation_usage_sha256"]),
        ("codex_last", Path("/generation-evidence/codex-last.txt"), audit["hashes"]["generation_codex_last_sha256"]),
        ("codex_output", Path("/generation-evidence/codex-output.log"), audit["hashes"]["generation_codex_output_sha256"]),
        ("generation_prompt", Path("/generation-evidence/prompt.txt"), audit["hashes"]["generation_prompt_sha256"]),
    ]
    for label, path, expected in hash_checks:
        if not path.exists() or not path.is_file() or path.is_symlink():
            problems.append(f"{label} absent, mistyped, or symlinked: {path}")
            continue
        if not report_hash(label, path, expected):
            problems.append(f"{label} hash mismatch")

    required = [
        Path("/audit-input.json"),
        LOCK,
        Path("/run.json"),
        Path("/task.json"),
        Path("/generation-result.json"),
        Path("/generation-evidence/invocation.json"),
        Path("/generation-evidence/metrics.json"),
        Path("/generation-evidence/runtime-metrics.json"),
        Path("/generation-evidence/usage.json"),
        Path("/generation-evidence/codex-last.txt"),
        Path("/generation-evidence/codex-output.log"),
        Path("/generation-evidence/prompt.txt"),
        Path("/reference/canonical.py"),
        Path("/reference/prompt.py"),
        Path("/reference/py2mpy.py"),
        Path("/reference/reference-semantics"),
        Path("/candidate"),
        Path("/candidate/prompt.py"),
        Path("/candidate/py2mpy.py"),
        Path("/candidate/reference-semantics"),
        Path("/generation-evidence/codex-trace"),
    ]
    for path in required:
        try:
            entry_kind = kind(path)
        except (FileNotFoundError, PermissionError) as err:
            problems.append(f"required path unreadable: {path}: {err}")
            continue
        print(f"REQUIRED {path}: {entry_kind}")
        if entry_kind == "symlink":
            problems.append(f"required path is symlink: {path}")

    for root in [
        Path("/candidate"),
        Path("/reference"),
        Path("/generation-evidence"),
    ]:
        symlinks = [p for p in root.rglob("*") if p.is_symlink()]
        print(f"SYMLINKS {root}: {len(symlinks)}")
        for path in symlinks:
            print(f"  {path} -> {os.readlink(path)}")

    pairs = [
        ("/candidate/prompt.py", "/reference/prompt.py", "prompt"),
        ("/candidate/py2mpy.py", "/reference/py2mpy.py", "translator"),
    ]
    for left_name, right_name, label in pairs:
        left = Path(left_name)
        right = Path(right_name)
        equal = left.read_bytes() == right.read_bytes()
        print(f"BYTE_EQUAL {label}: {equal}")
        if not equal:
            problems.append(f"candidate {label} differs from trusted")

    candidate_semantics = tree_entries(Path("/candidate/reference-semantics"))
    trusted_semantics = tree_entries(Path("/reference/reference-semantics"))
    all_paths = sorted(set(candidate_semantics) | set(trusted_semantics))
    differences = 0
    for rel in all_paths:
        left = candidate_semantics.get(rel)
        right = trusted_semantics.get(rel)
        if left != right:
            differences += 1
            print(f"SEMANTICS_DIFF {rel}: candidate={left} trusted={right}")
    print(f"SEMANTICS_ENTRY_COUNT candidate={len(candidate_semantics)} trusted={len(trusted_semantics)}")
    print(f"SEMANTICS_DIFFERENCES: {differences}")
    if differences:
        problems.append(f"supplied semantics tree has {differences} difference(s)")

    result = json.loads(Path("/generation-result.json").read_text())
    for relative, expected in sorted(result["outputs"]["evidence"].items()):
        path = Path("/generation-evidence") / relative
        if not path.exists() or not path.is_file() or path.is_symlink():
            problems.append(f"declared generation evidence absent/mistyped/symlinked: {relative}")
            continue
        if not report_hash(f"generation_result:{relative}", path, expected):
            problems.append(f"generation-result hash mismatch: {relative}")

    trace_files = sorted(Path("/generation-evidence/codex-trace").rglob("*"))
    trace_regular = [p for p in trace_files if p.is_file() and not p.is_symlink()]
    print(f"TRACE_REGULAR_FILES: {len(trace_regular)}")
    for path in trace_regular:
        report_hash(f"trace:{path.relative_to('/generation-evidence')}", path)

    print(f"PROBLEM_COUNT: {len(problems)}")
    for problem in problems:
        print(f"PROBLEM: {problem}")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
