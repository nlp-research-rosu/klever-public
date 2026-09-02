#!/usr/bin/env python3
"""Independent stage-1 provenance and mounted-input integrity checks."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from collections import Counter
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")
TRACE = Path(
    "/generation-evidence/codex-trace/2026/07/29/"
    "rollout-2026-07-29T08-50-54-019fae24-7cdb-7a70-856a-b202f3a61f1e.jsonl"
)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def manifest_tree_hash(root: Path) -> str:
    """Reimplement the pipeline-v3 tree digest without importing harness code."""
    if root.is_symlink() or not root.is_dir():
        raise ValueError(f"tree root is not a real directory: {root}")
    entries: list[tuple[str, str, Path]] = []
    pending = [root]
    while pending:
        directory = pending.pop()
        for entry in os.scandir(directory):
            path = Path(entry.path)
            mode = entry.stat(follow_symlinks=False).st_mode
            relative = path.relative_to(root).as_posix()
            if stat.S_ISDIR(mode):
                entries.append((relative, "directory", path))
                pending.append(path)
            elif stat.S_ISREG(mode):
                entries.append((relative, "file", path))
            else:
                raise ValueError(f"linked or unsupported tree entry: {path}")
    digest = hashlib.sha256()
    for relative, kind, path in sorted(entries):
        encoded = relative.encode()
        digest.update(len(encoded).to_bytes(4, "big"))
        digest.update(encoded)
        digest.update(kind.encode() + b"\0")
        if kind == "file":
            size = path.stat(follow_symlinks=False).st_size
            digest.update(size.to_bytes(8, "big"))
            with path.open("rb") as stream:
                for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                    digest.update(chunk)
    return digest.hexdigest()


def regular_tree(root: Path) -> dict[str, tuple[str, str | None]]:
    result: dict[str, tuple[str, str | None]] = {}
    pending = [root]
    while pending:
        directory = pending.pop()
        for entry in os.scandir(directory):
            path = Path(entry.path)
            mode = entry.stat(follow_symlinks=False).st_mode
            relative = path.relative_to(root).as_posix()
            if stat.S_ISDIR(mode):
                result[relative] = ("directory", None)
                pending.append(path)
            elif stat.S_ISREG(mode):
                result[relative] = ("file", sha256_file(path))
            else:
                result[relative] = ("unsupported", None)
    return result


audit_input = json.loads(AUDIT_INPUT.read_text(encoding="utf-8"))
record_layout = audit_input["record_layout"]
assert record_layout == "pipeline-v3"
assert audit_input["semantics_mode"] == "SUPPLIED_SEMANTICS"
assert audit_input["mount_reference_semantics"] is True

required_files = [
    Path("/audit-input.json"),
    Path("/audit-campaign-lock.json"),
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
    Path("/reference/canonical.py"),
    Path("/reference/prompt.py"),
    Path("/reference/py2mpy.py"),
]
required_directories = [
    Path("/candidate"),
    Path("/generation-evidence"),
    Path("/generation-evidence/codex-trace"),
    Path("/reference/reference-semantics"),
]

print(f"record_layout={record_layout}")
for path in required_files:
    ok = path.is_file() and not path.is_symlink() and os.access(path, os.R_OK)
    print(f"required_file {path} ok={ok}")
    assert ok
for path in required_directories:
    ok = path.is_dir() and not path.is_symlink() and os.access(path, os.R_OK)
    print(f"required_directory {path} ok={ok}")
    assert ok

campaign = json.loads(Path("/audit-campaign-lock.json").read_text(encoding="utf-8"))
print(f"campaign_object_equal={campaign == audit_input['audit_campaign']}")
assert campaign == audit_input["audit_campaign"]

hash_targets = {
    "audit_campaign_lock_sha256": Path("/audit-campaign-lock.json"),
    "canonical_sha256": Path("/reference/canonical.py"),
    "trusted_prompt_sha256": Path("/reference/prompt.py"),
    "trusted_translator_sha256": Path("/reference/py2mpy.py"),
    "candidate_prompt_sha256": Path("/candidate/prompt.py"),
    "candidate_translator_sha256": Path("/candidate/py2mpy.py"),
    "run_manifest_sha256": Path("/run.json"),
    "task_manifest_sha256": Path("/task.json"),
    "stage1_result_sha256": Path("/generation-result.json"),
    "stage1_invocation_sha256": Path("/generation-evidence/invocation.json"),
    "generation_metrics_sha256": Path("/generation-evidence/metrics.json"),
    "generation_runtime_metrics_sha256": Path(
        "/generation-evidence/runtime-metrics.json"
    ),
    "generation_usage_sha256": Path("/generation-evidence/usage.json"),
    "generation_codex_last_sha256": Path("/generation-evidence/codex-last.txt"),
    "generation_codex_output_sha256": Path("/generation-evidence/codex-output.log"),
    "generation_prompt_sha256": Path("/generation-evidence/prompt.txt"),
}
for key, path in hash_targets.items():
    actual = sha256_file(path)
    expected = audit_input["hashes"][key]
    print(f"sha256 {key} expected={expected} actual={actual} match={actual == expected}")
    assert actual == expected

assert Path("/candidate/prompt.py").read_bytes() == Path(
    "/reference/prompt.py"
).read_bytes()
assert Path("/candidate/py2mpy.py").read_bytes() == Path(
    "/reference/py2mpy.py"
).read_bytes()
print("candidate_prompt_byte_identity=True")
print("candidate_translator_byte_identity=True")

candidate_semantics = regular_tree(Path("/candidate/reference-semantics"))
trusted_semantics = regular_tree(Path("/reference/reference-semantics"))
print(f"semantics_entry_count={len(trusted_semantics)}")
print(f"semantics_tree_exact={candidate_semantics == trusted_semantics}")
assert candidate_semantics == trusted_semantics
assert all(kind != "unsupported" for kind, _ in candidate_semantics.values())

candidate_manifest_hash = manifest_tree_hash(Path("/candidate"))
semantics_manifest_hash = manifest_tree_hash(Path("/reference/reference-semantics"))
trace_manifest_hash = manifest_tree_hash(Path("/generation-evidence/codex-trace"))
result = json.loads(Path("/generation-result.json").read_text(encoding="utf-8"))
invocation = json.loads(
    Path("/generation-evidence/invocation.json").read_text(encoding="utf-8")
)
print(f"candidate_manifest_tree_sha256={candidate_manifest_hash}")
print(
    "candidate_matches_generation_result="
    f"{candidate_manifest_hash == result['outputs']['workspace_sha256']}"
)
print(
    "candidate_matches_invocation_output="
    f"{candidate_manifest_hash == invocation['outputs']['workspace_sha256']}"
)
print(f"semantics_manifest_tree_sha256={semantics_manifest_hash}")
print(
    "semantics_matches_recorded_manifest="
    f"{semantics_manifest_hash == audit_input['hashes']['trusted_reference_semantics_manifest_sha256']}"
)
print(f"trace_manifest_tree_sha256={trace_manifest_hash}")
print(
    "trace_matches_usage_source="
    f"{trace_manifest_hash == json.loads(Path('/generation-evidence/usage.json').read_text())['source_trace_sha256']}"
)

trace_file_hash = sha256_file(TRACE)
trace_expected = result["outputs"]["evidence"][str(TRACE.relative_to("/generation-evidence"))]
print(
    f"trace_file_sha256 expected={trace_expected} actual={trace_file_hash} "
    f"match={trace_file_hash == trace_expected}"
)
assert trace_file_hash == trace_expected

outer_types: Counter[str] = Counter()
payload_types: Counter[str] = Counter()
trace_lines = 0
with TRACE.open(encoding="utf-8") as stream:
    for trace_lines, line in enumerate(stream, 1):
        item = json.loads(line)
        outer_types[item.get("type", "<none>")] += 1
        payload = item.get("payload")
        if isinstance(payload, dict):
            payload_types[payload.get("type", "<none>")] += 1
print(f"trace_json_lines={trace_lines}")
print(f"trace_outer_types={dict(sorted(outer_types.items()))}")
print(f"trace_payload_types={dict(sorted(payload_types.items()))}")
assert trace_lines == 201

print("INTEGRITY_STATUS=PASS")
