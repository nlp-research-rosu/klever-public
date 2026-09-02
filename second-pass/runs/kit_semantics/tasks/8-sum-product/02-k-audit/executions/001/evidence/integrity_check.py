#!/usr/bin/env python3
"""Independent provenance and supplied-semantics integrity checks."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from pathlib import Path


AUDIT = Path("/audit-input.json")
LOCK = Path("/audit-campaign-lock.json")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_tree(path: Path) -> str:
    """Reimplement the pipeline-v3 length-delimited directory digest."""
    if path.is_symlink() or not path.is_dir():
        raise ValueError(f"not a real directory: {path}")
    pending = [path]
    entries: list[tuple[str, str, Path]] = []
    while pending:
        directory = pending.pop()
        for child in os.scandir(directory):
            child_path = Path(child.path)
            mode = child.stat(follow_symlinks=False).st_mode
            relative = child_path.relative_to(path).as_posix()
            if stat.S_ISDIR(mode):
                entries.append((relative, "directory", child_path))
                pending.append(child_path)
            elif stat.S_ISREG(mode):
                entries.append((relative, "file", child_path))
            else:
                raise ValueError(f"linked or unsupported entry: {child_path}")
    digest = hashlib.sha256()
    for relative, kind, child_path in sorted(entries):
        encoded = relative.encode()
        digest.update(len(encoded).to_bytes(4, "big"))
        digest.update(encoded)
        digest.update(kind.encode() + b"\0")
        if kind == "file":
            size = child_path.stat(follow_symlinks=False).st_size
            digest.update(size.to_bytes(8, "big"))
            with child_path.open("rb") as stream:
                for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                    digest.update(chunk)
    return digest.hexdigest()


def entry_manifest(root: Path) -> dict[str, tuple[str, str | None]]:
    result: dict[str, tuple[str, str | None]] = {}
    for entry in sorted(root.rglob("*")):
        relative = entry.relative_to(root).as_posix()
        mode = entry.lstat().st_mode
        if stat.S_ISLNK(mode):
            result[relative] = ("symlink", os.readlink(entry))
        elif stat.S_ISDIR(mode):
            result[relative] = ("directory", None)
        elif stat.S_ISREG(mode):
            result[relative] = ("file", sha256_file(entry))
        else:
            result[relative] = ("unsupported", None)
    return result


def check_regular(path: Path) -> list[str]:
    issues = []
    try:
        mode = path.lstat().st_mode
    except OSError as error:
        return [f"{path}: unreadable or absent: {error}"]
    if stat.S_ISLNK(mode):
        issues.append(f"{path}: symlink")
    elif not stat.S_ISREG(mode):
        issues.append(f"{path}: not a regular file")
    else:
        try:
            path.read_bytes()
        except OSError as error:
            issues.append(f"{path}: unreadable: {error}")
    return issues


audit = json.loads(AUDIT.read_text())
lock = json.loads(LOCK.read_text())
issues: list[str] = []

print(f"record_layout={audit.get('record_layout')}")
print(f"semantics_mode={audit.get('semantics_mode')}")
print(f"problem_id={audit.get('problem_id')}")

if audit.get("audit_campaign") != lock:
    issues.append("campaign lock JSON does not equal audit_campaign block")
print(f"campaign_block_equal={audit.get('audit_campaign') == lock}")

lock_hash = sha256_file(LOCK)
expected_lock_hash = audit["hashes"]["audit_campaign_lock_sha256"]
print(f"campaign_lock_sha256={lock_hash}")
print(f"campaign_lock_hash_matches={lock_hash == expected_lock_hash}")
if lock_hash != expected_lock_hash:
    issues.append("campaign lock hash mismatch")

required_pipeline_files = [
    AUDIT,
    LOCK,
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
for required in required_pipeline_files:
    issues.extend(check_regular(required))

required_directories = [
    Path("/candidate"),
    Path("/generation-evidence"),
    Path("/generation-evidence/codex-trace"),
    Path("/reference/reference-semantics"),
    Path("/candidate/reference-semantics"),
]
for required in required_directories:
    try:
        mode = required.lstat().st_mode
    except OSError as error:
        issues.append(f"{required}: unreadable or absent: {error}")
        continue
    if stat.S_ISLNK(mode) or not stat.S_ISDIR(mode):
        issues.append(f"{required}: not a real directory")

recorded_file_hashes = {
    Path("/audit-campaign-lock.json"): "audit_campaign_lock_sha256",
    Path("/reference/canonical.py"): "canonical_sha256",
    Path("/reference/prompt.py"): "trusted_prompt_sha256",
    Path("/reference/py2mpy.py"): "trusted_translator_sha256",
    Path("/candidate/prompt.py"): "candidate_prompt_sha256",
    Path("/candidate/py2mpy.py"): "candidate_translator_sha256",
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
}
for path, hash_key in recorded_file_hashes.items():
    actual = sha256_file(path)
    expected = audit["hashes"][hash_key]
    matched = actual == expected
    print(f"file_hash {path} {actual} expected={expected} match={matched}")
    if not matched:
        issues.append(f"recorded hash mismatch: {path}")

result = json.loads(Path("/generation-result.json").read_text())
invocation = json.loads(Path("/generation-evidence/invocation.json").read_text())
for relative, expected in result["outputs"]["evidence"].items():
    artifact = Path("/generation-evidence") / relative
    regular_issues = check_regular(artifact)
    issues.extend(regular_issues)
    if not regular_issues:
        actual = sha256_file(artifact)
        matched = actual == expected
        print(f"result_evidence_hash {relative} {actual} expected={expected} match={matched}")
        if not matched:
            issues.append(f"generation-result evidence hash mismatch: {relative}")
if result["outputs"]["evidence"] != invocation["outputs"]["evidence"]:
    issues.append("generation-result and invocation evidence hash maps differ")

trace_hash = sha256_tree(Path("/generation-evidence/codex-trace"))
usage = json.loads(Path("/generation-evidence/usage.json").read_text())
print(f"trace_tree_sha256={trace_hash}")
print(f"trace_tree_matches_usage={trace_hash == usage.get('source_trace_sha256')}")
if trace_hash != usage.get("source_trace_sha256"):
    issues.append("trace tree does not match usage source_trace_sha256")

candidate_tree_hash = sha256_tree(Path("/candidate"))
expected_workspace_hash = result["outputs"]["workspace_sha256"]
print(f"candidate_pipeline_tree_sha256={candidate_tree_hash}")
print(f"candidate_tree_matches_generation_result={candidate_tree_hash == expected_workspace_hash}")
if candidate_tree_hash != expected_workspace_hash:
    issues.append("mounted candidate differs from generation-result workspace hash")

trusted_semantics_tree_hash = sha256_tree(Path("/reference/reference-semantics"))
candidate_semantics_tree_hash = sha256_tree(Path("/candidate/reference-semantics"))
expected_semantics_manifest_hash = audit["hashes"][
    "trusted_reference_semantics_manifest_sha256"
]
print(f"trusted_semantics_tree_sha256={trusted_semantics_tree_hash}")
print(f"candidate_semantics_tree_sha256={candidate_semantics_tree_hash}")
print(
    "trusted_semantics_manifest_hash_matches="
    f"{trusted_semantics_tree_hash == expected_semantics_manifest_hash}"
)
if trusted_semantics_tree_hash != expected_semantics_manifest_hash:
    issues.append("trusted semantics manifest hash mismatch")

trusted_manifest = entry_manifest(Path("/reference/reference-semantics"))
candidate_manifest = entry_manifest(Path("/candidate/reference-semantics"))
print(f"trusted_semantics_entries={len(trusted_manifest)}")
print(f"candidate_semantics_entries={len(candidate_manifest)}")
print(f"semantics_recursive_manifest_equal={trusted_manifest == candidate_manifest}")
if trusted_manifest != candidate_manifest:
    trusted_keys = set(trusted_manifest)
    candidate_keys = set(candidate_manifest)
    for relative in sorted(trusted_keys - candidate_keys):
        issues.append(f"candidate semantics missing: {relative}")
    for relative in sorted(candidate_keys - trusted_keys):
        issues.append(f"candidate semantics additional: {relative}")
    for relative in sorted(trusted_keys & candidate_keys):
        if trusted_manifest[relative] != candidate_manifest[relative]:
            issues.append(
                f"candidate semantics changed or mistyped: {relative}: "
                f"{candidate_manifest[relative]} != {trusted_manifest[relative]}"
            )

byte_pairs = [
    (Path("/candidate/prompt.py"), Path("/reference/prompt.py"), "prompt"),
    (Path("/candidate/py2mpy.py"), Path("/reference/py2mpy.py"), "translator"),
]
for candidate_path, trusted_path, label in byte_pairs:
    equal = candidate_path.read_bytes() == trusted_path.read_bytes()
    print(f"{label}_byte_equal={equal}")
    if not equal:
        issues.append(f"candidate {label} differs from trusted input")

proof_artifacts = [
    "solution.py",
    "solution.mpy",
    "verification.k",
    "spec.k",
    "prove.sh",
    "PROOF.md",
]
for name in proof_artifacts:
    artifact_issues = check_regular(Path("/candidate") / name)
    if artifact_issues:
        issues.extend(f"candidate defect: {issue}" for issue in artifact_issues)
    else:
        print(f"proof_artifact_regular={name}")

print(f"ISSUE_COUNT={len(issues)}")
for issue in issues:
    print(f"ISSUE: {issue}")
raise SystemExit(1 if issues else 0)
