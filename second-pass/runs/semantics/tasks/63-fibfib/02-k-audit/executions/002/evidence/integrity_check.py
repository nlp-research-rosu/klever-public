#!/usr/bin/env python3
"""Independent integrity checks for the mounted audit inputs."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from pathlib import Path


AUDIT = Path("/audit-input.json")
LOCK = Path("/audit-campaign-lock.json")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def regular(path: Path) -> bool:
    mode = path.lstat().st_mode
    return stat.S_ISREG(mode)


def real_directory(path: Path) -> bool:
    mode = path.lstat().st_mode
    return stat.S_ISDIR(mode)


def tree_entries(root: Path) -> dict[str, tuple[str, str | None]]:
    result: dict[str, tuple[str, str | None]] = {}
    pending = [root]
    while pending:
        directory = pending.pop()
        for entry in os.scandir(directory):
            path = Path(entry.path)
            mode = entry.stat(follow_symlinks=False).st_mode
            relative = path.relative_to(root).as_posix()
            if stat.S_ISDIR(mode):
                result[relative] = ("directory", None)
                pending.append(path)
            elif stat.S_ISREG(mode):
                result[relative] = ("file", sha256(path))
            else:
                result[relative] = ("unsupported", None)
    return result


def pipeline_tree_sha256(root: Path) -> str:
    """Reproduce the length-delimited tree hash used by generation-result.json."""
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
                raise RuntimeError(f"unsupported tree entry: {path}")
    digest = hashlib.sha256()
    for relative, kind, path in sorted(entries):
        encoded = relative.encode()
        digest.update(len(encoded).to_bytes(4, "big"))
        digest.update(encoded)
        digest.update(kind.encode() + b"\0")
        if kind == "file":
            content = path.read_bytes()
            digest.update(len(content).to_bytes(8, "big"))
            digest.update(content)
    return digest.hexdigest()


audit = json.loads(AUDIT.read_text())
lock = json.loads(LOCK.read_text())

print(f"record_layout={audit['record_layout']}")
print(f"semantics_mode={audit['semantics_mode']}")
print(f"campaign_exact_equal={audit['audit_campaign'] == lock}")
print(
    "campaign_sha256="
    f"{sha256(LOCK)} expected={audit['hashes']['audit_campaign_lock_sha256']}"
)

required_files = [
    AUDIT,
    LOCK,
    Path("/run.json"),
    Path("/task.json"),
    Path("/generation-result.json"),
    Path("/generation-evidence/invocation.json"),
    Path("/generation-evidence/metrics.json"),
    Path("/generation-evidence/codex-last.txt"),
    Path("/generation-evidence/codex-output.log"),
    Path("/generation-evidence/prompt.txt"),
]
if Path("/generation-evidence/usage.json").exists():
    required_files.append(Path("/generation-evidence/usage.json"))
required_directories = [
    Path("/candidate"),
    Path("/generation-evidence"),
    Path("/generation-evidence/codex-trace"),
    Path("/reference/reference-semantics"),
]
for path in required_files:
    print(f"required_file={path} regular={regular(path)} readable={os.access(path, os.R_OK)}")
for path in required_directories:
    print(
        f"required_directory={path} real={real_directory(path)} "
        f"readable={os.access(path, os.R_OK | os.X_OK)}"
    )

hash_pairs = {
    "/reference/canonical.py": "canonical_sha256",
    "/reference/prompt.py": "trusted_prompt_sha256",
    "/reference/py2mpy.py": "trusted_translator_sha256",
    "/candidate/prompt.py": "candidate_prompt_sha256",
    "/candidate/py2mpy.py": "candidate_translator_sha256",
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
for path_string, key in hash_pairs.items():
    path = Path(path_string)
    actual = sha256(path)
    expected = audit["hashes"][key]
    print(f"hash={path} match={actual == expected} actual={actual} expected={expected}")

print(
    "prompt_pair_byte_equal="
    f"{Path('/candidate/prompt.py').read_bytes() == Path('/reference/prompt.py').read_bytes()}"
)
print(
    "translator_pair_byte_equal="
    f"{Path('/candidate/py2mpy.py').read_bytes() == Path('/reference/py2mpy.py').read_bytes()}"
)
candidate_semantics = tree_entries(Path("/candidate/reference-semantics"))
trusted_semantics = tree_entries(Path("/reference/reference-semantics"))
print(f"semantics_tree_entry_count={len(candidate_semantics)}")
print(f"semantics_tree_exact_equal={candidate_semantics == trusted_semantics}")
print(
    "semantics_unsupported_entries="
    f"{[name for name, value in candidate_semantics.items() if value[0] == 'unsupported']}"
)
generation_result = json.loads(Path("/generation-result.json").read_text())
candidate_pipeline_hash = pipeline_tree_sha256(Path("/candidate"))
print(
    "candidate_pipeline_tree_sha256="
    f"{candidate_pipeline_hash} "
    f"expected={generation_result['outputs']['workspace_sha256']} "
    f"match={candidate_pipeline_hash == generation_result['outputs']['workspace_sha256']}"
)
print(
    "trusted_semantics_pipeline_tree_sha256="
    f"{pipeline_tree_sha256(Path('/reference/reference-semantics'))} "
    f"expected={audit['hashes']['trusted_reference_semantics_manifest_sha256']}"
)

trace_entries = tree_entries(Path("/generation-evidence/codex-trace"))
print(f"trace_tree_entries={len(trace_entries)}")
print(
    "trace_unsupported_entries="
    f"{[name for name, value in trace_entries.items() if value[0] == 'unsupported']}"
)
usage = json.loads(Path("/generation-evidence/usage.json").read_text())
trace_pipeline_hash = pipeline_tree_sha256(Path("/generation-evidence/codex-trace"))
print(
    f"trace_pipeline_tree_sha256={trace_pipeline_hash} "
    f"expected={usage['source_trace_sha256']} "
    f"match={trace_pipeline_hash == usage['source_trace_sha256']}"
)
