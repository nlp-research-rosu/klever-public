#!/usr/bin/env python3
"""Independent provenance and mounted-input integrity checks."""

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


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def pipeline_tree_digest(root: Path) -> str:
    """Reimplement /opt/humaneval/tools/pipeline_contract.py:sha256_tree."""
    if root.is_symlink() or not root.is_dir():
        raise AssertionError(f"not a real directory: {root}")
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


def tree_manifest(root: Path) -> dict[str, tuple[str, str | None]]:
    if root.is_symlink() or not root.is_dir():
        raise AssertionError(f"not a real directory: {root}")
    result: dict[str, tuple[str, str | None]] = {}
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root).as_posix()
        mode = path.lstat().st_mode
        if stat.S_ISDIR(mode):
            result[relative] = ("directory", None)
        elif stat.S_ISREG(mode):
            result[relative] = ("file", sha256_file(path))
        else:
            result[relative] = ("unsupported", None)
    return result


print("COMMAND: python3 /audit-output/evidence/01_integrity.py")
audit = json.loads(AUDIT_INPUT.read_text())
lock = json.loads(LOCK.read_text())
assert audit["record_layout"] == "pipeline-v3"
assert audit["semantics_mode"] == "SUPPLIED_SEMANTICS"
assert audit["audit_campaign"] == lock
assert sha256_file(LOCK) == audit["hashes"]["audit_campaign_lock_sha256"]
print("campaign_lock: exact object and SHA-256 match")

required_regular = [
    Path("/run.json"),
    Path("/task.json"),
    Path("/generation-result.json"),
    GENERATION / "invocation.json",
    GENERATION / "metrics.json",
    GENERATION / "runtime-metrics.json",
    GENERATION / "usage.json",
    GENERATION / "codex-last.txt",
    GENERATION / "codex-output.log",
    GENERATION / "prompt.txt",
    REFERENCE / "canonical.py",
    REFERENCE / "prompt.py",
    REFERENCE / "py2mpy.py",
]
for path in required_regular:
    assert path.is_file() and not path.is_symlink(), path
print(f"required_regular_records: {len(required_regular)} present, regular, non-symlink")

expected_hashes = {
    LOCK: "audit_campaign_lock_sha256",
    REFERENCE / "canonical.py": "canonical_sha256",
    REFERENCE / "prompt.py": "trusted_prompt_sha256",
    REFERENCE / "py2mpy.py": "trusted_translator_sha256",
    Path("/run.json"): "run_manifest_sha256",
    Path("/task.json"): "task_manifest_sha256",
    Path("/generation-result.json"): "stage1_result_sha256",
    GENERATION / "invocation.json": "stage1_invocation_sha256",
    GENERATION / "metrics.json": "generation_metrics_sha256",
    GENERATION / "runtime-metrics.json": "generation_runtime_metrics_sha256",
    GENERATION / "usage.json": "generation_usage_sha256",
    GENERATION / "codex-last.txt": "generation_codex_last_sha256",
    GENERATION / "codex-output.log": "generation_codex_output_sha256",
    GENERATION / "prompt.txt": "generation_prompt_sha256",
}
for path, key in expected_hashes.items():
    actual = sha256_file(path)
    expected = audit["hashes"][key]
    assert actual == expected, (path, actual, expected)
    print(f"sha256 {path} {actual}")

assert (REFERENCE / "reference-semantics").is_dir()
assert not (REFERENCE / "reference-semantics").is_symlink()
assert (CANDIDATE / "reference-semantics").is_dir()
assert not (CANDIDATE / "reference-semantics").is_symlink()
trusted_semantics = tree_manifest(REFERENCE / "reference-semantics")
candidate_semantics = tree_manifest(CANDIDATE / "reference-semantics")
assert trusted_semantics == candidate_semantics
assert all(kind != "unsupported" for kind, _ in trusted_semantics.values())
print(f"reference_semantics_recursive_identity: {len(trusted_semantics)} entries")
trusted_semantics_digest = pipeline_tree_digest(REFERENCE / "reference-semantics")
candidate_semantics_digest = pipeline_tree_digest(CANDIDATE / "reference-semantics")
assert trusted_semantics_digest == candidate_semantics_digest
assert trusted_semantics_digest == audit["hashes"]["trusted_reference_semantics_manifest_sha256"]
print(f"reference_semantics_pipeline_tree_sha256: {trusted_semantics_digest}")

assert (CANDIDATE / "prompt.py").read_bytes() == (REFERENCE / "prompt.py").read_bytes()
assert (CANDIDATE / "py2mpy.py").read_bytes() == (REFERENCE / "py2mpy.py").read_bytes()
print("candidate prompt and translator: byte-identical to trusted mounts")

trace_files = sorted((GENERATION / "codex-trace").rglob("*"))
assert trace_files
assert all(not path.is_symlink() for path in trace_files)
trace_regular = [path for path in trace_files if path.is_file()]
assert len(trace_regular) == 1
result = json.loads(Path("/generation-result.json").read_text())
relative_trace = trace_regular[0].relative_to(GENERATION).as_posix()
assert sha256_file(trace_regular[0]) == result["outputs"]["evidence"][relative_trace]
trace_rows = [json.loads(line) for line in trace_regular[0].read_text().splitlines()]
assert len(trace_rows) == 437
trace_digest = pipeline_tree_digest(GENERATION / "codex-trace")
usage = json.loads((GENERATION / "usage.json").read_text())
assert trace_digest == usage["source_trace_sha256"]
print(f"trace: 1 regular JSONL, 437 parsed records, tree SHA-256 {trace_digest}")

candidate_digest = pipeline_tree_digest(CANDIDATE)
assert candidate_digest == result["outputs"]["workspace_sha256"]
print(f"candidate_pipeline_tree_sha256: {candidate_digest}")

proof_artifacts = [
    "solution.py",
    "solution.mpy",
    "verification.k",
    "spec.k",
    "prove.sh",
    "PROOF.md",
]
for name in proof_artifacts:
    path = CANDIDATE / name
    assert path.is_file() and not path.is_symlink() and path.stat().st_size > 0
print("required candidate proof artifacts: present, regular, nonempty, non-symlink")
print("RESULT: PASS")
