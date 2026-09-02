#!/usr/bin/env python3
"""Recompute and cross-check immutable Stage 4 producer provenance."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from tools.klean_export import tree_digest
from tools.pipeline_contract import sha256_tree


tools_dir = Path("/reference/generation-tools")
generation = Path("/reference/klean-generation")
audit_input = json.loads(Path("/audit-input.json").read_text())
source_manifest = json.loads((tools_dir / "source-manifest.json").read_text())
generator_manifest = json.loads(
    (generation / "generator-manifest.json").read_text()
)

actual = {
    name: hashlib.sha256((tools_dir / name).read_bytes()).hexdigest()
    for name in ("klean_export.py", "klean.py")
}
audit_resolution = audit_input["resolution"]
path_image_digest = Path(
    audit_resolution["generation_producer_sources"]
).name
path_image_id = f"sha256:{path_image_digest}"

checks = {
    "actual_equals_source_manifest": actual == source_manifest["files"],
    "exporter_equals_generator_manifest": actual["klean_export.py"]
    == generator_manifest["exporter_sha256"],
    "klean_equals_generator_manifest": actual["klean.py"]
    == generator_manifest["klean_py_sha256"],
    "source_image_equals_generator_image": source_manifest["generator_image_id"]
    == generator_manifest["provenance"]["generator_image_id"],
    "audit_path_image_equals_manifests": path_image_id
    == source_manifest["generator_image_id"]
    == generator_manifest["provenance"]["generator_image_id"],
    "launcher_tree_equals_audit_input": sha256_tree(tools_dir)
    == audit_resolution["hashes"]["generation_producer_sources_sha256"],
}

print(
    json.dumps(
        {
            "actual_file_sha256": actual,
            "source_manifest": source_manifest,
            "generator_manifest_fields": {
                "exporter_sha256": generator_manifest["exporter_sha256"],
                "klean_py_sha256": generator_manifest["klean_py_sha256"],
                "generator_image_id": generator_manifest["provenance"][
                    "generator_image_id"
                ],
            },
            "audit_input_fields": {
                "generation_producer_sources": audit_resolution[
                    "generation_producer_sources"
                ],
                "generation_producer_sources_sha256": audit_resolution[
                    "hashes"
                ]["generation_producer_sources_sha256"],
                "image_id_derived_from_keyed_path": path_image_id,
            },
            "recomputed_launcher_tree_sha256": sha256_tree(tools_dir),
            "exporter_tree_sha256_for_format_comparison": tree_digest(tools_dir),
            "checks": checks,
            "all_checks_pass": all(checks.values()),
        },
        indent=2,
        sort_keys=True,
    )
)
