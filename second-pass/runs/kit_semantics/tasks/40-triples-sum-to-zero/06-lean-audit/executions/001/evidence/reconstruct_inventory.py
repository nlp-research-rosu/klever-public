#!/usr/bin/env python3
import json
from pathlib import Path

from tools.k_rule_inventory import inventory_verification
from tools.lemma_discovery_contract import validate_trust_boundary


workspace = Path("/reference/k-proof")
manifest_path = Path("/reference/lemma-discovery.json")

inventory = inventory_verification(workspace)
manifest = json.loads(manifest_path.read_text())
validated = validate_trust_boundary(workspace, manifest_path)

canonical_ids = [rule["source_rule_id"] for rule in inventory["rules"]]
manifest_ids = [rule["source_rule_id"] for rule in manifest["rules"]]

summary = {
    "verification_file": inventory["verification_file"],
    "verification_sha256": inventory["verification_sha256"],
    "verification_module": inventory["verification_module"],
    "verification_modules": inventory["verification_modules"],
    "rule_count": len(inventory["rules"]),
    "inventory_sha256": inventory["inventory_sha256"],
    "manifest_inventory_sha256": manifest["inventory_sha256"],
    "contract_validation": "PASS",
    "canonical_ids_unique": len(canonical_ids) == len(set(canonical_ids)),
    "manifest_ids_unique": len(manifest_ids) == len(set(manifest_ids)),
    "same_ordered_identities": canonical_ids == manifest_ids,
    "same_identity_set": set(canonical_ids) == set(manifest_ids),
    "definitions": len(validated["definitions"]),
    "operational_rules": len(validated["operational_rules"]),
    "proved_derived_lemmas": len(validated["proved_derived_lemmas"]),
    "domain_lemmas": len(validated["domain_lemmas"]),
}

print(json.dumps(summary, indent=2, sort_keys=True))
print("CANONICAL INVENTORY:")
print(json.dumps(inventory, indent=2, sort_keys=True))
