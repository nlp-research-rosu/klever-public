#!/usr/bin/env python3
"""Independent integrity checks for the launcher-owned pipeline-v3 record."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from collections import Counter
from pathlib import Path

AUDIT_INPUT = Path("/audit-input.json")
AUDIT_LOCK = Path("/audit-campaign-lock.json")
CANDIDATE = Path("/candidate")
REFERENCE = Path("/reference")
GEN = Path("/generation-evidence")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def require_regular(path: Path) -> None:
    mode = path.lstat().st_mode
    if not stat.S_ISREG(mode):
        raise AssertionError(f"not a regular file: {path}")
    if path.is_symlink():
        raise AssertionError(f"symlink not allowed: {path}")


def tree_manifest(root: Path) -> tuple[str, list[str]]:
    entries: list[str] = []
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root).as_posix()
        mode = path.lstat().st_mode
        if stat.S_ISLNK(mode):
            kind = "symlink"
            payload = os.readlink(path)
        elif stat.S_ISDIR(mode):
            kind = "dir"
            payload = "-"
        elif stat.S_ISREG(mode):
            kind = "file"
            payload = sha256(path)
        else:
            kind = "other"
            payload = "-"
        entries.append(f"{kind}\t{relative}\t{payload}")
    encoded = ("\n".join(entries) + "\n").encode()
    return hashlib.sha256(encoded).hexdigest(), entries


def recorded_tree_hash(root: Path) -> str:
    """Recompute the length-delimited tree digest used by pipeline-v3."""
    digest = hashlib.sha256()
    entries: list[tuple[str, str, Path]] = []
    pending = [root]
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
                raise AssertionError(f"linked or unsupported tree entry: {path}")
    for relative, kind, path in sorted(entries):
        encoded = relative.encode()
        digest.update(len(encoded).to_bytes(4, "big"))
        digest.update(encoded)
        digest.update(kind.encode() + b"\0")
        if kind == "file":
            digest.update(path.stat(follow_symlinks=False).st_size.to_bytes(8, "big"))
            with path.open("rb") as stream:
                for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                    digest.update(chunk)
    return digest.hexdigest()


audit = json.loads(AUDIT_INPUT.read_text(encoding="utf-8"))
lock = json.loads(AUDIT_LOCK.read_text(encoding="utf-8"))
assert audit["record_layout"] == "pipeline-v3"
assert audit["semantics_mode"] == "SUPPLIED_SEMANTICS"
assert audit["audit_campaign"] == lock
print("campaign_block_exact_match=true")

required_records = [
    AUDIT_INPUT,
    AUDIT_LOCK,
    Path("/run.json"),
    Path("/task.json"),
    Path("/generation-result.json"),
    GEN / "invocation.json",
    GEN / "metrics.json",
    GEN / "runtime-metrics.json",
    GEN / "usage.json",
    GEN / "codex-last.txt",
    GEN / "codex-output.log",
    GEN / "prompt.txt",
]
for path in required_records:
    require_regular(path)
print(f"required_regular_records={len(required_records)}")

hash_checks = {
    AUDIT_LOCK: audit["hashes"]["audit_campaign_lock_sha256"],
    Path("/run.json"): audit["hashes"]["run_manifest_sha256"],
    Path("/task.json"): audit["hashes"]["task_manifest_sha256"],
    Path("/generation-result.json"): audit["hashes"]["stage1_result_sha256"],
    GEN / "invocation.json": audit["hashes"]["stage1_invocation_sha256"],
    GEN / "metrics.json": audit["hashes"]["generation_metrics_sha256"],
    GEN / "runtime-metrics.json": audit["hashes"][
        "generation_runtime_metrics_sha256"
    ],
    GEN / "usage.json": audit["hashes"]["generation_usage_sha256"],
    GEN / "codex-last.txt": audit["hashes"]["generation_codex_last_sha256"],
    GEN / "codex-output.log": audit["hashes"][
        "generation_codex_output_sha256"
    ],
    GEN / "prompt.txt": audit["hashes"]["generation_prompt_sha256"],
    REFERENCE / "canonical.py": audit["hashes"]["canonical_sha256"],
    REFERENCE / "prompt.py": audit["hashes"]["trusted_prompt_sha256"],
    REFERENCE / "py2mpy.py": audit["hashes"]["trusted_translator_sha256"],
}
for path, expected in hash_checks.items():
    actual = sha256(path)
    if actual != expected:
        raise AssertionError(f"hash mismatch: {path}: {actual} != {expected}")
    print(f"hash_ok\t{path}\t{actual}")

candidate_pairs = [
    (CANDIDATE / "prompt.py", REFERENCE / "prompt.py"),
    (CANDIDATE / "py2mpy.py", REFERENCE / "py2mpy.py"),
]
for candidate_path, trusted_path in candidate_pairs:
    require_regular(candidate_path)
    require_regular(trusted_path)
    assert candidate_path.read_bytes() == trusted_path.read_bytes()
    print(f"candidate_trusted_identity\t{candidate_path}\ttrue")

candidate_semantics = CANDIDATE / "reference-semantics"
trusted_semantics = REFERENCE / "reference-semantics"
candidate_sem_hash, candidate_sem_entries = tree_manifest(candidate_semantics)
trusted_sem_hash, trusted_sem_entries = tree_manifest(trusted_semantics)
assert candidate_sem_entries == trusted_sem_entries
assert all(not entry.startswith(("symlink\t", "other\t")) for entry in candidate_sem_entries)
print(f"semantics_entry_count={len(candidate_sem_entries)}")
print(f"candidate_semantics_reviewer_tree_sha256={candidate_sem_hash}")
print(f"trusted_semantics_reviewer_tree_sha256={trusted_sem_hash}")
print("semantics_exact_entry_type_and_byte_identity=true")
candidate_sem_recorded_hash = recorded_tree_hash(candidate_semantics)
trusted_sem_recorded_hash = recorded_tree_hash(trusted_semantics)
assert candidate_sem_recorded_hash == audit["hashes"][
    "trusted_reference_semantics_manifest_sha256"
]
assert trusted_sem_recorded_hash == audit["hashes"][
    "trusted_reference_semantics_manifest_sha256"
]
assert trusted_sem_recorded_hash == audit["manifest"]["inputs"][
    "reference_semantics_sha256"
]
print(f"candidate_semantics_pipeline_tree_hash_ok={candidate_sem_recorded_hash}")
print(f"trusted_semantics_pipeline_tree_hash_ok={trusted_sem_recorded_hash}")

proof_artifacts = [
    "solution.py",
    "solution.mpy",
    "verification.k",
    "verification-with-loop.k",
    "spec.k",
    "prove.sh",
    "PROOF.md",
]
for name in proof_artifacts:
    path = CANDIDATE / name
    require_regular(path)
    print(f"proof_artifact\t{name}\t{sha256(path)}")

candidate_tree_hash, candidate_tree_entries = tree_manifest(CANDIDATE)
print(f"candidate_reviewer_tree_entries={len(candidate_tree_entries)}")
print(f"candidate_reviewer_tree_sha256={candidate_tree_hash}")
candidate_recorded_tree_hash = recorded_tree_hash(CANDIDATE)
stage_result = json.loads(
    Path("/generation-result.json").read_text(encoding="utf-8")
)
assert candidate_recorded_tree_hash == stage_result["outputs"]["workspace_sha256"]
print(f"candidate_pipeline_tree_hash_ok={candidate_recorded_tree_hash}")

trace_files = sorted((GEN / "codex-trace").rglob("*"))
trace_files = [path for path in trace_files if path.is_file()]
assert len(trace_files) == 1
require_regular(trace_files[0])
trace_expected = json.loads(
    Path("/generation-result.json").read_text(encoding="utf-8")
)["outputs"]["evidence"][
    "codex-trace/2026/07/25/"
    "rollout-2026-07-25T00-36-29-019f97c6-63fd-7240-a748-7262d52c48fd.jsonl"
]
assert sha256(trace_files[0]) == trace_expected
trace_tree_hash = recorded_tree_hash(GEN / "codex-trace")
usage = json.loads((GEN / "usage.json").read_text(encoding="utf-8"))
assert trace_tree_hash == usage["source_trace_sha256"]
print(f"trace_pipeline_tree_hash_ok={trace_tree_hash}")

event_types: Counter[str] = Counter()
payload_types: Counter[str] = Counter()
trace_lines = 0
with trace_files[0].open(encoding="utf-8") as stream:
    for line in stream:
        record = json.loads(line)
        trace_lines += 1
        event_types[str(record.get("type"))] += 1
        payload = record.get("payload")
        if isinstance(payload, dict) and "type" in payload:
            payload_types[str(payload["type"])] += 1
print(f"trace_lines_parsed={trace_lines}")
print(f"trace_sha256={trace_expected}")
print(f"trace_event_types={dict(sorted(event_types.items()))}")
print(f"trace_payload_types={dict(sorted(payload_types.items()))}")

for path in [GEN / "codex-output.log", GEN / "codex-last.txt", GEN / "prompt.txt"]:
    text = path.read_text(encoding="utf-8")
    print(
        f"text_record_read\t{path.name}\tlines={len(text.splitlines())}"
        f"\tchars={len(text)}"
    )

print("PROVENANCE_CHECK=PASS")
