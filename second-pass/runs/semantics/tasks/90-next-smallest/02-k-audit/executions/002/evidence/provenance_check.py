#!/usr/bin/env python3
"""Read-only provenance and mount-integrity checks used by the audit."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from pathlib import Path


def file_hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def pipeline_tree_hash(root: Path) -> str:
    """The schema-v2 pipeline tree digest from pipeline_contract.sha256_tree."""
    if root.is_symlink() or not root.is_dir():
        raise AssertionError(f"not a real directory: {root}")
    pending = [root]
    entries: list[tuple[str, str, Path]] = []
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


audit_input = json.loads(Path("/audit-input.json").read_text())
campaign_lock = json.loads(Path("/audit-campaign-lock.json").read_text())
generation_result = json.loads(Path("/generation-result.json").read_text())
invocation = json.loads(Path("/generation-evidence/invocation.json").read_text())
usage = json.loads(Path("/generation-evidence/usage.json").read_text())

print(f"RECORD_LAYOUT: {audit_input['record_layout']}")
print(f"SEMANTICS_MODE: {audit_input['semantics_mode']}")
required_paths = [
    Path("/audit-input.json"),
    Path("/audit-campaign-lock.json"),
    Path("/candidate"),
    Path("/reference/canonical.py"),
    Path("/reference/prompt.py"),
    Path("/reference/py2mpy.py"),
    Path("/reference/reference-semantics"),
    Path("/run.json"),
    Path("/task.json"),
    Path("/generation-result.json"),
    Path("/generation-evidence/invocation.json"),
    Path("/generation-evidence/metrics.json"),
    Path("/generation-evidence/codex-last.txt"),
    Path("/generation-evidence/codex-output.log"),
    Path("/generation-evidence/prompt.txt"),
    Path("/generation-evidence/usage.json"),
    Path("/generation-evidence/codex-trace"),
]
for path in required_paths:
    kind_ok = path.is_dir() if path.suffix == "" and path.name in {
        "candidate", "reference-semantics", "codex-trace"
    } else path.is_file()
    print(
        f"REQUIRED {path}: exists={path.exists()} "
        f"symlink={path.is_symlink()} kind_ok={kind_ok} readable={os.access(path, os.R_OK)}"
    )
print(f"CAMPAIGN_BLOCK_EQUAL: {campaign_lock == audit_input['audit_campaign']}")
print(
    "CAMPAIGN_HASH: "
    f"{file_hash(Path('/audit-campaign-lock.json'))} "
    f"expected={audit_input['hashes']['audit_campaign_lock_sha256']}"
)

file_checks = [
    ("/reference/canonical.py", "canonical_sha256"),
    ("/reference/prompt.py", "trusted_prompt_sha256"),
    ("/reference/py2mpy.py", "trusted_translator_sha256"),
    ("/candidate/prompt.py", "candidate_prompt_sha256"),
    ("/candidate/py2mpy.py", "candidate_translator_sha256"),
    ("/run.json", "run_manifest_sha256"),
    ("/task.json", "task_manifest_sha256"),
    ("/generation-result.json", "stage1_result_sha256"),
    ("/generation-evidence/invocation.json", "stage1_invocation_sha256"),
    ("/generation-evidence/metrics.json", "generation_metrics_sha256"),
    ("/generation-evidence/codex-last.txt", "generation_codex_last_sha256"),
    ("/generation-evidence/codex-output.log", "generation_codex_output_sha256"),
    ("/generation-evidence/prompt.txt", "generation_prompt_sha256"),
    ("/generation-evidence/usage.json", "generation_usage_sha256"),
]
for raw_path, key in file_checks:
    path = Path(raw_path)
    actual = file_hash(path)
    expected = audit_input["hashes"][key]
    print(f"FILE_HASH {raw_path}: {actual} expected={expected} match={actual == expected}")

for relative, expected in sorted(generation_result["outputs"]["evidence"].items()):
    path = Path("/generation-evidence") / relative
    actual = file_hash(path)
    print(
        f"GENERATION_OUTPUT_HASH {relative}: {actual} "
        f"expected={expected} match={actual == expected}"
    )

candidate_tree = pipeline_tree_hash(Path("/candidate"))
candidate_expected = generation_result["outputs"]["workspace_sha256"]
print(
    f"PIPELINE_TREE /candidate: {candidate_tree} "
    f"expected={candidate_expected} match={candidate_tree == candidate_expected}"
)
print(
    "PIPELINE_TREE /candidate/reference-semantics: "
    f"{pipeline_tree_hash(Path('/candidate/reference-semantics'))} "
    f"expected={audit_input['hashes']['trusted_reference_semantics_manifest_sha256']}"
)
print(
    "PIPELINE_TREE /reference/reference-semantics: "
    f"{pipeline_tree_hash(Path('/reference/reference-semantics'))} "
    f"expected={audit_input['hashes']['trusted_reference_semantics_manifest_sha256']}"
)
trace_tree = pipeline_tree_hash(Path("/generation-evidence/codex-trace"))
print(
    f"PIPELINE_TREE /generation-evidence/codex-trace: {trace_tree} "
    f"usage_expected={usage['source_trace_sha256']} "
    f"invocation_input_expected={invocation['inputs'].get('source_trace_sha256', 'not-recorded')}"
)
