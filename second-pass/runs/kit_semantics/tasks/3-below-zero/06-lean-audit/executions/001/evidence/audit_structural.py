#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

from tools import (
    k_rule_inventory,
    klean_export,
    lemma_discovery_contract,
    pipeline_contract,
    stage6_resolution_contract,
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


audit = json.loads(Path("/audit-input.json").read_text())
source_manifest = json.loads(
    Path("/reference/generation-tools/source-manifest.json").read_text()
)
generator_manifest = json.loads(
    Path("/reference/klean-generation/generator-manifest.json").read_text()
)
discovery_path = Path("/reference/lemma-discovery.json")
discovery = json.loads(discovery_path.read_text())

producer_hashes = {
    name: sha256(Path("/reference/generation-tools") / name)
    for name in ("klean_export.py", "klean.py")
}
producer_tree = pipeline_contract.sha256_tree(
    Path("/reference/generation-tools")
)
recorded_image = source_manifest["generator_image_id"]
path_image = "sha256:" + Path(
    audit["resolution"]["generation_producer_sources"]
).name

print("PRODUCER_PROVENANCE")
print(json.dumps({
    "actual_file_hashes": producer_hashes,
    "source_manifest_file_hashes": source_manifest["files"],
    "generator_manifest_file_hashes": {
        "klean_export.py": generator_manifest["exporter_sha256"],
        "klean.py": generator_manifest["klean_py_sha256"],
    },
    "actual_tree_sha256": producer_tree,
    "audit_input_tree_sha256": audit["resolution"]["hashes"][
        "generation_producer_sources_sha256"
    ],
    "source_manifest_image_id": recorded_image,
    "generator_manifest_image_id": generator_manifest["provenance"][
        "generator_image_id"
    ],
    "audit_input_path_image_id": path_image,
    "all_file_hashes_match": producer_hashes == source_manifest["files"] == {
        "klean_export.py": generator_manifest["exporter_sha256"],
        "klean.py": generator_manifest["klean_py_sha256"],
    },
    "tree_hash_matches": producer_tree == audit["resolution"]["hashes"][
        "generation_producer_sources_sha256"
    ],
    "image_ids_match": recorded_image
        == generator_manifest["provenance"]["generator_image_id"]
        == path_image,
}, indent=2, sort_keys=True))

resolution = audit["resolution"]
mounted_hashes = {
    "k_workspace_sha256": pipeline_contract.sha256_tree(
        Path("/reference/k-proof")
    ),
    "stage1_export_sha256": klean_export.tree_digest(
        Path("/reference/k-proof")
    ),
    "discovery_manifest_sha256": sha256(discovery_path),
    "k_audit_sha256": pipeline_contract.sha256_tree(
        Path("/reference/k-audit")
    ),
    "klean_generation_sha256": pipeline_contract.sha256_tree(
        Path("/reference/klean-generation")
    ),
    "generation_producer_sources_sha256": producer_tree,
    "generated_tree_sha256": klean_export.tree_digest(
        Path("/reference/klean-generation/generated")
    ),
    "lean_workspace_sha256": pipeline_contract.sha256_tree(
        Path("/candidate")
    ),
}
recorded_hashes = resolution["hashes"]
print("MOUNTED_INPUT_HASHES")
print(json.dumps({
    "mounted": mounted_hashes,
    "recorded": {
        key: recorded_hashes[key] for key in mounted_hashes
    },
    "per_hash_match": {
        key: mounted_hashes[key] == recorded_hashes[key]
        for key in mounted_hashes
    },
    "signed_resolution_digest_actual": (
        stage6_resolution_contract.canonical_json_sha256(resolution)
    ),
    "signed_resolution_digest_recorded": audit["resolved_input_sha256"],
    "signed_resolution_digest_match": (
        stage6_resolution_contract.canonical_json_sha256(resolution)
        == audit["resolved_input_sha256"]
    ),
}, indent=2, sort_keys=True))

inventory = k_rule_inventory.inventory_verification(Path("/reference/k-proof"))
validated = lemma_discovery_contract.validate_trust_boundary(
    Path("/reference/k-proof"), discovery_path
)
canonical_ids = [r["source_rule_id"] for r in inventory["rules"]]
discovery_ids = [r["source_rule_id"] for r in discovery["rules"]]
print("INVENTORY_RECONSTRUCTION")
print(json.dumps({
    "verification_sha256": inventory["verification_sha256"],
    "verification_module": inventory["verification_module"],
    "verification_modules": inventory["verification_modules"],
    "required_files_sha256": inventory.get("required_files_sha256", {}),
    "inventory_sha256": inventory["inventory_sha256"],
    "manifest_inventory_sha256": discovery["inventory_sha256"],
    "rule_count": len(inventory["rules"]),
    "manifest_rule_count": len(discovery["rules"]),
    "canonical_ids": canonical_ids,
    "manifest_ids": discovery_ids,
    "ordered_identity_match": canonical_ids == discovery_ids,
    "unique_canonical_ids": len(canonical_ids) == len(set(canonical_ids)),
    "unique_manifest_ids": len(discovery_ids) == len(set(discovery_ids)),
    "contract_validation": "PASS",
}, indent=2, sort_keys=True))
print("CANONICAL_RULES")
print(json.dumps(inventory["rules"], indent=2, sort_keys=True))
print("CLASSIFIED_RULES_IN_CANONICAL_ORDER")
classified = {
    r["source_rule_id"]: {
        "classification": r["classification"],
        "rationale": r["rationale"],
    }
    for r in discovery["rules"]
}
print(json.dumps([
    {**r, **classified[r["source_rule_id"]]}
    for r in inventory["rules"]
], indent=2, sort_keys=True))
print("VALIDATED_COUNTS")
print(json.dumps({
    key: len(validated[key])
    for key in (
        "definitions", "operational_rules", "proved_derived_lemmas",
        "domain_lemmas",
    )
}, indent=2, sort_keys=True))
