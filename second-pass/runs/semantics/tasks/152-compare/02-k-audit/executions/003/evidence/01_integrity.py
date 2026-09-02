#!/usr/bin/env python3
"""Independent provenance and mounted-tree integrity checks for this audit."""

from __future__ import annotations

import collections
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


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def entry_manifest(root: Path) -> list[tuple[str, str, int, str]]:
    entries: list[tuple[str, str, int, str]] = []
    for path in sorted(root.rglob("*"), key=lambda item: item.as_posix()):
        relative = path.relative_to(root).as_posix()
        mode = stat.S_IMODE(path.lstat().st_mode)
        if path.is_symlink():
            entries.append((relative, "symlink", mode, os.readlink(path)))
        elif path.is_dir():
            entries.append((relative, "directory", mode, "-"))
        elif path.is_file():
            entries.append((relative, "file", mode, digest(path)))
        else:
            entries.append((relative, "other", mode, "-"))
    return entries


def compare_trees(left: Path, right: Path) -> list[str]:
    left_manifest = {
        rel: (kind, file_hash)
        for rel, kind, _mode, file_hash in entry_manifest(left)
    }
    right_manifest = {
        rel: (kind, file_hash)
        for rel, kind, _mode, file_hash in entry_manifest(right)
    }
    differences: list[str] = []
    for relative in sorted(left_manifest.keys() | right_manifest.keys()):
        if relative not in left_manifest:
            differences.append(f"missing from candidate: {relative}")
        elif relative not in right_manifest:
            differences.append(f"additional candidate entry: {relative}")
        elif left_manifest[relative] != right_manifest[relative]:
            differences.append(
                f"entry differs: {relative}: "
                f"candidate={left_manifest[relative]} trusted={right_manifest[relative]}"
            )
    return differences


def check_regular_readable(path: Path) -> tuple[bool, str]:
    try:
        info = path.lstat()
    except OSError as err:
        return False, f"lstat failed: {err}"
    if stat.S_ISLNK(info.st_mode):
        return False, "is a symlink"
    if not stat.S_ISREG(info.st_mode):
        return False, f"is not a regular file (mode={oct(info.st_mode)})"
    try:
        with path.open("rb") as stream:
            stream.read(1)
    except OSError as err:
        return False, f"read failed: {err}"
    return True, digest(path)


audit_input = json.loads(AUDIT_INPUT.read_text(encoding="utf-8"))
lock = json.loads(LOCK.read_text(encoding="utf-8"))

print(f"record_layout={audit_input.get('record_layout')}")
print(f"semantics_mode={audit_input.get('semantics_mode')}")
print(f"problem_id={audit_input.get('problem_id')}")
print(
    "campaign_block_exact_match="
    f"{audit_input.get('audit_campaign') == lock}"
)
actual_lock_hash = digest(LOCK)
declared_lock_hash = audit_input["hashes"]["audit_campaign_lock_sha256"]
print(f"audit_campaign_lock_actual_sha256={actual_lock_hash}")
print(f"audit_campaign_lock_declared_sha256={declared_lock_hash}")
print(f"audit_campaign_lock_hash_match={actual_lock_hash == declared_lock_hash}")

required_regular_files = [
    AUDIT_INPUT,
    LOCK,
    Path("/run.json"),
    Path("/task.json"),
    Path("/generation-result.json"),
    GENERATION / "invocation.json",
    GENERATION / "metrics.json",
    GENERATION / "codex-last.txt",
    GENERATION / "codex-output.log",
    GENERATION / "prompt.txt",
]
usage = GENERATION / "usage.json"
if usage.exists():
    required_regular_files.append(usage)

print("required_record_checks:")
all_required_ok = True
for path in required_regular_files:
    ok, detail = check_regular_readable(path)
    all_required_ok &= ok
    print(f"  {path}: ok={ok} detail={detail}")

container_paths = audit_input["container_paths"]
print("launcher_declared_mount_checks:")
for key, raw_path in sorted(container_paths.items()):
    path = Path(raw_path)
    exists = path.exists()
    is_link = path.is_symlink()
    readable = os.access(path, os.R_OK)
    all_required_ok &= exists and not is_link and readable
    print(
        f"  {key}: path={path} exists={exists} "
        f"symlink={is_link} readable={readable}"
    )

expected_hash_paths = {
    "audit_campaign_lock_sha256": LOCK,
    "canonical_sha256": REFERENCE / "canonical.py",
    "trusted_prompt_sha256": REFERENCE / "prompt.py",
    "candidate_prompt_sha256": CANDIDATE / "prompt.py",
    "trusted_translator_sha256": REFERENCE / "py2mpy.py",
    "candidate_translator_sha256": CANDIDATE / "py2mpy.py",
    "run_manifest_sha256": Path("/run.json"),
    "task_manifest_sha256": Path("/task.json"),
    "manifest_sha256": Path("/task.json"),
    "stage1_result_sha256": Path("/generation-result.json"),
    "stage1_invocation_sha256": GENERATION / "invocation.json",
    "generation_metrics_sha256": GENERATION / "metrics.json",
    "generation_codex_last_sha256": GENERATION / "codex-last.txt",
    "generation_codex_output_sha256": GENERATION / "codex-output.log",
    "generation_prompt_sha256": GENERATION / "prompt.txt",
}
if usage.exists():
    expected_hash_paths["generation_usage_sha256"] = usage

print("declared_file_hash_checks:")
all_hashes_ok = True
for key, path in expected_hash_paths.items():
    actual = digest(path)
    expected = audit_input["hashes"][key]
    matches = actual == expected
    all_hashes_ok &= matches
    print(
        f"  {key}: path={path} match={matches} "
        f"actual={actual} declared={expected}"
    )

prompt_match = (
    (CANDIDATE / "prompt.py").read_bytes()
    == (REFERENCE / "prompt.py").read_bytes()
)
translator_match = (
    (CANDIDATE / "py2mpy.py").read_bytes()
    == (REFERENCE / "py2mpy.py").read_bytes()
)
semantics_differences = compare_trees(
    CANDIDATE / "reference-semantics",
    REFERENCE / "reference-semantics",
)
candidate_semantics_links = [
    relative
    for relative, kind, _mode, _value
    in entry_manifest(CANDIDATE / "reference-semantics")
    if kind == "symlink"
]
trusted_semantics_links = [
    relative
    for relative, kind, _mode, _value
    in entry_manifest(REFERENCE / "reference-semantics")
    if kind == "symlink"
]
print(f"candidate_prompt_byte_match={prompt_match}")
print(f"candidate_translator_byte_match={translator_match}")
print(f"semantics_tree_difference_count={len(semantics_differences)}")
for difference in semantics_differences:
    print(f"  {difference}")
print(f"candidate_semantics_symlinks={candidate_semantics_links}")
print(f"trusted_semantics_symlinks={trusted_semantics_links}")
print("candidate_tree_manifest:")
candidate_tree_links: list[str] = []
for relative, kind, mode, value in entry_manifest(CANDIDATE):
    if kind == "symlink":
        candidate_tree_links.append(relative)
    print(
        f"  path={relative} kind={kind} mode={oct(mode)} "
        f"sha256_or_target={value}"
    )
print(f"candidate_tree_symlinks={candidate_tree_links}")

trace_root = Path(container_paths["generation_trace"])
trace_files = sorted(trace_root.rglob("*"))
trace_regular = [
    path for path in trace_files if path.is_file() and not path.is_symlink()
]
trace_other = [
    path
    for path in trace_files
    if path.is_symlink() or (not path.is_file() and not path.is_dir())
]
print(f"trace_regular_file_count={len(trace_regular)}")
print(f"trace_unexpected_entry_count={len(trace_other)}")
trace_event_types: collections.Counter[str] = collections.Counter()
trace_payload_types: collections.Counter[str] = collections.Counter()
function_calls: list[tuple[int, str, str]] = []
trace_line_count = 0
for trace_path in trace_regular:
    trace_hash = digest(trace_path)
    print(f"trace_file={trace_path} sha256={trace_hash}")
    relative_trace = trace_path.relative_to(GENERATION).as_posix()
    declared_trace_hash = (
        json.loads(Path("/generation-result.json").read_text(encoding="utf-8"))
        .get("outputs", {})
        .get("evidence", {})
        .get(relative_trace)
    )
    print(
        f"trace_file_declared_sha256={declared_trace_hash} "
        f"match={trace_hash == declared_trace_hash}"
    )
    with trace_path.open("r", encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, 1):
            trace_line_count += 1
            record = json.loads(line)
            record_type = str(record.get("type"))
            trace_event_types[record_type] += 1
            payload = record.get("payload")
            if isinstance(payload, dict):
                payload_type = str(payload.get("type"))
                trace_payload_types[payload_type] += 1
                if payload_type == "function_call":
                    function_calls.append(
                        (
                            line_number,
                            str(payload.get("name")),
                            str(payload.get("arguments")),
                        )
                    )
print(f"trace_json_line_count={trace_line_count}")
print(f"trace_event_types={dict(sorted(trace_event_types.items()))}")
print(f"trace_payload_types={dict(sorted(trace_payload_types.items()))}")
print(f"trace_function_call_count={len(function_calls)}")
for line_number, name, arguments in function_calls:
    print(f"  trace_line={line_number} tool={name} arguments={arguments}")

print(f"all_required_records_and_mounts_ok={all_required_ok}")
print(f"all_direct_declared_hashes_ok={all_hashes_ok}")
print(
    "stage1_integrity_ok="
    f"{all_required_ok and all_hashes_ok and prompt_match and translator_match and not semantics_differences and not candidate_semantics_links and not trusted_semantics_links and audit_input.get('audit_campaign') == lock and actual_lock_hash == declared_lock_hash}"
)
