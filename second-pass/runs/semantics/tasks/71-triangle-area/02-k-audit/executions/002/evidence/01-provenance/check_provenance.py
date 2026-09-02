#!/usr/bin/env python3
"""Independent checks of launcher records and mounted provenance inputs."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def require_regular(path: Path) -> None:
    assert path.exists(), f"missing: {path}"
    assert not path.is_symlink(), f"symlink forbidden: {path}"
    assert path.is_file(), f"not a regular file: {path}"


data = json.loads(AUDIT_INPUT.read_text())
assert data["record_layout"] == "legacy-selected-stage1"
assert data["semantics_mode"] == "SUPPLIED_SEMANTICS"

paths = {
    "audit_campaign_lock_sha256": Path("/audit-campaign-lock.json"),
    "canonical_sha256": Path("/reference/canonical.py"),
    "trusted_prompt_sha256": Path("/reference/prompt.py"),
    "trusted_translator_sha256": Path("/reference/py2mpy.py"),
    "candidate_prompt_sha256": Path("/candidate/prompt.py"),
    "candidate_translator_sha256": Path("/candidate/py2mpy.py"),
    "run_manifest_sha256": Path("/run.json"),
    "task_manifest_sha256": Path("/task.json"),
    "stage1_result_sha256": Path("/generation-result.json"),
    "stage1_invocation_sha256": Path("/generation-evidence/invocation.json"),
    "generation_metrics_sha256": Path("/generation-evidence/metrics.json"),
    "generation_usage_sha256": Path("/generation-evidence/usage.json"),
    "generation_codex_last_sha256": Path("/generation-evidence/codex-last.txt"),
    "generation_codex_output_sha256": Path("/generation-evidence/codex-output.log"),
    "generation_prompt_sha256": Path("/generation-evidence/prompt.txt"),
}

for key, path in paths.items():
    require_regular(path)
    actual = sha256(path)
    expected = data["hashes"][key]
    print(f"{key}: expected={expected} actual={actual} match={actual == expected}")
    assert actual == expected

lock = json.loads(Path("/audit-campaign-lock.json").read_text())
assert lock == data["audit_campaign"]
print("campaign lock structurally equals audit_input.audit_campaign: True")

required_layout_records = [
    Path("/run.json"),
    Path("/task.json"),
    Path("/generation-result.json"),
    Path("/generation-evidence/invocation.json"),
    Path("/generation-evidence/metrics.json"),
    Path("/generation-evidence/codex-last.txt"),
    Path("/generation-evidence/codex-output.log"),
    Path("/generation-evidence/prompt.txt"),
]
for path in required_layout_records:
    require_regular(path)
print(f"required legacy-selected-stage1 records: {len(required_layout_records)}/"
      f"{len(required_layout_records)} regular, non-symlink files")

trace_root = Path("/generation-evidence/codex-trace")
assert trace_root.is_dir() and not trace_root.is_symlink()
trace_files = sorted(p for p in trace_root.rglob("*") if p.is_file())
assert trace_files
for path in trace_files:
    require_regular(path)
    print(f"trace file {path.relative_to(trace_root)} sha256={sha256(path)}")

assert Path("/reference/reference-semantics").is_dir()
print("trusted reference semantics required by supplied mode: present")

for root in (Path("/candidate"), Path("/reference"), Path("/generation-evidence")):
    symlinks = [p for p in root.rglob("*") if p.is_symlink()]
    print(f"symlinks below {root}: {len(symlinks)}")
    assert not symlinks

print("PROVENANCE_CHECKS_OK")
