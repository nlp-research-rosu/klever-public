#!/usr/bin/env python3
"""Independent integrity checks for the launcher-owned audit inputs."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from collections import Counter
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")
CAMPAIGN_LOCK = Path("/audit-campaign-lock.json")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def require_regular(path: Path) -> None:
    assert path.exists(), f"missing required file: {path}"
    assert not path.is_symlink(), f"symlinked required file: {path}"
    assert path.is_file(), f"mistyped required file: {path}"
    with path.open("rb"):
        pass


def sha256_tree(root: Path) -> str:
    """Reimplement the launcher tree digest from mounted bytes and entry types."""
    root_stat = root.lstat()
    assert stat.S_ISDIR(root_stat.st_mode), f"not a real directory: {root}"
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


audit = json.loads(AUDIT_INPUT.read_text(encoding="utf-8"))
lock = json.loads(CAMPAIGN_LOCK.read_text(encoding="utf-8"))
assert audit["record_layout"] == "pipeline-v3"
assert audit["semantics_mode"] == "SUPPLIED_SEMANTICS"
assert audit["audit_campaign"] == lock
assert sha256(CAMPAIGN_LOCK) == audit["hashes"]["audit_campaign_lock_sha256"]

paths = audit["container_paths"]
required = {
    "audit_campaign_lock": Path(paths["audit_campaign_lock"]),
    "candidate": Path(paths["candidate"]),
    "canonical": Path(paths["canonical"]),
    "generation_last": Path(paths["generation_last"]),
    "generation_manifest": Path(paths["generation_manifest"]),
    "generation_metrics": Path(paths["generation_metrics"]),
    "generation_output": Path(paths["generation_output"]),
    "run_manifest": Path(paths["run_manifest"]),
    "stage1_result": Path(paths["stage1_result"]),
    "task_manifest": Path(paths["task_manifest"]),
    "translator": Path(paths["translator"]),
    "trusted_prompt": Path(paths["trusted_prompt"]),
    "generation_runtime_metrics": Path("/generation-evidence/runtime-metrics.json"),
    "generation_usage": Path("/generation-evidence/usage.json"),
    "generation_prompt": Path("/generation-evidence/prompt.txt"),
}
for key, path in required.items():
    if key == "candidate":
        assert path.is_dir() and not path.is_symlink(), f"invalid mount: {path}"
    else:
        require_regular(path)

trace_root = Path(paths["generation_trace"])
assert trace_root.is_dir() and not trace_root.is_symlink()
trace_files = sorted(trace_root.rglob("*"))
assert trace_files, "structured trace is empty"
assert not any(path.is_symlink() for path in trace_files)
trace_jsonl = [path for path in trace_files if path.is_file()]
assert len(trace_jsonl) == 1
trace_path = trace_jsonl[0]

hash_checks = {
    "canonical_sha256": Path(paths["canonical"]),
    "trusted_prompt_sha256": Path(paths["trusted_prompt"]),
    "trusted_translator_sha256": Path(paths["translator"]),
    "run_manifest_sha256": Path(paths["run_manifest"]),
    "task_manifest_sha256": Path(paths["task_manifest"]),
    "stage1_result_sha256": Path(paths["stage1_result"]),
    "stage1_invocation_sha256": Path(paths["generation_manifest"]),
    "generation_metrics_sha256": Path(paths["generation_metrics"]),
    "generation_runtime_metrics_sha256": required["generation_runtime_metrics"],
    "generation_usage_sha256": required["generation_usage"],
    "generation_codex_last_sha256": Path(paths["generation_last"]),
    "generation_codex_output_sha256": Path(paths["generation_output"]),
    "generation_prompt_sha256": required["generation_prompt"],
}
for hash_key, path in hash_checks.items():
    actual = sha256(path)
    expected = audit["hashes"][hash_key]
    assert actual == expected, f"{hash_key}: {actual} != {expected}"

result = json.loads(Path(paths["stage1_result"]).read_text(encoding="utf-8"))
usage = json.loads(required["generation_usage"].read_text(encoding="utf-8"))
trace_rel = str(trace_path.relative_to(Path(paths["generation_root"])))
trace_expected = result["outputs"]["evidence"][trace_rel]
assert sha256(trace_path) == trace_expected
assert sha256_tree(trace_root) == usage["source_trace_sha256"]

candidate = Path(paths["candidate"])
candidate_pipeline_tree_hash = sha256_tree(candidate)
assert candidate_pipeline_tree_hash == result["outputs"]["workspace_sha256"]
proof_artifacts = (
    "solution.py",
    "solution.mpy",
    "verification.k",
    "spec.k",
    "prove.sh",
    "PROOF.md",
)
for relative in proof_artifacts:
    require_regular(candidate / relative)

reference_semantics = Path("/reference/reference-semantics")
candidate_semantics = candidate / "reference-semantics"
assert reference_semantics.is_dir() and not reference_semantics.is_symlink()
assert candidate_semantics.is_dir() and not candidate_semantics.is_symlink()
trusted_semantics_tree_hash = sha256_tree(reference_semantics)
candidate_semantics_tree_hash = sha256_tree(candidate_semantics)
assert (
    trusted_semantics_tree_hash
    == audit["hashes"]["trusted_reference_semantics_manifest_sha256"]
)
assert candidate_semantics_tree_hash == trusted_semantics_tree_hash


def tree_entries(root: Path) -> dict[str, tuple[str, str | None]]:
    entries: dict[str, tuple[str, str | None]] = {}
    for path in sorted(root.rglob("*")):
        relative = str(path.relative_to(root))
        if path.is_symlink():
            entries[relative] = ("symlink", os.readlink(path))
        elif path.is_dir():
            entries[relative] = ("directory", None)
        elif path.is_file():
            entries[relative] = ("file", sha256(path))
        else:
            entries[relative] = ("other", None)
    return entries


trusted_entries = tree_entries(reference_semantics)
candidate_entries = tree_entries(candidate_semantics)
assert candidate_entries == trusted_entries
assert (candidate / "prompt.py").read_bytes() == Path(paths["trusted_prompt"]).read_bytes()
assert (candidate / "py2mpy.py").read_bytes() == Path(paths["translator"]).read_bytes()

event_counts: Counter[tuple[str, str]] = Counter()
line_count = 0
with trace_path.open(encoding="utf-8") as stream:
    for line_count, line in enumerate(stream, start=1):
        event = json.loads(line)
        event_counts[(event.get("type", ""), event.get("payload", {}).get("type", ""))] += 1

print("record_layout=pipeline-v3")
print("semantics_mode=SUPPLIED_SEMANTICS")
print("campaign_lock_json_match=true")
print("campaign_lock_hash_match=true")
print(f"required_launcher_records={len(required) + 1}")
print("required_launcher_records_present_regular=true")
print("candidate_required_proof_artifacts_present_regular=true")
print(f"candidate_pipeline_tree_sha256={candidate_pipeline_tree_hash}")
print("candidate_pipeline_tree_hash_matches_generation_result=true")
print("candidate_prompt_matches_trusted=true")
print("candidate_translator_matches_trusted=true")
print(f"supplied_semantics_entries={len(trusted_entries)}")
print(f"supplied_semantics_tree_sha256={trusted_semantics_tree_hash}")
print("supplied_semantics_recursive_identity=true")
print("symlink_count_candidate_reference_generation=0")
print(f"trace_path={trace_path}")
print(f"trace_lines={line_count}")
print(f"trace_sha256={sha256(trace_path)}")
print(f"trace_tree_sha256={sha256_tree(trace_root)}")
print("trace_tree_hash_matches_usage_record=true")
print("trace_json_parse=true")
print("trace_event_counts:")
for (top_type, payload_type), count in sorted(event_counts.items()):
    print(f"  {top_type}/{payload_type or '-'}={count}")
print("all_declared_single_file_hashes_match=true")
