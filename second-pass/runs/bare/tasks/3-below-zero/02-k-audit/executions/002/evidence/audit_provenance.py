#!/usr/bin/env python3
"""Independent read-only integrity checks for the mounted audit inputs."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def require_regular(path: Path) -> None:
    assert path.exists(), f"missing: {path}"
    assert path.is_file(), f"not a regular file: {path}"
    assert not path.is_symlink(), f"symlinked: {path}"
    with path.open("rb") as stream:
        stream.read(1)


audit = json.loads(AUDIT_INPUT.read_text())
assert audit["record_layout"] == "legacy-selected-stage1"
assert audit["semantics_mode"] == "GENERATED_SEMANTICS"

lock_path = Path(audit["container_paths"]["audit_campaign_lock"])
require_regular(lock_path)
lock = json.loads(lock_path.read_text())
assert lock == audit["audit_campaign"]
assert sha256(lock_path) == audit["hashes"]["audit_campaign_lock_sha256"]

required_hashes = {
    Path("/reference/canonical.py"): "canonical_sha256",
    Path("/reference/prompt.py"): "trusted_prompt_sha256",
    Path("/reference/py2mpy.py"): "trusted_translator_sha256",
    Path("/run.json"): "run_manifest_sha256",
    Path("/task.json"): "task_manifest_sha256",
    Path("/generation-result.json"): "stage1_result_sha256",
    Path("/generation-evidence/invocation.json"): "stage1_invocation_sha256",
    Path("/generation-evidence/metrics.json"): "generation_metrics_sha256",
    Path("/generation-evidence/codex-last.txt"): "generation_codex_last_sha256",
    Path("/generation-evidence/codex-output.log"): "generation_codex_output_sha256",
    Path("/generation-evidence/prompt.txt"): "generation_prompt_sha256",
    Path("/generation-evidence/usage.json"): "generation_usage_sha256",
}
for path, key in required_hashes.items():
    require_regular(path)
    actual = sha256(path)
    expected = audit["hashes"][key]
    assert actual == expected, f"{path}: {actual} != {expected}"
    print(f"HASH_OK {actual} {path}")

candidate_required = [
    "prompt.py",
    "py2mpy.py",
    "solution.py",
    "solution.mpy",
    "semantic.k",
    "verification.k",
    "spec.k",
    "prove.sh",
]
for name in candidate_required:
    require_regular(Path("/candidate") / name)

assert Path("/candidate/prompt.py").read_bytes() == Path("/reference/prompt.py").read_bytes()
assert Path("/candidate/py2mpy.py").read_bytes() == Path("/reference/py2mpy.py").read_bytes()
assert not Path("/reference/reference-semantics").exists()
assert not any(Path("/candidate").rglob("reference-semantics"))

trace_root = Path(audit["container_paths"]["generation_trace"])
assert trace_root.is_dir() and not trace_root.is_symlink()
trace_files = sorted(trace_root.rglob("*"))
trace_files = [path for path in trace_files if path.is_file()]
assert trace_files, "structured trace is empty"
for path in trace_files:
    assert not path.is_symlink()
    count = 0
    with path.open() as stream:
        for count, line in enumerate(stream, 1):
            json.loads(line)
    print(f"TRACE_JSONL_OK lines={count} sha256={sha256(path)} {path}")

result = json.loads(Path("/generation-result.json").read_text())
for relative, expected in result["outputs"]["evidence"].items():
    path = Path("/generation-evidence") / relative
    require_regular(path)
    actual = sha256(path)
    assert actual == expected, f"generation-result mismatch for {path}"
    print(f"GENERATION_RESULT_HASH_OK {actual} {path}")

for root in (Path("/candidate"), Path("/generation-evidence")):
    symlinks = sorted(path for path in root.rglob("*") if path.is_symlink())
    assert not symlinks, f"symlinks found below {root}: {symlinks}"

print("CAMPAIGN_LOCK_EXACT_MATCH")
print("CANDIDATE_PROMPT_BYTE_IDENTICAL")
print("CANDIDATE_TRANSLATOR_BYTE_IDENTICAL")
print("GENERATED_SEMANTICS_BOUNDARY_OK")
print("NO_SYMLINKS_IN_CANDIDATE_OR_GENERATION_EVIDENCE")
print("PROVENANCE_CHECK_PASS")
