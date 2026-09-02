#!/usr/bin/env python3
"""Independent integrity/readability checks for the mounted audit inputs."""

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


def pipeline_tree_sha256(root: Path) -> str:
    """Reproduce pipeline_contract.sha256_tree without importing benchmark code."""
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
                raise AssertionError(f"linked/unsupported tree entry: {path}")
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
    assert stat.S_ISREG(mode), f"not a real regular file: {path}"
    path.read_bytes()


def require_directory(path: Path) -> None:
    mode = path.lstat().st_mode
    assert stat.S_ISDIR(mode), f"not a real directory: {path}"


audit = json.loads(AUDIT_INPUT.read_text())
assert audit["record_layout"] == "legacy-selected-stage1"
assert audit["semantics_mode"] == "GENERATED_SEMANTICS"

required_files = [
    AUDIT_INPUT,
    Path("/audit-campaign-lock.json"),
    Path("/run.json"),
    Path("/task.json"),
    Path("/generation-result.json"),
    Path("/reference/canonical.py"),
    Path("/reference/prompt.py"),
    Path("/reference/py2mpy.py"),
    Path("/generation-evidence/invocation.json"),
    Path("/generation-evidence/metrics.json"),
    Path("/generation-evidence/codex-last.txt"),
    Path("/generation-evidence/codex-output.log"),
    Path("/generation-evidence/prompt.txt"),
]
usage = Path("/generation-evidence/usage.json")
if usage.exists():
    required_files.append(usage)
required_dirs = [
    Path("/candidate"),
    Path("/generation-evidence"),
    Path("/generation-evidence/codex-trace"),
]
for path in required_files:
    require_regular(path)
for path in required_dirs:
    require_directory(path)

assert not Path("/reference/reference-semantics").exists()
campaign = json.loads(Path("/audit-campaign-lock.json").read_text())
assert campaign == audit["audit_campaign"]

hash_pairs = {
    "audit_campaign_lock_sha256": Path("/audit-campaign-lock.json"),
    "canonical_sha256": Path("/reference/canonical.py"),
    "candidate_prompt_sha256": Path("/candidate/prompt.py"),
    "candidate_translator_sha256": Path("/candidate/py2mpy.py"),
    "trusted_prompt_sha256": Path("/reference/prompt.py"),
    "trusted_translator_sha256": Path("/reference/py2mpy.py"),
    "generation_codex_last_sha256": Path("/generation-evidence/codex-last.txt"),
    "generation_codex_output_sha256": Path("/generation-evidence/codex-output.log"),
    "generation_metrics_sha256": Path("/generation-evidence/metrics.json"),
    "generation_prompt_sha256": Path("/generation-evidence/prompt.txt"),
    "generation_usage_sha256": Path("/generation-evidence/usage.json"),
    "run_manifest_sha256": Path("/run.json"),
    "stage1_invocation_sha256": Path("/generation-evidence/invocation.json"),
    "stage1_result_sha256": Path("/generation-result.json"),
    "task_manifest_sha256": Path("/task.json"),
}
print(f"record_layout={audit['record_layout']}")
print(f"semantics_mode={audit['semantics_mode']}")
print(f"required_regular_files={len(required_files)}")
print(f"campaign_json_equal={campaign == audit['audit_campaign']}")
for key, path in hash_pairs.items():
    actual = sha256_file(path)
    expected = audit["hashes"][key]
    print(f"{key}: expected={expected} actual={actual} match={actual == expected}")
    assert actual == expected

assert Path("/candidate/prompt.py").read_bytes() == Path("/reference/prompt.py").read_bytes()
assert Path("/candidate/py2mpy.py").read_bytes() == Path("/reference/py2mpy.py").read_bytes()
print("candidate_prompt_byte_equal_trusted=True")
print("candidate_translator_byte_equal_trusted=True")

invocation = json.loads(Path("/generation-evidence/invocation.json").read_text())
result = json.loads(Path("/generation-result.json").read_text())
candidate_tree = pipeline_tree_sha256(Path("/candidate"))
trace_tree = pipeline_tree_sha256(Path("/generation-evidence/codex-trace"))
print(f"audit_recorded_candidate_tree_sha256={audit['hashes']['candidate_tree_sha256']}")
print(
    "audit_recorded_generation_codex_trace_sha256="
    f"{audit['hashes']['generation_codex_trace_sha256']}"
)
print(f"candidate_pipeline_tree_sha256={candidate_tree}")
print(f"invocation_retained_workspace_sha256={invocation['retained_workspace_sha256']}")
print(f"candidate_tree_matches_invocation={candidate_tree == invocation['retained_workspace_sha256']}")
print(f"candidate_tree_matches_result={candidate_tree == result['outputs']['workspace_sha256']}")
assert candidate_tree == invocation["retained_workspace_sha256"]
assert candidate_tree == result["outputs"]["workspace_sha256"]
print(f"trace_pipeline_tree_sha256={trace_tree}")
if usage.exists():
    usage_doc = json.loads(usage.read_text())
    print(f"usage_source_trace_sha256={usage_doc['source_trace_sha256']}")
    print(f"trace_tree_matches_usage={trace_tree == usage_doc['source_trace_sha256']}")
    assert trace_tree == usage_doc["source_trace_sha256"]

trace_files = sorted(Path("/generation-evidence/codex-trace").rglob("*"))
trace_regular = [p for p in trace_files if p.is_file() and not p.is_symlink()]
assert trace_regular
type_counts: Counter[str] = Counter()
payload_counts: Counter[str] = Counter()
line_count = 0
for path in trace_regular:
    expected = result["outputs"]["evidence"][str(path.relative_to("/generation-evidence"))]
    actual = sha256_file(path)
    print(
        f"trace_file={path.relative_to('/generation-evidence')} "
        f"expected={expected} actual={actual} match={expected == actual}"
    )
    assert expected == actual
    with path.open() as stream:
        for line_count_in_file, line in enumerate(stream, 1):
            document = json.loads(line)
            type_counts[document.get("type", "<none>")] += 1
            payload = document.get("payload")
            payload_type = payload.get("type", "<none>") if isinstance(payload, dict) else "<none>"
            payload_counts[payload_type] += 1
        line_count += line_count_in_file
print(f"trace_files={len(trace_regular)} trace_lines={line_count}")
print(f"trace_record_types={dict(sorted(type_counts.items()))}")
print(f"trace_payload_types={dict(sorted(payload_counts.items()))}")

for name in ("invocation.json", "metrics.json", "usage.json"):
    path = Path("/generation-evidence") / name
    if path.exists():
        json.loads(path.read_text())
for path in (
    Path("/run.json"),
    Path("/task.json"),
    Path("/generation-result.json"),
):
    json.loads(path.read_text())
for path in (
    Path("/generation-evidence/codex-last.txt"),
    Path("/generation-evidence/codex-output.log"),
    Path("/generation-evidence/prompt.txt"),
):
    data = path.read_bytes()
    print(f"read_text_record={path.name} bytes={len(data)}")

print("STAGE1_INTEGRITY_OK")
