#!/usr/bin/env python3
"""Independent, read-only provenance and mount-integrity checks."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from collections import Counter
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")
LOCK = Path("/audit-campaign-lock.json")
TRACE = Path(
    "/generation-evidence/codex-trace/2026/07/25/"
    "rollout-2026-07-25T02-53-20-019f9843-b083-7992-897a-4ce009a521df.jsonl"
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def tree_inventory(root: Path) -> tuple[list[tuple[str, str, str]], str]:
    entries: list[tuple[str, str, str]] = []
    digest = hashlib.sha256()
    for path in sorted(root.rglob("*")):
        rel = path.relative_to(root).as_posix()
        mode = path.lstat().st_mode
        if stat.S_ISLNK(mode):
            kind = "symlink"
            value = os.readlink(path)
        elif stat.S_ISDIR(mode):
            kind = "directory"
            value = "-"
        elif stat.S_ISREG(mode):
            kind = "file"
            value = sha256(path)
        else:
            kind = "other"
            value = f"{mode:o}"
        entries.append((rel, kind, value))
        digest.update(rel.encode())
        digest.update(b"\0")
        digest.update(kind.encode())
        digest.update(b"\0")
        digest.update(value.encode())
        digest.update(b"\0")
    return entries, digest.hexdigest()


with AUDIT_INPUT.open(encoding="utf-8") as stream:
    audit_input = json.load(stream)
with LOCK.open(encoding="utf-8") as stream:
    lock = json.load(stream)

print(f"record_layout={audit_input['record_layout']}")
print(f"semantics_mode={audit_input['semantics_mode']}")
print(f"campaign_block_equal={audit_input['audit_campaign'] == lock}")

required = [
    AUDIT_INPUT,
    LOCK,
    Path("/run.json"),
    Path("/task.json"),
    Path("/generation-result.json"),
    Path("/generation-evidence/invocation.json"),
    Path("/generation-evidence/metrics.json"),
    Path("/generation-evidence/runtime-metrics.json"),
    Path("/generation-evidence/usage.json"),
    Path("/generation-evidence/codex-last.txt"),
    Path("/generation-evidence/codex-output.log"),
    Path("/generation-evidence/prompt.txt"),
    Path("/generation-evidence/codex-trace"),
    Path("/reference/canonical.py"),
    Path("/reference/prompt.py"),
    Path("/reference/py2mpy.py"),
    Path("/reference/reference-semantics"),
    Path("/candidate"),
]
for path in required:
    readable = os.access(path, os.R_OK)
    print(
        f"required path={path} exists={path.exists()} readable={readable} "
        f"symlink={path.is_symlink()}"
    )

hash_key_by_path = {
    LOCK: "audit_campaign_lock_sha256",
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
    Path("/generation-evidence/runtime-metrics.json"):
        "generation_runtime_metrics_sha256",
    Path("/generation-evidence/usage.json"): "generation_usage_sha256",
    Path("/generation-evidence/codex-last.txt"): "generation_codex_last_sha256",
    Path("/generation-evidence/codex-output.log"): "generation_codex_output_sha256",
    Path("/generation-evidence/prompt.txt"): "generation_prompt_sha256",
}
for path, key in hash_key_by_path.items():
    actual = sha256(path)
    expected = audit_input["hashes"][key]
    print(
        f"hash path={path} actual={actual} expected={expected} "
        f"match={actual == expected}"
    )

with Path("/generation-evidence/invocation.json").open(encoding="utf-8") as stream:
    invocation = json.load(stream)
with Path("/generation-result.json").open(encoding="utf-8") as stream:
    generation_result = json.load(stream)
trace_expected = invocation["outputs"]["evidence"][str(TRACE.relative_to(
    "/generation-evidence"
))]
trace_expected_2 = generation_result["outputs"]["evidence"][str(
    TRACE.relative_to("/generation-evidence")
)]
trace_actual = sha256(TRACE)
print(
    f"trace_raw_sha256={trace_actual} invocation_expected={trace_expected} "
    f"result_expected={trace_expected_2} "
    f"match={trace_actual == trace_expected == trace_expected_2}"
)

trace_types: Counter[str] = Counter()
trace_lines = 0
with TRACE.open(encoding="utf-8") as stream:
    for trace_lines, line in enumerate(stream, 1):
        event = json.loads(line)
        trace_types[str(event.get("type", "<none>"))] += 1
print(f"trace_jsonl_valid=True lines={trace_lines} types={dict(trace_types)}")

candidate_entries, candidate_inventory_hash = tree_inventory(Path("/candidate"))
trusted_entries, trusted_inventory_hash = tree_inventory(
    Path("/reference/reference-semantics")
)
candidate_sem_entries, candidate_sem_inventory_hash = tree_inventory(
    Path("/candidate/reference-semantics")
)
print(
    f"candidate_inventory_entries={len(candidate_entries)} "
    f"reviewer_inventory_sha256={candidate_inventory_hash}"
)
print(
    f"trusted_semantics_entries={len(trusted_entries)} "
    f"reviewer_inventory_sha256={trusted_inventory_hash}"
)
print(
    f"candidate_semantics_entries={len(candidate_sem_entries)} "
    f"reviewer_inventory_sha256={candidate_sem_inventory_hash}"
)
print(
    "semantics_type_path_content_equal="
    f"{trusted_entries == candidate_sem_entries}"
)
print(
    "candidate_symlink_count="
    f"{sum(kind == 'symlink' for _, kind, _ in candidate_entries)}"
)
print(
    "trusted_semantics_symlink_count="
    f"{sum(kind == 'symlink' for _, kind, _ in trusted_entries)}"
)

candidate_required = [
    "solution.py",
    "solution.mpy",
    "verification.k",
    "spec.k",
    "prove.sh",
    "PROOF.md",
]
for name in candidate_required:
    path = Path("/candidate") / name
    print(
        f"candidate_required path={path} regular={path.is_file()} "
        f"symlink={path.is_symlink()} readable={os.access(path, os.R_OK)}"
    )
