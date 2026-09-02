#!/usr/bin/env python3
"""Independent integrity checks for audit stage 1.

This script is reviewer-authored.  It treats every mounted record as data,
checks regular-file/directory status without following symlinks, validates all
JSON/JSONL syntax, and recomputes the launcher-declared per-file hashes.
"""

from __future__ import annotations

import hashlib
import json
import os
import stat
import sys
from pathlib import Path


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    raise SystemExit(1)


def regular_file(path: Path) -> None:
    try:
        mode = path.lstat().st_mode
    except OSError as error:
        fail(f"missing or unreadable file {path}: {error}")
    if not stat.S_ISREG(mode):
        fail(f"not a real regular file: {path}")


def real_directory(path: Path) -> None:
    try:
        mode = path.lstat().st_mode
    except OSError as error:
        fail(f"missing or unreadable directory {path}: {error}")
    if not stat.S_ISDIR(mode):
        fail(f"not a real directory: {path}")


def sha256_file(path: Path) -> str:
    regular_file(path)
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_object(path: Path) -> dict[str, object]:
    regular_file(path)
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        fail(f"invalid JSON object {path}: {error}")
    if not isinstance(value, dict):
        fail(f"JSON root is not an object: {path}")
    return value


def walk_real_tree(root: Path) -> list[Path]:
    real_directory(root)
    result: list[Path] = []
    pending = [root]
    while pending:
        directory = pending.pop()
        try:
            entries = list(os.scandir(directory))
        except OSError as error:
            fail(f"cannot scan {directory}: {error}")
        for entry in entries:
            path = Path(entry.path)
            mode = entry.stat(follow_symlinks=False).st_mode
            if stat.S_ISDIR(mode):
                pending.append(path)
            elif not stat.S_ISREG(mode):
                fail(f"linked or unsupported tree entry: {path}")
            result.append(path)
    return sorted(result)


audit_input_path = Path("/audit-input.json")
campaign_lock_path = Path("/audit-campaign-lock.json")
audit_input = load_object(audit_input_path)
campaign_lock = load_object(campaign_lock_path)

if audit_input.get("record_layout") != "legacy-selected-stage1":
    fail(f"unexpected record_layout={audit_input.get('record_layout')!r}")
if audit_input.get("semantics_mode") != "GENERATED_SEMANTICS":
    fail(f"unexpected semantics_mode={audit_input.get('semantics_mode')!r}")
if audit_input.get("audit_campaign") != campaign_lock:
    fail("audit_campaign object does not exactly match campaign lock")

container_paths = audit_input.get("container_paths")
if not isinstance(container_paths, dict):
    fail("container_paths is not an object")
for key, value in sorted(container_paths.items()):
    if not isinstance(value, str) or not value.startswith("/"):
        fail(f"malformed container path {key}={value!r}")

required_files = [
    audit_input_path,
    campaign_lock_path,
    Path("/run.json"),
    Path("/task.json"),
    Path("/generation-result.json"),
    Path("/reference/canonical.py"),
    Path("/reference/prompt.py"),
    Path("/reference/py2mpy.py"),
    Path("/generation-evidence/invocation.json"),
    Path("/generation-evidence/metrics.json"),
    Path("/generation-evidence/usage.json"),
    Path("/generation-evidence/codex-last.txt"),
    Path("/generation-evidence/codex-output.log"),
    Path("/generation-evidence/prompt.txt"),
]
for path in required_files:
    regular_file(path)

required_dirs = [
    Path("/candidate"),
    Path("/generation-evidence"),
    Path("/generation-evidence/codex-trace"),
    Path("/reference"),
]
for path in required_dirs:
    real_directory(path)

if Path("/reference/reference-semantics").exists() or Path(
    "/reference/reference-semantics"
).is_symlink():
    fail("reference semantics exists in GENERATED_SEMANTICS mode")

for root in (Path("/candidate"), Path("/generation-evidence"), Path("/reference")):
    entries = walk_real_tree(root)
    print(f"REAL_TREE {root}: {len(entries)} non-root entries")

for path in (
    Path("/run.json"),
    Path("/task.json"),
    Path("/generation-result.json"),
    Path("/generation-evidence/invocation.json"),
    Path("/generation-evidence/metrics.json"),
    Path("/generation-evidence/usage.json"),
):
    load_object(path)

trace_files = [
    path
    for path in walk_real_tree(Path("/generation-evidence/codex-trace"))
    if path.is_file()
]
if not trace_files:
    fail("structured trace tree has no files")
trace_lines = 0
for path in trace_files:
    with path.open("r", encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, 1):
            trace_lines += 1
            try:
                value = json.loads(line)
            except json.JSONDecodeError as error:
                fail(f"invalid JSONL {path}:{line_number}: {error}")
            if not isinstance(value, dict):
                fail(f"non-object JSONL record {path}:{line_number}")
print(f"TRACE_JSONL: {len(trace_files)} files, {trace_lines} valid object records")

hashes = audit_input.get("hashes")
if not isinstance(hashes, dict):
    fail("hashes is not an object")
declared_hashes = {
    "audit_campaign_lock_sha256": campaign_lock_path,
    "canonical_sha256": Path("/reference/canonical.py"),
    "trusted_prompt_sha256": Path("/reference/prompt.py"),
    "trusted_translator_sha256": Path("/reference/py2mpy.py"),
    "candidate_prompt_sha256": Path("/candidate/prompt.py"),
    "candidate_translator_sha256": Path("/candidate/py2mpy.py"),
    "run_manifest_sha256": Path("/run.json"),
    "task_manifest_sha256": Path("/task.json"),
    "stage1_result_sha256": Path("/generation-result.json"),
    "stage1_invocation_sha256": Path("/generation-evidence/invocation.json"),
    "generation_metrics_sha256": Path("/generation-evidence/metrics.json"),
    "generation_usage_sha256": Path("/generation-evidence/usage.json"),
    "generation_prompt_sha256": Path("/generation-evidence/prompt.txt"),
    "generation_codex_last_sha256": Path("/generation-evidence/codex-last.txt"),
    "generation_codex_output_sha256": Path("/generation-evidence/codex-output.log"),
}
for field, path in declared_hashes.items():
    actual = sha256_file(path)
    expected = hashes.get(field)
    print(f"SHA256 {path} {actual}")
    if actual != expected:
        fail(f"{field} mismatch: expected {expected}, got {actual}")

if Path("/candidate/prompt.py").read_bytes() != Path("/reference/prompt.py").read_bytes():
    fail("candidate prompt differs from trusted prompt")
if Path("/candidate/py2mpy.py").read_bytes() != Path(
    "/reference/py2mpy.py"
).read_bytes():
    fail("candidate translator differs from trusted translator")

result = load_object(Path("/generation-result.json"))
evidence = result.get("outputs", {}).get("evidence", {})  # type: ignore[union-attr]
if not isinstance(evidence, dict):
    fail("generation-result outputs.evidence is not an object")
for relative, expected in sorted(evidence.items()):
    path = Path("/generation-evidence") / relative
    actual = sha256_file(path)
    print(f"GENERATION_SHA256 {relative} {actual}")
    if actual != expected:
        fail(f"generation evidence hash mismatch for {relative}")

# Recompute the pipeline-v2 recursive digest that is explicitly recorded in
# generation-result.json and invocation.json.  This algorithm length-prefixes
# paths and includes entry kinds, file sizes, and file bytes.
sys.path.insert(0, "/opt/humaneval")
from tools.pipeline_contract import sha256_tree  # noqa: E402

candidate_tree = sha256_tree(Path("/candidate"))
trace_tree = sha256_tree(Path("/generation-evidence/codex-trace"))
expected_workspace = result.get("outputs", {}).get("workspace_sha256")  # type: ignore[union-attr]
usage = load_object(Path("/generation-evidence/usage.json"))
expected_trace = usage.get("source_trace_sha256")
print(f"PIPELINE_TREE /candidate {candidate_tree}")
print(f"PIPELINE_TREE /generation-evidence/codex-trace {trace_tree}")
if candidate_tree != expected_workspace:
    fail("candidate recursive digest differs from generation-result workspace digest")
if trace_tree != expected_trace:
    fail("trace recursive digest differs from usage source_trace_sha256")

print(f"LAUNCHER_RECORDED candidate_tree_sha256={hashes.get('candidate_tree_sha256')}")
print(
    "LAUNCHER_RECORDED generation_codex_trace_sha256="
    f"{hashes.get('generation_codex_trace_sha256')}"
)
print("STAGE1_INTEGRITY_OK")
