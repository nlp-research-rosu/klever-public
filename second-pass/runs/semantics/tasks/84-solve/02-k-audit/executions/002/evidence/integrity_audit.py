#!/usr/bin/env python3
"""Reviewer-authored stage-1 integrity and provenance audit."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")
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


def tree_manifest(root: Path) -> list[dict[str, str | int]]:
    entries: list[dict[str, str | int]] = []
    for path in sorted(root.rglob("*"), key=lambda item: item.as_posix()):
        rel = path.relative_to(root).as_posix()
        mode = path.lstat().st_mode
        if stat.S_ISLNK(mode):
            entries.append({"path": rel, "type": "symlink", "target": os.readlink(path)})
        elif stat.S_ISDIR(mode):
            entries.append({"path": rel, "type": "directory"})
        elif stat.S_ISREG(mode):
            entries.append(
                {
                    "path": rel,
                    "type": "file",
                    "size": path.stat().st_size,
                    "sha256": sha256(path),
                }
            )
        else:
            entries.append({"path": rel, "type": f"mode:{stat.S_IFMT(mode):o}"})
    return entries


def manifest_digest(entries: list[dict[str, str | int]]) -> str:
    encoded = json.dumps(entries, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def regular_readable(path: Path) -> bool:
    try:
        mode = path.lstat().st_mode
    except OSError:
        return False
    return stat.S_ISREG(mode) and not stat.S_ISLNK(mode) and os.access(path, os.R_OK)


audit = json.loads(AUDIT_INPUT.read_text())
lock = json.loads(LOCK.read_text())
hashes = audit["hashes"]

print("record_layout:", audit["record_layout"])
print("semantics_mode:", audit["semantics_mode"])
print("campaign_block_matches_lock:", audit["audit_campaign"] == lock)
print("campaign_lock_sha256:", sha256(LOCK))
print("campaign_lock_recorded:", hashes["audit_campaign_lock_sha256"])
print("campaign_lock_hash_matches:", sha256(LOCK) == hashes["audit_campaign_lock_sha256"])

required_records = [
    Path("/audit-input.json"),
    Path("/audit-campaign-lock.json"),
    Path("/run.json"),
    Path("/task.json"),
    Path("/generation-result.json"),
    GENERATION / "invocation.json",
    GENERATION / "metrics.json",
    GENERATION / "codex-last.txt",
    GENERATION / "codex-output.log",
    GENERATION / "prompt.txt",
]
trace_files = sorted((GENERATION / "codex-trace").rglob("*"))
trace_regular = [path for path in trace_files if path.is_file() and not path.is_symlink()]
print("required_records:")
for path in required_records:
    print(f"  {path}: regular_readable={regular_readable(path)}")
print("trace_regular_files:", len(trace_regular))
print("trace_symlinks:", [str(path) for path in trace_files if path.is_symlink()])
print("usage_present:", (GENERATION / "usage.json").exists())
if (GENERATION / "usage.json").exists():
    print("usage_regular_readable:", regular_readable(GENERATION / "usage.json"))

plain_hash_checks = {
    "canonical_sha256": REFERENCE / "canonical.py",
    "trusted_prompt_sha256": REFERENCE / "prompt.py",
    "candidate_prompt_sha256": CANDIDATE / "prompt.py",
    "trusted_translator_sha256": REFERENCE / "py2mpy.py",
    "candidate_translator_sha256": CANDIDATE / "py2mpy.py",
    "run_manifest_sha256": Path("/run.json"),
    "task_manifest_sha256": Path("/task.json"),
    "stage1_result_sha256": Path("/generation-result.json"),
    "stage1_invocation_sha256": GENERATION / "invocation.json",
    "generation_metrics_sha256": GENERATION / "metrics.json",
    "generation_codex_last_sha256": GENERATION / "codex-last.txt",
    "generation_codex_output_sha256": GENERATION / "codex-output.log",
    "generation_prompt_sha256": GENERATION / "prompt.txt",
    "generation_usage_sha256": GENERATION / "usage.json",
}
print("plain_hash_checks:")
for key, path in plain_hash_checks.items():
    actual = sha256(path) if regular_readable(path) else "UNREADABLE"
    expected = hashes.get(key, "NOT_RECORDED")
    print(f"  {key}: actual={actual} expected={expected} match={actual == expected}")

print("candidate_prompt_byte_equal:", (CANDIDATE / "prompt.py").read_bytes() == (REFERENCE / "prompt.py").read_bytes())
print(
    "candidate_translator_byte_equal:",
    (CANDIDATE / "py2mpy.py").read_bytes() == (REFERENCE / "py2mpy.py").read_bytes(),
)

trusted_semantics = REFERENCE / "reference-semantics"
candidate_semantics = CANDIDATE / "reference-semantics"
trusted_manifest = tree_manifest(trusted_semantics)
candidate_manifest = tree_manifest(candidate_semantics)
print("trusted_semantics_present:", trusted_semantics.is_dir())
print("candidate_semantics_present:", candidate_semantics.is_dir())
print("trusted_semantics_entries:", len(trusted_manifest))
print("candidate_semantics_entries:", len(candidate_manifest))
print("trusted_semantics_review_digest:", manifest_digest(trusted_manifest))
print("candidate_semantics_review_digest:", manifest_digest(candidate_manifest))
print("semantics_manifests_byte_exact:", trusted_manifest == candidate_manifest)
print(
    "semantics_symlink_entries:",
    [
        entry
        for entry in candidate_manifest
        if entry["type"] == "symlink"
    ],
)
if trusted_manifest != candidate_manifest:
    trusted_by_path = {str(entry["path"]): entry for entry in trusted_manifest}
    candidate_by_path = {str(entry["path"]): entry for entry in candidate_manifest}
    all_paths = sorted(set(trusted_by_path) | set(candidate_by_path))
    for rel in all_paths:
        if trusted_by_path.get(rel) != candidate_by_path.get(rel):
            print("SEMANTICS_DIFF:", rel, trusted_by_path.get(rel), candidate_by_path.get(rel))

required_candidate = [
    "prompt.py",
    "py2mpy.py",
    "solution.py",
    "solution.mpy",
    "verification.k",
    "spec.k",
    "prove.sh",
]
print("required_candidate_artifacts:")
for rel in required_candidate:
    print(f"  {rel}: regular_readable={regular_readable(CANDIDATE / rel)}")

candidate_entries = tree_manifest(CANDIDATE)
print("candidate_symlink_entries:", [entry for entry in candidate_entries if entry["type"] == "symlink"])
print("candidate_review_digest:", manifest_digest(candidate_entries))

invocation = json.loads((GENERATION / "invocation.json").read_text())
print("invocation_evidence_hash_checks:")
for rel, expected in sorted(invocation["outputs"]["evidence"].items()):
    path = GENERATION / rel
    actual = sha256(path) if regular_readable(path) else "UNREADABLE"
    print(f"  {rel}: actual={actual} expected={expected} match={actual == expected}")

trace_json_ok = True
trace_lines = 0
for path in trace_regular:
    with path.open() as stream:
        for line_number, line in enumerate(stream, 1):
            trace_lines += 1
            try:
                json.loads(line)
            except json.JSONDecodeError as err:
                trace_json_ok = False
                print(f"TRACE_JSON_ERROR: {path}:{line_number}: {err}")
print("trace_json_lines:", trace_lines)
print("trace_json_all_valid:", trace_json_ok)
