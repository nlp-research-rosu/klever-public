#!/usr/bin/env python3
"""Independent integrity checks for the launcher-owned audit inputs."""

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


def file_kind(path: Path) -> str:
    mode = path.lstat().st_mode
    if stat.S_ISREG(mode):
        return "regular"
    if stat.S_ISDIR(mode):
        return "directory"
    if stat.S_ISLNK(mode):
        return "symlink"
    return f"other({oct(mode)})"


def launcher_tree_sha256(root: Path) -> str:
    """Reproduce the launcher tree digest documented in pipeline_contract.py."""
    digest = hashlib.sha256()
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
                raise AssertionError(f"linked or unsupported tree entry: {path}")
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


def export_tree_sha256(root: Path) -> str:
    """Reproduce the export-side digest used for audit mount provenance."""
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
                raise AssertionError(f"linked or unsupported tree entry: {path}")
    digest = hashlib.sha256()
    for relative, kind, path in sorted(entries):
        digest.update(relative.encode() + b"\0" + kind.encode() + b"\0")
        if kind == "file":
            digest.update(path.read_bytes())
    return digest.hexdigest()


def require_regular(path: Path) -> None:
    assert path.exists(), f"missing required file: {path}"
    assert not path.is_symlink(), f"symlinked required file: {path}"
    assert path.is_file(), f"required path is not a regular file: {path}"
    with path.open("rb") as stream:
        stream.read(1)


audit = json.loads(AUDIT_INPUT.read_text())
lock = json.loads(LOCK.read_text())

print(f"audit-input sha256={sha256(AUDIT_INPUT)}")
print(f"audit-campaign-lock sha256={sha256(LOCK)}")
print(f"record_layout={audit['record_layout']}")
print(f"semantics_mode={audit['semantics_mode']}")
print(f"campaign_block_equal_lock={audit['audit_campaign'] == lock}")
assert audit["audit_campaign"] == lock
assert sha256(LOCK) == audit["hashes"]["audit_campaign_lock_sha256"]

required = [
    Path("/run.json"),
    Path("/task.json"),
    Path("/generation-result.json"),
    Path("/generation-evidence/invocation.json"),
    Path("/generation-evidence/metrics.json"),
    Path("/generation-evidence/codex-last.txt"),
    Path("/generation-evidence/codex-output.log"),
    Path("/generation-evidence/prompt.txt"),
]
usage = Path("/generation-evidence/usage.json")
if usage.exists() or usage.is_symlink():
    required.append(usage)

for path in [AUDIT_INPUT, LOCK, *required]:
    require_regular(path)
    print(f"required_record {file_kind(path)} {path} sha256={sha256(path)}")

declared_hashes = {
    Path("/run.json"): "run_manifest_sha256",
    Path("/task.json"): "task_manifest_sha256",
    Path("/generation-result.json"): "stage1_result_sha256",
    Path("/generation-evidence/invocation.json"): "stage1_invocation_sha256",
    Path("/generation-evidence/metrics.json"): "generation_metrics_sha256",
    Path("/generation-evidence/usage.json"): "generation_usage_sha256",
    Path("/generation-evidence/codex-last.txt"): "generation_codex_last_sha256",
    Path("/generation-evidence/codex-output.log"): "generation_codex_output_sha256",
    Path("/generation-evidence/prompt.txt"): "generation_prompt_sha256",
    Path("/reference/canonical.py"): "canonical_sha256",
    Path("/reference/prompt.py"): "trusted_prompt_sha256",
    Path("/reference/py2mpy.py"): "trusted_translator_sha256",
    Path("/candidate/prompt.py"): "candidate_prompt_sha256",
    Path("/candidate/py2mpy.py"): "candidate_translator_sha256",
}
for path, key in declared_hashes.items():
    require_regular(path)
    actual = sha256(path)
    expected = audit["hashes"][key]
    print(f"declared_hash {key} expected={expected} actual={actual} match={actual == expected}")
    assert actual == expected

trace_files = sorted(Path("/generation-evidence/codex-trace").rglob("*"))
trace_regular = [path for path in trace_files if path.is_file() and not path.is_symlink()]
assert trace_regular, "structured trace has no regular files"
for path in trace_files:
    assert not path.is_symlink(), f"symlink in structured trace: {path}"
for path in trace_regular:
    print(f"trace_file {path} sha256={sha256(path)}")

print(
    "audit_recorded_tree_hash "
    f"candidate_tree_sha256={audit['hashes']['candidate_tree_sha256']}"
)
print(
    "audit_recorded_tree_hash "
    f"generation_codex_trace_sha256={audit['hashes']['generation_codex_trace_sha256']}"
)

generation_result = json.loads(Path("/generation-result.json").read_text())
workspace_expected = generation_result["outputs"]["workspace_sha256"]
workspace_actual = launcher_tree_sha256(Path("/candidate"))
print(
    "stage1_workspace_tree_hash "
    f"expected={workspace_expected} actual={workspace_actual} "
    f"match={workspace_actual == workspace_expected}"
)
assert workspace_actual == workspace_expected
usage_document = json.loads(Path("/generation-evidence/usage.json").read_text())
trace_expected = usage_document["source_trace_sha256"]
trace_actual = launcher_tree_sha256(Path("/generation-evidence/codex-trace"))
print(
    "usage_source_trace_tree_hash "
    f"expected={trace_expected} actual={trace_actual} "
    f"match={trace_actual == trace_expected}"
)
assert trace_actual == trace_expected
for relpath, expected in sorted(generation_result["outputs"]["evidence"].items()):
    path = Path("/generation-evidence") / relpath
    require_regular(path)
    actual = sha256(path)
    print(f"stage1_output {relpath} expected={expected} actual={actual} match={actual == expected}")
    assert actual == expected

for key, raw_path in sorted(audit["container_paths"].items()):
    path = Path(raw_path)
    exists = path.exists()
    kind = file_kind(path) if exists or path.is_symlink() else "absent"
    print(f"container_path {key} path={path} exists={exists} kind={kind}")
    assert exists, f"launcher-declared provenance mount absent: {key}={path}"
    assert not path.is_symlink(), f"launcher-declared provenance mount is symlink: {key}={path}"

assert not Path("/reference/reference-semantics").exists()
assert audit["mount_reference_semantics"] is False
assert audit["reference_semantics"] is None
print("generated_semantics_boundary reference-semantics=absent expected=absent")

for root in [Path("/candidate"), Path("/reference"), Path("/generation-evidence")]:
    for path in sorted(root.rglob("*")):
        if path.is_symlink():
            raise AssertionError(f"symlinked mounted artifact: {path}")
        if path.is_file():
            print(f"mounted_file root={root} path={path} sha256={sha256(path)}")
        elif path.is_dir():
            print(f"mounted_dir root={root} path={path}")
        else:
            raise AssertionError(f"mistyped mounted artifact: {path}")

assert Path("/candidate/prompt.py").read_bytes() == Path("/reference/prompt.py").read_bytes()
assert Path("/candidate/py2mpy.py").read_bytes() == Path("/reference/py2mpy.py").read_bytes()
print("candidate_prompt_byte_identity=true")
print("candidate_translator_byte_identity=true")
print("stage1_integrity_result=PASS")
