#!/usr/bin/env python3
"""Independent, read-only checks for the launcher-owned audit inputs."""

from __future__ import annotations

import collections
import hashlib
import json
import os
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")
CAMPAIGN_LOCK = Path("/audit-campaign-lock.json")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def require_regular(path: Path) -> None:
    if not path.exists():
        raise AssertionError(f"missing: {path}")
    if path.is_symlink():
        raise AssertionError(f"symlink where regular file required: {path}")
    if not path.is_file():
        raise AssertionError(f"not a regular file: {path}")
    if not os.access(path, os.R_OK):
        raise AssertionError(f"unreadable: {path}")


def compare_trees(candidate: Path, trusted: Path) -> int:
    candidate_entries = {
        str(path.relative_to(candidate)): path for path in candidate.rglob("*")
    }
    trusted_entries = {
        str(path.relative_to(trusted)): path for path in trusted.rglob("*")
    }
    if candidate_entries.keys() != trusted_entries.keys():
        raise AssertionError(
            "semantics entry mismatch: "
            f"candidate-only={sorted(candidate_entries.keys() - trusted_entries.keys())}, "
            f"trusted-only={sorted(trusted_entries.keys() - candidate_entries.keys())}"
        )
    files = 0
    for relative in sorted(candidate_entries):
        left = candidate_entries[relative]
        right = trusted_entries[relative]
        if left.is_symlink() or right.is_symlink():
            raise AssertionError(f"symlinked semantics entry: {relative}")
        if left.is_dir() != right.is_dir() or left.is_file() != right.is_file():
            raise AssertionError(f"semantics type mismatch: {relative}")
        if left.is_file():
            files += 1
            if sha256(left) != sha256(right):
                raise AssertionError(f"semantics content mismatch: {relative}")
    return files


def main() -> None:
    print("COMMAND: python3 /audit-output/evidence/integrity_check.py")
    require_regular(AUDIT_INPUT)
    require_regular(CAMPAIGN_LOCK)
    audit = json.loads(AUDIT_INPUT.read_text(encoding="utf-8"))
    campaign = json.loads(CAMPAIGN_LOCK.read_text(encoding="utf-8"))

    assert audit["record_layout"] == "pipeline-v3"
    assert audit["semantics_mode"] == "SUPPLIED_SEMANTICS"
    assert audit["problem_id"] == "84-solve"
    assert campaign == audit["audit_campaign"]
    assert sha256(CAMPAIGN_LOCK) == audit["hashes"]["audit_campaign_lock_sha256"]

    required = [
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
    ]
    for path in required:
        require_regular(path)

    expected_hashes = {
        Path("/run.json"): "run_manifest_sha256",
        Path("/task.json"): "task_manifest_sha256",
        Path("/generation-result.json"): "stage1_result_sha256",
        Path("/generation-evidence/invocation.json"): "stage1_invocation_sha256",
        Path("/generation-evidence/metrics.json"): "generation_metrics_sha256",
        Path("/generation-evidence/runtime-metrics.json"):
            "generation_runtime_metrics_sha256",
        Path("/generation-evidence/usage.json"): "generation_usage_sha256",
        Path("/generation-evidence/codex-last.txt"):
            "generation_codex_last_sha256",
        Path("/generation-evidence/codex-output.log"):
            "generation_codex_output_sha256",
        Path("/generation-evidence/prompt.txt"): "generation_prompt_sha256",
        Path("/reference/canonical.py"): "canonical_sha256",
        Path("/reference/prompt.py"): "trusted_prompt_sha256",
        Path("/reference/py2mpy.py"): "trusted_translator_sha256",
    }
    for path, key in expected_hashes.items():
        actual = sha256(path)
        expected = audit["hashes"][key]
        if actual != expected:
            raise AssertionError(f"hash mismatch for {path}: {actual} != {expected}")

    run = json.loads(Path("/run.json").read_text(encoding="utf-8"))
    task = json.loads(Path("/task.json").read_text(encoding="utf-8"))
    result = json.loads(Path("/generation-result.json").read_text(encoding="utf-8"))
    invocation = json.loads(
        Path("/generation-evidence/invocation.json").read_text(encoding="utf-8")
    )
    metrics = json.loads(
        Path("/generation-evidence/metrics.json").read_text(encoding="utf-8")
    )
    runtime_metrics = json.loads(
        Path("/generation-evidence/runtime-metrics.json").read_text(encoding="utf-8")
    )
    usage = json.loads(
        Path("/generation-evidence/usage.json").read_text(encoding="utf-8")
    )
    assert run["run_id"] == audit["run_id"]
    for key, value in task.items():
        assert audit["manifest"][key] == value
    assert audit["manifest"]["config"] == audit["config"]
    assert task["problem_id"] == "84-solve"
    assert result["status"] == invocation["status"] == metrics["status"] == "SUCCEEDED"
    assert runtime_metrics["final_exit_code"] == 0
    assert usage["status"] == "COMPLETE"

    evidence_hashes = invocation["outputs"]["evidence"]
    assert evidence_hashes == result["outputs"]["evidence"]
    for relative, expected in sorted(evidence_hashes.items()):
        path = Path("/generation-evidence") / relative
        require_regular(path)
        if sha256(path) != expected:
            raise AssertionError(f"generation evidence hash mismatch: {relative}")

    trace_root = Path("/generation-evidence/codex-trace")
    if trace_root.is_symlink() or not trace_root.is_dir():
        raise AssertionError("structured trace root is missing, symlinked, or mistyped")
    trace_files = sorted(trace_root.rglob("*"))
    if not trace_files:
        raise AssertionError("structured trace is empty")
    for path in trace_files:
        if path.is_symlink():
            raise AssertionError(f"symlink in structured trace: {path}")
        if not (path.is_dir() or path.is_file()):
            raise AssertionError(f"mistyped structured trace entry: {path}")

    top_types: collections.Counter[str] = collections.Counter()
    payload_types: collections.Counter[str] = collections.Counter()
    line_count = 0
    jsonl_files = [path for path in trace_files if path.suffix == ".jsonl"]
    for path in jsonl_files:
        require_regular(path)
        with path.open("r", encoding="utf-8") as stream:
            for line_count, line in enumerate(stream, start=1):
                record = json.loads(line)
                top_types[str(record.get("type"))] += 1
                payload = record.get("payload")
                if isinstance(payload, dict) and "type" in payload:
                    payload_types[str(payload["type"])] += 1
    selected = usage["selected_event"]
    selected_path = trace_root / selected["relative_path"]
    require_regular(selected_path)
    selected_lines = selected_path.read_text(encoding="utf-8").splitlines()
    if selected["line_number"] > len(selected_lines):
        raise AssertionError("usage selected_event points past end of trace")
    json.loads(selected_lines[selected["line_number"] - 1])

    output_bytes = Path("/generation-evidence/codex-output.log").read_bytes()
    output_text = output_bytes.decode("utf-8")
    prompt_text = Path("/generation-evidence/prompt.txt").read_text(encoding="utf-8")
    last_text = Path("/generation-evidence/codex-last.txt").read_text(encoding="utf-8")

    candidate_prompt = Path("/candidate/prompt.py")
    candidate_translator = Path("/candidate/py2mpy.py")
    require_regular(candidate_prompt)
    require_regular(candidate_translator)
    assert sha256(candidate_prompt) == sha256(Path("/reference/prompt.py"))
    assert sha256(candidate_translator) == sha256(Path("/reference/py2mpy.py"))

    candidate_required = [
        Path("/candidate/solution.py"),
        Path("/candidate/solution.mpy"),
        Path("/candidate/verification.k"),
        Path("/candidate/spec.k"),
        Path("/candidate/bridge-verification.k"),
        Path("/candidate/bridge-spec.k"),
        Path("/candidate/PROOF.md"),
    ]
    for path in candidate_required:
        require_regular(path)

    semantics_files = compare_trees(
        Path("/candidate/reference-semantics"),
        Path("/reference/reference-semantics"),
    )

    print("record_layout=pipeline-v3")
    print("semantics_mode=SUPPLIED_SEMANTICS")
    print("campaign_lock_exact_match=true")
    print(f"required_regular_files={len(required)}")
    print(f"generation_evidence_hashes_verified={len(evidence_hashes)}")
    print(f"structured_trace_jsonl_files={len(jsonl_files)}")
    print(f"structured_trace_lines={line_count}")
    print(f"structured_trace_top_types={dict(sorted(top_types.items()))}")
    print(f"structured_trace_payload_types={dict(sorted(payload_types.items()))}")
    print(f"codex_output_bytes={len(output_bytes)}")
    print(f"codex_output_lines={len(output_text.splitlines())}")
    print(f"generation_prompt_chars={len(prompt_text)}")
    print(f"generation_last_chars={len(last_text)}")
    print("candidate_prompt_matches_trusted=true")
    print("candidate_translator_matches_trusted=true")
    print(f"candidate_required_proof_files={len(candidate_required)}")
    print(f"supplied_semantics_files_byte_identical={semantics_files}")


if __name__ == "__main__":
    main()
