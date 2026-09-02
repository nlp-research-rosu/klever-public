#!/usr/bin/env python3
"""Recompute immutable Stage 4 producer and manifest hashes."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, "/reference")
from tools.klean_export import tree_digest
from tools.pipeline_contract import sha256_tree


audit = json.loads(Path("/audit-input.json").read_text())["resolution"]
generation = Path("/reference/klean-generation")
producer = Path("/reference/generation-tools")
generator_manifest = json.loads(
    (generation / "generator-manifest.json").read_text()
)
source_manifest = json.loads((producer / "source-manifest.json").read_text())

actual_files = {
    name: hashlib.sha256((producer / name).read_bytes()).hexdigest()
    for name in ("klean_export.py", "klean.py")
}
actual = {
    "producer_file_sha256": actual_files,
    "producer_tree_sha256": sha256_tree(producer),
    "generated_tree_sha256": tree_digest(generation / "generated"),
    "stage1_tree_sha256": tree_digest(Path("/reference/k-proof")),
    "discovery_manifest_sha256": hashlib.sha256(
        Path("/reference/lemma-discovery.json").read_bytes()
    ).hexdigest(),
    "generator_image_id": generator_manifest["provenance"][
        "generator_image_id"
    ],
}
expected = {
    "generator_manifest_exporter_sha256": generator_manifest["exporter_sha256"],
    "generator_manifest_klean_py_sha256": generator_manifest["klean_py_sha256"],
    "generator_manifest_generated_tree_sha256": generator_manifest[
        "generated_tree_sha256"
    ],
    "generator_manifest_stage1_tree_sha256": generator_manifest["provenance"][
        "stage1_workspace_sha256"
    ],
    "generator_manifest_discovery_sha256": generator_manifest["provenance"][
        "stage3_discovery_manifest_sha256"
    ],
    "source_manifest_files": source_manifest["files"],
    "source_manifest_generator_image_id": source_manifest["generator_image_id"],
    "audit_input_producer_tree_sha256": audit["hashes"][
        "generation_producer_sources_sha256"
    ],
    "audit_input_generated_tree_sha256": audit["hashes"][
        "generated_tree_sha256"
    ],
    "audit_input_stage1_export_sha256": audit["hashes"][
        "stage1_export_sha256"
    ],
    "audit_input_discovery_sha256": audit["hashes"][
        "discovery_manifest_sha256"
    ],
    "audit_input_producer_path": audit["generation_producer_sources"],
}
producer_path_image = Path(expected["audit_input_producer_path"]).name
checks = {
    "exporter_hash_matches_generator_manifest": (
        actual_files["klean_export.py"]
        == expected["generator_manifest_exporter_sha256"]
    ),
    "klean_hash_matches_generator_manifest": (
        actual_files["klean.py"]
        == expected["generator_manifest_klean_py_sha256"]
    ),
    "files_match_source_manifest": (
        actual_files == expected["source_manifest_files"]
    ),
    "image_ids_match_manifests": (
        actual["generator_image_id"]
        == expected["source_manifest_generator_image_id"]
    ),
    "audit_path_binds_image_id": (
        f"sha256:{producer_path_image}" == actual["generator_image_id"]
    ),
    "producer_tree_matches_audit_input": (
        actual["producer_tree_sha256"]
        == expected["audit_input_producer_tree_sha256"]
    ),
    "generated_tree_matches_generator_manifest": (
        actual["generated_tree_sha256"]
        == expected["generator_manifest_generated_tree_sha256"]
    ),
    "generated_tree_matches_audit_input": (
        actual["generated_tree_sha256"]
        == expected["audit_input_generated_tree_sha256"]
    ),
    "stage1_tree_matches_generator_manifest": (
        actual["stage1_tree_sha256"]
        == expected["generator_manifest_stage1_tree_sha256"]
    ),
    "stage1_tree_matches_audit_input_export": (
        actual["stage1_tree_sha256"]
        == expected["audit_input_stage1_export_sha256"]
    ),
    "discovery_matches_generator_manifest": (
        actual["discovery_manifest_sha256"]
        == expected["generator_manifest_discovery_sha256"]
    ),
    "discovery_matches_audit_input": (
        actual["discovery_manifest_sha256"]
        == expected["audit_input_discovery_sha256"]
    ),
}

print(
    json.dumps(
        {"actual": actual, "expected": expected, "checks": checks},
        indent=2,
        sort_keys=True,
    )
)
if not all(checks.values()):
    raise SystemExit(1)
