#!/usr/bin/env python3
"""Read-only Stage 4 producer provenance authentication."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from tools.pipeline_contract import sha256_tree


GENERATION = Path("/reference/klean-generation")
SOURCES = Path("/reference/generation-tools")
AUDIT_INPUT = Path("/audit-input.json")


def load(path: Path) -> dict:
    return json.loads(path.read_text())


generator = load(GENERATION / "generator-manifest.json")
source_manifest = load(SOURCES / "source-manifest.json")
audit = load(AUDIT_INPUT)
resolution = audit["resolution"]

actual = {
    name: hashlib.sha256((SOURCES / name).read_bytes()).hexdigest()
    for name in ("klean_export.py", "klean.py")
}
expected_generator = {
    "klean_export.py": generator["exporter_sha256"],
    "klean.py": generator["klean_py_sha256"],
}
expected_source_manifest = source_manifest["files"]
generator_image = generator["provenance"]["generator_image_id"]
source_image = source_manifest["generator_image_id"]
audit_image = "sha256:" + Path(resolution["generation_producer_sources"]).name
actual_tree = sha256_tree(SOURCES)
expected_tree = resolution["hashes"]["generation_producer_sources_sha256"]

evidence = {
    "audit_mode_env": __import__("os").environ.get("AUDIT_MODE"),
    "audit_mode_json": resolution["mode"],
    "semantics_mode": resolution["semantics_mode"],
    "actual_file_sha256": actual,
    "generator_manifest_file_sha256": expected_generator,
    "source_manifest_file_sha256": expected_source_manifest,
    "file_hashes_match_generator_manifest": actual == expected_generator,
    "file_hashes_match_source_manifest": actual == expected_source_manifest,
    "generator_manifest_image_id": generator_image,
    "source_manifest_image_id": source_image,
    "audit_input_producer_path_image_id": audit_image,
    "image_ids_match": generator_image == source_image == audit_image,
    "actual_producer_tree_sha256": actual_tree,
    "audit_input_producer_tree_sha256": expected_tree,
    "producer_tree_matches_audit_input": actual_tree == expected_tree,
}
print(json.dumps(evidence, indent=2, sort_keys=True))

if not (
    actual == expected_generator
    and actual == expected_source_manifest
    and generator_image == source_image == audit_image
    and actual_tree == expected_tree
    and __import__("os").environ.get("AUDIT_MODE") == resolution["mode"]
):
    raise SystemExit(1)
