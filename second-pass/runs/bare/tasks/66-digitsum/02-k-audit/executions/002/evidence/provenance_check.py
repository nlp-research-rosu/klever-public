#!/usr/bin/env python3
"""Independent integrity checks for the mounted audit inputs.

This script intentionally treats every generation record as data.  It reads
every required legacy-selected-stage1 record, validates the JSON/JSONL
structure, hashes the mounted bytes, and compares the hashes that have a
declared byte-level or pipeline-contract interpretation.
"""

from __future__ import annotations

import hashlib
import json
import os
import stat
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, "/opt/humaneval/tools")
from pipeline_contract import sha256_tree  # type: ignore  # audited helper


def file_hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def require_regular(path: Path) -> None:
    mode = path.lstat().st_mode
    if not stat.S_ISREG(mode):
        raise AssertionError(f"not a real regular file: {path}")
    with path.open("rb") as stream:
        stream.read(1)


def require_real_tree(path: Path) -> None:
    if not stat.S_ISDIR(path.lstat().st_mode):
        raise AssertionError(f"not a real directory: {path}")
    for current, directories, files in os.walk(path, followlinks=False):
        for name in directories + files:
            child = Path(current, name)
            mode = child.lstat().st_mode
            if not (stat.S_ISDIR(mode) or stat.S_ISREG(mode)):
                raise AssertionError(f"linked or unsupported tree entry: {child}")


def load_json(path: Path) -> object:
    require_regular(path)
    with path.open(encoding="utf-8") as stream:
        return json.load(stream)


audit_path = Path("/audit-input.json")
lock_path = Path("/audit-campaign-lock.json")
audit = load_json(audit_path)
lock = load_json(lock_path)
assert isinstance(audit, dict)
assert isinstance(lock, dict)

print("COMMAND: python3 /audit-output/evidence/provenance_check.py")
print(f"record_layout={audit['record_layout']}")
print(f"semantics_mode={audit['semantics_mode']}")
assert audit["record_layout"] == "legacy-selected-stage1"
assert audit["semantics_mode"] == "GENERATED_SEMANTICS"
assert audit["mount_reference_semantics"] is False
assert not Path("/reference/reference-semantics").exists()

assert audit["audit_campaign"] == lock
actual_lock_hash = file_hash(lock_path)
assert actual_lock_hash == audit["hashes"]["audit_campaign_lock_sha256"]
print(f"campaign_lock_exact_match=yes sha256={actual_lock_hash}")

required_files = [
    audit_path,
    lock_path,
    Path("/run.json"),
    Path("/task.json"),
    Path("/generation-result.json"),
    Path("/generation-evidence/invocation.json"),
    Path("/generation-evidence/metrics.json"),
    Path("/generation-evidence/codex-last.txt"),
    Path("/generation-evidence/codex-output.log"),
    Path("/generation-evidence/prompt.txt"),
    Path("/generation-evidence/usage.json"),
    Path("/reference/canonical.py"),
    Path("/reference/prompt.py"),
    Path("/reference/py2mpy.py"),
    Path("/candidate/prompt.py"),
    Path("/candidate/py2mpy.py"),
    Path("/candidate/solution.py"),
    Path("/candidate/solution.mpy"),
    Path("/candidate/semantic.k"),
    Path("/candidate/verification.k"),
    Path("/candidate/spec.k"),
    Path("/candidate/prove.sh"),
]
for required in required_files:
    require_regular(required)

for tree in (
    Path("/candidate"),
    Path("/generation-evidence"),
    Path("/generation-evidence/codex-trace"),
    Path("/reference"),
):
    require_real_tree(tree)
print(f"required_regular_files={len(required_files)} all_readable=yes")
print("required_trees_real_and_link_free=yes")

# Fully parse all structured records required for this layout.
structured_records = [
    Path("/run.json"),
    Path("/task.json"),
    Path("/generation-result.json"),
    Path("/generation-evidence/invocation.json"),
    Path("/generation-evidence/metrics.json"),
    Path("/generation-evidence/usage.json"),
]
records = {str(path): load_json(path) for path in structured_records}
print(f"required_json_records_parsed={len(records)}")

hash_expectations = {
    Path("/reference/canonical.py"): "canonical_sha256",
    Path("/reference/prompt.py"): "trusted_prompt_sha256",
    Path("/reference/py2mpy.py"): "trusted_translator_sha256",
    Path("/candidate/prompt.py"): "candidate_prompt_sha256",
    Path("/candidate/py2mpy.py"): "candidate_translator_sha256",
    Path("/run.json"): "run_manifest_sha256",
    Path("/task.json"): "task_manifest_sha256",
    Path("/generation-result.json"): "stage1_result_sha256",
    Path("/generation-evidence/invocation.json"): "stage1_invocation_sha256",
    Path("/generation-evidence/metrics.json"): "generation_metrics_sha256",
    Path("/generation-evidence/codex-last.txt"): "generation_codex_last_sha256",
    Path("/generation-evidence/codex-output.log"): "generation_codex_output_sha256",
    Path("/generation-evidence/prompt.txt"): "generation_prompt_sha256",
    Path("/generation-evidence/usage.json"): "generation_usage_sha256",
}
for path, key in hash_expectations.items():
    actual = file_hash(path)
    expected = audit["hashes"][key]
    assert actual == expected, (path, actual, expected)
    print(f"sha256_ok {path} {actual}")

assert Path("/candidate/prompt.py").read_bytes() == Path(
    "/reference/prompt.py"
).read_bytes()
assert Path("/candidate/py2mpy.py").read_bytes() == Path(
    "/reference/py2mpy.py"
).read_bytes()
print("candidate_prompt_matches_trusted_bytes=yes")
print("candidate_translator_matches_trusted_bytes=yes")

result = records["/generation-result.json"]
invocation = records["/generation-evidence/invocation.json"]
usage = records["/generation-evidence/usage.json"]
assert isinstance(result, dict)
assert isinstance(invocation, dict)
assert isinstance(usage, dict)

result_evidence = result["outputs"]["evidence"]
assert result_evidence == invocation["outputs"]["evidence"]
for relative, expected in sorted(result_evidence.items()):
    path = Path("/generation-evidence", relative)
    require_regular(path)
    actual = file_hash(path)
    assert actual == expected, (relative, actual, expected)
    print(f"generation_manifest_hash_ok {relative} {actual}")

workspace_hash = sha256_tree(Path("/candidate"))
assert workspace_hash == result["outputs"]["workspace_sha256"]
assert workspace_hash == invocation["retained_workspace_sha256"]
print(f"pipeline_contract_candidate_tree_sha256={workspace_hash}")

trace_hash = sha256_tree(Path("/generation-evidence/codex-trace"))
assert trace_hash == usage["source_trace_sha256"]
print(f"pipeline_contract_trace_tree_sha256={trace_hash}")

# The launcher also records opaque mount-snapshot tree digests.  Record them
# without conflating that representation with pipeline_contract.sha256_tree.
print(
    "launcher_candidate_tree_digest="
    + str(audit["hashes"]["candidate_tree_sha256"])
)
print(
    "launcher_trace_tree_digest="
    + str(audit["hashes"]["generation_codex_trace_sha256"])
)

trace_files = sorted(Path("/generation-evidence/codex-trace").rglob("*.jsonl"))
assert trace_files
line_types: Counter[str] = Counter()
line_count = 0
for trace_file in trace_files:
    with trace_file.open(encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, 1):
            event = json.loads(line)
            assert isinstance(event, dict)
            assert "timestamp" in event and "type" in event and "payload" in event
            line_types[str(event["type"])] += 1
            line_count += 1
print(f"structured_trace_files={len(trace_files)} json_lines={line_count}")
print("structured_trace_top_level_types=" + json.dumps(dict(sorted(line_types.items()))))

# Force complete reads of the two unstructured records, then report bounded
# metadata rather than replaying untrusted prose.
for path in (
    Path("/generation-evidence/codex-last.txt"),
    Path("/generation-evidence/codex-output.log"),
    Path("/generation-evidence/prompt.txt"),
):
    data = path.read_bytes()
    print(f"fully_read {path} bytes={len(data)} sha256={hashlib.sha256(data).hexdigest()}")

print("PROVENANCE_CHECK=PASS")
