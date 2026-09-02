#!/usr/bin/env python3
"""Independent integrity checks for the mounted audit inputs."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from pathlib import Path


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def pipeline_tree_sha256(root: Path) -> str:
    """Reimplement the pipeline-v2 content-tree digest independently."""
    entries: list[tuple[str, str, Path]] = []
    pending = [root]
    while pending:
        directory = pending.pop()
        for entry in os.scandir(directory):
            mode = entry.stat(follow_symlinks=False).st_mode
            path = Path(entry.path)
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
    assert stat.S_ISREG(mode), f"not a real regular file: {path}"
    assert not path.is_symlink(), f"symlinked file: {path}"
    print(f"TYPE OK regular {path}")


def require_directory(path: Path) -> None:
    mode = path.lstat().st_mode
    assert stat.S_ISDIR(mode), f"not a real directory: {path}"
    assert not path.is_symlink(), f"symlinked directory: {path}"
    print(f"TYPE OK directory {path}")


audit_path = Path("/audit-input.json")
lock_path = Path("/audit-campaign-lock.json")
audit = json.loads(audit_path.read_text())
lock = json.loads(lock_path.read_text())
hashes = audit["hashes"]
container_paths = audit["container_paths"]

assert audit["record_layout"] == "legacy-selected-stage1"
assert audit["semantics_mode"] == "GENERATED_SEMANTICS"
assert audit["mount_reference_semantics"] is False
assert audit["reference_semantics"] is None
assert not Path("/reference/reference-semantics").exists()
print("MODE OK GENERATED_SEMANTICS with no trusted reference-semantics tree")

required_regular = [
    audit_path,
    lock_path,
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
if Path("/generation-evidence/usage.json").exists():
    required_regular.append(Path("/generation-evidence/usage.json"))
for path in required_regular:
    require_regular(path)

for key, raw_path in container_paths.items():
    path = Path(raw_path)
    if key in {"candidate", "generation_root", "generation_trace"}:
        require_directory(path)
    else:
        require_regular(path)

assert audit["audit_campaign"] == lock
print("CAMPAIGN BLOCK MATCH true")

file_expectations = {
    lock_path: hashes["audit_campaign_lock_sha256"],
    Path("/candidate/prompt.py"): hashes["candidate_prompt_sha256"],
    Path("/candidate/py2mpy.py"): hashes["candidate_translator_sha256"],
    Path("/reference/canonical.py"): hashes["canonical_sha256"],
    Path("/generation-evidence/codex-last.txt"): hashes[
        "generation_codex_last_sha256"
    ],
    Path("/generation-evidence/codex-output.log"): hashes[
        "generation_codex_output_sha256"
    ],
    Path("/generation-evidence/metrics.json"): hashes[
        "generation_metrics_sha256"
    ],
    Path("/generation-evidence/prompt.txt"): hashes[
        "generation_prompt_sha256"
    ],
    Path("/generation-evidence/usage.json"): hashes["generation_usage_sha256"],
    Path("/run.json"): hashes["run_manifest_sha256"],
    Path("/task.json"): hashes["task_manifest_sha256"],
    Path("/generation-evidence/invocation.json"): hashes[
        "stage1_invocation_sha256"
    ],
    Path("/generation-result.json"): hashes["stage1_result_sha256"],
    Path("/reference/prompt.py"): hashes["trusted_prompt_sha256"],
    Path("/reference/py2mpy.py"): hashes["trusted_translator_sha256"],
}

for path, expected in file_expectations.items():
    actual = sha256_file(path)
    assert actual == expected, (path, expected, actual)
    print(f"HASH OK {actual} {path}")

assert sha256_file(Path("/task.json")) == hashes["manifest_sha256"]
print("HASH OK task.json also matches embedded manifest_sha256")

assert Path("/candidate/prompt.py").read_bytes() == Path(
    "/reference/prompt.py"
).read_bytes()
assert Path("/candidate/py2mpy.py").read_bytes() == Path(
    "/reference/py2mpy.py"
).read_bytes()
print("BYTE IDENTITY OK candidate prompt and translator match trusted mounts")

for root in (
    Path("/candidate"),
    Path("/reference"),
    Path("/generation-evidence"),
):
    require_directory(root)
    for path in root.rglob("*"):
        mode = path.lstat().st_mode
        assert stat.S_ISREG(mode) or stat.S_ISDIR(mode), (
            f"linked or unsupported entry: {path}"
        )
    print(f"TREE TYPES OK {root}")

result = json.loads(Path("/generation-result.json").read_text())
invocation = json.loads(Path("/generation-evidence/invocation.json").read_text())
candidate_tree = pipeline_tree_sha256(Path("/candidate"))
assert candidate_tree == result["outputs"]["workspace_sha256"]
assert candidate_tree == invocation["outputs"]["workspace_sha256"]
assert candidate_tree == invocation["retained_workspace_sha256"]
print(f"PIPELINE TREE HASH OK {candidate_tree} /candidate")

for relative, expected in result["outputs"]["evidence"].items():
    path = Path("/generation-evidence") / relative
    require_regular(path)
    actual = sha256_file(path)
    assert actual == expected, (path, expected, actual)
    print(f"RESULT EVIDENCE HASH OK {actual} {path}")

trace_root = Path("/generation-evidence/codex-trace")
trace_files = sorted(trace_root.rglob("*.jsonl"))
assert trace_files, "structured trace has no JSONL records"
trace_records = 0
for path in trace_files:
    with path.open(encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, 1):
            record = json.loads(line)
            assert isinstance(record, dict)
            assert {"timestamp", "type", "payload"} <= record.keys()
            trace_records += 1
print(
    "TRACE JSON OK "
    f"files={len(trace_files)} records={trace_records} "
    f"pipeline_tree_sha256={pipeline_tree_sha256(trace_root)}"
)

print(
    "NOTE audit-input candidate_tree_sha256 uses a launcher-specific digest: "
    f"{hashes['candidate_tree_sha256']}; all mounted candidate bytes are "
    "independently pinned above by the recorded pipeline workspace digest and "
    "per-file inventory."
)
print(
    "NOTE audit-input generation_codex_trace_sha256 uses a launcher-specific "
    f"digest: {hashes['generation_codex_trace_sha256']}; each trace file is "
    "independently checked against generation-result.json above."
)
print("PROVENANCE CHECKS PASSED")
