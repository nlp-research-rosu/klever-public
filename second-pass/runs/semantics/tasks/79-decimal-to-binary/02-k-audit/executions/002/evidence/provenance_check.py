#!/usr/bin/env python3
"""Independent launcher/mount integrity checks for audit stage 1."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_tree(path: Path) -> str:
    """Reimplement the launcher manifest hash without importing launcher code."""
    root = path.resolve(strict=True)
    digest = hashlib.sha256()
    pending = [root]
    entries: list[tuple[str, str, Path]] = []
    while pending:
        directory = pending.pop()
        for child in os.scandir(directory):
            child_path = Path(child.path)
            mode = child.stat(follow_symlinks=False).st_mode
            relative = child_path.relative_to(root).as_posix()
            if stat.S_ISDIR(mode):
                entries.append((relative, "directory", child_path))
                pending.append(child_path)
            elif stat.S_ISREG(mode):
                entries.append((relative, "file", child_path))
            else:
                raise AssertionError(f"linked/unsupported tree entry: {child_path}")
    for relative, kind, child_path in sorted(entries):
        encoded = relative.encode()
        digest.update(len(encoded).to_bytes(4, "big"))
        digest.update(encoded)
        digest.update(kind.encode() + b"\0")
        if kind == "file":
            size = child_path.stat(follow_symlinks=False).st_size
            digest.update(size.to_bytes(8, "big"))
            with child_path.open("rb") as stream:
                for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                    digest.update(chunk)
    return digest.hexdigest()


def require_regular(path: Path) -> None:
    st = path.lstat()
    assert stat.S_ISREG(st.st_mode), f"not a regular file: {path}"


def require_directory(path: Path) -> None:
    st = path.lstat()
    assert stat.S_ISDIR(st.st_mode), f"not a real directory: {path}"


def compare_trees(left: Path, right: Path) -> None:
    left_entries: dict[str, tuple[str, str | None]] = {}
    right_entries: dict[str, tuple[str, str | None]] = {}
    for root, target in ((left, left_entries), (right, right_entries)):
        require_directory(root)
        for path in sorted(root.rglob("*")):
            rel = path.relative_to(root).as_posix()
            mode = path.lstat().st_mode
            if stat.S_ISDIR(mode):
                target[rel] = ("directory", None)
            elif stat.S_ISREG(mode):
                target[rel] = ("file", sha256_file(path))
            else:
                target[rel] = ("linked/unsupported", None)
    assert left_entries == right_entries, "recursive semantics mismatch"


def main() -> None:
    require_regular(AUDIT_INPUT)
    audit = json.loads(AUDIT_INPUT.read_text())
    assert audit["record_layout"] == "legacy-selected-stage1"
    assert audit["semantics_mode"] == "SUPPLIED_SEMANTICS"
    assert audit["mount_reference_semantics"] is True

    paths = {key: Path(value) for key, value in audit["container_paths"].items()}
    for key, path in sorted(paths.items()):
        if key in {"candidate", "generation_root", "generation_trace"}:
            require_directory(path)
        else:
            require_regular(path)
        print(f"container_path_ok {key} {path}")

    required = [
        Path("/run.json"),
        Path("/task.json"),
        Path("/generation-result.json"),
        Path("/generation-evidence/invocation.json"),
        Path("/generation-evidence/metrics.json"),
        Path("/generation-evidence/codex-last.txt"),
        Path("/generation-evidence/codex-output.log"),
        Path("/generation-evidence/prompt.txt"),
    ]
    if Path("/generation-evidence/usage.json").exists():
        required.append(Path("/generation-evidence/usage.json"))
    for path in required:
        require_regular(path)

    trace_files = sorted(Path("/generation-evidence/codex-trace").rglob("*"))
    assert trace_files
    assert all(stat.S_ISDIR(p.lstat().st_mode) or stat.S_ISREG(p.lstat().st_mode) for p in trace_files)
    assert not any(p.is_symlink() for p in trace_files)

    lock_path = Path("/audit-campaign-lock.json")
    require_regular(lock_path)
    lock = json.loads(lock_path.read_text())
    assert lock == audit["audit_campaign"], "campaign block differs from lock"
    lock_hash = sha256_file(lock_path)
    assert lock_hash == audit["hashes"]["audit_campaign_lock_sha256"]
    print(f"campaign_lock_match sha256={lock_hash}")

    file_hash_checks = {
        "/run.json": "run_manifest_sha256",
        "/task.json": "task_manifest_sha256",
        "/generation-result.json": "stage1_result_sha256",
        "/generation-evidence/invocation.json": "stage1_invocation_sha256",
        "/generation-evidence/metrics.json": "generation_metrics_sha256",
        "/generation-evidence/codex-last.txt": "generation_codex_last_sha256",
        "/generation-evidence/codex-output.log": "generation_codex_output_sha256",
        "/generation-evidence/prompt.txt": "generation_prompt_sha256",
        "/generation-evidence/usage.json": "generation_usage_sha256",
        "/reference/canonical.py": "canonical_sha256",
        "/reference/prompt.py": "trusted_prompt_sha256",
        "/reference/py2mpy.py": "trusted_translator_sha256",
        "/candidate/prompt.py": "candidate_prompt_sha256",
        "/candidate/py2mpy.py": "candidate_translator_sha256",
    }
    observed: dict[str, str] = {}
    for raw_path, hash_key in file_hash_checks.items():
        path = Path(raw_path)
        if not path.exists() and raw_path.endswith("/usage.json"):
            continue
        require_regular(path)
        actual = sha256_file(path)
        expected = audit["hashes"][hash_key]
        assert actual == expected, f"hash mismatch {path}: {actual} != {expected}"
        observed[raw_path] = actual
        print(f"file_hash_match {path} {actual}")

    generation_result = json.loads(Path("/generation-result.json").read_text())
    declared_evidence = generation_result["outputs"]["evidence"]
    for relative, expected in sorted(declared_evidence.items()):
        path = Path("/generation-evidence") / relative
        require_regular(path)
        actual = sha256_file(path)
        assert actual == expected, f"generation evidence mismatch: {relative}"
        print(f"generation_result_hash_match {relative} {actual}")

    trace_hash = sha256_tree(Path("/generation-evidence/codex-trace"))
    assert trace_hash == json.loads(Path("/generation-evidence/usage.json").read_text())["source_trace_sha256"]
    print(f"trace_pipeline_tree_hash_match {trace_hash}")
    print(
        "trace_launcher_alternate_hash_recorded "
        + audit["hashes"]["generation_codex_trace_sha256"]
    )

    candidate_tree = sha256_tree(Path("/candidate"))
    assert candidate_tree == generation_result["outputs"]["workspace_sha256"]
    assert candidate_tree == json.loads(Path("/generation-evidence/invocation.json").read_text())["outputs"]["workspace_sha256"]
    print(f"candidate_workspace_hash_match {candidate_tree}")
    print(
        "candidate_launcher_alternate_hash_recorded "
        + audit["hashes"]["candidate_tree_sha256"]
    )

    trusted_semantics = Path("/reference/reference-semantics")
    candidate_semantics = Path("/candidate/reference-semantics")
    compare_trees(candidate_semantics, trusted_semantics)
    semantics_tree_hash = sha256_tree(trusted_semantics)
    assert semantics_tree_hash == audit["hashes"]["trusted_reference_semantics_manifest_sha256"]
    assert semantics_tree_hash == sha256_tree(candidate_semantics)
    print(f"supplied_semantics_recursive_match tree_sha256={semantics_tree_hash}")
    print(
        "semantics_launcher_alternate_hash_recorded "
        + audit["hashes"]["candidate_reference_semantics_sha256"]
    )

    assert Path("/candidate/prompt.py").read_bytes() == Path("/reference/prompt.py").read_bytes()
    assert Path("/candidate/py2mpy.py").read_bytes() == Path("/reference/py2mpy.py").read_bytes()
    task_manifest = json.loads(Path("/task.json").read_text())
    audit_manifest = dict(audit["manifest"])
    assert audit_manifest.pop("config") == audit["config"]
    assert task_manifest == audit_manifest
    print("candidate_prompt_byte_match")
    print("candidate_translator_byte_match")
    print("task_manifest_matches_audit_manifest_after_launcher_config_enrichment")

    output = {
        "audit_input_sha256": sha256_file(AUDIT_INPUT),
        "candidate_workspace_sha256_tree": candidate_tree,
        "campaign_lock_sha256": lock_hash,
        "generation_trace_sha256_tree": trace_hash,
        "reference_semantics_sha256_tree": semantics_tree_hash,
        "verified_file_hashes": observed,
    }
    Path("/audit-output/evidence/provenance-hashes.json").write_text(
        json.dumps(output, indent=2, sort_keys=True) + "\n"
    )
    print("STAGE1_PROVENANCE_OK")


if __name__ == "__main__":
    main()
