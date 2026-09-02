#!/usr/bin/env python3
"""Authenticate the immutable Stage 4 producer-source bundle."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from tools.pipeline_contract import sha256_tree


bundle = Path("/reference/generation-tools")
generator_manifest_path = Path(
    "/reference/klean-generation/generator-manifest.json"
)
source_manifest_path = bundle / "source-manifest.json"
audit_input_path = Path("/audit-input.json")

generator = json.loads(generator_manifest_path.read_text())
source = json.loads(source_manifest_path.read_text())
audit = json.loads(audit_input_path.read_text())["resolution"]

observed_files = sorted(
    path.relative_to(bundle).as_posix()
    for path in bundle.iterdir()
    if path.is_file()
)
file_hashes = {
    name: hashlib.sha256((bundle / name).read_bytes()).hexdigest()
    for name in ("klean_export.py", "klean.py")
}
image_id = generator["provenance"]["generator_image_id"]

result = {
    "observed_regular_files": observed_files,
    "observed_file_hashes": file_hashes,
    "generator_manifest_expected": {
        "klean_export.py": generator["exporter_sha256"],
        "klean.py": generator["klean_py_sha256"],
    },
    "source_manifest_expected": source["files"],
    "generator_manifest_image_id": image_id,
    "source_manifest_image_id": source["generator_image_id"],
    "audit_input_path_image_key": Path(
        audit["generation_producer_sources"]
    ).name,
    "observed_bundle_tree_sha256": sha256_tree(bundle),
    "audit_input_bundle_tree_sha256": audit["hashes"][
        "generation_producer_sources_sha256"
    ],
}
checks = {
    "exact_file_set": observed_files
    == ["klean.py", "klean_export.py", "source-manifest.json"],
    "files_match_generator_manifest": file_hashes
    == result["generator_manifest_expected"],
    "files_match_source_manifest": file_hashes
    == result["source_manifest_expected"],
    "image_ids_match": image_id == source["generator_image_id"],
    "audit_path_encodes_image_id": (
        result["audit_input_path_image_key"]
        == image_id.removeprefix("sha256:")
    ),
    "bundle_tree_matches_audit_input": (
        result["observed_bundle_tree_sha256"]
        == result["audit_input_bundle_tree_sha256"]
    ),
}
result["checks"] = checks
print(json.dumps(result, indent=2, sort_keys=True))
if not all(checks.values()):
    raise SystemExit(1)
