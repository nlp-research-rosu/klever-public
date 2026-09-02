#!/usr/bin/env python3
"""Independent launcher/mount integrity checks for audit 14-all-prefixes."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")
LOCK = Path("/audit-campaign-lock.json")
CANDIDATE = Path("/candidate")
REFERENCE = Path("/reference")
GENERATION = Path("/generation-evidence")


def load_json(path: Path) -> object:
    with path.open("r", encoding="utf-8") as stream:
        return json.load(stream)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def contract_tree_hash(root: Path) -> str:
    """Reimplement the pipeline-v2 sha256_tree format independently."""
    if not stat.S_ISDIR(root.lstat().st_mode):
        raise AssertionError(f"not a real directory: {root}")
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
                raise AssertionError(f"linked/unsupported tree entry: {path}")
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


def assert_regular(path: Path) -> None:
    assert stat.S_ISREG(path.lstat().st_mode), f"not a regular file: {path}"


def assert_directory(path: Path) -> None:
    assert stat.S_ISDIR(path.lstat().st_mode), f"not a real directory: {path}"


def inventory(root: Path) -> dict[str, tuple[str, str | None]]:
    result: dict[str, tuple[str, str | None]] = {}
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root).as_posix()
        mode = path.lstat().st_mode
        if stat.S_ISREG(mode):
            result[relative] = ("file", sha256_file(path))
        elif stat.S_ISDIR(mode):
            result[relative] = ("directory", None)
        elif stat.S_ISLNK(mode):
            result[relative] = ("symlink", os.readlink(path))
        else:
            result[relative] = ("unsupported", None)
    return result


def check_hash(label: str, path: Path, expected: str) -> None:
    assert_regular(path)
    actual = sha256_file(path)
    print(f"{label}: expected={expected} actual={actual} match={actual == expected}")
    assert actual == expected


def main() -> None:
    audit = load_json(AUDIT_INPUT)
    lock = load_json(LOCK)
    assert isinstance(audit, dict) and isinstance(lock, dict)
    print(f"record_layout={audit['record_layout']}")
    print(f"semantics_mode={audit['semantics_mode']}")
    assert audit["record_layout"] == "legacy-selected-stage1"
    assert audit["semantics_mode"] == "SUPPLIED_SEMANTICS"

    print(f"campaign_block_equals_lock={audit['audit_campaign'] == lock}")
    assert audit["audit_campaign"] == lock
    check_hash(
        "audit_campaign_lock",
        LOCK,
        audit["hashes"]["audit_campaign_lock_sha256"],
    )

    required_files = [
        Path("/run.json"),
        Path("/task.json"),
        Path("/generation-result.json"),
        GENERATION / "invocation.json",
        GENERATION / "metrics.json",
        GENERATION / "usage.json",
        GENERATION / "codex-last.txt",
        GENERATION / "codex-output.log",
        GENERATION / "prompt.txt",
        REFERENCE / "canonical.py",
        REFERENCE / "prompt.py",
        REFERENCE / "py2mpy.py",
    ]
    required_dirs = [
        CANDIDATE,
        GENERATION,
        GENERATION / "codex-trace",
        REFERENCE / "reference-semantics",
        CANDIDATE / "reference-semantics",
    ]
    for path in required_files:
        assert_regular(path)
    for path in required_dirs:
        assert_directory(path)
    print(f"required_regular_files={len(required_files)} all_present=true")
    print(f"required_real_directories={len(required_dirs)} all_present=true")
    print("runtime-metrics.json absent=true required_for_layout=false")

    hashes = audit["hashes"]
    file_checks = [
        ("canonical", REFERENCE / "canonical.py", hashes["canonical_sha256"]),
        ("trusted_prompt", REFERENCE / "prompt.py", hashes["trusted_prompt_sha256"]),
        ("candidate_prompt", CANDIDATE / "prompt.py", hashes["candidate_prompt_sha256"]),
        (
            "trusted_translator",
            REFERENCE / "py2mpy.py",
            hashes["trusted_translator_sha256"],
        ),
        (
            "candidate_translator",
            CANDIDATE / "py2mpy.py",
            hashes["candidate_translator_sha256"],
        ),
        ("run_manifest", Path("/run.json"), hashes["run_manifest_sha256"]),
        ("task_manifest", Path("/task.json"), hashes["task_manifest_sha256"]),
        ("stage1_result", Path("/generation-result.json"), hashes["stage1_result_sha256"]),
        (
            "stage1_invocation",
            GENERATION / "invocation.json",
            hashes["stage1_invocation_sha256"],
        ),
        ("generation_metrics", GENERATION / "metrics.json", hashes["generation_metrics_sha256"]),
        ("generation_usage", GENERATION / "usage.json", hashes["generation_usage_sha256"]),
        (
            "generation_codex_last",
            GENERATION / "codex-last.txt",
            hashes["generation_codex_last_sha256"],
        ),
        (
            "generation_codex_output",
            GENERATION / "codex-output.log",
            hashes["generation_codex_output_sha256"],
        ),
        ("generation_prompt", GENERATION / "prompt.txt", hashes["generation_prompt_sha256"]),
    ]
    for label, path, expected in file_checks:
        check_hash(label, path, expected)

    result = load_json(Path("/generation-result.json"))
    assert isinstance(result, dict)
    for relative, expected in sorted(result["outputs"]["evidence"].items()):
        path = GENERATION / relative
        check_hash(f"generation-result:{relative}", path, expected)

    candidate_semantics = inventory(CANDIDATE / "reference-semantics")
    trusted_semantics = inventory(REFERENCE / "reference-semantics")
    print(f"candidate_semantics_entries={len(candidate_semantics)}")
    print(f"trusted_semantics_entries={len(trusted_semantics)}")
    print(f"semantic_inventories_identical={candidate_semantics == trusted_semantics}")
    assert candidate_semantics == trusted_semantics
    assert all(kind != "symlink" for kind, _ in candidate_semantics.values())

    prompt_equal = (CANDIDATE / "prompt.py").read_bytes() == (
        REFERENCE / "prompt.py"
    ).read_bytes()
    translator_equal = (CANDIDATE / "py2mpy.py").read_bytes() == (
        REFERENCE / "py2mpy.py"
    ).read_bytes()
    print(f"candidate_prompt_byte_equal={prompt_equal}")
    print(f"candidate_translator_byte_equal={translator_equal}")
    assert prompt_equal and translator_equal

    candidate_tree = contract_tree_hash(CANDIDATE)
    candidate_tree_expected = result["outputs"]["workspace_sha256"]
    semantics_tree = contract_tree_hash(REFERENCE / "reference-semantics")
    semantics_expected = hashes["trusted_reference_semantics_manifest_sha256"]
    trace_tree = contract_tree_hash(GENERATION / "codex-trace")
    usage = load_json(GENERATION / "usage.json")
    assert isinstance(usage, dict)
    trace_expected = usage["source_trace_sha256"]
    print(
        f"candidate_contract_tree: expected={candidate_tree_expected} "
        f"actual={candidate_tree} match={candidate_tree == candidate_tree_expected}"
    )
    print(
        f"trusted_semantics_contract_tree: expected={semantics_expected} "
        f"actual={semantics_tree} match={semantics_tree == semantics_expected}"
    )
    print(
        f"trace_contract_tree: expected={trace_expected} "
        f"actual={trace_tree} match={trace_tree == trace_expected}"
    )
    assert candidate_tree == candidate_tree_expected
    assert semantics_tree == semantics_expected
    assert trace_tree == trace_expected

    trace_files = sorted((GENERATION / "codex-trace").rglob("*.jsonl"))
    lines = 0
    for trace_file in trace_files:
        with trace_file.open("r", encoding="utf-8") as stream:
            for line_number, line in enumerate(stream, 1):
                json.loads(line)
                lines += 1
    print(f"trace_jsonl_files={len(trace_files)} parsed_lines={lines} malformed=0")
    print("PROVENANCE_CHECK=PASS")


if __name__ == "__main__":
    main()
