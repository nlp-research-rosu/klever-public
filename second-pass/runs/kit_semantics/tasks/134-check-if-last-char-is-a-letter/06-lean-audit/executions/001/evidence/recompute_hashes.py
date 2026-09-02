#!/usr/bin/env python3
import hashlib
import json
import os
from pathlib import Path

from tools import klean_export, pipeline_contract

audit_input = json.loads(Path("/audit-input.json").read_text())
resolution = audit_input["resolution"]
expected = resolution["hashes"]
generator_manifest = json.loads(
    Path("/reference/klean-generation/generator-manifest.json").read_text()
)
source_manifest = json.loads(
    Path("/reference/generation-tools/source-manifest.json").read_text()
)


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


observed = {
    "audit_mode_env": os.environ.get("AUDIT_MODE"),
    "audit_mode_input": resolution["mode"],
    "condition": resolution["condition"],
    "semantics_mode": resolution["semantics_mode"],
    "k_workspace_sha256": pipeline_contract.sha256_tree(
        Path("/reference/k-proof")
    ),
    "stage1_export_sha256": klean_export.tree_digest(
        Path("/reference/k-proof")
    ),
    "discovery_manifest_sha256": file_sha256(
        Path("/reference/lemma-discovery.json")
    ),
    "k_audit_sha256": pipeline_contract.sha256_tree(
        Path("/reference/k-audit")
    ),
    "klean_generation_sha256": pipeline_contract.sha256_tree(
        Path("/reference/klean-generation")
    ),
    "generation_producer_sources_sha256": pipeline_contract.sha256_tree(
        Path("/reference/generation-tools")
    ),
    "generated_tree_sha256": klean_export.tree_digest(
        Path("/reference/klean-generation/generated")
    ),
    "lean_workspace_sha256": pipeline_contract.sha256_tree(
        Path("/candidate")
    ),
}

producer_hashes = {
    name: file_sha256(Path("/reference/generation-tools") / name)
    for name in ("klean_export.py", "klean.py")
}
producer_image_key_from_launcher_path = Path(
    resolution["generation_producer_sources"]
).name
manifest_image_id = generator_manifest["provenance"]["generator_image_id"]

comparison = {
    key: {
        "observed": value,
        "expected": expected.get(key),
        "matches": value == expected.get(key),
    }
    for key, value in observed.items()
    if key in expected
}

result = {
    "observed": observed,
    "comparison": comparison,
    "all_available_launcher_hashes_match": all(
        entry["matches"] for entry in comparison.values()
    ),
    "producer_hashes": producer_hashes,
    "producer_hashes_match_source_manifest": (
        producer_hashes == source_manifest["files"]
    ),
    "producer_hashes_match_generator_manifest": (
        producer_hashes["klean_export.py"]
        == generator_manifest["exporter_sha256"]
        and producer_hashes["klean.py"]
        == generator_manifest["klean_py_sha256"]
    ),
    "source_manifest_image_id": source_manifest["generator_image_id"],
    "generator_manifest_image_id": manifest_image_id,
    "launcher_path_image_key": producer_image_key_from_launcher_path,
    "image_identity_matches": (
        source_manifest["generator_image_id"] == manifest_image_id
        and manifest_image_id
        == "sha256:" + producer_image_key_from_launcher_path
    ),
    "source_manifest_exact_files": (
        set(source_manifest["files"])
        == {"klean_export.py", "klean.py"}
    ),
}

print(json.dumps(result, indent=2, sort_keys=True))
