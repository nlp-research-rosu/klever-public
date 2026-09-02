#!/usr/bin/env python3
"""Independent provenance and mounted-input integrity checks for audit 134."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from pathlib import Path


AUDIT = Path("/audit-input.json")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def pipeline_tree_sha256(root: Path) -> str:
    """Independent reimplementation of the recorded pipeline workspace digest."""
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
                raise AssertionError(f"unsupported or linked tree entry: {path}")
    for relative, kind, path in sorted(entries):
        encoded = relative.encode()
        digest.update(len(encoded).to_bytes(4, "big"))
        digest.update(encoded)
        digest.update(kind.encode() + b"\0")
        if kind == "file":
            digest.update(path.stat(follow_symlinks=False).st_size.to_bytes(8, "big"))
            with path.open("rb") as stream:
                for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                    digest.update(chunk)
    return digest.hexdigest()


def require_regular(path: Path) -> None:
    mode = path.stat(follow_symlinks=False).st_mode
    assert stat.S_ISREG(mode), f"not a regular file: {path}"


audit = json.loads(AUDIT.read_text())
lock_path = Path(audit["container_paths"]["audit_campaign_lock"])
lock = json.loads(lock_path.read_text())
assert audit["audit_campaign"] == lock
assert sha256(lock_path) == audit["hashes"]["audit_campaign_lock_sha256"]
assert audit["record_layout"] == "legacy-selected-stage1"
assert audit["semantics_mode"] == "GENERATED_SEMANTICS"
assert not Path("/reference/reference-semantics").exists()

required = [
    Path("/run.json"),
    Path("/task.json"),
    Path("/generation-result.json"),
    Path("/generation-evidence/invocation.json"),
    Path("/generation-evidence/metrics.json"),
    Path("/generation-evidence/codex-last.txt"),
    Path("/generation-evidence/codex-output.log"),
    Path("/generation-evidence/prompt.txt"),
    Path("/generation-evidence/usage.json"),
    Path("/reference/canonical.py"),
    Path("/reference/prompt.py"),
    Path("/reference/py2mpy.py"),
]
for path in required:
    require_regular(path)

trace_files = sorted(Path("/generation-evidence/codex-trace").rglob("*"))
trace_regular = [p for p in trace_files if p.is_file() and not p.is_symlink()]
assert len(trace_regular) == 1
for path in trace_files:
    assert not path.is_symlink(), path

recorded = audit["hashes"]
direct_checks = {
    "/audit-campaign-lock.json": recorded["audit_campaign_lock_sha256"],
    "/run.json": recorded["run_manifest_sha256"],
    "/task.json": recorded["task_manifest_sha256"],
    "/generation-result.json": recorded["stage1_result_sha256"],
    "/generation-evidence/invocation.json": recorded["stage1_invocation_sha256"],
    "/generation-evidence/metrics.json": recorded["generation_metrics_sha256"],
    "/generation-evidence/usage.json": recorded["generation_usage_sha256"],
    "/generation-evidence/codex-last.txt": recorded["generation_codex_last_sha256"],
    "/generation-evidence/codex-output.log": recorded["generation_codex_output_sha256"],
    "/generation-evidence/prompt.txt": recorded["generation_prompt_sha256"],
    "/reference/canonical.py": recorded["canonical_sha256"],
    "/reference/prompt.py": recorded["trusted_prompt_sha256"],
    "/reference/py2mpy.py": recorded["trusted_translator_sha256"],
    "/candidate/prompt.py": recorded["candidate_prompt_sha256"],
    "/candidate/py2mpy.py": recorded["candidate_translator_sha256"],
}
for raw_path, expected in direct_checks.items():
    actual = sha256(Path(raw_path))
    assert actual == expected, (raw_path, expected, actual)
    print(f"SHA256 OK {raw_path} {actual}")

assert Path("/candidate/prompt.py").read_bytes() == Path("/reference/prompt.py").read_bytes()
assert Path("/candidate/py2mpy.py").read_bytes() == Path("/reference/py2mpy.py").read_bytes()

result = json.loads(Path("/generation-result.json").read_text())
invocation = json.loads(Path("/generation-evidence/invocation.json").read_text())
for rel, expected in result["outputs"]["evidence"].items():
    path = Path("/generation-evidence") / rel
    require_regular(path)
    actual = sha256(path)
    assert actual == expected, (rel, expected, actual)
    assert invocation["outputs"]["evidence"][rel] == expected
    print(f"GENERATION EVIDENCE OK {rel} {actual}")

candidate_digest = pipeline_tree_sha256(Path("/candidate"))
trace_digest = pipeline_tree_sha256(Path("/generation-evidence/codex-trace"))
assert candidate_digest == result["outputs"]["workspace_sha256"]
assert candidate_digest == invocation["retained_workspace_sha256"]
assert trace_digest == json.loads(Path("/generation-evidence/usage.json").read_text())[
    "source_trace_sha256"
]
print(f"CANDIDATE PIPELINE TREE OK {candidate_digest}")
print(f"TRACE PIPELINE TREE OK {trace_digest}")
print(
    "LAUNCHER_RECORDED_CANDIDATE_TREE_SHA256 "
    + recorded["candidate_tree_sha256"]
)
print(
    "LAUNCHER_RECORDED_GENERATION_TRACE_SHA256 "
    + recorded["generation_codex_trace_sha256"]
)
print(
    "NOTE aggregate launcher tree encodings are recorded above; independent "
    "verification uses every direct file hash plus the pipeline workspace/trace "
    "digest algorithm attested by generation-result.json and usage.json"
)

print("CANDIDATE FILE MANIFEST")
for path in sorted(Path("/candidate").iterdir()):
    assert path.is_file() and not path.is_symlink(), path
    print(f"{path.name}\t{path.stat().st_size}\t{sha256(path)}")

print("PROVENANCE_RESULT=PASS")
