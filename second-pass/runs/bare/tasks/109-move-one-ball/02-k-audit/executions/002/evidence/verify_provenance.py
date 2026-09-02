#!/usr/bin/env python3
"""Independent launcher-record and mounted-input integrity checks."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require_regular(path: Path) -> None:
    if path.is_symlink() or not path.is_file() or not os.access(path, os.R_OK):
        raise AssertionError(f"required readable regular file missing: {path}")


def check_hash(label: str, path: Path, expected: str) -> None:
    require_regular(path)
    actual = sha256(path)
    print(f"{label}: actual={actual} expected={expected} match={actual == expected}")
    if actual != expected:
        raise AssertionError(label)


audit = json.load(open("/audit-input.json", encoding="utf-8"))
lock = json.load(open("/audit-campaign-lock.json", encoding="utf-8"))
hashes = audit["hashes"]

print(f"record_layout={audit['record_layout']}")
print(f"semantics_mode={audit['semantics_mode']}")
assert audit["record_layout"] == "legacy-selected-stage1"
assert audit["semantics_mode"] == "GENERATED_SEMANTICS"
assert lock == audit["audit_campaign"]
check_hash(
    "audit_campaign_lock",
    Path("/audit-campaign-lock.json"),
    hashes["audit_campaign_lock_sha256"],
)

direct = {
    "candidate_prompt": ("/candidate/prompt.py", "candidate_prompt_sha256"),
    "candidate_translator": ("/candidate/py2mpy.py", "candidate_translator_sha256"),
    "canonical": ("/reference/canonical.py", "canonical_sha256"),
    "generation_codex_last": (
        "/generation-evidence/codex-last.txt",
        "generation_codex_last_sha256",
    ),
    "generation_codex_output": (
        "/generation-evidence/codex-output.log",
        "generation_codex_output_sha256",
    ),
    "generation_metrics": (
        "/generation-evidence/metrics.json",
        "generation_metrics_sha256",
    ),
    "generation_prompt": (
        "/generation-evidence/prompt.txt",
        "generation_prompt_sha256",
    ),
    "generation_usage": (
        "/generation-evidence/usage.json",
        "generation_usage_sha256",
    ),
    "stage1_invocation": (
        "/generation-evidence/invocation.json",
        "stage1_invocation_sha256",
    ),
    "stage1_result": ("/generation-result.json", "stage1_result_sha256"),
    "run_manifest": ("/run.json", "run_manifest_sha256"),
    "task_manifest": ("/task.json", "task_manifest_sha256"),
    "trusted_prompt": ("/reference/prompt.py", "trusted_prompt_sha256"),
    "trusted_translator": ("/reference/py2mpy.py", "trusted_translator_sha256"),
}
for label, (path_text, key) in direct.items():
    check_hash(label, Path(path_text), hashes[key])

assert hashes["manifest_sha256"] == hashes["task_manifest_sha256"]
task_manifest = json.load(open("/task.json", encoding="utf-8"))
for key, value in task_manifest.items():
    assert audit["manifest"][key] == value
assert set(audit["manifest"]) - set(task_manifest) == {"config"}
assert audit["manifest"]["config"] == audit["config"]
print("audit_manifest_matches_task_fields_with_launcher_config_augmentation=True")
assert Path("/candidate/prompt.py").read_bytes() == Path("/reference/prompt.py").read_bytes()
assert Path("/candidate/py2mpy.py").read_bytes() == Path("/reference/py2mpy.py").read_bytes()
assert not Path("/reference/reference-semantics").exists()
print("candidate_prompt_matches_trusted=True")
print("candidate_translator_matches_trusted=True")
print("trusted_reference_semantics_absent=True")

required_layout_records = [
    Path("/run.json"),
    Path("/task.json"),
    Path("/generation-result.json"),
    Path("/generation-evidence/invocation.json"),
    Path("/generation-evidence/metrics.json"),
    Path("/generation-evidence/usage.json"),
    Path("/generation-evidence/codex-last.txt"),
    Path("/generation-evidence/codex-output.log"),
    Path("/generation-evidence/prompt.txt"),
]
for path in required_layout_records:
    require_regular(path)

for root in [Path("/candidate"), Path("/reference"), Path("/generation-evidence")]:
    symlinks = sorted(path for path in root.rglob("*") if path.is_symlink())
    print(f"symlinks_under_{root.name or 'root'}={len(symlinks)}")
    assert not symlinks

result = json.load(open("/generation-result.json", encoding="utf-8"))
for relative, expected in sorted(result["outputs"]["evidence"].items()):
    path = Path("/generation-evidence") / relative
    check_hash(f"generation_result_output:{relative}", path, expected)

trace_files = sorted(Path("/generation-evidence/codex-trace").rglob("*.jsonl"))
assert trace_files
trace_lines = 0
for path in trace_files:
    require_regular(path)
    with path.open(encoding="utf-8") as stream:
        for line in stream:
            json.loads(line)
            trace_lines += 1
print(f"structured_trace_files={len(trace_files)}")
print(f"structured_trace_json_lines={trace_lines}")

print("candidate_regular_file_manifest:")
for path in sorted(path for path in Path("/candidate").rglob("*") if path.is_file()):
    print(f"  {path.relative_to('/candidate')} size={path.stat().st_size} sha256={sha256(path)}")

print(f"recorded_candidate_tree_sha256={hashes['candidate_tree_sha256']}")
print(
    "recorded_generation_trace_tree_sha256="
    f"{hashes['generation_codex_trace_sha256']}"
)
print("PROVENANCE_CHECK=PASS")
