#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

from tools.pipeline_contract import sha256_tree


bundle = Path("/reference/generation-tools")
generation_manifest_path = Path("/reference/klean-generation/generator-manifest.json")
audit_input_path = Path("/audit-input.json")

source_manifest = json.loads((bundle / "source-manifest.json").read_text())
generation_manifest = json.loads(generation_manifest_path.read_text())
audit_input = json.loads(audit_input_path.read_text())["resolution"]

actual_files = sorted(
    path.relative_to(bundle).as_posix()
    for path in bundle.rglob("*")
    if path.is_file()
)
expected_files = ["klean.py", "klean_export.py", "source-manifest.json"]
assert actual_files == expected_files, (actual_files, expected_files)

expected_hashes = {
    "klean.py": generation_manifest["klean_py_sha256"],
    "klean_export.py": generation_manifest["exporter_sha256"],
}
assert source_manifest["files"] == expected_hashes

observed_hashes = {
    name: hashlib.sha256((bundle / name).read_bytes()).hexdigest()
    for name in expected_hashes
}
assert observed_hashes == expected_hashes

image_id = generation_manifest["provenance"]["generator_image_id"]
assert source_manifest["generator_image_id"] == image_id
assert Path(audit_input["generation_producer_sources"]).name == image_id.removeprefix(
    "sha256:"
)

bundle_hash = sha256_tree(bundle)
assert bundle_hash == audit_input["hashes"]["generation_producer_sources_sha256"]

print(
    json.dumps(
        {
            "status": "PASS",
            "actual_files": actual_files,
            "observed_hashes": observed_hashes,
            "generator_image_id": image_id,
            "audit_input_bundle_key": Path(
                audit_input["generation_producer_sources"]
            ).name,
            "bundle_tree_sha256": bundle_hash,
        },
        indent=2,
        sort_keys=True,
    )
)
