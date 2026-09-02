#!/usr/bin/env python3
"""Independently validate launcher records and mounted provenance inputs."""

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


def pipeline_tree_hash(root: Path) -> str:
    """Reproduce pipeline-v2's length-delimited regular-tree digest."""
    digest = hashlib.sha256()
    pending = [root]
    entries: list[tuple[str, str, Path]] = []
    while pending:
        directory = pending.pop()
        for child in os.scandir(directory):
            mode = child.stat(follow_symlinks=False).st_mode
            path = Path(child.path)
            relative = path.relative_to(root).as_posix()
            if stat.S_ISDIR(mode):
                entries.append((relative, "directory", path))
                pending.append(path)
            elif stat.S_ISREG(mode):
                entries.append((relative, "file", path))
            else:
                raise RuntimeError(f"linked/unsupported tree entry: {path}")
    for relative, kind, path in sorted(entries):
        encoded = relative.encode()
        digest.update(len(encoded).to_bytes(4, "big"))
        digest.update(encoded)
        digest.update(kind.encode() + b"\0")
        if kind == "file":
            data = path.read_bytes()
            digest.update(len(data).to_bytes(8, "big"))
            digest.update(data)
    return digest.hexdigest()


def require_regular(path: Path) -> None:
    mode = path.lstat().st_mode
    if not stat.S_ISREG(mode):
        raise RuntimeError(f"not a real regular file: {path}")


def main() -> None:
    audit = json.loads(AUDIT_INPUT.read_text())
    lock_path = Path(audit["container_paths"]["audit_campaign_lock"])
    lock = json.loads(lock_path.read_text())
    print(f"record_layout={audit['record_layout']}")
    print(f"semantics_mode={audit['semantics_mode']}")
    print(f"campaign_structural_match={audit['audit_campaign'] == lock}")

    required = [
        AUDIT_INPUT,
        lock_path,
        Path(audit["container_paths"]["run_manifest"]),
        Path(audit["container_paths"]["task_manifest"]),
        Path(audit["container_paths"]["stage1_result"]),
        Path(audit["container_paths"]["generation_manifest"]),
        Path(audit["container_paths"]["generation_metrics"]),
        Path(audit["container_paths"]["generation_last"]),
        Path(audit["container_paths"]["generation_output"]),
        Path(audit["container_paths"]["generation_root"]) / "prompt.txt",
    ]
    usage = Path(audit["container_paths"]["generation_root"]) / "usage.json"
    if usage.exists():
        required.append(usage)
    for path in required:
        require_regular(path)
        print(f"required_regular_readable={os.access(path, os.R_OK)} {path}")

    trace = Path(audit["container_paths"]["generation_trace"])
    if not stat.S_ISDIR(trace.lstat().st_mode):
        raise RuntimeError(f"trace is not a real directory: {trace}")
    trace_files = sorted(p for p in trace.rglob("*") if p.is_file())
    if any(p.is_symlink() for p in trace.rglob("*")):
        raise RuntimeError("trace contains a symlink")
    print(f"trace_regular_files={len(trace_files)}")

    checks = {
        "audit_campaign_lock_sha256": lock_path,
        "canonical_sha256": Path(audit["container_paths"]["canonical"]),
        "trusted_prompt_sha256": Path(audit["container_paths"]["trusted_prompt"]),
        "trusted_translator_sha256": Path(audit["container_paths"]["translator"]),
        "candidate_prompt_sha256": Path(audit["container_paths"]["candidate"]) / "prompt.py",
        "candidate_translator_sha256": Path(audit["container_paths"]["candidate"]) / "py2mpy.py",
        "run_manifest_sha256": Path(audit["container_paths"]["run_manifest"]),
        "task_manifest_sha256": Path(audit["container_paths"]["task_manifest"]),
        "stage1_result_sha256": Path(audit["container_paths"]["stage1_result"]),
        "stage1_invocation_sha256": Path(audit["container_paths"]["generation_manifest"]),
        "generation_metrics_sha256": Path(audit["container_paths"]["generation_metrics"]),
        "generation_usage_sha256": usage,
        "generation_codex_last_sha256": Path(audit["container_paths"]["generation_last"]),
        "generation_codex_output_sha256": Path(audit["container_paths"]["generation_output"]),
        "generation_prompt_sha256": Path(audit["container_paths"]["generation_root"]) / "prompt.txt",
    }
    for field, path in checks.items():
        observed = sha256_file(path)
        expected = audit["hashes"][field]
        print(f"{field}: expected={expected} observed={observed} match={expected == observed}")

    candidate = Path(audit["container_paths"]["candidate"])
    trusted_prompt = Path(audit["container_paths"]["trusted_prompt"])
    translator = Path(audit["container_paths"]["translator"])
    print(f"candidate_prompt_byte_match={candidate.joinpath('prompt.py').read_bytes() == trusted_prompt.read_bytes()}")
    print(f"candidate_translator_byte_match={candidate.joinpath('py2mpy.py').read_bytes() == translator.read_bytes()}")
    reference_semantics = trusted_prompt.parent / "reference-semantics"
    print(f"reference_semantics_absent={not reference_semantics.exists() and not reference_semantics.is_symlink()}")

    candidate_hash = pipeline_tree_hash(candidate)
    trace_hash = pipeline_tree_hash(trace)
    result = json.loads(Path(audit["container_paths"]["stage1_result"]).read_text())
    usage_record = json.loads(usage.read_text())
    print(f"candidate_pipeline_tree_hash={candidate_hash}")
    print(f"generation_result_workspace_hash={result['outputs']['workspace_sha256']}")
    print(f"candidate_matches_generation_result={candidate_hash == result['outputs']['workspace_sha256']}")
    print(f"trace_pipeline_tree_hash={trace_hash}")
    print(f"usage_source_trace_hash={usage_record['source_trace_sha256']}")
    print(f"trace_matches_usage={trace_hash == usage_record['source_trace_sha256']}")
    print(
        "note=audit-input candidate_tree_sha256 and generation_codex_trace_sha256 "
        "use a launcher digest distinct from the legacy pipeline-v2 tree digest"
    )


if __name__ == "__main__":
    main()
