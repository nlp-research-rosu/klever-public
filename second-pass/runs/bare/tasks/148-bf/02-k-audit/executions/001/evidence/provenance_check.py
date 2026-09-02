#!/usr/bin/env python3
"""Independent launcher/mount integrity checks for audit 148-bf."""

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
    """Reimplement pipeline_contract.sha256_tree without importing launcher code."""
    digest = hashlib.sha256()
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
                raise RuntimeError(f"linked or unsupported tree entry: {path}")
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


def require_file(path: Path) -> None:
    mode = path.lstat().st_mode
    assert stat.S_ISREG(mode), f"not a regular file: {path}"


def require_directory(path: Path) -> None:
    mode = path.lstat().st_mode
    assert stat.S_ISDIR(mode), f"not a real directory: {path}"


def check_hash(label: str, path: Path, expected: str) -> None:
    actual = sha256_file(path)
    print(f"{label}: expected={expected} actual={actual} match={actual == expected}")
    assert actual == expected


def main() -> None:
    require_file(AUDIT_INPUT)
    audit = json.loads(AUDIT_INPUT.read_text())
    assert audit["record_layout"] == "pipeline-v3"
    assert audit["semantics_mode"] == "GENERATED_SEMANTICS"
    print("record_layout=pipeline-v3")
    print("semantics_mode=GENERATED_SEMANTICS")

    paths = audit["container_paths"]
    required_files = [
        Path("/audit-campaign-lock.json"),
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
    for path in required_files:
        require_file(path)
    require_directory(Path(paths["candidate"]))
    require_directory(Path(paths["generation_root"]))
    require_directory(Path(paths["generation_trace"]))
    print(f"required regular files present={len(required_files)}")
    print("candidate, generation root, and trace are real directories")

    lock = json.loads(Path("/audit-campaign-lock.json").read_text())
    assert lock == audit["audit_campaign"]
    print("campaign lock JSON exactly equals audit_campaign block")

    hashes = audit["hashes"]
    direct = {
        "audit_campaign_lock_sha256": Path("/audit-campaign-lock.json"),
        "canonical_sha256": Path(paths["canonical"]),
        "trusted_prompt_sha256": Path(paths["trusted_prompt"]),
        "trusted_translator_sha256": Path(paths["translator"]),
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
    for label, path in direct.items():
        check_hash(label, path, hashes[label])

    check_hash(
        "candidate_prompt_sha256",
        Path("/candidate/prompt.py"),
        hashes["candidate_prompt_sha256"],
    )
    check_hash(
        "candidate_translator_sha256",
        Path("/candidate/py2mpy.py"),
        hashes["candidate_translator_sha256"],
    )
    assert Path("/candidate/prompt.py").read_bytes() == Path(
        paths["trusted_prompt"]
    ).read_bytes()
    assert Path("/candidate/py2mpy.py").read_bytes() == Path(
        paths["translator"]
    ).read_bytes()
    print("candidate prompt and translator are byte-identical to trusted mounts")

    assert not Path("/reference/reference-semantics").exists()
    assert not Path("/candidate/reference-semantics").exists()
    print("generated-semantics boundary satisfied: no trusted or candidate reference tree")

    result = json.loads(Path(paths["stage1_result"]).read_text())
    invocation = json.loads(Path(paths["generation_manifest"]).read_text())
    expected_evidence = result["outputs"]["evidence"]
    assert expected_evidence == invocation["outputs"]["evidence"]
    for relative, expected in sorted(expected_evidence.items()):
        check_hash(
            f"stage1 evidence {relative}",
            Path(paths["generation_root"]) / relative,
            expected,
        )
    assert result["outputs"]["workspace_sha256"] == invocation["outputs"][
        "workspace_sha256"
    ]

    candidate_tree = sha256_tree(Path(paths["candidate"]))
    trace_tree = sha256_tree(Path(paths["generation_trace"]))
    print(f"candidate tree independent digest={candidate_tree}")
    print(f"generation trace independent digest={trace_tree}")
    print(
        "candidate tree matches stage1 workspace="
        f"{candidate_tree == result['outputs']['workspace_sha256']}"
    )
    usage = json.loads(Path("/generation-evidence/usage.json").read_text())
    print(
        "trace tree matches usage source_trace_sha256="
        f"{trace_tree == usage['source_trace_sha256']}"
    )
    assert candidate_tree == result["outputs"]["workspace_sha256"]
    assert trace_tree == usage["source_trace_sha256"]

    # These aggregate audit-input fields are not pipeline tree digests. Preserve
    # them for comparison without treating the different encoding as corruption.
    print(f"audit-input candidate_tree_sha256={hashes['candidate_tree_sha256']}")
    print(
        "audit-input generation_codex_trace_sha256="
        f"{hashes['generation_codex_trace_sha256']}"
    )
    print("ALL REQUIRED PROVENANCE CHECKS PASSED")


if __name__ == "__main__":
    main()
