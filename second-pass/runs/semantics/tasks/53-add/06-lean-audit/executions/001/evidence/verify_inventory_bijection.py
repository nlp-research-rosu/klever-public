#!/usr/bin/env python3

import hashlib
import json
from pathlib import Path

from tools.k_rule_inventory import canonical_json_sha256, inventory_verification
from tools.lemma_discovery_contract import validate_trust_boundary


workspace = Path("/reference/k-proof")
discovery_path = Path("/reference/lemma-discovery.json")

inventory = inventory_verification(workspace)
discovery = json.loads(discovery_path.read_text())
validated = validate_trust_boundary(workspace, discovery_path)

inventory_ids = [rule["source_rule_id"] for rule in inventory["rules"]]
discovery_ids = [rule["source_rule_id"] for rule in discovery["rules"]]

rule_checks = []
for index, rule in enumerate(inventory["rules"]):
    normalized = " ".join(rule["text"].split())
    normalized_sha256 = hashlib.sha256(normalized.encode()).hexdigest()
    source_rule_id = f"rule-{normalized_sha256}"
    classification = discovery["rules"][index]["classification"]
    rule_checks.append(
        {
            "index": index,
            "module": rule["module"],
            "source_span": {
                "start_line": rule["start_line"],
                "end_line": rule["end_line"],
            },
            "attributes": rule["attributes"],
            "recomputed_normalized_sha256": normalized_sha256,
            "recorded_normalized_sha256": rule["normalized_sha256"],
            "recomputed_source_rule_id": source_rule_id,
            "recorded_source_rule_id": rule["source_rule_id"],
            "discovery_source_rule_id": discovery_ids[index],
            "classification": classification,
            "normalized_hash_matches": normalized_sha256
            == rule["normalized_sha256"],
            "source_rule_id_matches": source_rule_id
            == rule["source_rule_id"]
            == discovery_ids[index],
            "simplification": "simplification" in rule["attributes"],
        }
    )

classification_counts = {}
for rule in discovery["rules"]:
    classification_counts[rule["classification"]] = (
        classification_counts.get(rule["classification"], 0) + 1
    )

result = {
    "verification_file": inventory["verification_file"],
    "verification_module": inventory["verification_module"],
    "local_verification_module_closure": inventory[
        "verification_modules"
    ],
    "verification_sha256": inventory["verification_sha256"],
    "rule_count": len(inventory["rules"]),
    "inventory_ids": inventory_ids,
    "discovery_ids": discovery_ids,
    "inventory_ids_unique": len(inventory_ids) == len(set(inventory_ids)),
    "discovery_ids_unique": len(discovery_ids) == len(set(discovery_ids)),
    "ordered_identity_bijection": inventory_ids == discovery_ids,
    "recomputed_inventory_sha256": canonical_json_sha256(inventory["rules"]),
    "inventory_tool_inventory_sha256": inventory["inventory_sha256"],
    "discovery_inventory_sha256": discovery["inventory_sha256"],
    "inventory_hashes_all_match": (
        canonical_json_sha256(inventory["rules"])
        == inventory["inventory_sha256"]
        == discovery["inventory_sha256"]
    ),
    "validated_contract_inventory_sha256": validated["inventory_sha256"],
    "classification_counts": classification_counts,
    "all_inventory_entries_classified_once": len(discovery["rules"])
    == len(inventory["rules"]),
    "simplification_rule_count": sum(
        "simplification" in rule["attributes"]
        for rule in inventory["rules"]
    ),
    "rule_checks": rule_checks,
}

print(json.dumps(result, indent=2, sort_keys=True))
