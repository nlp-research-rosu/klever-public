#!/usr/bin/env python3
"""Independent mounted-input integrity checks for the 97-multiply audit."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")


def digest_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def tree_manifest(root: Path) -> tuple[str, list[str], list[str]]:
    """Hash a stable type/path/content manifest and report non-regular entries."""
    entries: list[str] = []
    irregular: list[str] = []
    for path in sorted(root.rglob("*"), key=lambda item: item.as_posix()):
        relative = path.relative_to(root).as_posix()
        mode = path.lstat().st_mode
        if stat.S_ISDIR(mode):
            entries.append(f"d\\0{relative}\\0")
        elif stat.S_ISREG(mode):
            entries.append(f"f\\0{relative}\\0{digest_file(path)}\\0")
        else:
            kind = (
                "l" if stat.S_ISLNK(mode) else
                "p" if stat.S_ISFIFO(mode) else
                "s" if stat.S_ISSOCK(mode) else
                "o"
            )
            entries.append(f"{kind}\\0{relative}\\0")
            irregular.append(f"{kind} {relative}")
    payload = "".join(entries).encode()
    return hashlib.sha256(payload).hexdigest(), entries, irregular


def launcher_tree_digest(root: Path) -> str:
    """Recompute the launcher-declared length/type/size/content tree digest."""
    entries: list[tuple[str, str, Path]] = []
    for path in root.rglob("*"):
        relative = path.relative_to(root).as_posix()
        mode = path.lstat().st_mode
        if stat.S_ISDIR(mode):
            entries.append((relative, "directory", path))
        elif stat.S_ISREG(mode):
            entries.append((relative, "file", path))
        else:
            raise ValueError(f"unsupported entry in launcher tree digest: {path}")
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


record = json.loads(AUDIT_INPUT.read_text(encoding="utf-8"))
paths = record["container_paths"]
expected = record["hashes"]

file_checks = {
    "audit_campaign_lock_sha256": Path(paths["audit_campaign_lock"]),
    "canonical_sha256": Path(paths["canonical"]),
    "trusted_prompt_sha256": Path(paths["trusted_prompt"]),
    "trusted_translator_sha256": Path(paths["translator"]),
    "generation_codex_last_sha256": Path(paths["generation_last"]),
    "generation_codex_output_sha256": Path(paths["generation_output"]),
    "generation_metrics_sha256": Path(paths["generation_metrics"]),
    "stage1_invocation_sha256": Path(paths["generation_manifest"]),
    "run_manifest_sha256": Path(paths["run_manifest"]),
    "stage1_result_sha256": Path(paths["stage1_result"]),
    "task_manifest_sha256": Path(paths["task_manifest"]),
}

all_ok = True
print("record_layout:", record["record_layout"])
print("semantics_mode:", record["semantics_mode"])
for key, path in file_checks.items():
    exists = path.is_file() and not path.is_symlink()
    actual = digest_file(path) if exists else "MISSING_OR_NOT_REGULAR"
    match = exists and actual == expected[key]
    all_ok &= match
    print(f"{key}: expected={expected[key]} actual={actual} match={match}")

extra_checks = {
    "generation_prompt_sha256": Path("/generation-evidence/prompt.txt"),
    "generation_usage_sha256": Path("/generation-evidence/usage.json"),
}
for key, path in extra_checks.items():
    exists = path.is_file() and not path.is_symlink()
    actual = digest_file(path) if exists else "MISSING_OR_NOT_REGULAR"
    match = exists and actual == expected[key]
    all_ok &= match
    print(f"{key}: expected={expected[key]} actual={actual} match={match}")

campaign = json.loads(Path(paths["audit_campaign_lock"]).read_text(encoding="utf-8"))
campaign_match = campaign == record["audit_campaign"]
all_ok &= campaign_match
print("campaign_block_exact_match:", campaign_match)

for label, root in (
    ("candidate", Path(paths["candidate"])),
    ("trusted_reference_semantics", Path("/reference/reference-semantics")),
    ("candidate_reference_semantics", Path("/candidate/reference-semantics")),
    ("generation_trace", Path(paths["generation_trace"])),
):
    digest, entries, irregular = tree_manifest(root)
    print(f"{label}_independent_manifest_sha256:", digest)
    print(f"{label}_entry_count:", len(entries))
    print(f"{label}_irregular_entries:", irregular)
    if irregular:
        all_ok = False

invocation = json.loads(
    Path(paths["generation_manifest"]).read_text(encoding="utf-8")
)
usage = json.loads(Path("/generation-evidence/usage.json").read_text(encoding="utf-8"))
pipeline_tree_checks = {
    "candidate_pipeline_tree": (
        Path(paths["candidate"]),
        invocation["outputs"]["workspace_sha256"],
    ),
    "trusted_reference_semantics_pipeline_tree": (
        Path("/reference/reference-semantics"),
        expected["trusted_reference_semantics_manifest_sha256"],
    ),
    "candidate_reference_semantics_pipeline_tree": (
        Path("/candidate/reference-semantics"),
        expected["trusted_reference_semantics_manifest_sha256"],
    ),
    "generation_trace_pipeline_tree": (
        Path(paths["generation_trace"]),
        usage["source_trace_sha256"],
    ),
}
for label, (root, recorded) in pipeline_tree_checks.items():
    actual = launcher_tree_digest(root)
    match = actual == recorded
    all_ok &= match
    print(f"{label}: recorded={recorded} actual={actual} match={match}")

print(
    "launcher_additional_tree_digests_read:",
    {
        key: expected[key]
        for key in (
            "candidate_tree_sha256",
            "trusted_reference_semantics_sha256",
            "candidate_reference_semantics_sha256",
            "generation_codex_trace_sha256",
        )
    },
)

print("all_direct_checks_pass:", all_ok)
raise SystemExit(0 if all_ok else 1)
