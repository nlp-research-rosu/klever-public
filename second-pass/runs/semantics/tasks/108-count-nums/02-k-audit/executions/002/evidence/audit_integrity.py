#!/usr/bin/env python3
"""Independent provenance and mount-integrity checks for audit 108-count-nums."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")
LOCK = Path("/audit-campaign-lock.json")
CANDIDATE = Path("/candidate")
REFERENCE = Path("/reference")
GENERATION = Path("/generation-evidence")


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def checked_regular(path: Path) -> None:
    assert path.exists(), f"missing: {path}"
    assert not path.is_symlink(), f"symlinked: {path}"
    assert path.is_file(), f"not a regular file: {path}"


audit = json.loads(AUDIT_INPUT.read_text())
lock = json.loads(LOCK.read_text())
print(f"record_layout={audit['record_layout']}")
print(f"semantics_mode={audit['semantics_mode']}")
assert audit["record_layout"] == "legacy-selected-stage1"
assert audit["semantics_mode"] == "SUPPLIED_SEMANTICS"
assert lock == audit["audit_campaign"]
assert digest(LOCK) == audit["hashes"]["audit_campaign_lock_sha256"]
print("campaign_lock_block_equal=true")
print(f"audit_campaign_lock_sha256={digest(LOCK)}")

required = {
    Path("/run.json"): "run_manifest_sha256",
    Path("/task.json"): "task_manifest_sha256",
    Path("/generation-result.json"): "stage1_result_sha256",
    GENERATION / "invocation.json": "stage1_invocation_sha256",
    GENERATION / "metrics.json": "generation_metrics_sha256",
    GENERATION / "codex-last.txt": "generation_codex_last_sha256",
    GENERATION / "codex-output.log": "generation_codex_output_sha256",
    GENERATION / "prompt.txt": "generation_prompt_sha256",
}
if (GENERATION / "usage.json").exists():
    required[GENERATION / "usage.json"] = "generation_usage_sha256"

for path, hash_key in required.items():
    checked_regular(path)
    actual = digest(path)
    expected = audit["hashes"][hash_key]
    assert actual == expected, (path, actual, expected)
    print(f"record_ok {path} sha256={actual}")

result = json.loads(Path("/generation-result.json").read_text())
for relative, expected in result["outputs"]["evidence"].items():
    path = GENERATION / relative
    checked_regular(path)
    actual = digest(path)
    assert actual == expected, (path, actual, expected)
    print(f"stage1_output_ok {relative} sha256={actual}")

trace_files = sorted((GENERATION / "codex-trace").rglob("*"))
assert trace_files
for path in trace_files:
    assert not path.is_symlink(), f"symlink in trace: {path}"
    if path.is_file():
        print(f"trace_file {path.relative_to(GENERATION)} sha256={digest(path)}")

trusted_hashes = {
    REFERENCE / "canonical.py": "canonical_sha256",
    REFERENCE / "prompt.py": "trusted_prompt_sha256",
    REFERENCE / "py2mpy.py": "trusted_translator_sha256",
    CANDIDATE / "prompt.py": "candidate_prompt_sha256",
    CANDIDATE / "py2mpy.py": "candidate_translator_sha256",
}
for path, hash_key in trusted_hashes.items():
    checked_regular(path)
    actual = digest(path)
    assert actual == audit["hashes"][hash_key], (path, actual)
    print(f"input_ok {path} sha256={actual}")

assert (CANDIDATE / "prompt.py").read_bytes() == (REFERENCE / "prompt.py").read_bytes()
assert (CANDIDATE / "py2mpy.py").read_bytes() == (REFERENCE / "py2mpy.py").read_bytes()
print("candidate_prompt_byte_equal=true")
print("candidate_translator_byte_equal=true")

trusted_semantics = REFERENCE / "reference-semantics"
candidate_semantics = CANDIDATE / "reference-semantics"
assert trusted_semantics.is_dir() and not trusted_semantics.is_symlink()
assert candidate_semantics.is_dir() and not candidate_semantics.is_symlink()


def tree_manifest(root: Path) -> dict[str, tuple[str, str | None]]:
    manifest: dict[str, tuple[str, str | None]] = {}
    for path in sorted(root.rglob("*")):
        rel = path.relative_to(root).as_posix()
        if path.is_symlink():
            manifest[rel] = ("symlink", os.readlink(path))
        elif path.is_dir():
            manifest[rel] = ("dir", None)
        elif path.is_file():
            manifest[rel] = ("file", digest(path))
        else:
            manifest[rel] = ("other", None)
    return manifest


def manifest_digest(manifest: dict[str, tuple[str, str | None]]) -> str:
    encoded = json.dumps(
        manifest, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


trusted_manifest = tree_manifest(trusted_semantics)
candidate_manifest = tree_manifest(candidate_semantics)
assert trusted_manifest == candidate_manifest
assert all(kind != "symlink" for kind, _ in trusted_manifest.values())
print(f"reference_semantics_entry_count={len(trusted_manifest)}")
print(f"reviewer_reference_semantics_manifest_sha256={manifest_digest(trusted_manifest)}")
print("reference_semantics_recursive_manifest_equal=true")
for rel, (kind, value) in trusted_manifest.items():
    if kind == "file":
        print(f"semantics_file {rel} sha256={value}")

proof_required = [
    "solution.py",
    "solution.mpy",
    "verification.k",
    "spec.k",
    "prove.sh",
]
for relative in proof_required:
    checked_regular(CANDIDATE / relative)
    print(f"proof_artifact {relative} sha256={digest(CANDIDATE / relative)}")

full_candidate_manifest = tree_manifest(CANDIDATE)
print(f"candidate_entry_count={len(full_candidate_manifest)}")
print(f"reviewer_candidate_manifest_sha256={manifest_digest(full_candidate_manifest)}")
print(f"launcher_recorded_candidate_tree_sha256={audit['hashes']['candidate_tree_sha256']}")
for rel, (kind, value) in full_candidate_manifest.items():
    if kind == "file":
        print(f"candidate_file {rel} sha256={value}")

for root in (CANDIDATE, REFERENCE, GENERATION):
    for path in root.rglob("*"):
        assert not path.is_symlink(), f"unexpected symlink: {path}"
print("mounted_tree_symlink_count=0")
print("INTEGRITY_CHECK=PASS")
