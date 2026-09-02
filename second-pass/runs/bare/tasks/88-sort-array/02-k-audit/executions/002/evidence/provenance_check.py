#!/usr/bin/env python3
"""Independent structural and hash checks for the mounted audit inputs."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from collections import Counter
from pathlib import Path


AUDIT = Path("/audit-input.json")
LOCK = Path("/audit-campaign-lock.json")
CANDIDATE = Path("/candidate")
EVIDENCE = Path("/generation-evidence")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_tree(root: Path) -> str:
    """Pipeline-v2 tree digest, independently reimplemented."""
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
            data = path.read_bytes()
            digest.update(len(data).to_bytes(8, "big"))
            digest.update(data)
    return digest.hexdigest()


def require_regular(path: Path) -> None:
    mode = path.lstat().st_mode
    assert stat.S_ISREG(mode), f"not a real regular file: {path}"


def require_directory(path: Path) -> None:
    mode = path.lstat().st_mode
    assert stat.S_ISDIR(mode), f"not a real directory: {path}"


audit = json.loads(AUDIT.read_text(encoding="utf-8"))
lock = json.loads(LOCK.read_text(encoding="utf-8"))
assert audit["record_layout"] == "legacy-selected-stage1"
assert audit["semantics_mode"] == "GENERATED_SEMANTICS"
assert audit["mount_reference_semantics"] is False
assert not Path("/reference/reference-semantics").exists()
assert lock == audit["audit_campaign"]
assert sha256_file(LOCK) == audit["hashes"]["audit_campaign_lock_sha256"]

required_files = [
    AUDIT,
    LOCK,
    Path("/run.json"),
    Path("/task.json"),
    Path("/generation-result.json"),
    EVIDENCE / "invocation.json",
    EVIDENCE / "metrics.json",
    EVIDENCE / "codex-last.txt",
    EVIDENCE / "codex-output.log",
    EVIDENCE / "prompt.txt",
    Path("/reference/canonical.py"),
    Path("/reference/prompt.py"),
    Path("/reference/py2mpy.py"),
]
if (EVIDENCE / "usage.json").exists():
    required_files.append(EVIDENCE / "usage.json")
for path in required_files:
    require_regular(path)
for path in [CANDIDATE, EVIDENCE, EVIDENCE / "codex-trace", Path("/reference")]:
    require_directory(path)

for path in CANDIDATE.rglob("*"):
    mode = path.lstat().st_mode
    assert stat.S_ISREG(mode) or stat.S_ISDIR(mode), (
        f"candidate contains linked or unsupported entry: {path}"
    )
for path in (EVIDENCE / "codex-trace").rglob("*"):
    mode = path.lstat().st_mode
    assert stat.S_ISREG(mode) or stat.S_ISDIR(mode), (
        f"trace contains linked or unsupported entry: {path}"
    )

hash_checks = {
    LOCK: "audit_campaign_lock_sha256",
    Path("/reference/canonical.py"): "canonical_sha256",
    Path("/reference/prompt.py"): "trusted_prompt_sha256",
    Path("/reference/py2mpy.py"): "trusted_translator_sha256",
    CANDIDATE / "prompt.py": "candidate_prompt_sha256",
    CANDIDATE / "py2mpy.py": "candidate_translator_sha256",
    Path("/run.json"): "run_manifest_sha256",
    Path("/task.json"): "task_manifest_sha256",
    Path("/generation-result.json"): "stage1_result_sha256",
    EVIDENCE / "invocation.json": "stage1_invocation_sha256",
    EVIDENCE / "metrics.json": "generation_metrics_sha256",
    EVIDENCE / "codex-last.txt": "generation_codex_last_sha256",
    EVIDENCE / "codex-output.log": "generation_codex_output_sha256",
    EVIDENCE / "prompt.txt": "generation_prompt_sha256",
}
if (EVIDENCE / "usage.json").exists():
    hash_checks[EVIDENCE / "usage.json"] = "generation_usage_sha256"
for path, key in hash_checks.items():
    actual = sha256_file(path)
    expected = audit["hashes"][key]
    assert actual == expected, f"{key}: expected {expected}, got {actual}"
    print(f"OK {key} {actual} {path}")

assert (CANDIDATE / "prompt.py").read_bytes() == Path(
    "/reference/prompt.py"
).read_bytes()
assert (CANDIDATE / "py2mpy.py").read_bytes() == Path(
    "/reference/py2mpy.py"
).read_bytes()

task = json.loads(Path("/task.json").read_text(encoding="utf-8"))
for key, value in task.items():
    assert audit["manifest"][key] == value
assert audit["manifest"]["config"] == audit["config"]
assert sha256_file(Path("/task.json")) == audit["hashes"]["manifest_sha256"]

result = json.loads(Path("/generation-result.json").read_text(encoding="utf-8"))
invocation = json.loads(
    (EVIDENCE / "invocation.json").read_text(encoding="utf-8")
)
metrics = json.loads((EVIDENCE / "metrics.json").read_text(encoding="utf-8"))
assert result["session_id"] == invocation["session_id"]
assert result["status"] == invocation["status"] == metrics["status"] == "SUCCEEDED"

trace_files = sorted((EVIDENCE / "codex-trace").rglob("*.jsonl"))
assert trace_files, "structured trace is empty"
events: Counter[str] = Counter()
payload_types: Counter[str] = Counter()
trace_lines = 0
for trace_file in trace_files:
    require_regular(trace_file)
    expected = result["outputs"]["evidence"][
        trace_file.relative_to(EVIDENCE).as_posix()
    ]
    assert sha256_file(trace_file) == expected
    for line in trace_file.read_text(encoding="utf-8").splitlines():
        record = json.loads(line)
        events[record["type"]] += 1
        payload = record.get("payload")
        if isinstance(payload, dict) and isinstance(payload.get("type"), str):
            payload_types[payload["type"]] += 1
        trace_lines += 1

workspace_digest = sha256_tree(CANDIDATE)
trace_digest = sha256_tree(EVIDENCE / "codex-trace")
assert workspace_digest == result["outputs"]["workspace_sha256"]
assert workspace_digest == invocation["outputs"]["workspace_sha256"]
usage = json.loads((EVIDENCE / "usage.json").read_text(encoding="utf-8"))
assert trace_digest == usage["source_trace_sha256"]

generation_log = (EVIDENCE / "codex-output.log").read_text(
    encoding="utf-8", errors="strict"
)
generation_last = (EVIDENCE / "codex-last.txt").read_text(
    encoding="utf-8", errors="strict"
)
generation_prompt = (EVIDENCE / "prompt.txt").read_text(
    encoding="utf-8", errors="strict"
)
assert "RESULT: KPROVE_PASSED" in generation_last
assert "RESULT: KPROVE_PASSED" in generation_log
assert "writing your own semantics" in generation_prompt

print(f"OK campaign block equals lock ({len(lock)} keys)")
print("OK generated-semantics boundary: no /reference/reference-semantics")
print(f"OK candidate prompt and translator are byte-identical to trusted mounts")
print(f"OK pipeline workspace tree digest {workspace_digest}")
print(
    "INFO launcher audit candidate_tree_sha256 "
    f"{audit['hashes']['candidate_tree_sha256']}"
)
print(f"OK structured trace tree digest {trace_digest}")
print(f"OK structured trace JSON lines {trace_lines}")
print(f"INFO trace top-level types {dict(events)}")
print(f"INFO trace payload types {dict(payload_types)}")
print(
    "INFO generation text sizes "
    f"prompt={len(generation_prompt.encode())} "
    f"output={len(generation_log.encode())} "
    f"last={len(generation_last.encode())}"
)
print("PROVENANCE_CHECK: PASS")
