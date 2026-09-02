#!/usr/bin/env python3
"""Independent audit of launcher records, mounted paths, and recorded hashes."""

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
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def require_regular(path: Path) -> None:
    assert path.exists(), f"missing: {path}"
    assert not path.is_symlink(), f"symlink not allowed: {path}"
    assert path.is_file(), f"not a regular file: {path}"


def pipeline_sha256_tree(root: Path) -> str:
    """Reimplement the recorded pipeline workspace/tree digest."""
    digest = hashlib.sha256()
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
                raise AssertionError(f"linked or unsupported tree entry: {path}")
    for relative, kind, path in sorted(entries):
        encoded = relative.encode()
        digest.update(len(encoded).to_bytes(4, "big"))
        digest.update(encoded)
        digest.update(kind.encode() + b"\0")
        if kind == "file":
            digest.update(path.stat(follow_symlinks=False).st_size.to_bytes(8, "big"))
            digest.update(path.read_bytes())
    return digest.hexdigest()


audit = json.loads(AUDIT_INPUT.read_text())
lock = json.loads(LOCK.read_text())
assert audit["record_layout"] == "legacy-selected-stage1"
assert audit["semantics_mode"] == "GENERATED_SEMANTICS"
assert lock == audit["audit_campaign"], "campaign lock does not match audit_campaign"
assert sha256(LOCK) == audit["hashes"]["audit_campaign_lock_sha256"]

paths = audit["container_paths"]
required_launcher = [
    Path(paths["audit_campaign_lock"]),
    Path(paths["candidate"]),
    Path(paths["canonical"]),
    Path(paths["generation_last"]),
    Path(paths["generation_manifest"]),
    Path(paths["generation_metrics"]),
    Path(paths["generation_output"]),
    Path(paths["generation_root"]),
    Path(paths["generation_trace"]),
    Path(paths["run_manifest"]),
    Path(paths["stage1_result"]),
    Path(paths["task_manifest"]),
    Path(paths["translator"]),
    Path(paths["trusted_prompt"]),
]
for path in required_launcher:
    assert path.exists(), f"missing launcher-declared mount: {path}"
    assert not path.is_symlink(), f"launcher-declared mount is symlinked: {path}"

required_layout = [
    Path("/run.json"),
    Path("/task.json"),
    Path("/generation-result.json"),
    Path("/generation-evidence/invocation.json"),
    Path("/generation-evidence/metrics.json"),
    Path("/generation-evidence/codex-last.txt"),
    Path("/generation-evidence/codex-output.log"),
    Path("/generation-evidence/prompt.txt"),
]
for path in required_layout:
    require_regular(path)
usage = Path("/generation-evidence/usage.json")
if usage.exists():
    require_regular(usage)

assert not Path("/reference/reference-semantics").exists(), (
    "reference semantics unexpectedly mounted in GENERATED_SEMANTICS mode"
)

candidate_required = [
    Path("/candidate/prompt.py"),
    Path("/candidate/py2mpy.py"),
    Path("/candidate/solution.py"),
    Path("/candidate/solution.mpy"),
    Path("/candidate/semantic.k"),
    Path("/candidate/verification.k"),
    Path("/candidate/spec.k"),
    Path("/candidate/prove.sh"),
]
for path in candidate_required:
    require_regular(path)

checks = {
    Path("/reference/canonical.py"): audit["hashes"]["canonical_sha256"],
    Path("/reference/prompt.py"): audit["hashes"]["trusted_prompt_sha256"],
    Path("/reference/py2mpy.py"): audit["hashes"]["trusted_translator_sha256"],
    Path("/candidate/prompt.py"): audit["hashes"]["candidate_prompt_sha256"],
    Path("/candidate/py2mpy.py"): audit["hashes"]["candidate_translator_sha256"],
    Path("/run.json"): audit["hashes"]["run_manifest_sha256"],
    Path("/task.json"): audit["hashes"]["task_manifest_sha256"],
    Path("/generation-result.json"): audit["hashes"]["stage1_result_sha256"],
    Path("/generation-evidence/invocation.json"): audit["hashes"]["stage1_invocation_sha256"],
    Path("/generation-evidence/metrics.json"): audit["hashes"]["generation_metrics_sha256"],
    Path("/generation-evidence/codex-last.txt"): audit["hashes"]["generation_codex_last_sha256"],
    Path("/generation-evidence/codex-output.log"): audit["hashes"]["generation_codex_output_sha256"],
    Path("/generation-evidence/prompt.txt"): audit["hashes"]["generation_prompt_sha256"],
}
if usage.exists():
    checks[usage] = audit["hashes"]["generation_usage_sha256"]
for path, expected in checks.items():
    require_regular(path)
    actual = sha256(path)
    assert actual == expected, f"hash mismatch: {path}: {actual} != {expected}"
    print(f"OK sha256 {actual} {path}")

assert Path("/candidate/prompt.py").read_bytes() == Path("/reference/prompt.py").read_bytes()
assert Path("/candidate/py2mpy.py").read_bytes() == Path("/reference/py2mpy.py").read_bytes()
assert audit["integrity"]["candidate_prompt_matches_trusted"] is True
assert audit["integrity"]["candidate_translator_matches_trusted"] is True

invocation = json.loads(Path("/generation-evidence/invocation.json").read_text())
generation_result = json.loads(Path("/generation-result.json").read_text())
for relative, expected in invocation["outputs"]["evidence"].items():
    path = Path("/generation-evidence") / relative
    require_regular(path)
    actual = sha256(path)
    assert actual == expected, f"invocation output hash mismatch: {relative}"
    print(f"OK invocation sha256 {actual} {path}")

candidate_pipeline_hash = pipeline_sha256_tree(Path("/candidate"))
assert candidate_pipeline_hash == invocation["retained_workspace_sha256"]
assert candidate_pipeline_hash == invocation["outputs"]["workspace_sha256"]
assert candidate_pipeline_hash == generation_result["outputs"]["workspace_sha256"]
print(f"OK pipeline_tree_sha256 {candidate_pipeline_hash} /candidate")

trace_pipeline_hash = pipeline_sha256_tree(Path("/generation-evidence/codex-trace"))
usage_record = json.loads(usage.read_text())
assert trace_pipeline_hash == usage_record["source_trace_sha256"]
print(f"OK pipeline_tree_sha256 {trace_pipeline_hash} /generation-evidence/codex-trace")

for root in (Path("/candidate"), Path("/generation-evidence/codex-trace")):
    print(f"TREE {root}")
    manifest_digest = hashlib.sha256()
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root).as_posix()
        if path.is_symlink():
            raise AssertionError(f"symlinked tree entry: {path}")
        if path.is_dir():
            print(f"DIR  {relative}")
            manifest_digest.update(f"D {relative}\n".encode())
        elif path.is_file():
            digest = sha256(path)
            print(f"FILE {digest} {relative}")
            manifest_digest.update(f"F {relative} {digest}\n".encode())
        else:
            raise AssertionError(f"mistyped tree entry: {path}")
    print(f"INDEPENDENT_TREE_MANIFEST_SHA256 {manifest_digest.hexdigest()} {root}")

print("PASS launcher/provenance integrity checks")
