#!/usr/bin/env python3
"""Independent integrity checks for the launcher-mounted audit inputs."""

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
    """Reimplement the stage-1 content-tree digest independently."""
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
                raise RuntimeError(f"unsupported tree entry: {path}")
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


audit = json.loads(Path("/audit-input.json").read_text(encoding="utf-8"))
campaign = json.loads(
    Path("/audit-campaign-lock.json").read_text(encoding="utf-8")
)
result = json.loads(Path("/generation-result.json").read_text(encoding="utf-8"))
invocation = json.loads(
    Path("/generation-evidence/invocation.json").read_text(encoding="utf-8")
)
usage = json.loads(
    Path("/generation-evidence/usage.json").read_text(encoding="utf-8")
)

assert audit["record_layout"] == "legacy-selected-stage1"
assert audit["semantics_mode"] == "GENERATED_SEMANTICS"
assert audit["audit_campaign"] == campaign
assert not Path("/reference/reference-semantics").exists()

required_files = [
    Path("/audit-input.json"),
    Path("/audit-campaign-lock.json"),
    Path("/run.json"),
    Path("/task.json"),
    Path("/generation-result.json"),
    Path("/generation-evidence/invocation.json"),
    Path("/generation-evidence/metrics.json"),
    Path("/generation-evidence/usage.json"),
    Path("/generation-evidence/codex-last.txt"),
    Path("/generation-evidence/codex-output.log"),
    Path("/generation-evidence/prompt.txt"),
    Path("/reference/canonical.py"),
    Path("/reference/prompt.py"),
    Path("/reference/py2mpy.py"),
]
required_directories = [
    Path("/candidate"),
    Path("/generation-evidence/codex-trace"),
]
for path in required_files:
    assert path.is_file() and not path.is_symlink(), path
for path in required_directories:
    assert path.is_dir() and not path.is_symlink(), path
for root in (Path("/candidate"), Path("/generation-evidence/codex-trace")):
    for path in root.rglob("*"):
        assert not path.is_symlink(), path

hash_checks = {
    "/audit-campaign-lock.json": "audit_campaign_lock_sha256",
    "/run.json": "run_manifest_sha256",
    "/task.json": "task_manifest_sha256",
    "/generation-result.json": "stage1_result_sha256",
    "/reference/canonical.py": "canonical_sha256",
    "/reference/prompt.py": "trusted_prompt_sha256",
    "/reference/py2mpy.py": "trusted_translator_sha256",
    "/candidate/prompt.py": "candidate_prompt_sha256",
    "/candidate/py2mpy.py": "candidate_translator_sha256",
    "/generation-evidence/invocation.json": "stage1_invocation_sha256",
    "/generation-evidence/metrics.json": "generation_metrics_sha256",
    "/generation-evidence/usage.json": "generation_usage_sha256",
    "/generation-evidence/codex-last.txt": "generation_codex_last_sha256",
    "/generation-evidence/codex-output.log": "generation_codex_output_sha256",
    "/generation-evidence/prompt.txt": "generation_prompt_sha256",
}
for name, field in hash_checks.items():
    actual = sha256_file(Path(name))
    expected = audit["hashes"][field]
    assert actual == expected, (name, actual, expected)
    print(f"MATCH {field} {actual} {name}")

trace_file = next(Path("/generation-evidence/codex-trace").rglob("*.jsonl"))
trace_file_sha = sha256_file(trace_file)
expected_trace_file_sha = result["outputs"]["evidence"][
    str(trace_file.relative_to("/generation-evidence"))
]
assert trace_file_sha == expected_trace_file_sha
print(f"MATCH generation-result trace-file {trace_file_sha} {trace_file}")

trace_tree_sha = pipeline_tree_sha256(
    Path("/generation-evidence/codex-trace")
)
assert trace_tree_sha == usage["source_trace_sha256"]
print(f"MATCH usage trace-tree {trace_tree_sha}")

candidate_tree_sha = pipeline_tree_sha256(Path("/candidate"))
for record, expected in (
    ("generation-result", result["outputs"]["workspace_sha256"]),
    ("invocation retained", invocation["retained_workspace_sha256"]),
):
    assert candidate_tree_sha == expected
    print(f"MATCH {record} candidate-tree {candidate_tree_sha}")

assert Path("/candidate/prompt.py").read_bytes() == Path(
    "/reference/prompt.py"
).read_bytes()
assert Path("/candidate/py2mpy.py").read_bytes() == Path(
    "/reference/py2mpy.py"
).read_bytes()
print("MATCH candidate prompt bytes to trusted prompt")
print("MATCH candidate translator bytes to trusted translator")

print("CANDIDATE FILE HASHES")
for path in sorted(Path("/candidate").rglob("*")):
    if path.is_file():
        print(f"{sha256_file(path)}  {path}")

print(
    "NOTE launcher candidate_tree_sha256="
    f"{audit['hashes']['candidate_tree_sha256']}"
)
print(
    "NOTE launcher generation_codex_trace_sha256="
    f"{audit['hashes']['generation_codex_trace_sha256']}"
)
print("ALL CHECKED CONTENT HASHES AND FILE-TYPE CHECKS PASSED")
