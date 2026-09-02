#!/usr/bin/env python3
"""Independent integrity checks for the mounted pipeline-v3 audit inputs."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from collections import Counter
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def kind(path: Path) -> str:
    mode = path.lstat().st_mode
    if stat.S_ISREG(mode):
        return "file"
    if stat.S_ISDIR(mode):
        return "dir"
    if stat.S_ISLNK(mode):
        return "symlink"
    return "other"


def require_regular(path: Path) -> None:
    assert path.exists(), f"missing: {path}"
    assert kind(path) == "file", f"not a regular file: {path} ({kind(path)})"
    assert os.access(path, os.R_OK), f"unreadable: {path}"


def walk_manifest(root: Path) -> dict[str, tuple[str, str | None]]:
    result: dict[str, tuple[str, str | None]] = {}
    for current, dirs, files in os.walk(root, topdown=True, followlinks=False):
        current_path = Path(current)
        for name in sorted(dirs + files):
            path = current_path / name
            rel = path.relative_to(root).as_posix()
            entry_kind = kind(path)
            digest = sha256(path) if entry_kind == "file" else None
            result[rel] = (entry_kind, digest)
    return result


with AUDIT_INPUT.open(encoding="utf-8") as stream:
    audit = json.load(stream)

assert audit["record_layout"] == "pipeline-v3"
assert audit["semantics_mode"] == "SUPPLIED_SEMANTICS"
paths = audit["container_paths"]

required_files = [
    Path("/audit-input.json"),
    Path(paths["audit_campaign_lock"]),
    Path(paths["run_manifest"]),
    Path(paths["task_manifest"]),
    Path(paths["stage1_result"]),
    Path(paths["generation_manifest"]),
    Path(paths["generation_metrics"]),
    Path("/generation-evidence/runtime-metrics.json"),
    Path("/generation-evidence/usage.json"),
    Path(paths["generation_last"]),
    Path(paths["generation_output"]),
    Path("/generation-evidence/prompt.txt"),
    Path(paths["canonical"]),
    Path(paths["trusted_prompt"]),
    Path(paths["translator"]),
]
for required in required_files:
    require_regular(required)

required_dirs = [
    Path(paths["candidate"]),
    Path(paths["generation_root"]),
    Path(paths["generation_trace"]),
    Path("/reference/reference-semantics"),
    Path("/candidate/reference-semantics"),
]
for required in required_dirs:
    assert required.exists(), f"missing: {required}"
    assert kind(required) == "dir", f"not a real directory: {required} ({kind(required)})"
    assert os.access(required, os.R_OK), f"unreadable: {required}"

with Path(paths["audit_campaign_lock"]).open(encoding="utf-8") as stream:
    campaign_lock = json.load(stream)
assert campaign_lock == audit["audit_campaign"], "campaign lock JSON differs from audit campaign block"

expected_hashes = audit["hashes"]
direct_hash_checks = {
    "audit_campaign_lock_sha256": Path(paths["audit_campaign_lock"]),
    "canonical_sha256": Path(paths["canonical"]),
    "run_manifest_sha256": Path(paths["run_manifest"]),
    "task_manifest_sha256": Path(paths["task_manifest"]),
    "manifest_sha256": Path(paths["task_manifest"]),
    "stage1_invocation_sha256": Path(paths["generation_manifest"]),
    "stage1_result_sha256": Path(paths["stage1_result"]),
    "generation_metrics_sha256": Path(paths["generation_metrics"]),
    "generation_runtime_metrics_sha256": Path("/generation-evidence/runtime-metrics.json"),
    "generation_usage_sha256": Path("/generation-evidence/usage.json"),
    "generation_codex_last_sha256": Path(paths["generation_last"]),
    "generation_codex_output_sha256": Path(paths["generation_output"]),
    "generation_prompt_sha256": Path("/generation-evidence/prompt.txt"),
    "trusted_prompt_sha256": Path(paths["trusted_prompt"]),
    "candidate_prompt_sha256": Path("/candidate/prompt.py"),
    "trusted_translator_sha256": Path(paths["translator"]),
    "candidate_translator_sha256": Path("/candidate/py2mpy.py"),
}
for key, path in direct_hash_checks.items():
    actual = sha256(path)
    assert actual == expected_hashes[key], f"{key}: {actual} != {expected_hashes[key]}"
    print(f"HASH_OK {key} {actual} {path}")

assert Path("/candidate/prompt.py").read_bytes() == Path(paths["trusted_prompt"]).read_bytes()
assert Path("/candidate/py2mpy.py").read_bytes() == Path(paths["translator"]).read_bytes()
print("BYTE_IDENTITY_OK candidate prompt == trusted prompt")
print("BYTE_IDENTITY_OK candidate translator == trusted translator")

candidate_semantics = walk_manifest(Path("/candidate/reference-semantics"))
trusted_semantics = walk_manifest(Path("/reference/reference-semantics"))
assert all(entry_kind != "symlink" for entry_kind, _ in candidate_semantics.values())
assert all(entry_kind != "symlink" for entry_kind, _ in trusted_semantics.values())
assert candidate_semantics == trusted_semantics, "candidate and trusted semantics trees differ"
print(f"SEMANTICS_TREE_IDENTITY_OK entries={len(candidate_semantics)} symlinks=0")

candidate_critical = [
    Path("/candidate/solution.py"),
    Path("/candidate/solution.mpy"),
    Path("/candidate/spec.k"),
    Path("/candidate/verification.k"),
]
for required in candidate_critical:
    require_regular(required)
    print(f"CANDIDATE_PROOF_SOURCE_OK {required} sha256={sha256(required)}")

trace_root = Path(paths["generation_trace"])
trace_manifest = walk_manifest(trace_root)
assert trace_manifest, "structured trace is empty"
assert all(entry_kind != "symlink" for entry_kind, _ in trace_manifest.values())
trace_files = [trace_root / rel for rel, (entry_kind, _) in trace_manifest.items() if entry_kind == "file"]
assert trace_files, "structured trace has no regular files"

event_types: Counter[str] = Counter()
trace_lines = 0
for trace_file in trace_files:
    with trace_file.open(encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, 1):
            record = json.loads(line)
            trace_lines += 1
            event_types[str(record.get("type", "<missing>"))] += 1
print(
    f"STRUCTURED_TRACE_OK files={len(trace_files)} json_records={trace_lines} "
    f"event_types={dict(sorted(event_types.items()))}"
)

with Path(paths["stage1_result"]).open(encoding="utf-8") as stream:
    stage1_result = json.load(stream)
recorded_outputs = stage1_result["outputs"]["evidence"]
for rel, expected in sorted(recorded_outputs.items()):
    output_path = Path(paths["generation_root"]) / rel
    require_regular(output_path)
    actual = sha256(output_path)
    assert actual == expected, f"generation-result hash mismatch for {rel}: {actual} != {expected}"
    print(f"GENERATION_OUTPUT_HASH_OK {actual} {output_path}")

print("CAMPAIGN_LOCK_MATCH_OK")
print("PIPELINE_V3_REQUIRED_RECORDS_OK")
print("PROVENANCE_CHECK_PASS")
