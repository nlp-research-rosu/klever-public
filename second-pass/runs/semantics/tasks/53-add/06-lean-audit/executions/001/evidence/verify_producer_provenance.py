#!/usr/bin/env python3

import hashlib
import json
from pathlib import Path

from tools.pipeline_contract import sha256_tree


audit_input = json.loads(Path("/audit-input.json").read_text())["resolution"]
generator_manifest = json.loads(
    Path("/reference/klean-generation/generator-manifest.json").read_text()
)
source_manifest = json.loads(
    Path("/reference/generation-tools/source-manifest.json").read_text()
)

producer_paths = [
    Path("/reference/generation-tools/klean_export.py"),
    Path("/reference/generation-tools/klean.py"),
]
actual_file_hashes = {
    path.name: hashlib.sha256(path.read_bytes()).hexdigest()
    for path in producer_paths
}
generator_file_hashes = {
    "klean_export.py": generator_manifest["exporter_sha256"],
    "klean.py": generator_manifest["klean_py_sha256"],
}
audit_image_id = (
    "sha256:" + Path(audit_input["generation_producer_sources"]).name
)

result = {
    "actual_file_hashes": actual_file_hashes,
    "generator_manifest_file_hashes": generator_file_hashes,
    "source_manifest_file_hashes": source_manifest["files"],
    "all_file_hashes_match": (
        actual_file_hashes
        == generator_file_hashes
        == source_manifest["files"]
    ),
    "actual_source_tree_sha256": sha256_tree(
        Path("/reference/generation-tools")
    ),
    "audit_input_source_tree_sha256": audit_input["hashes"][
        "generation_producer_sources_sha256"
    ],
    "source_tree_matches": (
        sha256_tree(Path("/reference/generation-tools"))
        == audit_input["hashes"]["generation_producer_sources_sha256"]
    ),
    "generator_manifest_image_id": generator_manifest["provenance"][
        "generator_image_id"
    ],
    "source_manifest_image_id": source_manifest["generator_image_id"],
    "audit_input_path_image_id": audit_image_id,
    "all_image_ids_match": (
        generator_manifest["provenance"]["generator_image_id"]
        == source_manifest["generator_image_id"]
        == audit_image_id
    ),
}

print(json.dumps(result, indent=2, sort_keys=True))
