#!/usr/bin/env python3
"""Independent integrity checks for the mounted 55-fib audit inputs."""

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
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def require_regular(path: Path) -> None:
    mode = path.lstat().st_mode
    assert stat.S_ISREG(mode), f"not a regular file: {path}"
    assert not path.is_symlink(), f"symlinked file: {path}"
    assert os.access(path, os.R_OK), f"unreadable file: {path}"


def tree_entries(root: Path) -> dict[str, tuple[str, int, str | None]]:
    """Return an lstat-based, symlink-sensitive independent tree manifest."""
    entries: dict[str, tuple[str, int, str | None]] = {}
    for path in sorted(root.rglob("*"), key=lambda item: item.relative_to(root).as_posix()):
        relative = path.relative_to(root).as_posix()
        mode = path.lstat().st_mode
        permissions = stat.S_IMODE(mode)
        if stat.S_ISDIR(mode):
            kind, digest = "directory", None
        elif stat.S_ISREG(mode):
            kind, digest = "file", sha256(path)
        elif stat.S_ISLNK(mode):
            kind, digest = "symlink", hashlib.sha256(os.readlink(path).encode()).hexdigest()
        else:
            kind, digest = f"other:{stat.S_IFMT(mode):o}", None
        entries[relative] = (kind, permissions, digest)
    return entries


def manifest_digest(entries: dict[str, tuple[str, int, str | None]]) -> str:
    digest = hashlib.sha256()
    for relative, (kind, permissions, content_digest) in entries.items():
        line = f"{kind}\0{permissions:o}\0{relative}\0{content_digest or ''}\n"
        digest.update(line.encode())
    return digest.hexdigest()


audit = json.loads(AUDIT_INPUT.read_text(encoding="utf-8"))
lock = json.loads(LOCK.read_text(encoding="utf-8"))
hashes = audit["hashes"]
container_paths = {key: Path(value) for key, value in audit["container_paths"].items()}

print(f"record_layout={audit['record_layout']}")
print(f"semantics_mode={audit['semantics_mode']}")
assert audit["record_layout"] == "legacy-selected-stage1"
assert audit["semantics_mode"] == "SUPPLIED_SEMANTICS"

require_regular(AUDIT_INPUT)
require_regular(LOCK)
assert audit["audit_campaign"] == lock
assert sha256(LOCK) == hashes["audit_campaign_lock_sha256"]
print(f"campaign_lock_sha256={sha256(LOCK)} structural_match=true")

for key, path in container_paths.items():
    mode = path.lstat().st_mode
    assert not stat.S_ISLNK(mode), f"launcher mount is symlinked: {key}={path}"
    assert os.access(path, os.R_OK), f"launcher mount is unreadable: {key}={path}"
    print(f"container_path[{key}]={path} type={'directory' if stat.S_ISDIR(mode) else 'file'}")

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
for path in required:
    require_regular(path)

usage = Path("/generation-evidence/usage.json")
if usage.exists():
    require_regular(usage)

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
    Path("/generation-evidence/prompt.txt"): "generation_prompt_sha256",
    Path("/generation-evidence/codex-last.txt"): "generation_codex_last_sha256",
    Path("/generation-evidence/codex-output.log"): "generation_codex_output_sha256",
    Path("/generation-evidence/usage.json"): "generation_usage_sha256",
}
for path, key in recorded_file_hashes.items():
    require_regular(path)
    actual = sha256(path)
    assert actual == hashes[key], f"{key}: recorded {hashes[key]}, actual {actual}"
    print(f"hash_ok {key}={actual} path={path}")

assert sha256(Path("/task.json")) == hashes["manifest_sha256"]
assert Path("/candidate/prompt.py").read_bytes() == Path("/reference/prompt.py").read_bytes()
assert Path("/candidate/py2mpy.py").read_bytes() == Path("/reference/py2mpy.py").read_bytes()
print("candidate_prompt_byte_identical=true")
print("candidate_translator_byte_identical=true")

candidate_tree = tree_entries(Path("/candidate"))
assert all(entry[0] in {"directory", "file"} for entry in candidate_tree.values())
print(f"candidate_entry_count={len(candidate_tree)}")
print(f"independent_candidate_manifest_sha256={manifest_digest(candidate_tree)}")

trusted_semantics = Path("/reference/reference-semantics")
candidate_semantics = Path("/candidate/reference-semantics")
assert trusted_semantics.is_dir() and not trusted_semantics.is_symlink()
assert candidate_semantics.is_dir() and not candidate_semantics.is_symlink()
trusted_entries = tree_entries(trusted_semantics)
candidate_entries = tree_entries(candidate_semantics)
assert candidate_entries == trusted_entries
assert all(entry[0] in {"directory", "file"} for entry in candidate_entries.values())
print(f"semantics_entry_count={len(trusted_entries)} recursive_exact_match=true")
print(f"independent_semantics_manifest_sha256={manifest_digest(trusted_entries)}")

trace_root = Path("/generation-evidence/codex-trace")
assert trace_root.is_dir() and not trace_root.is_symlink()
trace_entries = tree_entries(trace_root)
trace_files = [
    trace_root / relative
    for relative, (kind, _, _) in trace_entries.items()
    if kind == "file"
]
assert len(trace_files) == 1, trace_files
trace_result = json.loads(Path("/generation-result.json").read_text(encoding="utf-8"))
trace_relative = trace_files[0].relative_to(Path("/generation-evidence")).as_posix()
recorded_trace_hash = trace_result["outputs"]["evidence"][trace_relative]
actual_trace_hash = sha256(trace_files[0])
assert actual_trace_hash == recorded_trace_hash
print(f"trace_file={trace_relative} sha256={actual_trace_hash}")
print(f"independent_trace_manifest_sha256={manifest_digest(trace_entries)}")

bad_json_lines: list[int] = []
line_count = 0
for line_count, line in enumerate(trace_files[0].open(encoding="utf-8"), 1):
    try:
        json.loads(line)
    except json.JSONDecodeError:
        bad_json_lines.append(line_count)
assert not bad_json_lines
print(f"trace_json_lines={line_count} invalid_lines=0")

invocation = json.loads(Path("/generation-evidence/invocation.json").read_text(encoding="utf-8"))
for relative, expected in invocation["outputs"]["evidence"].items():
    artifact = Path("/generation-evidence") / relative
    require_regular(artifact)
    actual = sha256(artifact)
    assert actual == expected, f"{relative}: recorded {expected}, actual {actual}"
    print(f"invocation_output_hash_ok path={relative} sha256={actual}")

for name, claimed in audit["integrity"].items():
    assert claimed is True, f"launcher integrity field was not true: {name}={claimed!r}"
print("launcher_integrity_fields=true; independently_recomputed_checks=true")
print("stage1_status=PASS")
