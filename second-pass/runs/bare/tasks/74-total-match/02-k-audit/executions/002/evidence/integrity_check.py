#!/usr/bin/env python3
"""Independent launcher-record and structured-trace integrity checks."""

from __future__ import annotations

import collections
import hashlib
import json
import os
import stat
from pathlib import Path


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def pipeline_tree_digest(root: Path) -> str:
    """Reimplement the pipeline's path/type/size/content tree digest."""
    h = hashlib.sha256()
    entries: list[tuple[str, str, Path]] = []
    pending = [root]
    while pending:
        directory = pending.pop()
        for entry in os.scandir(directory):
            path = Path(entry.path)
            mode = entry.stat(follow_symlinks=False).st_mode
            relative = path.relative_to(root).as_posix()
            if stat.S_ISDIR(mode):
                entries.append((relative, "directory", path))
                pending.append(path)
            elif stat.S_ISREG(mode):
                entries.append((relative, "file", path))
            else:
                raise AssertionError(f"unsupported or linked tree entry: {path}")
    for relative, kind, path in sorted(entries):
        encoded = relative.encode()
        h.update(len(encoded).to_bytes(4, "big"))
        h.update(encoded)
        h.update(kind.encode() + b"\0")
        if kind == "file":
            size = path.stat(follow_symlinks=False).st_size
            h.update(size.to_bytes(8, "big"))
            with path.open("rb") as stream:
                for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                    h.update(chunk)
    return h.hexdigest()


audit = json.loads(Path("/audit-input.json").read_text())
lock = json.loads(Path("/audit-campaign-lock.json").read_text())
task = json.loads(Path("/task.json").read_text())
result = json.loads(Path("/generation-result.json").read_text())
invocation = json.loads(Path("/generation-evidence/invocation.json").read_text())

assert audit["audit_campaign"] == lock
assert sha256_file(Path("/audit-campaign-lock.json")) == audit["hashes"]["audit_campaign_lock_sha256"]
embedded_task = dict(audit["manifest"])
embedded_config = embedded_task.pop("config")
assert embedded_task == task
assert embedded_config == audit["config"] == audit["manifest_config"]
print(f"EMBEDDED_TASK_OK enriched_config={embedded_config}")
assert audit["record_layout"] == "legacy-selected-stage1"
assert audit["semantics_mode"] == "GENERATED_SEMANTICS"
assert not Path("/reference/reference-semantics").exists()

hash_bindings = {
    "/run.json": "run_manifest_sha256",
    "/task.json": "task_manifest_sha256",
    "/generation-result.json": "stage1_result_sha256",
    "/generation-evidence/invocation.json": "stage1_invocation_sha256",
    "/generation-evidence/metrics.json": "generation_metrics_sha256",
    "/generation-evidence/usage.json": "generation_usage_sha256",
    "/generation-evidence/codex-last.txt": "generation_codex_last_sha256",
    "/generation-evidence/codex-output.log": "generation_codex_output_sha256",
    "/generation-evidence/prompt.txt": "generation_prompt_sha256",
    "/reference/canonical.py": "canonical_sha256",
    "/reference/prompt.py": "trusted_prompt_sha256",
    "/reference/py2mpy.py": "trusted_translator_sha256",
    "/candidate/prompt.py": "candidate_prompt_sha256",
    "/candidate/py2mpy.py": "candidate_translator_sha256",
}
for raw_path, field in hash_bindings.items():
    path = Path(raw_path)
    actual = sha256_file(path)
    expected = audit["hashes"][field]
    assert actual == expected, (raw_path, actual, expected)
    print(f"HASH_OK {raw_path} {actual}")

candidate_digest = pipeline_tree_digest(Path("/candidate"))
trace_digest = pipeline_tree_digest(Path("/generation-evidence/codex-trace"))
assert candidate_digest == result["outputs"]["workspace_sha256"]
assert candidate_digest == invocation["retained_workspace_sha256"]
assert trace_digest == json.loads(Path("/generation-evidence/usage.json").read_text())["source_trace_sha256"]
print(f"PIPELINE_TREE_OK /candidate {candidate_digest}")
print(f"PIPELINE_TREE_OK /generation-evidence/codex-trace {trace_digest}")

for relative, expected in result["outputs"]["evidence"].items():
    path = Path("/generation-evidence") / relative
    assert path.is_file() and not path.is_symlink(), path
    actual = sha256_file(path)
    assert actual == expected, (relative, actual, expected)
    print(f"RESULT_EVIDENCE_OK {relative} {actual}")

trace_files = sorted(Path("/generation-evidence/codex-trace").rglob("*"))
trace_files = [path for path in trace_files if path.is_file()]
assert len(trace_files) == 1
type_counts: collections.Counter[str] = collections.Counter()
payload_type_counts: collections.Counter[str] = collections.Counter()
custom_calls = 0
custom_outputs = 0
assistant_messages = 0
event_messages = 0
line_count = 0
for trace_path in trace_files:
    with trace_path.open(encoding="utf-8") as stream:
        for line_count, line in enumerate(stream, 1):
            record = json.loads(line)
            record_type = record["type"]
            type_counts[record_type] += 1
            payload = record.get("payload", {})
            payload_type = payload.get("type")
            if payload_type:
                payload_type_counts[payload_type] += 1
            if payload_type == "custom_tool_call":
                custom_calls += 1
                print(f"TRACE_TOOL_CALL line={line_count} name={payload.get('name')} input={payload.get('input')}")
            elif payload_type == "custom_tool_call_output":
                custom_outputs += 1
            elif payload_type == "message" and payload.get("role") == "assistant":
                assistant_messages += 1
            elif record_type == "event_msg" and payload_type == "agent_message":
                event_messages += 1
assert custom_calls == custom_outputs
print(f"TRACE_JSON_OK files={len(trace_files)} lines={line_count}")
print(f"TRACE_TOP_TYPES {dict(sorted(type_counts.items()))}")
print(f"TRACE_PAYLOAD_TYPES {dict(sorted(payload_type_counts.items()))}")
print(
    "TRACE_COUNTS "
    f"tool_calls={custom_calls} tool_outputs={custom_outputs} "
    f"assistant_messages={assistant_messages} event_messages={event_messages}"
)
print("ALL_INTEGRITY_CHECKS_PASSED")
