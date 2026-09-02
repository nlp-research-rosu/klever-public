#!/usr/bin/env python3
"""Required Stage 4 producer-source provenance gate."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from tools.pipeline_contract import sha256_tree


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


producer_root = Path("/reference/generation-tools")
source_manifest = json.loads((producer_root / "source-manifest.json").read_text())
generator_manifest = json.loads(
    Path("/reference/klean-generation/generator-manifest.json").read_text()
)
audit_input = json.loads(Path("/audit-input.json").read_text())
resolution = audit_input["resolution"]

actual_files = {
    "klean.py": sha256_file(producer_root / "klean.py"),
    "klean_export.py": sha256_file(producer_root / "klean_export.py"),
}
recorded_files = source_manifest["files"]
producer_tree = sha256_tree(producer_root)
audit_tree = resolution["hashes"]["generation_producer_sources_sha256"]

source_image = source_manifest["generator_image_id"]
generator_image = generator_manifest["provenance"]["generator_image_id"]
audit_path_image = (
    "sha256:" + Path(resolution["generation_producer_sources"]).name
)

facts = {
    "actual_files": actual_files,
    "source_manifest_files": recorded_files,
    "generator_manifest_exporter_sha256": generator_manifest[
        "exporter_sha256"
    ],
    "generator_manifest_klean_py_sha256": generator_manifest[
        "klean_py_sha256"
    ],
    "producer_tree_sha256": producer_tree,
    "audit_input_producer_tree_sha256": audit_tree,
    "source_manifest_generator_image_id": source_image,
    "generator_manifest_generator_image_id": generator_image,
    "audit_input_path_generator_image_id": audit_path_image,
    "file_hashes_match_source_manifest": actual_files == recorded_files,
    "file_hashes_match_generator_manifest": (
        actual_files["klean_export.py"]
        == generator_manifest["exporter_sha256"]
        and actual_files["klean.py"] == generator_manifest["klean_py_sha256"]
    ),
    "producer_tree_matches_audit_input": producer_tree == audit_tree,
    "generator_image_ids_match": (
        source_image == generator_image == audit_path_image
    ),
}

print(json.dumps(facts, indent=2, sort_keys=True))
if not all(
    (
        facts["file_hashes_match_source_manifest"],
        facts["file_hashes_match_generator_manifest"],
        facts["producer_tree_matches_audit_input"],
        facts["generator_image_ids_match"],
    )
):
    raise SystemExit("PRODUCER_PROVENANCE_GATE: AUDIT_ERROR")
print("PRODUCER_PROVENANCE_GATE: PASS")
