#!/usr/bin/env python3
"""Independent integrity checks over launcher-mounted audit inputs."""

from __future__ import annotations

from collections import Counter
import hashlib
import json
from pathlib import Path
import stat
import sys


AUDIT_INPUT = Path("/audit-input.json")
LOCK = Path("/audit-campaign-lock.json")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def check_regular(path: Path, failures: list[str]) -> None:
    try:
        info = path.lstat()
    except OSError as err:
        failures.append(f"unreadable or absent required file {path}: {err}")
        return
    if stat.S_ISLNK(info.st_mode):
        failures.append(f"required file is a symlink: {path}")
    elif not stat.S_ISREG(info.st_mode):
        failures.append(f"required path is not a regular file: {path}")
    try:
        with path.open("rb") as stream:
            stream.read(1)
    except OSError as err:
        failures.append(f"required file cannot be read {path}: {err}")


def check_tree_no_symlinks(root: Path, failures: list[str]) -> None:
    for path in sorted(root.rglob("*")):
        if path.is_symlink():
            failures.append(f"symlinked tree entry: {path}")


def main() -> int:
    failures: list[str] = []
    audit = json.loads(AUDIT_INPUT.read_text())
    lock = json.loads(LOCK.read_text())

    print(f"record_layout={audit.get('record_layout')}")
    print(f"semantics_mode={audit.get('semantics_mode')}")
    print(f"problem_id={audit.get('problem_id')}")
    print(f"condition={audit.get('condition')}")

    if audit.get("audit_campaign") != lock:
        failures.append("audit_campaign block is not exactly equal to campaign lock")
    else:
        print("campaign_block_exact_match=YES")

    actual_lock_hash = sha256(LOCK)
    expected_lock_hash = audit["hashes"]["audit_campaign_lock_sha256"]
    print(f"audit_campaign_lock_sha256={actual_lock_hash}")
    if actual_lock_hash != expected_lock_hash:
        failures.append(
            f"campaign lock hash mismatch: expected {expected_lock_hash}, got {actual_lock_hash}"
        )

    layout = audit.get("record_layout")
    required_by_layout = {
        "pipeline-v3": [
            "/run.json",
            "/task.json",
            "/generation-result.json",
            "/generation-evidence/invocation.json",
            "/generation-evidence/metrics.json",
            "/generation-evidence/runtime-metrics.json",
            "/generation-evidence/usage.json",
            "/generation-evidence/codex-last.txt",
            "/generation-evidence/codex-output.log",
            "/generation-evidence/prompt.txt",
        ],
        "legacy-selected-stage1": [
            "/run.json",
            "/task.json",
            "/generation-result.json",
            "/generation-evidence/invocation.json",
            "/generation-evidence/metrics.json",
            "/generation-evidence/codex-last.txt",
            "/generation-evidence/codex-output.log",
            "/generation-evidence/prompt.txt",
        ],
        "legacy": [
            "/generation-evidence/run-input.json",
            "/generation-evidence/metrics.json",
            "/generation-evidence/codex-last.txt",
            "/generation-evidence/codex-output.log",
        ],
    }
    if layout not in required_by_layout:
        failures.append(f"unknown record layout: {layout!r}")
    else:
        for raw_path in required_by_layout[layout]:
            check_regular(Path(raw_path), failures)
        usage = Path("/generation-evidence/usage.json")
        if layout == "legacy-selected-stage1" and usage.exists():
            check_regular(usage, failures)

    trace_root = Path("/generation-evidence/codex-trace")
    if not trace_root.is_dir() or trace_root.is_symlink():
        failures.append("structured trace root is absent, symlinked, or not a directory")
    trace_files = sorted(trace_root.rglob("*.jsonl")) if trace_root.is_dir() else []
    if not trace_files:
        failures.append("structured trace has no JSONL files")
    for path in trace_files:
        check_regular(path, failures)

    container_paths = audit.get("container_paths", {})
    for label, raw_path in sorted(container_paths.items()):
        path = Path(raw_path)
        if not path.exists():
            failures.append(f"launcher-declared container path missing: {label}={path}")
        elif path.is_symlink():
            failures.append(f"launcher-declared container path is symlinked: {label}={path}")
        print(f"container_path[{label}]={path}")

    expected_file_hashes = {
        Path("/candidate/prompt.py"): "candidate_prompt_sha256",
        Path("/candidate/py2mpy.py"): "candidate_translator_sha256",
        Path("/reference/canonical.py"): "canonical_sha256",
        Path("/generation-evidence/codex-last.txt"): "generation_codex_last_sha256",
        Path("/generation-evidence/codex-output.log"): "generation_codex_output_sha256",
        Path("/generation-evidence/metrics.json"): "generation_metrics_sha256",
        Path("/generation-evidence/prompt.txt"): "generation_prompt_sha256",
        Path("/generation-evidence/usage.json"): "generation_usage_sha256",
        Path("/generation-evidence/invocation.json"): "stage1_invocation_sha256",
        Path("/generation-result.json"): "stage1_result_sha256",
        Path("/run.json"): "run_manifest_sha256",
        Path("/task.json"): "task_manifest_sha256",
        Path("/reference/prompt.py"): "trusted_prompt_sha256",
        Path("/reference/py2mpy.py"): "trusted_translator_sha256",
    }
    for path, key in expected_file_hashes.items():
        if not path.exists():
            if audit["hashes"].get(key) is not None:
                failures.append(f"declared hashed file missing: {path}")
            continue
        actual = sha256(path)
        expected = audit["hashes"].get(key)
        print(f"sha256[{path}]={actual}")
        if actual != expected:
            failures.append(f"hash mismatch for {path}: expected {expected}, got {actual}")

    task_hash = sha256(Path("/task.json"))
    if task_hash != audit["hashes"].get("manifest_sha256"):
        failures.append("manifest_sha256 does not match mounted /task.json")

    generation_result = json.loads(Path("/generation-result.json").read_text())
    for relative, expected in sorted(
        generation_result.get("outputs", {}).get("evidence", {}).items()
    ):
        path = Path("/generation-evidence") / relative
        if not path.exists():
            failures.append(f"generation-result output missing: {path}")
            continue
        actual = sha256(path)
        print(f"generation_output_sha256[{relative}]={actual}")
        if actual != expected:
            failures.append(
                f"generation-result hash mismatch for {relative}: expected {expected}, got {actual}"
            )

    if Path("/candidate/prompt.py").read_bytes() != Path("/reference/prompt.py").read_bytes():
        failures.append("candidate prompt differs byte-for-byte from trusted prompt")
    else:
        print("candidate_prompt_byte_identity=YES")
    if Path("/candidate/py2mpy.py").read_bytes() != Path("/reference/py2mpy.py").read_bytes():
        failures.append("candidate translator differs byte-for-byte from trusted translator")
    else:
        print("candidate_translator_byte_identity=YES")

    reference_semantics = Path("/reference/reference-semantics")
    if audit.get("semantics_mode") == "GENERATED_SEMANTICS":
        if reference_semantics.exists() or reference_semantics.is_symlink():
            failures.append("trusted reference semantics unexpectedly exists in generated mode")
        else:
            print("trusted_reference_semantics_absent=YES")

    for root in [
        Path("/candidate"),
        Path("/reference"),
        Path("/generation-evidence"),
    ]:
        check_tree_no_symlinks(root, failures)

    line_types: Counter[str] = Counter()
    payload_types: Counter[str] = Counter()
    trace_lines = 0
    for path in trace_files:
        expected = generation_result["outputs"]["evidence"].get(
            str(path.relative_to("/generation-evidence"))
        )
        actual = sha256(path)
        print(f"trace_file_sha256[{path}]={actual}")
        if expected is not None and actual != expected:
            failures.append(f"structured trace file hash mismatch: {path}")
        with path.open(encoding="utf-8") as stream:
            for line_number, line in enumerate(stream, 1):
                trace_lines += 1
                try:
                    record = json.loads(line)
                except json.JSONDecodeError as err:
                    failures.append(f"invalid JSONL at {path}:{line_number}: {err}")
                    continue
                line_types[str(record.get("type"))] += 1
                payload = record.get("payload")
                if isinstance(payload, dict):
                    payload_types[str(payload.get("type"))] += 1
    print(f"trace_json_lines={trace_lines}")
    print(f"trace_record_types={dict(sorted(line_types.items()))}")
    print(f"trace_payload_types={dict(sorted(payload_types.items()))}")

    if failures:
        print("INTEGRITY_RESULT=FAIL")
        for failure in failures:
            print(f"FAILURE: {failure}")
        return 1
    print("INTEGRITY_RESULT=PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
