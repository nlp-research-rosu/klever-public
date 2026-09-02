#!/usr/bin/env python3
"""Independent integrity checks for the mounted audit inputs."""

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


def sha256_tree(root: Path) -> str:
    """Pipeline-v3 tree hash, including real directory entries and file sizes."""
    if not root.is_dir() or root.is_symlink():
        raise ValueError(f"not a real directory: {root}")
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
                raise ValueError(f"linked or unsupported entry: {path}")
    digest = hashlib.sha256()
    for relative, kind, path in sorted(entries):
        encoded = relative.encode()
        digest.update(len(encoded).to_bytes(4, "big"))
        digest.update(encoded)
        digest.update(kind.encode() + b"\0")
        if kind == "file":
            data = path.read_bytes()
            digest.update(len(data).to_bytes(8, "big"))
            digest.update(data)
    return digest.hexdigest()


def regular_not_link(path: Path) -> bool:
    return path.is_file() and not path.is_symlink()


def check_hash(
    document: dict, label: str, path: Path, recorded_key: str
) -> bool:
    actual = sha256_file(path)
    recorded = document["hashes"][recorded_key]
    ok = actual == recorded
    print(
        f"HASH {label}: ok={ok} actual={actual} recorded={recorded} path={path}"
    )
    return ok


def main() -> int:
    audit = json.loads(AUDIT_INPUT.read_text())
    lock_path = Path(audit["container_paths"]["audit_campaign_lock"])
    lock = json.loads(lock_path.read_text())
    checks: list[bool] = []

    checks.append(audit["audit_campaign"] == lock)
    print(f"CAMPAIGN structural_equal={checks[-1]}")
    checks.append(
        sha256_file(lock_path) == audit["hashes"]["audit_campaign_lock_sha256"]
    )
    print(f"CAMPAIGN hash_equal={checks[-1]}")
    print(
        "MODE "
        f"record_layout={audit['record_layout']} "
        f"semantics_mode={audit['semantics_mode']} "
        f"mount_reference_semantics={audit['mount_reference_semantics']}"
    )

    required = [
        AUDIT_INPUT,
        lock_path,
        Path(audit["container_paths"]["run_manifest"]),
        Path(audit["container_paths"]["task_manifest"]),
        Path(audit["container_paths"]["stage1_result"]),
        Path(audit["container_paths"]["generation_manifest"]),
        Path(audit["container_paths"]["generation_metrics"]),
        Path(audit["container_paths"]["generation_last"]),
        Path(audit["container_paths"]["generation_output"]),
        Path(audit["container_paths"]["generation_root"]) / "prompt.txt",
        Path(audit["container_paths"]["generation_root"]) / "usage.json",
    ]
    trace_root = Path(audit["container_paths"]["generation_trace"])
    for path in required:
        ok = regular_not_link(path)
        checks.append(ok)
        print(f"REQUIRED regular_not_link={ok} path={path}")
    candidate_root = Path(audit["container_paths"]["candidate"])
    for name in [
        "prompt.py",
        "py2mpy.py",
        "solution.py",
        "solution.mpy",
        "semantic.k",
        "verification.k",
        "spec.k",
        "prove.sh",
    ]:
        path = candidate_root / name
        ok = regular_not_link(path)
        checks.append(ok)
        print(f"CANDIDATE_ARTIFACT regular_not_link={ok} path={path}")
    trace_ok = trace_root.is_dir() and not trace_root.is_symlink()
    checks.append(trace_ok)
    print(f"REQUIRED real_trace_directory={trace_ok} path={trace_root}")
    trace_entries = sorted(trace_root.rglob("*"))
    for path in trace_entries:
        ok = (
            (path.is_dir() and not path.is_symlink())
            or regular_not_link(path)
        )
        checks.append(ok)
        print(f"TRACE_ENTRY supported={ok} path={path}")

    direct = [
        ("lock", lock_path, "audit_campaign_lock_sha256"),
        (
            "run_manifest",
            Path(audit["container_paths"]["run_manifest"]),
            "run_manifest_sha256",
        ),
        (
            "task_manifest",
            Path(audit["container_paths"]["task_manifest"]),
            "task_manifest_sha256",
        ),
        (
            "stage1_result",
            Path(audit["container_paths"]["stage1_result"]),
            "stage1_result_sha256",
        ),
        (
            "stage1_invocation",
            Path(audit["container_paths"]["generation_manifest"]),
            "stage1_invocation_sha256",
        ),
        (
            "generation_metrics",
            Path(audit["container_paths"]["generation_metrics"]),
            "generation_metrics_sha256",
        ),
        (
            "generation_last",
            Path(audit["container_paths"]["generation_last"]),
            "generation_codex_last_sha256",
        ),
        (
            "generation_output",
            Path(audit["container_paths"]["generation_output"]),
            "generation_codex_output_sha256",
        ),
        (
            "generation_prompt",
            Path(audit["container_paths"]["generation_root"]) / "prompt.txt",
            "generation_prompt_sha256",
        ),
        (
            "generation_usage",
            Path(audit["container_paths"]["generation_root"]) / "usage.json",
            "generation_usage_sha256",
        ),
        (
            "canonical",
            Path(audit["container_paths"]["canonical"]),
            "canonical_sha256",
        ),
        (
            "trusted_prompt",
            Path(audit["container_paths"]["trusted_prompt"]),
            "trusted_prompt_sha256",
        ),
        (
            "trusted_translator",
            Path(audit["container_paths"]["translator"]),
            "trusted_translator_sha256",
        ),
        (
            "candidate_prompt",
            Path(audit["container_paths"]["candidate"]) / "prompt.py",
            "candidate_prompt_sha256",
        ),
        (
            "candidate_translator",
            Path(audit["container_paths"]["candidate"]) / "py2mpy.py",
            "candidate_translator_sha256",
        ),
    ]
    for label, path, key in direct:
        checks.append(check_hash(audit, label, path, key))

    reference_semantics = Path("/reference/reference-semantics")
    semantics_absent = not reference_semantics.exists()
    checks.append(semantics_absent)
    print(
        f"GENERATED_SEMANTICS reference_semantics_absent={semantics_absent}"
    )

    result = json.loads(
        Path(audit["container_paths"]["stage1_result"]).read_text()
    )
    usage = json.loads(
        (Path(audit["container_paths"]["generation_root"]) / "usage.json").read_text()
    )
    candidate_tree = sha256_tree(Path(audit["container_paths"]["candidate"]))
    trace_tree = sha256_tree(trace_root)
    expected_candidate_tree = result["outputs"]["workspace_sha256"]
    expected_trace_tree = usage["source_trace_sha256"]
    checks.extend(
        [
            candidate_tree == expected_candidate_tree,
            trace_tree == expected_trace_tree,
        ]
    )
    print(
        "TREE candidate "
        f"pipeline_sha256={candidate_tree} "
        f"stage1_recorded={expected_candidate_tree} "
        f"equal={candidate_tree == expected_candidate_tree}"
    )
    print(
        "TREE trace "
        f"pipeline_sha256={trace_tree} "
        f"usage_recorded={expected_trace_tree} "
        f"equal={trace_tree == expected_trace_tree}"
    )
    print(
        "AUDIT_AGGREGATE_FIELDS "
        f"candidate_tree_sha256={audit['hashes']['candidate_tree_sha256']} "
        f"generation_codex_trace_sha256="
        f"{audit['hashes']['generation_codex_trace_sha256']} "
        "scheme_not_declared_in_audit_input=True; "
        "pipeline hashes above are checked against the stage1 and usage records"
    )

    evidence_map = result["outputs"]["evidence"]
    generation_root = Path(audit["container_paths"]["generation_root"])
    for relative, expected in sorted(evidence_map.items()):
        path = generation_root / relative
        actual = sha256_file(path)
        ok = regular_not_link(path) and actual == expected
        checks.append(ok)
        print(
            f"EVIDENCE_MAP ok={ok} actual={actual} "
            f"recorded={expected} path={path}"
        )

    print(f"SUMMARY checks={len(checks)} failures={checks.count(False)}")
    return 0 if all(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
