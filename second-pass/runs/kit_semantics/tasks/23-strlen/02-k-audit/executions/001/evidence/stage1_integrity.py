#!/usr/bin/env python3
"""Independent integrity and provenance checks for the mounted audit inputs."""

from __future__ import annotations

import collections
import hashlib
import json
import os
import stat
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")
LOCK = Path("/audit-campaign-lock.json")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as stream:
        return json.load(stream)


def require_regular(path: Path) -> None:
    mode = path.lstat().st_mode
    assert stat.S_ISREG(mode), f"not a regular file: {path}"


def require_directory(path: Path) -> None:
    mode = path.lstat().st_mode
    assert stat.S_ISDIR(mode), f"not a directory: {path}"


def tree_entries(root: Path) -> dict[str, tuple[str, str | None]]:
    """Return relative paths mapped to (entry type, file digest). Never follow links."""
    require_directory(root)
    entries: dict[str, tuple[str, str | None]] = {}
    for directory, dirnames, filenames in os.walk(root, followlinks=False):
        directory_path = Path(directory)
        for name in sorted(dirnames + filenames):
            path = directory_path / name
            relative = path.relative_to(root).as_posix()
            mode = path.lstat().st_mode
            if stat.S_ISLNK(mode):
                entries[relative] = ("symlink", os.readlink(path))
            elif stat.S_ISDIR(mode):
                entries[relative] = ("directory", None)
            elif stat.S_ISREG(mode):
                entries[relative] = ("file", sha256(path))
            else:
                entries[relative] = ("other", None)
    return entries


audit = load_json(AUDIT_INPUT)
lock = load_json(LOCK)

print(f"record_layout={audit['record_layout']}")
print(f"semantics_mode={audit['semantics_mode']}")
print(f"problem_id={audit['problem_id']}")
assert audit["record_layout"] == "pipeline-v3"
assert audit["semantics_mode"] == "SUPPLIED_SEMANTICS"
assert audit["mount_reference_semantics"] is True
assert lock == audit["audit_campaign"], "campaign lock JSON differs from audit_campaign"
actual_lock_hash = sha256(LOCK)
expected_lock_hash = audit["hashes"]["audit_campaign_lock_sha256"]
print(f"campaign_lock_json_equal=true")
print(f"campaign_lock_sha256 actual={actual_lock_hash} expected={expected_lock_hash}")
assert actual_lock_hash == expected_lock_hash

required_files = [
    Path("/run.json"),
    Path("/task.json"),
    Path("/generation-result.json"),
    Path("/generation-evidence/invocation.json"),
    Path("/generation-evidence/metrics.json"),
    Path("/generation-evidence/runtime-metrics.json"),
    Path("/generation-evidence/usage.json"),
    Path("/generation-evidence/codex-last.txt"),
    Path("/generation-evidence/codex-output.log"),
    Path("/generation-evidence/prompt.txt"),
]
for path in required_files:
    require_regular(path)
require_directory(Path("/generation-evidence/codex-trace"))
print(f"pipeline_required_records_regular={len(required_files)}")

hash_checks = {
    Path("/run.json"): "run_manifest_sha256",
    Path("/task.json"): "task_manifest_sha256",
    Path("/generation-result.json"): "stage1_result_sha256",
    Path("/generation-evidence/invocation.json"): "stage1_invocation_sha256",
    Path("/generation-evidence/metrics.json"): "generation_metrics_sha256",
    Path("/generation-evidence/runtime-metrics.json"): "generation_runtime_metrics_sha256",
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
    require_regular(path)
    actual = sha256(path)
    expected = audit["hashes"][key]
    print(f"hash {path} actual={actual} expected={expected} match={actual == expected}")
    assert actual == expected

generation_result = load_json(Path("/generation-result.json"))
invocation = load_json(Path("/generation-evidence/invocation.json"))
for record in (generation_result, invocation):
    recorded = record["outputs"]["evidence"]
    for relative, expected in sorted(recorded.items()):
        path = Path("/generation-evidence") / relative
        require_regular(path)
        actual = sha256(path)
        print(
            f"generation_record_hash {relative} actual={actual} "
            f"expected={expected} match={actual == expected}"
        )
        assert actual == expected

assert Path("/candidate/prompt.py").read_bytes() == Path("/reference/prompt.py").read_bytes()
assert Path("/candidate/py2mpy.py").read_bytes() == Path("/reference/py2mpy.py").read_bytes()
print("candidate_prompt_byte_identical=true")
print("candidate_translator_byte_identical=true")

candidate_semantics = tree_entries(Path("/candidate/reference-semantics"))
trusted_semantics = tree_entries(Path("/reference/reference-semantics"))
assert all(kind not in {"symlink", "other"} for kind, _ in candidate_semantics.values())
assert all(kind not in {"symlink", "other"} for kind, _ in trusted_semantics.values())
assert candidate_semantics == trusted_semantics
semantics_manifest = "\n".join(
    f"{kind}\t{digest or '-'}\t{relative}"
    for relative, (kind, digest) in sorted(candidate_semantics.items())
)
semantics_manifest_digest = hashlib.sha256(semantics_manifest.encode()).hexdigest()
semantics_file_count = sum(kind == "file" for kind, _ in candidate_semantics.values())
semantics_dir_count = sum(kind == "directory" for kind, _ in candidate_semantics.values())
print(
    f"semantics_trees_byte_identical=true files={semantics_file_count} "
    f"directories={semantics_dir_count}"
)
print(f"independent_semantics_manifest_sha256={semantics_manifest_digest}")

generation_entries = tree_entries(Path("/generation-evidence"))
bad_generation_entries = [
    relative
    for relative, (kind, _) in generation_entries.items()
    if kind in {"symlink", "other"}
]
assert not bad_generation_entries
print(f"generation_tree_entries={len(generation_entries)} symlink_or_other=0")

candidate_entries = tree_entries(Path("/candidate"))
bad_candidate_entries = [
    relative
    for relative, (kind, _) in candidate_entries.items()
    if kind in {"symlink", "other"}
]
assert not bad_candidate_entries
candidate_manifest = "\n".join(
    f"{kind}\t{digest or '-'}\t{relative}"
    for relative, (kind, digest) in sorted(candidate_entries.items())
)
candidate_manifest_digest = hashlib.sha256(candidate_manifest.encode()).hexdigest()
candidate_file_count = sum(kind == "file" for kind, _ in candidate_entries.values())
candidate_dir_count = sum(kind == "directory" for kind, _ in candidate_entries.values())
print(
    f"candidate_tree_entries={len(candidate_entries)} files={candidate_file_count} "
    f"directories={candidate_dir_count} symlink_or_other=0"
)
print(f"independent_candidate_manifest_sha256={candidate_manifest_digest}")
for name in [
    "solution.py",
    "solution.mpy",
    "verification.k",
    "spec.k",
    "prove.sh",
    "PROOF.md",
]:
    path = Path("/candidate") / name
    require_regular(path)
    print(f"candidate_required_artifact {name} sha256={sha256(path)}")

trace_files = sorted(Path("/generation-evidence/codex-trace").rglob("*.jsonl"))
assert trace_files, "structured trace has no JSONL file"
trace_type_counts: collections.Counter[str] = collections.Counter()
payload_type_counts: collections.Counter[str] = collections.Counter()
trace_lines = 0
final_answers = 0
task_started = 0
task_complete = 0
for trace_path in trace_files:
    require_regular(trace_path)
    with trace_path.open("r", encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, 1):
            record = json.loads(line)
            trace_lines += 1
            trace_type_counts[str(record.get("type"))] += 1
            payload = record.get("payload")
            if isinstance(payload, dict):
                payload_type_counts[str(payload.get("type"))] += 1
                if payload.get("type") == "task_started":
                    task_started += 1
                if payload.get("type") == "task_complete":
                    task_complete += 1
                if payload.get("type") == "message" and payload.get("role") == "assistant":
                    if payload.get("phase") == "final_answer":
                        final_answers += 1
print(f"trace_files={len(trace_files)} trace_json_records={trace_lines}")
print(f"trace_record_types={dict(sorted(trace_type_counts.items()))}")
print(f"trace_payload_types={dict(sorted(payload_type_counts.items()))}")
print(
    f"trace_task_started={task_started} trace_task_complete={task_complete} "
    f"trace_final_answers={final_answers}"
)
assert task_started >= 1 and task_complete >= 1 and final_answers >= 1

for path in [
    Path("/generation-evidence/codex-output.log"),
    Path("/generation-evidence/codex-last.txt"),
    Path("/generation-evidence/prompt.txt"),
]:
    data = path.read_bytes()
    assert b"\x00" not in data
    data.decode("utf-8")
    print(f"text_record_utf8_no_nul {path}=true bytes={len(data)}")

print("STAGE1_INTEGRITY_OK")
