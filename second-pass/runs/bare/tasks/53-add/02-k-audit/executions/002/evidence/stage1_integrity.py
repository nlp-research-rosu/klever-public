#!/usr/bin/env python3
"""Independent read-only checks of the mounted audit records and inputs."""

from __future__ import annotations

import collections
import hashlib
import json
import os
from pathlib import Path
import stat
import sys


AUDIT = Path("/audit-input.json")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def pipeline_tree_hash(root: Path) -> str:
    """Reimplementation of the length-prefixed launcher tree digest."""
    if not root.is_dir() or root.is_symlink():
        raise AssertionError(f"not a real directory: {root}")
    entries: list[tuple[str, str, Path]] = []
    pending = [root]
    while pending:
        directory = pending.pop()
        for entry in os.scandir(directory):
            mode = entry.stat(follow_symlinks=False).st_mode
            path = Path(entry.path)
            relative = path.relative_to(root).as_posix()
            if stat.S_ISDIR(mode):
                entries.append((relative, "directory", path))
                pending.append(path)
            elif stat.S_ISREG(mode):
                entries.append((relative, "file", path))
            else:
                raise AssertionError(f"linked or unsupported entry: {path}")
    digest = hashlib.sha256()
    for relative, kind, path in sorted(entries):
        encoded = relative.encode()
        digest.update(len(encoded).to_bytes(4, "big"))
        digest.update(encoded)
        digest.update(kind.encode() + b"\0")
        if kind == "file":
            data = path.read_bytes()
            digest.update(len(data).to_bytes(8, "big"))
            digest.update(data)
    return digest.hexdigest()


def require_regular(path: Path) -> None:
    mode = path.lstat().st_mode
    if not stat.S_ISREG(mode):
        raise AssertionError(f"required record is not a regular file: {path}")


def main() -> int:
    audit = json.loads(AUDIT.read_text())
    assert audit["record_layout"] == "legacy-selected-stage1"
    assert audit["semantics_mode"] == "GENERATED_SEMANTICS"
    lock_path = Path(audit["container_paths"]["audit_campaign_lock"])
    lock = json.loads(lock_path.read_text())
    assert audit["audit_campaign"] == lock

    required = {
        "audit_input": AUDIT,
        "campaign_lock": lock_path,
        "run": Path(audit["container_paths"]["run_manifest"]),
        "task": Path(audit["container_paths"]["task_manifest"]),
        "generation_result": Path(audit["container_paths"]["stage1_result"]),
        "invocation": Path(audit["container_paths"]["generation_manifest"]),
        "metrics": Path(audit["container_paths"]["generation_metrics"]),
        "usage": Path("/generation-evidence/usage.json"),
        "codex_last": Path(audit["container_paths"]["generation_last"]),
        "codex_output": Path(audit["container_paths"]["generation_output"]),
        "generation_prompt": Path("/generation-evidence/prompt.txt"),
        "canonical": Path(audit["container_paths"]["canonical"]),
        "trusted_prompt": Path(audit["container_paths"]["trusted_prompt"]),
        "trusted_translator": Path(audit["container_paths"]["translator"]),
        "candidate_prompt": Path("/candidate/prompt.py"),
        "candidate_translator": Path("/candidate/py2mpy.py"),
    }
    for path in required.values():
        require_regular(path)

    expected_hashes = {
        "campaign_lock": "audit_campaign_lock_sha256",
        "run": "run_manifest_sha256",
        "task": "task_manifest_sha256",
        "generation_result": "stage1_result_sha256",
        "invocation": "stage1_invocation_sha256",
        "metrics": "generation_metrics_sha256",
        "usage": "generation_usage_sha256",
        "codex_last": "generation_codex_last_sha256",
        "codex_output": "generation_codex_output_sha256",
        "generation_prompt": "generation_prompt_sha256",
        "canonical": "canonical_sha256",
        "trusted_prompt": "trusted_prompt_sha256",
        "trusted_translator": "trusted_translator_sha256",
        "candidate_prompt": "candidate_prompt_sha256",
        "candidate_translator": "candidate_translator_sha256",
    }
    for label, hash_key in expected_hashes.items():
        actual = sha256_file(required[label])
        expected = audit["hashes"][hash_key]
        print(f"{label}: {actual} expected={expected} match={actual == expected}")
        assert actual == expected

    assert required["candidate_prompt"].read_bytes() == required["trusted_prompt"].read_bytes()
    assert required["candidate_translator"].read_bytes() == required["trusted_translator"].read_bytes()
    assert not Path("/reference/reference-semantics").exists()
    assert not Path("/candidate/reference-semantics").exists()

    trace_root = Path(audit["container_paths"]["generation_trace"])
    if not trace_root.is_dir() or trace_root.is_symlink():
        raise AssertionError("trace root is not a real directory")
    trace_files = sorted(trace_root.rglob("*.jsonl"))
    assert len(trace_files) == 1
    invocation = json.loads(required["invocation"].read_text())
    result = json.loads(required["generation_result"].read_text())
    generation_root = Path(audit["container_paths"]["generation_root"])
    for relative_name, expected in sorted(result["outputs"]["evidence"].items()):
        evidence_path = generation_root / relative_name
        require_regular(evidence_path)
        actual = sha256_file(evidence_path)
        invocation_expected = invocation["outputs"]["evidence"][relative_name]
        print(
            f"declared_evidence[{relative_name}]={actual} "
            f"result_match={actual == expected} "
            f"invocation_match={actual == invocation_expected}"
        )
        assert actual == expected == invocation_expected
        if evidence_path.suffix == ".json":
            record = json.loads(evidence_path.read_text())
            assert isinstance(record, dict)
            print(
                f"json_record[{relative_name}]_keys="
                f"{sorted(record.keys())}"
            )
    relative = trace_files[0].relative_to(Path("/generation-evidence")).as_posix()
    expected_trace_file = result["outputs"]["evidence"][relative]
    actual_trace_file = sha256_file(trace_files[0])
    print(
        f"trace_file: {actual_trace_file} expected={expected_trace_file} "
        f"match={actual_trace_file == expected_trace_file}"
    )
    assert actual_trace_file == expected_trace_file
    assert invocation["outputs"]["evidence"][relative] == actual_trace_file

    counts: collections.Counter[str] = collections.Counter()
    payload_counts: collections.Counter[str] = collections.Counter()
    line_count = 0
    for line_count, line in enumerate(trace_files[0].open(), 1):
        event = json.loads(line)
        counts[str(event.get("type"))] += 1
        payload = event.get("payload")
        if isinstance(payload, dict):
            payload_counts[str(payload.get("type"))] += 1
    usage = json.loads(required["usage"].read_text())
    assert line_count == 180
    assert usage["selected_event"]["line_number"] <= line_count
    print(f"trace_valid_jsonl_lines={line_count}")
    print(f"trace_event_counts={dict(counts)}")
    print(f"trace_payload_counts={dict(payload_counts)}")

    candidate_hash = pipeline_tree_hash(Path("/candidate"))
    trace_hash = pipeline_tree_hash(trace_root)
    print(f"candidate_pipeline_tree_hash={candidate_hash}")
    print(
        "candidate_manifest_workspace_hash="
        f"{result['outputs']['workspace_sha256']} "
        f"match={candidate_hash == result['outputs']['workspace_sha256']}"
    )
    print(f"trace_pipeline_tree_hash={trace_hash}")
    print(
        f"trace_usage_source_hash={usage['source_trace_sha256']} "
        f"match={trace_hash == usage['source_trace_sha256']}"
    )
    assert candidate_hash == result["outputs"]["workspace_sha256"]
    assert candidate_hash == invocation["retained_workspace_sha256"]
    assert trace_hash == usage["source_trace_sha256"]

    candidate_files = sorted(
        p.relative_to("/candidate").as_posix()
        for p in Path("/candidate").rglob("*")
        if p.is_file()
    )
    print(f"candidate_regular_files={candidate_files}")
    for relative_name in candidate_files:
        candidate_path = Path("/candidate") / relative_name
        require_regular(candidate_path)
        print(
            f"candidate_file[{relative_name}]_sha256="
            f"{sha256_file(candidate_path)}"
        )
    print("campaign_match=true")
    print("prompt_match=true")
    print("translator_match=true")
    print("generated_semantics_mode_absence_checks=true")
    print("STAGE1_INTEGRITY_OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
