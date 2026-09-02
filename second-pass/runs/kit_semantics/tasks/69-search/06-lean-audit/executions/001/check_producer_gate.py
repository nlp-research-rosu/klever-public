#!/usr/bin/env python3
"""Verify immutable Stage 4 producer provenance before judging generation."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from tools.pipeline_contract import sha256_tree


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    audit_input = json.loads(Path("/audit-input.json").read_text())
    generator = json.loads(
        Path("/reference/klean-generation/generator-manifest.json").read_text()
    )
    source = json.loads(
        Path("/reference/generation-tools/source-manifest.json").read_text()
    )
    tools = Path("/reference/generation-tools")
    actual_files = {
        name: file_sha256(tools / name)
        for name in ("klean_export.py", "klean.py")
    }
    recorded_files = {
        "klean_export.py": generator.get("exporter_sha256"),
        "klean.py": generator.get("klean_py_sha256"),
    }
    audit_producer_path = Path(
        audit_input["resolution"]["generation_producer_sources"]
    )
    audit_generator_id = f"sha256:{audit_producer_path.name}"
    expected_tree = audit_input["resolution"]["hashes"][
        "generation_producer_sources_sha256"
    ]
    actual_tree = sha256_tree(tools)
    generator_id = generator["provenance"]["generator_image_id"]
    source_generator_id = source["generator_image_id"]
    report = {
        "actual_file_sha256": actual_files,
        "generator_manifest_file_sha256": recorded_files,
        "source_manifest_file_sha256": source["files"],
        "file_hashes_match_generator_manifest": actual_files == recorded_files,
        "file_hashes_match_source_manifest": actual_files == source["files"],
        "actual_producer_tree_sha256": actual_tree,
        "audit_input_producer_tree_sha256": expected_tree,
        "producer_tree_hash_matches": actual_tree == expected_tree,
        "generator_manifest_image_id": generator_id,
        "source_manifest_image_id": source_generator_id,
        "audit_input_image_id_from_producer_path": audit_generator_id,
        "generator_image_ids_match": (
            generator_id == source_generator_id == audit_generator_id
        ),
    }
    report["producer_gate_pass"] = all(
        (
            report["file_hashes_match_generator_manifest"],
            report["file_hashes_match_source_manifest"],
            report["producer_tree_hash_matches"],
            report["generator_image_ids_match"],
        )
    )
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
