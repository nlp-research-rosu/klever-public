#!/usr/bin/env python3
"""Independently check launcher-recorded mounted-input hashes and campaign data."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from pathlib import Path
from typing import Any


AUDIT_INPUT = Path("/audit-input.json")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def canonical_json_hash(value: Any) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def content_tree_hash(root: Path) -> str:
    """Content digest used by the mounted pipeline records."""
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
                while chunk := stream.read(1024 * 1024):
                    digest.update(chunk)
    return digest.hexdigest()


def entry(path: Path) -> dict[str, Any]:
    return {
        "path": str(path),
        "exists": path.exists(),
        "is_symlink": path.is_symlink(),
        "is_file": path.is_file(),
        "is_dir": path.is_dir(),
        "readable": os.access(path, os.R_OK),
        "sha256": sha256_file(path) if path.is_file() and not path.is_symlink() else None,
    }


def main() -> None:
    audit = json.loads(AUDIT_INPUT.read_text())
    paths = {key: Path(value) for key, value in audit["container_paths"].items()}
    required = {
        "audit_input": Path("/audit-input.json"),
        "audit_campaign_lock": paths["audit_campaign_lock"],
        "candidate": paths["candidate"],
        "canonical": paths["canonical"],
        "translator": paths["translator"],
        "trusted_prompt": paths["trusted_prompt"],
        "run_manifest": paths["run_manifest"],
        "task_manifest": paths["task_manifest"],
        "stage1_result": paths["stage1_result"],
        "generation_manifest": paths["generation_manifest"],
        "generation_metrics": paths["generation_metrics"],
        "generation_last": paths["generation_last"],
        "generation_output": paths["generation_output"],
        "generation_prompt": paths["generation_root"] / "prompt.txt",
        "generation_trace": paths["generation_trace"],
    }
    if (paths["generation_root"] / "usage.json").exists():
        required["generation_usage"] = paths["generation_root"] / "usage.json"

    lock = json.loads(paths["audit_campaign_lock"].read_text())
    invocation = json.loads(paths["generation_manifest"].read_text())
    result_record = json.loads(paths["stage1_result"].read_text())
    usage_path = paths["generation_root"] / "usage.json"
    usage = json.loads(usage_path.read_text()) if usage_path.exists() else {}
    candidate_tree_hash = content_tree_hash(paths["candidate"])
    trace_tree_hash = content_tree_hash(paths["generation_trace"])
    result = {
        "record_layout": audit["record_layout"],
        "semantics_mode": audit["semantics_mode"],
        "required_mounts": {name: entry(path) for name, path in required.items()},
        "campaign_object_equal": lock == audit["audit_campaign"],
        "campaign_canonical_json_sha256": canonical_json_hash(lock),
        "reference_semantics_exists": Path("/reference/reference-semantics").exists(),
        "tree_hashes": {
            "candidate_content_tree_sha256": candidate_tree_hash,
            "candidate_matches_invocation_retained_workspace": (
                candidate_tree_hash == invocation.get("retained_workspace_sha256")
            ),
            "candidate_matches_result_workspace": (
                candidate_tree_hash
                == result_record.get("outputs", {}).get("workspace_sha256")
            ),
            "audit_input_candidate_tree_sha256": audit["hashes"].get(
                "candidate_tree_sha256"
            ),
            "trace_content_tree_sha256": trace_tree_hash,
            "trace_matches_usage_source_trace": (
                trace_tree_hash == usage.get("source_trace_sha256")
            ),
            "audit_input_generation_trace_sha256": audit["hashes"].get(
                "generation_codex_trace_sha256"
            ),
        },
        "recorded_vs_actual": {},
    }

    comparisons = {
        "audit_campaign_lock_sha256": paths["audit_campaign_lock"],
        "canonical_sha256": paths["canonical"],
        "trusted_prompt_sha256": paths["trusted_prompt"],
        "trusted_translator_sha256": paths["translator"],
        "candidate_prompt_sha256": paths["candidate"] / "prompt.py",
        "candidate_translator_sha256": paths["candidate"] / "py2mpy.py",
        "generation_codex_last_sha256": paths["generation_last"],
        "generation_codex_output_sha256": paths["generation_output"],
        "generation_metrics_sha256": paths["generation_metrics"],
        "generation_prompt_sha256": paths["generation_root"] / "prompt.txt",
        "generation_usage_sha256": paths["generation_root"] / "usage.json",
        "run_manifest_sha256": paths["run_manifest"],
        "task_manifest_sha256": paths["task_manifest"],
        "stage1_result_sha256": paths["stage1_result"],
        "stage1_invocation_sha256": paths["generation_manifest"],
    }
    for name, path in comparisons.items():
        recorded = audit["hashes"].get(name)
        actual = sha256_file(path) if path.is_file() and not path.is_symlink() else None
        result["recorded_vs_actual"][name] = {
            "recorded": recorded,
            "actual": actual,
            "match": recorded == actual,
        }

    declared_outputs = invocation.get("outputs", {}).get("evidence", {})
    output_checks: dict[str, Any] = {}
    for relative, recorded in sorted(declared_outputs.items()):
        path = paths["generation_root"] / relative
        actual = sha256_file(path) if path.is_file() and not path.is_symlink() else None
        output_checks[relative] = {
            "recorded": recorded,
            "actual": actual,
            "match": recorded == actual,
        }
    result["invocation_declared_outputs"] = output_checks

    trace_files = sorted(paths["generation_trace"].rglob("*.jsonl"))
    trace_line_count = 0
    trace_type_counts: dict[str, int] = {}
    for trace_file in trace_files:
        with trace_file.open() as stream:
            for line in stream:
                item = json.loads(line)
                trace_line_count += 1
                key = f"{item.get('type')}:{item.get('payload', {}).get('type')}"
                trace_type_counts[key] = trace_type_counts.get(key, 0) + 1
    result["structured_trace"] = {
        "files": [str(path) for path in trace_files],
        "valid_jsonl_lines": trace_line_count,
        "type_counts": dict(sorted(trace_type_counts.items())),
    }

    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
