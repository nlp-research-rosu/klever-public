#!/usr/bin/env python3
"""Independent launcher/provenance and supplied-semantics integrity checks."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from pathlib import Path

from pipeline_contract import sha256_tree


AUDIT_INPUT = Path("/audit-input.json")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require_regular(path: Path) -> None:
    mode = path.lstat().st_mode
    assert stat.S_ISREG(mode), f"not a real regular file: {path}"


def require_directory(path: Path) -> None:
    mode = path.lstat().st_mode
    assert stat.S_ISDIR(mode), f"not a real directory: {path}"


def tree_manifest(root: Path) -> dict[str, tuple[str, str | None]]:
    result: dict[str, tuple[str, str | None]] = {}
    pending = [root]
    while pending:
        directory = pending.pop()
        for entry in os.scandir(directory):
            path = Path(entry.path)
            mode = entry.stat(follow_symlinks=False).st_mode
            relative = path.relative_to(root).as_posix()
            if stat.S_ISDIR(mode):
                result[relative] = ("directory", None)
                pending.append(path)
            elif stat.S_ISREG(mode):
                result[relative] = ("file", sha256(path))
            else:
                raise AssertionError(f"linked or unsupported tree entry: {path}")
    return dict(sorted(result.items()))


def main() -> None:
    audit_input = json.loads(AUDIT_INPUT.read_text(encoding="utf-8"))
    assert audit_input["record_layout"] == "pipeline-v3"
    assert audit_input["semantics_mode"] == "SUPPLIED_SEMANTICS"

    required_files = [
        AUDIT_INPUT,
        Path("/audit-campaign-lock.json"),
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
    for path in required_files:
        require_regular(path)
    for path in (
        Path("/candidate"),
        Path("/generation-evidence"),
        Path("/generation-evidence/codex-trace"),
        Path("/reference/reference-semantics"),
    ):
        require_directory(path)

    lock = json.loads(Path("/audit-campaign-lock.json").read_text(encoding="utf-8"))
    assert lock == audit_input["audit_campaign"]

    hashes = audit_input["hashes"]
    direct_hashes = {
        "/audit-campaign-lock.json": "audit_campaign_lock_sha256",
        "/run.json": "run_manifest_sha256",
        "/task.json": "task_manifest_sha256",
        "/generation-result.json": "stage1_result_sha256",
        "/generation-evidence/invocation.json": "stage1_invocation_sha256",
        "/generation-evidence/metrics.json": "generation_metrics_sha256",
        "/generation-evidence/runtime-metrics.json":
            "generation_runtime_metrics_sha256",
        "/generation-evidence/usage.json": "generation_usage_sha256",
        "/generation-evidence/codex-last.txt": "generation_codex_last_sha256",
        "/generation-evidence/codex-output.log":
            "generation_codex_output_sha256",
        "/generation-evidence/prompt.txt": "generation_prompt_sha256",
        "/reference/canonical.py": "canonical_sha256",
        "/reference/prompt.py": "trusted_prompt_sha256",
        "/reference/py2mpy.py": "trusted_translator_sha256",
    }
    for name, key in direct_hashes.items():
        actual = sha256(Path(name))
        expected = hashes[key]
        print(f"HASH {name} actual={actual} expected={expected}")
        assert actual == expected

    invocation = json.loads(
        Path("/generation-evidence/invocation.json").read_text(encoding="utf-8")
    )
    generation_result = json.loads(
        Path("/generation-result.json").read_text(encoding="utf-8")
    )
    trace_files = sorted(Path("/generation-evidence/codex-trace").rglob("*.jsonl"))
    assert len(trace_files) == 1
    trace_relative = trace_files[0].relative_to(
        Path("/generation-evidence/codex-trace")
    ).as_posix()
    expected_trace_file_hash = invocation["outputs"]["evidence"][
        f"codex-trace/{trace_relative}"
    ]
    assert sha256(trace_files[0]) == expected_trace_file_hash

    candidate_tree_hash = sha256_tree(Path("/candidate"))
    trace_tree_hash = sha256_tree(Path("/generation-evidence/codex-trace"))
    semantics_tree_hash = sha256_tree(Path("/reference/reference-semantics"))
    print(f"TREE /candidate {candidate_tree_hash}")
    print(f"TREE /generation-evidence/codex-trace {trace_tree_hash}")
    print(f"TREE /reference/reference-semantics {semantics_tree_hash}")
    assert candidate_tree_hash == invocation["outputs"]["workspace_sha256"]
    assert candidate_tree_hash == generation_result["outputs"]["workspace_sha256"]
    usage = json.loads(
        Path("/generation-evidence/usage.json").read_text(encoding="utf-8")
    )
    assert trace_tree_hash == usage["source_trace_sha256"]
    assert (
        semantics_tree_hash
        == hashes["trusted_reference_semantics_manifest_sha256"]
    )

    assert Path("/candidate/prompt.py").read_bytes() == Path(
        "/reference/prompt.py"
    ).read_bytes()
    assert Path("/candidate/py2mpy.py").read_bytes() == Path(
        "/reference/py2mpy.py"
    ).read_bytes()
    trusted_semantics = tree_manifest(Path("/reference/reference-semantics"))
    candidate_semantics = tree_manifest(Path("/candidate/reference-semantics"))
    assert trusted_semantics == candidate_semantics

    # Validate the structured trace by parsing every record.
    trace_records = 0
    for path in trace_files:
        for line_number, line in enumerate(
            path.read_text(encoding="utf-8").splitlines(), 1
        ):
            try:
                json.loads(line)
            except json.JSONDecodeError as error:
                raise AssertionError(f"{path}:{line_number}: {error}") from error
            trace_records += 1

    print(f"TRACE parsed_records={trace_records}")
    print(
        "SUPPLIED_SEMANTICS entries="
        f"{len(trusted_semantics)} candidate_equals_trusted=True"
    )
    print("PIPELINE_V3_INTEGRITY=PASS")


if __name__ == "__main__":
    main()
