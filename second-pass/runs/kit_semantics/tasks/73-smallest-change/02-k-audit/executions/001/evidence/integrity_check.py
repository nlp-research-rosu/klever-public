#!/usr/bin/env python3
"""Independent mounted-input and pipeline-v3 integrity checks."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")
LOCK = Path("/audit-campaign-lock.json")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def entry_manifest(root: Path) -> list[tuple[str, str, str | None]]:
    entries: list[tuple[str, str, str | None]] = []
    for path in sorted(root.rglob("*")):
        rel = path.relative_to(root).as_posix()
        if path.is_symlink():
            entries.append((rel, "symlink", os.readlink(path)))
        elif path.is_dir():
            entries.append((rel, "dir", None))
        elif path.is_file():
            entries.append((rel, "file", sha256(path)))
        else:
            entries.append((rel, "other", None))
    return entries


def manifest_sha256(entries: list[tuple[str, str, str | None]]) -> str:
    payload = json.dumps(
        entries, ensure_ascii=False, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def check_hash(
    label: str, path: Path, expected: str, failures: list[str]
) -> None:
    actual = sha256(path)
    ok = actual == expected
    print(f"HASH {label} ok={ok} actual={actual} expected={expected} path={path}")
    if not ok:
        failures.append(f"hash mismatch: {label}")


def main() -> int:
    failures: list[str] = []
    audit = json.loads(AUDIT_INPUT.read_text())
    lock = json.loads(LOCK.read_text())
    print(f"record_layout={audit.get('record_layout')}")
    print(f"semantics_mode={audit.get('semantics_mode')}")
    print(f"campaign_block_equal={audit.get('audit_campaign') == lock}")
    if audit.get("audit_campaign") != lock:
        failures.append("campaign block does not equal lock")

    paths = audit["container_paths"]
    required_keys = [
        "audit_campaign_lock",
        "candidate",
        "canonical",
        "generation_last",
        "generation_manifest",
        "generation_metrics",
        "generation_output",
        "generation_root",
        "generation_trace",
        "run_manifest",
        "stage1_result",
        "task_manifest",
        "translator",
        "trusted_prompt",
    ]
    for key in required_keys:
        path = Path(paths[key])
        ok = path.exists() and os.access(path, os.R_OK)
        print(f"MOUNT key={key} ok={ok} path={path}")
        if not ok:
            failures.append(f"missing or unreadable mount: {key}")

    required_pipeline = [
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
        Path("/generation-evidence/codex-trace"),
    ]
    for path in required_pipeline:
        ok = path.exists() and os.access(path, os.R_OK)
        print(f"PIPELINE_RECORD ok={ok} path={path}")
        if not ok:
            failures.append(f"missing or unreadable pipeline-v3 record: {path}")

    hashes = audit["hashes"]
    run_record = json.loads(Path("/run.json").read_text())
    task_record = json.loads(Path("/task.json").read_text())
    generation_result = json.loads(Path("/generation-result.json").read_text())
    invocation_record = json.loads(
        Path("/generation-evidence/invocation.json").read_text()
    )
    metrics_record = json.loads(
        Path("/generation-evidence/metrics.json").read_text()
    )
    runtime_metrics_record = json.loads(
        Path("/generation-evidence/runtime-metrics.json").read_text()
    )
    usage_record = json.loads(
        Path("/generation-evidence/usage.json").read_text()
    )
    task_core_keys = (
        "condition",
        "current_stage",
        "inputs",
        "problem_id",
        "schema_version",
    )
    consistency = {
        "audit_manifest_matches_task_core": all(
            audit["manifest"][key] == task_record[key] for key in task_core_keys
        ),
        "problem_id_consistent": (
            audit["problem_id"]
            == task_record["problem_id"]
            == "73-smallest-change"
        ),
        "condition_consistent": (
            audit["condition"]
            == run_record["condition"]["name"]
            == task_record["condition"]["name"]
            == "kit-semantics"
        ),
        "run_id_consistent": audit["run_id"] == run_record["run_id"],
        "generation_session_consistent": (
            generation_result["session_id"] == invocation_record["session_id"]
        ),
        "generation_output_manifest_consistent": (
            generation_result["outputs"] == invocation_record["outputs"]
        ),
        "metrics_consistent": (
            invocation_record["exit_code"]
            == metrics_record["exit_code"]
            == runtime_metrics_record["final_exit_code"]
            == 0
        ),
        "usage_complete": usage_record["status"] == "COMPLETE",
    }
    for label, ok in consistency.items():
        print(f"RECORD_CONSISTENCY {label}={ok}")
        if not ok:
            failures.append(f"pipeline-v3 record inconsistency: {label}")

    file_hashes = [
        ("audit_campaign_lock", LOCK, hashes["audit_campaign_lock_sha256"]),
        (
            "audit_prompt",
            Path("/audit-prompt.md"),
            lock["audit_prompt_sha256"],
        ),
        ("canonical", Path("/reference/canonical.py"), hashes["canonical_sha256"]),
        ("trusted_prompt", Path("/reference/prompt.py"), hashes["trusted_prompt_sha256"]),
        ("trusted_translator", Path("/reference/py2mpy.py"), hashes["trusted_translator_sha256"]),
        ("candidate_prompt", Path("/candidate/prompt.py"), hashes["candidate_prompt_sha256"]),
        ("candidate_translator", Path("/candidate/py2mpy.py"), hashes["candidate_translator_sha256"]),
        ("run_manifest", Path("/run.json"), hashes["run_manifest_sha256"]),
        ("task_manifest", Path("/task.json"), hashes["task_manifest_sha256"]),
        ("stage1_result", Path("/generation-result.json"), hashes["stage1_result_sha256"]),
        (
            "stage1_invocation",
            Path("/generation-evidence/invocation.json"),
            hashes["stage1_invocation_sha256"],
        ),
        (
            "generation_metrics",
            Path("/generation-evidence/metrics.json"),
            hashes["generation_metrics_sha256"],
        ),
        (
            "generation_runtime_metrics",
            Path("/generation-evidence/runtime-metrics.json"),
            hashes["generation_runtime_metrics_sha256"],
        ),
        (
            "generation_usage",
            Path("/generation-evidence/usage.json"),
            hashes["generation_usage_sha256"],
        ),
        (
            "generation_last",
            Path("/generation-evidence/codex-last.txt"),
            hashes["generation_codex_last_sha256"],
        ),
        (
            "generation_output",
            Path("/generation-evidence/codex-output.log"),
            hashes["generation_codex_output_sha256"],
        ),
        (
            "generation_prompt",
            Path("/generation-evidence/prompt.txt"),
            hashes["generation_prompt_sha256"],
        ),
    ]
    for label, path, expected in file_hashes:
        check_hash(label, path, expected, failures)

    result = json.loads(Path("/generation-result.json").read_text())
    recorded_outputs = result["outputs"]["evidence"]
    for relative, expected in sorted(recorded_outputs.items()):
        if relative == "codex-trace/2026/07/29/rollout-2026-07-29T10-08-58-019fae6b-f480-7332-a3c8-fee3e86d331b.jsonl":
            path = Path("/generation-evidence") / relative
        else:
            path = Path("/generation-evidence") / relative
        check_hash(f"generation-result:{relative}", path, expected, failures)

    candidate_prompt_equal = Path("/candidate/prompt.py").read_bytes() == Path(
        "/reference/prompt.py"
    ).read_bytes()
    candidate_translator_equal = Path("/candidate/py2mpy.py").read_bytes() == Path(
        "/reference/py2mpy.py"
    ).read_bytes()
    print(f"candidate_prompt_byte_equal={candidate_prompt_equal}")
    print(f"candidate_translator_byte_equal={candidate_translator_equal}")
    if not candidate_prompt_equal:
        failures.append("candidate prompt differs from trusted prompt")
    if not candidate_translator_equal:
        failures.append("candidate translator differs from trusted translator")

    required_candidate = [
        "solution.py",
        "solution.mpy",
        "verification.k",
        "verification-base.k",
        "spec.k",
        "prove.sh",
        "PROOF.md",
    ]
    for relative in required_candidate:
        path = Path("/candidate") / relative
        ok = path.is_file() and not path.is_symlink() and os.access(path, os.R_OK)
        print(f"CANDIDATE_ARTIFACT ok={ok} path={path}")
        if not ok:
            failures.append(f"missing, unreadable, or linked candidate artifact: {path}")

    trusted_semantics = Path("/reference/reference-semantics")
    candidate_semantics = Path("/candidate/reference-semantics")
    trusted_manifest = entry_manifest(trusted_semantics)
    candidate_manifest = entry_manifest(candidate_semantics)
    semantics_equal = candidate_manifest == trusted_manifest
    no_semantics_symlinks = not any(
        kind == "symlink"
        for _, kind, _ in trusted_manifest + candidate_manifest
    )
    print(f"semantics_entry_count={len(trusted_manifest)}")
    print(f"semantics_recursive_manifest_equal={semantics_equal}")
    print(f"semantics_no_symlinks={no_semantics_symlinks}")
    print(
        "trusted_semantics_independent_manifest_sha256="
        f"{manifest_sha256(trusted_manifest)}"
    )
    print(
        "candidate_semantics_independent_manifest_sha256="
        f"{manifest_sha256(candidate_manifest)}"
    )
    print(
        "launcher_recorded_trusted_semantics_sha256="
        f"{hashes['trusted_reference_semantics_sha256']}"
    )
    print(
        "launcher_recorded_candidate_semantics_sha256="
        f"{hashes['candidate_reference_semantics_sha256']}"
    )
    if not semantics_equal:
        failures.append("candidate supplied semantics tree differs from trusted tree")
    if not no_semantics_symlinks:
        failures.append("symlink in supplied semantics tree")

    trace_files = sorted(Path("/generation-evidence/codex-trace").rglob("*"))
    trace_files = [path for path in trace_files if path.is_file()]
    print(f"trace_file_count={len(trace_files)}")
    invalid_json_lines = 0
    trace_lines = 0
    last_type = None
    last_payload_type = None
    for path in trace_files:
        with path.open(encoding="utf-8") as stream:
            for line in stream:
                trace_lines += 1
                try:
                    record = json.loads(line)
                except json.JSONDecodeError:
                    invalid_json_lines += 1
                    continue
                last_type = record.get("type")
                payload = record.get("payload")
                last_payload_type = (
                    payload.get("type") if isinstance(payload, dict) else None
                )
    print(f"trace_lines={trace_lines}")
    print(f"trace_invalid_json_lines={invalid_json_lines}")
    print(f"trace_last_type={last_type}")
    print(f"trace_last_payload_type={last_payload_type}")
    if invalid_json_lines:
        failures.append("invalid JSONL record in trace")

    trace_manifest = entry_manifest(Path("/generation-evidence/codex-trace"))
    candidate_tree_manifest = entry_manifest(Path("/candidate"))
    print(
        "trace_independent_manifest_sha256="
        f"{manifest_sha256(trace_manifest)}"
    )
    print(
        "candidate_tree_independent_manifest_sha256="
        f"{manifest_sha256(candidate_tree_manifest)}"
    )
    print(
        "launcher_recorded_trace_tree_sha256="
        f"{hashes['generation_codex_trace_sha256']}"
    )
    print(
        "launcher_recorded_candidate_tree_sha256="
        f"{hashes['candidate_tree_sha256']}"
    )
    candidate_tree_symlinks = [
        relative
        for relative, kind, _ in candidate_tree_manifest
        if kind == "symlink"
    ]
    print(f"candidate_tree_symlink_count={len(candidate_tree_symlinks)}")
    if candidate_tree_symlinks:
        failures.append(
            "candidate tree contains symlinks: " + repr(candidate_tree_symlinks)
        )

    print(f"FAILURE_COUNT={len(failures)}")
    for failure in failures:
        print(f"FAILURE {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
