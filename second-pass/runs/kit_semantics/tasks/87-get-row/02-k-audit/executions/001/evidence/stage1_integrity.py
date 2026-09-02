#!/usr/bin/env python3
"""Independent integrity checks for the mounted audit inputs."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def require_regular(path: Path) -> None:
    mode = path.lstat().st_mode
    assert stat.S_ISREG(mode), f"not a regular file: {path}"
    assert not path.is_symlink(), f"symlinked file: {path}"


def require_tree_without_symlinks(root: Path) -> None:
    mode = root.lstat().st_mode
    assert stat.S_ISDIR(mode), f"not a directory: {root}"
    assert not root.is_symlink(), f"symlinked root: {root}"
    for current, dirs, files in os.walk(root, followlinks=False):
        for name in dirs + files:
            path = Path(current, name)
            mode = path.lstat().st_mode
            assert not stat.S_ISLNK(mode), f"symlink in tree: {path}"
            assert stat.S_ISDIR(mode) or stat.S_ISREG(mode), (
                f"unsupported entry type in tree: {path}"
            )


def tree_manifest(root: Path) -> tuple[list[str], str]:
    """Return a transparent reviewer-defined file manifest and its digest."""
    lines: list[str] = []
    for path in sorted(root.rglob("*")):
        rel = path.relative_to(root).as_posix()
        mode = path.lstat().st_mode
        if stat.S_ISDIR(mode):
            lines.append(f"d {rel}")
        elif stat.S_ISREG(mode):
            lines.append(f"f {rel} {digest(path)}")
        elif stat.S_ISLNK(mode):
            lines.append(f"l {rel} -> {os.readlink(path)}")
        else:
            lines.append(f"? {rel}")
    encoded = ("\n".join(lines) + "\n").encode()
    return lines, hashlib.sha256(encoded).hexdigest()


def compare_trees(left: Path, right: Path) -> list[str]:
    left_lines, _ = tree_manifest(left)
    right_lines, _ = tree_manifest(right)
    failures: list[str] = []
    left_entries = {line.split(" ", 2)[1]: line for line in left_lines}
    right_entries = {line.split(" ", 2)[1]: line for line in right_lines}
    for rel in sorted(left_entries.keys() | right_entries.keys()):
        if left_entries.get(rel) != right_entries.get(rel):
            failures.append(
                f"{rel}: candidate={left_entries.get(rel)!r}; "
                f"trusted={right_entries.get(rel)!r}"
            )
    return failures


def check_hash(label: str, path: Path, expected: str) -> None:
    require_regular(path)
    actual = digest(path)
    print(f"HASH {label}: {actual} expected={expected} match={actual == expected}")
    assert actual == expected, f"hash mismatch for {label}"


def main() -> None:
    require_regular(AUDIT_INPUT)
    audit = json.loads(AUDIT_INPUT.read_text())
    assert audit["record_layout"] == "pipeline-v3"
    assert audit["semantics_mode"] == "SUPPLIED_SEMANTICS"
    paths = audit["container_paths"]
    hashes = audit["hashes"]

    lock_path = Path(paths["audit_campaign_lock"])
    require_regular(lock_path)
    lock = json.loads(lock_path.read_text())
    assert lock == audit["audit_campaign"], "campaign lock fields differ"
    check_hash(
        "audit_campaign_lock",
        lock_path,
        hashes["audit_campaign_lock_sha256"],
    )
    print("CAMPAIGN_BLOCK_MATCH: true")

    required_regular = [
        Path("/run.json"),
        Path("/task.json"),
        Path("/generation-result.json"),
        Path("/generation-evidence/invocation.json"),
        Path("/generation-evidence/metrics.json"),
        Path("/generation-evidence/runtime-metrics.json"),
        Path("/generation-evidence/usage.json"),
        Path("/generation-evidence/codex-last.txt"),
        Path("/generation-evidence/codex-output.log"),
        Path("/generation-evidence/prompt.txt"),
        Path("/reference/canonical.py"),
        Path("/reference/prompt.py"),
        Path("/reference/py2mpy.py"),
    ]
    for path in required_regular:
        require_regular(path)
    require_tree_without_symlinks(Path("/generation-evidence/codex-trace"))
    require_tree_without_symlinks(Path("/candidate"))
    require_tree_without_symlinks(Path("/reference/reference-semantics"))
    print("REQUIRED_TYPES_AND_SYMLINK_CHECKS: true")

    recorded_files = {
        "run_manifest": (Path("/run.json"), hashes["run_manifest_sha256"]),
        "task_manifest": (Path("/task.json"), hashes["task_manifest_sha256"]),
        "stage1_result": (
            Path("/generation-result.json"),
            hashes["stage1_result_sha256"],
        ),
        "stage1_invocation": (
            Path("/generation-evidence/invocation.json"),
            hashes["stage1_invocation_sha256"],
        ),
        "generation_metrics": (
            Path("/generation-evidence/metrics.json"),
            hashes["generation_metrics_sha256"],
        ),
        "generation_runtime_metrics": (
            Path("/generation-evidence/runtime-metrics.json"),
            hashes["generation_runtime_metrics_sha256"],
        ),
        "generation_usage": (
            Path("/generation-evidence/usage.json"),
            hashes["generation_usage_sha256"],
        ),
        "generation_codex_last": (
            Path("/generation-evidence/codex-last.txt"),
            hashes["generation_codex_last_sha256"],
        ),
        "generation_codex_output": (
            Path("/generation-evidence/codex-output.log"),
            hashes["generation_codex_output_sha256"],
        ),
        "generation_prompt": (
            Path("/generation-evidence/prompt.txt"),
            hashes["generation_prompt_sha256"],
        ),
        "canonical": (
            Path("/reference/canonical.py"),
            hashes["canonical_sha256"],
        ),
        "trusted_prompt": (
            Path("/reference/prompt.py"),
            hashes["trusted_prompt_sha256"],
        ),
        "candidate_prompt": (
            Path("/candidate/prompt.py"),
            hashes["candidate_prompt_sha256"],
        ),
        "trusted_translator": (
            Path("/reference/py2mpy.py"),
            hashes["trusted_translator_sha256"],
        ),
        "candidate_translator": (
            Path("/candidate/py2mpy.py"),
            hashes["candidate_translator_sha256"],
        ),
    }
    for label, (path, expected) in recorded_files.items():
        check_hash(label, path, expected)

    result = json.loads(Path("/generation-result.json").read_text())
    for rel, expected in result["outputs"]["evidence"].items():
        check_hash(
            f"generation-result:{rel}",
            Path("/generation-evidence") / rel,
            expected,
        )

    assert Path("/candidate/prompt.py").read_bytes() == Path(
        "/reference/prompt.py"
    ).read_bytes()
    assert Path("/candidate/py2mpy.py").read_bytes() == Path(
        "/reference/py2mpy.py"
    ).read_bytes()
    print("PROMPT_AND_TRANSLATOR_BYTE_IDENTITY: true")

    candidate_semantics = Path("/candidate/reference-semantics")
    trusted_semantics = Path("/reference/reference-semantics")
    mismatches = compare_trees(candidate_semantics, trusted_semantics)
    print(f"SEMANTICS_TREE_MISMATCH_COUNT: {len(mismatches)}")
    for mismatch in mismatches:
        print(f"SEMANTICS_MISMATCH: {mismatch}")
    assert not mismatches

    candidate_lines, candidate_digest = tree_manifest(candidate_semantics)
    trusted_lines, trusted_digest = tree_manifest(trusted_semantics)
    print(f"SEMANTICS_ENTRY_COUNT: {len(candidate_lines)}")
    print(f"REVIEWER_CANDIDATE_SEMANTICS_TREE_SHA256: {candidate_digest}")
    print(f"REVIEWER_TRUSTED_SEMANTICS_TREE_SHA256: {trusted_digest}")
    assert candidate_digest == trusted_digest
    print("ALL_STAGE1_INTEGRITY_CHECKS_PASSED")


if __name__ == "__main__":
    main()
