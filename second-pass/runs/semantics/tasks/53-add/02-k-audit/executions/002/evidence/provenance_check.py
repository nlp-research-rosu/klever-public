#!/usr/bin/env python3
"""Independent read-only integrity checks for the mounted audit inputs."""

from __future__ import annotations

import hashlib
import json
import os
import stat
import sys
from pathlib import Path


AUDIT = Path("/audit-input.json")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def require_regular(path: Path) -> None:
    mode = path.lstat().st_mode
    if not stat.S_ISREG(mode):
        raise AssertionError(f"not a real regular file: {path}")


def require_directory(path: Path) -> None:
    mode = path.lstat().st_mode
    if not stat.S_ISDIR(mode):
        raise AssertionError(f"not a real directory: {path}")


def tree(root: Path) -> dict[str, tuple[str, str | None]]:
    require_directory(root)
    result: dict[str, tuple[str, str | None]] = {}
    pending = [root]
    while pending:
        directory = pending.pop()
        for entry in os.scandir(directory):
            path = Path(entry.path)
            rel = path.relative_to(root).as_posix()
            mode = entry.stat(follow_symlinks=False).st_mode
            if stat.S_ISDIR(mode):
                result[rel] = ("directory", None)
                pending.append(path)
            elif stat.S_ISREG(mode):
                result[rel] = ("file", sha256(path))
            else:
                raise AssertionError(f"linked or unsupported tree entry: {path}")
    return result


def pipeline_tree_hash(root: Path) -> str:
    """Recompute the recorded pipeline_contract.sha256_tree digest."""
    entries: list[tuple[str, str, Path]] = []
    pending = [root]
    while pending:
        directory = pending.pop()
        for entry in os.scandir(directory):
            path = Path(entry.path)
            rel = path.relative_to(root).as_posix()
            mode = entry.stat(follow_symlinks=False).st_mode
            if stat.S_ISDIR(mode):
                entries.append((rel, "directory", path))
                pending.append(path)
            elif stat.S_ISREG(mode):
                entries.append((rel, "file", path))
            else:
                raise AssertionError(f"linked or unsupported tree entry: {path}")
    digest = hashlib.sha256()
    for rel, kind, path in sorted(entries):
        encoded = rel.encode()
        digest.update(len(encoded).to_bytes(4, "big"))
        digest.update(encoded)
        digest.update(kind.encode() + b"\0")
        if kind == "file":
            data = path.read_bytes()
            digest.update(len(data).to_bytes(8, "big"))
            digest.update(data)
    return digest.hexdigest()


def legacy_file_tree_hash(root: Path) -> str:
    """Recompute the legacy file-only source-tree digest."""
    digest = hashlib.sha256()
    for path in sorted(candidate for candidate in root.rglob("*") if candidate.is_file()):
        require_regular(path)
        rel = path.relative_to(root).as_posix().encode()
        data = path.read_bytes()
        digest.update(len(rel).to_bytes(4, "big"))
        digest.update(rel)
        digest.update(len(data).to_bytes(8, "big"))
        digest.update(data)
    return digest.hexdigest()


def check_hash(label: str, path: Path, expected: str) -> None:
    require_regular(path)
    actual = sha256(path)
    print(f"{label}: expected={expected} actual={actual} match={actual == expected}")
    if actual != expected:
        raise AssertionError(f"{label} hash mismatch")


def main() -> int:
    require_regular(AUDIT)
    audit = json.loads(AUDIT.read_text())
    paths = {key: Path(value) for key, value in audit["container_paths"].items()}
    hashes = audit["hashes"]

    print(f"record_layout={audit['record_layout']}")
    print(f"semantics_mode={audit['semantics_mode']}")
    assert audit["record_layout"] == "legacy-selected-stage1"
    assert audit["semantics_mode"] == "SUPPLIED_SEMANTICS"

    lock_path = paths["audit_campaign_lock"]
    require_regular(lock_path)
    lock = json.loads(lock_path.read_text())
    print(f"campaign_block_equal={audit['audit_campaign'] == lock}")
    assert audit["audit_campaign"] == lock
    check_hash(
        "audit_campaign_lock",
        lock_path,
        hashes["audit_campaign_lock_sha256"],
    )

    record_hashes = [
        ("run_manifest", paths["run_manifest"], hashes["run_manifest_sha256"]),
        ("task_manifest", paths["task_manifest"], hashes["task_manifest_sha256"]),
        ("stage1_result", paths["stage1_result"], hashes["stage1_result_sha256"]),
        (
            "stage1_invocation",
            paths["generation_manifest"],
            hashes["stage1_invocation_sha256"],
        ),
        (
            "generation_metrics",
            paths["generation_metrics"],
            hashes["generation_metrics_sha256"],
        ),
        (
            "generation_usage",
            Path("/generation-evidence/usage.json"),
            hashes["generation_usage_sha256"],
        ),
        (
            "generation_codex_last",
            paths["generation_last"],
            hashes["generation_codex_last_sha256"],
        ),
        (
            "generation_codex_output",
            paths["generation_output"],
            hashes["generation_codex_output_sha256"],
        ),
        (
            "generation_prompt",
            Path("/generation-evidence/prompt.txt"),
            hashes["generation_prompt_sha256"],
        ),
    ]
    for args in record_hashes:
        check_hash(*args)

    check_hash("canonical", paths["canonical"], hashes["canonical_sha256"])
    check_hash("trusted_prompt", paths["trusted_prompt"], hashes["trusted_prompt_sha256"])
    check_hash(
        "trusted_translator",
        paths["translator"],
        hashes["trusted_translator_sha256"],
    )

    candidate = paths["candidate"]
    require_directory(candidate)
    check_hash(
        "candidate_prompt",
        candidate / "prompt.py",
        hashes["candidate_prompt_sha256"],
    )
    check_hash(
        "candidate_translator",
        candidate / "py2mpy.py",
        hashes["candidate_translator_sha256"],
    )
    assert (candidate / "prompt.py").read_bytes() == paths["trusted_prompt"].read_bytes()
    assert (candidate / "py2mpy.py").read_bytes() == paths["translator"].read_bytes()
    print("candidate_prompt_byte_identity=True")
    print("candidate_translator_byte_identity=True")

    trusted_semantics = Path("/reference/reference-semantics")
    candidate_semantics = candidate / "reference-semantics"
    trusted_tree = tree(trusted_semantics)
    candidate_tree = tree(candidate_semantics)
    print(f"trusted_semantics_entries={len(trusted_tree)}")
    print(f"candidate_semantics_entries={len(candidate_tree)}")
    print(f"semantics_tree_identity={trusted_tree == candidate_tree}")
    if trusted_tree != candidate_tree:
        for missing in sorted(set(trusted_tree) - set(candidate_tree)):
            print(f"MISSING_CANDIDATE_SEMANTICS_ENTRY {missing}")
        for extra in sorted(set(candidate_tree) - set(trusted_tree)):
            print(f"ADDITIONAL_CANDIDATE_SEMANTICS_ENTRY {extra}")
        for shared in sorted(set(trusted_tree) & set(candidate_tree)):
            if trusted_tree[shared] != candidate_tree[shared]:
                print(
                    f"CHANGED_CANDIDATE_SEMANTICS_ENTRY {shared} "
                    f"trusted={trusted_tree[shared]} candidate={candidate_tree[shared]}"
                )
        raise AssertionError("supplied semantics trees differ")

    trusted_manifest_hash = pipeline_tree_hash(trusted_semantics)
    candidate_manifest_hash = pipeline_tree_hash(candidate_semantics)
    expected_manifest_hash = hashes["trusted_reference_semantics_manifest_sha256"]
    print(
        "trusted_semantics_pipeline_tree_hash="
        f"{trusted_manifest_hash} expected={expected_manifest_hash} "
        f"match={trusted_manifest_hash == expected_manifest_hash}"
    )
    print(
        "candidate_semantics_pipeline_tree_hash="
        f"{candidate_manifest_hash} expected={expected_manifest_hash} "
        f"match={candidate_manifest_hash == expected_manifest_hash}"
    )
    assert trusted_manifest_hash == candidate_manifest_hash == expected_manifest_hash

    trusted_legacy_hash = legacy_file_tree_hash(trusted_semantics)
    expected_legacy_hash = hashes["trusted_reference_semantics_legacy_sha256"]
    print(
        f"trusted_semantics_legacy_hash={trusted_legacy_hash} "
        f"expected={expected_legacy_hash} match={trusted_legacy_hash == expected_legacy_hash}"
    )
    assert trusted_legacy_hash == expected_legacy_hash

    result = json.loads(paths["stage1_result"].read_text())
    invocation = json.loads(paths["generation_manifest"].read_text())
    generation_root = paths["generation_root"]
    for owner, record in (("result", result), ("invocation", invocation)):
        for rel, expected in sorted(record["outputs"]["evidence"].items()):
            check_hash(f"{owner}.outputs.evidence[{rel}]", generation_root / rel, expected)

    trace_dir = paths["generation_trace"]
    require_directory(trace_dir)
    trace_files = [
        path for path in sorted(trace_dir.rglob("*")) if path.is_file()
    ]
    print(f"trace_file_count={len(trace_files)}")
    for path in trace_files:
        require_regular(path)
        print(f"trace_file={path.relative_to(trace_dir)} sha256={sha256(path)}")

    candidate_pipeline_hash = pipeline_tree_hash(candidate)
    expected_workspace_hash = invocation["retained_workspace_sha256"]
    print(
        f"candidate_pipeline_tree_hash={candidate_pipeline_hash} "
        f"expected_retained_workspace={expected_workspace_hash} "
        f"match={candidate_pipeline_hash == expected_workspace_hash}"
    )
    assert candidate_pipeline_hash == expected_workspace_hash

    usage = json.loads(Path("/generation-evidence/usage.json").read_text())
    trace_pipeline_hash = pipeline_tree_hash(trace_dir)
    expected_trace_hash = usage["source_trace_sha256"]
    print(
        f"trace_pipeline_tree_hash={trace_pipeline_hash} "
        f"expected={expected_trace_hash} match={trace_pipeline_hash == expected_trace_hash}"
    )
    assert trace_pipeline_hash == expected_trace_hash

    print("PROVENANCE_CHECK=PASS")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (AssertionError, OSError, ValueError, KeyError) as error:
        print(f"PROVENANCE_CHECK=FAIL: {error}", file=sys.stderr)
        raise SystemExit(1)
