#!/usr/bin/env python3
"""Independent provenance and supplied-semantics integrity checks."""

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


def pipeline_tree_hash(root: Path) -> str:
    """Reimplement the mounted pipeline's length-delimited tree hash."""
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
                raise AssertionError(f"linked or unsupported entry: {path}")
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


audit_input = json.loads(Path("/audit-input.json").read_text())
campaign_lock = json.loads(Path("/audit-campaign-lock.json").read_text())
assert audit_input["audit_campaign"] == campaign_lock
assert (
    sha256_file(Path("/audit-campaign-lock.json"))
    == audit_input["hashes"]["audit_campaign_lock_sha256"]
)
assert audit_input["record_layout"] == "legacy-selected-stage1"
assert audit_input["semantics_mode"] == "SUPPLIED_SEMANTICS"

required = [
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
]
for path in required:
    mode = path.lstat().st_mode
    assert stat.S_ISREG(mode), f"required record is not a regular file: {path}"

recorded_file_hashes = {
    "/audit-campaign-lock.json": "audit_campaign_lock_sha256",
    "/reference/canonical.py": "canonical_sha256",
    "/reference/prompt.py": "trusted_prompt_sha256",
    "/reference/py2mpy.py": "trusted_translator_sha256",
    "/candidate/prompt.py": "candidate_prompt_sha256",
    "/candidate/py2mpy.py": "candidate_translator_sha256",
    "/run.json": "run_manifest_sha256",
    "/task.json": "task_manifest_sha256",
    "/generation-result.json": "stage1_result_sha256",
    "/generation-evidence/invocation.json": "stage1_invocation_sha256",
    "/generation-evidence/metrics.json": "generation_metrics_sha256",
    "/generation-evidence/usage.json": "generation_usage_sha256",
    "/generation-evidence/codex-last.txt": "generation_codex_last_sha256",
    "/generation-evidence/codex-output.log": "generation_codex_output_sha256",
    "/generation-evidence/prompt.txt": "generation_prompt_sha256",
}
for raw_path, hash_key in recorded_file_hashes.items():
    path = Path(raw_path)
    actual = sha256_file(path)
    expected = audit_input["hashes"][hash_key]
    assert actual == expected, f"{path}: {actual} != {expected}"
    print(f"hash_ok {path} {actual}")

candidate_semantics = Path("/candidate/reference-semantics")
trusted_semantics = Path("/reference/reference-semantics")


def entry_manifest(root: Path) -> dict[str, tuple[str, str | None]]:
    result: dict[str, tuple[str, str | None]] = {}
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root).as_posix()
        mode = path.lstat().st_mode
        if stat.S_ISDIR(mode):
            result[relative] = ("directory", None)
        elif stat.S_ISREG(mode):
            result[relative] = ("file", sha256_file(path))
        else:
            result[relative] = ("UNSUPPORTED", None)
    return result


candidate_manifest = entry_manifest(candidate_semantics)
trusted_manifest = entry_manifest(trusted_semantics)
assert candidate_manifest == trusted_manifest
assert all(kind != "UNSUPPORTED" for kind, _ in candidate_manifest.values())

print(f"campaign_lock_match=true")
print(f"required_records={len(required)}")
print(f"semantics_entries={len(candidate_manifest)}")
print(f"semantics_recursive_match=true")
print(f"candidate_pipeline_tree_sha256={pipeline_tree_hash(Path('/candidate'))}")
print(
    "candidate_generation_workspace_sha256="
    + json.loads(Path("/generation-result.json").read_text())["outputs"][
        "workspace_sha256"
    ]
)
print(
    f"trusted_semantics_pipeline_tree_sha256={pipeline_tree_hash(trusted_semantics)}"
)
print(
    f"candidate_semantics_pipeline_tree_sha256={pipeline_tree_hash(candidate_semantics)}"
)
print(
    "trace_pipeline_tree_sha256="
    + pipeline_tree_hash(Path("/generation-evidence/codex-trace"))
)
print("RESULT: provenance and supplied-semantics integrity checks passed")
