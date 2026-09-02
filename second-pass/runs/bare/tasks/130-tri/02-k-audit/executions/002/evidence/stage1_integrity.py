#!/usr/bin/env python3
"""Independent integrity checks for the mounted audit inputs.

This deliberately reads container_paths from /audit-input.json and never
follows the host provenance paths recorded alongside them.
"""

from __future__ import annotations

import hashlib
import json
import os
import stat
from collections import Counter
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_tree(root: Path) -> str:
    """The pipeline-v2 tree digest used by the generation manifests."""
    if not root.is_dir() or root.is_symlink():
        raise AssertionError(f"not a real directory: {root}")
    digest = hashlib.sha256()
    pending = [root]
    entries: list[tuple[str, str, Path]] = []
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


def require_file(path: Path) -> None:
    mode = path.lstat().st_mode
    assert stat.S_ISREG(mode), f"required path is not a regular file: {path}"


def require_dir(path: Path) -> None:
    mode = path.lstat().st_mode
    assert stat.S_ISDIR(mode), f"required path is not a real directory: {path}"


def load_json(path: Path) -> object:
    require_file(path)
    return json.loads(path.read_text(encoding="utf-8"))


audit = load_json(AUDIT_INPUT)
assert isinstance(audit, dict)
assert audit["record_layout"] == "legacy-selected-stage1"
assert audit["semantics_mode"] == "GENERATED_SEMANTICS"
paths = {name: Path(value) for name, value in audit["container_paths"].items()}

required_files = [
    AUDIT_INPUT,
    paths["audit_campaign_lock"],
    paths["run_manifest"],
    paths["task_manifest"],
    paths["stage1_result"],
    paths["canonical"],
    paths["trusted_prompt"],
    paths["translator"],
    paths["generation_manifest"],
    paths["generation_metrics"],
    paths["generation_last"],
    paths["generation_output"],
    paths["generation_root"] / "prompt.txt",
]
usage_path = paths["generation_root"] / "usage.json"
if usage_path.exists():
    required_files.append(usage_path)
required_dirs = [
    paths["candidate"],
    paths["generation_root"],
    paths["generation_trace"],
]

for path in required_files:
    require_file(path)
for path in required_dirs:
    require_dir(path)

candidate_required = [
    "prompt.py",
    "py2mpy.py",
    "solution.py",
    "solution.mpy",
    "semantic.k",
    "verification.k",
    "spec.k",
    "prove.sh",
]
for name in candidate_required:
    require_file(paths["candidate"] / name)

assert not Path("/reference/reference-semantics").exists()
assert not (paths["candidate"] / "reference-semantics").exists()

campaign_lock = load_json(paths["audit_campaign_lock"])
assert campaign_lock == audit["audit_campaign"]
assert (
    sha256_file(paths["audit_campaign_lock"])
    == audit["hashes"]["audit_campaign_lock_sha256"]
)

hash_checks = {
    paths["run_manifest"]: "run_manifest_sha256",
    paths["task_manifest"]: "task_manifest_sha256",
    paths["stage1_result"]: "stage1_result_sha256",
    paths["canonical"]: "canonical_sha256",
    paths["trusted_prompt"]: "trusted_prompt_sha256",
    paths["translator"]: "trusted_translator_sha256",
    paths["candidate"] / "prompt.py": "candidate_prompt_sha256",
    paths["candidate"] / "py2mpy.py": "candidate_translator_sha256",
    paths["generation_manifest"]: "stage1_invocation_sha256",
    paths["generation_metrics"]: "generation_metrics_sha256",
    paths["generation_last"]: "generation_codex_last_sha256",
    paths["generation_output"]: "generation_codex_output_sha256",
    paths["generation_root"] / "prompt.txt": "generation_prompt_sha256",
}
if usage_path.exists():
    hash_checks[usage_path] = "generation_usage_sha256"

for path, key in hash_checks.items():
    actual = sha256_file(path)
    expected = audit["hashes"][key]
    assert actual == expected, f"hash mismatch: {path}: {actual} != {expected}"
    print(f"SHA256 OK {path} {actual}")

assert (paths["candidate"] / "prompt.py").read_bytes() == paths[
    "trusted_prompt"
].read_bytes()
assert (paths["candidate"] / "py2mpy.py").read_bytes() == paths[
    "translator"
].read_bytes()
assert audit["integrity"]["candidate_prompt_matches_trusted"] is True
assert audit["integrity"]["candidate_translator_matches_trusted"] is True

run_manifest = load_json(paths["run_manifest"])
task_manifest = load_json(paths["task_manifest"])
stage1_result = load_json(paths["stage1_result"])
invocation = load_json(paths["generation_manifest"])
metrics = load_json(paths["generation_metrics"])
usage = load_json(usage_path) if usage_path.exists() else None
assert {
    key: value for key, value in audit["manifest"].items() if key != "config"
} == task_manifest
assert audit["manifest"]["config"] == audit["config"]
assert run_manifest["run_id"] == audit["run_id"]
assert task_manifest["problem_id"] == audit["problem_id"]
assert stage1_result["invocation"] == invocation["name"]
assert metrics["exit_code"] == invocation["exit_code"] == 0
assert stage1_result["status"] == invocation["status"] == "SUCCEEDED"

for relative, expected in sorted(stage1_result["outputs"]["evidence"].items()):
    evidence_path = paths["generation_root"] / relative
    require_file(evidence_path)
    actual = sha256_file(evidence_path)
    assert actual == expected
    print(f"STAGE RESULT EVIDENCE SHA256 OK {evidence_path} {actual}")

trace_files = sorted(paths["generation_trace"].rglob("*"))
trace_regular = [path for path in trace_files if path.is_file()]
assert trace_regular and all(not path.is_symlink() for path in trace_files)
events = Counter()
payload_events = Counter()
session_ids: set[str] = set()
trace_lines = 0
for path in trace_regular:
    require_file(path)
    expected = stage1_result["outputs"]["evidence"].get(
        str(path.relative_to(paths["generation_root"]))
    )
    if expected is not None:
        actual = sha256_file(path)
        assert actual == expected
        print(f"TRACE FILE SHA256 OK {path} {actual}")
    with path.open(encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, 1):
            if not line.strip():
                continue
            event = json.loads(line)
            assert isinstance(event, dict)
            trace_lines += 1
            events[event.get("type")] += 1
            payload = event.get("payload")
            if isinstance(payload, dict):
                payload_events[payload.get("type")] += 1
                if event.get("type") == "session_meta" and payload.get("id"):
                    session_ids.add(payload["id"])
assert session_ids == {invocation["session_id"]}

output_bytes = paths["generation_output"].read_bytes()
output_text = output_bytes.decode("utf-8")
last_text = paths["generation_last"].read_text(encoding="utf-8")
prompt_text = (paths["generation_root"] / "prompt.txt").read_text(encoding="utf-8")
assert "RESULT: KPROVE_PASSED" in output_text
assert "RESULT: KPROVE_PASSED" in last_text
assert "writing your own semantics" in prompt_text

candidate_pipeline_digest = sha256_tree(paths["candidate"])
trace_pipeline_digest = sha256_tree(paths["generation_trace"])
assert candidate_pipeline_digest == invocation["retained_workspace_sha256"]
assert candidate_pipeline_digest == stage1_result["outputs"]["workspace_sha256"]
if usage is not None:
    assert trace_pipeline_digest == usage["source_trace_sha256"]

print(f"CAMPAIGN BLOCK MATCH {campaign_lock == audit['audit_campaign']}")
print(f"RECORD LAYOUT {audit['record_layout']}")
print(f"SEMANTICS MODE {audit['semantics_mode']}")
print("REFERENCE SEMANTICS ABSENT")
print(f"CANDIDATE PIPELINE TREE SHA256 {candidate_pipeline_digest}")
print(f"TRACE PIPELINE TREE SHA256 {trace_pipeline_digest}")
print(f"TRACE LINES {trace_lines}")
print(f"TRACE EVENT TYPES {dict(events)}")
print(f"TRACE PAYLOAD TYPES {dict(payload_events)}")
print(f"GENERATION OUTPUT BYTES {len(output_bytes)}")
print(f"GENERATION OUTPUT LINES {len(output_text.splitlines())}")
print("STAGE1 INTEGRITY PASS")
