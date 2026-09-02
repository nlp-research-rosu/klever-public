#!/usr/bin/env python3
"""Independent integrity checks for audit record layout and mounted inputs."""

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
    digest = hashlib.sha256()
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
                raise RuntimeError(f"unsupported/symlinked tree entry: {path}")
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


def require_regular(path: Path) -> None:
    mode = path.lstat().st_mode
    if not stat.S_ISREG(mode):
        raise RuntimeError(f"not a real regular file: {path}")


def require_directory(path: Path) -> None:
    mode = path.lstat().st_mode
    if not stat.S_ISDIR(mode):
        raise RuntimeError(f"not a real directory: {path}")


def check(label: str, actual: object, expected: object) -> None:
    status = "OK" if actual == expected else "MISMATCH"
    print(f"{status} {label}: actual={actual!r} expected={expected!r}")
    if status != "OK":
        raise RuntimeError(f"{label} mismatch")


def report(label: str, actual: object, recorded: object) -> None:
    status = "MATCH" if actual == recorded else "DIFFERENT"
    print(f"{status} {label}: recomputed={actual!r} recorded={recorded!r}")


def main() -> None:
    require_regular(AUDIT_INPUT)
    data = json.loads(AUDIT_INPUT.read_text())
    check("record_layout", data["record_layout"], "legacy-selected-stage1")
    check("semantics_mode", data["semantics_mode"], "GENERATED_SEMANTICS")

    cp = {name: Path(path) for name, path in data["container_paths"].items()}
    for name in (
        "audit_campaign_lock",
        "canonical",
        "generation_last",
        "generation_manifest",
        "generation_metrics",
        "generation_output",
        "run_manifest",
        "stage1_result",
        "task_manifest",
        "translator",
        "trusted_prompt",
    ):
        require_regular(cp[name])
        print(f"OK regular launcher mount {name}: {cp[name]}")
    for name in ("candidate", "generation_root", "generation_trace"):
        require_directory(cp[name])
        print(f"OK directory launcher mount {name}: {cp[name]}")

    required_generation = (
        "invocation.json",
        "metrics.json",
        "codex-last.txt",
        "codex-output.log",
        "prompt.txt",
    )
    for name in required_generation:
        path = cp["generation_root"] / name
        require_regular(path)
        print(f"OK required legacy-selected-stage1 record: {path}")
    usage = cp["generation_root"] / "usage.json"
    if usage.exists():
        require_regular(usage)
        print(f"OK optional-present usage record: {usage}")

    check(
        "campaign lock hash",
        sha256_file(cp["audit_campaign_lock"]),
        data["hashes"]["audit_campaign_lock_sha256"],
    )
    campaign_lock = json.loads(cp["audit_campaign_lock"].read_text())
    check("campaign lock object", campaign_lock, data["audit_campaign"])

    file_hash_checks = {
        "canonical_sha256": cp["canonical"],
        "trusted_prompt_sha256": cp["trusted_prompt"],
        "trusted_translator_sha256": cp["translator"],
        "candidate_prompt_sha256": cp["candidate"] / "prompt.py",
        "candidate_translator_sha256": cp["candidate"] / "py2mpy.py",
        "run_manifest_sha256": cp["run_manifest"],
        "task_manifest_sha256": cp["task_manifest"],
        "stage1_result_sha256": cp["stage1_result"],
        "stage1_invocation_sha256": cp["generation_manifest"],
        "generation_metrics_sha256": cp["generation_metrics"],
        "generation_usage_sha256": usage,
        "generation_prompt_sha256": cp["generation_root"] / "prompt.txt",
        "generation_codex_last_sha256": cp["generation_last"],
        "generation_codex_output_sha256": cp["generation_output"],
    }
    for hash_name, path in file_hash_checks.items():
        check(hash_name, sha256_file(path), data["hashes"][hash_name])

    check(
        "candidate prompt byte identity",
        sha256_file(cp["candidate"] / "prompt.py"),
        sha256_file(cp["trusted_prompt"]),
    )
    check(
        "candidate translator byte identity",
        sha256_file(cp["candidate"] / "py2mpy.py"),
        sha256_file(cp["translator"]),
    )
    check(
        "reference-semantics absent",
        Path("/reference/reference-semantics").exists(),
        False,
    )

    result = json.loads(cp["stage1_result"].read_text())
    invocation = json.loads(cp["generation_manifest"].read_text())
    candidate_pipeline_hash = sha256_tree(cp["candidate"])
    check(
        "candidate tree equals generation-result workspace (pipeline-v3 hash)",
        candidate_pipeline_hash,
        result["outputs"]["workspace_sha256"],
    )
    report(
        "candidate tree versus audit-input opaque tree digest",
        candidate_pipeline_hash,
        data["hashes"]["candidate_tree_sha256"],
    )
    report(
        "generation trace versus audit-input opaque tree digest",
        sha256_tree(cp["generation_trace"]),
        data["hashes"]["generation_codex_trace_sha256"],
    )
    for relative, expected in result["outputs"]["evidence"].items():
        path = cp["generation_root"] / relative
        require_regular(path)
        check(f"generation-result evidence {relative}", sha256_file(path), expected)
    check(
        "result/invocation evidence maps",
        result["outputs"]["evidence"],
        invocation["outputs"]["evidence"],
    )
    print("ALL PROVENANCE CHECKS PASSED")


if __name__ == "__main__":
    main()
