#!/usr/bin/env python3
"""Independent, read-only provenance and supplied-semantics integrity checks."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")
LOCK = Path("/audit-campaign-lock.json")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def regular_file(path: Path) -> None:
    mode = path.lstat().st_mode
    assert stat.S_ISREG(mode), f"not a regular file: {path}"


def tree_manifest(root: Path) -> list[tuple[str, str, int]]:
    result: list[tuple[str, str, int]] = []
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root).as_posix()
        mode = path.lstat().st_mode
        assert not stat.S_ISLNK(mode), f"symlinked tree entry: {path}"
        if stat.S_ISDIR(mode):
            result.append((relative + "/", "DIR", 0))
        elif stat.S_ISREG(mode):
            result.append((relative, sha256(path), path.stat().st_size))
        else:
            raise AssertionError(f"unexpected tree entry type: {path}")
    return result


def manifest_digest(entries: list[tuple[str, str, int]]) -> str:
    payload = json.dumps(entries, ensure_ascii=False, separators=(",", ":")).encode()
    return hashlib.sha256(payload).hexdigest()


def length_delimited_tree_digest(root: Path) -> str:
    """Independently implement the record-layout's length-delimited tree hash."""
    entries: list[tuple[str, str, Path]] = []
    for path in root.rglob("*"):
        mode = path.lstat().st_mode
        relative = path.relative_to(root).as_posix()
        if stat.S_ISDIR(mode):
            entries.append((relative, "directory", path))
        elif stat.S_ISREG(mode):
            entries.append((relative, "file", path))
        else:
            raise AssertionError(f"linked/unsupported tree entry: {path}")
    digest = hashlib.sha256()
    for relative, kind, path in sorted(entries):
        encoded = relative.encode()
        digest.update(len(encoded).to_bytes(4, "big"))
        digest.update(encoded)
        digest.update(kind.encode() + b"\0")
        if kind == "file":
            digest.update(path.stat().st_size.to_bytes(8, "big"))
            digest.update(path.read_bytes())
    return digest.hexdigest()


audit = json.loads(AUDIT_INPUT.read_text())
lock = json.loads(LOCK.read_text())

print(f"record_layout={audit['record_layout']}")
print(f"semantics_mode={audit['semantics_mode']}")
assert audit["record_layout"] == "legacy-selected-stage1"
assert audit["semantics_mode"] == "SUPPLIED_SEMANTICS"
assert audit["mount_reference_semantics"] is True
assert lock == audit["audit_campaign"], "campaign lock content differs"

paths = audit["container_paths"]
required = {
    "audit input": AUDIT_INPUT,
    "campaign lock": Path(paths["audit_campaign_lock"]),
    "candidate": Path(paths["candidate"]),
    "canonical": Path(paths["canonical"]),
    "trusted prompt": Path(paths["trusted_prompt"]),
    "translator": Path(paths["translator"]),
    "run manifest": Path(paths["run_manifest"]),
    "task manifest": Path(paths["task_manifest"]),
    "stage1 result": Path(paths["stage1_result"]),
    "generation invocation": Path(paths["generation_manifest"]),
    "generation metrics": Path(paths["generation_metrics"]),
    "generation last": Path(paths["generation_last"]),
    "generation output": Path(paths["generation_output"]),
    "generation trace": Path(paths["generation_trace"]),
    "generation prompt": Path(paths["generation_root"]) / "prompt.txt",
}
for label, path in required.items():
    assert path.exists(), f"required {label} missing: {path}"
    assert os.access(path, os.R_OK), f"required {label} unreadable: {path}"
    print(f"required {label}: PRESENT {path}")

# usage.json is present and required to be inspected when present for this layout.
usage = Path(paths["generation_root"]) / "usage.json"
assert usage.is_file()
print(f"optional usage record: PRESENT {usage}")

file_hash_expectations = {
    LOCK: "audit_campaign_lock_sha256",
    Path("/candidate/prompt.py"): "candidate_prompt_sha256",
    Path("/candidate/py2mpy.py"): "candidate_translator_sha256",
    Path("/reference/prompt.py"): "trusted_prompt_sha256",
    Path("/reference/py2mpy.py"): "trusted_translator_sha256",
    Path("/reference/canonical.py"): "canonical_sha256",
    Path("/run.json"): "run_manifest_sha256",
    Path("/task.json"): "task_manifest_sha256",
    Path("/generation-result.json"): "stage1_result_sha256",
    Path("/generation-evidence/invocation.json"): "stage1_invocation_sha256",
    Path("/generation-evidence/metrics.json"): "generation_metrics_sha256",
    Path("/generation-evidence/usage.json"): "generation_usage_sha256",
    Path("/generation-evidence/codex-last.txt"): "generation_codex_last_sha256",
    Path("/generation-evidence/codex-output.log"): "generation_codex_output_sha256",
    Path("/generation-evidence/prompt.txt"): "generation_prompt_sha256",
}
for path, key in file_hash_expectations.items():
    regular_file(path)
    actual = sha256(path)
    expected = audit["hashes"][key]
    assert actual == expected, f"hash mismatch for {path}: {actual} != {expected}"
    print(f"sha256 {path} {actual} MATCH {key}")

assert Path("/candidate/prompt.py").read_bytes() == Path("/reference/prompt.py").read_bytes()
assert Path("/candidate/py2mpy.py").read_bytes() == Path("/reference/py2mpy.py").read_bytes()
print("candidate prompt byte identity: MATCH")
print("candidate translator byte identity: MATCH")

candidate_semantics = tree_manifest(Path("/candidate/reference-semantics"))
trusted_semantics = tree_manifest(Path("/reference/reference-semantics"))
assert candidate_semantics == trusted_semantics, "candidate supplied semantics tree differs"
print(f"supplied semantics entry count: {len(candidate_semantics)}")
print(f"reviewer semantics manifest sha256: {manifest_digest(candidate_semantics)}")
print("candidate/trusted supplied semantics recursive byte-and-type identity: MATCH")

candidate_tree = tree_manifest(Path("/candidate"))
print(f"candidate entry count: {len(candidate_tree)}")
print(f"reviewer candidate manifest sha256: {manifest_digest(candidate_tree)}")

stage1_result = json.loads(Path("/generation-result.json").read_text())
invocation = json.loads(Path("/generation-evidence/invocation.json").read_text())
candidate_ld_hash = length_delimited_tree_digest(Path("/candidate"))
assert candidate_ld_hash == stage1_result["outputs"]["workspace_sha256"]
assert candidate_ld_hash == invocation["retained_workspace_sha256"]
print(f"length-delimited candidate tree sha256: {candidate_ld_hash} MATCH generation records")

semantics_ld_hash = length_delimited_tree_digest(Path("/reference/reference-semantics"))
assert semantics_ld_hash == audit["hashes"]["trusted_reference_semantics_manifest_sha256"]
print(f"length-delimited semantics tree sha256: {semantics_ld_hash} MATCH audit record")

trace_files = sorted(Path(paths["generation_trace"]).rglob("*"))
trace_files = [path for path in trace_files if path.is_file()]
result = json.loads(Path("/generation-result.json").read_text())
declared_outputs = result["outputs"]["evidence"]
for path in trace_files:
    regular_file(path)
    rel = "codex-trace/" + path.relative_to(paths["generation_trace"]).as_posix()
    actual = sha256(path)
    assert declared_outputs.get(rel) == actual, f"trace hash mismatch: {rel}"
    print(f"sha256 {path} {actual} MATCH generation-result")

usage_document = json.loads(usage.read_text())
trace_ld_hash = length_delimited_tree_digest(Path(paths["generation_trace"]))
assert trace_ld_hash == usage_document["source_trace_sha256"]
print(f"length-delimited trace tree sha256: {trace_ld_hash} MATCH usage record")

assert audit["integrity"] == {
    "candidate_prompt_matches_trusted": True,
    "candidate_reference_semantics_matches_trusted": True,
    "candidate_translator_matches_trusted": True,
    "manifest_prompt_hash_matches_trusted": True,
    "manifest_reference_semantics_hash_matches_trusted": True,
    "manifest_translator_hash_matches_trusted": True,
}
print("launcher integrity claims are consistent with independent mounted-file checks")
print("PROVENANCE_CHECK=PASS")
