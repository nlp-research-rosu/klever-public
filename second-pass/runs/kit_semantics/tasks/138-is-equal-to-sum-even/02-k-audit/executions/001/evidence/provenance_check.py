#!/usr/bin/env python3
"""Independent integrity checks for the mounted pipeline-v3 audit inputs."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from collections import Counter
from pathlib import Path


AUDIT = Path("/audit-input.json")
LOCK = Path("/audit-campaign-lock.json")
CANDIDATE = Path("/candidate")
REFERENCE = Path("/reference")
GENERATION = Path("/generation-evidence")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def require_regular(path: Path) -> None:
    metadata = path.lstat()
    assert stat.S_ISREG(metadata.st_mode), f"not a regular file: {path}"
    assert not path.is_symlink(), f"symlink is forbidden: {path}"


def tree_manifest(root: Path) -> list[tuple[str, str, str]]:
    result: list[tuple[str, str, str]] = []
    for path in sorted(root.rglob("*")):
        metadata = path.lstat()
        relative = path.relative_to(root).as_posix()
        if stat.S_ISLNK(metadata.st_mode):
            raise AssertionError(f"symlink is forbidden: {path}")
        if stat.S_ISDIR(metadata.st_mode):
            result.append((relative, "dir", f"{stat.S_IMODE(metadata.st_mode):04o}"))
        elif stat.S_ISREG(metadata.st_mode):
            result.append((relative, "file", sha256(path)))
        else:
            raise AssertionError(f"unexpected entry type: {path}")
    return result


def manifest_digest(entries: list[tuple[str, str, str]]) -> str:
    encoded = json.dumps(entries, separators=(",", ":"), ensure_ascii=True).encode()
    return hashlib.sha256(encoded).hexdigest()


def pipeline_tree_sha256(root: Path) -> str:
    """Reimplement the pipeline-v3 tree digest over paths, types, sizes, and bytes."""
    digest = hashlib.sha256()
    entries: list[tuple[str, str, Path]] = []
    for path in root.rglob("*"):
        metadata = path.lstat()
        relative = path.relative_to(root).as_posix()
        if stat.S_ISDIR(metadata.st_mode):
            entries.append((relative, "directory", path))
        elif stat.S_ISREG(metadata.st_mode):
            entries.append((relative, "file", path))
        else:
            raise AssertionError(f"linked or unsupported tree entry: {path}")
    for relative, kind, path in sorted(entries):
        encoded = relative.encode()
        digest.update(len(encoded).to_bytes(4, "big"))
        digest.update(encoded)
        digest.update(kind.encode() + b"\0")
        if kind == "file":
            content = path.read_bytes()
            digest.update(len(content).to_bytes(8, "big"))
            digest.update(content)
    return digest.hexdigest()


audit = json.loads(AUDIT.read_text())
lock = json.loads(LOCK.read_text())

print(f"record_layout={audit['record_layout']}")
print(f"semantics_mode={audit['semantics_mode']}")
assert audit["record_layout"] == "pipeline-v3"
assert audit["semantics_mode"] == "SUPPLIED_SEMANTICS"
assert lock == audit["audit_campaign"]
assert sha256(LOCK) == audit["hashes"]["audit_campaign_lock_sha256"]
print(f"campaign_block_match=true lock_sha256={sha256(LOCK)}")

required_records = [
    Path("/run.json"),
    Path("/task.json"),
    Path("/generation-result.json"),
    GENERATION / "invocation.json",
    GENERATION / "metrics.json",
    GENERATION / "runtime-metrics.json",
    GENERATION / "usage.json",
    GENERATION / "codex-last.txt",
    GENERATION / "codex-output.log",
    GENERATION / "prompt.txt",
]
for path in required_records:
    require_regular(path)
print(f"required_pipeline_records={len(required_records)} all_regular=true")

hash_pairs = {
    Path("/run.json"): "run_manifest_sha256",
    Path("/task.json"): "task_manifest_sha256",
    Path("/generation-result.json"): "stage1_result_sha256",
    GENERATION / "invocation.json": "stage1_invocation_sha256",
    GENERATION / "metrics.json": "generation_metrics_sha256",
    GENERATION / "runtime-metrics.json": "generation_runtime_metrics_sha256",
    GENERATION / "usage.json": "generation_usage_sha256",
    GENERATION / "codex-last.txt": "generation_codex_last_sha256",
    GENERATION / "codex-output.log": "generation_codex_output_sha256",
    GENERATION / "prompt.txt": "generation_prompt_sha256",
    REFERENCE / "canonical.py": "canonical_sha256",
    REFERENCE / "prompt.py": "trusted_prompt_sha256",
    REFERENCE / "py2mpy.py": "trusted_translator_sha256",
    CANDIDATE / "prompt.py": "candidate_prompt_sha256",
    CANDIDATE / "py2mpy.py": "candidate_translator_sha256",
}
for path, field in hash_pairs.items():
    require_regular(path)
    actual = sha256(path)
    expected = audit["hashes"][field]
    assert actual == expected, f"{path}: {actual} != {expected}"
    print(f"sha256_ok {path} {actual}")

result = json.loads(Path("/generation-result.json").read_text())
invocation = json.loads((GENERATION / "invocation.json").read_text())
run = json.loads(Path("/run.json").read_text())
task = json.loads(Path("/task.json").read_text())
metrics = json.loads((GENERATION / "metrics.json").read_text())
runtime_metrics = json.loads((GENERATION / "runtime-metrics.json").read_text())
usage = json.loads((GENERATION / "usage.json").read_text())
for key, value in task.items():
    assert audit["manifest"][key] == value
assert audit["manifest"]["config"] == audit["config"]
assert run["run_id"] == audit["run_id"]
assert run["config"] == audit["config"]
assert run["condition"] == audit["manifest"]["condition"]
assert result["status"] == invocation["status"] == metrics["status"] == "SUCCEEDED"
assert result["outputs"] == invocation["outputs"]
assert metrics["exit_code"] == invocation["exit_code"] == 0
assert runtime_metrics["final_exit_code"] == runtime_metrics["harness_exit_code"] == 0
assert not metrics["oom_killed"] and not metrics["timeout_marker"]
assert not runtime_metrics["oom_killed"] and not runtime_metrics["timeout_marker"]
assert usage["status"] == "COMPLETE"
print("cross_record_consistency=true status_claim=SUCCEEDED")
for relative, expected in result["outputs"]["evidence"].items():
    path = GENERATION / relative
    require_regular(path)
    assert sha256(path) == expected
for relative, expected in invocation["outputs"]["evidence"].items():
    path = GENERATION / relative
    require_regular(path)
    assert sha256(path) == expected
print("generation_result_evidence_hashes_match=true")
print("invocation_evidence_hashes_match=true")

candidate_pipeline_digest = pipeline_tree_sha256(CANDIDATE)
semantics_pipeline_digest = pipeline_tree_sha256(REFERENCE / "reference-semantics")
trace_pipeline_digest = pipeline_tree_sha256(GENERATION / "codex-trace")
assert candidate_pipeline_digest == result["outputs"]["workspace_sha256"]
assert candidate_pipeline_digest == invocation["outputs"]["workspace_sha256"]
assert semantics_pipeline_digest == task["inputs"]["reference_semantics_sha256"]
assert (
    semantics_pipeline_digest
    == audit["hashes"]["trusted_reference_semantics_manifest_sha256"]
)
assert trace_pipeline_digest == usage["source_trace_sha256"]
print(f"pipeline_tree_sha256 /candidate {candidate_pipeline_digest}")
print(
    "pipeline_tree_sha256 /reference/reference-semantics "
    f"{semantics_pipeline_digest}"
)
print(f"pipeline_tree_sha256 /generation-evidence/codex-trace {trace_pipeline_digest}")
print(
    "launcher_additional_candidate_tree_hash="
    f"{audit['hashes']['candidate_tree_sha256']}"
)

trace_files = sorted((GENERATION / "codex-trace").rglob("*"))
assert trace_files, "empty trace tree"
trace_records = 0
trace_types: Counter[tuple[str | None, str | None]] = Counter()
for path in trace_files:
    metadata = path.lstat()
    assert not stat.S_ISLNK(metadata.st_mode)
    if stat.S_ISDIR(metadata.st_mode):
        continue
    require_regular(path)
    assert path.suffix == ".jsonl"
    with path.open() as stream:
        for line_number, line in enumerate(stream, 1):
            item = json.loads(line)
            payload = item.get("payload") or {}
            trace_types[(item.get("type"), payload.get("type"))] += 1
            trace_records += 1
print(f"structured_trace_files={sum(p.is_file() for p in trace_files)}")
print(f"structured_trace_records_parsed={trace_records}")
for key, count in sorted(trace_types.items(), key=lambda pair: (-pair[1], str(pair[0]))):
    print(f"trace_event_count {key} {count}")

candidate_semantics = tree_manifest(CANDIDATE / "reference-semantics")
trusted_semantics = tree_manifest(REFERENCE / "reference-semantics")
assert candidate_semantics == trusted_semantics
print(f"semantics_entries={len(trusted_semantics)} exact_manifest_match=true")
print(f"independent_semantics_manifest_sha256={manifest_digest(trusted_semantics)}")
for relative, kind, value in trusted_semantics:
    print(f"semantics_entry {kind} {relative} {value}")

for candidate_path, trusted_path in [
    (CANDIDATE / "prompt.py", REFERENCE / "prompt.py"),
    (CANDIDATE / "py2mpy.py", REFERENCE / "py2mpy.py"),
]:
    assert candidate_path.read_bytes() == trusted_path.read_bytes()
    print(f"byte_identity=true {candidate_path} {trusted_path}")

required_candidate = [
    "solution.py",
    "solution.mpy",
    "verification.k",
    "spec.k",
    "prove.sh",
    "PROOF.md",
]
for relative in required_candidate:
    require_regular(CANDIDATE / relative)
print(f"required_candidate_artifacts={len(required_candidate)} all_regular=true")

all_candidate_symlinks = [
    path.as_posix()
    for path in CANDIDATE.rglob("*")
    if path.is_symlink()
]
assert not all_candidate_symlinks
print("candidate_symlinks=0")
candidate_independent_manifest = tree_manifest(CANDIDATE)
print(f"candidate_tree_entries={len(candidate_independent_manifest)}")
print(
    "independent_candidate_manifest_sha256="
    f"{manifest_digest(candidate_independent_manifest)}"
)
print("PROVENANCE_CHECK=PASS")
