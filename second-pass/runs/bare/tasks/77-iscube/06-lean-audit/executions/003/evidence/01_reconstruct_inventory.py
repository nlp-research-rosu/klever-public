import json
from pathlib import Path

from tools.k_rule_inventory import canonical_json_sha256, inventory_verification


workspace = Path("/reference/k-proof")
discovery_path = Path("/reference/lemma-discovery.json")
inventory = inventory_verification(workspace)
discovery = json.loads(discovery_path.read_text())

actual_ids = [rule["source_rule_id"] for rule in inventory["rules"]]
protected_ids = [rule["source_rule_id"] for rule in discovery["rules"]]
actual_docs = [
    {
        "source_rule_id": rule["source_rule_id"],
        "module": rule["module"],
        "start_line": rule["start_line"],
        "end_line": rule["end_line"],
        "normalized_sha256": rule["normalized_sha256"],
        "attributes": rule["attributes"],
        "text": rule["text"],
    }
    for rule in inventory["rules"]
]

report = {
    "reconstructed_inventory": inventory,
    "comparison": {
        "rule_count_reconstructed": len(actual_ids),
        "rule_count_protected": len(protected_ids),
        "ordered_ids_equal": actual_ids == protected_ids,
        "unique_reconstructed_ids": len(actual_ids) == len(set(actual_ids)),
        "unique_protected_ids": len(protected_ids) == len(set(protected_ids)),
        "missing_from_protected": [
            rule_id for rule_id in actual_ids if rule_id not in protected_ids
        ],
        "extra_in_protected": [
            rule_id for rule_id in protected_ids if rule_id not in actual_ids
        ],
        "recomputed_rule_documents_sha256": canonical_json_sha256(actual_docs),
        "trusted_inventory_sha256": inventory["inventory_sha256"],
        "protected_inventory_sha256": discovery["inventory_sha256"],
        "hashes_equal": (
            canonical_json_sha256(actual_docs)
            == inventory["inventory_sha256"]
            == discovery["inventory_sha256"]
        ),
        "all_protected_entries_classified": all(
            rule.get("classification")
            in {
                "DEFINITION",
                "OPERATIONAL_RULE",
                "PROVED_DERIVED_LEMMA",
                "DOMAIN_LEMMA",
            }
            for rule in discovery["rules"]
        ),
    },
}

print(json.dumps(report, indent=2, sort_keys=True))
