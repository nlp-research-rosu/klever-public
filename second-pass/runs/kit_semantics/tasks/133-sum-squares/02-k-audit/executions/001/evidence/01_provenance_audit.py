#!/usr/bin/env python3
"""Independent provenance and supplied-semantics integrity checks."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from collections import Counter
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")
CAMPAIGN_LOCK = Path("/audit-campaign-lock.json")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1024 * 1024):
            h.update(chunk)
    return h.hexdigest()


def tree_records(root: Path) -> dict[str, tuple[str, str | None]]:
    records: dict[str, tuple[str, str | None]] = {}
    for base, dirs, files in os.walk(root, topdown=True, followlinks=False):
        base_path = Path(base)
        for name in sorted(dirs + files):
            path = base_path / name
            rel = path.relative_to(root).as_posix()
            mode = path.lstat().st_mode
            if stat.S_ISLNK(mode):
                records[rel] = ("symlink", os.readlink(path))
            elif stat.S_ISDIR(mode):
                records[rel] = ("directory", None)
            elif stat.S_ISREG(mode):
                records[rel] = ("file", sha256(path))
            else:
                records[rel] = ("other", oct(mode))
    return records


def transparent_tree_digest(records: dict[str, tuple[str, str | None]]) -> str:
    h = hashlib.sha256()
    for rel, (kind, value) in sorted(records.items()):
        h.update(kind.encode())
        h.update(b"\0")
        h.update(rel.encode())
        h.update(b"\0")
        h.update((value or "").encode())
        h.update(b"\n")
    return h.hexdigest()


def require_regular(path: Path) -> None:
    mode = path.lstat().st_mode
    assert stat.S_ISREG(mode), f"not a regular file: {path}"
    with path.open("rb") as stream:
        stream.read(1)


audit = json.loads(AUDIT_INPUT.read_text())
lock = json.loads(CAMPAIGN_LOCK.read_text())
print(f"record_layout={audit['record_layout']}")
print(f"semantics_mode={audit['semantics_mode']}")
print(f"problem_id={audit['problem_id']}")
assert audit["record_layout"] == "pipeline-v3"
assert audit["semantics_mode"] == "SUPPLIED_SEMANTICS"
assert audit["problem_id"] == "133-sum-squares"

lock_hash = sha256(CAMPAIGN_LOCK)
print(f"audit_campaign_lock_sha256 actual={lock_hash}")
print(
    "audit_campaign_lock_sha256 recorded="
    + audit["hashes"]["audit_campaign_lock_sha256"]
)
assert lock_hash == audit["hashes"]["audit_campaign_lock_sha256"]
assert lock == audit["audit_campaign"]
print("campaign_block_matches_lock=true")

container_paths = audit["container_paths"]
required_regular = [
    AUDIT_INPUT,
    CAMPAIGN_LOCK,
    Path(container_paths["run_manifest"]),
    Path(container_paths["task_manifest"]),
    Path(container_paths["stage1_result"]),
    Path(container_paths["generation_manifest"]),
    Path(container_paths["generation_metrics"]),
    Path("/generation-evidence/runtime-metrics.json"),
    Path("/generation-evidence/usage.json"),
    Path(container_paths["generation_last"]),
    Path(container_paths["generation_output"]),
    Path("/generation-evidence/prompt.txt"),
    Path(container_paths["canonical"]),
    Path(container_paths["trusted_prompt"]),
    Path(container_paths["translator"]),
]
for path in required_regular:
    require_regular(path)

required_dirs = [
    Path(container_paths["candidate"]),
    Path(container_paths["generation_root"]),
    Path(container_paths["generation_trace"]),
    Path("/reference/reference-semantics"),
]
for path in required_dirs:
    assert path.is_dir() and not path.is_symlink(), f"bad required directory: {path}"
print(
    f"required_regular_records={len(required_regular)} "
    f"required_directories={len(required_dirs)} all_readable=true"
)

hash_bindings = {
    CAMPAIGN_LOCK: "audit_campaign_lock_sha256",
    Path("/run.json"): "run_manifest_sha256",
    Path("/task.json"): "task_manifest_sha256",
    Path("/generation-result.json"): "stage1_result_sha256",
    Path("/generation-evidence/invocation.json"): "stage1_invocation_sha256",
    Path("/generation-evidence/metrics.json"): "generation_metrics_sha256",
    Path("/generation-evidence/runtime-metrics.json"):
        "generation_runtime_metrics_sha256",
    Path("/generation-evidence/usage.json"): "generation_usage_sha256",
    Path("/generation-evidence/codex-last.txt"): "generation_codex_last_sha256",
    Path("/generation-evidence/codex-output.log"):
        "generation_codex_output_sha256",
    Path("/generation-evidence/prompt.txt"): "generation_prompt_sha256",
    Path("/reference/canonical.py"): "canonical_sha256",
    Path("/reference/prompt.py"): "trusted_prompt_sha256",
    Path("/reference/py2mpy.py"): "trusted_translator_sha256",
    Path("/candidate/prompt.py"): "candidate_prompt_sha256",
    Path("/candidate/py2mpy.py"): "candidate_translator_sha256",
}
for path, key in hash_bindings.items():
    actual = sha256(path)
    expected = audit["hashes"][key]
    print(f"hash {path} actual={actual} expected={expected} match={actual == expected}")
    assert actual == expected

run = json.loads(Path("/run.json").read_text())
task = json.loads(Path("/task.json").read_text())
result = json.loads(Path("/generation-result.json").read_text())
invocation = json.loads(Path("/generation-evidence/invocation.json").read_text())
metrics = json.loads(Path("/generation-evidence/metrics.json").read_text())
runtime_metrics = json.loads(
    Path("/generation-evidence/runtime-metrics.json").read_text()
)
usage = json.loads(Path("/generation-evidence/usage.json").read_text())

for key, value in task.items():
    assert audit["manifest"][key] == value
assert audit["manifest"]["config"] == audit["config"] == run["config"]
assert task["condition"]["name"] == audit["condition"]
assert run["run_id"] == audit["run_id"]
assert run["condition"] == task["condition"]
assert result["status"] == "SUCCEEDED"
assert invocation["status"] == "SUCCEEDED"
assert metrics["status"] == "SUCCEEDED"
assert runtime_metrics["final_exit_code"] == 0
assert usage["status"] == "COMPLETE"
print("pipeline_manifest_cross_checks=true")

generation_hashes = result["outputs"]["evidence"]
for rel, expected in sorted(generation_hashes.items()):
    path = Path("/generation-evidence") / rel
    assert path.exists(), f"missing generation evidence: {path}"
    actual = sha256(path)
    print(f"result_evidence {rel} actual={actual} expected={expected} match={actual == expected}")
    assert actual == expected

trace_root = Path(container_paths["generation_trace"])
trace_files = sorted(trace_root.rglob("*"))
trace_non_dirs = [path for path in trace_files if not path.is_dir()]
assert trace_non_dirs, "structured trace is empty"
assert all(path.is_file() and not path.is_symlink() for path in trace_non_dirs)
trace_expected = {
    rel: expected
    for rel, expected in generation_hashes.items()
    if rel.startswith("codex-trace/")
}
assert len(trace_non_dirs) == len(trace_expected)
for path in trace_non_dirs:
    rel = path.relative_to(Path("/generation-evidence")).as_posix()
    assert rel in trace_expected
    assert sha256(path) == trace_expected[rel]
print(f"structured_trace_files={len(trace_non_dirs)} hashes_match=true")

trace_line_count = 0
trace_top_types: Counter[str | None] = Counter()
trace_payload_types: Counter[tuple[str | None, str | None]] = Counter()
trace_calls: list[tuple[int, str, str]] = []
for path in trace_non_dirs:
    with path.open(encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, 1):
            item = json.loads(line)
            trace_line_count += 1
            top_type = item.get("type")
            payload = item.get("payload") or {}
            payload_type = payload.get("type") if isinstance(payload, dict) else None
            trace_top_types[top_type] += 1
            trace_payload_types[(top_type, payload_type)] += 1
            if (
                top_type == "response_item"
                and payload_type in {"function_call", "custom_tool_call"}
            ):
                arguments = payload.get("arguments", payload.get("input", ""))
                trace_calls.append(
                    (line_number, str(payload.get("name")), str(arguments))
                )
print(f"structured_trace_json_lines={trace_line_count} all_json_valid=true")
print(f"structured_trace_top_types={dict(trace_top_types)}")
print(f"structured_trace_payload_types={dict(trace_payload_types)}")
print(f"structured_trace_tool_calls={len(trace_calls)}")

for path in [
    Path("/generation-evidence/codex-output.log"),
    Path("/generation-evidence/codex-last.txt"),
    Path("/generation-evidence/prompt.txt"),
]:
    data = path.read_bytes()
    line_count = data.count(b"\n")
    print(f"read_full_record {path} bytes={len(data)} lines={line_count}")

candidate_prompt = Path("/candidate/prompt.py").read_bytes()
trusted_prompt = Path("/reference/prompt.py").read_bytes()
candidate_translator = Path("/candidate/py2mpy.py").read_bytes()
trusted_translator = Path("/reference/py2mpy.py").read_bytes()
assert candidate_prompt == trusted_prompt
assert candidate_translator == trusted_translator
print("candidate_prompt_byte_identity=true")
print("candidate_translator_byte_identity=true")

trusted_semantics = tree_records(Path("/reference/reference-semantics"))
candidate_semantics = tree_records(Path("/candidate/reference-semantics"))
assert trusted_semantics == candidate_semantics
assert all(kind in {"directory", "file"} for kind, _ in trusted_semantics.values())
print(
    "supplied_semantics_recursive_identity=true "
    f"entries={len(trusted_semantics)} "
    f"files={sum(kind == 'file' for kind, _ in trusted_semantics.values())}"
)
print(
    "trusted_semantics_reviewer_tree_sha256="
    + transparent_tree_digest(trusted_semantics)
)
print(
    "candidate_semantics_reviewer_tree_sha256="
    + transparent_tree_digest(candidate_semantics)
)

for root in [
    Path("/candidate"),
    Path("/reference"),
    Path("/generation-evidence"),
]:
    records = tree_records(root)
    links = [rel for rel, (kind, _) in records.items() if kind == "symlink"]
    others = [rel for rel, (kind, _) in records.items() if kind == "other"]
    print(f"mount_types {root} symlinks={links} other_special_entries={others}")
    assert not links and not others

deliverables = [
    "solution.py",
    "solution.mpy",
    "verification.k",
    "spec.k",
    "prove.sh",
    "PROOF.md",
]
for name in deliverables:
    require_regular(Path("/candidate") / name)
print("required_candidate_proof_artifacts_present=true")
print("PROVENANCE_AUDIT_OK")
