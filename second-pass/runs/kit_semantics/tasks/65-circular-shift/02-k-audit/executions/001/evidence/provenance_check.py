#!/usr/bin/env python3
"""Independent provenance/type/hash checks for audit stage 1."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")
LOCK = Path("/audit-campaign-lock.json")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def require_regular(path: Path) -> None:
    info = path.lstat()
    assert stat.S_ISREG(info.st_mode), f"not a regular file: {path}"
    assert not path.is_symlink(), f"symlinked file: {path}"


def require_directory(path: Path) -> None:
    info = path.lstat()
    assert stat.S_ISDIR(info.st_mode), f"not a directory: {path}"
    assert not path.is_symlink(), f"symlinked directory: {path}"


def tree_entries(root: Path) -> dict[str, tuple[str, str | None]]:
    """Return every relative entry with its type and file digest."""
    require_directory(root)
    result: dict[str, tuple[str, str | None]] = {}
    pending = [root]
    while pending:
        directory = pending.pop()
        for entry in os.scandir(directory):
            path = Path(entry.path)
            relative = path.relative_to(root).as_posix()
            mode = entry.stat(follow_symlinks=False).st_mode
            if stat.S_ISDIR(mode):
                result[relative] = ("directory", None)
                pending.append(path)
            elif stat.S_ISREG(mode):
                result[relative] = ("file", sha256(path))
            elif stat.S_ISLNK(mode):
                result[relative] = ("symlink", None)
            else:
                result[relative] = ("unsupported", None)
    return dict(sorted(result.items()))


def check_hash(label: str, path: Path, expected: str) -> None:
    require_regular(path)
    actual = sha256(path)
    print(f"HASH {label}: expected={expected} actual={actual} match={actual == expected}")
    assert actual == expected


def main() -> None:
    require_regular(AUDIT_INPUT)
    require_regular(LOCK)
    audit = json.loads(AUDIT_INPUT.read_text())
    lock = json.loads(LOCK.read_text())

    print(f"record_layout={audit['record_layout']}")
    print(f"semantics_mode={audit['semantics_mode']}")
    assert audit["record_layout"] == "pipeline-v3"
    assert audit["semantics_mode"] == "SUPPLIED_SEMANTICS"
    assert audit["mount_reference_semantics"] is True

    print(f"campaign_block_equal={audit['audit_campaign'] == lock}")
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
        Path("/candidate/prompt.py"),
        Path("/candidate/py2mpy.py"),
        Path("/candidate/solution.py"),
        Path("/candidate/solution.mpy"),
        Path("/candidate/verification.k"),
        Path("/candidate/spec.k"),
    ]
    required_directories = [
        Path("/candidate"),
        Path("/generation-evidence"),
        Path("/generation-evidence/codex-trace"),
        Path("/reference/reference-semantics"),
        Path("/candidate/reference-semantics"),
    ]
    for path in required_files:
        require_regular(path)
        print(f"REQUIRED regular {path}")
    for path in required_directories:
        require_directory(path)
        print(f"REQUIRED directory {path}")

    hashes = audit["hashes"]
    file_hash_checks = {
        "canonical_sha256": Path("/reference/canonical.py"),
        "trusted_prompt_sha256": Path("/reference/prompt.py"),
        "trusted_translator_sha256": Path("/reference/py2mpy.py"),
        "candidate_prompt_sha256": Path("/candidate/prompt.py"),
        "candidate_translator_sha256": Path("/candidate/py2mpy.py"),
        "run_manifest_sha256": Path("/run.json"),
        "task_manifest_sha256": Path("/task.json"),
        "stage1_result_sha256": Path("/generation-result.json"),
        "stage1_invocation_sha256": Path("/generation-evidence/invocation.json"),
        "generation_metrics_sha256": Path("/generation-evidence/metrics.json"),
        "generation_runtime_metrics_sha256": Path(
            "/generation-evidence/runtime-metrics.json"
        ),
        "generation_usage_sha256": Path("/generation-evidence/usage.json"),
        "generation_codex_last_sha256": Path(
            "/generation-evidence/codex-last.txt"
        ),
        "generation_codex_output_sha256": Path(
            "/generation-evidence/codex-output.log"
        ),
        "generation_prompt_sha256": Path("/generation-evidence/prompt.txt"),
    }
    for key, path in file_hash_checks.items():
        check_hash(key, path, hashes[key])

    result = json.loads(Path("/generation-result.json").read_text())
    generation_outputs = result["outputs"]["evidence"]
    trace_root = Path("/generation-evidence/codex-trace")
    trace_entries = tree_entries(trace_root)
    assert all(
        kind in {"file", "directory"} for kind, _digest in trace_entries.values()
    ), "structured trace contains a symlink or unsupported entry"
    declared_trace_paths = {
        key: value
        for key, value in generation_outputs.items()
        if key.startswith("codex-trace/")
    }
    assert declared_trace_paths, "generation result declares no structured trace"
    actual_trace_files = sorted(
        path.relative_to(Path("/generation-evidence")).as_posix()
        for path in trace_root.rglob("*")
        if path.is_file() and not path.is_symlink()
    )
    print(f"declared_trace_files={sorted(declared_trace_paths)}")
    print(f"actual_trace_files={actual_trace_files}")
    assert sorted(declared_trace_paths) == actual_trace_files
    for relative, expected in declared_trace_paths.items():
        check_hash(relative, Path("/generation-evidence") / relative, expected)

    direct_output_map = {
        "codex-last.txt": Path("/generation-evidence/codex-last.txt"),
        "codex-output.log": Path("/generation-evidence/codex-output.log"),
        "prompt.txt": Path("/generation-evidence/prompt.txt"),
        "runtime-metrics.json": Path("/generation-evidence/runtime-metrics.json"),
        "usage.json": Path("/generation-evidence/usage.json"),
    }
    for name, path in direct_output_map.items():
        check_hash(f"generation-result:{name}", path, generation_outputs[name])

    for candidate, trusted, label in [
        (Path("/candidate/prompt.py"), Path("/reference/prompt.py"), "prompt"),
        (
            Path("/candidate/py2mpy.py"),
            Path("/reference/py2mpy.py"),
            "translator",
        ),
    ]:
        require_regular(candidate)
        require_regular(trusted)
        equal = candidate.read_bytes() == trusted.read_bytes()
        print(f"BYTE_IDENTITY {label}: {equal}")
        assert equal

    candidate_semantics = tree_entries(Path("/candidate/reference-semantics"))
    trusted_semantics = tree_entries(Path("/reference/reference-semantics"))
    print(f"candidate_semantics_entries={len(candidate_semantics)}")
    print(f"trusted_semantics_entries={len(trusted_semantics)}")
    print(f"semantics_trees_identical={candidate_semantics == trusted_semantics}")
    assert candidate_semantics == trusted_semantics
    assert all(
        kind in {"file", "directory"}
        for kind, _digest in candidate_semantics.values()
    )
    for relative, (kind, digest) in trusted_semantics.items():
        if kind == "file":
            print(f"SEMANTICS_FILE {relative} sha256={digest}")

    integrity = audit["integrity"]
    expected_integrity = {
        "candidate_prompt_matches_trusted": True,
        "candidate_reference_semantics_matches_trusted": True,
        "candidate_translator_matches_trusted": True,
        "manifest_prompt_hash_matches_trusted": True,
        "manifest_reference_semantics_hash_matches_trusted": True,
        "manifest_translator_hash_matches_trusted": True,
    }
    print(f"integrity_fields={json.dumps(integrity, sort_keys=True)}")
    assert integrity == expected_integrity

    print("PROVENANCE_CHECK: PASS")


if __name__ == "__main__":
    main()
