#!/usr/bin/env python3
"""Independent read-only provenance and supplied-semantics integrity check."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from pathlib import Path


AUDIT = Path("/audit-input.json")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def manifest(root: Path) -> tuple[list[dict[str, object]], str]:
    rows: list[dict[str, object]] = []
    for path in sorted(root.rglob("*"), key=lambda p: p.relative_to(root).as_posix()):
        rel = path.relative_to(root).as_posix()
        info = path.lstat()
        kind = (
            "symlink"
            if stat.S_ISLNK(info.st_mode)
            else "file"
            if stat.S_ISREG(info.st_mode)
            else "dir"
            if stat.S_ISDIR(info.st_mode)
            else "other"
        )
        row: dict[str, object] = {
            "path": rel,
            "kind": kind,
            "mode": stat.S_IMODE(info.st_mode),
        }
        if kind == "file":
            row["size"] = info.st_size
            row["sha256"] = sha256_file(path)
        elif kind == "symlink":
            row["target"] = os.readlink(path)
        rows.append(row)
    encoded = json.dumps(rows, sort_keys=True, separators=(",", ":")).encode()
    return rows, hashlib.sha256(encoded).hexdigest()


def pipeline_tree_hash(root: Path) -> str:
    """Independently reproduce the length-delimited mounted-tree digest."""
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
                for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                    digest.update(chunk)
    return digest.hexdigest()


data = json.loads(AUDIT.read_text())
record_layout = data["record_layout"]
print(f"record_layout={record_layout}")
print(f"semantics_mode={data['semantics_mode']}")

lock_path = Path(data["container_paths"]["audit_campaign_lock"])
lock = json.loads(lock_path.read_text())
print(f"campaign_structural_match={lock == data['audit_campaign']}")
actual_lock_hash = sha256_file(lock_path)
print(f"audit_campaign_lock_sha256={actual_lock_hash}")
print(
    "audit_campaign_lock_hash_match="
    f"{actual_lock_hash == data['hashes']['audit_campaign_lock_sha256']}"
)

required = {
    "audit_input": AUDIT,
    "campaign_lock": lock_path,
    "run_manifest": Path(data["container_paths"]["run_manifest"]),
    "task_manifest": Path(data["container_paths"]["task_manifest"]),
    "stage1_result": Path(data["container_paths"]["stage1_result"]),
    "invocation": Path(data["container_paths"]["generation_manifest"]),
    "metrics": Path(data["container_paths"]["generation_metrics"]),
    "usage": Path("/generation-evidence/usage.json"),
    "codex_last": Path(data["container_paths"]["generation_last"]),
    "codex_output": Path(data["container_paths"]["generation_output"]),
    "prompt": Path("/generation-evidence/prompt.txt"),
    "trace": Path(data["container_paths"]["generation_trace"]),
    "canonical": Path(data["container_paths"]["canonical"]),
    "trusted_prompt": Path(data["container_paths"]["trusted_prompt"]),
    "translator": Path(data["container_paths"]["translator"]),
    "candidate": Path(data["container_paths"]["candidate"]),
    "trusted_semantics": Path("/reference/reference-semantics"),
}
for name, path in required.items():
    info = path.lstat()
    print(
        f"required[{name}] exists=True readable={os.access(path, os.R_OK)} "
        f"symlink={stat.S_ISLNK(info.st_mode)} "
        f"type={'dir' if stat.S_ISDIR(info.st_mode) else 'file' if stat.S_ISREG(info.st_mode) else 'other'} "
        f"path={path}"
    )

recorded_file_hashes = {
    "/audit-campaign-lock.json": "audit_campaign_lock_sha256",
    "/run.json": "run_manifest_sha256",
    "/task.json": "task_manifest_sha256",
    "/generation-result.json": "stage1_result_sha256",
    "/reference/canonical.py": "canonical_sha256",
    "/reference/prompt.py": "trusted_prompt_sha256",
    "/reference/py2mpy.py": "trusted_translator_sha256",
    "/generation-evidence/invocation.json": "stage1_invocation_sha256",
    "/generation-evidence/metrics.json": "generation_metrics_sha256",
    "/generation-evidence/usage.json": "generation_usage_sha256",
    "/generation-evidence/codex-last.txt": "generation_codex_last_sha256",
    "/generation-evidence/codex-output.log": "generation_codex_output_sha256",
    "/generation-evidence/prompt.txt": "generation_prompt_sha256",
}
for raw_path, key in recorded_file_hashes.items():
    actual = sha256_file(Path(raw_path))
    expected = data["hashes"][key]
    print(f"hash[{raw_path}] actual={actual} recorded={expected} match={actual == expected}")

result = json.loads(Path("/generation-result.json").read_text())
for rel, expected in sorted(result["outputs"]["evidence"].items()):
    path = Path("/generation-evidence") / rel
    actual = sha256_file(path)
    print(f"result_evidence_hash[{rel}] actual={actual} recorded={expected} match={actual == expected}")

usage = json.loads(Path("/generation-evidence/usage.json").read_text())
invocation = json.loads(Path("/generation-evidence/invocation.json").read_text())
candidate_pipeline_hash = pipeline_tree_hash(Path("/candidate"))
trusted_semantics_pipeline_hash = pipeline_tree_hash(Path("/reference/reference-semantics"))
submitted_semantics_pipeline_hash = pipeline_tree_hash(Path("/candidate/reference-semantics"))
trace_pipeline_hash = pipeline_tree_hash(Path("/generation-evidence/codex-trace"))
print(
    "candidate_pipeline_tree_hash="
    f"{candidate_pipeline_hash} "
    f"generation_result_match={candidate_pipeline_hash == result['outputs']['workspace_sha256']} "
    f"invocation_match={candidate_pipeline_hash == invocation['retained_workspace_sha256']}"
)
print(
    "trusted_semantics_pipeline_tree_hash="
    f"{trusted_semantics_pipeline_hash} "
    "recorded_manifest_match="
    f"{trusted_semantics_pipeline_hash == data['hashes']['trusted_reference_semantics_manifest_sha256']}"
)
print(
    "submitted_semantics_pipeline_tree_hash="
    f"{submitted_semantics_pipeline_hash} "
    f"trusted_match={submitted_semantics_pipeline_hash == trusted_semantics_pipeline_hash}"
)
print(
    "trace_pipeline_tree_hash="
    f"{trace_pipeline_hash} "
    f"usage_match={trace_pipeline_hash == usage['source_trace_sha256']}"
)

comparisons = [
    (Path("/candidate/prompt.py"), Path("/reference/prompt.py"), "candidate_prompt"),
    (Path("/candidate/py2mpy.py"), Path("/reference/py2mpy.py"), "candidate_translator"),
]
for left, right, label in comparisons:
    print(
        f"{label}_byte_identity="
        f"{left.read_bytes() == right.read_bytes()} "
        f"left_sha256={sha256_file(left)} right_sha256={sha256_file(right)}"
    )

candidate_rows, candidate_manifest_hash = manifest(Path("/candidate"))
trusted_rows, trusted_manifest_hash = manifest(Path("/reference/reference-semantics"))
submitted_rows, submitted_manifest_hash = manifest(Path("/candidate/reference-semantics"))
print(f"reviewer_candidate_manifest_sha256={candidate_manifest_hash}")
print(f"reviewer_trusted_semantics_manifest_sha256={trusted_manifest_hash}")
print(f"reviewer_submitted_semantics_manifest_sha256={submitted_manifest_hash}")
print(f"semantics_manifest_identity={trusted_rows == submitted_rows}")
print(
    "candidate_special_entries="
    + json.dumps([row for row in candidate_rows if row["kind"] not in {"file", "dir"}])
)

if data["semantics_mode"] != "SUPPLIED_SEMANTICS":
    raise SystemExit("ERROR: rendered semantics mode is not SUPPLIED_SEMANTICS")
if not Path("/reference/reference-semantics").is_dir():
    raise SystemExit("ERROR: trusted supplied semantics mount is absent")
if lock != data["audit_campaign"]:
    raise SystemExit("ERROR: campaign lock mismatch")
if trusted_rows != submitted_rows:
    raise SystemExit("ERROR: supplied-semantics tree mismatch")

print("INTEGRITY_CHECK=PASS")
