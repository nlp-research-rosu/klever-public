#!/usr/bin/env python3
"""Independent integrity checks for the launcher-owned audit inputs."""

from __future__ import annotations

import collections
import hashlib
import json
import os
import stat
from pathlib import Path


AUDIT = Path("/audit-input.json")
LOCK = Path("/audit-campaign-lock.json")
CANDIDATE = Path("/candidate")
REFERENCE = Path("/reference")
GEN = Path("/generation-evidence")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def pipeline_tree_hash(root: Path) -> str:
    """Reimplement the schema-v2 pipeline tree digest without importing tooling."""
    if root.is_symlink() or not root.is_dir():
        raise AssertionError(f"not a real directory: {root}")
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
    digest = hashlib.sha256()
    for relative, kind, path in sorted(entries):
        encoded = relative.encode()
        digest.update(len(encoded).to_bytes(4, "big"))
        digest.update(encoded)
        digest.update(kind.encode() + b"\0")
        if kind == "file":
            size = path.stat(follow_symlinks=False).st_size
            digest.update(size.to_bytes(8, "big"))
            with path.open("rb") as stream:
                for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                    digest.update(chunk)
    return digest.hexdigest()


def require_regular(path: Path) -> None:
    mode = path.lstat().st_mode
    if not stat.S_ISREG(mode):
        raise AssertionError(f"required path is not a regular file: {path}")


def require_real_dir(path: Path) -> None:
    mode = path.lstat().st_mode
    if not stat.S_ISDIR(mode):
        raise AssertionError(f"required path is not a real directory: {path}")


audit = json.loads(AUDIT.read_text(encoding="utf-8"))
lock = json.loads(LOCK.read_text(encoding="utf-8"))

assert audit["record_layout"] == "legacy-selected-stage1"
assert audit["semantics_mode"] == "GENERATED_SEMANTICS"
assert audit["audit_campaign"] == lock
assert sha256_file(LOCK) == audit["hashes"]["audit_campaign_lock_sha256"]
assert not (REFERENCE / "reference-semantics").exists()

required_files = [
    AUDIT,
    LOCK,
    Path("/run.json"),
    Path("/task.json"),
    Path("/generation-result.json"),
    GEN / "invocation.json",
    GEN / "metrics.json",
    GEN / "usage.json",
    GEN / "codex-last.txt",
    GEN / "codex-output.log",
    GEN / "prompt.txt",
    REFERENCE / "canonical.py",
    REFERENCE / "prompt.py",
    REFERENCE / "py2mpy.py",
    CANDIDATE / "prompt.py",
    CANDIDATE / "py2mpy.py",
]
for path in required_files:
    require_regular(path)
for path in (CANDIDATE, REFERENCE, GEN, GEN / "codex-trace"):
    require_real_dir(path)

hash_checks = {
    "audit_campaign_lock_sha256": LOCK,
    "canonical_sha256": REFERENCE / "canonical.py",
    "trusted_prompt_sha256": REFERENCE / "prompt.py",
    "trusted_translator_sha256": REFERENCE / "py2mpy.py",
    "candidate_prompt_sha256": CANDIDATE / "prompt.py",
    "candidate_translator_sha256": CANDIDATE / "py2mpy.py",
    "generation_codex_last_sha256": GEN / "codex-last.txt",
    "generation_codex_output_sha256": GEN / "codex-output.log",
    "generation_metrics_sha256": GEN / "metrics.json",
    "generation_prompt_sha256": GEN / "prompt.txt",
    "generation_usage_sha256": GEN / "usage.json",
    "run_manifest_sha256": Path("/run.json"),
    "task_manifest_sha256": Path("/task.json"),
    "stage1_invocation_sha256": GEN / "invocation.json",
    "stage1_result_sha256": Path("/generation-result.json"),
}
for field, path in hash_checks.items():
    actual = sha256_file(path)
    expected = audit["hashes"][field]
    assert actual == expected, (field, expected, actual)
    print(f"HASH OK {field} {actual} {path}")

assert (CANDIDATE / "prompt.py").read_bytes() == (
    REFERENCE / "prompt.py"
).read_bytes()
assert (CANDIDATE / "py2mpy.py").read_bytes() == (
    REFERENCE / "py2mpy.py"
).read_bytes()
assert audit["integrity"]["candidate_prompt_matches_trusted"] is True
assert audit["integrity"]["candidate_translator_matches_trusted"] is True
audit_manifest = dict(audit["manifest"])
audit_manifest.pop("config", None)
assert audit_manifest == json.loads(Path("/task.json").read_text())

result = json.loads(Path("/generation-result.json").read_text())
invocation = json.loads((GEN / "invocation.json").read_text())
usage = json.loads((GEN / "usage.json").read_text())
trace_files = sorted(
    path for path in (GEN / "codex-trace").rglob("*") if path.is_file()
)
assert trace_files
for path in trace_files:
    require_regular(path)
    relative = path.relative_to(GEN).as_posix()
    actual = sha256_file(path)
    assert result["outputs"]["evidence"][relative] == actual
    assert invocation["outputs"]["evidence"][relative] == actual
    print(f"TRACE FILE HASH OK {actual} {relative}")

candidate_pipeline_hash = pipeline_tree_hash(CANDIDATE)
trace_pipeline_hash = pipeline_tree_hash(GEN / "codex-trace")
assert candidate_pipeline_hash == result["outputs"]["workspace_sha256"]
assert candidate_pipeline_hash == invocation["retained_workspace_sha256"]
assert trace_pipeline_hash == usage["source_trace_sha256"]
print(f"PIPELINE TREE HASH OK candidate {candidate_pipeline_hash}")
print(f"PIPELINE TREE HASH OK trace {trace_pipeline_hash}")

# Inspect every structured trace record rather than trusting its summaries.
top_types: collections.Counter[str] = collections.Counter()
payload_types: collections.Counter[str] = collections.Counter()
trace_lines = 0
final_messages: list[str] = []
for path in trace_files:
    with path.open(encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, 1):
            record = json.loads(line)
            assert isinstance(record, dict)
            trace_lines += 1
            top_types[str(record.get("type"))] += 1
            payload = record.get("payload")
            if isinstance(payload, dict):
                payload_types[str(payload.get("type"))] += 1
                if payload.get("type") == "agent_message":
                    final_messages.append(str(payload.get("message")))
print(f"TRACE PARSE OK lines={trace_lines}")
print(f"TRACE TOP TYPES {dict(sorted(top_types.items()))}")
print(f"TRACE PAYLOAD TYPES {dict(sorted(payload_types.items()))}")
print(f"TRACE FINAL MESSAGES {len(final_messages)}")

# Read the complete unstructured log and summarize its candidate claims.
generation_log = (GEN / "codex-output.log").read_text(
    encoding="utf-8", errors="replace"
)
for needle in (
    "kprove",
    "#Top",
    "39 claims",
    "RESULT: KPROVE_PASSED",
    "WarnStuckClaimState",
):
    print(f"GENERATION LOG COUNT {needle!r} {generation_log.count(needle)}")

print("PROVENANCE CHECK PASS")
