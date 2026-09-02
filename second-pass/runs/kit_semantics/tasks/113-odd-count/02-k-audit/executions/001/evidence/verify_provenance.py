#!/usr/bin/env python3
"""Independent mounted-input and supplied-semantics integrity checks."""

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


def kind(path: Path) -> str:
    mode = path.lstat().st_mode
    if stat.S_ISREG(mode):
        return "file"
    if stat.S_ISDIR(mode):
        return "dir"
    if stat.S_ISLNK(mode):
        return "symlink"
    return f"other({mode:o})"


def tree_entries(root: Path) -> dict[str, tuple[str, str | None]]:
    entries: dict[str, tuple[str, str | None]] = {}
    for current, dirs, files in os.walk(root, followlinks=False):
        current_path = Path(current)
        for name in sorted(dirs + files):
            path = current_path / name
            rel = path.relative_to(root).as_posix()
            entry_kind = kind(path)
            entries[rel] = (
                entry_kind,
                sha256(path) if entry_kind == "file" else None,
            )
    return entries


data = json.loads(AUDIT_INPUT.read_text())
hashes = data["hashes"]
paths = data["container_paths"]

print(f"record_layout={data['record_layout']}")
print(f"semantics_mode={data['semantics_mode']}")
print(f"audit_input_kind={kind(AUDIT_INPUT)}")
print(f"campaign_lock_kind={kind(LOCK)}")
lock_hash = sha256(LOCK)
print(f"campaign_lock_sha256={lock_hash}")
print(
    "campaign_lock_hash_match="
    f"{lock_hash == hashes['audit_campaign_lock_sha256']}"
)
lock_data = json.loads(LOCK.read_text())
print(f"campaign_block_exact_match={lock_data == data['audit_campaign']}")

file_checks = [
    ("canonical", Path(paths["canonical"]), "canonical_sha256"),
    ("trusted_prompt", Path(paths["trusted_prompt"]), "trusted_prompt_sha256"),
    ("candidate_prompt", Path(paths["candidate"]) / "prompt.py", "candidate_prompt_sha256"),
    ("translator", Path(paths["translator"]), "trusted_translator_sha256"),
    ("candidate_translator", Path(paths["candidate"]) / "py2mpy.py", "candidate_translator_sha256"),
    ("run_manifest", Path(paths["run_manifest"]), "run_manifest_sha256"),
    ("task_manifest", Path(paths["task_manifest"]), "task_manifest_sha256"),
    ("stage1_result", Path(paths["stage1_result"]), "stage1_result_sha256"),
    ("stage1_invocation", Path(paths["generation_manifest"]), "stage1_invocation_sha256"),
    ("generation_metrics", Path(paths["generation_metrics"]), "generation_metrics_sha256"),
    ("generation_last", Path(paths["generation_last"]), "generation_codex_last_sha256"),
    ("generation_output", Path(paths["generation_output"]), "generation_codex_output_sha256"),
    ("generation_prompt", Path(paths["generation_root"]) / "prompt.txt", "generation_prompt_sha256"),
    (
        "generation_runtime_metrics",
        Path(paths["generation_root"]) / "runtime-metrics.json",
        "generation_runtime_metrics_sha256",
    ),
    ("generation_usage", Path(paths["generation_root"]) / "usage.json", "generation_usage_sha256"),
]

for label, path, key in file_checks:
    present = path.exists()
    entry_kind = kind(path) if present or path.is_symlink() else "missing"
    actual = sha256(path) if entry_kind == "file" else None
    expected = hashes[key]
    print(
        f"{label}: present={present} kind={entry_kind} "
        f"sha256={actual} expected={expected} match={actual == expected}"
    )

json_records = [
    ("run", Path(paths["run_manifest"])),
    ("task", Path(paths["task_manifest"])),
    ("generation_result", Path(paths["stage1_result"])),
    ("invocation", Path(paths["generation_manifest"])),
    ("metrics", Path(paths["generation_metrics"])),
    ("runtime_metrics", Path(paths["generation_root"]) / "runtime-metrics.json"),
    ("usage", Path(paths["generation_root"]) / "usage.json"),
]
for label, path in json_records:
    record = json.loads(path.read_text())
    selected = {
        key: record[key]
        for key in (
            "schema_version",
            "run_id",
            "problem_id",
            "current_stage",
            "stage",
            "status",
            "kind",
            "exit_code",
            "final_exit_code",
            "harness_exit_code",
            "model_exit_code",
            "oom_killed",
            "timeout_marker",
        )
        if key in record
    }
    print(
        f"json_record {label}: parsed=True keys={sorted(record)} "
        f"selected={selected}"
    )

for label, path in [
    ("generation_prompt_text", Path(paths["generation_root"]) / "prompt.txt"),
    ("generation_last_text", Path(paths["generation_last"])),
    ("generation_output_log", Path(paths["generation_output"])),
]:
    text = path.read_text(errors="strict")
    print(
        f"text_record {label}: decoded_utf8=True "
        f"characters={len(text)} lines={len(text.splitlines())}"
    )

trace_root = Path(paths["generation_trace"])
trace_entries = tree_entries(trace_root)
print(f"trace_entry_count={len(trace_entries)}")
for rel, (entry_kind, digest) in sorted(trace_entries.items()):
    print(f"trace_entry {rel} kind={entry_kind} sha256={digest}")
result = json.loads(Path(paths["stage1_result"]).read_text())
declared_trace = {
    key.removeprefix("codex-trace/"): value
    for key, value in result["outputs"]["evidence"].items()
    if key.startswith("codex-trace/")
}
actual_trace_files = {
    rel: digest
    for rel, (entry_kind, digest) in trace_entries.items()
    if entry_kind == "file"
}
print(f"trace_matches_stage1_result={actual_trace_files == declared_trace}")

candidate_semantics = Path(paths["candidate"]) / "reference-semantics"
trusted_semantics = Path("/reference/reference-semantics")
candidate_entries = tree_entries(candidate_semantics)
trusted_entries = tree_entries(trusted_semantics)
print(f"candidate_semantics_kind={kind(candidate_semantics)}")
print(f"trusted_semantics_kind={kind(trusted_semantics)}")
print(f"candidate_semantics_entries={len(candidate_entries)}")
print(f"trusted_semantics_entries={len(trusted_entries)}")
print(f"semantics_trees_exact_match={candidate_entries == trusted_entries}")
for rel in sorted(set(candidate_entries) | set(trusted_entries)):
    if candidate_entries.get(rel) != trusted_entries.get(rel):
        print(
            f"SEMANTICS_DIFF {rel}: candidate={candidate_entries.get(rel)} "
            f"trusted={trusted_entries.get(rel)}"
        )

candidate_root = Path(paths["candidate"])
symlinks = [
    path.relative_to(candidate_root).as_posix()
    for path in candidate_root.rglob("*")
    if path.is_symlink()
]
print(f"candidate_symlink_count={len(symlinks)}")
for rel in symlinks:
    print(f"CANDIDATE_SYMLINK {rel}")

required_candidate = [
    "prompt.py",
    "py2mpy.py",
    "reference-semantics",
    "solution.py",
    "solution.mpy",
    "spec.k",
    "verification.k",
]
for rel in required_candidate:
    path = candidate_root / rel
    print(
        f"required_candidate {rel}: "
        f"kind={kind(path) if path.exists() or path.is_symlink() else 'missing'}"
    )
