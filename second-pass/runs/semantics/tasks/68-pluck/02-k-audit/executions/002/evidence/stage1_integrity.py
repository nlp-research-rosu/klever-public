#!/usr/bin/env python3
"""Independent integrity and record-layout checks for audit 68-pluck."""

from __future__ import annotations

import hashlib
import json
import os
import stat
import sys
from collections import Counter
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")
LOCK = Path("/audit-campaign-lock.json")
CANDIDATE = Path("/candidate")
REFERENCE = Path("/reference")
GENERATION = Path("/generation-evidence")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def tree_entries(root: Path) -> list[tuple[str, str, Path]]:
    if not stat.S_ISDIR(root.lstat().st_mode):
        raise ValueError(f"tree root is not a real directory: {root}")
    pending = [root]
    entries: list[tuple[str, str, Path]] = []
    while pending:
        directory = pending.pop()
        for child in os.scandir(directory):
            path = Path(child.path)
            mode = child.stat(follow_symlinks=False).st_mode
            relative = path.relative_to(root).as_posix()
            if stat.S_ISDIR(mode):
                entries.append((relative, "directory", path))
                pending.append(path)
            elif stat.S_ISREG(mode):
                entries.append((relative, "file", path))
            else:
                entries.append((relative, f"unsupported:{stat.S_IFMT(mode):o}", path))
    return sorted(entries)


def sha256_tree(root: Path) -> str:
    """Reproduce the launcher pipeline_contract.sha256_tree algorithm."""
    digest = hashlib.sha256()
    for relative, kind, path in tree_entries(root):
        if kind not in {"directory", "file"}:
            raise ValueError(f"unsupported tree entry: {relative} ({kind})")
        encoded = relative.encode()
        digest.update(len(encoded).to_bytes(4, "big"))
        digest.update(encoded)
        digest.update(kind.encode() + b"\0")
        if kind == "file":
            size = path.stat(follow_symlinks=False).st_size
            digest.update(size.to_bytes(8, "big"))
            with path.open("rb") as stream:
                for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                    digest.update(chunk)
    return digest.hexdigest()


def legacy_tree_digest(root: Path) -> str:
    """Reproduce the recorded legacy tree_digest algorithm."""
    digest = hashlib.sha256()
    for relative, kind, path in tree_entries(root):
        if kind not in {"directory", "file"}:
            raise ValueError(f"unsupported tree entry: {relative} ({kind})")
        digest.update(relative.encode() + b"\0" + kind.encode() + b"\0")
        if kind == "file":
            digest.update(path.read_bytes())
    return digest.hexdigest()


def require_regular(path: Path, failures: list[str]) -> None:
    try:
        mode = path.lstat().st_mode
    except OSError as error:
        failures.append(f"missing/unreadable required file {path}: {error}")
        return
    if not stat.S_ISREG(mode):
        failures.append(f"required path is not a real regular file: {path}")


def require_directory(path: Path, failures: list[str]) -> None:
    try:
        mode = path.lstat().st_mode
    except OSError as error:
        failures.append(f"missing/unreadable required directory {path}: {error}")
        return
    if not stat.S_ISDIR(mode):
        failures.append(f"required path is not a real directory: {path}")


def compare_trees(left: Path, right: Path, failures: list[str]) -> None:
    left_entries = {(rel, kind): path for rel, kind, path in tree_entries(left)}
    right_entries = {(rel, kind): path for rel, kind, path in tree_entries(right)}
    if left_entries.keys() != right_entries.keys():
        missing = sorted(left_entries.keys() - right_entries.keys())
        additional = sorted(right_entries.keys() - left_entries.keys())
        failures.append(f"semantics missing/mistyped entries: {missing}")
        failures.append(f"semantics additional/mistyped entries: {additional}")
    for key in sorted(left_entries.keys() & right_entries.keys()):
        rel, kind = key
        if kind == "file":
            left_hash = sha256_file(left_entries[key])
            right_hash = sha256_file(right_entries[key])
            if left_hash != right_hash:
                failures.append(
                    f"semantics content mismatch: {rel}: {left_hash} != {right_hash}"
                )


def main() -> int:
    failures: list[str] = []
    for path in (AUDIT_INPUT, LOCK, Path("/run.json"), Path("/task.json"),
                 Path("/generation-result.json")):
        require_regular(path, failures)
    require_directory(CANDIDATE, failures)
    require_directory(REFERENCE, failures)
    require_directory(GENERATION, failures)
    if failures:
        for failure in failures:
            print(f"FAIL {failure}")
        return 1

    audit = json.loads(AUDIT_INPUT.read_text())
    lock = json.loads(LOCK.read_text())
    print(f"record_layout={audit.get('record_layout')}")
    print(f"semantics_mode={audit.get('semantics_mode')}")
    if audit.get("record_layout") != "legacy-selected-stage1":
        failures.append("unexpected record_layout")
    if audit.get("semantics_mode") != "SUPPLIED_SEMANTICS":
        failures.append("unexpected semantics mode")

    lock_hash = sha256_file(LOCK)
    expected_lock_hash = audit["hashes"]["audit_campaign_lock_sha256"]
    print(f"audit_campaign_lock_sha256={lock_hash} expected={expected_lock_hash}")
    if lock_hash != expected_lock_hash:
        failures.append("campaign-lock byte hash mismatch")
    if audit["audit_campaign"] != lock:
        failures.append("campaign-lock JSON does not equal audit_campaign block")
    else:
        print("campaign_lock_json_matches_audit_campaign=true")

    required_files = [
        Path("/run.json"),
        Path("/task.json"),
        Path("/generation-result.json"),
        GENERATION / "invocation.json",
        GENERATION / "metrics.json",
        GENERATION / "codex-last.txt",
        GENERATION / "codex-output.log",
        GENERATION / "prompt.txt",
    ]
    if (GENERATION / "usage.json").exists() or (GENERATION / "usage.json").is_symlink():
        required_files.append(GENERATION / "usage.json")
    for path in required_files:
        require_regular(path, failures)
    require_directory(GENERATION / "codex-trace", failures)

    declared_file_hashes = {
        LOCK: "audit_campaign_lock_sha256",
        REFERENCE / "canonical.py": "canonical_sha256",
        REFERENCE / "prompt.py": "trusted_prompt_sha256",
        REFERENCE / "py2mpy.py": "trusted_translator_sha256",
        CANDIDATE / "prompt.py": "candidate_prompt_sha256",
        CANDIDATE / "py2mpy.py": "candidate_translator_sha256",
        Path("/run.json"): "run_manifest_sha256",
        Path("/task.json"): "task_manifest_sha256",
        Path("/generation-result.json"): "stage1_result_sha256",
        GENERATION / "invocation.json": "stage1_invocation_sha256",
        GENERATION / "metrics.json": "generation_metrics_sha256",
        GENERATION / "codex-last.txt": "generation_codex_last_sha256",
        GENERATION / "codex-output.log": "generation_codex_output_sha256",
        GENERATION / "prompt.txt": "generation_prompt_sha256",
    }
    if (GENERATION / "usage.json").is_file():
        declared_file_hashes[GENERATION / "usage.json"] = "generation_usage_sha256"
    for path, key in declared_file_hashes.items():
        require_regular(path, failures)
        if path.is_file() and not path.is_symlink():
            actual = sha256_file(path)
            expected = audit["hashes"][key]
            print(f"{key}={actual} expected={expected}")
            if actual != expected:
                failures.append(f"recorded hash mismatch for {path}")

    if audit["hashes"]["manifest_sha256"] != sha256_file(Path("/task.json")):
        failures.append("manifest_sha256 does not match task.json")
    else:
        print("manifest_sha256_matches_task_json=true")

    container_paths = audit["container_paths"]
    expected_container_paths = {
        "audit_campaign_lock": LOCK,
        "candidate": CANDIDATE,
        "canonical": REFERENCE / "canonical.py",
        "generation_last": GENERATION / "codex-last.txt",
        "generation_manifest": GENERATION / "invocation.json",
        "generation_metrics": GENERATION / "metrics.json",
        "generation_output": GENERATION / "codex-output.log",
        "generation_root": GENERATION,
        "generation_trace": GENERATION / "codex-trace",
        "run_manifest": Path("/run.json"),
        "stage1_result": Path("/generation-result.json"),
        "task_manifest": Path("/task.json"),
        "translator": REFERENCE / "py2mpy.py",
        "trusted_prompt": REFERENCE / "prompt.py",
    }
    for key, expected_path in expected_container_paths.items():
        declared = container_paths.get(key)
        print(f"container_path[{key}]={declared}")
        if declared != str(expected_path):
            failures.append(f"container path mismatch for {key}")

    trusted_semantics = REFERENCE / "reference-semantics"
    candidate_semantics = CANDIDATE / "reference-semantics"
    require_directory(trusted_semantics, failures)
    require_directory(candidate_semantics, failures)
    if trusted_semantics.is_dir() and candidate_semantics.is_dir():
        compare_trees(trusted_semantics, candidate_semantics, failures)
        for label, path in (
            ("trusted", trusted_semantics),
            ("candidate", candidate_semantics),
        ):
            modern = sha256_tree(path)
            legacy = legacy_tree_digest(path)
            print(f"{label}_semantics_sha256_tree={modern}")
            print(f"{label}_semantics_legacy_tree_digest={legacy}")
        manifest_hash = audit["hashes"]["trusted_reference_semantics_manifest_sha256"]
        print(f"recorded_trusted_semantics_manifest_sha256={manifest_hash}")
        if sha256_tree(trusted_semantics) != manifest_hash:
            failures.append("trusted semantics manifest tree hash mismatch")
        print(
            "recorded_launcher_semantics_hashes="
            f"trusted:{audit['hashes']['trusted_reference_semantics_sha256']} "
            f"candidate:{audit['hashes']['candidate_reference_semantics_sha256']} "
            f"legacy:{audit['hashes']['trusted_reference_semantics_legacy_sha256']}"
        )
        if (
            audit["hashes"]["trusted_reference_semantics_sha256"]
            != audit["hashes"]["candidate_reference_semantics_sha256"]
        ):
            failures.append("recorded candidate/trusted launcher semantics hashes disagree")
        if sha256_tree(trusted_semantics) == sha256_tree(candidate_semantics):
            print("candidate_semantics_exact_tree_match=true")

    candidate_tree = sha256_tree(CANDIDATE)
    generation_workspace = json.loads(Path("/generation-result.json").read_text())[
        "outputs"
    ]["workspace_sha256"]
    print(
        f"candidate_manifest_tree_sha256={candidate_tree} "
        f"generation_workspace_expected={generation_workspace}"
    )
    print(
        "recorded_launcher_candidate_tree_sha256="
        f"{audit['hashes']['candidate_tree_sha256']}"
    )
    if candidate_tree != generation_workspace:
        failures.append("candidate manifest tree hash mismatch")

    trace_root = GENERATION / "codex-trace"
    trace_tree = sha256_tree(trace_root)
    usage = json.loads((GENERATION / "usage.json").read_text())
    source_trace_hash = usage["source_trace_sha256"]
    print(
        f"generation_trace_manifest_tree_sha256={trace_tree} "
        f"usage_source_trace_expected={source_trace_hash}"
    )
    print(
        "recorded_launcher_generation_trace_sha256="
        f"{audit['hashes']['generation_codex_trace_sha256']}"
    )
    if trace_tree != source_trace_hash:
        failures.append("generation trace manifest tree hash mismatch")

    generation_result = json.loads(Path("/generation-result.json").read_text())
    recorded_evidence = generation_result["outputs"]["evidence"]
    trace_lines = 0
    trace_types: Counter[str] = Counter()
    jsonl_files = sorted(trace_root.rglob("*.jsonl"))
    if not jsonl_files:
        failures.append("structured trace contains no JSONL files")
    for path in jsonl_files:
        if path.is_symlink() or not path.is_file():
            failures.append(f"trace entry is not a real regular file: {path}")
            continue
        relative = path.relative_to(GENERATION).as_posix()
        actual = sha256_file(path)
        expected = recorded_evidence.get(relative)
        print(f"trace_file={relative} sha256={actual} expected={expected}")
        if actual != expected:
            failures.append(f"trace file hash mismatch: {relative}")
        with path.open() as stream:
            for line_number, line in enumerate(stream, 1):
                try:
                    item = json.loads(line)
                except ValueError as error:
                    failures.append(f"malformed trace JSON: {relative}:{line_number}: {error}")
                    continue
                trace_lines += 1
                trace_types[str(item.get("type"))] += 1
    print(f"trace_json_records={trace_lines}")
    print(f"trace_top_level_types={dict(sorted(trace_types.items()))}")

    for relative, expected in sorted(recorded_evidence.items()):
        path = GENERATION / relative
        require_regular(path, failures)
        if path.is_file() and not path.is_symlink():
            actual = sha256_file(path)
            print(f"generation_result_evidence[{relative}]={actual} expected={expected}")
            if actual != expected:
                failures.append(f"generation-result evidence mismatch: {relative}")

    if failures:
        for failure in failures:
            print(f"FAIL {failure}")
        print(f"failure_count={len(failures)}")
        return 1
    print("failure_count=0")
    print("STAGE1_INTEGRITY=PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
