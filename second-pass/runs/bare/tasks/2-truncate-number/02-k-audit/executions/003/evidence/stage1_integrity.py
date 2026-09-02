#!/usr/bin/env python3
"""Independent integrity and provenance checks for this audit.

This script intentionally uses only mounted container paths.  The aggregate
tree digest below is reviewer-defined and transparent; launcher-recorded
per-artifact SHA-256 values are checked directly wherever the manifest states
their byte-level meaning.
"""

from __future__ import annotations

import hashlib
import json
import os
import stat
from collections import Counter
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")
LOCK = Path("/audit-campaign-lock.json")
TRACE = Path("/generation-evidence/codex-trace")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require_regular(path: Path) -> None:
    mode = path.lstat().st_mode
    assert stat.S_ISREG(mode), f"not a regular file: {path}"
    assert not path.is_symlink(), f"symlinked file: {path}"
    with path.open("rb") as stream:
        stream.read(1)


def require_tree(path: Path) -> list[tuple[str, str, int]]:
    mode = path.lstat().st_mode
    assert stat.S_ISDIR(mode), f"not a real directory: {path}"
    assert not path.is_symlink(), f"symlinked directory: {path}"
    inventory: list[tuple[str, str, int]] = []
    pending = [path]
    while pending:
        directory = pending.pop()
        for entry in os.scandir(directory):
            entry_mode = entry.stat(follow_symlinks=False).st_mode
            child = Path(entry.path)
            relative = child.relative_to(path).as_posix()
            if stat.S_ISDIR(entry_mode):
                inventory.append((relative, "directory", 0))
                pending.append(child)
            elif stat.S_ISREG(entry_mode):
                inventory.append((relative, "file", entry.stat().st_size))
            else:
                raise AssertionError(f"linked/unsupported tree entry: {child}")
    return sorted(inventory)


def transparent_tree_digest(path: Path) -> tuple[str, list[tuple[str, str]]]:
    digest = hashlib.sha256()
    file_hashes: list[tuple[str, str]] = []
    for relative, kind, _ in require_tree(path):
        child = path / relative
        digest.update(relative.encode("utf-8") + b"\0")
        digest.update(kind.encode("ascii") + b"\0")
        if kind == "file":
            content = child.read_bytes()
            child_hash = hashlib.sha256(content).hexdigest()
            digest.update(content)
            file_hashes.append((relative, child_hash))
    return digest.hexdigest(), file_hashes


def check_hash(path: Path, expected: str, label: str) -> None:
    actual = sha256(path)
    print(f"HASH {label}: expected={expected} actual={actual}")
    assert actual == expected, f"hash mismatch: {label}"


audit = json.loads(AUDIT_INPUT.read_text(encoding="utf-8"))
lock = json.loads(LOCK.read_text(encoding="utf-8"))
hashes = audit["hashes"]

print(f"record_layout={audit['record_layout']}")
print(f"semantics_mode={audit['semantics_mode']}")
assert audit["record_layout"] == "legacy-selected-stage1"
assert audit["semantics_mode"] == "GENERATED_SEMANTICS"
assert audit["mount_reference_semantics"] is False
assert not Path("/reference/reference-semantics").exists()

require_regular(AUDIT_INPUT)
require_regular(LOCK)
assert lock == audit["audit_campaign"], "campaign lock/block mismatch"
check_hash(LOCK, hashes["audit_campaign_lock_sha256"], "campaign lock")

container_paths = audit["container_paths"]
for label, rendered in sorted(container_paths.items()):
    path = Path(rendered)
    if label in {"candidate", "generation_root", "generation_trace"}:
        entries = require_tree(path)
        print(f"MOUNT {label}: real directory, entries={len(entries)} path={path}")
    else:
        require_regular(path)
        print(f"MOUNT {label}: regular readable file path={path}")

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
require_tree(TRACE)
usage = Path("/generation-evidence/usage.json")
if usage.exists():
    require_regular(usage)
    print("usage.json present and inspected")

checks = [
    (Path("/reference/canonical.py"), hashes["canonical_sha256"], "canonical"),
    (Path("/reference/prompt.py"), hashes["trusted_prompt_sha256"], "trusted prompt"),
    (Path("/reference/py2mpy.py"), hashes["trusted_translator_sha256"], "trusted translator"),
    (Path("/candidate/prompt.py"), hashes["candidate_prompt_sha256"], "candidate prompt"),
    (Path("/candidate/py2mpy.py"), hashes["candidate_translator_sha256"], "candidate translator"),
    (Path("/run.json"), hashes["run_manifest_sha256"], "run manifest"),
    (Path("/task.json"), hashes["task_manifest_sha256"], "task manifest"),
    (Path("/generation-result.json"), hashes["stage1_result_sha256"], "stage1 result"),
    (Path("/generation-evidence/invocation.json"), hashes["stage1_invocation_sha256"], "invocation"),
    (Path("/generation-evidence/metrics.json"), hashes["generation_metrics_sha256"], "metrics"),
    (Path("/generation-evidence/codex-last.txt"), hashes["generation_codex_last_sha256"], "codex-last"),
    (Path("/generation-evidence/codex-output.log"), hashes["generation_codex_output_sha256"], "codex-output"),
    (Path("/generation-evidence/prompt.txt"), hashes["generation_prompt_sha256"], "generation prompt"),
]
if usage.exists():
    checks.append((usage, hashes["generation_usage_sha256"], "usage"))
for path, expected, label in checks:
    check_hash(path, expected, label)

assert Path("/candidate/prompt.py").read_bytes() == Path("/reference/prompt.py").read_bytes()
assert Path("/candidate/py2mpy.py").read_bytes() == Path("/reference/py2mpy.py").read_bytes()
print("IDENTITY candidate prompt == trusted prompt")
print("IDENTITY candidate translator == trusted translator")

result = json.loads(Path("/generation-result.json").read_text(encoding="utf-8"))
evidence_hashes = result["outputs"]["evidence"]
for relative, expected in sorted(evidence_hashes.items()):
    path = Path("/generation-evidence") / relative
    require_regular(path)
    check_hash(path, expected, f"generation result evidence/{relative}")

trace_digest, trace_files = transparent_tree_digest(TRACE)
print(f"TRACE reviewer_tree_sha256={trace_digest}")
for relative, actual in trace_files:
    expected = evidence_hashes.get(f"codex-trace/{relative}")
    print(f"TRACE_FILE {relative}: expected={expected} actual={actual}")
    assert expected == actual
print(f"TRACE launcher_aggregate_claim={hashes['generation_codex_trace_sha256']}")

candidate_digest, candidate_files = transparent_tree_digest(Path("/candidate"))
print(f"CANDIDATE reviewer_tree_sha256={candidate_digest}")
print(f"CANDIDATE launcher_aggregate_claim={hashes['candidate_tree_sha256']}")
for relative, actual in candidate_files:
    print(f"CANDIDATE_FILE {relative}: sha256={actual}")

trace_counts: Counter[str] = Counter()
trace_path = next(path for path in TRACE.rglob("*") if path.is_file())
line_count = 0
tool_calls = 0
tool_outputs = 0
roles: Counter[str] = Counter()
with trace_path.open(encoding="utf-8") as stream:
    for line_count, line in enumerate(stream, 1):
        event = json.loads(line)
        trace_counts[event.get("type", "<missing>")] += 1
        payload = event.get("payload", {})
        if isinstance(payload, dict):
            role = payload.get("role")
            if role:
                roles[str(role)] += 1
            if payload.get("type") in {"function_call", "custom_tool_call"}:
                tool_calls += 1
            if payload.get("type") in {"function_call_output", "custom_tool_call_output"}:
                tool_outputs += 1
print(f"TRACE_JSON valid_lines={line_count} top_types={dict(trace_counts)}")
print(f"TRACE_JSON roles={dict(roles)} tool_calls={tool_calls} tool_outputs={tool_outputs}")

print("STAGE1_INTEGRITY_OK")
