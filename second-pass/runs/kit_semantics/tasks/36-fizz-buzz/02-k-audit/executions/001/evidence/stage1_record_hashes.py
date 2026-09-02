#!/usr/bin/env python3
"""Compare launcher-declared hashes with independently mounted-file hashes."""

import json
from hashlib import sha256
from pathlib import Path


audit = json.loads(Path("/audit-input.json").read_text())
result = json.loads(Path("/generation-result.json").read_text())

checks = {
    "audit_campaign_lock_sha256": Path("/audit-campaign-lock.json"),
    "run_manifest_sha256": Path("/run.json"),
    "task_manifest_sha256": Path("/task.json"),
    "stage1_result_sha256": Path("/generation-result.json"),
    "stage1_invocation_sha256": Path("/generation-evidence/invocation.json"),
    "generation_metrics_sha256": Path("/generation-evidence/metrics.json"),
    "generation_runtime_metrics_sha256": Path("/generation-evidence/runtime-metrics.json"),
    "generation_usage_sha256": Path("/generation-evidence/usage.json"),
    "generation_codex_last_sha256": Path("/generation-evidence/codex-last.txt"),
    "generation_codex_output_sha256": Path("/generation-evidence/codex-output.log"),
    "generation_prompt_sha256": Path("/generation-evidence/prompt.txt"),
    "canonical_sha256": Path("/reference/canonical.py"),
    "trusted_prompt_sha256": Path("/reference/prompt.py"),
    "trusted_translator_sha256": Path("/reference/py2mpy.py"),
    "candidate_prompt_sha256": Path("/candidate/prompt.py"),
    "candidate_translator_sha256": Path("/candidate/py2mpy.py"),
}

ok = True
for key, path in checks.items():
    actual = sha256(path.read_bytes()).hexdigest()
    expected = audit["hashes"][key]
    match = actual == expected
    print(f"{key}: expected={expected} actual={actual} match={match}")
    ok &= match

for relative, expected in sorted(result["outputs"]["evidence"].items()):
    path = Path("/generation-evidence") / relative
    actual = sha256(path.read_bytes()).hexdigest()
    match = actual == expected
    print(f"generation-result:{relative}: expected={expected} actual={actual} match={match}")
    ok &= match

raise SystemExit(0 if ok else 1)
