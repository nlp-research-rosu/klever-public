#!/usr/bin/env python3
"""Independent provenance and mounted-input integrity audit."""

from __future__ import annotations

import hashlib
import json
import os
from collections import Counter
from pathlib import Path


AUDIT = Path("/audit-input.json")
LOCK = Path("/audit-campaign-lock.json")
GEN = Path("/generation-evidence")
TRACE = GEN / "codex-trace"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def entry_kind(path: Path) -> str:
    if path.is_symlink():
        return "symlink"
    if path.is_file():
        return "regular-file"
    if path.is_dir():
        return "directory"
    return "other"


audit = json.loads(AUDIT.read_text())
lock = json.loads(LOCK.read_text())
print(f"record_layout={audit['record_layout']}")
print(f"semantics_mode={audit['semantics_mode']}")
print(f"campaign_structural_equal={audit['audit_campaign'] == lock}")
print(f"campaign_hash_actual={sha256(LOCK)}")
print(f"campaign_hash_recorded={audit['hashes']['audit_campaign_lock_sha256']}")

required = [
    Path("/run.json"),
    Path("/task.json"),
    Path("/generation-result.json"),
    GEN / "invocation.json",
    GEN / "metrics.json",
    GEN / "codex-last.txt",
    GEN / "codex-output.log",
    GEN / "prompt.txt",
    TRACE,
]
if (GEN / "usage.json").exists():
    required.append(GEN / "usage.json")

print("required-records:")
for path in required:
    readable = os.access(path, os.R_OK)
    print(f"  {path}: kind={entry_kind(path)} readable={readable}")

hash_pairs = [
    (LOCK, "audit_campaign_lock_sha256"),
    (Path("/candidate/prompt.py"), "candidate_prompt_sha256"),
    (Path("/candidate/py2mpy.py"), "candidate_translator_sha256"),
    (Path("/reference/canonical.py"), "canonical_sha256"),
    (Path("/reference/prompt.py"), "trusted_prompt_sha256"),
    (Path("/reference/py2mpy.py"), "trusted_translator_sha256"),
    (Path("/run.json"), "run_manifest_sha256"),
    (Path("/task.json"), "task_manifest_sha256"),
    (Path("/generation-result.json"), "stage1_result_sha256"),
    (GEN / "invocation.json", "stage1_invocation_sha256"),
    (GEN / "metrics.json", "generation_metrics_sha256"),
    (GEN / "usage.json", "generation_usage_sha256"),
    (GEN / "codex-last.txt", "generation_codex_last_sha256"),
    (GEN / "codex-output.log", "generation_codex_output_sha256"),
    (GEN / "prompt.txt", "generation_prompt_sha256"),
]
print("recorded-single-file-hashes:")
for path, key in hash_pairs:
    actual = sha256(path)
    expected = audit["hashes"][key]
    print(f"  {path}: match={actual == expected} actual={actual} expected={expected}")

declared_outputs: dict[str, str] = json.loads(
    Path("/generation-result.json").read_text()
)["outputs"]["evidence"]
print("generation-result-output-hashes:")
for relative, expected in sorted(declared_outputs.items()):
    path = GEN / relative
    actual = sha256(path)
    print(f"  {relative}: match={actual == expected} actual={actual} expected={expected}")

print("candidate-trusted-file-byte-comparisons:")
for candidate, trusted in [
    (Path("/candidate/prompt.py"), Path("/reference/prompt.py")),
    (Path("/candidate/py2mpy.py"), Path("/reference/py2mpy.py")),
]:
    print(f"  {candidate} == {trusted}: {candidate.read_bytes() == trusted.read_bytes()}")

def tree_manifest(root: Path) -> list[tuple[str, str, str | None]]:
    entries: list[tuple[str, str, str | None]] = []
    for directory, dirnames, filenames in os.walk(root, followlinks=False):
        dirnames.sort()
        filenames.sort()
        for name in dirnames + filenames:
            path = Path(directory) / name
            relative = path.relative_to(root).as_posix()
            kind = entry_kind(path)
            digest = sha256(path) if kind == "regular-file" else None
            entries.append((relative, kind, digest))
    return entries


candidate_semantics = tree_manifest(Path("/candidate/reference-semantics"))
trusted_semantics = tree_manifest(Path("/reference/reference-semantics"))
print(f"semantics_entry_count_candidate={len(candidate_semantics)}")
print(f"semantics_entry_count_trusted={len(trusted_semantics)}")
print(f"semantics_manifests_identical={candidate_semantics == trusted_semantics}")
if candidate_semantics != trusted_semantics:
    print("semantics_manifest_difference:")
    for entry in sorted(set(candidate_semantics) ^ set(trusted_semantics)):
        print(f"  {entry}")

all_symlinks: list[str] = []
for root in [
    Path("/candidate"),
    Path("/reference"),
    GEN,
]:
    for directory, dirnames, filenames in os.walk(root, followlinks=False):
        for name in dirnames + filenames:
            path = Path(directory) / name
            if path.is_symlink():
                all_symlinks.append(str(path))
print(f"symlink_count_in_mounted_inputs={len(all_symlinks)}")
for path in all_symlinks:
    print(f"  symlink={path}")

trace_files = sorted(TRACE.rglob("*.jsonl"))
print(f"trace_file_count={len(trace_files)}")
top_types: Counter[str] = Counter()
payload_types: Counter[str] = Counter()
function_names: Counter[str] = Counter()
parse_errors: list[str] = []
total_lines = 0
for path in trace_files:
    file_lines = 0
    with path.open(encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, 1):
            file_lines += 1
            total_lines += 1
            try:
                item = json.loads(line)
            except Exception as error:
                parse_errors.append(f"{path}:{line_number}: {error}")
                continue
            top_types[str(item.get("type"))] += 1
            payload = item.get("payload")
            if isinstance(payload, dict):
                payload_types[str(payload.get("type"))] += 1
                if payload.get("type") == "function_call":
                    function_names[str(payload.get("name"))] += 1
    print(f"  trace={path} lines={file_lines} sha256={sha256(path)}")
print(f"trace_total_lines={total_lines}")
print(f"trace_parse_error_count={len(parse_errors)}")
print(f"trace_top_level_types={dict(sorted(top_types.items()))}")
print(f"trace_payload_types={dict(sorted(payload_types.items()))}")
print(f"trace_function_names={dict(sorted(function_names.items()))}")
for error in parse_errors:
    print(f"  {error}")

output_log = (GEN / "codex-output.log").read_text(errors="replace")
print(f"codex_output_chars_read={len(output_log)}")
print(f"codex_output_line_count={len(output_log.splitlines())}")
for needle in ["#Top", "WarnStuckClaimState", "Process exited with code", "KPROVE_PASSED"]:
    print(f"codex_output_count[{needle!r}]={output_log.count(needle)}")

print("status=PASS" if not parse_errors else "status=FAIL")
