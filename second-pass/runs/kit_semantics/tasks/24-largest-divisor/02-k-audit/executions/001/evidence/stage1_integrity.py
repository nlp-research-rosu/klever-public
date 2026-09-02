#!/usr/bin/env python3
"""Independent integrity and provenance checks for audit stage 1."""

from __future__ import annotations

from collections import Counter
import hashlib
import json
import os
from pathlib import Path
import stat
import sys


CHUNK = 1024 * 1024
AUDIT_INPUT = Path("/audit-input.json")
CAMPAIGN_LOCK = Path("/audit-campaign-lock.json")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(CHUNK), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_tree(root: Path) -> str:
    """Pipeline-v3 tree digest from tools/pipeline_contract.py."""
    digest = hashlib.sha256()
    entries: list[tuple[str, str, Path]] = []
    pending = [root]
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
                raise RuntimeError(f"linked or unsupported tree entry: {path}")
    for relative, kind, path in sorted(entries):
        encoded = relative.encode()
        digest.update(len(encoded).to_bytes(4, "big"))
        digest.update(encoded)
        digest.update(kind.encode() + b"\0")
        if kind == "file":
            size = path.stat(follow_symlinks=False).st_size
            digest.update(size.to_bytes(8, "big"))
            with path.open("rb") as stream:
                for chunk in iter(lambda: stream.read(CHUNK), b""):
                    digest.update(chunk)
    return digest.hexdigest()


def require_regular(path: Path) -> None:
    mode = path.lstat().st_mode
    if not stat.S_ISREG(mode):
        raise RuntimeError(f"not a real regular file: {path}")
    with path.open("rb") as stream:
        stream.read(1)


def require_directory(path: Path) -> None:
    mode = path.lstat().st_mode
    if not stat.S_ISDIR(mode):
        raise RuntimeError(f"not a real directory: {path}")


def inventory_tree(root: Path) -> dict[str, tuple[str, int, str | None]]:
    result: dict[str, tuple[str, int, str | None]] = {}
    pending = [root]
    while pending:
        directory = pending.pop()
        for child in os.scandir(directory):
            path = Path(child.path)
            mode = child.stat(follow_symlinks=False).st_mode
            relative = path.relative_to(root).as_posix()
            if stat.S_ISDIR(mode):
                result[relative] = ("directory", 0, None)
                pending.append(path)
            elif stat.S_ISREG(mode):
                result[relative] = ("file", path.stat().st_size, sha256_file(path))
            else:
                result[relative] = ("unsupported", 0, None)
    return result


def print_hash(label: str, path: Path, expected: str) -> None:
    observed = sha256_file(path)
    status = "MATCH" if observed == expected else "MISMATCH"
    print(f"{status} {label}: expected={expected} observed={observed} path={path}")


def main() -> int:
    audit = json.loads(AUDIT_INPUT.read_text(encoding="utf-8"))
    campaign = json.loads(CAMPAIGN_LOCK.read_text(encoding="utf-8"))
    hashes = audit["hashes"]

    print("DECLARATION")
    print(f"record_layout={audit['record_layout']}")
    print(f"problem_id={audit['problem_id']}")
    print(f"condition={audit['condition']}")
    print(f"semantics_mode={audit['semantics_mode']}")
    print(f"mount_reference_semantics={audit['mount_reference_semantics']}")

    required_files = [
        AUDIT_INPUT,
        CAMPAIGN_LOCK,
        Path("/run.json"),
        Path("/task.json"),
        Path("/generation-result.json"),
        Path("/reference/canonical.py"),
        Path("/reference/prompt.py"),
        Path("/reference/py2mpy.py"),
        Path("/generation-evidence/invocation.json"),
        Path("/generation-evidence/metrics.json"),
        Path("/generation-evidence/runtime-metrics.json"),
        Path("/generation-evidence/usage.json"),
        Path("/generation-evidence/codex-last.txt"),
        Path("/generation-evidence/codex-output.log"),
        Path("/generation-evidence/prompt.txt"),
    ]
    required_directories = [
        Path("/candidate"),
        Path("/reference/reference-semantics"),
        Path("/generation-evidence"),
        Path("/generation-evidence/codex-trace"),
    ]
    for path in required_files:
        require_regular(path)
        print(f"OK required regular file: {path}")
    for path in required_directories:
        require_directory(path)
        print(f"OK required real directory: {path}")

    print("CAMPAIGN")
    print(f"campaign_block_equal={audit['audit_campaign'] == campaign}")
    print_hash(
        "audit campaign lock",
        CAMPAIGN_LOCK,
        hashes["audit_campaign_lock_sha256"],
    )

    expected_files = [
        ("run manifest", Path("/run.json"), "run_manifest_sha256"),
        ("task manifest", Path("/task.json"), "task_manifest_sha256"),
        ("stage1 result", Path("/generation-result.json"), "stage1_result_sha256"),
        (
            "stage1 invocation",
            Path("/generation-evidence/invocation.json"),
            "stage1_invocation_sha256",
        ),
        (
            "generation metrics",
            Path("/generation-evidence/metrics.json"),
            "generation_metrics_sha256",
        ),
        (
            "runtime metrics",
            Path("/generation-evidence/runtime-metrics.json"),
            "generation_runtime_metrics_sha256",
        ),
        (
            "usage",
            Path("/generation-evidence/usage.json"),
            "generation_usage_sha256",
        ),
        (
            "codex last",
            Path("/generation-evidence/codex-last.txt"),
            "generation_codex_last_sha256",
        ),
        (
            "codex output",
            Path("/generation-evidence/codex-output.log"),
            "generation_codex_output_sha256",
        ),
        (
            "generation prompt",
            Path("/generation-evidence/prompt.txt"),
            "generation_prompt_sha256",
        ),
        ("canonical", Path("/reference/canonical.py"), "canonical_sha256"),
        ("trusted prompt", Path("/reference/prompt.py"), "trusted_prompt_sha256"),
        (
            "candidate prompt",
            Path("/candidate/prompt.py"),
            "candidate_prompt_sha256",
        ),
        (
            "trusted translator",
            Path("/reference/py2mpy.py"),
            "trusted_translator_sha256",
        ),
        (
            "candidate translator",
            Path("/candidate/py2mpy.py"),
            "candidate_translator_sha256",
        ),
    ]
    print("RECORDED FILE HASHES")
    for label, path, key in expected_files:
        print_hash(label, path, hashes[key])

    trace_files = sorted(
        path
        for path in Path("/generation-evidence/codex-trace").rglob("*")
        if path.is_file() and not path.is_symlink()
    )
    print(f"trace_regular_file_count={len(trace_files)}")
    for path in trace_files:
        print(f"trace_file_sha256={sha256_file(path)} path={path}")

    print("PIPELINE TREE HASHES")
    candidate_tree = sha256_tree(Path("/candidate"))
    supplied_tree = sha256_tree(Path("/reference/reference-semantics"))
    candidate_supplied_tree = sha256_tree(Path("/candidate/reference-semantics"))
    trace_tree = sha256_tree(Path("/generation-evidence/codex-trace"))
    generation_result = json.loads(
        Path("/generation-result.json").read_text(encoding="utf-8")
    )
    usage = json.loads(Path("/generation-evidence/usage.json").read_text(encoding="utf-8"))
    print(
        f"candidate={candidate_tree} "
        f"generation_result={generation_result['outputs']['workspace_sha256']} "
        f"match={candidate_tree == generation_result['outputs']['workspace_sha256']}"
    )
    print(
        f"trusted_supplied={supplied_tree} "
        f"recorded_manifest={hashes['trusted_reference_semantics_manifest_sha256']} "
        f"match={supplied_tree == hashes['trusted_reference_semantics_manifest_sha256']}"
    )
    print(
        f"candidate_supplied={candidate_supplied_tree} "
        f"trusted_supplied={supplied_tree} "
        f"match={candidate_supplied_tree == supplied_tree}"
    )
    print(
        f"trace={trace_tree} usage_source_trace={usage['source_trace_sha256']} "
        f"match={trace_tree == usage['source_trace_sha256']}"
    )

    print("BYTE/TYPE TREE COMPARISON")
    trusted_inventory = inventory_tree(Path("/reference/reference-semantics"))
    candidate_inventory = inventory_tree(Path("/candidate/reference-semantics"))
    trusted_only = sorted(trusted_inventory.keys() - candidate_inventory.keys())
    candidate_only = sorted(candidate_inventory.keys() - trusted_inventory.keys())
    differing = sorted(
        relative
        for relative in trusted_inventory.keys() & candidate_inventory.keys()
        if trusted_inventory[relative] != candidate_inventory[relative]
    )
    print(f"trusted_entries={len(trusted_inventory)}")
    print(f"candidate_entries={len(candidate_inventory)}")
    print(f"trusted_only={trusted_only}")
    print(f"candidate_only={candidate_only}")
    print(f"differing={differing}")
    print(
        "candidate_prompt_byte_equal="
        f"{Path('/candidate/prompt.py').read_bytes() == Path('/reference/prompt.py').read_bytes()}"
    )
    print(
        "candidate_translator_byte_equal="
        f"{Path('/candidate/py2mpy.py').read_bytes() == Path('/reference/py2mpy.py').read_bytes()}"
    )

    print("RECORD CONSISTENCY")
    task = json.loads(Path("/task.json").read_text(encoding="utf-8"))
    run = json.loads(Path("/run.json").read_text(encoding="utf-8"))
    invocation = json.loads(
        Path("/generation-evidence/invocation.json").read_text(encoding="utf-8")
    )
    metrics = json.loads(
        Path("/generation-evidence/metrics.json").read_text(encoding="utf-8")
    )
    runtime = json.loads(
        Path("/generation-evidence/runtime-metrics.json").read_text(encoding="utf-8")
    )
    print(f"audit_manifest_equals_task={audit['manifest'] == task}")
    print(
        "audit_manifest_only_keys="
        f"{sorted(audit['manifest'].keys() - task.keys())}"
    )
    print(
        "task_manifest_only_keys="
        f"{sorted(task.keys() - audit['manifest'].keys())}"
    )
    print(f"run_condition_equals_task={run['condition'] == task['condition']}")
    print(
        "invocation_evidence_equals_result="
        f"{invocation['outputs']['evidence'] == generation_result['outputs']['evidence']}"
    )
    print(
        "metrics_status_tuple="
        f"{(metrics['status'], metrics['exit_code'], metrics['oom_killed'], metrics['timeout_marker'])}"
    )
    print(
        "runtime_status_tuple="
        f"{(runtime['final_exit_code'], runtime['model_exit_code'], runtime['harness_exit_code'], runtime['oom_killed'], runtime['timeout_marker'])}"
    )

    print("STRUCTURED TRACE FULL PARSE")
    event_types: Counter[str] = Counter()
    response_types: Counter[str] = Counter()
    function_names: Counter[str] = Counter()
    trace_lines = 0
    for path in trace_files:
        with path.open(encoding="utf-8") as stream:
            for line_number, line in enumerate(stream, 1):
                record = json.loads(line)
                trace_lines += 1
                event_types[str(record.get("type"))] += 1
                payload = record.get("payload", {})
                if record.get("type") == "response_item":
                    response_types[str(payload.get("type"))] += 1
                    if payload.get("type") == "function_call":
                        function_names[str(payload.get("name"))] += 1
    output_bytes = Path("/generation-evidence/codex-output.log").read_bytes()
    print(f"trace_json_lines={trace_lines}")
    print(f"trace_event_types={dict(sorted(event_types.items()))}")
    print(f"trace_response_types={dict(sorted(response_types.items()))}")
    print(f"trace_function_names={dict(sorted(function_names.items()))}")
    print(f"codex_output_bytes_read={len(output_bytes)}")
    print(f"codex_output_lines={output_bytes.count(bytes([10]))}")
    print("STAGE1_INTEGRITY_CHECKS_COMPLETE")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as error:
        print(f"INTEGRITY_CHECK_ERROR: {error}", file=sys.stderr)
        raise
