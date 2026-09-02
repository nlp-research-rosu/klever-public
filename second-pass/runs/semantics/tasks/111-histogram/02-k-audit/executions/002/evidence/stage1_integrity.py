#!/usr/bin/env python3
"""Independent integrity checks for the mounted audit inputs."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from pathlib import Path
from typing import Iterable


AUDIT = Path("/audit-input.json")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as src:
        for chunk in iter(lambda: src.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def entries(root: Path) -> Iterable[Path]:
    yield root
    yield from sorted(root.rglob("*"), key=lambda p: p.relative_to(root).as_posix())


def pipeline_tree_sha256(root: Path) -> str:
    """Reimplement the mounted pipeline-v2 length-delimited tree digest."""
    digest = hashlib.sha256()
    pending = [root]
    tree_entries: list[tuple[str, str, Path]] = []
    while pending:
        directory = pending.pop()
        for child in os.scandir(directory):
            path = Path(child.path)
            mode = child.stat(follow_symlinks=False).st_mode
            relative = path.relative_to(root).as_posix()
            if stat.S_ISDIR(mode):
                tree_entries.append((relative, "directory", path))
                pending.append(path)
            elif stat.S_ISREG(mode):
                tree_entries.append((relative, "file", path))
            else:
                raise ValueError(f"unsupported tree entry: {path}")
    for relative, kind, path in sorted(tree_entries):
        encoded = relative.encode()
        digest.update(len(encoded).to_bytes(4, "big"))
        digest.update(encoded)
        digest.update(kind.encode() + b"\0")
        if kind == "file":
            digest.update(path.stat(follow_symlinks=False).st_size.to_bytes(8, "big"))
            with path.open("rb") as src:
                for chunk in iter(lambda: src.read(1024 * 1024), b""):
                    digest.update(chunk)
    return digest.hexdigest()


def compare_trees(left: Path, right: Path) -> list[str]:
    issues: list[str] = []
    left_entries = {
        p.relative_to(left).as_posix(): p for p in entries(left) if p != left
    }
    right_entries = {
        p.relative_to(right).as_posix(): p for p in entries(right) if p != right
    }
    for rel in sorted(left_entries.keys() | right_entries.keys()):
        lp = left_entries.get(rel)
        rp = right_entries.get(rel)
        if lp is None:
            issues.append(f"candidate missing entry: {rel}")
            continue
        if rp is None:
            issues.append(f"candidate additional entry: {rel}")
            continue
        if lp.is_symlink() or rp.is_symlink():
            issues.append(f"symlink entry: {rel}")
            continue
        lkind = "dir" if lp.is_dir() else "file" if lp.is_file() else "other"
        rkind = "dir" if rp.is_dir() else "file" if rp.is_file() else "other"
        if lkind != rkind:
            issues.append(f"entry type mismatch: {rel}: {lkind} != {rkind}")
        elif lkind == "file" and sha256_file(lp) != sha256_file(rp):
            issues.append(f"file content mismatch: {rel}")
    return issues


def check_regular(path: Path, issues: list[str], label: str) -> None:
    if not path.exists():
        issues.append(f"missing {label}: {path}")
    elif path.is_symlink():
        issues.append(f"symlinked {label}: {path}")
    elif not path.is_file():
        issues.append(f"mistyped {label}: {path}")
    elif not os.access(path, os.R_OK):
        issues.append(f"unreadable {label}: {path}")


def main() -> int:
    data = json.loads(AUDIT.read_text())
    paths = data["container_paths"]
    issues: list[str] = []

    print(f"record_layout={data['record_layout']}")
    print(f"semantics_mode={data['semantics_mode']}")

    required = {
        "audit input": AUDIT,
        "campaign lock": Path(paths["audit_campaign_lock"]),
        "run manifest": Path(paths["run_manifest"]),
        "task manifest": Path(paths["task_manifest"]),
        "stage1 result": Path(paths["stage1_result"]),
        "generation invocation": Path(paths["generation_manifest"]),
        "generation metrics": Path(paths["generation_metrics"]),
        "generation last": Path(paths["generation_last"]),
        "generation output": Path(paths["generation_output"]),
        "generation prompt": Path(paths["generation_root"]) / "prompt.txt",
        "trusted canonical": Path(paths["canonical"]),
        "trusted prompt": Path(paths["trusted_prompt"]),
        "trusted translator": Path(paths["translator"]),
    }
    for label, path in required.items():
        check_regular(path, issues, label)

    trace_root = Path(paths["generation_trace"])
    if not trace_root.exists():
        issues.append(f"missing structured trace: {trace_root}")
    elif trace_root.is_symlink() or not trace_root.is_dir():
        issues.append(f"mistyped or symlinked structured trace: {trace_root}")
    else:
        trace_files = [p for p in trace_root.rglob("*") if p.is_file()]
        if not trace_files:
            issues.append(f"empty structured trace: {trace_root}")
        for p in entries(trace_root):
            if p.is_symlink():
                issues.append(f"symlink in structured trace: {p}")
            elif not (p.is_dir() or p.is_file()):
                issues.append(f"mistyped structured-trace entry: {p}")

    candidate = Path(paths["candidate"])
    if not candidate.exists() or candidate.is_symlink() or not candidate.is_dir():
        issues.append(f"missing, mistyped, or symlinked candidate mount: {candidate}")
    else:
        for p in entries(candidate):
            if p.is_symlink():
                issues.append(f"symlink in candidate: {p}")
            elif not (p.is_dir() or p.is_file()):
                issues.append(f"mistyped candidate entry: {p}")

    trusted_semantics = Path("/reference/reference-semantics")
    candidate_semantics = candidate / "reference-semantics"
    if data["semantics_mode"] != "SUPPLIED_SEMANTICS":
        issues.append("unexpected semantics mode for this audit script")
    if not trusted_semantics.exists():
        issues.append("trusted supplied-semantics mount is absent")
    elif trusted_semantics.is_symlink() or not trusted_semantics.is_dir():
        issues.append("trusted supplied-semantics mount is mistyped or symlinked")
    if not candidate_semantics.exists():
        issues.append("candidate reference-semantics tree is absent")
    elif candidate_semantics.is_symlink() or not candidate_semantics.is_dir():
        issues.append("candidate reference-semantics tree is mistyped or symlinked")
    elif trusted_semantics.is_dir():
        issues.extend(compare_trees(candidate_semantics, trusted_semantics))

    lock_path = Path(paths["audit_campaign_lock"])
    if lock_path.is_file():
        lock_bytes_hash = sha256_file(lock_path)
        print(f"audit_campaign_lock_sha256={lock_bytes_hash}")
        print(
            "audit_campaign_lock_hash_match="
            f"{lock_bytes_hash == data['hashes']['audit_campaign_lock_sha256']}"
        )
        lock = json.loads(lock_path.read_text())
        print(f"audit_campaign_object_match={lock == data['audit_campaign']}")
        if lock_bytes_hash != data["hashes"]["audit_campaign_lock_sha256"]:
            issues.append("campaign lock byte hash differs from audit-input")
        if lock != data["audit_campaign"]:
            issues.append("campaign lock object differs from audit campaign block")

    file_hash_checks = {
        "canonical_sha256": Path(paths["canonical"]),
        "trusted_prompt_sha256": Path(paths["trusted_prompt"]),
        "candidate_prompt_sha256": candidate / "prompt.py",
        "trusted_translator_sha256": Path(paths["translator"]),
        "candidate_translator_sha256": candidate / "py2mpy.py",
        "run_manifest_sha256": Path(paths["run_manifest"]),
        "task_manifest_sha256": Path(paths["task_manifest"]),
        "manifest_sha256": Path(paths["task_manifest"]),
        "stage1_result_sha256": Path(paths["stage1_result"]),
        "stage1_invocation_sha256": Path(paths["generation_manifest"]),
        "generation_metrics_sha256": Path(paths["generation_metrics"]),
        "generation_codex_last_sha256": Path(paths["generation_last"]),
        "generation_codex_output_sha256": Path(paths["generation_output"]),
        "generation_prompt_sha256": Path(paths["generation_root"]) / "prompt.txt",
        "generation_usage_sha256": Path(paths["generation_root"]) / "usage.json",
    }
    for field, path in file_hash_checks.items():
        if not path.is_file():
            if field != "generation_usage_sha256":
                issues.append(f"cannot hash missing regular file for {field}: {path}")
            continue
        actual = sha256_file(path)
        expected = data["hashes"][field]
        ok = actual == expected
        print(f"{field}: expected={expected} actual={actual} match={ok}")
        if not ok:
            issues.append(f"declared hash mismatch for {field}: {path}")

    for manifest_path in (
        Path(paths["stage1_result"]),
        Path(paths["generation_manifest"]),
    ):
        if not manifest_path.is_file():
            continue
        record = json.loads(manifest_path.read_text())
        declared_outputs = record.get("outputs", {}).get("evidence", {})
        for rel, expected in sorted(declared_outputs.items()):
            path = Path(paths["generation_root"]) / rel
            if not path.exists():
                issues.append(
                    f"declared generation output missing ({manifest_path.name}): {rel}"
                )
                continue
            if path.is_symlink() or not path.is_file():
                issues.append(
                    f"declared generation output mistyped/symlinked "
                    f"({manifest_path.name}): {rel}"
                )
                continue
            actual = sha256_file(path)
            ok = actual == expected
            print(
                f"{manifest_path.name} output {rel}: "
                f"expected={expected} actual={actual} match={ok}"
            )
            if not ok:
                issues.append(
                    f"declared generation output hash mismatch "
                    f"({manifest_path.name}): {rel}"
                )

    if (candidate / "prompt.py").is_file() and Path(paths["trusted_prompt"]).is_file():
        same = (candidate / "prompt.py").read_bytes() == Path(
            paths["trusted_prompt"]
        ).read_bytes()
        print(f"candidate_prompt_byte_identity={same}")
        if not same:
            issues.append("candidate prompt differs from trusted prompt")
    if (candidate / "py2mpy.py").is_file() and Path(paths["translator"]).is_file():
        same = (candidate / "py2mpy.py").read_bytes() == Path(
            paths["translator"]
        ).read_bytes()
        print(f"candidate_translator_byte_identity={same}")
        if not same:
            issues.append("candidate translator differs from trusted translator")

    result_record = json.loads(Path(paths["stage1_result"]).read_text())
    invocation_record = json.loads(Path(paths["generation_manifest"]).read_text())
    candidate_pipeline_hash = pipeline_tree_sha256(candidate)
    print(f"candidate_pipeline_tree_sha256={candidate_pipeline_hash}")
    for label, expected in (
        (
            "stage1_result.outputs.workspace_sha256",
            result_record["outputs"]["workspace_sha256"],
        ),
        (
            "invocation.retained_workspace_sha256",
            invocation_record["retained_workspace_sha256"],
        ),
    ):
        ok = candidate_pipeline_hash == expected
        print(f"{label}: expected={expected} match={ok}")
        if not ok:
            issues.append(f"candidate pipeline tree differs from {label}")

    trusted_semantics_pipeline_hash = pipeline_tree_sha256(trusted_semantics)
    candidate_semantics_pipeline_hash = pipeline_tree_sha256(candidate_semantics)
    expected_semantics_manifest = data["hashes"][
        "trusted_reference_semantics_manifest_sha256"
    ]
    print(
        "trusted_semantics_pipeline_tree_sha256="
        f"{trusted_semantics_pipeline_hash}"
    )
    print(
        "candidate_semantics_pipeline_tree_sha256="
        f"{candidate_semantics_pipeline_hash}"
    )
    if trusted_semantics_pipeline_hash != expected_semantics_manifest:
        issues.append("trusted semantics pipeline-tree hash differs from manifest hash")
    if candidate_semantics_pipeline_hash != expected_semantics_manifest:
        issues.append("candidate semantics pipeline-tree hash differs from manifest hash")

    usage_path = Path(paths["generation_root"]) / "usage.json"
    if usage_path.is_file():
        usage_record = json.loads(usage_path.read_text())
        trace_pipeline_hash = pipeline_tree_sha256(trace_root)
        expected_trace = usage_record["source_trace_sha256"]
        print(f"trace_pipeline_tree_sha256={trace_pipeline_hash}")
        print(
            "usage.source_trace_sha256_match="
            f"{trace_pipeline_hash == expected_trace}"
        )
        if trace_pipeline_hash != expected_trace:
            issues.append("structured trace pipeline-tree hash differs from usage")

    print(f"semantics_tree_issue_count={len(compare_trees(candidate_semantics, trusted_semantics)) if candidate_semantics.is_dir() and trusted_semantics.is_dir() else 'N/A'}")
    print(f"issue_count={len(issues)}")
    for issue in issues:
        print(f"ISSUE: {issue}")
    return 1 if issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
