#!/usr/bin/env python3
"""Independent mounted-input and launcher-record integrity checks."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from pathlib import Path


CHUNK = 1024 * 1024


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(CHUNK), b""):
            digest.update(chunk)
    return digest.hexdigest()


def pipeline_tree_sha256(root: Path) -> str:
    """Reimplement the length-delimited pipeline-v2 tree digest."""
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
        encoded = relative.encode()
        digest.update(len(encoded).to_bytes(4, "big"))
        digest.update(encoded)
        digest.update(kind.encode() + b"\0")
        if kind == "file":
            size = path.stat(follow_symlinks=False).st_size
            digest.update(size.to_bytes(8, "big"))
            with path.open("rb") as stream:
                for chunk in iter(lambda: stream.read(CHUNK), b""):
                    digest.update(chunk)
    return digest.hexdigest()


def require_regular(path: Path) -> None:
    assert path.is_file(), f"missing/non-file: {path}"
    assert not path.is_symlink(), f"symlinked required file: {path}"


def require_directory(path: Path) -> None:
    assert path.is_dir(), f"missing/non-directory: {path}"
    assert not path.is_symlink(), f"symlinked required directory: {path}"


audit = json.loads(Path("/audit-input.json").read_text(encoding="utf-8"))
lock = json.loads(Path("/audit-campaign-lock.json").read_text(encoding="utf-8"))
result = json.loads(Path("/generation-result.json").read_text(encoding="utf-8"))
usage = json.loads(
    Path("/generation-evidence/usage.json").read_text(encoding="utf-8")
)

assert audit["record_layout"] == "legacy-selected-stage1"
assert audit["semantics_mode"] == "GENERATED_SEMANTICS"
assert not audit["mount_reference_semantics"]
assert not Path("/reference/reference-semantics").exists()
assert lock == audit["audit_campaign"], "campaign lock differs from audit block"
assert file_sha256(Path("/audit-campaign-lock.json")) == audit["hashes"][
    "audit_campaign_lock_sha256"
]

required_files = [
    "/audit-input.json",
    "/audit-campaign-lock.json",
    "/run.json",
    "/task.json",
    "/generation-result.json",
    "/reference/canonical.py",
    "/reference/prompt.py",
    "/reference/py2mpy.py",
    "/generation-evidence/invocation.json",
    "/generation-evidence/metrics.json",
    "/generation-evidence/codex-last.txt",
    "/generation-evidence/codex-output.log",
    "/generation-evidence/prompt.txt",
    "/generation-evidence/usage.json",
]
required_directories = [
    "/candidate",
    "/generation-evidence",
    "/generation-evidence/codex-trace",
]
for name in required_files:
    require_regular(Path(name))
for name in required_directories:
    require_directory(Path(name))

trace_files = sorted(Path("/generation-evidence/codex-trace").rglob("*"))
assert trace_files, "empty structured trace"
for path in trace_files:
    assert not path.is_symlink(), f"symlinked trace entry: {path}"
    assert path.is_dir() or path.is_file(), f"mistyped trace entry: {path}"

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

hash_pairs = {
    "/reference/canonical.py": "canonical_sha256",
    "/reference/prompt.py": "trusted_prompt_sha256",
    "/reference/py2mpy.py": "trusted_translator_sha256",
    "/candidate/prompt.py": "candidate_prompt_sha256",
    "/candidate/py2mpy.py": "candidate_translator_sha256",
    "/run.json": "run_manifest_sha256",
    "/task.json": "task_manifest_sha256",
    "/generation-result.json": "stage1_result_sha256",
    "/generation-evidence/invocation.json": "stage1_invocation_sha256",
    "/generation-evidence/metrics.json": "generation_metrics_sha256",
    "/generation-evidence/usage.json": "generation_usage_sha256",
    "/generation-evidence/codex-last.txt": "generation_codex_last_sha256",
    "/generation-evidence/codex-output.log": "generation_codex_output_sha256",
    "/generation-evidence/prompt.txt": "generation_prompt_sha256",
}
for name, key in hash_pairs.items():
    observed = file_sha256(Path(name))
    expected = audit["hashes"][key]
    assert observed == expected, f"{name}: {observed} != {expected}"
    print(f"MATCH {key} {observed} {name}")

assert Path("/candidate/prompt.py").read_bytes() == Path(
    "/reference/prompt.py"
).read_bytes()
assert Path("/candidate/py2mpy.py").read_bytes() == Path(
    "/reference/py2mpy.py"
).read_bytes()
print("MATCH candidate prompt bytes == trusted prompt bytes")
print("MATCH candidate translator bytes == trusted translator bytes")

candidate_tree = pipeline_tree_sha256(Path("/candidate"))
trace_tree = pipeline_tree_sha256(Path("/generation-evidence/codex-trace"))
assert candidate_tree == result["outputs"]["workspace_sha256"]
assert trace_tree == usage["source_trace_sha256"]
print(
    "MATCH independent candidate tree (pipeline-v2 convention) "
    f"{candidate_tree}"
)
print(
    "MATCH independent trace tree (pipeline-v2 convention) "
    f"{trace_tree}"
)

trace_regular_files = [path for path in trace_files if path.is_file()]
assert len(trace_regular_files) == 1
trace_relative = trace_regular_files[0].relative_to(
    "/generation-evidence"
).as_posix()
trace_sha = file_sha256(trace_regular_files[0])
assert result["outputs"]["evidence"][trace_relative] == trace_sha
print(f"MATCH structured trace file {trace_sha} {trace_relative}")
print(
    "NOTE audit-input candidate_tree_sha256 and "
    "generation_codex_trace_sha256 use a launcher snapshot convention not "
    "declared in the record; the independently reproducible pipeline-v2 tree "
    "hashes above match the generation-result and usage records."
)
print("PROVENANCE_CHECK: PASS")
