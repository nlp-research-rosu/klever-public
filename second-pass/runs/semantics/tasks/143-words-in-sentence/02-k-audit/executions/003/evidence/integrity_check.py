#!/usr/bin/env python3
"""Independent launcher/provenance and supplied-semantics integrity check."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def tree_manifest(root: Path):
    manifest = []
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root).as_posix()
        if path.is_symlink():
            manifest.append((relative, "symlink", os.readlink(path)))
        elif path.is_dir():
            manifest.append((relative, "dir", ""))
        elif path.is_file():
            manifest.append((relative, "file", sha256(path)))
        else:
            manifest.append((relative, "other", ""))
    return manifest


audit_input_path = Path("/audit-input.json")
lock_path = Path("/audit-campaign-lock.json")
audit_input = json.loads(audit_input_path.read_text())
campaign_lock = json.loads(lock_path.read_text())

print(f"record_layout={audit_input['record_layout']}")
print(f"semantics_mode={audit_input['semantics_mode']}")
print(f"campaign_block_exact_match={audit_input['audit_campaign'] == campaign_lock}")
actual_lock_hash = sha256(lock_path)
print(f"campaign_lock_sha256={actual_lock_hash}")
print(
    "campaign_lock_hash_matches_recorded="
    f"{actual_lock_hash == audit_input['hashes']['audit_campaign_lock_sha256']}"
)

required = [
    Path("/run.json"),
    Path("/task.json"),
    Path("/generation-result.json"),
    Path("/generation-evidence/invocation.json"),
    Path("/generation-evidence/metrics.json"),
    Path("/generation-evidence/codex-last.txt"),
    Path("/generation-evidence/codex-output.log"),
    Path("/generation-evidence/prompt.txt"),
    Path("/generation-evidence/codex-trace"),
    Path("/candidate"),
    Path("/reference/canonical.py"),
    Path("/reference/prompt.py"),
    Path("/reference/py2mpy.py"),
    Path("/reference/reference-semantics"),
]
missing = [str(path) for path in required if not path.exists()]
wrong_types = [
    str(path)
    for path in required
    if path.exists()
    and (
        (path.name in {"codex-trace", "candidate", "reference-semantics"} and not path.is_dir())
        or (path.name not in {"codex-trace", "candidate", "reference-semantics"} and not path.is_file())
    )
]
print(f"required_missing={missing}")
print(f"required_wrong_types={wrong_types}")

hash_checks = {
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
    "/generation-evidence/codex-last.txt": "generation_codex_last_sha256",
    "/generation-evidence/codex-output.log": "generation_codex_output_sha256",
    "/generation-evidence/prompt.txt": "generation_prompt_sha256",
}
if Path("/generation-evidence/usage.json").exists():
    hash_checks["/generation-evidence/usage.json"] = "generation_usage_sha256"
for raw_path, key in hash_checks.items():
    actual = sha256(Path(raw_path))
    print(f"hash_match[{raw_path}]={actual == audit_input['hashes'][key]} {actual}")

reference_tree = tree_manifest(Path("/reference/reference-semantics"))
candidate_tree = tree_manifest(Path("/candidate/reference-semantics"))
reference_blob = json.dumps(reference_tree, separators=(",", ":")).encode()
candidate_blob = json.dumps(candidate_tree, separators=(",", ":")).encode()
print(f"reference_semantics_entry_count={len(reference_tree)}")
print(f"candidate_semantics_entry_count={len(candidate_tree)}")
print(f"reference_semantics_manifest_sha256={hashlib.sha256(reference_blob).hexdigest()}")
print(f"candidate_semantics_manifest_sha256={hashlib.sha256(candidate_blob).hexdigest()}")
print(f"semantics_manifests_exact_match={reference_tree == candidate_tree}")
print(
    "candidate_prompt_byte_match="
    f"{Path('/candidate/prompt.py').read_bytes() == Path('/reference/prompt.py').read_bytes()}"
)
print(
    "candidate_translator_byte_match="
    f"{Path('/candidate/py2mpy.py').read_bytes() == Path('/reference/py2mpy.py').read_bytes()}"
)

all_roots = [
    Path("/candidate"),
    Path("/reference"),
    Path("/generation-evidence"),
]
symlinks = [
    str(path)
    for root in all_roots
    for path in root.rglob("*")
    if path.is_symlink()
]
print(f"symlink_count={len(symlinks)}")
print(f"symlinks={symlinks}")

result = json.loads(Path("/generation-result.json").read_text())
trace_files = sorted(Path("/generation-evidence/codex-trace").rglob("*.jsonl"))
trace_records = 0
trace_valid_json = True
for trace_file in trace_files:
    relative = trace_file.relative_to("/generation-evidence").as_posix()
    expected = result["outputs"]["evidence"].get(relative)
    actual = sha256(trace_file)
    print(f"trace_hash_match[{relative}]={expected == actual} {actual}")
    with trace_file.open() as stream:
        for line in stream:
            trace_records += 1
            try:
                json.loads(line)
            except json.JSONDecodeError:
                trace_valid_json = False
print(f"trace_file_count={len(trace_files)}")
print(f"trace_record_count={trace_records}")
print(f"trace_all_records_valid_json={trace_valid_json}")

candidate_required = [
    "solution.py",
    "solution.mpy",
    "verification.k",
    "spec.k",
    "prove.sh",
]
print(
    "candidate_required_missing="
    f"{[name for name in candidate_required if not Path('/candidate', name).is_file()]}"
)
