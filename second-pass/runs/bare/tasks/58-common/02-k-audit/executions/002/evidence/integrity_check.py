#!/usr/bin/env python3
"""Recheck mounted provenance using only container paths."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from pathlib import Path
import sys

sys.path.insert(0, "/opt/humaneval/tools")
from pipeline_contract import sha256_tree  # type: ignore  # launcher pipeline helper


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


audit = json.loads(Path("/audit-input.json").read_text())
lock = json.loads(Path("/audit-campaign-lock.json").read_text())
hashes = audit["hashes"]

checks = {
    "/audit-campaign-lock.json": hashes["audit_campaign_lock_sha256"],
    "/run.json": hashes["run_manifest_sha256"],
    "/task.json": hashes["task_manifest_sha256"],
    "/generation-result.json": hashes["stage1_result_sha256"],
    "/generation-evidence/invocation.json": hashes["stage1_invocation_sha256"],
    "/generation-evidence/metrics.json": hashes["generation_metrics_sha256"],
    "/generation-evidence/usage.json": hashes["generation_usage_sha256"],
    "/generation-evidence/codex-last.txt": hashes["generation_codex_last_sha256"],
    "/generation-evidence/codex-output.log": hashes["generation_codex_output_sha256"],
    "/generation-evidence/prompt.txt": hashes["generation_prompt_sha256"],
    "/reference/canonical.py": hashes["canonical_sha256"],
    "/reference/prompt.py": hashes["trusted_prompt_sha256"],
    "/reference/py2mpy.py": hashes["trusted_translator_sha256"],
    "/candidate/prompt.py": hashes["candidate_prompt_sha256"],
    "/candidate/py2mpy.py": hashes["candidate_translator_sha256"],
}

failures = []
print("record_layout=", audit["record_layout"])
print("semantics_mode=", audit["semantics_mode"])
print("campaign_object_equals_lock=", audit["audit_campaign"] == lock)
if audit["audit_campaign"] != lock:
    failures.append("campaign object differs")

for raw_path, expected in checks.items():
    path = Path(raw_path)
    mode = path.lstat().st_mode
    regular = stat.S_ISREG(mode)
    actual = digest(path) if regular else "NOT_REGULAR"
    matched = actual == expected
    print(f"FILE {raw_path} regular={regular} actual={actual} expected={expected} match={matched}")
    if not regular or not matched:
        failures.append(raw_path)

required_layout_files = [
    "/run.json",
    "/task.json",
    "/generation-result.json",
    "/generation-evidence/invocation.json",
    "/generation-evidence/metrics.json",
    "/generation-evidence/codex-last.txt",
    "/generation-evidence/codex-output.log",
    "/generation-evidence/prompt.txt",
    "/generation-evidence/usage.json",
]
for raw_path in required_layout_files:
    path = Path(raw_path)
    okay = path.exists() and stat.S_ISREG(path.lstat().st_mode)
    print(f"REQUIRED {raw_path} regular={okay}")
    if not okay:
        failures.append(raw_path)

for root in [Path("/candidate"), Path("/generation-evidence/codex-trace")]:
    bad = []
    for current, directories, files in os.walk(root):
        for name in directories + files:
            path = Path(current) / name
            mode = path.lstat().st_mode
            if not (stat.S_ISDIR(mode) or stat.S_ISREG(mode)):
                bad.append(str(path))
    print(f"TREE_TYPES {root} unsupported_or_linked={bad}")
    failures.extend(bad)

candidate_tree = sha256_tree(Path("/candidate"))
trace_tree = sha256_tree(Path("/generation-evidence/codex-trace"))
generation_result = json.loads(Path("/generation-result.json").read_text())
usage = json.loads(Path("/generation-evidence/usage.json").read_text())
print("PIPELINE_TREE /candidate", candidate_tree)
print("RECORDED generation-result workspace_sha256", generation_result["outputs"]["workspace_sha256"])
print("PIPELINE_TREE /generation-evidence/codex-trace", trace_tree)
print("RECORDED usage source_trace_sha256", usage["source_trace_sha256"])
if candidate_tree != generation_result["outputs"]["workspace_sha256"]:
    failures.append("candidate pipeline tree mismatch")
if trace_tree != usage["source_trace_sha256"]:
    failures.append("trace pipeline tree mismatch")

prompt_match = Path("/candidate/prompt.py").read_bytes() == Path("/reference/prompt.py").read_bytes()
translator_match = (
    Path("/candidate/py2mpy.py").read_bytes() == Path("/reference/py2mpy.py").read_bytes()
)
no_reference_semantics = not Path("/reference/reference-semantics").exists()
print("candidate_prompt_matches_trusted=", prompt_match)
print("candidate_translator_matches_trusted=", translator_match)
print("generated_mode_reference_semantics_absent=", no_reference_semantics)
if not (prompt_match and translator_match and no_reference_semantics):
    failures.append("trusted input or semantics-mode boundary mismatch")

print("FAILURES=", failures)
raise SystemExit(bool(failures))
