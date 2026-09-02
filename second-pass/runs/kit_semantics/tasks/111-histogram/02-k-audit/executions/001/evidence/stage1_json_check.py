#!/usr/bin/env python3
"""Independently check launcher JSON records and their declared SHA-256 values."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


def load_json(path: str) -> object:
    with Path(path).open("rb") as handle:
        return json.load(handle)


def sha256(path: str) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


audit = load_json("/audit-input.json")
lock = load_json("/audit-campaign-lock.json")
assert isinstance(audit, dict)
assert audit["record_layout"] == "pipeline-v3"
assert audit["semantics_mode"] == "SUPPLIED_SEMANTICS"
assert audit["audit_campaign"] == lock
print("audit_campaign exactly equals lock JSON: yes")

hash_checks = {
    "audit_campaign_lock_sha256": "/audit-campaign-lock.json",
    "canonical_sha256": "/reference/canonical.py",
    "trusted_prompt_sha256": "/reference/prompt.py",
    "trusted_translator_sha256": "/reference/py2mpy.py",
    "candidate_prompt_sha256": "/candidate/prompt.py",
    "candidate_translator_sha256": "/candidate/py2mpy.py",
    "run_manifest_sha256": "/run.json",
    "task_manifest_sha256": "/task.json",
    "stage1_result_sha256": "/generation-result.json",
    "stage1_invocation_sha256": "/generation-evidence/invocation.json",
    "generation_metrics_sha256": "/generation-evidence/metrics.json",
    "generation_runtime_metrics_sha256": "/generation-evidence/runtime-metrics.json",
    "generation_usage_sha256": "/generation-evidence/usage.json",
    "generation_codex_last_sha256": "/generation-evidence/codex-last.txt",
    "generation_codex_output_sha256": "/generation-evidence/codex-output.log",
    "generation_prompt_sha256": "/generation-evidence/prompt.txt",
}
for field, path in hash_checks.items():
    actual = sha256(path)
    expected = audit["hashes"][field]
    assert actual == expected, (field, expected, actual)
print(f"declared individual SHA-256 checks passed: {len(hash_checks)}")

for logical_name, path in audit["container_paths"].items():
    assert Path(path).exists(), (logical_name, path)
print(f"declared container paths present: {len(audit['container_paths'])}")

json_records = [
    "/run.json",
    "/task.json",
    "/generation-result.json",
    "/generation-evidence/invocation.json",
    "/generation-evidence/metrics.json",
    "/generation-evidence/runtime-metrics.json",
    "/generation-evidence/usage.json",
]
for path in json_records:
    value = load_json(path)
    assert isinstance(value, (dict, list)), path
print(f"required JSON records parse successfully: {len(json_records)}")
