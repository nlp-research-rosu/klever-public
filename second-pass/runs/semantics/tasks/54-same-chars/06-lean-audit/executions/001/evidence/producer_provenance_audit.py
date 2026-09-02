#!/usr/bin/env python3
import hashlib
import json
import stat
from pathlib import Path

from tools.pipeline_contract import sha256_tree


bundle = Path("/reference/generation-tools")
generation = Path("/reference/klean-generation")
audit_input = json.loads(Path("/audit-input.json").read_text())
generator = json.loads((generation / "generator-manifest.json").read_text())
source_manifest = json.loads((bundle / "source-manifest.json").read_text())
resolution = audit_input["resolution"]
provenance = generator["provenance"]

observed_files = {}
entry_kinds = {}
for path in sorted(bundle.iterdir()):
    mode = path.lstat().st_mode
    entry_kinds[path.name] = (
        "regular"
        if stat.S_ISREG(mode)
        else "directory"
        if stat.S_ISDIR(mode)
        else "unsafe"
    )
    if stat.S_ISREG(mode):
        observed_files[path.name] = hashlib.sha256(path.read_bytes()).hexdigest()

expected_producer_files = {
    "klean_export.py": generator["exporter_sha256"],
    "klean.py": generator["klean_py_sha256"],
}
recorded_bundle_path = Path(resolution["generation_producer_sources"])
image_id_from_audit_path = f"sha256:{recorded_bundle_path.name}"
bundle_sha256 = sha256_tree(bundle)

checks = {
    "source_manifest_exact_keys": set(source_manifest)
    == {"schema_version", "generator_image_id", "files"},
    "source_manifest_schema": source_manifest["schema_version"] == 1,
    "bundle_exact_entry_set": set(entry_kinds)
    == {"source-manifest.json", "klean_export.py", "klean.py"},
    "bundle_all_regular": set(entry_kinds.values()) == {"regular"},
    "producer_file_hashes_match_generator": {
        name: observed_files.get(name) == expected
        for name, expected in expected_producer_files.items()
    },
    "source_manifest_files_match_generator": (
        source_manifest["files"] == expected_producer_files
    ),
    "source_manifest_image_matches_generator": (
        source_manifest["generator_image_id"]
        == provenance["generator_image_id"]
    ),
    "audit_path_image_matches_generator": (
        image_id_from_audit_path == provenance["generator_image_id"]
    ),
    "bundle_tree_hash_matches_audit_input": (
        bundle_sha256
        == resolution["hashes"]["generation_producer_sources_sha256"]
    ),
}

print(
    json.dumps(
        {
            "observed_file_sha256": observed_files,
            "entry_kinds": entry_kinds,
            "expected_producer_files_from_generator_manifest": (
                expected_producer_files
            ),
            "source_manifest": source_manifest,
            "generator_image_id": provenance["generator_image_id"],
            "audit_recorded_bundle_path": str(recorded_bundle_path),
            "image_id_from_audit_path": image_id_from_audit_path,
            "bundle_tree_sha256": bundle_sha256,
            "audit_recorded_bundle_tree_sha256": resolution["hashes"][
                "generation_producer_sources_sha256"
            ],
            "checks": checks,
        },
        indent=2,
        sort_keys=True,
    )
)

assert checks["source_manifest_exact_keys"]
assert checks["source_manifest_schema"]
assert checks["bundle_exact_entry_set"]
assert checks["bundle_all_regular"]
assert all(checks["producer_file_hashes_match_generator"].values())
assert checks["source_manifest_files_match_generator"]
assert checks["source_manifest_image_matches_generator"]
assert checks["audit_path_image_matches_generator"]
assert checks["bundle_tree_hash_matches_audit_input"]
