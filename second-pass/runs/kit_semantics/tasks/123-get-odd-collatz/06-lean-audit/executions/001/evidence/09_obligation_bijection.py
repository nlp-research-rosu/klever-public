#!/usr/bin/env python3
import json
from pathlib import Path

from tools.k_rule_inventory import inventory_verification


inventory = inventory_verification(Path("/reference/k-proof"))
discovery = json.loads(Path("/reference/lemma-discovery.json").read_text())
obligation_map = json.loads(
    Path(
        "/reference/klean-generation/generated/obligation-map.json"
    ).read_text()
)

classification_by_id = {
    entry["source_rule_id"]: entry["classification"]
    for entry in discovery["rules"]
}
domain_rules = [
    rule
    for rule in inventory["rules"]
    if classification_by_id[rule["source_rule_id"]] == "DOMAIN_LEMMA"
]
obligations = obligation_map["obligations"]

paired = []
for source_rule, obligation in zip(domain_rules, obligations):
    conjunct = obligation["lean_conjunct"]
    paired.append(
        {
            "source_rule_id": source_rule["source_rule_id"],
            "source_span": {
                "start_line": source_rule["start_line"],
                "end_line": source_rule["end_line"],
            },
            "source_text": source_rule["text"],
            "lean_conjunct": conjunct,
            "same_source_rule_id": (
                source_rule["source_rule_id"]
                == obligation["source_rule_id"]
            ),
            "same_normalized_hash": (
                source_rule["normalized_sha256"]
                == obligation["normalized_sha256"]
            ),
            "vacuity_token_scan": {
                "is_True": conjunct.strip() == "True",
                "is_False": conjunct.strip() == "False",
                "contains_sorry": "sorry" in conjunct,
                "contains_admit": "admit" in conjunct,
            },
        }
    )

domain_ids = [rule["source_rule_id"] for rule in domain_rules]
source_rule_ids = [
    rule["source_rule_id"] for rule in obligation_map["source_rules"]
]
obligation_ids = [
    obligation["source_rule_id"] for obligation in obligations
]

print(
    json.dumps(
        {
            "domain_rule_count": len(domain_rules),
            "source_rule_count": len(source_rule_ids),
            "obligation_count": len(obligation_ids),
            "domain_to_source_rule_exact_order": domain_ids
            == source_rule_ids,
            "domain_to_obligation_exact_order": domain_ids
            == obligation_ids,
            "unique_domain_ids": len(set(domain_ids)) == len(domain_ids),
            "unique_source_rule_ids": len(set(source_rule_ids))
            == len(source_rule_ids),
            "unique_obligation_ids": len(set(obligation_ids))
            == len(obligation_ids),
            "paired_rules_and_conjuncts": paired,
        },
        indent=2,
        sort_keys=True,
    )
)
