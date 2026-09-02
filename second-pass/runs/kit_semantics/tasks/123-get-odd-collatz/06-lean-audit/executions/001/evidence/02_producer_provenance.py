#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

from tools.pipeline_contract import sha256_tree


audit_input = json.loads(Path("/audit-input.json").read_text())
generator_manifest = json.loads(
    Path("/reference/klean-generation/generator-manifest.json").read_text()
)
source_manifest = json.loads(
    Path("/reference/generation-tools/source-manifest.json").read_text()
)

producer_root = Path("/reference/generation-tools")
observed_files = {
    name: hashlib.sha256((producer_root / name).read_bytes()).hexdigest()
    for name in ("klean_export.py", "klean.py")
}
observed_tree = sha256_tree(producer_root)
audit_resolution = audit_input["resolution"]
audit_bundle = Path(audit_resolution["generation_producer_sources"])
audit_image_id = f"sha256:{audit_bundle.name}"
generator_image_id = generator_manifest["provenance"]["generator_image_id"]

result = {
    "observed_files": observed_files,
    "observed_tree_sha256": observed_tree,
    "expected_from_generator_manifest": {
        "klean_export.py": generator_manifest["exporter_sha256"],
        "klean.py": generator_manifest["klean_py_sha256"],
    },
    "source_manifest": source_manifest,
    "generator_manifest_image_id": generator_image_id,
    "audit_input_bundle_path": str(audit_bundle),
    "audit_input_image_id_from_bundle_path": audit_image_id,
    "audit_input_tree_sha256": audit_resolution["hashes"][
        "generation_producer_sources_sha256"
    ],
    "checks": {
        "file_hashes_match_generator_manifest": observed_files
        == {
            "klean_export.py": generator_manifest["exporter_sha256"],
            "klean.py": generator_manifest["klean_py_sha256"],
        },
        "file_hashes_match_source_manifest": observed_files
        == source_manifest["files"],
        "image_id_matches_all_records": (
            generator_image_id
            == source_manifest["generator_image_id"]
            == audit_image_id
        ),
        "tree_hash_matches_audit_input": (
            observed_tree
            == audit_resolution["hashes"][
                "generation_producer_sources_sha256"
            ]
        ),
        "exact_bundle_file_set": sorted(
            path.relative_to(producer_root).as_posix()
            for path in producer_root.rglob("*")
            if path.is_file()
        )
        == ["klean.py", "klean_export.py", "source-manifest.json"],
    },
}

print(json.dumps(result, indent=2, sort_keys=True))
