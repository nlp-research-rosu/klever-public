#!/usr/bin/env python3
"""Independent integrity checks for the mounted audit inputs."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from pathlib import Path


AUDIT = Path("/audit-input.json")
LOCK = Path("/audit-campaign-lock.json")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def pipeline_tree_hash(root: Path) -> str:
    """Reimplement the length-delimited pipeline-v3 tree digest."""
    root_stat = root.lstat()
    if not stat.S_ISDIR(root_stat.st_mode):
        raise RuntimeError(f"not a real directory: {root}")
    entries: list[tuple[str, str, Path]] = []
    pending = [root]
    while pending:
        directory = pending.pop()
        for entry in os.scandir(directory):
            mode = entry.stat(follow_symlinks=False).st_mode
            path = Path(entry.path)
            relative = path.relative_to(root).as_posix()
            if stat.S_ISDIR(mode):
                entries.append((relative, "directory", path))
                pending.append(path)
            elif stat.S_ISREG(mode):
                entries.append((relative, "file", path))
            else:
                raise RuntimeError(f"linked or unsupported tree entry: {path}")
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


def require_regular(path: Path) -> None:
    mode = path.lstat().st_mode
    if not stat.S_ISREG(mode):
        raise RuntimeError(f"required regular file has wrong type: {path}")
    with path.open("rb") as stream:
        stream.read(1)


def require_directory(path: Path) -> None:
    if not stat.S_ISDIR(path.lstat().st_mode):
        raise RuntimeError(f"required real directory has wrong type: {path}")


def compare_trees(left: Path, right: Path) -> None:
    def inventory(root: Path) -> dict[str, tuple[str, str | None]]:
        answer: dict[str, tuple[str, str | None]] = {}
        pending = [root]
        while pending:
            directory = pending.pop()
            for entry in os.scandir(directory):
                path = Path(entry.path)
                relative = path.relative_to(root).as_posix()
                mode = entry.stat(follow_symlinks=False).st_mode
                if stat.S_ISDIR(mode):
                    answer[relative] = ("directory", None)
                    pending.append(path)
                elif stat.S_ISREG(mode):
                    answer[relative] = ("file", sha256_file(path))
                else:
                    answer[relative] = ("unsupported", None)
        return answer

    left_inventory = inventory(left)
    right_inventory = inventory(right)
    if left_inventory != right_inventory:
        all_names = sorted(set(left_inventory) | set(right_inventory))
        differences = [
            (name, left_inventory.get(name), right_inventory.get(name))
            for name in all_names
            if left_inventory.get(name) != right_inventory.get(name)
        ]
        raise RuntimeError(f"tree mismatch: {differences}")


def main() -> None:
    audit = json.loads(AUDIT.read_text())
    lock = json.loads(LOCK.read_text())
    hashes = audit["hashes"]

    print(f"record_layout={audit['record_layout']}")
    print(f"semantics_mode={audit['semantics_mode']}")
    assert audit["record_layout"] == "legacy-selected-stage1"
    assert audit["semantics_mode"] == "SUPPLIED_SEMANTICS"
    assert audit["mount_reference_semantics"] is True
    assert audit["audit_campaign"] == lock
    assert sha256_file(LOCK) == hashes["audit_campaign_lock_sha256"]
    print("campaign_lock_block_and_hash=MATCH")

    required_files = [
        AUDIT,
        LOCK,
        Path("/run.json"),
        Path("/task.json"),
        Path("/generation-result.json"),
        Path("/reference/canonical.py"),
        Path("/reference/prompt.py"),
        Path("/reference/py2mpy.py"),
        Path("/generation-evidence/invocation.json"),
        Path("/generation-evidence/metrics.json"),
        Path("/generation-evidence/codex-last.txt"),
        Path("/generation-evidence/codex-output.log"),
        Path("/generation-evidence/prompt.txt"),
    ]
    # usage.json is optional for this legacy layout, but it is present and is
    # therefore inspected and hashed.
    optional_usage = Path("/generation-evidence/usage.json")
    if optional_usage.exists() or optional_usage.is_symlink():
        required_files.append(optional_usage)
    required_directories = [
        Path("/candidate"),
        Path("/reference/reference-semantics"),
        Path("/candidate/reference-semantics"),
        Path("/generation-evidence"),
        Path("/generation-evidence/codex-trace"),
    ]
    for path in required_files:
        require_regular(path)
    for path in required_directories:
        require_directory(path)
    print(f"required_regular_files={len(required_files)} OK")
    print(f"required_real_directories={len(required_directories)} OK")

    direct_hashes = {
        "/audit-campaign-lock.json": "audit_campaign_lock_sha256",
        "/reference/canonical.py": "canonical_sha256",
        "/reference/prompt.py": "trusted_prompt_sha256",
        "/reference/py2mpy.py": "trusted_translator_sha256",
        "/candidate/prompt.py": "candidate_prompt_sha256",
        "/candidate/py2mpy.py": "candidate_translator_sha256",
        "/run.json": "run_manifest_sha256",
        "/task.json": "task_manifest_sha256",
        "/generation-result.json": "stage1_result_sha256",
        "/generation-evidence/invocation.json": "stage1_invocation_sha256",
        "/generation-evidence/metrics.json": "generation_metrics_sha256",
        "/generation-evidence/codex-last.txt": "generation_codex_last_sha256",
        "/generation-evidence/codex-output.log": "generation_codex_output_sha256",
        "/generation-evidence/prompt.txt": "generation_prompt_sha256",
        "/generation-evidence/usage.json": "generation_usage_sha256",
    }
    for name, key in direct_hashes.items():
        actual = sha256_file(Path(name))
        expected = hashes[key]
        print(f"sha256 {name} actual={actual} expected={expected}")
        assert actual == expected
    print("all_launcher_direct_hashes=MATCH")

    assert Path("/candidate/prompt.py").read_bytes() == Path(
        "/reference/prompt.py"
    ).read_bytes()
    assert Path("/candidate/py2mpy.py").read_bytes() == Path(
        "/reference/py2mpy.py"
    ).read_bytes()
    compare_trees(
        Path("/candidate/reference-semantics"),
        Path("/reference/reference-semantics"),
    )
    print("candidate_prompt=MATCH_TRUSTED")
    print("candidate_translator=MATCH_TRUSTED")
    print("candidate_reference_semantics=MATCH_TRUSTED_RECURSIVELY")

    tree_hashes = {
        "trusted_reference": pipeline_tree_hash(
            Path("/reference/reference-semantics")
        ),
        "candidate_reference": pipeline_tree_hash(
            Path("/candidate/reference-semantics")
        ),
        "candidate": pipeline_tree_hash(Path("/candidate")),
        "generation_trace": pipeline_tree_hash(
            Path("/generation-evidence/codex-trace")
        ),
    }
    for name, value in tree_hashes.items():
        print(f"pipeline_tree_sha256 {name}={value}")
    assert (
        tree_hashes["trusted_reference"]
        == hashes["trusted_reference_semantics_manifest_sha256"]
    )
    invocation = json.loads(
        Path("/generation-evidence/invocation.json").read_text()
    )
    assert tree_hashes["candidate"] == invocation["retained_workspace_sha256"]
    usage = json.loads(Path("/generation-evidence/usage.json").read_text())
    assert tree_hashes["generation_trace"] == usage["source_trace_sha256"]
    print("algorithm_identified_tree_hashes=MATCH")

    result = json.loads(Path("/generation-result.json").read_text())
    evidence_root = Path("/generation-evidence")
    for relative, expected in result["outputs"]["evidence"].items():
        target = evidence_root / relative
        if target.is_dir():
            continue
        require_regular(target)
        actual = sha256_file(target)
        print(
            f"generation_result_evidence {relative} "
            f"actual={actual} expected={expected}"
        )
        assert actual == expected

    trace_files = sorted(
        path
        for path in Path("/generation-evidence/codex-trace").rglob("*")
        if path.is_file()
    )
    assert trace_files
    trace_lines = 0
    for path in trace_files:
        with path.open(encoding="utf-8") as stream:
            for line_number, line in enumerate(stream, 1):
                json.loads(line)
                trace_lines += 1
    print(f"structured_trace_files={len(trace_files)}")
    print(f"structured_trace_json_lines={trace_lines}")

    # Force a complete read of the textual generation log, not just a head or
    # tail sample.
    output_bytes = Path("/generation-evidence/codex-output.log").read_bytes()
    print(f"codex_output_bytes_read={len(output_bytes)}")
    print(
        "codex_output_contains_final_marker="
        + str(b"RESULT: KPROVE_PASSED" in output_bytes)
    )

    proof_artifacts = [
        "solution.py",
        "solution.mpy",
        "verification.k",
        "spec.k",
        "prove.sh",
    ]
    for name in proof_artifacts:
        require_regular(Path("/candidate") / name)
    print("required_candidate_proof_artifacts=OK")
    print("INTEGRITY_CHECK=PASS")


if __name__ == "__main__":
    main()
