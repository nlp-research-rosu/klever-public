#!/usr/bin/env python3
import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, "/reference")
from tools.pipeline_contract import sha256_tree

producer_dir = Path("/reference/generation-tools")
generator_manifest = json.loads(
    Path("/reference/klean-generation/generator-manifest.json").read_text()
)
source_manifest = json.loads(
    (producer_dir / "source-manifest.json").read_text()
)
audit_input = json.loads(Path("/audit-input.json").read_text())

actual_files = {
    name: hashlib.sha256((producer_dir / name).read_bytes()).hexdigest()
    for name in ("klean_export.py", "klean.py")
}
actual_tree = sha256_tree(producer_dir)
generator_files = {
    "klean_export.py": generator_manifest["exporter_sha256"],
    "klean.py": generator_manifest["klean_py_sha256"],
}
source_files = source_manifest["files"]
image_ids = {
    "generator_manifest": generator_manifest["provenance"]["generator_image_id"],
    "source_manifest": source_manifest["generator_image_id"],
    "audit_input_path_component": "sha256:"
    + Path(audit_input["resolution"]["generation_producer_sources"]).name,
}
expected_tree = audit_input["resolution"]["hashes"][
    "generation_producer_sources_sha256"
]

checks = {
    "actual_matches_generator_manifest": actual_files == generator_files,
    "actual_matches_source_manifest": actual_files == source_files,
    "image_ids_match": len(set(image_ids.values())) == 1,
    "producer_tree_matches_audit_input": actual_tree == expected_tree,
}
print(
    json.dumps(
        {
            "actual_files": actual_files,
            "actual_tree_sha256": actual_tree,
            "expected_tree_sha256": expected_tree,
            "generator_manifest_files": generator_files,
            "source_manifest_files": source_files,
            "image_ids": image_ids,
            "checks": checks,
            "all_checks_pass": all(checks.values()),
        },
        indent=2,
        sort_keys=True,
    )
)
