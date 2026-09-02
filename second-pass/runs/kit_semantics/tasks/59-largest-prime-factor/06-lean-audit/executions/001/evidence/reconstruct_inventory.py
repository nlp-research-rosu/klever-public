#!/usr/bin/env python3
import json
from pathlib import Path

from tools.k_rule_inventory import inventory_verification
from tools.lemma_discovery_contract import validate_trust_boundary

workspace = Path("/reference/k-proof")
manifest = Path("/reference/lemma-discovery.json")
inventory = inventory_verification(workspace)
validated = validate_trust_boundary(workspace, manifest)
document = json.loads(manifest.read_text())
inventory_ids = [rule["source_rule_id"] for rule in inventory["rules"]]
manifest_ids = [rule["source_rule_id"] for rule in document["rules"]]
print(json.dumps(inventory, indent=2, sort_keys=True))
print(json.dumps({
    "ids_exact_order_equal": inventory_ids == manifest_ids,
    "inventory_ids_unique": len(inventory_ids) == len(set(inventory_ids)),
    "manifest_ids_unique": len(manifest_ids) == len(set(manifest_ids)),
    "inventory_sha256_equal": (
        inventory["inventory_sha256"] == document["inventory_sha256"]
    ),
    "definition_count": len(validated["definitions"]),
    "operational_count": len(validated["operational_rules"]),
    "derived_count": len(validated["proved_derived_lemmas"]),
    "domain_count": len(validated["domain_lemmas"]),
}, indent=2, sort_keys=True))
