#!/usr/bin/env python3
"""Independently inspect launcher records and mounted input integrity."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import stat


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require_real_file(path: Path) -> None:
    mode = path.lstat().st_mode
    assert stat.S_ISREG(mode), f"not a real regular file: {path}"


def require_real_tree(path: Path) -> None:
    assert stat.S_ISDIR(path.lstat().st_mode), f"not a real directory: {path}"
    for root, dirs, files in os.walk(path, followlinks=False):
        for name in dirs:
            item = Path(root, name)
            assert stat.S_ISDIR(item.lstat().st_mode), f"linked/non-dir entry: {item}"
        for name in files:
            item = Path(root, name)
            assert stat.S_ISREG(item.lstat().st_mode), f"linked/non-file entry: {item}"


def tree_manifest(path: Path) -> list[tuple[str, str]]:
    return [
        (item.relative_to(path).as_posix(), sha256(item))
        for item in sorted(path.rglob("*"))
        if item.is_file() and not item.is_symlink()
    ]


def main() -> int:
    audit_input_path = Path("/audit-input.json")
    lock_path = Path("/audit-campaign-lock.json")
    require_real_file(audit_input_path)
    require_real_file(lock_path)
    audit_input = json.loads(audit_input_path.read_text())
    lock = json.loads(lock_path.read_text())
    assert audit_input["record_layout"] == "legacy-selected-stage1"
    assert audit_input["semantics_mode"] == "SUPPLIED_SEMANTICS"
    assert audit_input["audit_campaign"] == lock
    assert sha256(lock_path) == audit_input["hashes"]["audit_campaign_lock_sha256"]
    print("campaign_block_equal=true")
    print(f"audit_campaign_lock_sha256={sha256(lock_path)}")

    required_files = [
        Path("/run.json"),
        Path("/task.json"),
        Path("/generation-result.json"),
        Path("/generation-evidence/invocation.json"),
        Path("/generation-evidence/metrics.json"),
        Path("/generation-evidence/codex-last.txt"),
        Path("/generation-evidence/codex-output.log"),
        Path("/generation-evidence/prompt.txt"),
    ]
    usage = Path("/generation-evidence/usage.json")
    if usage.exists():
        required_files.append(usage)
    for path in required_files:
        require_real_file(path)
        print(f"real_file {path} sha256={sha256(path)}")
    for path in (
        Path("/candidate"),
        Path("/generation-evidence"),
        Path("/generation-evidence/codex-trace"),
        Path("/reference/reference-semantics"),
    ):
        require_real_tree(path)
        print(f"real_tree {path}")

    expected_file_hashes = {
        "/reference/canonical.py": "canonical_sha256",
        "/reference/prompt.py": "trusted_prompt_sha256",
        "/reference/py2mpy.py": "trusted_translator_sha256",
        "/candidate/prompt.py": "candidate_prompt_sha256",
        "/candidate/py2mpy.py": "candidate_translator_sha256",
        "/run.json": "run_manifest_sha256",
        "/task.json": "task_manifest_sha256",
        "/generation-result.json": "stage1_result_sha256",
        "/generation-evidence/invocation.json": "stage1_invocation_sha256",
        "/generation-evidence/metrics.json": "generation_metrics_sha256",
        "/generation-evidence/codex-last.txt": "generation_codex_last_sha256",
        "/generation-evidence/codex-output.log": "generation_codex_output_sha256",
        "/generation-evidence/prompt.txt": "generation_prompt_sha256",
        "/generation-evidence/usage.json": "generation_usage_sha256",
    }
    for raw_path, key in expected_file_hashes.items():
        path = Path(raw_path)
        observed = sha256(path)
        expected = audit_input["hashes"][key]
        assert observed == expected, f"hash mismatch {path}: {observed} != {expected}"
        print(f"recorded_hash_match {path} {observed}")

    pairs = [
        (Path("/candidate/prompt.py"), Path("/reference/prompt.py"), "prompt"),
        (Path("/candidate/py2mpy.py"), Path("/reference/py2mpy.py"), "translator"),
    ]
    for left, right, label in pairs:
        assert left.read_bytes() == right.read_bytes()
        print(f"byte_identity {label}=true")

    candidate_manifest = tree_manifest(Path("/candidate/reference-semantics"))
    trusted_manifest = tree_manifest(Path("/reference/reference-semantics"))
    assert candidate_manifest == trusted_manifest
    print(f"semantics_recursive_identity=true entries={len(trusted_manifest)}")
    for relative, digest in trusted_manifest:
        print(f"semantics_file {digest} {relative}")

    result = json.loads(Path("/generation-result.json").read_text())
    for relative, expected in result["outputs"]["evidence"].items():
        path = Path("/generation-evidence", relative)
        require_real_file(path)
        assert sha256(path) == expected
        print(f"generation_result_hash_match {relative} {expected}")

    trace_files = [
        item
        for item in Path("/generation-evidence/codex-trace").rglob("*")
        if item.is_file()
    ]
    assert trace_files
    for path in trace_files:
        lines = 0
        with path.open() as handle:
            for lines, line in enumerate(handle, 1):
                json.loads(line)
        print(f"trace_jsonl_valid {path} lines={lines} sha256={sha256(path)}")
    print("INTEGRITY_OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
