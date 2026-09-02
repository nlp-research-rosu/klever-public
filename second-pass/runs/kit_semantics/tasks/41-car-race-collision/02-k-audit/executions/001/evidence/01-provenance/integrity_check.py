#!/usr/bin/env python3
"""Independent provenance and mount-integrity checks for this audit."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")
LOCK = Path("/audit-campaign-lock.json")
TRACE = Path(
    "/generation-evidence/codex-trace/2026/07/25/"
    "rollout-2026-07-25T00-05-21-019f97a9-e3c3-7762-80df-7fa1b1660ec9.jsonl"
)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def pipeline_tree_sha256(root: Path) -> str:
    """Reimplement the pipeline-v3 length-delimited tree digest."""
    if not root.is_dir() or root.is_symlink():
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
                raise AssertionError(f"linked or unsupported entry: {path}")
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
    assert stat.S_ISREG(mode), f"required record is not regular: {path}"
    with path.open("rb") as stream:
        stream.read(1)


audit = json.loads(AUDIT_INPUT.read_text())
lock = json.loads(LOCK.read_text())
assert audit["record_layout"] == "pipeline-v3"
assert audit["semantics_mode"] == "SUPPLIED_SEMANTICS"
assert audit["mount_reference_semantics"] is True
assert lock == audit["audit_campaign"]
assert sha256_file(LOCK) == audit["hashes"]["audit_campaign_lock_sha256"]
print("campaign_block_equal: True")
print("campaign_lock_sha256:", sha256_file(LOCK))

required = [
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
    TRACE,
    Path("/reference/canonical.py"),
    Path("/reference/prompt.py"),
    Path("/reference/py2mpy.py"),
    Path("/candidate"),
    Path("/reference/reference-semantics"),
]
for path in required:
    if path.is_dir() and not path.is_symlink():
        next(path.iterdir())
    else:
        require_regular(path)
print("required_pipeline_v3_records_readable:", len(required))

recorded_file_hashes = {
    Path("/run.json"): "run_manifest_sha256",
    Path("/task.json"): "task_manifest_sha256",
    Path("/generation-result.json"): "stage1_result_sha256",
    Path("/generation-evidence/invocation.json"): "stage1_invocation_sha256",
    Path("/generation-evidence/metrics.json"): "generation_metrics_sha256",
    Path("/generation-evidence/runtime-metrics.json"):
        "generation_runtime_metrics_sha256",
    Path("/generation-evidence/usage.json"): "generation_usage_sha256",
    Path("/generation-evidence/codex-last.txt"):
        "generation_codex_last_sha256",
    Path("/generation-evidence/codex-output.log"):
        "generation_codex_output_sha256",
    Path("/generation-evidence/prompt.txt"): "generation_prompt_sha256",
    Path("/reference/canonical.py"): "canonical_sha256",
    Path("/reference/prompt.py"): "trusted_prompt_sha256",
    Path("/reference/py2mpy.py"): "trusted_translator_sha256",
}
for path, key in recorded_file_hashes.items():
    actual = sha256_file(path)
    expected = audit["hashes"][key]
    assert actual == expected, (path, actual, expected)
    print(f"hash_match {path}: {actual}")

result = json.loads(Path("/generation-result.json").read_text())
invocation = json.loads(
    Path("/generation-evidence/invocation.json").read_text()
)
trace_hash = sha256_file(TRACE)
expected_trace_hash = result["outputs"]["evidence"][str(TRACE.relative_to(
    Path("/generation-evidence")
))]
assert trace_hash == expected_trace_hash
assert invocation["outputs"]["evidence"] == result["outputs"]["evidence"]
candidate_tree = pipeline_tree_sha256(Path("/candidate"))
assert candidate_tree == result["outputs"]["workspace_sha256"]
assert candidate_tree == invocation["outputs"]["workspace_sha256"]
trace_tree = pipeline_tree_sha256(Path("/generation-evidence/codex-trace"))
usage = json.loads(Path("/generation-evidence/usage.json").read_text())
assert trace_tree == usage["source_trace_sha256"]
print("candidate_pipeline_tree_sha256:", candidate_tree)
print("trace_file_sha256:", trace_hash)
print("trace_pipeline_tree_sha256:", trace_tree)

assert Path("/candidate/prompt.py").read_bytes() == Path(
    "/reference/prompt.py"
).read_bytes()
assert Path("/candidate/py2mpy.py").read_bytes() == Path(
    "/reference/py2mpy.py"
).read_bytes()
candidate_semantics = Path("/candidate/reference-semantics")
trusted_semantics = Path("/reference/reference-semantics")
assert pipeline_tree_sha256(candidate_semantics) == pipeline_tree_sha256(
    trusted_semantics
)
for root in [candidate_semantics, trusted_semantics]:
    for entry in root.rglob("*"):
        assert not entry.is_symlink(), f"symlink in semantics tree: {entry}"
candidate_entries = {
    (
        path.relative_to(candidate_semantics).as_posix(),
        "directory" if path.is_dir() else "file",
        None if path.is_dir() else sha256_file(path),
    )
    for path in candidate_semantics.rglob("*")
}
trusted_entries = {
    (
        path.relative_to(trusted_semantics).as_posix(),
        "directory" if path.is_dir() else "file",
        None if path.is_dir() else sha256_file(path),
    )
    for path in trusted_semantics.rglob("*")
}
assert candidate_entries == trusted_entries
print("candidate_prompt_byte_equal: True")
print("candidate_translator_byte_equal: True")
print("supplied_semantics_recursive_equal: True")
print("supplied_semantics_entries:", len(candidate_entries))
print(
    "supplied_semantics_pipeline_tree_sha256:",
    pipeline_tree_sha256(trusted_semantics),
)

trace_types: dict[tuple[str | None, str | None], int] = {}
trace_lines = 0
with TRACE.open() as stream:
    for trace_lines, line in enumerate(stream, 1):
        event = json.loads(line)
        key = (event.get("type"), event.get("payload", {}).get("type"))
        trace_types[key] = trace_types.get(key, 0) + 1
assert trace_lines == 216
print("structured_trace_json_lines:", trace_lines)
for key in sorted(trace_types, key=str):
    print("trace_type", key, trace_types[key])

print("INTEGRITY_CHECK: PASS")
