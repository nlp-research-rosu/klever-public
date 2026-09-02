#!/usr/bin/env python3
"""Independent integrity and generation-record checks for this audit."""

from __future__ import annotations

import hashlib
import json
import os
from collections import Counter
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")
LOCK = Path("/audit-campaign-lock.json")
CANDIDATE = Path("/candidate")
REFERENCE = Path("/reference")
GENERATION = Path("/generation-evidence")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def tree_manifest(root: Path) -> tuple[list[str], str]:
    rows: list[str] = []
    for path in sorted([root, *root.rglob("*")], key=lambda item: str(item)):
        stat = path.lstat()
        rel = "." if path == root else path.relative_to(root).as_posix()
        if path.is_symlink():
            kind = "symlink"
            value = os.readlink(path)
        elif path.is_dir():
            kind = "directory"
            value = "-"
        elif path.is_file():
            kind = "file"
            value = sha256(path)
        else:
            kind = "other"
            value = "-"
        rows.append(f"{kind}\t{stat.st_mode & 0o777:o}\t{rel}\t{value}")
    blob = ("\n".join(rows) + "\n").encode()
    return rows, hashlib.sha256(blob).hexdigest()


def compare_trees(left: Path, right: Path) -> list[str]:
    problems: list[str] = []
    left_entries = {
        path.relative_to(left).as_posix(): path
        for path in [left, *left.rglob("*")]
        if path != left
    }
    right_entries = {
        path.relative_to(right).as_posix(): path
        for path in [right, *right.rglob("*")]
        if path != right
    }
    for rel in sorted(left_entries.keys() | right_entries.keys()):
        if rel not in left_entries:
            problems.append(f"additional candidate entry: {rel}")
            continue
        if rel not in right_entries:
            problems.append(f"missing candidate entry: {rel}")
            continue
        lhs = left_entries[rel]
        rhs = right_entries[rel]
        lhs_kind = (
            "symlink"
            if lhs.is_symlink()
            else "directory"
            if lhs.is_dir()
            else "file"
            if lhs.is_file()
            else "other"
        )
        rhs_kind = (
            "symlink"
            if rhs.is_symlink()
            else "directory"
            if rhs.is_dir()
            else "file"
            if rhs.is_file()
            else "other"
        )
        if lhs_kind != rhs_kind:
            problems.append(f"type mismatch: {rel}: trusted={lhs_kind} candidate={rhs_kind}")
        elif rhs_kind == "symlink":
            problems.append(f"candidate symlink forbidden: {rel} -> {os.readlink(rhs)}")
        elif rhs_kind == "file" and lhs.read_bytes() != rhs.read_bytes():
            problems.append(f"content mismatch: {rel}")
    return problems


audit = json.loads(AUDIT_INPUT.read_text())
lock = json.loads(LOCK.read_text())

print(f"record_layout={audit['record_layout']}")
print(f"semantics_mode={audit['semantics_mode']}")
print(f"campaign_block_exact_match={lock == audit['audit_campaign']}")
actual_lock_hash = sha256(LOCK)
print(f"campaign_lock_sha256={actual_lock_hash}")
print(
    "campaign_lock_hash_match="
    f"{actual_lock_hash == audit['hashes']['audit_campaign_lock_sha256']}"
)

required = [
    Path("/run.json"),
    Path("/task.json"),
    Path("/generation-result.json"),
    GENERATION / "invocation.json",
    GENERATION / "metrics.json",
    GENERATION / "codex-last.txt",
    GENERATION / "codex-output.log",
    GENERATION / "prompt.txt",
    GENERATION / "codex-trace",
]
if (GENERATION / "usage.json").exists():
    required.append(GENERATION / "usage.json")
print("required_records:")
for path in required:
    print(
        f"  {path}: exists={path.exists()} readable={os.access(path, os.R_OK)} "
        f"symlink={path.is_symlink()}"
    )

hash_bindings = [
    ("canonical_sha256", REFERENCE / "canonical.py"),
    ("trusted_prompt_sha256", REFERENCE / "prompt.py"),
    ("candidate_prompt_sha256", CANDIDATE / "prompt.py"),
    ("trusted_translator_sha256", REFERENCE / "py2mpy.py"),
    ("candidate_translator_sha256", CANDIDATE / "py2mpy.py"),
    ("run_manifest_sha256", Path("/run.json")),
    ("task_manifest_sha256", Path("/task.json")),
    ("stage1_result_sha256", Path("/generation-result.json")),
    ("stage1_invocation_sha256", GENERATION / "invocation.json"),
    ("generation_metrics_sha256", GENERATION / "metrics.json"),
    ("generation_usage_sha256", GENERATION / "usage.json"),
    ("generation_codex_last_sha256", GENERATION / "codex-last.txt"),
    ("generation_codex_output_sha256", GENERATION / "codex-output.log"),
    ("generation_prompt_sha256", GENERATION / "prompt.txt"),
]
print("recorded_file_hash_checks:")
for key, path in hash_bindings:
    actual = sha256(path)
    expected = audit["hashes"][key]
    print(f"  {key}: match={actual == expected} actual={actual}")

semantics_problems = compare_trees(
    REFERENCE / "reference-semantics", CANDIDATE / "reference-semantics"
)
print(f"semantics_tree_problem_count={len(semantics_problems)}")
for problem in semantics_problems:
    print(f"  {problem}")

for name, root in [
    ("trusted_semantics", REFERENCE / "reference-semantics"),
    ("candidate_semantics", CANDIDATE / "reference-semantics"),
    ("candidate", CANDIDATE),
]:
    rows, digest = tree_manifest(root)
    manifest_path = Path("/audit-output/evidence") / f"{name}-tree-manifest.tsv"
    manifest_path.write_text("\n".join(rows) + "\n")
    print(f"{name}_independent_manifest_sha256={digest}")
    print(f"{name}_entry_count={len(rows)}")

result = json.loads(Path("/generation-result.json").read_text())
for rel, expected in sorted(result["outputs"]["evidence"].items()):
    path = GENERATION / rel
    actual = sha256(path)
    print(f"generation_result_entry={rel} match={actual == expected} actual={actual}")

json_records = [
    Path("/run.json"),
    Path("/task.json"),
    Path("/generation-result.json"),
    GENERATION / "invocation.json",
    GENERATION / "metrics.json",
    GENERATION / "usage.json",
]
for path in json_records:
    value = json.loads(path.read_text())
    print(f"json_parse={path}: ok top_type={type(value).__name__}")

output_log = (GENERATION / "codex-output.log").read_text(errors="strict")
print(f"codex_output_chars={len(output_log)}")
for needle in [
    "kompile verification.k",
    "kprove spec.k",
    "#Top",
    "WarnStuckClaimState",
    "KPROVE_PASSED",
]:
    print(f"codex_output_count[{needle!r}]={output_log.count(needle)}")

trace_files = sorted((GENERATION / "codex-trace").rglob("*.jsonl"))
print(f"trace_file_count={len(trace_files)}")
for path in trace_files:
    top_types: Counter[str] = Counter()
    payload_types: Counter[str] = Counter()
    timestamps: list[str] = []
    lines = 0
    selected_tokens = None
    for lines, raw in enumerate(path.open(), start=1):
        event = json.loads(raw)
        top_types[str(event.get("type"))] += 1
        payload = event.get("payload")
        if isinstance(payload, dict):
            payload_types[str(payload.get("type"))] += 1
            if payload.get("type") == "token_count":
                selected_tokens = payload
        if "timestamp" in event:
            timestamps.append(event["timestamp"])
    print(
        f"trace={path.relative_to(GENERATION)} lines={lines} "
        f"sha256={sha256(path)} first={timestamps[0]} last={timestamps[-1]}"
    )
    print(f"  top_types={dict(sorted(top_types.items()))}")
    print(f"  payload_types={dict(sorted(payload_types.items()))}")
    if selected_tokens:
        usage = selected_tokens["info"]["total_token_usage"]
        print(f"  final_total_token_usage={usage}")

candidate_root_symlinks = [
    str(path) for path in [CANDIDATE, *CANDIDATE.rglob("*")] if path.is_symlink()
]
print(f"candidate_symlink_count={len(candidate_root_symlinks)}")
for path in candidate_root_symlinks:
    print(f"  {path}")
