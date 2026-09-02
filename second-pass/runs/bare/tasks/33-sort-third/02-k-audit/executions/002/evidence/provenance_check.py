#!/usr/bin/env python3
"""Independent checks of launcher-declared mounted records and file hashes."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


audit_input = json.loads(Path("/audit-input.json").read_text(encoding="utf-8"))
campaign_lock = json.loads(
    Path("/audit-campaign-lock.json").read_text(encoding="utf-8")
)

print(f"record_layout={audit_input['record_layout']}")
print(f"semantics_mode={audit_input['semantics_mode']}")
print(f"campaign_block_equal={campaign_lock == audit_input['audit_campaign']}")
print(
    "reference_semantics_absent="
    f"{not Path('/reference/reference-semantics').exists()}"
)

required = [
    Path("/audit-input.json"),
    Path("/audit-campaign-lock.json"),
    Path("/run.json"),
    Path("/task.json"),
    Path("/generation-result.json"),
    Path("/generation-evidence/invocation.json"),
    Path("/generation-evidence/metrics.json"),
    Path("/generation-evidence/codex-last.txt"),
    Path("/generation-evidence/codex-output.log"),
    Path("/generation-evidence/prompt.txt"),
    Path("/generation-evidence/usage.json"),
]
print(
    "required_regular_readable="
    f"{all(p.is_file() and not p.is_symlink() and os.access(p, os.R_OK) for p in required)}"
)

checks = {
    "audit_campaign_lock_sha256": Path("/audit-campaign-lock.json"),
    "candidate_prompt_sha256": Path("/candidate/prompt.py"),
    "candidate_translator_sha256": Path("/candidate/py2mpy.py"),
    "canonical_sha256": Path("/reference/canonical.py"),
    "generation_codex_last_sha256": Path(
        "/generation-evidence/codex-last.txt"
    ),
    "generation_codex_output_sha256": Path(
        "/generation-evidence/codex-output.log"
    ),
    "stage1_invocation_sha256": Path(
        "/generation-evidence/invocation.json"
    ),
    "generation_metrics_sha256": Path(
        "/generation-evidence/metrics.json"
    ),
    "generation_prompt_sha256": Path("/generation-evidence/prompt.txt"),
    "generation_usage_sha256": Path("/generation-evidence/usage.json"),
    "run_manifest_sha256": Path("/run.json"),
    "task_manifest_sha256": Path("/task.json"),
    "stage1_result_sha256": Path("/generation-result.json"),
    "trusted_prompt_sha256": Path("/reference/prompt.py"),
    "trusted_translator_sha256": Path("/reference/py2mpy.py"),
}
for key, path in checks.items():
    actual = sha256(path)
    expected = audit_input["hashes"][key]
    print(f"{key}={actual} match={actual == expected}")

result = json.loads(Path("/generation-result.json").read_text(encoding="utf-8"))
trace_manifest = result["outputs"]["evidence"]
trace_root = Path("/generation-evidence/codex-trace")
for path in sorted(item for item in trace_root.rglob("*") if item.is_file()):
    relative = "codex-trace/" + path.relative_to(trace_root).as_posix()
    actual = sha256(path)
    print(f"{relative}={actual} match={actual == trace_manifest[relative]}")
    lines = path.read_text(encoding="utf-8").splitlines()
    for line in lines:
        json.loads(line)
    print(f"{relative}_jsonl_records={len(lines)} all_parsed=True")

print(
    "candidate_symlinks="
    f"{sum(path.is_symlink() for path in Path('/candidate').rglob('*'))}"
)
print(
    "reference_symlinks="
    f"{sum(path.is_symlink() for path in Path('/reference').rglob('*'))}"
)
