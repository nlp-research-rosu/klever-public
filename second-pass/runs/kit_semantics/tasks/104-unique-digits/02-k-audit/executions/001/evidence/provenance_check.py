#!/usr/bin/env python3
"""Read-only integrity checks for the launcher-owned pipeline-v3 records."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from pathlib import Path


AUDIT = Path("/audit-input.json")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def pipeline_tree_hash(root: Path) -> str:
    """Independent implementation of pipeline_contract.sha256_tree."""
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
                raise AssertionError(f"linked/unsupported tree entry: {path}")
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


document = json.loads(AUDIT.read_text(encoding="utf-8"))
assert document["record_layout"] == "pipeline-v3"
assert document["semantics_mode"] == "SUPPLIED_SEMANTICS"

required_files = [
    Path("/audit-input.json"),
    Path("/audit-campaign-lock.json"),
    Path("/run.json"),
    Path("/task.json"),
    Path("/generation-result.json"),
    Path("/reference/canonical.py"),
    Path("/reference/prompt.py"),
    Path("/reference/py2mpy.py"),
    Path("/generation-evidence/invocation.json"),
    Path("/generation-evidence/metrics.json"),
    Path("/generation-evidence/runtime-metrics.json"),
    Path("/generation-evidence/usage.json"),
    Path("/generation-evidence/codex-last.txt"),
    Path("/generation-evidence/codex-output.log"),
    Path("/generation-evidence/prompt.txt"),
]
required_dirs = [
    Path("/candidate"),
    Path("/reference/reference-semantics"),
    Path("/generation-evidence/codex-trace"),
]
for path in required_files:
    assert path.is_file() and not path.is_symlink(), path
    print(f"OK regular file {path}")
for path in required_dirs:
    assert path.is_dir() and not path.is_symlink(), path
    print(f"OK real directory {path}")

lock = json.loads(Path("/audit-campaign-lock.json").read_text(encoding="utf-8"))
assert lock == document["audit_campaign"]
print("OK campaign JSON equals audit-input campaign block")

hashes = document["hashes"]
file_checks = {
    "audit_campaign_lock_sha256": Path("/audit-campaign-lock.json"),
    "canonical_sha256": Path("/reference/canonical.py"),
    "trusted_prompt_sha256": Path("/reference/prompt.py"),
    "trusted_translator_sha256": Path("/reference/py2mpy.py"),
    "candidate_prompt_sha256": Path("/candidate/prompt.py"),
    "candidate_translator_sha256": Path("/candidate/py2mpy.py"),
    "stage1_invocation_sha256": Path("/generation-evidence/invocation.json"),
    "generation_metrics_sha256": Path("/generation-evidence/metrics.json"),
    "generation_runtime_metrics_sha256": Path(
        "/generation-evidence/runtime-metrics.json"
    ),
    "generation_usage_sha256": Path("/generation-evidence/usage.json"),
    "generation_codex_last_sha256": Path(
        "/generation-evidence/codex-last.txt"
    ),
    "generation_codex_output_sha256": Path(
        "/generation-evidence/codex-output.log"
    ),
    "generation_prompt_sha256": Path("/generation-evidence/prompt.txt"),
    "run_manifest_sha256": Path("/run.json"),
    "task_manifest_sha256": Path("/task.json"),
    "stage1_result_sha256": Path("/generation-result.json"),
}
for key, path in file_checks.items():
    actual = sha256_file(path)
    assert actual == hashes[key], (key, actual, hashes[key])
    print(f"OK {key} {actual} {path}")

task = json.loads(Path("/task.json").read_text(encoding="utf-8"))
embedded_manifest = dict(document["manifest"])
embedded_config = embedded_manifest.pop("config")
assert embedded_config == document["manifest_config"]
assert task == embedded_manifest
print("OK task.json equals task-owned fields in audit-input manifest block")
print("OK audit-input launcher-added manifest config matches manifest_config")

result = json.loads(Path("/generation-result.json").read_text(encoding="utf-8"))
invocation = json.loads(
    Path("/generation-evidence/invocation.json").read_text(encoding="utf-8")
)
assert result["outputs"] == invocation["outputs"]
for relative, expected in result["outputs"]["evidence"].items():
    path = Path("/generation-evidence") / relative
    assert path.is_file() and not path.is_symlink(), path
    actual = sha256_file(path)
    assert actual == expected, (path, actual, expected)
    print(f"OK generation result evidence {actual} {relative}")

trusted_semantics_hash = pipeline_tree_hash(
    Path("/reference/reference-semantics")
)
candidate_semantics_hash = pipeline_tree_hash(
    Path("/candidate/reference-semantics")
)
candidate_hash = pipeline_tree_hash(Path("/candidate"))
trace_hash = pipeline_tree_hash(Path("/generation-evidence/codex-trace"))
assert trusted_semantics_hash == hashes[
    "trusted_reference_semantics_manifest_sha256"
]
assert candidate_semantics_hash == trusted_semantics_hash
assert candidate_hash == result["outputs"]["workspace_sha256"]
assert trace_hash == json.loads(
    Path("/generation-evidence/usage.json").read_text(encoding="utf-8")
)["source_trace_sha256"]
print(f"OK trusted supplied-semantics tree {trusted_semantics_hash}")
print(f"OK candidate supplied-semantics tree {candidate_semantics_hash}")
print(f"OK mounted candidate pipeline tree {candidate_hash}")
print(f"OK structured trace pipeline tree {trace_hash}")

trace_files = sorted(Path("/generation-evidence/codex-trace").rglob("*"))
trace_lines = 0
for path in trace_files:
    if path.is_file():
        assert not path.is_symlink(), path
        for line_number, line in enumerate(
            path.read_text(encoding="utf-8").splitlines(), 1
        ):
            try:
                json.loads(line)
            except json.JSONDecodeError as error:
                raise AssertionError(f"{path}:{line_number}: {error}") from error
            trace_lines += 1
print(f"OK structured trace JSONL records={trace_lines}")

print("PROVENANCE_CHECK: PASS")
