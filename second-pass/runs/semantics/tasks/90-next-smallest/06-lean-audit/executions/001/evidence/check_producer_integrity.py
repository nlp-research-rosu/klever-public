#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

from tools.klean_export import tree_digest
from tools.pipeline_contract import sha256_tree


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


audit = json.loads(Path("/audit-input.json").read_text())
source = json.loads(
    Path("/reference/generation-tools/source-manifest.json").read_text()
)
generator = json.loads(
    Path("/reference/klean-generation/generator-manifest.json").read_text()
)
resolution = audit["resolution"]

actual_files = {
    name: sha256(Path("/reference/generation-tools") / name)
    for name in ("klean_export.py", "klean.py")
}
source_path_image = (
    "sha256:" + Path(resolution["generation_producer_sources"]).name
)
checks = {
    "actual_files_match_source_manifest": actual_files == source["files"],
    "exporter_matches_generator_manifest": (
        actual_files["klean_export.py"] == generator["exporter_sha256"]
    ),
    "klean_matches_generator_manifest": (
        actual_files["klean.py"] == generator["klean_py_sha256"]
    ),
    "image_matches_generator_manifest": (
        source["generator_image_id"]
        == generator["provenance"]["generator_image_id"]
    ),
    "image_matches_audit_input_bound_path": (
        source["generator_image_id"] == source_path_image
    ),
    "producer_tree_matches_audit_input": (
        sha256_tree(Path("/reference/generation-tools"))
        == resolution["hashes"]["generation_producer_sources_sha256"]
    ),
}
result = {
    "actual_file_sha256": actual_files,
    "source_manifest_files": source["files"],
    "source_manifest_image_id": source["generator_image_id"],
    "generator_manifest_image_id": generator["provenance"][
        "generator_image_id"
    ],
    "audit_input_bound_image_id": source_path_image,
    "actual_pipeline_artifact_tree_sha256": sha256_tree(
        Path("/reference/generation-tools")
    ),
    "informational_klean_tree_sha256": tree_digest(
        Path("/reference/generation-tools")
    ),
    "audit_input_producer_tree_sha256": resolution["hashes"][
        "generation_producer_sources_sha256"
    ],
    "checks": checks,
    "status": "PASS" if all(checks.values()) else "AUDIT_ERROR",
}
print(json.dumps(result, indent=2, sort_keys=True))
