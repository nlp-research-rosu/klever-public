#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

from tools import pipeline_contract


AUDIT_INPUT = Path("/audit-input.json")
BUNDLE = Path("/reference/generation-tools")
GENERATOR_MANIFEST = Path("/reference/klean-generation/generator-manifest.json")


def read_json(path: Path) -> dict:
    value = json.loads(path.read_text())
    if not isinstance(value, dict):
        raise AssertionError(f"{path} is not a JSON object")
    return value


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


audit = read_json(AUDIT_INPUT)
source_manifest = read_json(BUNDLE / "source-manifest.json")
generator_manifest = read_json(GENERATOR_MANIFEST)
resolution = audit["resolution"]
provenance = generator_manifest["provenance"]

actual_files = sorted(
    path.relative_to(BUNDLE).as_posix()
    for path in BUNDLE.rglob("*")
    if path.is_file()
)
expected_files = ["klean.py", "klean_export.py", "source-manifest.json"]
assert actual_files == expected_files, (actual_files, expected_files)

observed = {
    "klean.py": file_sha256(BUNDLE / "klean.py"),
    "klean_export.py": file_sha256(BUNDLE / "klean_export.py"),
}
manifest_expected = {
    "klean.py": generator_manifest["klean_py_sha256"],
    "klean_export.py": generator_manifest["exporter_sha256"],
}
assert source_manifest == {
    "schema_version": 1,
    "generator_image_id": provenance["generator_image_id"],
    "files": manifest_expected,
}
assert observed == manifest_expected

image_id = provenance["generator_image_id"]
assert image_id.startswith("sha256:")
image_digest = image_id.removeprefix("sha256:")
recorded_bundle = Path(resolution["generation_producer_sources"])
assert recorded_bundle.name == image_digest

tree_sha256 = pipeline_contract.sha256_tree(BUNDLE)
assert (
    tree_sha256
    == resolution["hashes"]["generation_producer_sources_sha256"]
)

print("actual_files =", actual_files)
print("observed_file_hashes =", json.dumps(observed, sort_keys=True))
print("source_manifest_files =", json.dumps(source_manifest["files"], sort_keys=True))
print("generator_manifest_hashes =", json.dumps(manifest_expected, sort_keys=True))
print("generator_manifest_image_id =", image_id)
print("source_manifest_image_id =", source_manifest["generator_image_id"])
print("audit_input_recorded_bundle =", recorded_bundle)
print("audit_input_bundle_key =", recorded_bundle.name)
print("producer_bundle_tree_sha256 =", tree_sha256)
print(
    "audit_input_producer_bundle_tree_sha256 =",
    resolution["hashes"]["generation_producer_sources_sha256"],
)
print("RESULT: PASS")
