#!/usr/bin/env python3
"""Independent, read-only integrity checks for the mounted audit inputs."""

from __future__ import annotations

from collections import Counter
import hashlib
import json
import os
from pathlib import Path
import stat


AUDIT_INPUT = Path("/audit-input.json")
AUDIT_LOCK = Path("/audit-campaign-lock.json")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def pipeline_tree_digest(root: Path) -> str:
    """Reimplement the pipeline-v2 tree digest over names, types, sizes, bytes."""
    root = root.resolve(strict=True)
    digest = hashlib.sha256()
    pending = [root]
    entries: list[tuple[str, str, Path]] = []
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
                raise RuntimeError(f"linked/unsupported tree entry: {path}")
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
        raise RuntimeError(f"not a real regular file: {path}")


def require_directory(path: Path) -> None:
    mode = path.lstat().st_mode
    if not stat.S_ISDIR(mode):
        raise RuntimeError(f"not a real directory: {path}")


audit_input = json.loads(AUDIT_INPUT.read_text(encoding="utf-8"))
lock = json.loads(AUDIT_LOCK.read_text(encoding="utf-8"))
result = json.loads(Path("/generation-result.json").read_text(encoding="utf-8"))
invocation = json.loads(
    Path("/generation-evidence/invocation.json").read_text(encoding="utf-8")
)
usage = json.loads(
    Path("/generation-evidence/usage.json").read_text(encoding="utf-8")
)

print(f"record_layout={audit_input['record_layout']}")
print(f"semantics_mode={audit_input['semantics_mode']}")
assert audit_input["record_layout"] == "legacy-selected-stage1"
assert audit_input["semantics_mode"] == "GENERATED_SEMANTICS"

required_files = [
    Path("/audit-input.json"),
    Path("/audit-campaign-lock.json"),
    Path("/audit-prompt.md"),
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
required_directories = [
    Path("/candidate"),
    Path("/generation-evidence"),
    Path("/generation-evidence/codex-trace"),
]
for path in required_files:
    require_regular(path)
for path in required_directories:
    require_directory(path)
print(f"required_real_files={len(required_files)} OK")
print(f"required_real_directories={len(required_directories)} OK")

assert audit_input["audit_campaign"] == lock
assert (
    sha256_file(AUDIT_LOCK)
    == audit_input["hashes"]["audit_campaign_lock_sha256"]
)
assert sha256_file(Path("/audit-prompt.md")) == lock["audit_prompt_sha256"]
print("campaign_block_equals_lock=true")
print("campaign_lock_hash_matches=true")
print("audit_prompt_hash_matches_campaign=true")

direct_hashes = {
    "/audit-campaign-lock.json": "audit_campaign_lock_sha256",
    "/candidate/prompt.py": "candidate_prompt_sha256",
    "/candidate/py2mpy.py": "candidate_translator_sha256",
    "/reference/canonical.py": "canonical_sha256",
    "/reference/prompt.py": "trusted_prompt_sha256",
    "/reference/py2mpy.py": "trusted_translator_sha256",
    "/run.json": "run_manifest_sha256",
    "/task.json": "task_manifest_sha256",
    "/generation-result.json": "stage1_result_sha256",
    "/generation-evidence/invocation.json": "stage1_invocation_sha256",
    "/generation-evidence/metrics.json": "generation_metrics_sha256",
    "/generation-evidence/usage.json": "generation_usage_sha256",
    "/generation-evidence/codex-last.txt": "generation_codex_last_sha256",
    "/generation-evidence/codex-output.log": "generation_codex_output_sha256",
    "/generation-evidence/prompt.txt": "generation_prompt_sha256",
}
for path_text, key in direct_hashes.items():
    actual = sha256_file(Path(path_text))
    expected = audit_input["hashes"][key]
    assert actual == expected, (path_text, actual, expected)
    print(f"hash OK {key}={actual}")

assert Path("/candidate/prompt.py").read_bytes() == Path(
    "/reference/prompt.py"
).read_bytes()
assert Path("/candidate/py2mpy.py").read_bytes() == Path(
    "/reference/py2mpy.py"
).read_bytes()
assert not Path("/reference/reference-semantics").exists()
print("candidate_prompt_byte_identical=true")
print("candidate_translator_byte_identical=true")
print("trusted_reference_semantics_absent=true")

for root in (Path("/candidate"), Path("/generation-evidence")):
    for path in root.rglob("*"):
        mode = path.lstat().st_mode
        if not (stat.S_ISREG(mode) or stat.S_ISDIR(mode)):
            raise RuntimeError(f"linked/unsupported entry: {path}")
print("candidate_and_generation_trees_have_only_real_files_and_directories=true")

candidate_digest = pipeline_tree_digest(Path("/candidate"))
expected_workspace = result["outputs"]["workspace_sha256"]
assert candidate_digest == expected_workspace
assert candidate_digest == invocation["retained_workspace_sha256"]
print(f"candidate_pipeline_tree_digest={candidate_digest}")
print("candidate_tree_matches_generation_workspace=true")
print(
    "audit_input_candidate_tree_record="
    + audit_input["hashes"]["candidate_tree_sha256"]
    + " (launcher-specific aggregate; all mounted files are independently hashed above)"
)

trace_root = Path("/generation-evidence/codex-trace")
trace_digest = pipeline_tree_digest(trace_root)
assert trace_digest == usage["source_trace_sha256"]
print(f"trace_pipeline_tree_digest={trace_digest}")
print("trace_tree_matches_usage_source_trace=true")

evidence_hashes = result["outputs"]["evidence"]
for relative, expected in sorted(evidence_hashes.items()):
    path = Path("/generation-evidence") / relative
    require_regular(path)
    actual = sha256_file(path)
    assert actual == expected, (relative, actual, expected)
    print(f"result-evidence-hash OK {relative}={actual}")

json_records = [
    "/run.json",
    "/task.json",
    "/generation-result.json",
    "/generation-evidence/invocation.json",
    "/generation-evidence/metrics.json",
    "/generation-evidence/usage.json",
]
for path_text in json_records:
    document = json.loads(Path(path_text).read_text(encoding="utf-8"))
    print(
        f"json-read OK {path_text} keys={','.join(sorted(document.keys()))}"
    )

trace_files = sorted(trace_root.rglob("*.jsonl"))
assert trace_files
outer_types: Counter[str] = Counter()
payload_types: Counter[str] = Counter()
roles: Counter[str] = Counter()
trace_lines = 0
for trace_file in trace_files:
    with trace_file.open(encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, 1):
            record = json.loads(line)
            trace_lines += 1
            outer_types[str(record.get("type"))] += 1
            payload = record.get("payload")
            if isinstance(payload, dict):
                payload_types[str(payload.get("type"))] += 1
                if "role" in payload:
                    roles[str(payload["role"])] += 1
print(f"trace_files={len(trace_files)} trace_json_lines={trace_lines}")
print(f"trace_outer_types={dict(sorted(outer_types.items()))}")
print(f"trace_payload_types={dict(sorted(payload_types.items()))}")
print(f"trace_roles={dict(sorted(roles.items()))}")

for path_text in (
    "/generation-evidence/codex-last.txt",
    "/generation-evidence/codex-output.log",
    "/generation-evidence/prompt.txt",
):
    text = Path(path_text).read_text(encoding="utf-8")
    print(
        f"text-read OK {path_text} bytes={len(text.encode())} "
        f"lines={len(text.splitlines())} "
        f"#Top_count={text.count('#Top')} "
        f"KPROVE_PASSED_count={text.count('KPROVE_PASSED')}"
    )

print("PROVENANCE_AUDIT_OK")
