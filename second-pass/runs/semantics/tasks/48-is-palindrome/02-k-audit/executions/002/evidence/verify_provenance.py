#!/usr/bin/env python3
"""Independent integrity checks for launcher mounts and legacy-selected records."""

from __future__ import annotations

import hashlib
import json
import os
import pathlib
import stat
import sys


def digest(path: pathlib.Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def load_json(path: pathlib.Path) -> object:
    with path.open(encoding="utf-8") as stream:
        return json.load(stream)


def tree_manifest(root: pathlib.Path) -> list[dict[str, object]]:
    entries: list[dict[str, object]] = []
    for path in sorted(root.rglob("*")):
        rel = path.relative_to(root).as_posix()
        mode = path.lstat().st_mode
        if stat.S_ISLNK(mode):
            kind = "symlink"
            payload: object = os.readlink(path)
        elif stat.S_ISDIR(mode):
            kind = "directory"
            payload = None
        elif stat.S_ISREG(mode):
            kind = "file"
            payload = {"size": path.stat().st_size, "sha256": digest(path)}
        else:
            kind = "other"
            payload = stat.S_IFMT(mode)
        entries.append({"path": rel, "kind": kind, "payload": payload})
    return entries


def reviewer_tree_digest(entries: list[dict[str, object]]) -> str:
    encoded = json.dumps(entries, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def pipeline_tree_digest(root: pathlib.Path) -> str:
    """Independently reproduce the provenance manifest tree hash."""
    entries: list[tuple[str, str, pathlib.Path]] = []
    for path in root.rglob("*"):
        rel = path.relative_to(root).as_posix()
        mode = path.lstat().st_mode
        if stat.S_ISDIR(mode):
            entries.append((rel, "directory", path))
        elif stat.S_ISREG(mode):
            entries.append((rel, "file", path))
        else:
            raise ValueError(f"unsupported tree entry: {path}")
    hasher = hashlib.sha256()
    for rel, kind, path in sorted(entries):
        encoded = rel.encode()
        hasher.update(len(encoded).to_bytes(4, "big"))
        hasher.update(encoded)
        hasher.update(kind.encode() + b"\0")
        if kind == "file":
            hasher.update(path.stat().st_size.to_bytes(8, "big"))
            hasher.update(path.read_bytes())
    return hasher.hexdigest()


audit_path = pathlib.Path("/audit-input.json")
lock_path = pathlib.Path("/audit-campaign-lock.json")
audit = load_json(audit_path)
lock = load_json(lock_path)
assert isinstance(audit, dict)
assert isinstance(lock, dict)
hashes = audit["hashes"]
container_paths = audit["container_paths"]

failures: list[str] = []


def check_equal(label: str, actual: object, expected: object) -> None:
    status = actual == expected
    print(f"{label}: {'OK' if status else 'MISMATCH'}")
    if not status:
        print(f"  actual={actual!r}")
        print(f"  expected={expected!r}")
        failures.append(label)


check_equal("record_layout", audit["record_layout"], "legacy-selected-stage1")
check_equal("semantics_mode", audit["semantics_mode"], "SUPPLIED_SEMANTICS")
check_equal("campaign_block_equals_lock", audit["audit_campaign"], lock)
check_equal(
    "audit_campaign_lock_sha256",
    digest(lock_path),
    hashes["audit_campaign_lock_sha256"],
)

required_files = [
    pathlib.Path("/run.json"),
    pathlib.Path("/task.json"),
    pathlib.Path("/generation-result.json"),
    pathlib.Path("/generation-evidence/invocation.json"),
    pathlib.Path("/generation-evidence/metrics.json"),
    pathlib.Path("/generation-evidence/usage.json"),
    pathlib.Path("/generation-evidence/codex-last.txt"),
    pathlib.Path("/generation-evidence/codex-output.log"),
    pathlib.Path("/generation-evidence/prompt.txt"),
    pathlib.Path("/reference/canonical.py"),
    pathlib.Path("/reference/prompt.py"),
    pathlib.Path("/reference/py2mpy.py"),
]
required_dirs = [
    pathlib.Path("/candidate"),
    pathlib.Path("/reference/reference-semantics"),
    pathlib.Path("/generation-evidence/codex-trace"),
]
for path in required_files:
    check_equal(f"regular_readable:{path}", path.is_file() and os.access(path, os.R_OK), True)
    check_equal(f"not_symlink:{path}", path.is_symlink(), False)
for path in required_dirs:
    check_equal(f"directory_readable:{path}", path.is_dir() and os.access(path, os.R_OK), True)
    check_equal(f"not_symlink:{path}", path.is_symlink(), False)

file_checks = {
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
for raw_path, key in file_checks.items():
    check_equal(f"sha256:{raw_path}", digest(pathlib.Path(raw_path)), hashes[key])

for key, raw_path in container_paths.items():
    path = pathlib.Path(raw_path)
    check_equal(f"declared_mount_exists:{key}", path.exists(), True)

trusted_semantics = tree_manifest(pathlib.Path("/reference/reference-semantics"))
candidate_semantics = tree_manifest(pathlib.Path("/candidate/reference-semantics"))
check_equal("candidate_semantics_exact_manifest", candidate_semantics, trusted_semantics)
check_equal(
    "candidate_semantics_contains_no_symlink",
    any(entry["kind"] == "symlink" for entry in candidate_semantics),
    False,
)
print(
    "reviewer_semantics_tree_sha256="
    + reviewer_tree_digest(trusted_semantics)
)

candidate_tree = tree_manifest(pathlib.Path("/candidate"))
check_equal(
    "candidate_tree_contains_no_symlink",
    any(entry["kind"] == "symlink" for entry in candidate_tree),
    False,
)
print("reviewer_candidate_tree_sha256=" + reviewer_tree_digest(candidate_tree))

trace_entries = tree_manifest(pathlib.Path("/generation-evidence/codex-trace"))
check_equal(
    "trace_tree_contains_no_symlink",
    any(entry["kind"] == "symlink" for entry in trace_entries),
    False,
)
print("reviewer_trace_tree_sha256=" + reviewer_tree_digest(trace_entries))

generation_result = load_json(pathlib.Path("/generation-result.json"))
assert isinstance(generation_result, dict)
for rel_path, expected in generation_result["outputs"]["evidence"].items():
    mounted = pathlib.Path("/generation-evidence") / rel_path
    check_equal(f"generation_result_sha256:{rel_path}", digest(mounted), expected)

invocation = load_json(pathlib.Path("/generation-evidence/invocation.json"))
usage = load_json(pathlib.Path("/generation-evidence/usage.json"))
assert isinstance(invocation, dict)
assert isinstance(usage, dict)
candidate_pipeline_hash = pipeline_tree_digest(pathlib.Path("/candidate"))
check_equal(
    "candidate_pipeline_tree_matches_generation_result",
    candidate_pipeline_hash,
    generation_result["outputs"]["workspace_sha256"],
)
check_equal(
    "candidate_pipeline_tree_matches_invocation",
    candidate_pipeline_hash,
    invocation["retained_workspace_sha256"],
)
semantics_pipeline_hash = pipeline_tree_digest(
    pathlib.Path("/reference/reference-semantics")
)
check_equal(
    "trusted_semantics_pipeline_manifest_sha256",
    semantics_pipeline_hash,
    hashes["trusted_reference_semantics_manifest_sha256"],
)
check_equal(
    "candidate_semantics_pipeline_manifest_sha256",
    pipeline_tree_digest(pathlib.Path("/candidate/reference-semantics")),
    hashes["trusted_reference_semantics_manifest_sha256"],
)
check_equal(
    "trace_pipeline_tree_matches_usage",
    pipeline_tree_digest(pathlib.Path("/generation-evidence/codex-trace")),
    usage["source_trace_sha256"],
)

check_equal(
    "candidate_prompt_bytes_equal_trusted",
    pathlib.Path("/candidate/prompt.py").read_bytes(),
    pathlib.Path("/reference/prompt.py").read_bytes(),
)
check_equal(
    "candidate_translator_bytes_equal_trusted",
    pathlib.Path("/candidate/py2mpy.py").read_bytes(),
    pathlib.Path("/reference/py2mpy.py").read_bytes(),
)

print(f"FAILURE_COUNT={len(failures)}")
if failures:
    sys.exit(1)
