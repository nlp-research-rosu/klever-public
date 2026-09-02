#!/usr/bin/env python3
"""Independent integrity checks for the mounted audit inputs."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")
CAMPAIGN_LOCK = Path("/audit-campaign-lock.json")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_tree(root: Path) -> str:
    """Pipeline-v3 tree digest, independently reimplemented."""
    if root.is_symlink() or not root.is_dir():
        raise RuntimeError(f"not a real directory: {root}")
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
                raise RuntimeError(f"linked or unsupported tree entry: {path}")
    digest = hashlib.sha256()
    for relative, kind, path in sorted(entries):
        encoded = relative.encode()
        digest.update(len(encoded).to_bytes(4, "big"))
        digest.update(encoded)
        digest.update(kind.encode() + b"\0")
        if kind == "file":
            digest.update(path.stat(follow_symlinks=False).st_size.to_bytes(8, "big"))
            with path.open("rb") as stream:
                for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                    digest.update(chunk)
    return digest.hexdigest()


audit = json.loads(AUDIT_INPUT.read_text())
lock = json.loads(CAMPAIGN_LOCK.read_text())
task_manifest = json.loads(Path("/task.json").read_text())
print("record_layout", audit["record_layout"])
print("semantics_mode", audit["semantics_mode"])
print("campaign_equal", audit["audit_campaign"] == lock)
manifest_without_launcher_config = dict(audit["manifest"])
manifest_without_launcher_config.pop("config", None)
print(
    "manifest_block_matches_task_after_launcher_config_overlay",
    manifest_without_launcher_config == task_manifest,
)
print(
    "manifest_hash_matches_task_file",
    audit["hashes"]["manifest_sha256"] == sha256_file(Path("/task.json")),
)

checks = {
    "audit_campaign_lock_sha256": CAMPAIGN_LOCK,
    "candidate_prompt_sha256": Path("/candidate/prompt.py"),
    "candidate_translator_sha256": Path("/candidate/py2mpy.py"),
    "canonical_sha256": Path("/reference/canonical.py"),
    "generation_codex_last_sha256": Path("/generation-evidence/codex-last.txt"),
    "generation_codex_output_sha256": Path("/generation-evidence/codex-output.log"),
    "generation_metrics_sha256": Path("/generation-evidence/metrics.json"),
    "generation_prompt_sha256": Path("/generation-evidence/prompt.txt"),
    "generation_usage_sha256": Path("/generation-evidence/usage.json"),
    "run_manifest_sha256": Path("/run.json"),
    "stage1_invocation_sha256": Path("/generation-evidence/invocation.json"),
    "stage1_result_sha256": Path("/generation-result.json"),
    "task_manifest_sha256": Path("/task.json"),
    "trusted_prompt_sha256": Path("/reference/prompt.py"),
    "trusted_translator_sha256": Path("/reference/py2mpy.py"),
}
for key, path in checks.items():
    actual = sha256_file(path)
    expected = audit["hashes"][key]
    print(key, "MATCH" if actual == expected else "MISMATCH", actual, path)

result = json.loads(Path("/generation-result.json").read_text())
invocation = json.loads(Path("/generation-evidence/invocation.json").read_text())
for record, expected_map in (
    ("generation-result", result["outputs"]["evidence"]),
    ("invocation", invocation["outputs"]["evidence"]),
):
    for relative, expected in sorted(expected_map.items()):
        path = Path("/generation-evidence") / relative
        actual = sha256_file(path)
        print(record, relative, "MATCH" if actual == expected else "MISMATCH", actual)

candidate_tree = sha256_tree(Path("/candidate"))
trace_tree = sha256_tree(Path("/generation-evidence/codex-trace"))
print("candidate_tree_pipeline_digest", candidate_tree)
print("generation_record_workspace_digest", invocation["retained_workspace_sha256"])
print("candidate_matches_generation_workspace", candidate_tree == invocation["retained_workspace_sha256"])
print("audit_input_candidate_tree_field", audit["hashes"]["candidate_tree_sha256"])
print("trace_tree_pipeline_digest", trace_tree)
print(
    "trace_tree_matches_audit_input",
    trace_tree == audit["hashes"]["generation_codex_trace_sha256"],
)
print("usage_source_trace_digest", json.loads(Path("/generation-evidence/usage.json").read_text())["source_trace_sha256"])
print("reference_semantics_exists", Path("/reference/reference-semantics").exists())
print("candidate_reference_semantics_exists", Path("/candidate/reference-semantics").exists())

for path in (
    Path("/audit-input.json"),
    Path("/audit-campaign-lock.json"),
    Path("/run.json"),
    Path("/task.json"),
    Path("/generation-result.json"),
    Path("/generation-evidence/invocation.json"),
    Path("/generation-evidence/metrics.json"),
    Path("/generation-evidence/codex-last.txt"),
    Path("/generation-evidence/codex-output.log"),
    Path("/generation-evidence/prompt.txt"),
    Path("/generation-evidence/codex-trace"),
):
    print("required", path, "OK" if path.exists() and not path.is_symlink() else "BAD")
