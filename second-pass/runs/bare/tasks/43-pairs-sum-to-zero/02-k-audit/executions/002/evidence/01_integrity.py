#!/usr/bin/env python3
"""Independent mount/type/hash checks for audit stage 1."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from pathlib import Path


AUDIT = Path("/audit-input.json")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_tree(root: Path) -> str:
    """Reimplement the launcher's length-delimited tree hash."""
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
                raise AssertionError(f"linked or unsupported entry: {path}")
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


def check_hash(label: str, path: Path, expected: str) -> None:
    require_regular(path)
    actual = sha256_file(path)
    print(f"{label}: expected={expected} actual={actual} match={actual == expected}")
    assert actual == expected


def main() -> None:
    doc = json.loads(AUDIT.read_text())
    assert doc["record_layout"] == "legacy-selected-stage1"
    assert doc["semantics_mode"] == "GENERATED_SEMANTICS"
    assert doc["mount_reference_semantics"] is False

    lock_path = Path(doc["container_paths"]["audit_campaign_lock"])
    require_regular(AUDIT)
    require_regular(lock_path)
    lock = json.loads(lock_path.read_text())
    print("campaign_block_equal:", lock == doc["audit_campaign"])
    assert lock == doc["audit_campaign"]

    hashes = doc["hashes"]
    checks = {
        "audit_campaign_lock_sha256": lock_path,
        "run_manifest_sha256": Path(doc["container_paths"]["run_manifest"]),
        "task_manifest_sha256": Path(doc["container_paths"]["task_manifest"]),
        "stage1_result_sha256": Path(doc["container_paths"]["stage1_result"]),
        "stage1_invocation_sha256": Path(doc["container_paths"]["generation_manifest"]),
        "generation_metrics_sha256": Path(doc["container_paths"]["generation_metrics"]),
        "generation_usage_sha256": Path("/generation-evidence/usage.json"),
        "generation_codex_last_sha256": Path(doc["container_paths"]["generation_last"]),
        "generation_codex_output_sha256": Path(doc["container_paths"]["generation_output"]),
        "generation_prompt_sha256": Path("/generation-evidence/prompt.txt"),
        "canonical_sha256": Path(doc["container_paths"]["canonical"]),
        "trusted_prompt_sha256": Path(doc["container_paths"]["trusted_prompt"]),
        "trusted_translator_sha256": Path(doc["container_paths"]["translator"]),
        "candidate_prompt_sha256": Path("/candidate/prompt.py"),
        "candidate_translator_sha256": Path("/candidate/py2mpy.py"),
    }
    for label, path in checks.items():
        check_hash(label, path, hashes[label])

    candidate = Path(doc["container_paths"]["candidate"])
    generation_root = Path(doc["container_paths"]["generation_root"])
    generation_trace = Path(doc["container_paths"]["generation_trace"])
    reference = Path("/reference")
    for directory in (candidate, generation_root, generation_trace, reference):
        require_directory(directory)

    candidate_tree = sha256_tree(candidate)
    trace_tree = sha256_tree(generation_trace)
    invocation_record = json.loads(
        Path("/generation-evidence/invocation.json").read_text()
    )
    usage_record = json.loads(Path("/generation-evidence/usage.json").read_text())
    candidate_pipeline_expected = invocation_record["retained_workspace_sha256"]
    trace_pipeline_expected = usage_record["source_trace_sha256"]
    print(
        "candidate_pipeline_tree_sha256:",
        f"expected={candidate_pipeline_expected}",
        f"actual={candidate_tree}",
        f"match={candidate_tree == candidate_pipeline_expected}",
    )
    print(
        "generation_trace_pipeline_tree_sha256:",
        f"expected={trace_pipeline_expected}",
        f"actual={trace_tree}",
        f"match={trace_tree == trace_pipeline_expected}",
    )
    print(
        "audit_input_candidate_tree_digest_record:",
        hashes["candidate_tree_sha256"],
    )
    print(
        "audit_input_generation_trace_digest_record:",
        hashes["generation_codex_trace_sha256"],
    )
    assert candidate_tree == candidate_pipeline_expected
    assert trace_tree == trace_pipeline_expected

    expected_required = [
        "/run.json",
        "/task.json",
        "/generation-result.json",
        "/generation-evidence/invocation.json",
        "/generation-evidence/metrics.json",
        "/generation-evidence/codex-last.txt",
        "/generation-evidence/codex-output.log",
        "/generation-evidence/prompt.txt",
        "/generation-evidence/usage.json",
        "/reference/canonical.py",
        "/reference/prompt.py",
        "/reference/py2mpy.py",
        "/candidate/prompt.py",
        "/candidate/py2mpy.py",
    ]
    for item in expected_required:
        require_regular(Path(item))
    assert not Path("/reference/reference-semantics").exists()
    assert not Path("/reference/reference-semantics").is_symlink()

    assert Path("/candidate/prompt.py").read_bytes() == Path(
        "/reference/prompt.py"
    ).read_bytes()
    assert Path("/candidate/py2mpy.py").read_bytes() == Path(
        "/reference/py2mpy.py"
    ).read_bytes()
    print("candidate_prompt_byte_identity: true")
    print("candidate_translator_byte_identity: true")
    print("trusted_reference_semantics_absent: true")

    result = json.loads(Path("/generation-result.json").read_text())
    invocation = json.loads(Path("/generation-evidence/invocation.json").read_text())
    evidence_hashes = result["outputs"]["evidence"]
    assert evidence_hashes == invocation["outputs"]["evidence"]
    for relative, expected in sorted(evidence_hashes.items()):
        check_hash(
            f"generation-result.outputs.evidence[{relative}]",
            Path("/generation-evidence") / relative,
            expected,
        )

    for root in (candidate, generation_root, reference):
        for path in root.rglob("*"):
            mode = path.lstat().st_mode
            assert stat.S_ISREG(mode) or stat.S_ISDIR(mode), (
                f"symlinked or mistyped artifact: {path}"
            )

    print("candidate_files:")
    for path in sorted(candidate.rglob("*")):
        if path.is_file():
            print(
                f"  {path.relative_to(candidate).as_posix()} "
                f"{path.stat().st_size} {sha256_file(path)}"
            )
    print("INTEGRITY_CHECKS: PASS")


if __name__ == "__main__":
    main()
