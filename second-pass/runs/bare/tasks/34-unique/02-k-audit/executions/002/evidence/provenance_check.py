#!/usr/bin/env python3
"""Independent Stage-1 integrity checks over the mounted audit inputs."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import stat
import sys


AUDIT_INPUT = Path("/audit-input.json")
CAMPAIGN_LOCK = Path("/audit-campaign-lock.json")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def require_regular(path: Path) -> None:
    mode = path.lstat().st_mode
    if not stat.S_ISREG(mode):
        raise AssertionError(f"not a real regular file: {path}")
    print(f"REGULAR_FILE {path}")


def require_directory_tree(path: Path) -> None:
    if not stat.S_ISDIR(path.lstat().st_mode):
        raise AssertionError(f"not a real directory: {path}")
    for root, directories, files in os.walk(path, followlinks=False):
        root_path = Path(root)
        for name in directories:
            child = root_path / name
            if not stat.S_ISDIR(child.lstat().st_mode):
                raise AssertionError(f"linked/unsupported directory: {child}")
        for name in files:
            child = root_path / name
            if not stat.S_ISREG(child.lstat().st_mode):
                raise AssertionError(f"linked/unsupported file: {child}")
    print(f"REAL_DIRECTORY_TREE {path}")


def pipeline_tree_hash(path: Path) -> str:
    """Reimplement the recorded pipeline-v2 tree digest independently."""
    entries: list[tuple[str, str, Path]] = []
    pending = [path]
    while pending:
        directory = pending.pop()
        for child in os.scandir(directory):
            child_path = Path(child.path)
            mode = child.stat(follow_symlinks=False).st_mode
            relative = child_path.relative_to(path).as_posix()
            if stat.S_ISDIR(mode):
                entries.append((relative, "directory", child_path))
                pending.append(child_path)
            elif stat.S_ISREG(mode):
                entries.append((relative, "file", child_path))
            else:
                raise AssertionError(f"linked/unsupported tree entry: {child_path}")
    digest = hashlib.sha256()
    for relative, kind, child_path in sorted(entries):
        encoded = relative.encode()
        digest.update(len(encoded).to_bytes(4, "big"))
        digest.update(encoded)
        digest.update(kind.encode() + b"\0")
        if kind == "file":
            size = child_path.stat(follow_symlinks=False).st_size
            digest.update(size.to_bytes(8, "big"))
            with child_path.open("rb") as stream:
                for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                    digest.update(chunk)
    return digest.hexdigest()


def check_hash(label: str, path: Path, expected: str) -> None:
    actual = sha256_file(path)
    print(f"SHA256 {label} actual={actual} expected={expected}")
    if actual != expected:
        raise AssertionError(f"hash mismatch for {label}")


def main() -> int:
    require_regular(AUDIT_INPUT)
    require_regular(CAMPAIGN_LOCK)
    audit = json.loads(AUDIT_INPUT.read_text(encoding="utf-8"))
    campaign = json.loads(CAMPAIGN_LOCK.read_text(encoding="utf-8"))

    assert audit["record_layout"] == "legacy-selected-stage1"
    assert audit["semantics_mode"] == "GENERATED_SEMANTICS"
    assert audit["mount_reference_semantics"] is False
    assert not Path("/reference/reference-semantics").exists()
    assert audit["audit_campaign"] == campaign
    print("CAMPAIGN_BLOCK_MATCH true")
    print("GENERATED_SEMANTICS_BOUNDARY true")

    required_files = [
        Path("/run.json"),
        Path("/task.json"),
        Path("/generation-result.json"),
        Path("/generation-evidence/invocation.json"),
        Path("/generation-evidence/metrics.json"),
        Path("/generation-evidence/codex-last.txt"),
        Path("/generation-evidence/codex-output.log"),
        Path("/generation-evidence/prompt.txt"),
        Path("/reference/canonical.py"),
        Path("/reference/prompt.py"),
        Path("/reference/py2mpy.py"),
    ]
    optional_usage = Path("/generation-evidence/usage.json")
    if optional_usage.exists():
        required_files.append(optional_usage)
    for path in required_files:
        require_regular(path)

    for path in (
        Path("/candidate"),
        Path("/generation-evidence"),
        Path("/generation-evidence/codex-trace"),
    ):
        require_directory_tree(path)

    for name in (
        "prompt.py",
        "py2mpy.py",
        "solution.py",
        "solution.mpy",
        "semantic.k",
        "verification.k",
        "spec.k",
        "prove.sh",
    ):
        require_regular(Path("/candidate") / name)

    assert Path("/candidate/prompt.py").read_bytes() == Path(
        "/reference/prompt.py"
    ).read_bytes()
    assert Path("/candidate/py2mpy.py").read_bytes() == Path(
        "/reference/py2mpy.py"
    ).read_bytes()
    print("CANDIDATE_PROMPT_BYTE_IDENTICAL true")
    print("CANDIDATE_TRANSLATOR_BYTE_IDENTICAL true")

    hashes = audit["hashes"]
    file_hashes = {
        "audit_campaign_lock_sha256": CAMPAIGN_LOCK,
        "candidate_prompt_sha256": Path("/candidate/prompt.py"),
        "candidate_translator_sha256": Path("/candidate/py2mpy.py"),
        "canonical_sha256": Path("/reference/canonical.py"),
        "generation_codex_last_sha256": Path(
            "/generation-evidence/codex-last.txt"
        ),
        "generation_codex_output_sha256": Path(
            "/generation-evidence/codex-output.log"
        ),
        "generation_metrics_sha256": Path("/generation-evidence/metrics.json"),
        "generation_prompt_sha256": Path("/generation-evidence/prompt.txt"),
        "manifest_sha256": Path("/task.json"),
        "run_manifest_sha256": Path("/run.json"),
        "stage1_invocation_sha256": Path(
            "/generation-evidence/invocation.json"
        ),
        "stage1_result_sha256": Path("/generation-result.json"),
        "task_manifest_sha256": Path("/task.json"),
        "trusted_prompt_sha256": Path("/reference/prompt.py"),
        "trusted_translator_sha256": Path("/reference/py2mpy.py"),
    }
    if optional_usage.exists():
        file_hashes["generation_usage_sha256"] = optional_usage
    for label, path in file_hashes.items():
        check_hash(label, path, hashes[label])

    result = json.loads(
        Path("/generation-result.json").read_text(encoding="utf-8")
    )
    invocation = json.loads(
        Path("/generation-evidence/invocation.json").read_text(encoding="utf-8")
    )
    for relative, expected in result["outputs"]["evidence"].items():
        check_hash(
            f"generation-result.outputs.evidence[{relative}]",
            Path("/generation-evidence") / relative,
            expected,
        )
    assert result["outputs"]["evidence"] == invocation["outputs"]["evidence"]
    print("RESULT_INVOCATION_EVIDENCE_MAP_MATCH true")

    candidate_hash = pipeline_tree_hash(Path("/candidate"))
    trace_hash = pipeline_tree_hash(Path("/generation-evidence/codex-trace"))
    print(f"PIPELINE_TREE_SHA256 candidate={candidate_hash}")
    print(f"PIPELINE_TREE_SHA256 trace={trace_hash}")
    print(
        "RECORDED_PIPELINE_TREE_SHA256 "
        f"candidate={result['outputs']['workspace_sha256']} "
        f"trace={json.loads(optional_usage.read_text())['source_trace_sha256']}"
    )
    assert candidate_hash == result["outputs"]["workspace_sha256"]
    assert candidate_hash == invocation["retained_workspace_sha256"]
    if optional_usage.exists():
        usage = json.loads(optional_usage.read_text(encoding="utf-8"))
        assert trace_hash == usage["source_trace_sha256"]
    print("PIPELINE_TREE_HASHES_MATCH true")

    # The launcher also records opaque publication-tree digests in audit-input.
    # Preserve them beside independently reproducible pipeline tree digests.
    print(
        "LAUNCHER_RECORDED_TREE_SHA256 "
        f"candidate={hashes['candidate_tree_sha256']} "
        f"trace={hashes['generation_codex_trace_sha256']}"
    )

    task = json.loads(Path("/task.json").read_text(encoding="utf-8"))
    manifest = audit["manifest"]
    for key, value in task.items():
        assert manifest[key] == value
    assert set(manifest) - set(task) == {"config"}
    assert manifest["config"] == audit["config"]
    assert task["inputs"]["problem_prompt_sha256"] == hashes[
        "trusted_prompt_sha256"
    ]
    assert task["inputs"]["translator_sha256"] == hashes[
        "trusted_translator_sha256"
    ]
    assert task["inputs"]["instruction_prompt_sha256"] == hashes[
        "generation_prompt_sha256"
    ]
    print("TASK_MANIFEST_AND_INPUT_HASH_LINKS_MATCH true")

    print("PROVENANCE_CHECK PASS")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as error:
        print(f"PROVENANCE_CHECK FAIL: {error}", file=sys.stderr)
        raise
