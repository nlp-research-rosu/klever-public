#!/usr/bin/env python3
"""Independent provenance/type/hash checks for the 11-string-xor audit."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import sys


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def require_regular(path: Path) -> None:
    if path.is_symlink() or not path.is_file():
        raise AssertionError(f"not a non-symlink regular file: {path}")


def require_directory(path: Path) -> None:
    if path.is_symlink() or not path.is_dir():
        raise AssertionError(f"not a non-symlink directory: {path}")


def tree_manifest(root: Path) -> tuple[list[dict[str, str]], str]:
    require_directory(root)
    entries: list[dict[str, str]] = []
    for path in sorted(root.rglob("*"), key=lambda item: item.relative_to(root).as_posix()):
        rel = path.relative_to(root).as_posix()
        if path.is_symlink():
            kind = "symlink"
            value = os.readlink(path)
        elif path.is_dir():
            kind = "directory"
            value = ""
        elif path.is_file():
            kind = "file"
            value = sha256_file(path)
        else:
            kind = "other"
            value = ""
        entries.append({"path": rel, "type": kind, "sha256_or_target": value})
    encoded = json.dumps(entries, sort_keys=True, separators=(",", ":")).encode()
    return entries, hashlib.sha256(encoded).hexdigest()


audit_input_path = Path("/audit-input.json")
lock_path = Path("/audit-campaign-lock.json")
require_regular(audit_input_path)
require_regular(lock_path)
audit_input = json.loads(audit_input_path.read_text(encoding="utf-8"))
lock = json.loads(lock_path.read_text(encoding="utf-8"))

print(f"record_layout={audit_input['record_layout']}")
print(f"semantics_mode={audit_input['semantics_mode']}")
assert audit_input["record_layout"] == "legacy-selected-stage1"
assert audit_input["semantics_mode"] == "SUPPLIED_SEMANTICS"
assert audit_input["audit_campaign"] == lock
print("campaign_object_match=true")

hashes = audit_input["hashes"]
fixed_hash_checks = {
    Path("/audit-campaign-lock.json"): "audit_campaign_lock_sha256",
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
for path, key in fixed_hash_checks.items():
    require_regular(path)
    actual = sha256_file(path)
    expected = hashes[key]
    print(f"hash {path} actual={actual} expected={expected} match={actual == expected}")
    assert actual == expected

required_records = [
    Path("/run.json"),
    Path("/task.json"),
    Path("/generation-result.json"),
    Path("/generation-evidence/invocation.json"),
    Path("/generation-evidence/metrics.json"),
    Path("/generation-evidence/codex-last.txt"),
    Path("/generation-evidence/codex-output.log"),
    Path("/generation-evidence/prompt.txt"),
]
for path in required_records:
    require_regular(path)
print(f"required_layout_records={len(required_records)} all_regular=true")

trace_root = Path("/generation-evidence/codex-trace")
require_directory(trace_root)
trace_files = sorted(trace_root.rglob("*.jsonl"))
assert trace_files
stage1_result = json.loads(Path("/generation-result.json").read_text(encoding="utf-8"))
declared_outputs = stage1_result["outputs"]["evidence"]
for path in trace_files:
    rel = path.relative_to(Path("/generation-evidence")).as_posix()
    require_regular(path)
    actual = sha256_file(path)
    expected = declared_outputs[rel]
    print(f"trace_hash {rel} actual={actual} expected={expected} match={actual == expected}")
    assert actual == expected
    line_count = 0
    with path.open(encoding="utf-8") as stream:
        for line_count, line in enumerate(stream, 1):
            json.loads(line)
    print(f"trace_jsonl {rel} lines={line_count} parse_ok=true")

candidate = Path("/candidate")
trusted_semantics = Path("/reference/reference-semantics")
candidate_semantics = candidate / "reference-semantics"
for root in (candidate, trusted_semantics, candidate_semantics):
    require_directory(root)

required_candidate_files = [
    "solution.py",
    "solution.mpy",
    "verification.k",
    "spec.k",
    "prove.sh",
]
for rel in required_candidate_files:
    require_regular(candidate / rel)
print(f"required_candidate_files={len(required_candidate_files)} all_regular=true")

candidate_entries, candidate_manifest_hash = tree_manifest(candidate)
trusted_entries, trusted_manifest_hash = tree_manifest(trusted_semantics)
submitted_entries, submitted_manifest_hash = tree_manifest(candidate_semantics)
assert all(entry["type"] in {"file", "directory"} for entry in candidate_entries)
assert trusted_entries == submitted_entries
print(f"candidate_entries={len(candidate_entries)} symlinks_or_other=0")
print(f"candidate_manifest_sha256={candidate_manifest_hash}")
print(f"launcher_recorded_candidate_tree_sha256={hashes['candidate_tree_sha256']}")
print(f"trusted_semantics_entries={len(trusted_entries)}")
print(f"trusted_semantics_manifest_sha256={trusted_manifest_hash}")
print(f"candidate_semantics_manifest_sha256={submitted_manifest_hash}")
print("semantics_trees_identical=true")

assert (candidate / "prompt.py").read_bytes() == Path("/reference/prompt.py").read_bytes()
assert (candidate / "py2mpy.py").read_bytes() == Path("/reference/py2mpy.py").read_bytes()
print("candidate_prompt_byte_identical=true")
print("candidate_translator_byte_identical=true")

generation_result = json.loads(Path("/generation-result.json").read_text(encoding="utf-8"))
invocation = json.loads(Path("/generation-evidence/invocation.json").read_text(encoding="utf-8"))
metrics = json.loads(Path("/generation-evidence/metrics.json").read_text(encoding="utf-8"))
usage = json.loads(Path("/generation-evidence/usage.json").read_text(encoding="utf-8"))
assert generation_result["status"] == invocation["status"] == metrics["status"] == "SUCCEEDED"
assert invocation["exit_code"] == metrics["exit_code"] == 0
assert usage["status"] == "COMPLETE"
print("generation_records_json_parse=true")
print("generation_records_claim_success=true (untrusted claim only)")
print("STAGE1_INTEGRITY_OK")

sys.exit(0)
