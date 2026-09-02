#!/usr/bin/env python3
"""Cross-check all Stage 4 producer-source provenance bindings."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from tools import pipeline_contract
from tools.klean_export import tree_digest


generation_tools = Path("/reference/generation-tools")
generator_manifest = json.loads(
    Path("/reference/klean-generation/generator-manifest.json").read_text()
)
source_manifest = json.loads(
    (generation_tools / "source-manifest.json").read_text()
)
audit_input = json.loads(Path("/audit-input.json").read_text())["resolution"]

actual_files = {
    name: hashlib.sha256((generation_tools / name).read_bytes()).hexdigest()
    for name in ("klean_export.py", "klean.py")
}
actual_export_tree = tree_digest(generation_tools)
actual_launcher_tree = pipeline_contract.sha256_tree(generation_tools)
generator_image = generator_manifest["provenance"]["generator_image_id"]
source_image = source_manifest["generator_image_id"]
audit_source_selector = Path(
    audit_input["generation_producer_sources"]
).name

checks = {
    "klean_export_matches_generator_manifest": (
        actual_files["klean_export.py"] == generator_manifest["exporter_sha256"]
    ),
    "klean_matches_generator_manifest": (
        actual_files["klean.py"] == generator_manifest["klean_py_sha256"]
    ),
    "files_match_source_manifest": actual_files == source_manifest["files"],
    "generator_image_matches_source_manifest": generator_image == source_image,
    "generator_image_matches_audit_source_selector": (
        generator_image == f"sha256:{audit_source_selector}"
    ),
    "producer_tree_matches_audit_input": (
        actual_launcher_tree
        == audit_input["hashes"]["generation_producer_sources_sha256"]
    ),
}

report = {
    "actual_file_sha256": actual_files,
    "actual_generation_tools_export_tree_sha256": actual_export_tree,
    "actual_generation_tools_launcher_tree_sha256": actual_launcher_tree,
    "generator_manifest_exporter_sha256": generator_manifest["exporter_sha256"],
    "generator_manifest_klean_py_sha256": generator_manifest["klean_py_sha256"],
    "generator_manifest_image_id": generator_image,
    "source_manifest": source_manifest,
    "audit_input_generation_producer_sources": audit_input[
        "generation_producer_sources"
    ],
    "audit_input_generation_producer_sources_sha256": audit_input["hashes"][
        "generation_producer_sources_sha256"
    ],
    "checks": checks,
    "all_checks_pass": all(checks.values()),
}
print(json.dumps(report, indent=2, sort_keys=True))
