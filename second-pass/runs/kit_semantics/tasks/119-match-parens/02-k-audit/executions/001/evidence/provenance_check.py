#!/usr/bin/env python3
"""Independent integrity checks for the mounted audit inputs."""

from __future__ import annotations

import collections
import hashlib
import json
import os
import stat
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as stream:
        return json.load(stream)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def stable_tree_hash(root: Path) -> str:
    """Reviewer-defined tree digest over entry type, relative path, and bytes."""
    digest = hashlib.sha256()
    for path in sorted(root.rglob("*"), key=lambda item: item.relative_to(root).as_posix()):
        relative = path.relative_to(root).as_posix().encode()
        mode = path.lstat().st_mode
        if stat.S_ISDIR(mode):
            kind = b"d"
            payload = b""
        elif stat.S_ISREG(mode):
            kind = b"f"
            payload = path.read_bytes()
        elif stat.S_ISLNK(mode):
            kind = b"l"
            payload = os.readlink(path).encode()
        else:
            kind = b"o"
            payload = b""
        digest.update(kind + b"\0" + relative + b"\0" + payload + b"\0")
    return digest.hexdigest()


def compare_trees(left: Path, right: Path):
    left_entries = {
        path.relative_to(left).as_posix(): path for path in left.rglob("*")
    }
    right_entries = {
        path.relative_to(right).as_posix(): path for path in right.rglob("*")
    }
    assert left_entries.keys() == right_entries.keys()
    for relative in sorted(left_entries):
        left_path = left_entries[relative]
        right_path = right_entries[relative]
        left_mode = left_path.lstat().st_mode
        right_mode = right_path.lstat().st_mode
        assert stat.S_IFMT(left_mode) == stat.S_IFMT(right_mode), relative
        assert not stat.S_ISLNK(left_mode), relative
        if stat.S_ISREG(left_mode):
            assert left_path.read_bytes() == right_path.read_bytes(), relative


record = load_json(AUDIT_INPUT)
assert record["record_layout"] == "pipeline-v3"
assert record["semantics_mode"] == "SUPPLIED_SEMANTICS"
paths = {name: Path(value) for name, value in record["container_paths"].items()}

required = [
    AUDIT_INPUT,
    paths["audit_campaign_lock"],
    paths["candidate"],
    paths["canonical"],
    paths["generation_last"],
    paths["generation_manifest"],
    paths["generation_metrics"],
    paths["generation_output"],
    paths["generation_trace"],
    paths["run_manifest"],
    paths["stage1_result"],
    paths["task_manifest"],
    paths["translator"],
    paths["trusted_prompt"],
    Path("/generation-evidence/runtime-metrics.json"),
    Path("/generation-evidence/usage.json"),
    Path("/generation-evidence/prompt.txt"),
    Path("/reference/reference-semantics"),
]
for path in required:
    assert path.exists(), path
    assert os.access(path, os.R_OK), path
    assert not path.is_symlink(), path

lock = load_json(paths["audit_campaign_lock"])
assert lock == record["audit_campaign"]
assert sha256(paths["audit_campaign_lock"]) == record["hashes"]["audit_campaign_lock_sha256"]

hash_checks = {
    paths["canonical"]: "canonical_sha256",
    paths["trusted_prompt"]: "trusted_prompt_sha256",
    paths["translator"]: "trusted_translator_sha256",
    paths["run_manifest"]: "run_manifest_sha256",
    paths["task_manifest"]: "task_manifest_sha256",
    paths["stage1_result"]: "stage1_result_sha256",
    paths["generation_manifest"]: "stage1_invocation_sha256",
    paths["generation_metrics"]: "generation_metrics_sha256",
    paths["generation_last"]: "generation_codex_last_sha256",
    paths["generation_output"]: "generation_codex_output_sha256",
    Path("/generation-evidence/runtime-metrics.json"): "generation_runtime_metrics_sha256",
    Path("/generation-evidence/usage.json"): "generation_usage_sha256",
    Path("/generation-evidence/prompt.txt"): "generation_prompt_sha256",
}
for path, key in hash_checks.items():
    actual = sha256(path)
    expected = record["hashes"][key]
    assert actual == expected, (path, actual, expected)

run = load_json(paths["run_manifest"])
task = load_json(paths["task_manifest"])
result = load_json(paths["stage1_result"])
invocation = load_json(paths["generation_manifest"])
metrics = load_json(paths["generation_metrics"])
runtime_metrics = load_json(Path("/generation-evidence/runtime-metrics.json"))
usage = load_json(Path("/generation-evidence/usage.json"))
assert run["schema_version"] == 3
assert run["config"] == record["config"]
assert record["problem_id"] in run["tasks"]
for key in ("condition", "current_stage", "inputs", "problem_id", "schema_version"):
    assert task[key] == record["manifest"][key], key
assert result["schema_version"] == 3 and result["status"] == "SUCCEEDED"
assert invocation["schema_version"] == 3 and invocation["status"] == "SUCCEEDED"
assert metrics["status"] == "SUCCEEDED" and metrics["exit_code"] == 0
assert runtime_metrics["final_exit_code"] == 0 and not runtime_metrics["oom_killed"]
assert usage["status"] == "COMPLETE"
for relative, expected in result["outputs"]["evidence"].items():
    evidence_path = Path("/generation-evidence") / relative
    assert sha256(evidence_path) == expected, evidence_path

candidate = paths["candidate"]
assert (candidate / "prompt.py").read_bytes() == paths["trusted_prompt"].read_bytes()
assert (candidate / "py2mpy.py").read_bytes() == paths["translator"].read_bytes()
compare_trees(candidate / "reference-semantics", Path("/reference/reference-semantics"))

trace_entries = sorted(paths["generation_trace"].rglob("*"))
assert trace_entries and all(not path.is_symlink() for path in trace_entries)
trace_files = [path for path in trace_entries if path.is_file()]
assert trace_files
trace_counts: collections.Counter[str] = collections.Counter()
payload_counts: collections.Counter[str] = collections.Counter()
trace_lines = 0
for trace_path in trace_files:
    with trace_path.open("r", encoding="utf-8") as stream:
        for line in stream:
            item = json.loads(line)
            trace_lines += 1
            trace_counts[item["type"]] += 1
            payload = item.get("payload")
            if isinstance(payload, dict) and "type" in payload:
                payload_counts[str(payload["type"])] += 1

print("record_layout: pipeline-v3")
print("semantics_mode: SUPPLIED_SEMANTICS")
print(f"required_records: {len(required)} present/readable")
print(f"campaign_lock: exact block match, sha256={sha256(paths['audit_campaign_lock'])}")
print(f"recorded_file_hashes: {len(hash_checks)} matched")
print("pipeline_records: schema/config/task/status/output-map checks passed")
print("candidate_prompt: byte-identical to trusted prompt")
print("candidate_translator: byte-identical to trusted translator")
print("candidate_reference_semantics: exact entry/type/byte match, no symlinks")
print(
    "reviewer_tree_sha256(candidate/reference-semantics): "
    f"{stable_tree_hash(candidate / 'reference-semantics')}"
)
print(
    "reviewer_tree_sha256(reference/reference-semantics): "
    f"{stable_tree_hash(Path('/reference/reference-semantics'))}"
)
print(f"reviewer_tree_sha256(candidate): {stable_tree_hash(candidate)}")
print(f"structured_trace: {len(trace_files)} file(s), {trace_lines} valid JSON events")
print("trace_top_level_types:", dict(sorted(trace_counts.items())))
print("trace_payload_types:", dict(sorted(payload_counts.items())))
print("PROVENANCE CHECK: PASS")
