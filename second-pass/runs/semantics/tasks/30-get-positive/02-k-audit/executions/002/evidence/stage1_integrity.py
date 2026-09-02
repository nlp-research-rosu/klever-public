#!/usr/bin/env python3
"""Independent integrity checks for the launcher-owned audit inputs."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def require_regular(path: Path) -> None:
    mode = path.lstat().st_mode
    if not stat.S_ISREG(mode) or path.is_symlink():
        raise AssertionError(f"not a real regular file: {path}")
    if not os.access(path, os.R_OK):
        raise AssertionError(f"not readable: {path}")


def require_directory(path: Path) -> None:
    mode = path.lstat().st_mode
    if not stat.S_ISDIR(mode) or path.is_symlink():
        raise AssertionError(f"not a real directory: {path}")
    if not os.access(path, os.R_OK | os.X_OK):
        raise AssertionError(f"not readable/searchable: {path}")


def tree_manifest(root: Path) -> list[dict[str, str | int]]:
    require_directory(root)
    manifest: list[dict[str, str | int]] = []
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root).as_posix()
        mode = path.lstat().st_mode
        if stat.S_ISLNK(mode):
            raise AssertionError(f"symlinked tree entry: {path}")
        if stat.S_ISDIR(mode):
            manifest.append({"path": relative, "type": "directory"})
        elif stat.S_ISREG(mode):
            require_regular(path)
            manifest.append(
                {
                    "path": relative,
                    "type": "file",
                    "size": path.stat().st_size,
                    "sha256": sha256(path),
                }
            )
        else:
            raise AssertionError(f"unsupported tree entry: {path}")
    return manifest


def compare_trees(left: Path, right: Path) -> tuple[bool, list[str]]:
    left_manifest = tree_manifest(left)
    right_manifest = tree_manifest(right)
    problems: list[str] = []
    left_by_path = {str(item["path"]): item for item in left_manifest}
    right_by_path = {str(item["path"]): item for item in right_manifest}
    for relative in sorted(left_by_path.keys() | right_by_path.keys()):
        if relative not in left_by_path:
            problems.append(f"missing candidate entry: {relative}")
        elif relative not in right_by_path:
            problems.append(f"additional candidate entry: {relative}")
        elif left_by_path[relative] != right_by_path[relative]:
            problems.append(
                f"changed or mistyped entry: {relative}: "
                f"candidate={left_by_path[relative]!r} "
                f"trusted={right_by_path[relative]!r}"
            )
    return not problems, problems


def manifest_hash(manifest: list[dict[str, str | int]]) -> str:
    data = json.dumps(
        manifest, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode()
    return hashlib.sha256(data).hexdigest()


def main() -> None:
    require_regular(AUDIT_INPUT)
    audit = json.loads(AUDIT_INPUT.read_text(encoding="utf-8"))
    assert audit["record_layout"] == "legacy-selected-stage1"
    assert audit["semantics_mode"] == "SUPPLIED_SEMANTICS"
    assert audit["mount_reference_semantics"] is True

    required_files = [
        AUDIT_INPUT,
        Path("/audit-campaign-lock.json"),
        Path("/run.json"),
        Path("/task.json"),
        Path("/generation-result.json"),
        Path("/generation-evidence/invocation.json"),
        Path("/generation-evidence/metrics.json"),
        Path("/generation-evidence/codex-last.txt"),
        Path("/generation-evidence/codex-output.log"),
        Path("/generation-evidence/prompt.txt"),
    ]
    usage = Path("/generation-evidence/usage.json")
    if usage.exists():
        required_files.append(usage)
    for path in required_files:
        require_regular(path)

    required_directories = [
        Path("/candidate"),
        Path("/generation-evidence"),
        Path("/generation-evidence/codex-trace"),
        Path("/reference/reference-semantics"),
    ]
    for path in required_directories:
        require_directory(path)

    for value in audit["container_paths"].values():
        path = Path(value)
        if not path.exists():
            raise AssertionError(f"missing launcher-declared mount: {path}")
        if path.is_dir():
            require_directory(path)
        else:
            require_regular(path)

    campaign = json.loads(
        Path("/audit-campaign-lock.json").read_text(encoding="utf-8")
    )
    assert campaign == audit["audit_campaign"], "campaign block differs from lock"

    recorded_file_hashes = {
        Path("/audit-campaign-lock.json"): "audit_campaign_lock_sha256",
        Path("/run.json"): "run_manifest_sha256",
        Path("/task.json"): "task_manifest_sha256",
        Path("/generation-result.json"): "stage1_result_sha256",
        Path("/generation-evidence/invocation.json"): "stage1_invocation_sha256",
        Path("/generation-evidence/metrics.json"): "generation_metrics_sha256",
        Path("/generation-evidence/usage.json"): "generation_usage_sha256",
        Path("/generation-evidence/codex-last.txt"): "generation_codex_last_sha256",
        Path("/generation-evidence/codex-output.log"): "generation_codex_output_sha256",
        Path("/generation-evidence/prompt.txt"): "generation_prompt_sha256",
        Path("/reference/canonical.py"): "canonical_sha256",
        Path("/reference/prompt.py"): "trusted_prompt_sha256",
        Path("/reference/py2mpy.py"): "trusted_translator_sha256",
        Path("/candidate/prompt.py"): "candidate_prompt_sha256",
        Path("/candidate/py2mpy.py"): "candidate_translator_sha256",
    }
    for path, key in recorded_file_hashes.items():
        require_regular(path)
        actual = sha256(path)
        expected = audit["hashes"][key]
        print(f"HASH {path} {actual} recorded={expected} match={actual == expected}")
        assert actual == expected, f"hash mismatch for {path}"

    result = json.loads(Path("/generation-result.json").read_text())
    invocation = json.loads(Path("/generation-evidence/invocation.json").read_text())
    output_hashes = result["outputs"]["evidence"]
    assert output_hashes == invocation["outputs"]["evidence"]
    for relative, expected in sorted(output_hashes.items()):
        path = Path("/generation-evidence") / relative
        require_regular(path)
        actual = sha256(path)
        print(
            f"GENERATION_RECORD {relative} {actual} "
            f"recorded={expected} match={actual == expected}"
        )
        assert actual == expected, f"generation output hash mismatch for {path}"

    prompt_equal = Path("/candidate/prompt.py").read_bytes() == Path(
        "/reference/prompt.py"
    ).read_bytes()
    translator_equal = Path("/candidate/py2mpy.py").read_bytes() == Path(
        "/reference/py2mpy.py"
    ).read_bytes()
    print(f"PROMPT_BYTE_IDENTITY {prompt_equal}")
    print(f"TRANSLATOR_BYTE_IDENTITY {translator_equal}")
    assert prompt_equal and translator_equal

    semantics_equal, semantics_problems = compare_trees(
        Path("/candidate/reference-semantics"),
        Path("/reference/reference-semantics"),
    )
    print(f"REFERENCE_SEMANTICS_ENTRY_IDENTITY {semantics_equal}")
    for problem in semantics_problems:
        print(f"REFERENCE_SEMANTICS_PROBLEM {problem}")
    assert semantics_equal

    for artifact in (
        "solution.py",
        "solution.mpy",
        "verification.k",
        "spec.k",
        "prove.sh",
    ):
        require_regular(Path("/candidate") / artifact)

    candidate_manifest = tree_manifest(Path("/candidate"))
    trusted_semantics_manifest = tree_manifest(Path("/reference/reference-semantics"))
    trace_manifest = tree_manifest(Path("/generation-evidence/codex-trace"))
    print(
        "INDEPENDENT_MANIFEST_HASH candidate "
        f"{manifest_hash(candidate_manifest)} entries={len(candidate_manifest)}"
    )
    print(
        "INDEPENDENT_MANIFEST_HASH trusted_semantics "
        f"{manifest_hash(trusted_semantics_manifest)} "
        f"entries={len(trusted_semantics_manifest)}"
    )
    print(
        "INDEPENDENT_MANIFEST_HASH generation_trace "
        f"{manifest_hash(trace_manifest)} entries={len(trace_manifest)}"
    )
    print("STAGE1_INTEGRITY_OK")


if __name__ == "__main__":
    main()
