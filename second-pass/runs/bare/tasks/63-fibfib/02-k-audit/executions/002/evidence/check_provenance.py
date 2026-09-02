#!/usr/bin/env python3
"""Independent, read-only integrity checks for the mounted audit inputs."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from collections import Counter
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def pipeline_tree_sha256(root: Path) -> str:
    """Reproduce the pipeline-v2 relative-path/type/size/content tree digest."""
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
    print(f"REGULAR {path} size={path.stat().st_size}")


def main() -> None:
    audit = json.loads(AUDIT_INPUT.read_text())
    assert audit["record_layout"] == "legacy-selected-stage1"
    assert audit["semantics_mode"] == "GENERATED_SEMANTICS"

    paths = audit["container_paths"]
    launcher_records = [
        Path("/audit-input.json"),
        Path(paths["audit_campaign_lock"]),
        Path(paths["run_manifest"]),
        Path(paths["task_manifest"]),
        Path(paths["stage1_result"]),
        Path(paths["generation_manifest"]),
        Path(paths["generation_metrics"]),
        Path(paths["generation_last"]),
        Path(paths["generation_output"]),
        Path(paths["generation_root"]) / "prompt.txt",
    ]
    usage = Path(paths["generation_root"]) / "usage.json"
    if usage.exists():
        launcher_records.append(usage)
    for path in launcher_records:
        require_regular(path)

    candidate = Path(paths["candidate"])
    reference_files = [
        Path(paths["canonical"]),
        Path(paths["trusted_prompt"]),
        Path(paths["translator"]),
    ]
    proof_files = [
        candidate / name
        for name in (
            "prompt.py",
            "py2mpy.py",
            "solution.py",
            "solution.mpy",
            "semantic.k",
            "verification.k",
            "spec.k",
            "prove.sh",
        )
    ]
    for path in reference_files + proof_files:
        require_regular(path)

    assert not Path("/reference/reference-semantics").exists()
    assert not (candidate / "reference-semantics").exists()
    assert (candidate / "prompt.py").read_bytes() == Path(paths["trusted_prompt"]).read_bytes()
    assert (candidate / "py2mpy.py").read_bytes() == Path(paths["translator"]).read_bytes()
    print("BYTE_IDENTITY candidate prompt == trusted prompt")
    print("BYTE_IDENTITY candidate translator == trusted translator")
    print("MODE_BOUNDARY no trusted or candidate reference-semantics tree")

    lock_path = Path(paths["audit_campaign_lock"])
    lock = json.loads(lock_path.read_text())
    assert lock == audit["audit_campaign"]
    lock_hash = file_sha256(lock_path)
    assert lock_hash == audit["hashes"]["audit_campaign_lock_sha256"]
    print(f"CAMPAIGN_LOCK exact block match sha256={lock_hash}")

    hash_paths = {
        "audit_campaign_lock_sha256": lock_path,
        "canonical_sha256": Path(paths["canonical"]),
        "trusted_prompt_sha256": Path(paths["trusted_prompt"]),
        "trusted_translator_sha256": Path(paths["translator"]),
        "candidate_prompt_sha256": candidate / "prompt.py",
        "candidate_translator_sha256": candidate / "py2mpy.py",
        "run_manifest_sha256": Path(paths["run_manifest"]),
        "task_manifest_sha256": Path(paths["task_manifest"]),
        "stage1_result_sha256": Path(paths["stage1_result"]),
        "stage1_invocation_sha256": Path(paths["generation_manifest"]),
        "generation_metrics_sha256": Path(paths["generation_metrics"]),
        "generation_prompt_sha256": Path(paths["generation_root"]) / "prompt.txt",
        "generation_usage_sha256": usage,
        "generation_codex_last_sha256": Path(paths["generation_last"]),
        "generation_codex_output_sha256": Path(paths["generation_output"]),
    }
    for field, path in hash_paths.items():
        if field not in audit["hashes"] or audit["hashes"][field] is None:
            continue
        observed = file_sha256(path)
        expected = audit["hashes"][field]
        assert observed == expected, (field, observed, expected)
        print(f"HASH_OK {field} {observed}")
    assert audit["hashes"]["manifest_sha256"] == audit["hashes"]["task_manifest_sha256"]
    assert audit["hashes"]["candidate_reference_semantics_sha256"] is None
    assert audit["hashes"]["trusted_reference_semantics_sha256"] is None
    print("HASH_OK manifest_sha256 aliases the checked task manifest")

    invocation = json.loads(Path(paths["generation_manifest"]).read_text())
    result = json.loads(Path(paths["stage1_result"]).read_text())
    for relative, expected in invocation["outputs"]["evidence"].items():
        artifact = Path(paths["generation_root"]) / relative
        require_regular(artifact)
        observed = file_sha256(artifact)
        assert observed == expected, (relative, observed, expected)
        print(f"GENERATION_HASH_OK {relative} {observed}")
    assert invocation["outputs"]["evidence"] == result["outputs"]["evidence"]

    candidate_pipeline_hash = pipeline_tree_sha256(candidate)
    assert candidate_pipeline_hash == invocation["outputs"]["workspace_sha256"]
    assert candidate_pipeline_hash == result["outputs"]["workspace_sha256"]
    print(f"CANDIDATE_PIPELINE_TREE_HASH_OK {candidate_pipeline_hash}")
    print(
        "LAUNCHER_RECORDED_TREE_HASHES "
        f"candidate={audit['hashes']['candidate_tree_sha256']} "
        f"trace={audit['hashes']['generation_codex_trace_sha256']}"
    )

    trace_root = Path(paths["generation_trace"])
    assert trace_root.is_dir() and not trace_root.is_symlink()
    trace_files = sorted(path for path in trace_root.rglob("*") if path.is_file())
    assert trace_files
    trace_counts: Counter[str] = Counter()
    trace_lines = 0
    for trace_file in trace_files:
        assert not trace_file.is_symlink()
        with trace_file.open() as stream:
            for line_number, line in enumerate(stream, 1):
                event = json.loads(line)
                trace_counts[event["type"]] += 1
                trace_lines += 1
        relative = trace_file.relative_to(trace_root).as_posix()
        expected = invocation["outputs"]["evidence"][f"codex-trace/{relative}"]
        assert file_sha256(trace_file) == expected
    print(f"TRACE_VALID files={len(trace_files)} lines={trace_lines} types={dict(trace_counts)}")
    print(f"TRACE_PIPELINE_TREE_SHA256 {pipeline_tree_sha256(trace_root)}")

    for root in (candidate, Path("/reference"), Path(paths["generation_root"])):
        links = [path for path in root.rglob("*") if path.is_symlink()]
        assert not links, links
        print(f"NO_SYMLINKS {root}")

    print("PROVENANCE_CHECK_PASS")


if __name__ == "__main__":
    main()
