#!/usr/bin/env python3
"""Independent provenance and mount-integrity checks for this audit."""

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
        while chunk := stream.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def require_plain_file(path: Path) -> None:
    assert path.exists(), f"missing required record: {path}"
    assert path.is_file(), f"not a regular file: {path}"
    assert not path.is_symlink(), f"symlinked required record: {path}"
    with path.open("rb") as stream:
        stream.read(1)


audit = json.loads(AUDIT_INPUT.read_text(encoding="utf-8"))
lock = json.loads(LOCK.read_text(encoding="utf-8"))

print(f"record_layout={audit['record_layout']}")
print(f"semantics_mode={audit['semantics_mode']}")
assert audit["record_layout"] == "legacy-selected-stage1"
assert audit["semantics_mode"] == "SUPPLIED_SEMANTICS"
assert lock == audit["audit_campaign"]
print("campaign_block_matches_lock=true")

declared_lock_hash = audit["hashes"]["audit_campaign_lock_sha256"]
actual_lock_hash = sha256(LOCK)
print(f"audit_campaign_lock_sha256={actual_lock_hash}")
assert actual_lock_hash == declared_lock_hash

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
for path in required:
    require_plain_file(path)
require_plain_file(Path("/generation-evidence/usage.json"))

trace_files = sorted(Path("/generation-evidence/codex-trace").rglob("*"))
trace_regular = [p for p in trace_files if p.is_file() and not p.is_symlink()]
assert trace_regular, "structured trace is empty"
assert not any(p.is_symlink() for p in trace_files), "symlink in structured trace"
print(f"trace_regular_files={len(trace_regular)}")

hash_checks = {
    Path("/run.json"): "run_manifest_sha256",
    Path("/task.json"): "task_manifest_sha256",
    Path("/generation-result.json"): "stage1_result_sha256",
    Path("/generation-evidence/invocation.json"): "stage1_invocation_sha256",
    Path("/generation-evidence/metrics.json"): "generation_metrics_sha256",
    Path("/generation-evidence/usage.json"): "generation_usage_sha256",
    Path("/generation-evidence/codex-last.txt"): "generation_codex_last_sha256",
    Path("/generation-evidence/codex-output.log"): "generation_codex_output_sha256",
    Path("/generation-evidence/prompt.txt"): "generation_prompt_sha256",
    Path("/reference/canonical.py"): "canonical_sha256",
    Path("/reference/prompt.py"): "trusted_prompt_sha256",
    Path("/reference/py2mpy.py"): "trusted_translator_sha256",
    Path("/candidate/prompt.py"): "candidate_prompt_sha256",
    Path("/candidate/py2mpy.py"): "candidate_translator_sha256",
}
for path, key in hash_checks.items():
    require_plain_file(path)
    actual = sha256(path)
    expected = audit["hashes"][key]
    print(f"{key}: expected={expected} actual={actual} match={actual == expected}")
    assert actual == expected

result = json.loads(Path("/generation-result.json").read_text(encoding="utf-8"))
invocation = json.loads(
    Path("/generation-evidence/invocation.json").read_text(encoding="utf-8")
)
for rel, expected in result["outputs"]["evidence"].items():
    path = Path("/generation-evidence") / rel
    require_plain_file(path)
    actual = sha256(path)
    print(f"result evidence {rel}: expected={expected} actual={actual} match={actual == expected}")
    assert actual == expected
for rel, expected in invocation["outputs"]["evidence"].items():
    path = Path("/generation-evidence") / rel
    require_plain_file(path)
    actual = sha256(path)
    assert actual == expected, (rel, expected, actual)
print("invocation_evidence_hashes_match=true")

assert Path("/reference/reference-semantics").is_dir()
assert Path("/candidate/reference-semantics").is_dir()
print("required_supplied_semantics_mounts_present=true")

for root in [
    Path("/candidate"),
    Path("/reference/reference-semantics"),
    Path("/generation-evidence/codex-trace"),
]:
    links = [str(p) for p in root.rglob("*") if p.is_symlink()]
    print(f"symlinks_under_{root}={len(links)}")
    assert not links

print("PROVENANCE_CHECK=PASS")
