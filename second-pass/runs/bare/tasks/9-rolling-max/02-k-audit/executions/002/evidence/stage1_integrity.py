#!/usr/bin/env python3
"""Independently validate the mounted legacy-selected-stage1 records."""

from __future__ import annotations

from collections import Counter
import hashlib
import json
import os
from pathlib import Path
import stat
import sys


AUDIT_INPUT = Path("/audit-input.json")
LOCK = Path("/audit-campaign-lock.json")
CANDIDATE = Path("/candidate")
REFERENCE = Path("/reference")
GENERATION = Path("/generation-evidence")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def sha256_tree(root: Path) -> str:
    """Pipeline-v2 tree digest, reconstructed from the public record format."""
    digest = hashlib.sha256()
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
                raise AssertionError(f"linked or unsupported tree entry: {path}")
    for relative, kind, path in sorted(entries):
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


def require_regular(path: Path) -> None:
    mode = path.lstat().st_mode
    assert stat.S_ISREG(mode), f"not a regular file: {path}"
    with path.open("rb") as stream:
        while stream.read(1024 * 1024):
            pass


def main() -> int:
    audit = json.loads(AUDIT_INPUT.read_text(encoding="utf-8"))
    lock = json.loads(LOCK.read_text(encoding="utf-8"))
    assert audit["record_layout"] == "legacy-selected-stage1"
    assert audit["semantics_mode"] == "GENERATED_SEMANTICS"
    assert audit["audit_campaign"] == lock
    assert not (REFERENCE / "reference-semantics").exists()

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
    for path in required:
        require_regular(path)

    expected_hashes = {
        LOCK: audit["hashes"]["audit_campaign_lock_sha256"],
        Path("/reference/canonical.py"): audit["hashes"]["canonical_sha256"],
        Path("/reference/prompt.py"): audit["hashes"]["trusted_prompt_sha256"],
        Path("/reference/py2mpy.py"): audit["hashes"]["trusted_translator_sha256"],
        CANDIDATE / "prompt.py": audit["hashes"]["candidate_prompt_sha256"],
        CANDIDATE / "py2mpy.py": audit["hashes"]["candidate_translator_sha256"],
        Path("/run.json"): audit["hashes"]["run_manifest_sha256"],
        Path("/task.json"): audit["hashes"]["task_manifest_sha256"],
        Path("/generation-result.json"): audit["hashes"]["stage1_result_sha256"],
        GENERATION / "invocation.json": audit["hashes"]["stage1_invocation_sha256"],
        GENERATION / "metrics.json": audit["hashes"]["generation_metrics_sha256"],
        GENERATION / "codex-last.txt": audit["hashes"]["generation_codex_last_sha256"],
        GENERATION / "codex-output.log": audit["hashes"]["generation_codex_output_sha256"],
        GENERATION / "prompt.txt": audit["hashes"]["generation_prompt_sha256"],
        GENERATION / "usage.json": audit["hashes"]["generation_usage_sha256"],
    }
    for path, expected in expected_hashes.items():
        actual = sha256_file(path)
        assert actual == expected, f"hash mismatch: {path}: {actual} != {expected}"

    assert (CANDIDATE / "prompt.py").read_bytes() == (
        REFERENCE / "prompt.py"
    ).read_bytes()
    assert (CANDIDATE / "py2mpy.py").read_bytes() == (
        REFERENCE / "py2mpy.py"
    ).read_bytes()

    invocation = json.loads(
        (GENERATION / "invocation.json").read_text(encoding="utf-8")
    )
    result = json.loads(Path("/generation-result.json").read_text(encoding="utf-8"))
    run_manifest = json.loads(Path("/run.json").read_text(encoding="utf-8"))
    task_manifest = json.loads(Path("/task.json").read_text(encoding="utf-8"))
    metrics = json.loads((GENERATION / "metrics.json").read_text(encoding="utf-8"))
    legacy_metrics = json.loads(
        (GENERATION / "legacy-metrics.json").read_text(encoding="utf-8")
    )
    legacy_run_input = json.loads(
        (GENERATION / "legacy-run-input.json").read_text(encoding="utf-8")
    )
    workspace_digest = sha256_tree(CANDIDATE)
    assert workspace_digest == invocation["retained_workspace_sha256"]
    assert workspace_digest == result["outputs"]["workspace_sha256"]

    trace_files = sorted(
        path for path in (GENERATION / "codex-trace").rglob("*") if path.is_file()
    )
    assert len(trace_files) == 1
    trace_file = trace_files[0]
    trace_relative = trace_file.relative_to(GENERATION).as_posix()
    assert sha256_file(trace_file) == result["outputs"]["evidence"][trace_relative]
    for relative, expected in result["outputs"]["evidence"].items():
        evidence_path = GENERATION / relative
        require_regular(evidence_path)
        assert sha256_file(evidence_path) == expected

    usage = json.loads((GENERATION / "usage.json").read_text(encoding="utf-8"))
    trace_tree_digest = sha256_tree(GENERATION / "codex-trace")
    assert trace_tree_digest == usage["source_trace_sha256"]

    type_counts: Counter[str] = Counter()
    payload_type_counts: Counter[str] = Counter()
    line_count = 0
    with trace_file.open(encoding="utf-8") as stream:
        for line_count, line in enumerate(stream, 1):
            record = json.loads(line)
            type_counts[record["type"]] += 1
            payload = record.get("payload")
            if isinstance(payload, dict) and isinstance(payload.get("type"), str):
                payload_type_counts[payload["type"]] += 1
    assert line_count > 0

    symlinks = []
    for root in [CANDIDATE, REFERENCE, GENERATION]:
        for path in [root, *root.rglob("*")]:
            if path.is_symlink():
                symlinks.append(str(path))
    assert not symlinks, f"symlinks found: {symlinks}"

    print("record_layout: legacy-selected-stage1")
    print("run_id:", run_manifest["run_id"])
    print("task_problem_id:", task_manifest["problem_id"])
    print("task_input_provenance:", task_manifest["input_provenance"])
    print("generation_status:", result["status"])
    print("generation_result_marker_claim:", result["result_marker"])
    print("invocation_exit_code:", invocation["exit_code"])
    print("metrics_status:", metrics["status"])
    print("legacy_metrics_exit_code:", legacy_metrics["exit_code"])
    print("legacy_run_problem_id:", legacy_run_input["problem_id"])
    print("usage_status:", usage["status"])
    print("campaign_lock_object_match: yes")
    print("required_records_regular_and_readable:", len(required))
    print("generated_semantics_boundary_reference_tree_absent: yes")
    print("candidate_prompt_byte_match: yes")
    print("candidate_translator_byte_match: yes")
    print("single_file_hashes_matched:", len(expected_hashes))
    print("candidate_pipeline_tree_sha256:", workspace_digest)
    print("recorded_audit_candidate_tree_sha256:", audit["hashes"]["candidate_tree_sha256"])
    print("candidate_tree_matches_stage1_workspace_record: yes")
    print("trace_file_sha256_matched: yes")
    print("trace_tree_sha256_matched: yes")
    print("trace_jsonl_lines:", line_count)
    print("trace_record_types:", dict(sorted(type_counts.items())))
    print("trace_payload_types:", dict(sorted(payload_type_counts.items())))
    print("symlinks: none")
    return 0


if __name__ == "__main__":
    sys.exit(main())
