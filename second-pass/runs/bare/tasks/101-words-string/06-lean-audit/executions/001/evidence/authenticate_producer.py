#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

from tools.pipeline_contract import sha256_tree


generation_tools = Path("/reference/generation-tools")
generation = Path("/reference/klean-generation")
audit_input = json.loads(Path("/audit-input.json").read_text())
source_manifest = json.loads(
    (generation_tools / "source-manifest.json").read_text()
)
generator_manifest = json.loads(
    (generation / "generator-manifest.json").read_text()
)
resolution = audit_input["resolution"]

actual_file_hashes = {
    name: hashlib.sha256((generation_tools / name).read_bytes()).hexdigest()
    for name in ("klean_export.py", "klean.py")
}
checks = {
    "actual_file_hashes": actual_file_hashes,
    "source_manifest_file_hashes": source_manifest["files"],
    "generator_manifest_file_hashes": {
        "klean_export.py": generator_manifest["exporter_sha256"],
        "klean.py": generator_manifest["klean_py_sha256"],
    },
    "generation_tools_tree_sha256_actual": sha256_tree(generation_tools),
    "generation_tools_tree_sha256_audit_input": resolution["hashes"][
        "generation_producer_sources_sha256"
    ],
    "source_manifest_image_id": source_manifest["generator_image_id"],
    "generator_manifest_image_id": generator_manifest["provenance"][
        "generator_image_id"
    ],
    "audit_input_producer_path": resolution["generation_producer_sources"],
    "audit_input_producer_path_image_id": "sha256:"
    + Path(resolution["generation_producer_sources"]).name,
}

checks["all_individual_hashes_match"] = (
    checks["actual_file_hashes"]
    == checks["source_manifest_file_hashes"]
    == checks["generator_manifest_file_hashes"]
)
checks["tree_hash_matches_audit_input"] = (
    checks["generation_tools_tree_sha256_actual"]
    == checks["generation_tools_tree_sha256_audit_input"]
)
checks["all_image_ids_match"] = (
    checks["source_manifest_image_id"]
    == checks["generator_manifest_image_id"]
    == checks["audit_input_producer_path_image_id"]
)
print(json.dumps(checks, indent=2, sort_keys=True))

if not all(
    checks[key]
    for key in (
        "all_individual_hashes_match",
        "tree_hash_matches_audit_input",
        "all_image_ids_match",
    )
):
    raise SystemExit(1)
