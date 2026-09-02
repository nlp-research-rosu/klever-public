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
classified_ids = [rule["source_rule_id"] for rule in manifest["rules"]]
classification_by_id = {
    rule["source_rule_id"]: {
        "classification": rule["classification"],
        "rationale": rule["rationale"],
    }
    for rule in manifest["rules"]
}

comparison = {
    "canonical_rule_count": len(canonical_ids),
    "classified_rule_count": len(classified_ids),
    "duplicate_classified_ids": sorted(
        source_rule_id
        for source_rule_id in set(classified_ids)
        if classified_ids.count(source_rule_id) > 1
    ),
    "extra_classified_ids": sorted(set(classified_ids) - set(canonical_ids)),
    "missing_classified_ids": sorted(set(canonical_ids) - set(classified_ids)),
    "ordered_identities_match": classified_ids == canonical_ids,
    "manifest_inventory_hash_matches": (
        manifest["inventory_sha256"] == inventory["inventory_sha256"]
    ),
    "validated_definition_ids": [
        rule["source_rule_id"] for rule in validated["definitions"]
    ],
    "validated_operational_rule_ids": [
        rule["source_rule_id"] for rule in validated["operational_rules"]
    ],
    "validated_proved_derived_lemma_ids": [
        rule["source_rule_id"] for rule in validated["proved_derived_lemmas"]
    ],
    "validated_domain_lemma_ids": [
        rule["source_rule_id"] for rule in validated["domain_lemmas"]
    ],
}

classified_inventory = [
    {**rule, **classification_by_id[rule["source_rule_id"]]}
    for rule in inventory["rules"]
]

print(
    json.dumps(
        {
            "comparison": comparison,
            "inventory": inventory,
            "classified_inventory_in_canonical_order": classified_inventory,
        },
        indent=2,
        sort_keys=True,
    )
)
