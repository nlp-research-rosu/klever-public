#!/usr/bin/env python3
"""Verify mounted Stage 4 producer sources against all recorded provenance."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path, PurePosixPath

from tools.pipeline_contract import sha256_tree


BUNDLE = Path("/reference/generation-tools")
GENERATOR_MANIFEST = Path("/reference/klean-generation/generator-manifest.json")
AUDIT_INPUT = Path("/audit-input.json")


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    generator = json.loads(GENERATOR_MANIFEST.read_text())
    source_manifest = json.loads((BUNDLE / "source-manifest.json").read_text())
    audit_input = json.loads(AUDIT_INPUT.read_text())
    resolution = audit_input["resolution"]
    provenance = generator["provenance"]

    observed_files = sorted(
        path.relative_to(BUNDLE).as_posix()
        for path in BUNDLE.rglob("*")
        if path.is_file()
    )
    observed_hashes = {
        "klean.py": file_sha256(BUNDLE / "klean.py"),
        "klean_export.py": file_sha256(BUNDLE / "klean_export.py"),
    }
    expected_from_generator = {
        "klean.py": generator["klean_py_sha256"],
        "klean_export.py": generator["exporter_sha256"],
    }
    recorded_bundle_path = PurePosixPath(
        resolution["generation_producer_sources"]
    )
    image_id_from_audit_path = f"sha256:{recorded_bundle_path.name}"
    observed_tree_hash = sha256_tree(BUNDLE)

    checks = {
        "bundle_file_set_exact": observed_files
        == ["klean.py", "klean_export.py", "source-manifest.json"],
        "source_manifest_schema_version_1": (
            source_manifest.get("schema_version") == 1
        ),
        "source_manifest_file_map_exact": (
            source_manifest.get("files") == expected_from_generator
        ),
        "mounted_source_hashes_match_generator": (
            observed_hashes == expected_from_generator
        ),
        "mounted_source_hashes_match_source_manifest": (
            observed_hashes == source_manifest.get("files")
        ),
        "image_id_generator_matches_source_manifest": (
            provenance.get("generator_image_id")
            == source_manifest.get("generator_image_id")
        ),
        "image_id_generator_matches_audit_input_path": (
            provenance.get("generator_image_id") == image_id_from_audit_path
        ),
        "producer_bundle_tree_hash_matches_audit_input": (
            observed_tree_hash
            == resolution["hashes"]["generation_producer_sources_sha256"]
        ),
    }
    result = {
        "bundle": str(BUNDLE),
        "observed_files": observed_files,
        "observed_hashes": observed_hashes,
        "expected_from_generator_manifest": expected_from_generator,
        "source_manifest": source_manifest,
        "generator_image_id": provenance.get("generator_image_id"),
        "audit_input_recorded_bundle_path": str(recorded_bundle_path),
        "image_id_from_audit_input_path": image_id_from_audit_path,
        "observed_pipeline_tree_sha256": observed_tree_hash,
        "audit_input_pipeline_tree_sha256": resolution["hashes"][
            "generation_producer_sources_sha256"
        ],
        "checks": checks,
        "all_checks_pass": all(checks.values()),
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    if not result["all_checks_pass"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
