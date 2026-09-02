#!/usr/bin/env python3
"""Read-only provenance and supplied-semantics integrity checks."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from pathlib import Path


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_tree(root: Path) -> str:
    digest = hashlib.sha256()
    entries: list[tuple[str, str, Path]] = []
    pending = [root]
    while pending:
        directory = pending.pop()
        for child in os.scandir(directory):
            path = Path(child.path)
            mode = child.stat(follow_symlinks=False).st_mode
            relative = path.relative_to(root).as_posix()
            if stat.S_ISDIR(mode):
                entries.append((relative, "directory", path))
                pending.append(path)
            elif stat.S_ISREG(mode):
                entries.append((relative, "file", path))
            else:
                raise AssertionError(f"linked/unsupported tree entry: {path}")
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


def require_regular(path: Path) -> None:
    mode = path.lstat().st_mode
    assert stat.S_ISREG(mode), f"not a regular non-symlink file: {path}"


audit_input_path = Path("/audit-input.json")
lock_path = Path("/audit-campaign-lock.json")
audit_input = json.loads(audit_input_path.read_text(encoding="utf-8"))
lock = json.loads(lock_path.read_text(encoding="utf-8"))

assert audit_input["record_layout"] == "pipeline-v3"
assert audit_input["semantics_mode"] == "SUPPLIED_SEMANTICS"
assert audit_input["audit_campaign"] == lock
assert sha256_file(lock_path) == audit_input["hashes"]["audit_campaign_lock_sha256"]

required_records = [
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
for path in required_records:
    require_regular(path)

declared_file_hashes = {
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
for path, key in declared_file_hashes.items():
    require_regular(path)
    actual = sha256_file(path)
    assert actual == audit_input["hashes"][key], (path, actual, audit_input["hashes"][key])

generation_result = json.loads(Path("/generation-result.json").read_text())
for relative, expected in generation_result["outputs"]["evidence"].items():
    path = Path("/generation-evidence") / relative
    require_regular(path)
    assert sha256_file(path) == expected

trace_root = Path("/generation-evidence/codex-trace")
trace_files = sorted(trace_root.rglob("*.jsonl"))
assert len(trace_files) == 1
trace_line_count = 0
with trace_files[0].open(encoding="utf-8") as stream:
    for trace_line_count, line in enumerate(stream, start=1):
        json.loads(line)
assert trace_line_count == 384

candidate_semantics = Path("/candidate/reference-semantics")
trusted_semantics = Path("/reference/reference-semantics")
assert candidate_semantics.is_dir() and trusted_semantics.is_dir()

def tree_manifest(root: Path) -> dict[str, tuple[str, str | None]]:
    manifest: dict[str, tuple[str, str | None]] = {}
    for path in sorted(root.rglob("*")):
        mode = path.lstat().st_mode
        relative = path.relative_to(root).as_posix()
        if stat.S_ISDIR(mode):
            manifest[relative] = ("directory", None)
        elif stat.S_ISREG(mode):
            manifest[relative] = ("file", sha256_file(path))
        else:
            manifest[relative] = ("unsupported", None)
    return manifest


candidate_manifest = tree_manifest(candidate_semantics)
trusted_manifest = tree_manifest(trusted_semantics)
assert candidate_manifest == trusted_manifest
assert all(kind != "unsupported" for kind, _ in candidate_manifest.values())

for proof_name in [
    "solution.py",
    "solution.mpy",
    "verification.k",
    "spec.k",
    "prove.sh",
    "PROOF.md",
]:
    require_regular(Path("/candidate") / proof_name)

candidate_tree_hash = sha256_tree(Path("/candidate"))
candidate_semantics_tree_hash = sha256_tree(candidate_semantics)
trusted_semantics_tree_hash = sha256_tree(trusted_semantics)
trace_tree_hash = sha256_tree(trace_root)

assert candidate_tree_hash == generation_result["outputs"]["workspace_sha256"]
assert candidate_semantics_tree_hash == trusted_semantics_tree_hash
assert candidate_semantics_tree_hash == json.loads(Path("/task.json").read_text())["inputs"]["reference_semantics_sha256"]
assert trace_tree_hash == json.loads(Path("/generation-evidence/usage.json").read_text())["source_trace_sha256"]

print("record_layout=pipeline-v3")
print("semantics_mode=SUPPLIED_SEMANTICS")
print("campaign_block_equal=True")
print(f"campaign_lock_sha256={sha256_file(lock_path)}")
print(f"required_record_count={len(required_records)}")
print(f"declared_file_hash_count={len(declared_file_hashes)}")
print("all_declared_file_hashes_match=True")
print(f"trace_file_count={len(trace_files)}")
print(f"trace_json_line_count={trace_line_count}")
print(f"trace_tree_sha256={trace_tree_hash}")
print(f"candidate_tree_sha256_pipeline={candidate_tree_hash}")
print(f"candidate_semantics_entry_count={len(candidate_manifest)}")
print(f"candidate_semantics_tree_sha256_pipeline={candidate_semantics_tree_hash}")
print(f"trusted_semantics_tree_sha256_pipeline={trusted_semantics_tree_hash}")
print("semantics_manifests_equal=True")
print("candidate_required_proof_artifacts_regular=True")
print("RESULT=PASS")
