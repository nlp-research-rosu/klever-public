#!/usr/bin/env python3
"""Independent mounted-input checks for audit stage 1."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def require_regular(path: Path) -> None:
    assert path.exists(), f"missing: {path}"
    assert not path.is_symlink(), f"symlink forbidden: {path}"
    assert path.is_file(), f"not a regular file: {path}"


audit = json.loads(AUDIT_INPUT.read_text())
assert audit["record_layout"] == "legacy-selected-stage1"
assert audit["semantics_mode"] == "GENERATED_SEMANTICS"

lock_path = Path(audit["container_paths"]["audit_campaign_lock"])
require_regular(lock_path)
lock = json.loads(lock_path.read_text())
assert lock == audit["audit_campaign"]
assert sha256(lock_path) == audit["hashes"]["audit_campaign_lock_sha256"]

required_hashes = {
    Path("/run.json"): "run_manifest_sha256",
    Path("/task.json"): "task_manifest_sha256",
    Path("/generation-result.json"): "stage1_result_sha256",
    Path("/generation-evidence/invocation.json"): "stage1_invocation_sha256",
    Path("/generation-evidence/metrics.json"): "generation_metrics_sha256",
    Path("/generation-evidence/codex-last.txt"): "generation_codex_last_sha256",
    Path("/generation-evidence/codex-output.log"): "generation_codex_output_sha256",
    Path("/generation-evidence/prompt.txt"): "generation_prompt_sha256",
    Path("/generation-evidence/usage.json"): "generation_usage_sha256",
    Path("/reference/canonical.py"): "canonical_sha256",
    Path("/reference/prompt.py"): "trusted_prompt_sha256",
    Path("/reference/py2mpy.py"): "trusted_translator_sha256",
    Path("/candidate/prompt.py"): "candidate_prompt_sha256",
    Path("/candidate/py2mpy.py"): "candidate_translator_sha256",
}

for path, hash_key in required_hashes.items():
    require_regular(path)
    actual = sha256(path)
    expected = audit["hashes"][hash_key]
    assert actual == expected, (path, actual, expected)
    print(f"OK sha256 {path} {actual}")

stage1_result = json.loads(Path("/generation-result.json").read_text())
for relative, expected in stage1_result["outputs"]["evidence"].items():
    path = Path("/generation-evidence") / relative
    require_regular(path)
    actual = sha256(path)
    assert actual == expected, (path, actual, expected)
    print(f"OK stage1 evidence sha256 {path} {actual}")

trace_root = Path(audit["container_paths"]["generation_trace"])
assert trace_root.is_dir() and not trace_root.is_symlink()
trace_files = sorted(trace_root.rglob("*"))
assert trace_files
for path in trace_files:
    assert not path.is_symlink(), f"symlink forbidden: {path}"
for path in (p for p in trace_files if p.is_file()):
    print(f"TRACE sha256 {path} {sha256(path)}")
    with path.open() as stream:
        records = [json.loads(line) for line in stream]
    print(f"TRACE parsed_records {path} {len(records)}")

candidate_root = Path(audit["container_paths"]["candidate"])
assert candidate_root.is_dir() and not candidate_root.is_symlink()
for path in sorted(candidate_root.rglob("*")):
    assert not path.is_symlink(), f"symlink forbidden: {path}"
    if path.is_file():
        print(f"CANDIDATE sha256 {path} {sha256(path)}")

assert Path("/candidate/prompt.py").read_bytes() == Path(
    "/reference/prompt.py"
).read_bytes()
assert Path("/candidate/py2mpy.py").read_bytes() == Path(
    "/reference/py2mpy.py"
).read_bytes()
assert not Path("/reference/reference-semantics").exists()
assert not Path("/candidate/reference-semantics").exists()
assert sha256(Path("/audit-prompt.md")) == audit["audit_campaign"][
    "audit_prompt_sha256"
]

print("OK campaign object and hash")
print("OK required legacy-selected-stage1 records")
print("OK prompt and translator byte identity")
print("OK GENERATED_SEMANTICS absence boundary")
