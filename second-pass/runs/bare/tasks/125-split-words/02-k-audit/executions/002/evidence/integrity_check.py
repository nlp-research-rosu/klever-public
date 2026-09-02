#!/usr/bin/env python3
"""Independent integrity checks for the mounted audit record."""

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


def pipeline_tree_digest(root: Path) -> str:
    """Reproduce the public pipeline-v3 tree digest for an independent check."""
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
                raise AssertionError(f"unsupported or linked tree entry: {path}")
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
    assert stat.S_ISREG(mode), f"required record is not a regular file: {path}"


def require_real_directory(path: Path) -> None:
    mode = path.lstat().st_mode
    assert stat.S_ISDIR(mode), f"required mount is not a real directory: {path}"


def main() -> None:
    print("COMMAND: python3 /audit-output/evidence/integrity_check.py")
    require_regular(AUDIT_INPUT)
    audit = json.loads(AUDIT_INPUT.read_text())
    assert audit["record_layout"] == "legacy-selected-stage1"
    assert audit["semantics_mode"] == "GENERATED_SEMANTICS"

    paths = {key: Path(value) for key, value in audit["container_paths"].items()}
    for key in (
        "audit_campaign_lock",
        "canonical",
        "generation_last",
        "generation_manifest",
        "generation_metrics",
        "generation_output",
        "run_manifest",
        "stage1_result",
        "task_manifest",
        "translator",
        "trusted_prompt",
    ):
        require_regular(paths[key])
    for key in ("candidate", "generation_root", "generation_trace"):
        require_real_directory(paths[key])

    required_generation = (
        "invocation.json",
        "metrics.json",
        "codex-last.txt",
        "codex-output.log",
        "prompt.txt",
    )
    for name in required_generation:
        require_regular(paths["generation_root"] / name)
    usage = paths["generation_root"] / "usage.json"
    if usage.exists():
        require_regular(usage)

    lock = json.loads(paths["audit_campaign_lock"].read_text())
    assert lock == audit["audit_campaign"], "campaign lock block mismatch"
    hashes = audit["hashes"]
    assert sha256_file(paths["audit_campaign_lock"]) == hashes[
        "audit_campaign_lock_sha256"
    ]

    file_checks = {
        paths["canonical"]: "canonical_sha256",
        paths["trusted_prompt"]: "trusted_prompt_sha256",
        paths["translator"]: "trusted_translator_sha256",
        paths["candidate"] / "prompt.py": "candidate_prompt_sha256",
        paths["candidate"] / "py2mpy.py": "candidate_translator_sha256",
        paths["run_manifest"]: "run_manifest_sha256",
        paths["task_manifest"]: "task_manifest_sha256",
        paths["stage1_result"]: "stage1_result_sha256",
        paths["generation_manifest"]: "stage1_invocation_sha256",
        paths["generation_metrics"]: "generation_metrics_sha256",
        paths["generation_last"]: "generation_codex_last_sha256",
        paths["generation_output"]: "generation_codex_output_sha256",
        paths["generation_root"] / "prompt.txt": "generation_prompt_sha256",
    }
    if usage.exists():
        file_checks[usage] = "generation_usage_sha256"
    for path, hash_key in file_checks.items():
        actual = sha256_file(path)
        expected = hashes[hash_key]
        assert actual == expected, f"hash mismatch for {path}: {actual} != {expected}"
        print(f"OK SHA256 {actual} {path}")

    assert (paths["candidate"] / "prompt.py").read_bytes() == paths[
        "trusted_prompt"
    ].read_bytes()
    assert (paths["candidate"] / "py2mpy.py").read_bytes() == paths[
        "translator"
    ].read_bytes()
    assert not Path("/reference/reference-semantics").exists()

    for root in (paths["candidate"], Path("/reference"), paths["generation_root"]):
        for path in root.rglob("*"):
            assert not path.is_symlink(), f"symlink found in mounted tree: {path}"

    invocation = json.loads(paths["generation_manifest"].read_text())
    result = json.loads(paths["stage1_result"].read_text())
    candidate_pipeline_digest = pipeline_tree_digest(paths["candidate"])
    trace_pipeline_digest = pipeline_tree_digest(paths["generation_trace"])
    assert candidate_pipeline_digest == invocation["retained_workspace_sha256"]
    assert candidate_pipeline_digest == invocation["outputs"]["workspace_sha256"]
    assert candidate_pipeline_digest == result["outputs"]["workspace_sha256"]
    print(f"OK pipeline tree digest {candidate_pipeline_digest} /candidate")
    if usage.exists():
        usage_doc = json.loads(usage.read_text())
        assert trace_pipeline_digest == usage_doc["source_trace_sha256"]
    print(
        f"OK pipeline tree digest {trace_pipeline_digest} "
        "/generation-evidence/codex-trace"
    )

    result_outputs = result["outputs"]["evidence"]
    for relative, expected in result_outputs.items():
        path = paths["generation_root"] / relative
        require_regular(path)
        actual = sha256_file(path)
        assert actual == expected, f"stage-result evidence mismatch: {path}"
        print(f"OK RESULT-EVIDENCE {actual} {path}")

    print(
        "NOTE launcher candidate_tree_sha256 uses a different digest scheme: "
        f"{hashes['candidate_tree_sha256']}"
    )
    print(
        "NOTE launcher generation_codex_trace_sha256 uses a different digest "
        f"scheme: {hashes['generation_codex_trace_sha256']}"
    )
    print("INTEGRITY_CHECK: PASS")


if __name__ == "__main__":
    main()
