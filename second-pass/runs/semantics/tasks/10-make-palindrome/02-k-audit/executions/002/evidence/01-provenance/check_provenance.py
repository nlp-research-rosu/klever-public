#!/usr/bin/env python3
"""Independent launcher/provenance checks for the 10-make-palindrome audit."""

from __future__ import annotations

import collections
import hashlib
import json
import os
import stat
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")
CAMPAIGN_LOCK = Path("/audit-campaign-lock.json")
CANDIDATE = Path("/candidate")
REFERENCE = Path("/reference")
GENERATION = Path("/generation-evidence")
TRACE = GENERATION / "codex-trace/2026/07/22/rollout-2026-07-22T21-13-06-019f8cbf-79b7-7571-b6ad-5449cf299015.jsonl"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def regular_tree(root: Path) -> tuple[list[str], str]:
    """Return paths and a reviewer-defined path+content digest.

    This digest is deliberately independent of the launcher's unspecified
    directory-hash serialization. Exact recursive equality is checked
    separately below.
    """

    entries: list[str] = []
    digest = hashlib.sha256()
    for current, dirs, files in os.walk(root, followlinks=False):
        dirs.sort()
        files.sort()
        current_path = Path(current)
        for name in dirs + files:
            path = current_path / name
            mode = os.lstat(path).st_mode
            assert not stat.S_ISLNK(mode), f"symlink forbidden: {path}"
            assert stat.S_ISDIR(mode) or stat.S_ISREG(mode), (
                f"special tree entry forbidden: {path}"
            )
        for name in files:
            path = current_path / name
            rel = path.relative_to(root).as_posix()
            entries.append(rel)
            content = path.read_bytes()
            rel_bytes = rel.encode("utf-8")
            digest.update(len(rel_bytes).to_bytes(8, "big"))
            digest.update(rel_bytes)
            digest.update(len(content).to_bytes(8, "big"))
            digest.update(content)
    return entries, digest.hexdigest()


audit = json.loads(AUDIT_INPUT.read_text())
lock = json.loads(CAMPAIGN_LOCK.read_text())

assert audit["record_layout"] == "legacy-selected-stage1"
assert audit["semantics_mode"] == "SUPPLIED_SEMANTICS"
assert audit["mount_reference_semantics"] is True
assert audit["audit_campaign"] == lock
assert sha256(CAMPAIGN_LOCK) == audit["hashes"]["audit_campaign_lock_sha256"]

required = [
    Path("/run.json"),
    Path("/task.json"),
    Path("/generation-result.json"),
    GENERATION / "invocation.json",
    GENERATION / "metrics.json",
    GENERATION / "codex-last.txt",
    GENERATION / "codex-output.log",
    GENERATION / "prompt.txt",
    GENERATION / "usage.json",
    TRACE,
]
for path in required:
    assert path.is_file(), f"missing/unreadable required record: {path}"
    assert not path.is_symlink(), f"required record is a symlink: {path}"

direct_hashes = {
    CAMPAIGN_LOCK: "audit_campaign_lock_sha256",
    REFERENCE / "canonical.py": "canonical_sha256",
    CANDIDATE / "prompt.py": "candidate_prompt_sha256",
    CANDIDATE / "py2mpy.py": "candidate_translator_sha256",
    REFERENCE / "prompt.py": "trusted_prompt_sha256",
    REFERENCE / "py2mpy.py": "trusted_translator_sha256",
    Path("/run.json"): "run_manifest_sha256",
    Path("/task.json"): "task_manifest_sha256",
    Path("/generation-result.json"): "stage1_result_sha256",
    GENERATION / "invocation.json": "stage1_invocation_sha256",
    GENERATION / "metrics.json": "generation_metrics_sha256",
    GENERATION / "usage.json": "generation_usage_sha256",
    GENERATION / "codex-last.txt": "generation_codex_last_sha256",
    GENERATION / "codex-output.log": "generation_codex_output_sha256",
    GENERATION / "prompt.txt": "generation_prompt_sha256",
}
for path, key in direct_hashes.items():
    actual = sha256(path)
    expected = audit["hashes"][key]
    assert actual == expected, f"{key}: {actual} != {expected}"

assert (CANDIDATE / "prompt.py").read_bytes() == (
    REFERENCE / "prompt.py"
).read_bytes()
assert (CANDIDATE / "py2mpy.py").read_bytes() == (
    REFERENCE / "py2mpy.py"
).read_bytes()

candidate_semantics = CANDIDATE / "reference-semantics"
trusted_semantics = REFERENCE / "reference-semantics"
candidate_entries, candidate_digest = regular_tree(candidate_semantics)
trusted_entries, trusted_digest = regular_tree(trusted_semantics)
assert candidate_entries == trusted_entries
for rel in candidate_entries:
    assert (candidate_semantics / rel).read_bytes() == (
        trusted_semantics / rel
    ).read_bytes(), f"semantics content mismatch: {rel}"

candidate_entries_all, candidate_tree_digest = regular_tree(CANDIDATE)

result = json.loads(Path("/generation-result.json").read_text())
for rel, expected in result["outputs"]["evidence"].items():
    path = GENERATION / rel
    assert path.is_file(), f"generation-result output absent: {path}"
    actual = sha256(path)
    assert actual == expected, f"generation-result hash mismatch: {path}"

trace_types: collections.Counter[str] = collections.Counter()
payload_types: collections.Counter[str] = collections.Counter()
trace_lines = 0
with TRACE.open(encoding="utf-8") as stream:
    for trace_lines, line in enumerate(stream, 1):
        record = json.loads(line)
        trace_types[str(record.get("type"))] += 1
        payload = record.get("payload")
        if isinstance(payload, dict):
            payload_types[str(payload.get("type"))] += 1

print("record_layout=legacy-selected-stage1")
print("semantics_mode=SUPPLIED_SEMANTICS")
print("campaign_block_equals_lock=true")
print(f"campaign_lock_sha256={sha256(CAMPAIGN_LOCK)}")
print(f"required_records={len(required)} all_present_regular=true")
print(f"direct_declared_hashes={len(direct_hashes)} all_match=true")
print("candidate_prompt_matches_trusted=true")
print("candidate_translator_matches_trusted=true")
print(
    "candidate_semantics_matches_trusted=true "
    f"files={len(candidate_entries)} "
    f"reviewer_tree_sha256={candidate_digest}"
)
print(
    "trusted_semantics "
    f"files={len(trusted_entries)} "
    f"reviewer_tree_sha256={trusted_digest}"
)
print(
    "candidate_tree "
    f"files={len(candidate_entries_all)} "
    f"reviewer_tree_sha256={candidate_tree_digest}"
)
print(
    f"generation_result_evidence_hashes={len(result['outputs']['evidence'])} "
    "all_match=true"
)
print(f"trace_lines={trace_lines} valid_jsonl=true")
print(f"trace_record_types={dict(sorted(trace_types.items()))}")
print(f"trace_payload_types={dict(sorted(payload_types.items()))}")
print(
    "runtime-metrics.json=absent "
    "(allowed for legacy-selected-stage1; historical metric not reconstructed)"
)
