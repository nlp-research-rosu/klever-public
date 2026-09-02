#!/usr/bin/env python3
"""Independent integrity checks for the launcher-owned audit inputs."""

from __future__ import annotations

import collections
import hashlib
import json
import os
import stat
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")
audit = json.loads(AUDIT_INPUT.read_text())
hashes = audit["hashes"]


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def pipeline_style_tree_hash(root: Path) -> str:
    """Independently implement the retained-workspace tree hash."""
    entries: list[tuple[str, str, Path]] = []
    pending = [root]
    while pending:
        directory = pending.pop()
        for child in os.scandir(directory):
            mode = child.stat(follow_symlinks=False).st_mode
            path = Path(child.path)
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
    mode = path.stat(follow_symlinks=False).st_mode
    assert stat.S_ISREG(mode), f"not a real regular file: {path}"


required_files = [
    Path("/audit-input.json"),
    Path("/audit-campaign-lock.json"),
    Path("/run.json"),
    Path("/task.json"),
    Path("/generation-result.json"),
    Path("/generation-evidence/invocation.json"),
    Path("/generation-evidence/metrics.json"),
    Path("/generation-evidence/codex-last.txt"),
    Path("/generation-evidence/codex-output.log"),
    Path("/generation-evidence/prompt.txt"),
    Path("/reference/canonical.py"),
    Path("/reference/prompt.py"),
    Path("/reference/py2mpy.py"),
]
usage_path = Path("/generation-evidence/usage.json")
if usage_path.exists():
    required_files.append(usage_path)

for required in required_files:
    require_regular(required)

trace_root = Path("/generation-evidence/codex-trace")
assert trace_root.is_dir() and not trace_root.is_symlink()
trace_files = sorted(path for path in trace_root.rglob("*") if path.is_file())
assert trace_files
for trace_file in trace_files:
    require_regular(trace_file)

assert audit["record_layout"] == "legacy-selected-stage1"
assert audit["semantics_mode"] == "GENERATED_SEMANTICS"
assert not Path("/reference/reference-semantics").exists()

campaign_lock = json.loads(Path("/audit-campaign-lock.json").read_text())
assert campaign_lock == audit["audit_campaign"]

direct_checks = {
    Path("/audit-campaign-lock.json"): "audit_campaign_lock_sha256",
    Path("/candidate/prompt.py"): "candidate_prompt_sha256",
    Path("/candidate/py2mpy.py"): "candidate_translator_sha256",
    Path("/reference/canonical.py"): "canonical_sha256",
    Path("/reference/prompt.py"): "trusted_prompt_sha256",
    Path("/reference/py2mpy.py"): "trusted_translator_sha256",
    Path("/run.json"): "run_manifest_sha256",
    Path("/task.json"): "task_manifest_sha256",
    Path("/generation-result.json"): "stage1_result_sha256",
    Path("/generation-evidence/invocation.json"): "stage1_invocation_sha256",
    Path("/generation-evidence/metrics.json"): "generation_metrics_sha256",
    Path("/generation-evidence/codex-last.txt"): "generation_codex_last_sha256",
    Path("/generation-evidence/codex-output.log"): "generation_codex_output_sha256",
    Path("/generation-evidence/prompt.txt"): "generation_prompt_sha256",
}
if usage_path.exists():
    direct_checks[usage_path] = "generation_usage_sha256"

for path, field in direct_checks.items():
    actual = sha256_file(path)
    expected = hashes[field]
    print(f"HASH {path} actual={actual} expected={expected} match={actual == expected}")
    assert actual == expected

assert Path("/candidate/prompt.py").read_bytes() == Path(
    "/reference/prompt.py"
).read_bytes()
assert Path("/candidate/py2mpy.py").read_bytes() == Path(
    "/reference/py2mpy.py"
).read_bytes()

stage_result = json.loads(Path("/generation-result.json").read_text())
for relative, expected in stage_result["outputs"]["evidence"].items():
    evidence_path = Path("/generation-evidence") / relative
    require_regular(evidence_path)
    actual = sha256_file(evidence_path)
    print(
        f"GENERATION_OUTPUT {relative} actual={actual} "
        f"expected={expected} match={actual == expected}"
    )
    assert actual == expected

candidate_tree = pipeline_style_tree_hash(Path("/candidate"))
retained_workspace = json.loads(
    Path("/generation-evidence/invocation.json").read_text()
)["retained_workspace_sha256"]
stage_workspace = stage_result["outputs"]["workspace_sha256"]
print(
    f"CANDIDATE_RETAINED_TREE actual={candidate_tree} "
    f"invocation={retained_workspace} stage_result={stage_workspace}"
)
assert candidate_tree == retained_workspace == stage_workspace

trace_tree = pipeline_style_tree_hash(trace_root)
if usage_path.exists():
    usage_trace = json.loads(usage_path.read_text())["source_trace_sha256"]
    print(f"TRACE_TREE actual={trace_tree} usage_source={usage_trace}")
    assert trace_tree == usage_trace

payload_types: collections.Counter[str | None] = collections.Counter()
outer_types: collections.Counter[str | None] = collections.Counter()
trace_lines = 0
for trace_file in trace_files:
    with trace_file.open() as stream:
        for trace_lines, line in enumerate(stream, trace_lines + 1):
            record = json.loads(line)
            outer_types[record.get("type")] += 1
            payload = record.get("payload")
            payload_types[payload.get("type") if isinstance(payload, dict) else None] += 1
print(f"TRACE_JSON lines={trace_lines} outer_types={dict(outer_types)}")
print(f"TRACE_PAYLOAD_TYPES {dict(payload_types)}")

codex_output = Path("/generation-evidence/codex-output.log").read_text()
print(
    "CODEX_OUTPUT "
    f"lines={len(codex_output.splitlines())} chars={len(codex_output)} "
    f"top_lines={sum(line == '#Top' for line in codex_output.splitlines())} "
    f"result_markers={codex_output.count('RESULT: KPROVE_PASSED')}"
)
print(f"AUDIT_INPUT_SHA256 {sha256_file(AUDIT_INPUT)}")
print("INTEGRITY_STATUS OK")
