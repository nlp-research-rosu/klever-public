#!/usr/bin/env python3
"""Independent provenance and supplied-semantics integrity checks."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from collections import Counter
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")
CAMPAIGN_LOCK = Path("/audit-campaign-lock.json")
CANDIDATE = Path("/candidate")
REFERENCE = Path("/reference")
GENERATION = Path("/generation-evidence")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def load_json(path: Path):
    with path.open("rb") as stream:
        return json.load(stream)


def type_name(path: Path) -> str:
    mode = path.lstat().st_mode
    if stat.S_ISREG(mode):
        return "file"
    if stat.S_ISDIR(mode):
        return "dir"
    if stat.S_ISLNK(mode):
        return "symlink"
    return "other"


def tree_records(root: Path):
    records = []
    for current, dirs, files in os.walk(root, topdown=True, followlinks=False):
        current_path = Path(current)
        for name in sorted(dirs + files):
            path = current_path / name
            relative = path.relative_to(root).as_posix()
            entry_type = type_name(path)
            if entry_type == "file":
                records.append(
                    (relative, entry_type, path.stat().st_size, sha256_file(path))
                )
            elif entry_type == "symlink":
                records.append((relative, entry_type, 0, os.readlink(path)))
            else:
                records.append((relative, entry_type, 0, ""))
    return sorted(records)


def tree_manifest_hash(records) -> str:
    digest = hashlib.sha256()
    for relative, entry_type, size, content_hash in records:
        digest.update(
            f"{entry_type}\t{relative}\t{size}\t{content_hash}\n".encode("utf-8")
        )
    return digest.hexdigest()


def main() -> int:
    failures: list[str] = []
    audit_input = load_json(AUDIT_INPUT)
    campaign_lock = load_json(CAMPAIGN_LOCK)

    print(f"record_layout={audit_input.get('record_layout')}")
    print(f"semantics_mode={audit_input.get('semantics_mode')}")
    print(f"problem_id={audit_input.get('problem_id')}")

    campaign_equal = audit_input.get("audit_campaign") == campaign_lock
    campaign_actual_hash = sha256_file(CAMPAIGN_LOCK)
    campaign_expected_hash = audit_input["hashes"]["audit_campaign_lock_sha256"]
    print(f"campaign_block_exact_match={campaign_equal}")
    print(f"campaign_lock_sha256_actual={campaign_actual_hash}")
    print(f"campaign_lock_sha256_expected={campaign_expected_hash}")
    if not campaign_equal or campaign_actual_hash != campaign_expected_hash:
        failures.append("campaign lock mismatch")

    for name, raw_path in sorted(audit_input["container_paths"].items()):
        path = Path(raw_path)
        exists = path.exists()
        readable = os.access(path, os.R_OK)
        entry_type = type_name(path) if exists or path.is_symlink() else "missing"
        print(
            f"container_path[{name}]={path} exists={exists} "
            f"readable={readable} type={entry_type}"
        )
        if not exists or not readable:
            failures.append(f"launcher-declared mount unavailable: {name}={path}")

    required = [
        Path("/run.json"),
        Path("/task.json"),
        Path("/generation-result.json"),
        GENERATION / "invocation.json",
        GENERATION / "metrics.json",
        GENERATION / "codex-last.txt",
        GENERATION / "codex-output.log",
        GENERATION / "prompt.txt",
    ]
    if (GENERATION / "usage.json").exists():
        required.append(GENERATION / "usage.json")
    trace_root = GENERATION / "codex-trace"
    required.append(trace_root)

    for path in required:
        kind = type_name(path) if path.exists() or path.is_symlink() else "missing"
        readable = path.exists() and os.access(path, os.R_OK)
        print(f"required_record={path} readable={readable} type={kind}")
        if not readable or kind == "symlink":
            failures.append(f"required record invalid: {path}")

    hash_checks = {
        CAMPAIGN_LOCK: "audit_campaign_lock_sha256",
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
        GENERATION / "usage.json": "generation_usage_sha256",
    }
    for path, key in hash_checks.items():
        if not path.is_file() or path.is_symlink():
            failures.append(f"hash target is not a regular non-symlink file: {path}")
            continue
        actual = sha256_file(path)
        expected = audit_input["hashes"].get(key)
        matches = actual == expected
        print(
            f"hash[{key}] path={path} actual={actual} expected={expected} "
            f"matches={matches}"
        )
        if not matches:
            failures.append(f"recorded hash mismatch: {path}")

    prompt_equal = (CANDIDATE / "prompt.py").read_bytes() == (
        REFERENCE / "prompt.py"
    ).read_bytes()
    translator_equal = (CANDIDATE / "py2mpy.py").read_bytes() == (
        REFERENCE / "py2mpy.py"
    ).read_bytes()
    print(f"candidate_prompt_byte_equal={prompt_equal}")
    print(f"candidate_translator_byte_equal={translator_equal}")
    if not prompt_equal:
        failures.append("candidate prompt differs from trusted prompt")
    if not translator_equal:
        failures.append("candidate translator differs from trusted translator")

    trusted_semantics = REFERENCE / "reference-semantics"
    candidate_semantics = CANDIDATE / "reference-semantics"
    if audit_input.get("semantics_mode") != "SUPPLIED_SEMANTICS":
        failures.append("unexpected semantics mode")
    if not trusted_semantics.is_dir() or trusted_semantics.is_symlink():
        failures.append("trusted supplied semantics is missing or symlinked")
    if not candidate_semantics.is_dir() or candidate_semantics.is_symlink():
        failures.append("candidate supplied semantics is missing or symlinked")
    trusted_records = tree_records(trusted_semantics)
    candidate_records = tree_records(candidate_semantics)
    print(f"trusted_semantics_entries={len(trusted_records)}")
    print(f"candidate_semantics_entries={len(candidate_records)}")
    print(
        "trusted_semantics_independent_manifest_sha256="
        + tree_manifest_hash(trusted_records)
    )
    print(
        "candidate_semantics_independent_manifest_sha256="
        + tree_manifest_hash(candidate_records)
    )
    semantics_equal = candidate_records == trusted_records
    print(f"supplied_semantics_recursive_type_path_byte_equal={semantics_equal}")
    if not semantics_equal:
        failures.append("candidate supplied semantics tree differs from trusted tree")
        trusted_map = {record[0]: record[1:] for record in trusted_records}
        candidate_map = {record[0]: record[1:] for record in candidate_records}
        for relative in sorted(set(trusted_map) | set(candidate_map)):
            if trusted_map.get(relative) != candidate_map.get(relative):
                print(
                    f"semantics_difference path={relative} "
                    f"trusted={trusted_map.get(relative)} "
                    f"candidate={candidate_map.get(relative)}"
                )

    all_candidate_records = tree_records(CANDIDATE)
    candidate_symlinks = [
        relative
        for relative, entry_type, _, _ in all_candidate_records
        if entry_type == "symlink"
    ]
    print(f"candidate_symlinks={candidate_symlinks}")

    result = load_json(Path("/generation-result.json"))
    evidence_hashes = result.get("outputs", {}).get("evidence", {})
    for relative, expected in sorted(evidence_hashes.items()):
        path = GENERATION / relative
        valid = path.is_file() and not path.is_symlink()
        actual = sha256_file(path) if valid else None
        matches = valid and actual == expected
        print(
            f"generation_result_evidence={relative} valid={valid} "
            f"actual={actual} expected={expected} matches={matches}"
        )
        if not matches:
            failures.append(f"generation-result evidence mismatch: {relative}")

    jsonl_files = sorted(trace_root.rglob("*.jsonl"))
    non_jsonl_entries = [
        path
        for path in trace_root.rglob("*")
        if path.is_file() and path.suffix != ".jsonl"
    ]
    print(f"trace_jsonl_files={len(jsonl_files)}")
    print(f"trace_non_jsonl_files={len(non_jsonl_entries)}")
    if not jsonl_files:
        failures.append("structured trace contains no JSONL files")
    top_types: Counter[str] = Counter()
    nested_types: Counter[str] = Counter()
    trace_lines = 0
    for path in jsonl_files:
        if path.is_symlink():
            failures.append(f"trace file is symlinked: {path}")
            continue
        with path.open("r", encoding="utf-8") as stream:
            for line_number, line in enumerate(stream, 1):
                trace_lines += 1
                try:
                    item = json.loads(line)
                except json.JSONDecodeError as err:
                    failures.append(f"invalid JSONL {path}:{line_number}: {err}")
                    continue
                top_types[str(item.get("type"))] += 1
                payload = item.get("payload")
                if isinstance(payload, dict):
                    nested_types[str(payload.get("type"))] += 1
    print(f"trace_lines_parsed={trace_lines}")
    print(f"trace_top_level_types={dict(sorted(top_types.items()))}")
    print(f"trace_payload_types={dict(sorted(nested_types.items()))}")

    for path in [GENERATION / "codex-output.log", GENERATION / "codex-last.txt"]:
        data = path.read_bytes()
        print(
            f"generation_text_scan path={path} bytes={len(data)} "
            f"lines={data.count(bytes([10]))} nul_bytes={data.count(bytes([0]))} "
            f"kprove_top_mentions={data.count(b'#Top')} "
            f"result_marker_mentions={data.count(b'RESULT: KPROVE_PASSED')}"
        )

    print(f"FAILURE_COUNT={len(failures)}")
    for failure in failures:
        print(f"FAILURE={failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
