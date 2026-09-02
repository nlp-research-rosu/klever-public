#!/usr/bin/env python3
"""Independently verify mounted pipeline-v3 provenance and supplied semantics."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")
CAMPAIGN_LOCK = Path("/audit-campaign-lock.json")
CANDIDATE = Path("/candidate")
REFERENCE = Path("/reference")
GENERATION = Path("/generation-evidence")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_tree(root: Path) -> str:
    """Reimplement the pipeline-v3 path/kind/size/content tree digest."""
    root = root.resolve(strict=True)
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
                raise AssertionError(f"linked or unsupported tree entry: {path}")
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
    assert stat.S_ISREG(mode), f"not a real regular file: {path}"


def require_directory(path: Path) -> None:
    mode = path.lstat().st_mode
    assert stat.S_ISDIR(mode), f"not a real directory: {path}"


def compare_trees(left: Path, right: Path) -> list[str]:
    def inventory(root: Path) -> dict[str, tuple[str, str | None]]:
        result: dict[str, tuple[str, str | None]] = {}
        for path in sorted(root.rglob("*")):
            relative = path.relative_to(root).as_posix()
            mode = path.lstat().st_mode
            if stat.S_ISDIR(mode):
                result[relative] = ("directory", None)
            elif stat.S_ISREG(mode):
                result[relative] = ("file", sha256_file(path))
            elif stat.S_ISLNK(mode):
                result[relative] = ("symlink", os.readlink(path))
            else:
                result[relative] = ("unsupported", None)
        return result

    li = inventory(left)
    ri = inventory(right)
    differences = []
    for name in sorted(set(li) | set(ri)):
        if li.get(name) != ri.get(name):
            differences.append(f"{name}: candidate={li.get(name)} trusted={ri.get(name)}")
    return differences


def main() -> None:
    require_regular(AUDIT_INPUT)
    require_regular(CAMPAIGN_LOCK)
    audit = json.loads(AUDIT_INPUT.read_text())
    lock = json.loads(CAMPAIGN_LOCK.read_text())

    print(f"record_layout={audit['record_layout']}")
    print(f"semantics_mode={audit['semantics_mode']}")
    assert audit["record_layout"] == "pipeline-v3"
    assert audit["semantics_mode"] == "SUPPLIED_SEMANTICS"
    assert audit["mount_reference_semantics"] is True

    lock_hash = sha256_file(CAMPAIGN_LOCK)
    print(f"audit_campaign_lock_sha256={lock_hash}")
    assert lock_hash == audit["hashes"]["audit_campaign_lock_sha256"]
    assert lock == audit["audit_campaign"]
    print("campaign_lock_matches_audit_campaign=true")

    required_files = [
        Path("/run.json"),
        Path("/task.json"),
        Path("/generation-result.json"),
        GENERATION / "invocation.json",
        GENERATION / "metrics.json",
        GENERATION / "runtime-metrics.json",
        GENERATION / "usage.json",
        GENERATION / "codex-last.txt",
        GENERATION / "codex-output.log",
        GENERATION / "prompt.txt",
        REFERENCE / "canonical.py",
        REFERENCE / "prompt.py",
        REFERENCE / "py2mpy.py",
    ]
    for path in required_files:
        require_regular(path)
    require_directory(GENERATION / "codex-trace")
    require_directory(CANDIDATE)
    require_directory(REFERENCE / "reference-semantics")
    require_directory(CANDIDATE / "reference-semantics")

    trace_files = sorted((GENERATION / "codex-trace").rglob("*"))
    trace_files = [path for path in trace_files if path.is_file()]
    assert trace_files, "structured trace contains no files"
    for path in trace_files:
        require_regular(path)

    direct_hash_checks = {
        "/run.json": "run_manifest_sha256",
        "/task.json": "task_manifest_sha256",
        "/generation-result.json": "stage1_result_sha256",
        "/generation-evidence/invocation.json": "stage1_invocation_sha256",
        "/generation-evidence/metrics.json": "generation_metrics_sha256",
        "/generation-evidence/runtime-metrics.json": "generation_runtime_metrics_sha256",
        "/generation-evidence/usage.json": "generation_usage_sha256",
        "/generation-evidence/codex-last.txt": "generation_codex_last_sha256",
        "/generation-evidence/codex-output.log": "generation_codex_output_sha256",
        "/generation-evidence/prompt.txt": "generation_prompt_sha256",
        "/reference/canonical.py": "canonical_sha256",
        "/reference/prompt.py": "trusted_prompt_sha256",
        "/reference/py2mpy.py": "trusted_translator_sha256",
        "/candidate/prompt.py": "candidate_prompt_sha256",
        "/candidate/py2mpy.py": "candidate_translator_sha256",
    }
    for raw_path, key in direct_hash_checks.items():
        path = Path(raw_path)
        require_regular(path)
        actual = sha256_file(path)
        expected = audit["hashes"][key]
        print(f"{key}: actual={actual} expected={expected} match={actual == expected}")
        assert actual == expected

    invocation = json.loads((GENERATION / "invocation.json").read_text())
    result = json.loads(Path("/generation-result.json").read_text())
    for relative, expected in sorted(result["outputs"]["evidence"].items()):
        path = GENERATION / relative
        require_regular(path)
        actual = sha256_file(path)
        print(f"generation_result[{relative}]: actual={actual} expected={expected} match={actual == expected}")
        assert actual == expected
        assert invocation["outputs"]["evidence"][relative] == expected

    candidate_tree = sha256_tree(CANDIDATE)
    trace_tree = sha256_tree(GENERATION / "codex-trace")
    candidate_semantics_tree = sha256_tree(CANDIDATE / "reference-semantics")
    trusted_semantics_tree = sha256_tree(REFERENCE / "reference-semantics")
    print(f"candidate_tree_pipeline_digest={candidate_tree}")
    print(f"generation_result_workspace_sha256={result['outputs']['workspace_sha256']}")
    print(f"trace_tree_pipeline_digest={trace_tree}")
    print(f"usage_source_trace_sha256={json.loads((GENERATION / 'usage.json').read_text())['source_trace_sha256']}")
    print(f"candidate_semantics_tree_pipeline_digest={candidate_semantics_tree}")
    print(f"trusted_semantics_tree_pipeline_digest={trusted_semantics_tree}")
    assert candidate_tree == result["outputs"]["workspace_sha256"]
    assert candidate_tree == invocation["outputs"]["workspace_sha256"]
    assert trace_tree == json.loads((GENERATION / "usage.json").read_text())["source_trace_sha256"]
    assert candidate_semantics_tree == trusted_semantics_tree
    assert candidate_semantics_tree == audit["hashes"]["trusted_reference_semantics_manifest_sha256"]
    assert candidate_semantics_tree == audit["manifest"]["inputs"]["reference_semantics_sha256"]

    assert (CANDIDATE / "prompt.py").read_bytes() == (REFERENCE / "prompt.py").read_bytes()
    assert (CANDIDATE / "py2mpy.py").read_bytes() == (REFERENCE / "py2mpy.py").read_bytes()
    semantics_differences = compare_trees(
        CANDIDATE / "reference-semantics",
        REFERENCE / "reference-semantics",
    )
    print(f"semantics_recursive_difference_count={len(semantics_differences)}")
    for difference in semantics_differences:
        print(difference)
    assert not semantics_differences

    proof_files = [
        "solution.py",
        "solution.mpy",
        "verification.k",
        "spec.k",
        "prove.sh",
        "PROOF.md",
    ]
    for relative in proof_files:
        require_regular(CANDIDATE / relative)
    print("required_candidate_proof_artifacts_are_regular=true")
    print("PROVENANCE_INTEGRITY=PASS")


if __name__ == "__main__":
    main()
