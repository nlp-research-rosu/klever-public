#!/usr/bin/env python3
"""Independent mounted-input/provenance checks for the 47-median audit."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")
LOCK = Path("/audit-campaign-lock.json")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def pipeline_sha256_tree(root: Path) -> str:
    """Pipeline-contract tree hash, independently recomputed from the mount."""
    digest = hashlib.sha256()
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
                raise RuntimeError(f"unsupported tree entry: {path}")
    for relative, entry_kind, path in sorted(entries):
        encoded = relative.encode()
        digest.update(len(encoded).to_bytes(4, "big"))
        digest.update(encoded)
        digest.update(entry_kind.encode() + b"\0")
        if entry_kind == "file":
            digest.update(path.stat(follow_symlinks=False).st_size.to_bytes(8, "big"))
            with path.open("rb") as stream:
                for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                    digest.update(chunk)
    return digest.hexdigest()


def kind(path: Path) -> str:
    mode = path.lstat().st_mode
    if stat.S_ISREG(mode):
        return "regular"
    if stat.S_ISDIR(mode):
        return "directory"
    if stat.S_ISLNK(mode):
        return "symlink"
    return f"other:{oct(mode)}"


def lexists(path: Path) -> bool:
    return os.path.lexists(path)


audit_input = json.loads(AUDIT_INPUT.read_text())
lock = json.loads(LOCK.read_text())
result = json.loads(Path("/generation-result.json").read_text())
usage = json.loads(Path("/generation-evidence/usage.json").read_text())

print(f"record_layout={audit_input['record_layout']}")
print(f"semantics_mode={audit_input['semantics_mode']}")
print(f"campaign_block_equal={audit_input['audit_campaign'] == lock}")
actual_lock_hash = sha256(LOCK)
print(f"audit_campaign_lock expected={audit_input['hashes']['audit_campaign_lock_sha256']}")
print(f"audit_campaign_lock actual={actual_lock_hash}")

required = [
    Path("/audit-input.json"),
    Path("/audit-campaign-lock.json"),
    Path("/run.json"),
    Path("/task.json"),
    Path("/generation-result.json"),
    Path("/generation-evidence/invocation.json"),
    Path("/generation-evidence/metrics.json"),
    Path("/generation-evidence/codex-last.txt"),
    Path("/generation-evidence/codex-output.log"),
    Path("/generation-evidence/prompt.txt"),
    Path("/generation-evidence/codex-trace"),
    Path("/candidate"),
    Path("/reference/canonical.py"),
    Path("/reference/prompt.py"),
    Path("/reference/py2mpy.py"),
]
for path in required:
    print(
        f"required {path}: exists={path.exists()} readable={os.access(path, os.R_OK)} "
        f"kind={kind(path) if lexists(path) else 'missing'}"
    )

hash_map = {
    Path("/audit-campaign-lock.json"): "audit_campaign_lock_sha256",
    Path("/run.json"): "run_manifest_sha256",
    Path("/task.json"): "task_manifest_sha256",
    Path("/generation-result.json"): "stage1_result_sha256",
    Path("/reference/canonical.py"): "canonical_sha256",
    Path("/reference/prompt.py"): "trusted_prompt_sha256",
    Path("/reference/py2mpy.py"): "trusted_translator_sha256",
    Path("/candidate/prompt.py"): "candidate_prompt_sha256",
    Path("/candidate/py2mpy.py"): "candidate_translator_sha256",
    Path("/generation-evidence/invocation.json"): "stage1_invocation_sha256",
    Path("/generation-evidence/metrics.json"): "generation_metrics_sha256",
    Path("/generation-evidence/usage.json"): "generation_usage_sha256",
    Path("/generation-evidence/codex-last.txt"): "generation_codex_last_sha256",
    Path("/generation-evidence/codex-output.log"): "generation_codex_output_sha256",
    Path("/generation-evidence/prompt.txt"): "generation_prompt_sha256",
}
for path, key in hash_map.items():
    expected = audit_input["hashes"].get(key)
    actual = sha256(path) if path.is_file() else None
    print(f"hash {path}: expected={expected} actual={actual} match={expected == actual}")

print(
    "candidate_prompt_byte_equal="
    f"{Path('/candidate/prompt.py').read_bytes() == Path('/reference/prompt.py').read_bytes()}"
)
print(
    "candidate_translator_byte_equal="
    f"{Path('/candidate/py2mpy.py').read_bytes() == Path('/reference/py2mpy.py').read_bytes()}"
)
print(f"trusted_reference_semantics_absent={not lexists(Path('/reference/reference-semantics'))}")
candidate_tree_hash = pipeline_sha256_tree(Path("/candidate"))
trace_tree_hash = pipeline_sha256_tree(Path("/generation-evidence/codex-trace"))
print(
    "candidate_tree_pipeline_hash "
    f"expected={result['outputs']['workspace_sha256']} "
    f"actual={candidate_tree_hash} "
    f"match={candidate_tree_hash == result['outputs']['workspace_sha256']}"
)
print(
    "generation_trace_pipeline_hash "
    f"expected={usage['source_trace_sha256']} "
    f"actual={trace_tree_hash} "
    f"match={trace_tree_hash == usage['source_trace_sha256']}"
)
print(
    "audit_snapshot_tree_digests_recorded="
    f"candidate:{audit_input['hashes']['candidate_tree_sha256']},"
    f"trace:{audit_input['hashes']['generation_codex_trace_sha256']}"
)

invocation = json.loads(Path("/generation-evidence/invocation.json").read_text())
expected_evidence = invocation["outputs"]["evidence"]
print(f"invocation_result_evidence_maps_equal={expected_evidence == result['outputs']['evidence']}")
for relative, expected in sorted(expected_evidence.items()):
    path = Path("/generation-evidence") / relative
    actual = sha256(path) if path.is_file() else None
    print(
        f"generation_record {relative}: exists={path.exists()} "
        f"kind={kind(path) if lexists(path) else 'missing'} expected={expected} "
        f"actual={actual} match={expected == actual}"
    )

for root in (Path("/candidate"), Path("/generation-evidence"), Path("/reference")):
    print(f"tree_manifest root={root}")
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root)
        entry_kind = kind(path)
        if entry_kind == "regular":
            print(f"  {entry_kind} {relative} sha256={sha256(path)} size={path.stat().st_size}")
        elif entry_kind == "symlink":
            print(f"  {entry_kind} {relative} -> {os.readlink(path)}")
        else:
            print(f"  {entry_kind} {relative}")
