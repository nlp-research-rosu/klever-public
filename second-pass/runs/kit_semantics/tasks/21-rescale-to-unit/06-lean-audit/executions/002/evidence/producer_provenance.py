#!/usr/bin/env python3
"""Generation-time producer provenance gate."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from tools.pipeline_contract import sha256_tree


source_root = Path("/reference/generation-tools")
source_manifest = json.loads(
    (source_root / "source-manifest.json").read_text()
)
generator_manifest = json.loads(
    Path(
        "/reference/klean-generation/generator-manifest.json"
    ).read_text()
)
audit = json.loads(Path("/audit-input.json").read_text())["resolution"]

actual = {
    name: hashlib.sha256((source_root / name).read_bytes()).hexdigest()
    for name in ("klean_export.py", "klean.py")
}
launcher_image_id = (
    "sha256:" + Path(audit["generation_producer_sources"]).name
)
checks = {
    "klean_export_hash_matches": (
        actual["klean_export.py"]
        == source_manifest["files"]["klean_export.py"]
        == generator_manifest["exporter_sha256"]
    ),
    "klean_hash_matches": (
        actual["klean.py"]
        == source_manifest["files"]["klean.py"]
        == generator_manifest["klean_py_sha256"]
    ),
    "producer_tree_matches_audit_input": (
        sha256_tree(source_root)
        == audit["hashes"]["generation_producer_sources_sha256"]
    ),
    "generator_image_id_matches": (
        source_manifest["generator_image_id"]
        == generator_manifest["provenance"]["generator_image_id"]
        == launcher_image_id
    ),
}
print("actual_file_hashes:", json.dumps(actual, sort_keys=True))
print("actual_producer_tree_sha256:", sha256_tree(source_root))
print("source_manifest_image_id:", source_manifest["generator_image_id"])
print(
    "generator_manifest_image_id:",
    generator_manifest["provenance"]["generator_image_id"],
)
print("audit_input_launcher_image_id:", launcher_image_id)
for name, result in checks.items():
    print(f"{name}: {result}")
print("PRODUCER_PROVENANCE_PASS:", all(checks.values()))
