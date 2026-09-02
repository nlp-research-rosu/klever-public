#!/usr/bin/env python3
"""Independent integrity checks for the launcher-owned audit inputs."""

from __future__ import annotations

import hashlib
import json
import os
import stat
import sys
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")
LOCK = Path("/audit-campaign-lock.json")


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def tree_entries(root: Path) -> list[tuple[str, str, Path]]:
    root_stat = root.lstat()
    if not stat.S_ISDIR(root_stat.st_mode):
        raise ValueError(f"tree root is not a real directory: {root}")
    entries: list[tuple[str, str, Path]] = []
    pending = [root]
    while pending:
        directory = pending.pop()
        for entry in os.scandir(directory):
            path = Path(entry.path)
            mode = entry.stat(follow_symlinks=False).st_mode
            relative = path.relative_to(root).as_posix()
            if stat.S_ISDIR(mode):
                entries.append((relative, "directory", path))
                pending.append(path)
            elif stat.S_ISREG(mode):
                entries.append((relative, "file", path))
            else:
                raise ValueError(f"linked or unsupported tree entry: {path}")
    return sorted(entries)


def tree_sha256(root: Path) -> str:
    """Reproduce the pipeline-v3 length-delimited tree digest."""
    digest = hashlib.sha256()
    for relative, kind, path in tree_entries(root):
        encoded = relative.encode()
        digest.update(len(encoded).to_bytes(4, "big"))
        digest.update(encoded)
        digest.update(kind.encode() + b"\0")
        if kind == "file":
            size = path.stat(follow_symlinks=False).st_size
            digest.update(size.to_bytes(8, "big"))
            with path.open("rb") as stream:
                for block in iter(lambda: stream.read(1024 * 1024), b""):
                    digest.update(block)
    return digest.hexdigest()


def read_regular_json(path: Path) -> object:
    mode = path.lstat().st_mode
    if not stat.S_ISREG(mode):
        raise ValueError(f"not a real regular file: {path}")
    with path.open(encoding="utf-8") as stream:
        return json.load(stream)


def compare_trees(left: Path, right: Path) -> list[str]:
    left_items = {(rel, kind): path for rel, kind, path in tree_entries(left)}
    right_items = {(rel, kind): path for rel, kind, path in tree_entries(right)}
    issues: list[str] = []
    for key in sorted(left_items.keys() - right_items.keys()):
        issues.append(f"only in {left}: {key[1]} {key[0]}")
    for key in sorted(right_items.keys() - left_items.keys()):
        issues.append(f"only in {right}: {key[1]} {key[0]}")
    for key in sorted(left_items.keys() & right_items.keys()):
        if key[1] == "file":
            left_hash = file_sha256(left_items[key])
            right_hash = file_sha256(right_items[key])
            if left_hash != right_hash:
                issues.append(f"content mismatch: {key[0]}")
    return issues


def check_hash(label: str, path: Path, expected: str, issues: list[str]) -> None:
    actual = file_sha256(path)
    status = "OK" if actual == expected else "MISMATCH"
    print(f"FILE {label}: {status} expected={expected} actual={actual} path={path}")
    if status != "OK":
        issues.append(f"{label} hash mismatch")


def main() -> int:
    issues: list[str] = []
    audit = read_regular_json(AUDIT_INPUT)
    lock = read_regular_json(LOCK)
    assert isinstance(audit, dict)
    assert isinstance(lock, dict)

    print(f"record_layout={audit.get('record_layout')}")
    print(f"semantics_mode={audit.get('semantics_mode')}")
    print(f"problem_id={audit.get('problem_id')}")
    if audit.get("record_layout") != "pipeline-v3":
        issues.append("unexpected record layout")
    if audit.get("semantics_mode") != "SUPPLIED_SEMANTICS":
        issues.append("unexpected semantics mode")

    campaign_matches = lock == audit.get("audit_campaign")
    print(f"campaign_block_matches_lock={campaign_matches}")
    if not campaign_matches:
        issues.append("campaign lock content mismatch")

    hashes = audit["hashes"]
    check_hash(
        "audit_campaign_lock",
        LOCK,
        hashes["audit_campaign_lock_sha256"],
        issues,
    )

    required_records = [
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
    ]
    for path in required_records:
        try:
            mode = path.lstat().st_mode
        except OSError as error:
            issues.append(f"missing/unreadable required record {path}: {error}")
            continue
        if not stat.S_ISREG(mode):
            issues.append(f"required record is not a real regular file: {path}")
        print(f"RECORD {path}: mode={stat.filemode(mode)} size={path.stat().st_size}")

    declared_mounts = audit["container_paths"]
    for name, value in sorted(declared_mounts.items()):
        path = Path(value)
        try:
            mode = path.lstat().st_mode
        except OSError as error:
            issues.append(f"missing/unreadable declared mount {name}={path}: {error}")
            continue
        if stat.S_ISLNK(mode):
            issues.append(f"declared mount is a symlink: {name}={path}")
        print(f"MOUNT {name}: {stat.filemode(mode)} {path}")

    file_hashes = [
        ("canonical", Path("/reference/canonical.py"), "canonical_sha256"),
        ("candidate_prompt", Path("/candidate/prompt.py"), "candidate_prompt_sha256"),
        (
            "candidate_translator",
            Path("/candidate/py2mpy.py"),
            "candidate_translator_sha256",
        ),
        ("trusted_prompt", Path("/reference/prompt.py"), "trusted_prompt_sha256"),
        (
            "trusted_translator",
            Path("/reference/py2mpy.py"),
            "trusted_translator_sha256",
        ),
        ("run_manifest", Path("/run.json"), "run_manifest_sha256"),
        ("task_manifest", Path("/task.json"), "task_manifest_sha256"),
        ("stage1_result", Path("/generation-result.json"), "stage1_result_sha256"),
        (
            "stage1_invocation",
            Path("/generation-evidence/invocation.json"),
            "stage1_invocation_sha256",
        ),
        (
            "generation_metrics",
            Path("/generation-evidence/metrics.json"),
            "generation_metrics_sha256",
        ),
        (
            "generation_runtime_metrics",
            Path("/generation-evidence/runtime-metrics.json"),
            "generation_runtime_metrics_sha256",
        ),
        (
            "generation_usage",
            Path("/generation-evidence/usage.json"),
            "generation_usage_sha256",
        ),
        (
            "generation_codex_last",
            Path("/generation-evidence/codex-last.txt"),
            "generation_codex_last_sha256",
        ),
        (
            "generation_codex_output",
            Path("/generation-evidence/codex-output.log"),
            "generation_codex_output_sha256",
        ),
        (
            "generation_prompt",
            Path("/generation-evidence/prompt.txt"),
            "generation_prompt_sha256",
        ),
    ]
    for label, path, hash_key in file_hashes:
        check_hash(label, path, hashes[hash_key], issues)

    byte_pairs = [
        (
            "candidate prompt versus trusted prompt",
            Path("/candidate/prompt.py"),
            Path("/reference/prompt.py"),
        ),
        (
            "candidate translator versus trusted translator",
            Path("/candidate/py2mpy.py"),
            Path("/reference/py2mpy.py"),
        ),
    ]
    for label, left, right in byte_pairs:
        same = left.read_bytes() == right.read_bytes()
        print(f"BYTE_COMPARE {label}: {same}")
        if not same:
            issues.append(f"{label} differs")

    candidate_semantics = Path("/candidate/reference-semantics")
    trusted_semantics = Path("/reference/reference-semantics")
    semantics_issues = compare_trees(candidate_semantics, trusted_semantics)
    print(f"SEMANTICS_COMPARE issues={len(semantics_issues)}")
    for issue in semantics_issues:
        print(f"SEMANTICS_ISSUE {issue}")
        issues.append(f"reference-semantics integrity: {issue}")

    result = read_regular_json(Path("/generation-result.json"))
    usage = read_regular_json(Path("/generation-evidence/usage.json"))
    task = read_regular_json(Path("/task.json"))
    assert isinstance(result, dict)
    assert isinstance(usage, dict)
    assert isinstance(task, dict)
    # pipeline-v3 records a length-delimited digest in the authoritative
    # generation/task records.  audit-input.json also contains secondary tree
    # digests made by its launcher; that second serialization is not declared
    # in the input schema, so print those values but do not miscompare them as
    # if they used the pipeline-v3 algorithm.
    tree_checks = [
        (
            "candidate_tree",
            Path("/candidate"),
            result["outputs"]["workspace_sha256"],
            hashes["candidate_tree_sha256"],
        ),
        (
            "candidate_reference_semantics",
            candidate_semantics,
            task["inputs"]["reference_semantics_sha256"],
            hashes["candidate_reference_semantics_sha256"],
        ),
        (
            "trusted_reference_semantics",
            trusted_semantics,
            hashes["trusted_reference_semantics_manifest_sha256"],
            hashes["trusted_reference_semantics_sha256"],
        ),
        (
            "generation_trace",
            Path("/generation-evidence/codex-trace"),
            usage["source_trace_sha256"],
            hashes["generation_codex_trace_sha256"],
        ),
    ]
    for label, path, expected, secondary_recorded in tree_checks:
        try:
            actual = tree_sha256(path)
        except (OSError, ValueError) as error:
            print(f"TREE {label}: ERROR {error}")
            issues.append(f"{label}: {error}")
            continue
        status = "OK" if actual == expected else "MISMATCH"
        print(
            f"TREE {label}: {status} expected={expected} actual={actual} path={path}"
        )
        print(
            f"TREE {label}: audit-input secondary digest "
            f"(serialization undeclared)={secondary_recorded}"
        )
        if status != "OK":
            issues.append(f"{label} tree hash mismatch")

    evidence_hashes = result["outputs"]["evidence"]
    for relative, expected in sorted(evidence_hashes.items()):
        path = Path("/generation-evidence") / relative
        check_hash(f"generation-result:{relative}", path, expected, issues)

    trace_files = [path for rel, kind, path in tree_entries(
        Path("/generation-evidence/codex-trace")
    ) if kind == "file"]
    if not trace_files:
        issues.append("structured trace contains no files")
    for path in trace_files:
        print(f"TRACE_FILE {path} size={path.stat().st_size}")

    print(f"ISSUE_COUNT={len(issues)}")
    for issue in issues:
        print(f"ISSUE {issue}")
    return 1 if issues else 0


if __name__ == "__main__":
    sys.exit(main())
