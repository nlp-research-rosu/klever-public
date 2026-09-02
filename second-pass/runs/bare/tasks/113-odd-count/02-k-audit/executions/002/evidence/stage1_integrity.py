#!/usr/bin/env python3
"""Independent, read-only provenance and mount-integrity checks."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from collections import Counter
from pathlib import Path


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def pipeline_tree_sha256(root: Path) -> str:
    """Reimplement the pipeline-v2 length/type/size/content tree digest."""
    if not root.is_dir() or root.is_symlink():
        raise AssertionError(f"not a real directory: {root}")
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
    if not path.is_file() or path.is_symlink():
        raise AssertionError(f"required regular file missing/mistyped/linked: {path}")


def require_directory(path: Path) -> None:
    if not path.is_dir() or path.is_symlink():
        raise AssertionError(f"required real directory missing/mistyped/linked: {path}")


audit_path = Path("/audit-input.json")
lock_path = Path("/audit-campaign-lock.json")
require_regular(audit_path)
require_regular(lock_path)
audit = json.loads(audit_path.read_text(encoding="utf-8"))
lock = json.loads(lock_path.read_text(encoding="utf-8"))

print(f"record_layout={audit['record_layout']}")
print(f"semantics_mode={audit['semantics_mode']}")
print(f"problem_id={audit['problem_id']}")
assert audit["record_layout"] == "legacy-selected-stage1"
assert audit["semantics_mode"] == "GENERATED_SEMANTICS"
assert audit["audit_campaign"] == lock
print("campaign_block_equals_lock=true")

actual_lock_hash = sha256_file(lock_path)
expected_lock_hash = audit["hashes"]["audit_campaign_lock_sha256"]
print(f"audit_campaign_lock_sha256 actual={actual_lock_hash} expected={expected_lock_hash}")
assert actual_lock_hash == expected_lock_hash

container_paths = {key: Path(value) for key, value in audit["container_paths"].items()}
directory_keys = {"candidate", "generation_root", "generation_trace"}
for key, path in sorted(container_paths.items()):
    if key in directory_keys:
        require_directory(path)
        print(f"container_path {key}=real-directory:{path}")
    else:
        require_regular(path)
        print(f"container_path {key}=regular-file:{path}")

required_files = [
    Path("/run.json"),
    Path("/task.json"),
    Path("/generation-result.json"),
    Path("/generation-evidence/invocation.json"),
    Path("/generation-evidence/metrics.json"),
    Path("/generation-evidence/codex-last.txt"),
    Path("/generation-evidence/codex-output.log"),
    Path("/generation-evidence/prompt.txt"),
]
for path in required_files:
    require_regular(path)
    print(f"required_record=regular-file:{path}")
require_directory(Path("/generation-evidence/codex-trace"))
print("required_record=real-directory:/generation-evidence/codex-trace")

usage_path = Path("/generation-evidence/usage.json")
if usage_path.exists():
    require_regular(usage_path)
    print("optional_usage=regular-file:/generation-evidence/usage.json")
else:
    print("optional_usage=absent")

reference_semantics = Path("/reference/reference-semantics")
assert audit["mount_reference_semantics"] is False
assert audit["reference_semantics"] is None
assert not reference_semantics.exists() and not reference_semantics.is_symlink()
print("generated_semantics_boundary=trusted-reference-semantics-absent")

hash_checks = {
    "audit_campaign_lock_sha256": lock_path,
    "canonical_sha256": Path("/reference/canonical.py"),
    "trusted_prompt_sha256": Path("/reference/prompt.py"),
    "candidate_prompt_sha256": Path("/candidate/prompt.py"),
    "trusted_translator_sha256": Path("/reference/py2mpy.py"),
    "candidate_translator_sha256": Path("/candidate/py2mpy.py"),
    "run_manifest_sha256": Path("/run.json"),
    "task_manifest_sha256": Path("/task.json"),
    "manifest_sha256": Path("/task.json"),
    "stage1_result_sha256": Path("/generation-result.json"),
    "stage1_invocation_sha256": Path("/generation-evidence/invocation.json"),
    "generation_metrics_sha256": Path("/generation-evidence/metrics.json"),
    "generation_codex_last_sha256": Path("/generation-evidence/codex-last.txt"),
    "generation_codex_output_sha256": Path("/generation-evidence/codex-output.log"),
    "generation_prompt_sha256": Path("/generation-evidence/prompt.txt"),
    "generation_usage_sha256": usage_path,
}
for hash_key, path in hash_checks.items():
    require_regular(path)
    actual = sha256_file(path)
    expected = audit["hashes"][hash_key]
    print(f"{hash_key} actual={actual} expected={expected} match={actual == expected}")
    assert actual == expected

assert Path("/candidate/prompt.py").read_bytes() == Path("/reference/prompt.py").read_bytes()
assert Path("/candidate/py2mpy.py").read_bytes() == Path("/reference/py2mpy.py").read_bytes()
print("candidate_prompt_byte_identity=true")
print("candidate_translator_byte_identity=true")

generation_result = json.loads(Path("/generation-result.json").read_text(encoding="utf-8"))
invocation = json.loads(
    Path("/generation-evidence/invocation.json").read_text(encoding="utf-8")
)
usage = json.loads(usage_path.read_text(encoding="utf-8"))

for relative, expected in sorted(
    generation_result["outputs"]["evidence"].items()
):
    path = Path("/generation-evidence") / relative
    require_regular(path)
    actual = sha256_file(path)
    print(f"stage1_evidence {relative} actual={actual} expected={expected} match={actual == expected}")
    assert actual == expected

assert generation_result["outputs"]["evidence"] == invocation["outputs"]["evidence"]
print("result_invocation_evidence_map_identity=true")

candidate_pipeline_hash = pipeline_tree_sha256(Path("/candidate"))
trace_pipeline_hash = pipeline_tree_sha256(Path("/generation-evidence/codex-trace"))
print(f"candidate_pipeline_tree_sha256={candidate_pipeline_hash}")
print(f"generation_result_workspace_sha256={generation_result['outputs']['workspace_sha256']}")
print(f"invocation_retained_workspace_sha256={invocation['retained_workspace_sha256']}")
assert candidate_pipeline_hash == generation_result["outputs"]["workspace_sha256"]
assert candidate_pipeline_hash == invocation["retained_workspace_sha256"]
print("candidate_tree_matches_stage1_workspace=true")

print(f"trace_pipeline_tree_sha256={trace_pipeline_hash}")
print(f"usage_source_trace_sha256={usage['source_trace_sha256']}")
assert trace_pipeline_hash == usage["source_trace_sha256"]
print("trace_tree_matches_usage_source=true")

trace_files = sorted(
    path for path in Path("/generation-evidence/codex-trace").rglob("*") if path.is_file()
)
assert trace_files
trace_event_counts: Counter[str] = Counter()
trace_payload_counts: Counter[str] = Counter()
trace_lines = 0
for trace_file in trace_files:
    require_regular(trace_file)
    with trace_file.open(encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, 1):
            record = json.loads(line)
            trace_lines += 1
            trace_event_counts[str(record.get("type"))] += 1
            payload = record.get("payload")
            if isinstance(payload, dict):
                trace_payload_counts[str(payload.get("type"))] += 1
print(f"structured_trace_files={len(trace_files)}")
print(f"structured_trace_lines={trace_lines}")
print(f"structured_trace_event_counts={dict(sorted(trace_event_counts.items()))}")
print(f"structured_trace_payload_counts={dict(sorted(trace_payload_counts.items()))}")

codex_output = Path("/generation-evidence/codex-output.log")
with codex_output.open("rb") as stream:
    output_lines = sum(1 for _ in stream)
print(f"codex_output_lines={output_lines}")

candidate_entries = sorted(
    path.relative_to("/candidate").as_posix()
    for path in Path("/candidate").rglob("*")
)
print(f"candidate_entries={candidate_entries}")

print("STAGE1_INTEGRITY=PASS")
