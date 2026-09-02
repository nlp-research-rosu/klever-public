#!/usr/bin/env python3
"""Independent integrity checks for the mounted 46-fib4 audit inputs."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from collections import Counter
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_tree(root: Path) -> str:
    """Recompute the launcher tree digest from entry names, kinds, sizes, bytes."""
    if not stat.S_ISDIR(root.lstat().st_mode):
        raise RuntimeError(f"not a real directory: {root}")
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
                while chunk := stream.read(1024 * 1024):
                    digest.update(chunk)
    return digest.hexdigest()


def real_kind(path: Path) -> str:
    mode = path.lstat().st_mode
    if stat.S_ISREG(mode):
        return "regular"
    if stat.S_ISDIR(mode):
        return "directory"
    if stat.S_ISLNK(mode):
        return "symlink"
    return f"unsupported:{mode:o}"


def report_digest(label: str, path: Path, expected: str, tree: bool = False) -> None:
    actual = sha256_tree(path) if tree else sha256_file(path)
    print(
        f"{label}: kind={real_kind(path)} expected={expected} "
        f"actual={actual} match={actual == expected}"
    )


def main() -> None:
    audit = json.loads(AUDIT_INPUT.read_text())
    hashes = audit["hashes"]
    paths = audit["container_paths"]

    print(f"record_layout={audit['record_layout']}")
    print(f"semantics_mode={audit['semantics_mode']}")
    print(f"mount_reference_semantics={audit['mount_reference_semantics']}")

    lock_path = Path(paths["audit_campaign_lock"])
    lock = json.loads(lock_path.read_text())
    print(f"campaign_block_equal={lock == audit['audit_campaign']}")

    required_files = {
        "audit_input": AUDIT_INPUT,
        "audit_campaign_lock": lock_path,
        "run_manifest": Path(paths["run_manifest"]),
        "task_manifest": Path(paths["task_manifest"]),
        "stage1_result": Path(paths["stage1_result"]),
        "generation_manifest": Path(paths["generation_manifest"]),
        "generation_metrics": Path(paths["generation_metrics"]),
        "generation_last": Path(paths["generation_last"]),
        "generation_output": Path(paths["generation_output"]),
        "generation_prompt": Path(paths["generation_root"]) / "prompt.txt",
        "generation_usage": Path(paths["generation_root"]) / "usage.json",
        "canonical": Path(paths["canonical"]),
        "translator": Path(paths["translator"]),
        "trusted_prompt": Path(paths["trusted_prompt"]),
        "candidate_prompt": Path(paths["candidate"]) / "prompt.py",
        "candidate_translator": Path(paths["candidate"]) / "py2mpy.py",
    }
    for label, path in required_files.items():
        print(f"required {label}: exists={path.exists()} kind={real_kind(path)} path={path}")

    digest_checks = {
        "audit_campaign_lock_sha256": lock_path,
        "run_manifest_sha256": Path(paths["run_manifest"]),
        "task_manifest_sha256": Path(paths["task_manifest"]),
        "stage1_result_sha256": Path(paths["stage1_result"]),
        "stage1_invocation_sha256": Path(paths["generation_manifest"]),
        "generation_metrics_sha256": Path(paths["generation_metrics"]),
        "generation_codex_last_sha256": Path(paths["generation_last"]),
        "generation_codex_output_sha256": Path(paths["generation_output"]),
        "generation_prompt_sha256": Path(paths["generation_root"]) / "prompt.txt",
        "generation_usage_sha256": Path(paths["generation_root"]) / "usage.json",
        "canonical_sha256": Path(paths["canonical"]),
        "trusted_prompt_sha256": Path(paths["trusted_prompt"]),
        "trusted_translator_sha256": Path(paths["translator"]),
        "candidate_prompt_sha256": Path(paths["candidate"]) / "prompt.py",
        "candidate_translator_sha256": Path(paths["candidate"]) / "py2mpy.py",
    }
    for key, path in digest_checks.items():
        report_digest(key, path, hashes[key])
    report_digest(
        "candidate_tree_sha256",
        Path(paths["candidate"]),
        hashes["candidate_tree_sha256"],
        tree=True,
    )
    report_digest(
        "generation_codex_trace_sha256",
        Path(paths["generation_trace"]),
        hashes["generation_codex_trace_sha256"],
        tree=True,
    )

    candidate_prompt = (Path(paths["candidate"]) / "prompt.py").read_bytes()
    trusted_prompt = Path(paths["trusted_prompt"]).read_bytes()
    candidate_translator = (Path(paths["candidate"]) / "py2mpy.py").read_bytes()
    trusted_translator = Path(paths["translator"]).read_bytes()
    print(f"candidate_prompt_byte_equal={candidate_prompt == trusted_prompt}")
    print(f"candidate_translator_byte_equal={candidate_translator == trusted_translator}")
    print(f"reference_semantics_exists={Path('/reference/reference-semantics').exists()}")
    print(f"candidate_reference_semantics_exists={Path('/candidate/reference-semantics').exists()}")

    trace_root = Path(paths["generation_trace"])
    trace_files = sorted(trace_root.rglob("*"))
    print(f"trace_entries={len(trace_files)}")
    for path in trace_files:
        print(f"trace_entry kind={real_kind(path)} relative={path.relative_to(trace_root)}")
    jsonl_files = [path for path in trace_files if path.is_file() and path.suffix == ".jsonl"]
    event_types: Counter[str] = Counter()
    payload_types: Counter[str] = Counter()
    total_lines = 0
    for trace in jsonl_files:
        with trace.open() as stream:
            for line_number, line in enumerate(stream, 1):
                total_lines += 1
                record = json.loads(line)
                event_types[str(record.get("type"))] += 1
                payload = record.get("payload")
                if isinstance(payload, dict):
                    payload_types[str(payload.get("type"))] += 1
    print(f"trace_jsonl_files={len(jsonl_files)}")
    print(f"trace_jsonl_lines={total_lines}")
    print(f"trace_event_types={dict(sorted(event_types.items()))}")
    print(f"trace_payload_types={dict(sorted(payload_types.items()))}")


if __name__ == "__main__":
    main()
