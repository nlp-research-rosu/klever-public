#!/usr/bin/env python3
"""Independently validate mounted provenance records and their declared hashes."""

from __future__ import annotations

import hashlib
import json
import os
import stat
import sys
from pathlib import Path

sys.path.insert(0, "/opt/humaneval/tools")
import pipeline_contract  # type: ignore  # launcher-adjacent hash implementation


AUDIT_INPUT = Path("/audit-input.json")


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require_regular(path: Path) -> None:
    mode = path.lstat().st_mode
    assert stat.S_ISREG(mode), f"not a real regular file: {path}"


def main() -> int:
    document = json.loads(AUDIT_INPUT.read_text())
    paths = document["container_paths"]
    hashes = document["hashes"]

    required = [
        Path("/run.json"),
        Path("/task.json"),
        Path("/generation-result.json"),
        Path("/generation-evidence/invocation.json"),
        Path("/generation-evidence/metrics.json"),
        Path("/generation-evidence/codex-last.txt"),
        Path("/generation-evidence/codex-output.log"),
        Path("/generation-evidence/prompt.txt"),
    ]
    if Path("/generation-evidence/usage.json").exists():
        required.append(Path("/generation-evidence/usage.json"))
    required.extend(sorted(Path("/generation-evidence/codex-trace").rglob("*")))
    for path in required:
        if path.is_dir():
            assert not path.is_symlink(), f"symlinked directory: {path}"
        else:
            require_regular(path)

    lock = json.loads(Path(paths["audit_campaign_lock"]).read_text())
    print("campaign_block_equals_lock:", document["audit_campaign"] == lock)
    print(
        "campaign_lock_sha256:",
        sha256_file(Path(paths["audit_campaign_lock"])),
        "expected:",
        hashes["audit_campaign_lock_sha256"],
    )

    file_checks = {
        "candidate_prompt_sha256": Path("/candidate/prompt.py"),
        "candidate_translator_sha256": Path("/candidate/py2mpy.py"),
        "canonical_sha256": Path(paths["canonical"]),
        "trusted_prompt_sha256": Path(paths["trusted_prompt"]),
        "trusted_translator_sha256": Path(paths["translator"]),
        "run_manifest_sha256": Path(paths["run_manifest"]),
        "task_manifest_sha256": Path(paths["task_manifest"]),
        "stage1_result_sha256": Path(paths["stage1_result"]),
        "stage1_invocation_sha256": Path(paths["generation_manifest"]),
        "generation_metrics_sha256": Path(paths["generation_metrics"]),
        "generation_codex_last_sha256": Path(paths["generation_last"]),
        "generation_codex_output_sha256": Path(paths["generation_output"]),
        "generation_prompt_sha256": Path("/generation-evidence/prompt.txt"),
        "generation_usage_sha256": Path("/generation-evidence/usage.json"),
    }
    all_match = True
    for field, path in file_checks.items():
        require_regular(path)
        actual = sha256_file(path)
        expected = hashes[field]
        match = actual == expected
        all_match &= match
        print(f"{field}: match={match} actual={actual} expected={expected}")

    trace_manifest = json.loads(Path("/generation-result.json").read_text())
    trace_outputs = trace_manifest["outputs"]["evidence"]
    for relative, expected in sorted(trace_outputs.items()):
        path = Path("/generation-evidence") / relative
        require_regular(path)
        actual = sha256_file(path)
        match = actual == expected
        all_match &= match
        print(f"generation-result {relative}: match={match} actual={actual}")

    prompt_equal = Path("/candidate/prompt.py").read_bytes() == Path(
        paths["trusted_prompt"]
    ).read_bytes()
    translator_equal = Path("/candidate/py2mpy.py").read_bytes() == Path(
        paths["translator"]
    ).read_bytes()
    print("candidate_prompt_byte_equal:", prompt_equal)
    print("candidate_translator_byte_equal:", translator_equal)
    print("trusted_reference_semantics_absent:", not Path("/reference/reference-semantics").exists())
    print("candidate_reference_semantics_absent:", not Path("/candidate/reference-semantics").exists())
    print("candidate_symlinks:", list(Path("/candidate").rglob("*")) and [
        str(p) for p in Path("/candidate").rglob("*") if p.is_symlink()
    ])
    print("generation_symlinks:", [
        str(p) for p in Path("/generation-evidence").rglob("*") if p.is_symlink()
    ])

    candidate_tree = pipeline_contract.sha256_tree(Path("/candidate"))
    trace_tree = pipeline_contract.sha256_tree(Path(paths["generation_trace"]))
    invocation = json.loads(Path(paths["generation_manifest"]).read_text())
    usage = json.loads(Path("/generation-evidence/usage.json").read_text())
    print("candidate_pipeline_tree_sha256:", candidate_tree)
    print("generation_manifest_workspace_sha256:", invocation["outputs"]["workspace_sha256"])
    print("audit_input_candidate_tree_sha256:", hashes["candidate_tree_sha256"])
    print("trace_pipeline_tree_sha256:", trace_tree)
    print("usage_source_trace_sha256:", usage["source_trace_sha256"])
    print("audit_input_trace_tree_sha256:", hashes["generation_codex_trace_sha256"])

    task_manifest = json.loads(Path("/task.json").read_text())
    embedded_manifest = document["manifest"]
    manifest_match = all(
        task_manifest[key] == embedded_manifest[key]
        for key in (
            "schema_version",
            "condition",
            "current_stage",
            "input_provenance",
            "inputs",
            "problem_id",
        )
    )
    print("task_manifest_core_equals_embedded_manifest:", manifest_match)
    print(
        "embedded_manifest_launcher_annotation:",
        {"config": embedded_manifest.get("config")},
    )
    all_match &= (
        document["audit_campaign"] == lock
        and prompt_equal
        and translator_equal
        and manifest_match
        and candidate_tree == invocation["outputs"]["workspace_sha256"]
        and trace_tree == usage["source_trace_sha256"]
        and not Path("/reference/reference-semantics").exists()
        and not Path("/candidate/reference-semantics").exists()
    )
    print("ALL_REQUIRED_PROVENANCE_CHECKS_PASS:", all_match)
    return 0 if all_match else 1


if __name__ == "__main__":
    raise SystemExit(main())
