#!/usr/bin/env python3
"""Independent integrity checks over the mounted audit inputs."""

from __future__ import annotations

import hashlib
import json
import os
from collections import Counter
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")
LOCK = Path("/audit-campaign-lock.json")
GEN = Path("/generation-evidence")
CANDIDATE = Path("/candidate")
REFERENCE = Path("/reference")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require_regular(path: Path) -> None:
    assert path.exists(), f"missing: {path}"
    assert path.is_file(), f"not a regular file: {path}"
    assert not path.is_symlink(), f"symlinked: {path}"
    with path.open("rb") as stream:
        stream.read(1)


audit_input = json.loads(AUDIT_INPUT.read_text())
lock = json.loads(LOCK.read_text())

assert audit_input["record_layout"] == "legacy-selected-stage1"
assert audit_input["semantics_mode"] == "GENERATED_SEMANTICS"
assert audit_input["mount_reference_semantics"] is False
assert not (REFERENCE / "reference-semantics").exists()
assert lock == audit_input["audit_campaign"]
assert sha256(LOCK) == audit_input["hashes"]["audit_campaign_lock_sha256"]

required = [
    Path("/run.json"),
    Path("/task.json"),
    Path("/generation-result.json"),
    GEN / "invocation.json",
    GEN / "metrics.json",
    GEN / "codex-last.txt",
    GEN / "codex-output.log",
    GEN / "prompt.txt",
]
for path in required:
    require_regular(path)

trace_root = GEN / "codex-trace"
assert trace_root.is_dir() and not trace_root.is_symlink()
trace_files = sorted(path for path in trace_root.rglob("*") if path.is_file())
assert trace_files, "empty structured trace"
for path in trace_files:
    require_regular(path)

for root in (CANDIDATE, REFERENCE, GEN):
    symlinks = [str(path) for path in root.rglob("*") if path.is_symlink()]
    assert not symlinks, f"unexpected symlinks below {root}: {symlinks}"

hash_checks = {
    LOCK: "audit_campaign_lock_sha256",
    Path("/reference/canonical.py"): "canonical_sha256",
    Path("/reference/prompt.py"): "trusted_prompt_sha256",
    Path("/reference/py2mpy.py"): "trusted_translator_sha256",
    Path("/candidate/prompt.py"): "candidate_prompt_sha256",
    Path("/candidate/py2mpy.py"): "candidate_translator_sha256",
    Path("/run.json"): "run_manifest_sha256",
    Path("/task.json"): "task_manifest_sha256",
    Path("/generation-result.json"): "stage1_result_sha256",
    GEN / "invocation.json": "stage1_invocation_sha256",
    GEN / "metrics.json": "generation_metrics_sha256",
    GEN / "codex-last.txt": "generation_codex_last_sha256",
    GEN / "codex-output.log": "generation_codex_output_sha256",
    GEN / "prompt.txt": "generation_prompt_sha256",
}
if (GEN / "usage.json").exists():
    require_regular(GEN / "usage.json")
    hash_checks[GEN / "usage.json"] = "generation_usage_sha256"

for path, key in hash_checks.items():
    actual = sha256(path)
    expected = audit_input["hashes"][key]
    assert actual == expected, (path, actual, expected)
    print(f"HASH_OK {key} {actual} {path}")

assert (CANDIDATE / "prompt.py").read_bytes() == (REFERENCE / "prompt.py").read_bytes()
assert (CANDIDATE / "py2mpy.py").read_bytes() == (REFERENCE / "py2mpy.py").read_bytes()
print("BYTE_IDENTITY_OK candidate/prompt.py reference/prompt.py")
print("BYTE_IDENTITY_OK candidate/py2mpy.py reference/py2mpy.py")

invocation = json.loads((GEN / "invocation.json").read_text())
result = json.loads(Path("/generation-result.json").read_text())
declared_outputs = invocation["outputs"]["evidence"]
assert declared_outputs == result["outputs"]["evidence"]
for relative, expected in sorted(declared_outputs.items()):
    path = GEN / relative
    require_regular(path)
    actual = sha256(path)
    assert actual == expected, (path, actual, expected)
    print(f"DECLARED_OUTPUT_OK {actual} {relative}")

trace_lines = 0
trace_top_types: Counter[str] = Counter()
trace_payload_types: Counter[str] = Counter()
for path in trace_files:
    with path.open(encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, 1):
            record = json.loads(line)
            trace_lines += 1
            trace_top_types[str(record.get("type", "<none>"))] += 1
            payload = record.get("payload")
            if isinstance(payload, dict):
                trace_payload_types[str(payload.get("type", "<none>"))] += 1
print(f"TRACE_JSON_OK files={len(trace_files)} records={trace_lines}")
print(f"TRACE_TOP_TYPES {dict(trace_top_types)}")
print(f"TRACE_PAYLOAD_TYPES {dict(trace_payload_types)}")

print("RECORD_LAYOUT legacy-selected-stage1")
print("SEMANTICS_BOUNDARY GENERATED_SEMANTICS reference-semantics absent")
print("CAMPAIGN_LOCK deep-equal and hash-matched")
print("PROVENANCE_RESULT PASS")
