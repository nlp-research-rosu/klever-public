#!/usr/bin/env python3
"""Independent mounted-input and legacy-selected-stage1 provenance checks."""

from __future__ import annotations

import collections
import hashlib
import json
import os
import stat
from pathlib import Path


def file_hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def pipeline_tree_hash(root: Path) -> str:
    """Reproduce the length-delimited sha256_tree used by pipeline-v2 records."""
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
            size = path.stat(follow_symlinks=False).st_size
            digest.update(size.to_bytes(8, "big"))
            with path.open("rb") as stream:
                for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                    digest.update(chunk)
    return digest.hexdigest()


def require_regular(path: Path) -> None:
    mode = path.lstat().st_mode
    assert stat.S_ISREG(mode), f"not a real regular file: {path}"


def require_directory(path: Path) -> None:
    mode = path.lstat().st_mode
    assert stat.S_ISDIR(mode), f"not a real directory: {path}"


def report_hash(path: Path, expected: str) -> None:
    require_regular(path)
    actual = file_hash(path)
    print(f"FILE {path}: expected={expected} actual={actual} match={actual == expected}")
    assert actual == expected


audit_input_path = Path("/audit-input.json")
campaign_lock_path = Path("/audit-campaign-lock.json")
require_regular(audit_input_path)
require_regular(campaign_lock_path)
audit_input = json.loads(audit_input_path.read_text())
campaign_lock = json.loads(campaign_lock_path.read_text())

print(f"record_layout={audit_input['record_layout']}")
print(f"semantics_mode={audit_input['semantics_mode']}")
assert audit_input["record_layout"] == "legacy-selected-stage1"
assert audit_input["semantics_mode"] == "GENERATED_SEMANTICS"
assert campaign_lock == audit_input["audit_campaign"]
print("campaign_lock_matches_audit_campaign=True")
report_hash(
    campaign_lock_path,
    audit_input["hashes"]["audit_campaign_lock_sha256"],
)

paths = audit_input["container_paths"]
required_regular_paths = [
    Path(paths["candidate"]) / "prompt.py",
    Path(paths["candidate"]) / "py2mpy.py",
    Path(paths["canonical"]),
    Path(paths["trusted_prompt"]),
    Path(paths["translator"]),
    Path(paths["run_manifest"]),
    Path(paths["task_manifest"]),
    Path(paths["stage1_result"]),
    Path(paths["generation_manifest"]),
    Path(paths["generation_metrics"]),
    Path(paths["generation_last"]),
    Path(paths["generation_output"]),
    Path(paths["generation_root"]) / "prompt.txt",
    Path(paths["generation_root"]) / "usage.json",
]
for path in required_regular_paths:
    require_regular(path)

require_directory(Path(paths["candidate"]))
require_directory(Path(paths["generation_root"]))
require_directory(Path(paths["generation_trace"]))

hash_bindings = {
    Path(paths["canonical"]): "canonical_sha256",
    Path(paths["trusted_prompt"]): "trusted_prompt_sha256",
    Path(paths["translator"]): "trusted_translator_sha256",
    Path(paths["candidate"]) / "prompt.py": "candidate_prompt_sha256",
    Path(paths["candidate"]) / "py2mpy.py": "candidate_translator_sha256",
    Path(paths["run_manifest"]): "run_manifest_sha256",
    Path(paths["task_manifest"]): "task_manifest_sha256",
    Path(paths["stage1_result"]): "stage1_result_sha256",
    Path(paths["generation_manifest"]): "stage1_invocation_sha256",
    Path(paths["generation_metrics"]): "generation_metrics_sha256",
    Path(paths["generation_last"]): "generation_codex_last_sha256",
    Path(paths["generation_output"]): "generation_codex_output_sha256",
    Path(paths["generation_root"]) / "prompt.txt": "generation_prompt_sha256",
    Path(paths["generation_root"]) / "usage.json": "generation_usage_sha256",
}
for path, key in hash_bindings.items():
    report_hash(path, audit_input["hashes"][key])

task_hash = file_hash(Path(paths["task_manifest"]))
assert task_hash == audit_input["hashes"]["manifest_sha256"]
print("manifest_sha256_matches_task_manifest=True")

candidate_root = Path(paths["candidate"])
proof_artifacts = [
    "solution.py",
    "solution.mpy",
    "semantic.k",
    "verification.k",
    "spec.k",
    "prove.sh",
]
for name in proof_artifacts:
    require_regular(candidate_root / name)
print(f"candidate_required_artifacts={','.join(proof_artifacts)}")

assert not (Path("/reference") / "reference-semantics").exists()
assert not (candidate_root / "reference-semantics").exists()
print("generated_semantics_boundary_reference_semantics_absent=True")

assert (candidate_root / "prompt.py").read_bytes() == Path(paths["trusted_prompt"]).read_bytes()
assert (candidate_root / "py2mpy.py").read_bytes() == Path(paths["translator"]).read_bytes()
print("candidate_prompt_byte_matches_trusted=True")
print("candidate_translator_byte_matches_trusted=True")

candidate_pipeline_hash = pipeline_tree_hash(candidate_root)
result = json.loads(Path(paths["stage1_result"]).read_text())
invocation = json.loads(Path(paths["generation_manifest"]).read_text())
print(f"candidate_pipeline_tree_sha256={candidate_pipeline_hash}")
print(f"stage1_workspace_sha256={result['outputs']['workspace_sha256']}")
assert candidate_pipeline_hash == result["outputs"]["workspace_sha256"]
assert candidate_pipeline_hash == invocation["outputs"]["workspace_sha256"]

usage = json.loads((Path(paths["generation_root"]) / "usage.json").read_text())
trace_root = Path(paths["generation_trace"])
trace_pipeline_hash = pipeline_tree_hash(trace_root)
print(f"trace_pipeline_tree_sha256={trace_pipeline_hash}")
print(f"usage_source_trace_sha256={usage['source_trace_sha256']}")
assert trace_pipeline_hash == usage["source_trace_sha256"]

for relative, expected in result["outputs"]["evidence"].items():
    report_hash(Path(paths["generation_root"]) / relative, expected)

trace_files = sorted(trace_root.rglob("*"))
for path in trace_files:
    mode = path.lstat().st_mode
    assert stat.S_ISDIR(mode) or stat.S_ISREG(mode), f"trace has unsupported entry: {path}"

trace_type_counts: collections.Counter[str] = collections.Counter()
response_item_counts: collections.Counter[str] = collections.Counter()
tool_counts: collections.Counter[str] = collections.Counter()
trace_lines = 0
final_messages: list[str] = []
for trace_file in [path for path in trace_files if path.is_file()]:
    with trace_file.open() as stream:
        for line_number, line in enumerate(stream, 1):
            record = json.loads(line)
            trace_lines += 1
            trace_type_counts[record["type"]] += 1
            payload = record.get("payload", {})
            if record["type"] == "response_item":
                subtype = payload.get("type", "<missing>")
                response_item_counts[subtype] += 1
                if subtype in {"function_call", "custom_tool_call"}:
                    tool_counts[payload.get("name", "<missing>")] += 1
                if subtype == "message" and payload.get("role") == "assistant":
                    text = "\n".join(
                        item.get("text", "")
                        for item in payload.get("content", [])
                        if item.get("type") == "output_text"
                    )
                    if text:
                        final_messages.append(text)
print(f"trace_json_lines_valid={trace_lines}")
print(f"trace_types={dict(sorted(trace_type_counts.items()))}")
print(f"trace_response_item_types={dict(sorted(response_item_counts.items()))}")
print(f"trace_tool_calls={dict(sorted(tool_counts.items()))}")
print(f"trace_final_assistant_message={final_messages[-1]!r}")

output_path = Path(paths["generation_output"])
output_text = output_path.read_text(errors="replace")
print(f"codex_output_chars_read={len(output_text)}")
print(f"codex_output_lines_read={len(output_text.splitlines())}")
print(f"codex_output_top_count={output_text.count('#Top')}")

print("PROVENANCE_CHECK=PASS")
