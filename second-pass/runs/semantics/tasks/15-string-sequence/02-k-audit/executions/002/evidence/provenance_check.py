#!/usr/bin/env python3
"""Independent integrity checks for the mounted audit inputs."""

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


def tree_entries(root: Path) -> list[tuple[str, str, str | None]]:
    entries: list[tuple[str, str, str | None]] = []
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root).as_posix()
        if path.is_symlink():
            entries.append((relative, "symlink", os.readlink(path)))
        elif path.is_dir():
            entries.append((relative, "directory", None))
        elif path.is_file():
            entries.append((relative, "file", sha256(path)))
        else:
            entries.append((relative, "other", None))
    return entries


def strict_tree_sha256(root: Path) -> str:
    """Reproduce the pipeline's length-delimited path/type/content tree digest."""
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
                raise AssertionError(f"unsupported tree entry: {path}")
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
                for block in iter(lambda: stream.read(1024 * 1024), b""):
                    digest.update(block)
    return digest.hexdigest()


audit = json.loads(AUDIT_INPUT.read_text())
lock = json.loads(LOCK.read_text())
assert audit["record_layout"] == "legacy-selected-stage1"
assert audit["semantics_mode"] == "SUPPLIED_SEMANTICS"
assert audit["audit_campaign"] == lock
assert sha256(LOCK) == audit["hashes"]["audit_campaign_lock_sha256"]

paths = audit["container_paths"]
required = [
    Path(paths["candidate"]),
    Path(paths["canonical"]),
    Path(paths["translator"]),
    Path(paths["trusted_prompt"]),
    Path(paths["audit_campaign_lock"]),
    Path(paths["run_manifest"]),
    Path(paths["task_manifest"]),
    Path(paths["stage1_result"]),
    Path(paths["generation_manifest"]),
    Path(paths["generation_metrics"]),
    Path(paths["generation_last"]),
    Path(paths["generation_output"]),
    Path(paths["generation_root"]) / "prompt.txt",
    Path(paths["generation_trace"]),
    Path("/audit-prompt.md"),
]
missing = [str(path) for path in required if not path.exists()]
assert not missing, missing
assert sha256(Path("/audit-prompt.md")) == lock["audit_prompt_sha256"]

file_hash_expectations = {
    LOCK: "audit_campaign_lock_sha256",
    Path("/candidate/prompt.py"): "candidate_prompt_sha256",
    Path("/candidate/py2mpy.py"): "candidate_translator_sha256",
    Path("/reference/canonical.py"): "canonical_sha256",
    Path("/reference/prompt.py"): "trusted_prompt_sha256",
    Path("/reference/py2mpy.py"): "trusted_translator_sha256",
    Path("/run.json"): "run_manifest_sha256",
    Path("/task.json"): "task_manifest_sha256",
    Path("/generation-result.json"): "stage1_result_sha256",
    Path("/generation-evidence/invocation.json"): "stage1_invocation_sha256",
    Path("/generation-evidence/metrics.json"): "generation_metrics_sha256",
    Path("/generation-evidence/usage.json"): "generation_usage_sha256",
    Path("/generation-evidence/codex-last.txt"): "generation_codex_last_sha256",
    Path("/generation-evidence/codex-output.log"): "generation_codex_output_sha256",
    Path("/generation-evidence/prompt.txt"): "generation_prompt_sha256",
}
for path, key in file_hash_expectations.items():
    actual = sha256(path)
    expected = audit["hashes"][key]
    assert actual == expected, (path, actual, expected)

trace_files = sorted(Path(paths["generation_trace"]).rglob("*"))
trace_files = [path for path in trace_files if path.is_file()]
assert len(trace_files) == 1
assert sha256(trace_files[0]) == (
    "f8af2f79072a8d57747d971f57d6b10a8e6e655d34dbaef64632c8ca93752edb"
)

generation_result = json.loads(Path("/generation-result.json").read_text())
invocation = json.loads(Path("/generation-evidence/invocation.json").read_text())
candidate_manifest_hash = strict_tree_sha256(Path("/candidate"))
assert candidate_manifest_hash == generation_result["outputs"]["workspace_sha256"]
assert candidate_manifest_hash == invocation["retained_workspace_sha256"]
semantics_manifest_hash = strict_tree_sha256(Path("/reference/reference-semantics"))
assert semantics_manifest_hash == audit["hashes"]["trusted_reference_semantics_manifest_sha256"]
assert semantics_manifest_hash == strict_tree_sha256(Path("/candidate/reference-semantics"))
trace_manifest_hash = strict_tree_sha256(Path(paths["generation_trace"]))
usage = json.loads(Path("/generation-evidence/usage.json").read_text())
assert trace_manifest_hash == usage["source_trace_sha256"]

assert Path("/candidate/prompt.py").read_bytes() == Path("/reference/prompt.py").read_bytes()
assert Path("/candidate/py2mpy.py").read_bytes() == Path("/reference/py2mpy.py").read_bytes()

candidate_semantics = tree_entries(Path("/candidate/reference-semantics"))
trusted_semantics = tree_entries(Path("/reference/reference-semantics"))
assert candidate_semantics == trusted_semantics
assert not [entry for entry in candidate_semantics if entry[1] == "symlink"]

trace_lines = 0
with trace_files[0].open() as stream:
    for trace_lines, line in enumerate(stream, 1):
        json.loads(line)
assert trace_lines == 724

print("record_layout=legacy-selected-stage1")
print("semantics_mode=SUPPLIED_SEMANTICS")
print("campaign_lock_match=yes")
print("audit_prompt_hash_match=yes")
print(f"required_mounts_and_records={len(required)} present")
print(f"recorded_file_hashes={len(file_hash_expectations)} match")
print(f"candidate_manifest_sha256={candidate_manifest_hash} matches_generation_records")
print(f"semantics_manifest_sha256={semantics_manifest_hash} matches_audit_input")
print(f"trace_manifest_sha256={trace_manifest_hash} matches_usage_record")
print(f"trace_files={len(trace_files)} trace_json_lines={trace_lines} all_valid")
print("candidate_prompt_matches_trusted=yes")
print("candidate_translator_matches_trusted=yes")
print(f"semantics_entries={len(candidate_semantics)} exact_type_and_byte_match")
print("semantics_symlinks=0")
print("runtime_metrics=absent_and_not_required_for_legacy_selected_stage1")
