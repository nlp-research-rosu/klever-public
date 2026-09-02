#!/usr/bin/env python3
"""Independent producer-provenance and K rule-inventory reconstruction."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from tools import k_rule_inventory, klean_export, pipeline_contract


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


audit_input = json.loads(Path("/audit-input.json").read_text())
source_manifest = json.loads(
    Path("/reference/generation-tools/source-manifest.json").read_text()
)
generator_manifest = json.loads(
    Path("/reference/klean-generation/generator-manifest.json").read_text()
)
discovery = json.loads(Path("/reference/lemma-discovery.json").read_text())

producer_hashes = {
    name: sha256(Path("/reference/generation-tools") / name)
    for name in ("klean_export.py", "klean.py")
}
producer_tree_hash = klean_export.tree_digest(
    Path("/reference/generation-tools")
)
producer_launcher_tree_hash = pipeline_contract.sha256_tree(
    Path("/reference/generation-tools")
)
audit_producer_path = Path(
    audit_input["resolution"]["generation_producer_sources"]
)
audit_generator_image_id = "sha256:" + audit_producer_path.name
source_generator_image_id = source_manifest["generator_image_id"]
manifest_generator_image_id = generator_manifest["provenance"][
    "generator_image_id"
]

print("PRODUCER PROVENANCE")
print(json.dumps({
    "computed_file_sha256": producer_hashes,
    "source_manifest_files": source_manifest["files"],
    "generator_manifest_exporter_sha256": generator_manifest["exporter_sha256"],
    "generator_manifest_klean_py_sha256": generator_manifest["klean_py_sha256"],
    "computed_klean_tree_digest": producer_tree_hash,
    "computed_launcher_sha256_tree": producer_launcher_tree_hash,
    "audit_input_producer_tree_sha256": audit_input["resolution"]["hashes"][
        "generation_producer_sources_sha256"
    ],
    "audit_input_generator_image_id_from_path": audit_generator_image_id,
    "source_manifest_generator_image_id": source_generator_image_id,
    "generator_manifest_generator_image_id": manifest_generator_image_id,
}, indent=2, sort_keys=True))

assert producer_hashes == source_manifest["files"]
assert producer_hashes["klean_export.py"] == generator_manifest["exporter_sha256"]
assert producer_hashes["klean.py"] == generator_manifest["klean_py_sha256"]
assert producer_launcher_tree_hash == audit_input["resolution"]["hashes"][
    "generation_producer_sources_sha256"
]
assert audit_generator_image_id == source_generator_image_id
assert source_generator_image_id == manifest_generator_image_id
print("PRODUCER_PROVENANCE_MATCH=true")

inventory = k_rule_inventory.inventory_verification(
    Path("/reference/k-proof")
)
print("\nRECONSTRUCTED INVENTORY")
print(json.dumps(inventory, indent=2, sort_keys=True))

inventory_rules = inventory["rules"]
discovery_rules = discovery["rules"]
inventory_ids = [rule["source_rule_id"] for rule in inventory_rules]
discovery_ids = [rule["source_rule_id"] for rule in discovery_rules]
comparison = {
    "inventory_rule_count": len(inventory_rules),
    "discovery_rule_count": len(discovery_rules),
    "inventory_unique_ids": len(set(inventory_ids)),
    "discovery_unique_ids": len(set(discovery_ids)),
    "same_ordered_identities": inventory_ids == discovery_ids,
    "omitted_by_discovery": [item for item in inventory_ids if item not in discovery_ids],
    "extra_in_discovery": [item for item in discovery_ids if item not in inventory_ids],
    "reconstructed_inventory_sha256": inventory["inventory_sha256"],
    "discovery_inventory_sha256": discovery["inventory_sha256"],
}
print("\nBIJECTIVE COMPARISON")
print(json.dumps(comparison, indent=2, sort_keys=True))

assert discovery.get("schema_version") == 2
assert comparison["inventory_rule_count"] == comparison["discovery_rule_count"]
assert comparison["inventory_unique_ids"] == len(inventory_ids)
assert comparison["discovery_unique_ids"] == len(discovery_ids)
assert comparison["same_ordered_identities"]
assert not comparison["omitted_by_discovery"]
assert not comparison["extra_in_discovery"]
assert inventory["inventory_sha256"] == discovery["inventory_sha256"]
for rule in inventory_rules:
    assert rule["source_rule_id"] == "rule-" + rule["normalized_sha256"]
print("INVENTORY_BIJECTION_MATCH=true")
