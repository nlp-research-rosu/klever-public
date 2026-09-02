#!/usr/bin/env python3
"""Verify immutable Stage 4 producer provenance against all recorded sources."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from tools.pipeline_contract import sha256_tree


bundle = Path("/reference/generation-tools")
source_manifest = json.loads((bundle / "source-manifest.json").read_text())
generator_manifest = json.loads(
    Path("/reference/klean-generation/generator-manifest.json").read_text()
)
audit_input = json.loads(Path("/audit-input.json").read_text())["resolution"]

observed_files = sorted(path.name for path in bundle.iterdir())
assert observed_files == ["klean.py", "klean_export.py", "source-manifest.json"]

observed_hashes = {
    name: hashlib.sha256((bundle / name).read_bytes()).hexdigest()
    for name in ("klean_export.py", "klean.py")
}
assert observed_hashes == source_manifest["files"]
assert observed_hashes["klean_export.py"] == generator_manifest["exporter_sha256"]
assert observed_hashes["klean.py"] == generator_manifest["klean_py_sha256"]

image_id = source_manifest["generator_image_id"]
assert image_id == generator_manifest["provenance"]["generator_image_id"]
assert audit_input["generation_producer_sources"].endswith(
    "/" + image_id.removeprefix("sha256:")
)

bundle_hash = sha256_tree(bundle)
assert (
    bundle_hash
    == audit_input["hashes"]["generation_producer_sources_sha256"]
)

print("PRODUCER_PROVENANCE: PASS")
print(f"GENERATOR_IMAGE_ID: {image_id}")
print(f"KLEAN_EXPORT_SHA256: {observed_hashes['klean_export.py']}")
print(f"KLEAN_PY_SHA256: {observed_hashes['klean.py']}")
print(f"PRODUCER_BUNDLE_SHA256: {bundle_hash}")
