#!/usr/bin/env python3
"""Independent integrity checks for the mounted audit inputs."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import sys


AUDIT_INPUT = Path("/audit-input.json")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def compare_trees(left: Path, right: Path) -> list[str]:
    problems: list[str] = []
    left_entries = {
        str(path.relative_to(left)): path
        for path in left.rglob("*")
    }
    right_entries = {
        str(path.relative_to(right)): path
        for path in right.rglob("*")
    }
    for rel in sorted(set(left_entries) | set(right_entries)):
        a = left_entries.get(rel)
        b = right_entries.get(rel)
        if a is None:
            problems.append(f"missing-left {rel}")
            continue
        if b is None:
            problems.append(f"missing-right {rel}")
            continue
        if a.is_symlink() or b.is_symlink():
            problems.append(f"symlink {rel}: left={a.is_symlink()} right={b.is_symlink()}")
            continue
        a_kind = "dir" if a.is_dir() else "file" if a.is_file() else "other"
        b_kind = "dir" if b.is_dir() else "file" if b.is_file() else "other"
        if a_kind != b_kind:
            problems.append(f"type {rel}: left={a_kind} right={b_kind}")
        elif a_kind == "file" and sha256_file(a) != sha256_file(b):
            problems.append(f"content {rel}: left={sha256_file(a)} right={sha256_file(b)}")
    return problems


def main() -> int:
    manifest = json.loads(AUDIT_INPUT.read_text())
    hashes = manifest["hashes"]
    paths = {
        "audit_campaign_lock_sha256": Path("/audit-campaign-lock.json"),
        "run_manifest_sha256": Path("/run.json"),
        "task_manifest_sha256": Path("/task.json"),
        "stage1_result_sha256": Path("/generation-result.json"),
        "stage1_invocation_sha256": Path("/generation-evidence/invocation.json"),
        "generation_metrics_sha256": Path("/generation-evidence/metrics.json"),
        "generation_usage_sha256": Path("/generation-evidence/usage.json"),
        "generation_codex_last_sha256": Path("/generation-evidence/codex-last.txt"),
        "generation_codex_output_sha256": Path("/generation-evidence/codex-output.log"),
        "generation_prompt_sha256": Path("/generation-evidence/prompt.txt"),
        "canonical_sha256": Path("/reference/canonical.py"),
        "trusted_prompt_sha256": Path("/reference/prompt.py"),
        "candidate_prompt_sha256": Path("/candidate/prompt.py"),
        "trusted_translator_sha256": Path("/reference/py2mpy.py"),
        "candidate_translator_sha256": Path("/candidate/py2mpy.py"),
    }
    trace = Path(
        "/generation-evidence/codex-trace/2026/07/23/"
        "rollout-2026-07-23T01-23-30-019f8da4-b81d-7d42-972c-696eaae8c3fa.jsonl"
    )
    required = [
        AUDIT_INPUT,
        Path("/audit-campaign-lock.json"),
        Path("/run.json"),
        Path("/task.json"),
        Path("/generation-result.json"),
        Path("/generation-evidence/invocation.json"),
        Path("/generation-evidence/metrics.json"),
        Path("/generation-evidence/codex-last.txt"),
        Path("/generation-evidence/codex-output.log"),
        Path("/generation-evidence/prompt.txt"),
        Path("/generation-evidence/usage.json"),
        trace,
        Path("/reference/canonical.py"),
        Path("/reference/prompt.py"),
        Path("/reference/py2mpy.py"),
        Path("/reference/reference-semantics"),
        Path("/candidate"),
        Path("/candidate/solution.py"),
        Path("/candidate/solution.mpy"),
        Path("/candidate/verification.k"),
        Path("/candidate/spec.k"),
        Path("/candidate/prove.sh"),
        Path("/candidate/prompt.py"),
        Path("/candidate/py2mpy.py"),
        Path("/candidate/reference-semantics"),
    ]

    failures: list[str] = []
    print(f"record_layout={manifest.get('record_layout')}")
    print(f"semantics_mode={manifest.get('semantics_mode')}")
    for path in required:
        ok = path.exists() and os.access(path, os.R_OK)
        print(f"required readable={ok} symlink={path.is_symlink()} path={path}")
        if not ok or path.is_symlink():
            failures.append(f"bad required path: {path}")

    lock = json.loads(Path("/audit-campaign-lock.json").read_text())
    lock_matches = lock == manifest["audit_campaign"]
    print(f"campaign_lock_matches_block={lock_matches}")
    if not lock_matches:
        failures.append("campaign lock JSON differs from audit_campaign block")

    for key, path in paths.items():
        actual = sha256_file(path)
        expected = hashes[key]
        ok = actual == expected
        print(f"hash ok={ok} key={key} actual={actual} expected={expected} path={path}")
        if not ok:
            failures.append(f"hash mismatch: {key}")

    trace_actual = sha256_file(trace)
    trace_expected = json.loads(Path("/generation-result.json").read_text())[
        "outputs"
    ]["evidence"][
        "codex-trace/2026/07/23/"
        "rollout-2026-07-23T01-23-30-019f8da4-b81d-7d42-972c-696eaae8c3fa.jsonl"
    ]
    print(
        f"trace_hash ok={trace_actual == trace_expected} "
        f"actual={trace_actual} expected={trace_expected}"
    )
    if trace_actual != trace_expected:
        failures.append("trace hash mismatch")

    for a, b, label in [
        (Path("/candidate/prompt.py"), Path("/reference/prompt.py"), "prompt"),
        (Path("/candidate/py2mpy.py"), Path("/reference/py2mpy.py"), "translator"),
    ]:
        same = a.read_bytes() == b.read_bytes()
        print(f"byte_identity {label}={same}")
        if not same:
            failures.append(f"{label} differs")

    tree_problems = compare_trees(
        Path("/candidate/reference-semantics"),
        Path("/reference/reference-semantics"),
    )
    print(f"semantics_tree_problem_count={len(tree_problems)}")
    for problem in tree_problems:
        print(f"semantics_tree_problem={problem}")
    failures.extend(tree_problems)

    print(f"RESULT={'PASS' if not failures else 'FAIL'} failures={len(failures)}")
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
