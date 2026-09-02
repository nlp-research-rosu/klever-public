#!/usr/bin/env python3
"""Recompute launcher-recorded hashes for every mounted input."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from tools import klean_export, pipeline_contract


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    audit_input = json.loads(Path("/audit-input.json").read_text())
    resolution = audit_input["resolution"]
    expected_source_hashes = resolution["stage1_source_hashes"]
    actual_source_hashes = {}
    missing_source_files = []
    mismatched_source_files = []
    for relative, expected in expected_source_hashes.items():
        path = Path("/reference/k-proof") / relative
        if not path.is_file() or path.is_symlink():
            missing_source_files.append(relative)
            continue
        actual = file_sha256(path)
        actual_source_hashes[relative] = actual
        if actual != expected:
            mismatched_source_files.append(
                {"file": relative, "expected": expected, "actual": actual}
            )

    expected = resolution["hashes"]
    actual = {
        "discovery_manifest_sha256": file_sha256(
            Path("/reference/lemma-discovery.json")
        ),
        "generated_tree_sha256": klean_export.tree_digest(
            Path("/reference/klean-generation/generated")
        ),
        "generation_producer_sources_sha256": pipeline_contract.sha256_tree(
            Path("/reference/generation-tools")
        ),
        "k_audit_sha256": pipeline_contract.sha256_tree(
            Path("/reference/k-audit")
        ),
        "k_workspace_sha256": pipeline_contract.sha256_tree(
            Path("/reference/k-proof")
        ),
        "klean_generation_sha256": pipeline_contract.sha256_tree(
            Path("/reference/klean-generation")
        ),
        "lean_workspace_sha256": pipeline_contract.sha256_tree(
            Path("/candidate")
        ),
        "stage1_export_sha256": klean_export.tree_digest(
            Path("/reference/k-proof")
        ),
    }
    hash_checks = {
        key: {
            "expected": expected[key],
            "actual": value,
            "matches": expected[key] == value,
        }
        for key, value in actual.items()
    }
    report = {
        "stage1_source_hash_count": len(expected_source_hashes),
        "stage1_source_files_checked": len(actual_source_hashes),
        "stage1_source_files_missing": missing_source_files,
        "stage1_source_files_mismatched": mismatched_source_files,
        "mounted_hash_checks": hash_checks,
        "unmounted_hash_records": {
            "lean_invocation_sha256": expected["lean_invocation_sha256"]
        },
        "all_mounted_recorded_hashes_match": (
            not missing_source_files
            and not mismatched_source_files
            and all(item["matches"] for item in hash_checks.values())
        ),
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
