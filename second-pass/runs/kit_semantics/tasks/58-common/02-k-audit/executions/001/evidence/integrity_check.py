#!/usr/bin/env python3
"""Independent mounted-input integrity checks for the 58-common audit."""

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
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def entry_inventory(root: Path) -> dict[str, tuple[str, str | None]]:
    inventory: dict[str, tuple[str, str | None]] = {}
    for current, dirs, files in os.walk(root, topdown=True, followlinks=False):
        current_path = Path(current)
        names = sorted(dirs + files)
        for name in names:
            path = current_path / name
            relative = path.relative_to(root).as_posix()
            mode = path.lstat().st_mode
            if stat.S_ISLNK(mode):
                inventory[relative] = ("symlink", os.readlink(path))
            elif stat.S_ISDIR(mode):
                inventory[relative] = ("directory", None)
            elif stat.S_ISREG(mode):
                inventory[relative] = ("file", sha256(path))
            else:
                inventory[relative] = ("other", None)
    return inventory


def manifest_digest(inventory: dict[str, tuple[str, str | None]]) -> str:
    payload = "".join(
        f"{kind}\t{relative}\t{value or ''}\n"
        for relative, (kind, value) in sorted(inventory.items())
    )
    return hashlib.sha256(payload.encode()).hexdigest()


def pipeline_tree_digest(root: Path) -> str:
    """Independent reimplementation of the pipeline-v3 length-delimited digest."""
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
                raise RuntimeError(f"linked or unsupported tree entry: {path}")
    for relative, kind, path in sorted(entries):
        encoded = relative.encode()
        digest.update(len(encoded).to_bytes(4, "big"))
        digest.update(encoded)
        digest.update(kind.encode() + b"\0")
        if kind == "file":
            size = path.stat(follow_symlinks=False).st_size
            digest.update(size.to_bytes(8, "big"))
            with path.open("rb") as stream:
                for block in iter(lambda: stream.read(1024 * 1024), b""):
                    digest.update(block)
    return digest.hexdigest()


def require_regular(path: Path) -> bool:
    ok = path.exists() and not path.is_symlink() and path.is_file()
    print(f"REQUIRED_REGULAR {path}: {ok}")
    if ok:
        print(f"SHA256 {path}: {sha256(path)}")
    return ok


with AUDIT_INPUT.open(encoding="utf-8") as stream:
    audit_input = json.load(stream)
with LOCK.open(encoding="utf-8") as stream:
    lock = json.load(stream)

print(f"record_layout={audit_input.get('record_layout')}")
print(f"semantics_mode={audit_input.get('semantics_mode')}")
print(f"campaign_block_equals_lock={audit_input.get('audit_campaign') == lock}")
actual_lock_hash = sha256(LOCK)
recorded_lock_hash = audit_input["hashes"]["audit_campaign_lock_sha256"]
print(f"campaign_lock_sha256_actual={actual_lock_hash}")
print(f"campaign_lock_sha256_recorded={recorded_lock_hash}")
print(f"campaign_lock_hash_matches={actual_lock_hash == recorded_lock_hash}")

required = [
    AUDIT_INPUT,
    LOCK,
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
    Path("/reference/prompt.py"),
    Path("/reference/canonical.py"),
    Path("/reference/py2mpy.py"),
    Path("/candidate/prompt.py"),
    Path("/candidate/py2mpy.py"),
    Path("/candidate/solution.py"),
    Path("/candidate/solution.mpy"),
    Path("/candidate/verification.k"),
    Path("/candidate/spec.k"),
    Path("/candidate/prove.sh"),
]
required_ok = all(require_regular(path) for path in required)
print(f"all_required_regular={required_ok}")

declared_hash_checks = [
    ("/run.json", "run_manifest_sha256"),
    ("/task.json", "task_manifest_sha256"),
    ("/generation-result.json", "stage1_result_sha256"),
    ("/generation-evidence/invocation.json", "stage1_invocation_sha256"),
    ("/generation-evidence/metrics.json", "generation_metrics_sha256"),
    ("/generation-evidence/runtime-metrics.json", "generation_runtime_metrics_sha256"),
    ("/generation-evidence/usage.json", "generation_usage_sha256"),
    ("/generation-evidence/codex-last.txt", "generation_codex_last_sha256"),
    ("/generation-evidence/codex-output.log", "generation_codex_output_sha256"),
    ("/generation-evidence/prompt.txt", "generation_prompt_sha256"),
    ("/reference/prompt.py", "trusted_prompt_sha256"),
    ("/reference/canonical.py", "canonical_sha256"),
    ("/reference/py2mpy.py", "trusted_translator_sha256"),
    ("/candidate/prompt.py", "candidate_prompt_sha256"),
    ("/candidate/py2mpy.py", "candidate_translator_sha256"),
]
for name, key in declared_hash_checks:
    actual = sha256(Path(name))
    expected = audit_input["hashes"][key]
    print(f"DECLARED_HASH {name} key={key} match={actual == expected}")

trace_files = sorted(Path("/generation-evidence/codex-trace").rglob("*"))
trace_regular = [
    path for path in trace_files
    if path.is_file() and not path.is_symlink()
]
trace_bad = [
    path for path in trace_files
    if path.is_symlink() or (not path.is_file() and not path.is_dir())
]
print(f"trace_regular_file_count={len(trace_regular)}")
print(f"trace_bad_entry_count={len(trace_bad)}")
with Path("/generation-result.json").open(encoding="utf-8") as stream:
    generation_result = json.load(stream)
recorded_trace = {
    key: value
    for key, value in generation_result["outputs"]["evidence"].items()
    if key.startswith("codex-trace/")
}
actual_trace = {
    path.relative_to("/generation-evidence").as_posix(): sha256(path)
    for path in trace_regular
}
print(f"trace_paths_match_result={set(recorded_trace) == set(actual_trace)}")
for relative in sorted(set(recorded_trace) | set(actual_trace)):
    print(
        f"TRACE_HASH {relative} "
        f"match={recorded_trace.get(relative) == actual_trace.get(relative)}"
    )

candidate_pipeline_digest = pipeline_tree_digest(Path("/candidate"))
result_workspace_digest = generation_result["outputs"]["workspace_sha256"]
print(f"candidate_pipeline_tree_sha256={candidate_pipeline_digest}")
print(
    "candidate_tree_matches_generation_result="
    f"{candidate_pipeline_digest == result_workspace_digest}"
)

candidate_prompt_match = (
    Path("/candidate/prompt.py").read_bytes()
    == Path("/reference/prompt.py").read_bytes()
)
candidate_translator_match = (
    Path("/candidate/py2mpy.py").read_bytes()
    == Path("/reference/py2mpy.py").read_bytes()
)
print(f"candidate_prompt_byte_match={candidate_prompt_match}")
print(f"candidate_translator_byte_match={candidate_translator_match}")

trusted_semantics = Path("/reference/reference-semantics")
candidate_semantics = Path("/candidate/reference-semantics")
print(f"trusted_semantics_present={trusted_semantics.is_dir()}")
print(f"candidate_semantics_present={candidate_semantics.is_dir()}")
trusted_inventory = entry_inventory(trusted_semantics)
candidate_inventory = entry_inventory(candidate_semantics)
print(f"trusted_semantics_manifest_sha256={manifest_digest(trusted_inventory)}")
print(f"candidate_semantics_manifest_sha256={manifest_digest(candidate_inventory)}")
print(
    "semantics_path_type_hash_match="
    f"{trusted_inventory == candidate_inventory}"
)
all_semantics_paths = sorted(set(trusted_inventory) | set(candidate_inventory))
for relative in all_semantics_paths:
    trusted_entry = trusted_inventory.get(relative)
    candidate_entry = candidate_inventory.get(relative)
    if trusted_entry != candidate_entry:
        print(
            f"SEMANTICS_MISMATCH {relative}: "
            f"trusted={trusted_entry} candidate={candidate_entry}"
        )
print(
    "trusted_semantics_symlink_count="
    f"{sum(kind == 'symlink' for kind, _ in trusted_inventory.values())}"
)
print(
    "candidate_semantics_symlink_count="
    f"{sum(kind == 'symlink' for kind, _ in candidate_inventory.values())}"
)
trusted_pipeline_digest = pipeline_tree_digest(trusted_semantics)
candidate_semantics_pipeline_digest = pipeline_tree_digest(candidate_semantics)
print(f"trusted_semantics_pipeline_tree_sha256={trusted_pipeline_digest}")
print(
    "trusted_semantics_pipeline_hash_matches_task="
    f"{trusted_pipeline_digest == audit_input['manifest']['inputs']['reference_semantics_sha256']}"
)
print(
    "candidate_semantics_pipeline_hash_matches_task="
    f"{candidate_semantics_pipeline_digest == audit_input['manifest']['inputs']['reference_semantics_sha256']}"
)

with Path("/generation-evidence/invocation.json").open(encoding="utf-8") as stream:
    invocation = json.load(stream)
for relative, expected in sorted(invocation["outputs"]["evidence"].items()):
    mounted = Path("/generation-evidence") / relative
    actual = sha256(mounted) if mounted.is_file() and not mounted.is_symlink() else None
    print(f"INVOCATION_EVIDENCE_HASH {relative} match={actual == expected}")
print(
    "candidate_tree_matches_invocation_output="
    f"{candidate_pipeline_digest == invocation['outputs']['workspace_sha256']}"
)
trace_pipeline_digest = pipeline_tree_digest(Path("/generation-evidence/codex-trace"))
with Path("/generation-evidence/usage.json").open(encoding="utf-8") as stream:
    usage = json.load(stream)
print(f"trace_pipeline_tree_sha256={trace_pipeline_digest}")
print(
    "trace_tree_matches_usage_source="
    f"{trace_pipeline_digest == usage['source_trace_sha256']}"
)

print("INTEGRITY_CHECK_COMPLETE")
