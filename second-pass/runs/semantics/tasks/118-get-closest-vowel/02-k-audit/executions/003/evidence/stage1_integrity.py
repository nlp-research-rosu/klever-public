#!/usr/bin/env python3
"""Independent provenance and mount-integrity checks for this audit."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import sys


AUDIT = Path("/audit-input.json")
LOCK = Path("/audit-campaign-lock.json")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def entry_kind(path: Path) -> str:
    if path.is_symlink():
        return "symlink"
    if path.is_file():
        return "file"
    if path.is_dir():
        return "dir"
    return "other"


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
    for relative in sorted(set(left_entries) | set(right_entries)):
        lp = left_entries.get(relative)
        rp = right_entries.get(relative)
        if lp is None:
            problems.append(f"missing candidate entry: {relative}")
            continue
        if rp is None:
            problems.append(f"additional candidate entry: {relative}")
            continue
        lk = entry_kind(lp)
        rk = entry_kind(rp)
        if lk != rk:
            problems.append(f"type mismatch {relative}: candidate={lk}, trusted={rk}")
            continue
        if lk == "symlink":
            problems.append(
                f"symlink forbidden {relative}: "
                f"candidate->{os.readlink(lp)!r}, trusted->{os.readlink(rp)!r}"
            )
        elif lk == "file" and sha256_file(lp) != sha256_file(rp):
            problems.append(f"content mismatch: {relative}")
    return problems


def check_hash(label: str, path: Path, expected: str, problems: list[str]) -> None:
    actual = sha256_file(path)
    status = "OK" if actual == expected else "MISMATCH"
    print(f"HASH {status} {label} expected={expected} actual={actual} path={path}")
    if status != "OK":
        problems.append(f"hash mismatch: {label}")


def main() -> int:
    problems: list[str] = []
    audit = json.loads(AUDIT.read_text())
    lock = json.loads(LOCK.read_text())
    print(f"record_layout={audit.get('record_layout')}")
    print(f"semantics_mode={audit.get('semantics_mode')}")
    if audit.get("record_layout") != "legacy-selected-stage1":
        problems.append("unexpected record_layout")
    if audit.get("semantics_mode") != "SUPPLIED_SEMANTICS":
        problems.append("unexpected semantics_mode")

    if lock == audit.get("audit_campaign"):
        print("CAMPAIGN OK lock exactly equals audit_input.audit_campaign")
    else:
        print("CAMPAIGN MISMATCH")
        problems.append("campaign lock differs from audit campaign block")

    hashes = audit["hashes"]
    paths = {
        "audit_campaign_lock_sha256": LOCK,
        "canonical_sha256": Path("/reference/canonical.py"),
        "trusted_prompt_sha256": Path("/reference/prompt.py"),
        "candidate_prompt_sha256": Path("/candidate/prompt.py"),
        "trusted_translator_sha256": Path("/reference/py2mpy.py"),
        "candidate_translator_sha256": Path("/candidate/py2mpy.py"),
        "run_manifest_sha256": Path("/run.json"),
        "task_manifest_sha256": Path("/task.json"),
        "stage1_result_sha256": Path("/generation-result.json"),
        "stage1_invocation_sha256": Path("/generation-evidence/invocation.json"),
        "generation_metrics_sha256": Path("/generation-evidence/metrics.json"),
        "generation_usage_sha256": Path("/generation-evidence/usage.json"),
        "generation_codex_last_sha256": Path("/generation-evidence/codex-last.txt"),
        "generation_codex_output_sha256": Path("/generation-evidence/codex-output.log"),
        "generation_prompt_sha256": Path("/generation-evidence/prompt.txt"),
    }
    for key, path in paths.items():
        if not path.is_file():
            problems.append(f"missing required file: {path}")
            print(f"MISSING {path}")
        else:
            check_hash(key, path, hashes[key], problems)

    required_records = [
        Path("/run.json"),
        Path("/task.json"),
        Path("/generation-result.json"),
        Path("/generation-evidence/invocation.json"),
        Path("/generation-evidence/metrics.json"),
        Path("/generation-evidence/codex-last.txt"),
        Path("/generation-evidence/codex-output.log"),
        Path("/generation-evidence/prompt.txt"),
        Path("/generation-evidence/codex-trace"),
    ]
    for path in required_records:
        status = "OK" if path.exists() and os.access(path, os.R_OK) else "MISSING_OR_UNREADABLE"
        print(f"REQUIRED {status} {path}")
        if status != "OK":
            problems.append(f"missing or unreadable required record: {path}")

    json_records = [
        AUDIT,
        LOCK,
        Path("/run.json"),
        Path("/task.json"),
        Path("/generation-result.json"),
        Path("/generation-evidence/invocation.json"),
        Path("/generation-evidence/metrics.json"),
        Path("/generation-evidence/usage.json"),
        Path("/generation-evidence/legacy-metrics.json"),
        Path("/generation-evidence/legacy-run-input.json"),
    ]
    for path in json_records:
        try:
            json.loads(path.read_text())
            print(f"JSON OK {path}")
        except Exception as err:
            print(f"JSON INVALID {path}: {err}")
            problems.append(f"invalid JSON: {path}")

    result = json.loads(Path("/generation-result.json").read_text())
    trace_expected = {
        name: digest
        for name, digest in result["outputs"]["evidence"].items()
        if name.startswith("codex-trace/")
    }
    trace_root = Path("/generation-evidence")
    actual_trace_files = sorted(Path("/generation-evidence/codex-trace").rglob("*"))
    actual_trace_files = [p for p in actual_trace_files if p.is_file() or p.is_symlink()]
    expected_names = sorted(trace_expected)
    actual_names = sorted(str(p.relative_to(trace_root)) for p in actual_trace_files)
    if actual_names == expected_names:
        print(f"TRACE INVENTORY OK files={len(actual_names)}")
    else:
        print(f"TRACE INVENTORY MISMATCH expected={expected_names} actual={actual_names}")
        problems.append("trace inventory mismatch")

    trace_event_count = 0
    trace_types: dict[str, int] = {}
    for name, expected in sorted(trace_expected.items()):
        path = trace_root / name
        if path.is_symlink():
            problems.append(f"trace file is symlink: {path}")
            print(f"TRACE SYMLINK {path}")
            continue
        check_hash(name, path, expected, problems)
        with path.open(encoding="utf-8") as stream:
            for line_number, line in enumerate(stream, 1):
                try:
                    event = json.loads(line)
                except Exception as err:
                    print(f"TRACE JSON INVALID {path}:{line_number}: {err}")
                    problems.append(f"invalid trace JSONL at {path}:{line_number}")
                    break
                trace_event_count += 1
                event_type = str(event.get("type", "<missing>"))
                trace_types[event_type] = trace_types.get(event_type, 0) + 1
    print(f"TRACE JSONL OK events={trace_event_count} top_level_types={trace_types}")

    candidate_symlinks = sorted(p for p in Path("/candidate").rglob("*") if p.is_symlink())
    print(f"CANDIDATE SYMLINK COUNT {len(candidate_symlinks)}")
    if candidate_symlinks:
        problems.extend(f"candidate symlink: {path}" for path in candidate_symlinks)

    semantics_problems = compare_trees(
        Path("/candidate/reference-semantics"),
        Path("/reference/reference-semantics"),
    )
    if semantics_problems:
        print("SUPPLIED SEMANTICS TREE MISMATCH")
        for problem in semantics_problems:
            print(f"  {problem}")
        problems.extend(semantics_problems)
    else:
        print("SUPPLIED SEMANTICS TREE OK exact paths, types, and file bytes")

    for candidate, trusted, label in [
        (Path("/candidate/prompt.py"), Path("/reference/prompt.py"), "prompt"),
        (Path("/candidate/py2mpy.py"), Path("/reference/py2mpy.py"), "translator"),
    ]:
        if candidate.read_bytes() == trusted.read_bytes():
            print(f"TRUSTED COPY OK {label}")
        else:
            print(f"TRUSTED COPY MISMATCH {label}")
            problems.append(f"{label} differs from trusted copy")

    for root in [
        Path("/candidate"),
        Path("/reference"),
        Path("/generation-evidence"),
    ]:
        kind_counts: dict[str, int] = {}
        for path in [root, *root.rglob("*")]:
            kind = entry_kind(path)
            kind_counts[kind] = kind_counts.get(kind, 0) + 1
        print(f"ENTRY TYPES {root} {kind_counts}")

    if problems:
        print(f"STAGE1_RESULT FAIL problems={len(problems)}")
        for problem in problems:
            print(f"PROBLEM {problem}")
        return 1
    print("STAGE1_RESULT PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
