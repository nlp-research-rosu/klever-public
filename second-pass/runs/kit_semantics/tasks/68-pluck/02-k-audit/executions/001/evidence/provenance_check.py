#!/usr/bin/env python3
"""Independent pipeline-v3 provenance and mount-integrity checks."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_tree(root: Path) -> str:
    """Pipeline-v3 tree digest, reconstructed independently from mounted bytes."""
    if not stat.S_ISDIR(root.lstat().st_mode):
        raise AssertionError(f"not a real directory: {root}")
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
                raise AssertionError(f"linked or unsupported tree entry: {path}")
    digest = hashlib.sha256()
    for relative, kind, path in sorted(entries):
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


def require_regular(path: Path) -> None:
    mode = path.lstat().st_mode
    if not stat.S_ISREG(mode):
        raise AssertionError(f"required regular file is absent/mistyped/symlinked: {path}")


def main() -> None:
    require_regular(AUDIT_INPUT)
    audit_input = json.loads(AUDIT_INPUT.read_text())
    assert audit_input["record_layout"] == "pipeline-v3"
    assert audit_input["semantics_mode"] == "SUPPLIED_SEMANTICS"
    assert audit_input["problem_id"] == "68-pluck"

    paths = audit_input["container_paths"]
    required = {
        "audit_campaign_lock": Path(paths["audit_campaign_lock"]),
        "run_manifest": Path(paths["run_manifest"]),
        "task_manifest": Path(paths["task_manifest"]),
        "stage1_result": Path(paths["stage1_result"]),
        "generation_manifest": Path(paths["generation_manifest"]),
        "generation_metrics": Path(paths["generation_metrics"]),
        "generation_last": Path(paths["generation_last"]),
        "generation_output": Path(paths["generation_output"]),
        "trusted_prompt": Path(paths["trusted_prompt"]),
        "translator": Path(paths["translator"]),
        "canonical": Path(paths["canonical"]),
        "generation_prompt": Path(paths["generation_root"]) / "prompt.txt",
        "runtime_metrics": Path(paths["generation_root"]) / "runtime-metrics.json",
        "usage": Path(paths["generation_root"]) / "usage.json",
    }
    for path in required.values():
        require_regular(path)

    trace_root = Path(paths["generation_trace"])
    candidate_root = Path(paths["candidate"])
    trusted_semantics = Path("/reference/reference-semantics")
    candidate_semantics = candidate_root / "reference-semantics"
    for directory in (trace_root, candidate_root, trusted_semantics, candidate_semantics):
        if not stat.S_ISDIR(directory.lstat().st_mode):
            raise AssertionError(f"required real directory is absent/mistyped: {directory}")
        sha256_tree(directory)  # also rejects every symlink/special entry recursively

    lock = json.loads(required["audit_campaign_lock"].read_text())
    assert lock == audit_input["audit_campaign"]
    assert sha256_file(required["audit_campaign_lock"]) == audit_input["hashes"][
        "audit_campaign_lock_sha256"
    ]

    file_hash_checks = {
        required["run_manifest"]: "run_manifest_sha256",
        required["task_manifest"]: "task_manifest_sha256",
        required["stage1_result"]: "stage1_result_sha256",
        required["generation_manifest"]: "stage1_invocation_sha256",
        required["generation_metrics"]: "generation_metrics_sha256",
        required["runtime_metrics"]: "generation_runtime_metrics_sha256",
        required["usage"]: "generation_usage_sha256",
        required["generation_last"]: "generation_codex_last_sha256",
        required["generation_output"]: "generation_codex_output_sha256",
        required["generation_prompt"]: "generation_prompt_sha256",
        required["canonical"]: "canonical_sha256",
        required["trusted_prompt"]: "trusted_prompt_sha256",
        required["translator"]: "trusted_translator_sha256",
        candidate_root / "prompt.py": "candidate_prompt_sha256",
        candidate_root / "py2mpy.py": "candidate_translator_sha256",
    }
    for path, key in file_hash_checks.items():
        actual = sha256_file(path)
        expected = audit_input["hashes"][key]
        assert actual == expected, (path, actual, expected)

    generation_result = json.loads(required["stage1_result"].read_text())
    output_hashes = generation_result["outputs"]["evidence"]
    generated_files = {
        "codex-last.txt": required["generation_last"],
        "codex-output.log": required["generation_output"],
        "prompt.txt": required["generation_prompt"],
        "runtime-metrics.json": required["runtime_metrics"],
        "usage.json": required["usage"],
    }
    for relative, path in generated_files.items():
        assert sha256_file(path) == output_hashes[relative]
    trace_files = sorted(trace_root.rglob("*.jsonl"))
    assert len(trace_files) == 1
    trace_relative = trace_files[0].relative_to(trace_root).as_posix()
    assert sha256_file(trace_files[0]) == output_hashes[f"codex-trace/{trace_relative}"]

    # Parse every structured trace line, rather than accepting a trailing summary.
    event_counts: dict[str, int] = {}
    trace_lines = 0
    for trace_file in trace_files:
        with trace_file.open() as stream:
            for line_number, line in enumerate(stream, 1):
                item = json.loads(line)
                assert "type" in item and "payload" in item, (trace_file, line_number)
                event_counts[item["type"]] = event_counts.get(item["type"], 0) + 1
                trace_lines += 1

    assert sha256_tree(candidate_root) == generation_result["outputs"]["workspace_sha256"]
    assert sha256_tree(candidate_semantics) == sha256_tree(trusted_semantics)
    assert (candidate_root / "prompt.py").read_bytes() == required["trusted_prompt"].read_bytes()
    assert (candidate_root / "py2mpy.py").read_bytes() == required["translator"].read_bytes()

    run = json.loads(required["run_manifest"].read_text())
    task = json.loads(required["task_manifest"].read_text())
    invocation = json.loads(required["generation_manifest"].read_text())
    metrics = json.loads(required["generation_metrics"].read_text())
    runtime_metrics = json.loads(required["runtime_metrics"].read_text())
    usage = json.loads(required["usage"].read_text())
    assert run["run_id"] == audit_input["run_id"]
    manifest_projection = dict(audit_input["manifest"])
    # audit-input adds the launcher-selected config beside the verbatim task fields.
    assert manifest_projection.pop("config") == audit_input["config"]
    assert task == manifest_projection
    assert task["problem_id"] == "68-pluck"
    assert invocation["status"] == metrics["status"] == generation_result["status"] == "SUCCEEDED"
    assert invocation["exit_code"] == metrics["exit_code"] == 0
    assert runtime_metrics["final_exit_code"] == 0
    assert usage["status"] == "COMPLETE"

    print("record_layout=pipeline-v3")
    print("semantics_mode=SUPPLIED_SEMANTICS")
    print("required_regular_files=PASS")
    print("campaign_lock_block_and_hash=PASS")
    print(f"generation_trace_json_lines={trace_lines}")
    print(f"generation_trace_event_counts={event_counts}")
    print(f"candidate_pipeline_tree_sha256={sha256_tree(candidate_root)}")
    print(f"trace_pipeline_tree_sha256={sha256_tree(trace_root)}")
    print(f"semantics_pipeline_tree_sha256={sha256_tree(trusted_semantics)}")
    print("recorded_file_hashes=PASS")
    print("generation_result_output_hashes=PASS")
    print("prompt_translator_semantics_integrity=PASS")


if __name__ == "__main__":
    main()
