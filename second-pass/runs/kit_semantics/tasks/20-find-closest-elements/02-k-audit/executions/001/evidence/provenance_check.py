#!/usr/bin/env python3
"""Independent integrity checks for the launcher-owned audit inputs."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from collections import Counter
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")
LOCK = Path("/audit-campaign-lock.json")
TRACE_ROOT = Path("/generation-evidence/codex-trace")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def tree_manifest(root: Path) -> tuple[list[tuple[str, str, str]], str]:
    entries: list[tuple[str, str, str]] = []
    for path in sorted(root.rglob("*")):
        rel = path.relative_to(root).as_posix()
        mode = path.lstat().st_mode
        if stat.S_ISLNK(mode):
            entries.append(("symlink", rel, os.readlink(path)))
        elif stat.S_ISDIR(mode):
            entries.append(("directory", rel, ""))
        elif stat.S_ISREG(mode):
            entries.append(("file", rel, sha256(path)))
        else:
            entries.append(("other", rel, oct(mode)))
    encoded = json.dumps(entries, separators=(",", ":"), ensure_ascii=True).encode()
    return entries, hashlib.sha256(encoded).hexdigest()


audit_input = json.loads(AUDIT_INPUT.read_text())
lock = json.loads(LOCK.read_text())
expected = audit_input["hashes"]
problems: list[str] = []

print(f"audit_input_sha256={sha256(AUDIT_INPUT)}")
if lock != audit_input["audit_campaign"]:
    problems.append("campaign lock JSON differs from audit_campaign block")

checks = {
    LOCK: expected["audit_campaign_lock_sha256"],
    Path("/run.json"): expected["run_manifest_sha256"],
    Path("/task.json"): expected["task_manifest_sha256"],
    Path("/generation-result.json"): expected["stage1_result_sha256"],
    Path("/reference/canonical.py"): expected["canonical_sha256"],
    Path("/reference/prompt.py"): expected["trusted_prompt_sha256"],
    Path("/reference/py2mpy.py"): expected["trusted_translator_sha256"],
    Path("/candidate/prompt.py"): expected["candidate_prompt_sha256"],
    Path("/candidate/py2mpy.py"): expected["candidate_translator_sha256"],
    Path("/generation-evidence/invocation.json"): expected["stage1_invocation_sha256"],
    Path("/generation-evidence/metrics.json"): expected["generation_metrics_sha256"],
    Path("/generation-evidence/runtime-metrics.json"): expected[
        "generation_runtime_metrics_sha256"
    ],
    Path("/generation-evidence/usage.json"): expected["generation_usage_sha256"],
    Path("/generation-evidence/codex-last.txt"): expected[
        "generation_codex_last_sha256"
    ],
    Path("/generation-evidence/codex-output.log"): expected[
        "generation_codex_output_sha256"
    ],
    Path("/generation-evidence/prompt.txt"): expected["generation_prompt_sha256"],
}

print(f"record_layout={audit_input['record_layout']}")
print(f"semantics_mode={audit_input['semantics_mode']}")
print(f"campaign_json_equal={lock == audit_input['audit_campaign']}")
for path, wanted in checks.items():
    regular = path.is_file() and not path.is_symlink()
    got = sha256(path) if regular else "<not-regular>"
    matched = regular and got == wanted
    print(f"file={path} regular={regular} sha256={got} expected={wanted} match={matched}")
    if not matched:
        problems.append(f"file integrity mismatch: {path}")

candidate_entries, candidate_manifest_hash = tree_manifest(
    Path("/candidate/reference-semantics")
)
trusted_entries, trusted_manifest_hash = tree_manifest(
    Path("/reference/reference-semantics")
)
whole_candidate_entries, whole_candidate_manifest_hash = tree_manifest(Path("/candidate"))
print(f"candidate_semantics_manifest_sha256={candidate_manifest_hash}")
print(f"trusted_semantics_manifest_sha256={trusted_manifest_hash}")
print(f"semantics_entry_count={len(candidate_entries)}")
print(f"semantics_manifests_equal={candidate_entries == trusted_entries}")
print(
    "semantics_symlink_count="
    f"{sum(kind == 'symlink' for kind, _, _ in candidate_entries)}"
)
print(f"whole_candidate_manifest_sha256={whole_candidate_manifest_hash}")
print(f"whole_candidate_entry_count={len(whole_candidate_entries)}")
print(
    "whole_candidate_symlink_count="
    f"{sum(kind == 'symlink' for kind, _, _ in whole_candidate_entries)}"
)
print(
    "whole_candidate_special_entry_count="
    f"{sum(kind == 'other' for kind, _, _ in whole_candidate_entries)}"
)
if candidate_entries != trusted_entries:
    problems.append("candidate and trusted semantics manifests differ")

trace_counts: Counter[str] = Counter()
payload_counts: Counter[str] = Counter()
trace_files = sorted(TRACE_ROOT.rglob("*"))
trace_files = [path for path in trace_files if path.is_file()]
trace_lines = 0
for path in trace_files:
    if path.is_symlink():
        problems.append(f"trace entry is symlink: {path}")
    with path.open() as stream:
        for line_number, line in enumerate(stream, 1):
            trace_lines += 1
            try:
                event = json.loads(line)
            except json.JSONDecodeError as err:
                problems.append(f"invalid trace JSON {path}:{line_number}: {err}")
                continue
            trace_counts[str(event.get("type"))] += 1
            payload = event.get("payload")
            if isinstance(payload, dict):
                payload_counts[str(payload.get("type"))] += 1

print(f"trace_file_count={len(trace_files)}")
print(f"trace_line_count={trace_lines}")
print(f"trace_event_counts={dict(sorted(trace_counts.items()))}")
print(f"trace_payload_counts={dict(sorted(payload_counts.items()))}")

generation_result = json.loads(Path("/generation-result.json").read_text())
for relative, wanted in sorted(generation_result["outputs"]["evidence"].items()):
    path = Path("/generation-evidence") / relative
    got = sha256(path) if path.is_file() and not path.is_symlink() else "<not-regular>"
    matched = got == wanted
    print(
        f"stage1_output={relative} sha256={got} expected={wanted} match={matched}"
    )
    if not matched:
        problems.append(f"stage1 output integrity mismatch: {relative}")

for name, raw_path in sorted(audit_input["container_paths"].items()):
    path = Path(raw_path)
    present = path.exists()
    symlink = path.is_symlink()
    print(
        f"container_path={name} path={path} present={present} symlink={symlink}"
    )
    if not present or symlink:
        problems.append(f"invalid launcher-declared container path: {name}={path}")

print(f"problems={len(problems)}")
for problem in problems:
    print(f"PROBLEM: {problem}")

raise SystemExit(1 if problems else 0)
