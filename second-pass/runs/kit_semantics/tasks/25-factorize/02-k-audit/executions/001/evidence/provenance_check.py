#!/usr/bin/env python3
"""Independently validate mounted provenance records and supplied inputs."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from pathlib import Path


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def walk_entries(root: Path) -> list[tuple[str, str, int, str | None]]:
    entries: list[tuple[str, str, int, str | None]] = []
    for base, dirs, files in os.walk(root, topdown=True, followlinks=False):
        dirs.sort()
        files.sort()
        for name in dirs + files:
            path = Path(base) / name
            rel = path.relative_to(root).as_posix()
            mode = path.lstat().st_mode
            if stat.S_ISLNK(mode):
                entries.append((rel, "symlink", stat.S_IMODE(mode), os.readlink(path)))
            elif stat.S_ISDIR(mode):
                entries.append((rel, "dir", stat.S_IMODE(mode), None))
            elif stat.S_ISREG(mode):
                entries.append((rel, "file", stat.S_IMODE(mode), sha256_file(path)))
            else:
                entries.append((rel, "other", stat.S_IMODE(mode), None))
    return entries


def sha256_tree(root: Path) -> str:
    """Reimplement the pipeline tree hash from entry type/path/size/content."""
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
    for relative, kind, path in sorted(entries):
        encoded = relative.encode()
        digest.update(len(encoded).to_bytes(4, "big"))
        digest.update(encoded)
        digest.update(kind.encode() + b"\0")
        if kind == "file":
            raw = path.read_bytes()
            digest.update(len(raw).to_bytes(8, "big"))
            digest.update(raw)
    return digest.hexdigest()


def compare_trees(left: Path, right: Path) -> list[str]:
    differences: list[str] = []
    left_entries = {entry[0]: entry[1:] for entry in walk_entries(left)}
    right_entries = {entry[0]: entry[1:] for entry in walk_entries(right)}
    for rel in sorted(left_entries.keys() | right_entries.keys()):
        if rel not in left_entries:
            differences.append(f"missing from candidate: {rel}")
        elif rel not in right_entries:
            differences.append(f"additional in candidate: {rel}")
        elif left_entries[rel][0] != right_entries[rel][0]:
            differences.append(
                f"type mismatch {rel}: candidate={left_entries[rel][0]} "
                f"trusted={right_entries[rel][0]}"
            )
        elif left_entries[rel][0] == "symlink":
            differences.append(f"symlink entry is forbidden: {rel}")
        elif left_entries[rel][0] == "file" and left_entries[rel][2] != right_entries[rel][2]:
            differences.append(
                f"content mismatch {rel}: candidate={left_entries[rel][2]} "
                f"trusted={right_entries[rel][2]}"
            )
    return differences


def main() -> None:
    audit_path = Path("/audit-input.json")
    audit_raw = audit_path.read_bytes()
    audit = json.loads(audit_raw)
    lock_path = Path(audit["container_paths"]["audit_campaign_lock"])
    lock_raw = lock_path.read_bytes()
    lock = json.loads(lock_raw)
    recorded = audit["hashes"]

    print(f"record_layout={audit['record_layout']}")
    print(f"semantics_mode={audit['semantics_mode']}")
    print(f"audit_input_sha256={hashlib.sha256(audit_raw).hexdigest()}")
    print(
        "campaign_lock_sha256="
        f"{hashlib.sha256(lock_raw).hexdigest()} "
        f"recorded={recorded['audit_campaign_lock_sha256']}"
    )
    print(f"campaign_block_exact_match={lock == audit['audit_campaign']}")

    file_checks = [
        ("canonical", Path(audit["container_paths"]["canonical"]), "canonical_sha256"),
        ("trusted_prompt", Path(audit["container_paths"]["trusted_prompt"]), "trusted_prompt_sha256"),
        ("candidate_prompt", Path("/candidate/prompt.py"), "candidate_prompt_sha256"),
        ("trusted_translator", Path(audit["container_paths"]["translator"]), "trusted_translator_sha256"),
        ("candidate_translator", Path("/candidate/py2mpy.py"), "candidate_translator_sha256"),
        ("run_manifest", Path(audit["container_paths"]["run_manifest"]), "run_manifest_sha256"),
        ("task_manifest", Path(audit["container_paths"]["task_manifest"]), "task_manifest_sha256"),
        ("stage1_result", Path(audit["container_paths"]["stage1_result"]), "stage1_result_sha256"),
        ("invocation", Path(audit["container_paths"]["generation_manifest"]), "stage1_invocation_sha256"),
        ("generation_metrics", Path(audit["container_paths"]["generation_metrics"]), "generation_metrics_sha256"),
        ("generation_last", Path(audit["container_paths"]["generation_last"]), "generation_codex_last_sha256"),
        ("generation_output", Path(audit["container_paths"]["generation_output"]), "generation_codex_output_sha256"),
        ("generation_prompt", Path("/generation-evidence/prompt.txt"), "generation_prompt_sha256"),
        ("runtime_metrics", Path("/generation-evidence/runtime-metrics.json"), "generation_runtime_metrics_sha256"),
        ("usage", Path("/generation-evidence/usage.json"), "generation_usage_sha256"),
    ]
    for name, path, key in file_checks:
        if not path.exists():
            print(f"{name}: MISSING path={path}")
            continue
        kind = "symlink" if path.is_symlink() else "regular" if path.is_file() else "other"
        actual = sha256_file(path) if path.is_file() else "-"
        print(
            f"{name}: type={kind} path={path} sha256={actual} "
            f"recorded={recorded.get(key)} match={actual == recorded.get(key)}"
        )

    trace_root = Path(audit["container_paths"]["generation_trace"])
    result = json.loads(Path(audit["container_paths"]["stage1_result"]).read_text())
    for rel, expected in result["outputs"]["evidence"].items():
        path = Path(audit["container_paths"]["generation_root"]) / rel
        actual = sha256_file(path) if path.is_file() else "MISSING"
        print(
            f"result_evidence: {rel} type="
            f"{'symlink' if path.is_symlink() else 'regular' if path.is_file() else 'missing'} "
            f"sha256={actual} recorded={expected} match={actual == expected}"
        )

    print(f"trace_root={trace_root}")
    for entry in walk_entries(trace_root):
        print(f"trace_entry={entry}")

    semantics_differences = compare_trees(
        Path("/candidate/reference-semantics"),
        Path("/reference/reference-semantics"),
    )
    print(f"reference_semantics_difference_count={len(semantics_differences)}")
    for difference in semantics_differences:
        print(f"reference_semantics_difference={difference}")

    candidate_links = [entry for entry in walk_entries(Path("/candidate")) if entry[1] == "symlink"]
    print(f"candidate_symlink_count={len(candidate_links)}")
    for entry in candidate_links:
        print(f"candidate_symlink={entry}")
    for name in [
        "solution.py",
        "solution.mpy",
        "verification.k",
        "spec.k",
        "prove.sh",
        "PROOF.md",
        "prompt.py",
        "py2mpy.py",
    ]:
        path = Path("/candidate") / name
        mode = path.lstat().st_mode if path.exists() else 0
        print(
            f"candidate_artifact={name} "
            f"type={'regular' if stat.S_ISREG(mode) else 'missing-or-wrong-type'} "
            f"sha256={sha256_file(path) if stat.S_ISREG(mode) else '-'}"
        )

    usage = json.loads(Path("/generation-evidence/usage.json").read_text())
    pipeline_tree_checks = [
        (
            "candidate_tree",
            Path("/candidate"),
            result["outputs"]["workspace_sha256"],
            "generation-result.outputs.workspace_sha256",
        ),
        (
            "candidate_reference_semantics_tree",
            Path("/candidate/reference-semantics"),
            recorded["trusted_reference_semantics_manifest_sha256"],
            "audit-input.hashes.trusted_reference_semantics_manifest_sha256",
        ),
        (
            "trusted_reference_semantics_tree",
            Path("/reference/reference-semantics"),
            recorded["trusted_reference_semantics_manifest_sha256"],
            "audit-input.hashes.trusted_reference_semantics_manifest_sha256",
        ),
        (
            "generation_trace_tree",
            trace_root,
            usage["source_trace_sha256"],
            "generation-evidence/usage.json.source_trace_sha256",
        ),
    ]
    for name, path, expected, source in pipeline_tree_checks:
        actual = sha256_tree(path)
        print(
            f"{name}: pipeline_sha256_tree={actual} recorded={expected} "
            f"record_source={source} match={actual == expected}"
        )
    print(
        "launcher_alternate_tree_digests="
        f"candidate:{recorded['candidate_tree_sha256']},"
        f"candidate_semantics:{recorded['candidate_reference_semantics_sha256']},"
        f"trusted_semantics:{recorded['trusted_reference_semantics_sha256']},"
        f"trace:{recorded['generation_codex_trace_sha256']}"
    )


if __name__ == "__main__":
    main()
