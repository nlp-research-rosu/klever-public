#!/usr/bin/env python3
"""Independent integrity checks for the mounted audit inputs."""

from __future__ import annotations

import hashlib
import json
import os
import stat
import sys
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def sha256_tree(root: Path) -> str:
    """Hash type, relative path, size, and bytes for every tree entry."""
    root_mode = root.lstat().st_mode
    if not stat.S_ISDIR(root_mode):
        raise RuntimeError(f"tree root is not a real directory: {root}")
    entries: list[tuple[str, str, Path]] = []
    pending = [root]
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
                raise RuntimeError(f"linked or unsupported tree entry: {child_path}")
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
                for block in iter(lambda: stream.read(1024 * 1024), b""):
                    digest.update(block)
    return digest.hexdigest()


def require_regular(path: Path) -> None:
    mode = path.lstat().st_mode
    if not stat.S_ISREG(mode):
        raise RuntimeError(f"not a real regular file: {path}")


def require_directory(path: Path) -> None:
    mode = path.lstat().st_mode
    if not stat.S_ISDIR(mode):
        raise RuntimeError(f"not a real directory: {path}")


def compare_tree(left: Path, right: Path) -> list[str]:
    def inventory(root: Path) -> dict[str, tuple[str, bytes | None]]:
        result: dict[str, tuple[str, bytes | None]] = {}
        for path in sorted(root.rglob("*")):
            relative = path.relative_to(root).as_posix()
            mode = path.lstat().st_mode
            if stat.S_ISDIR(mode):
                result[relative] = ("directory", None)
            elif stat.S_ISREG(mode):
                result[relative] = ("file", path.read_bytes())
            else:
                result[relative] = ("unsupported", None)
        return result

    lhs = inventory(left)
    rhs = inventory(right)
    problems: list[str] = []
    for name in sorted(lhs.keys() | rhs.keys()):
        if name not in lhs:
            problems.append(f"candidate-only: {name}")
        elif name not in rhs:
            problems.append(f"trusted-only: {name}")
        elif lhs[name][0] != rhs[name][0]:
            problems.append(f"type differs: {name}: {lhs[name][0]} != {rhs[name][0]}")
        elif lhs[name][1] != rhs[name][1]:
            problems.append(f"bytes differ: {name}")
    return problems


def report_check(label: str, actual: object, expected: object) -> bool:
    okay = actual == expected
    print(f"{label}: {'OK' if okay else 'MISMATCH'}")
    print(f"  actual:   {actual}")
    print(f"  expected: {expected}")
    return okay


def report_bytes_equal(label: str, left: bytes, right: bytes) -> bool:
    okay = left == right
    print(f"{label}: {'OK' if okay else 'MISMATCH'}")
    print(f"  left_sha256:  {hashlib.sha256(left).hexdigest()}")
    print(f"  right_sha256: {hashlib.sha256(right).hexdigest()}")
    return okay


def main() -> int:
    audit = json.loads(AUDIT_INPUT.read_text())
    hashes = audit["hashes"]
    paths = audit["container_paths"]
    failures = 0

    required_files = [
        Path("/audit-input.json"),
        Path(paths["audit_campaign_lock"]),
        Path(paths["canonical"]),
        Path(paths["translator"]),
        Path(paths["trusted_prompt"]),
        Path(paths["run_manifest"]),
        Path(paths["task_manifest"]),
        Path(paths["stage1_result"]),
        Path(paths["generation_manifest"]),
        Path(paths["generation_metrics"]),
        Path("/generation-evidence/runtime-metrics.json"),
        Path("/generation-evidence/usage.json"),
        Path(paths["generation_last"]),
        Path(paths["generation_output"]),
        Path("/generation-evidence/prompt.txt"),
    ]
    required_directories = [
        Path(paths["candidate"]),
        Path(paths["generation_root"]),
        Path(paths["generation_trace"]),
        Path("/reference/reference-semantics"),
        Path("/candidate/reference-semantics"),
    ]
    print("REQUIRED PATH TYPES")
    for path in required_files:
        try:
            require_regular(path)
            print(f"OK regular {path}")
        except Exception as error:
            failures += 1
            print(f"FAIL {error}")
    for path in required_directories:
        try:
            require_directory(path)
            print(f"OK directory {path}")
        except Exception as error:
            failures += 1
            print(f"FAIL {error}")

    file_checks = {
        "audit_campaign_lock_sha256": Path(paths["audit_campaign_lock"]),
        "canonical_sha256": Path(paths["canonical"]),
        "trusted_prompt_sha256": Path(paths["trusted_prompt"]),
        "candidate_prompt_sha256": Path("/candidate/prompt.py"),
        "trusted_translator_sha256": Path(paths["translator"]),
        "candidate_translator_sha256": Path("/candidate/py2mpy.py"),
        "run_manifest_sha256": Path(paths["run_manifest"]),
        "task_manifest_sha256": Path(paths["task_manifest"]),
        "stage1_result_sha256": Path(paths["stage1_result"]),
        "stage1_invocation_sha256": Path(paths["generation_manifest"]),
        "generation_metrics_sha256": Path(paths["generation_metrics"]),
        "generation_runtime_metrics_sha256": Path(
            "/generation-evidence/runtime-metrics.json"
        ),
        "generation_usage_sha256": Path("/generation-evidence/usage.json"),
        "generation_codex_last_sha256": Path(paths["generation_last"]),
        "generation_codex_output_sha256": Path(paths["generation_output"]),
        "generation_prompt_sha256": Path("/generation-evidence/prompt.txt"),
    }
    print("\nRECORDED FILE HASHES")
    for key, path in file_checks.items():
        actual = sha256_file(path)
        if not report_check(key, actual, hashes[key]):
            failures += 1

    print("\nPIPELINE TREE HASHES")
    result = json.loads(Path(paths["stage1_result"]).read_text())
    task = json.loads(Path(paths["task_manifest"]).read_text())
    usage = json.loads(Path("/generation-evidence/usage.json").read_text())
    pipeline_tree_checks = [
        (
            "candidate tree vs generation workspace",
            sha256_tree(Path(paths["candidate"])),
            result["outputs"]["workspace_sha256"],
        ),
        (
            "candidate reference-semantics vs task input",
            sha256_tree(Path("/candidate/reference-semantics")),
            task["inputs"]["reference_semantics_sha256"],
        ),
        (
            "trusted reference-semantics vs task input",
            sha256_tree(Path("/reference/reference-semantics")),
            task["inputs"]["reference_semantics_sha256"],
        ),
        (
            "generation trace vs usage source trace",
            sha256_tree(Path(paths["generation_trace"])),
            usage["source_trace_sha256"],
        ),
    ]
    for label, actual, expected in pipeline_tree_checks:
        if not report_check(label, actual, expected):
            failures += 1

    print("\nLAUNCHER SNAPSHOT DIGEST RELATIONS")
    if not report_check(
        "candidate/trusted semantics snapshot digests agree",
        hashes["candidate_reference_semantics_sha256"],
        hashes["trusted_reference_semantics_sha256"],
    ):
        failures += 1
    print(
        "launcher candidate snapshot digest: "
        + hashes["candidate_tree_sha256"]
    )
    print(
        "launcher generation-trace snapshot digest: "
        + hashes["generation_codex_trace_sha256"]
    )

    print("\nCAMPAIGN LOCK")
    lock = json.loads(Path(paths["audit_campaign_lock"]).read_text())
    if not report_check("lock JSON equals audit_campaign block", lock, audit["audit_campaign"]):
        failures += 1

    print("\nCANDIDATE TRUSTED-INPUT COMPARISONS")
    comparisons = [
        (Path("/candidate/prompt.py"), Path(paths["trusted_prompt"])),
        (Path("/candidate/py2mpy.py"), Path(paths["translator"])),
    ]
    for left, right in comparisons:
        if not report_bytes_equal(
            f"{left} bytes equal {right}", left.read_bytes(), right.read_bytes()
        ):
            failures += 1
    semantic_problems = compare_tree(
        Path("/reference/reference-semantics"),
        Path("/candidate/reference-semantics"),
    )
    if semantic_problems:
        failures += len(semantic_problems)
        print("reference-semantics recursive comparison: MISMATCH")
        for problem in semantic_problems:
            print(f"  {problem}")
    else:
        print("reference-semantics recursive comparison: OK")

    print("\nGENERATION RESULT EVIDENCE HASHES")
    evidence_root = Path(paths["generation_root"])
    for relative, expected in sorted(result["outputs"]["evidence"].items()):
        path = evidence_root / relative
        try:
            require_regular(path)
            actual = sha256_file(path)
        except Exception as error:
            failures += 1
            print(f"{relative}: FAIL {error}")
            continue
        if not report_check(relative, actual, expected):
            failures += 1

    print(f"\nTOTAL_FAILURES={failures}")
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
