#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from tools.k_rule_inventory import canonical_json_sha256, inventory_verification
from tools.lemma_discovery_contract import validate_trust_boundary


WORKSPACE = Path("/reference/k-proof")
DISCOVERY = Path("/reference/lemma-discovery.json")

inventory = inventory_verification(WORKSPACE)
discovery = json.loads(DISCOVERY.read_text())
validated = validate_trust_boundary(WORKSPACE, DISCOVERY)
source_lines = (WORKSPACE / "verification.k").read_text().splitlines()

inventory_ids = [rule["source_rule_id"] for rule in inventory["rules"]]
discovery_ids = [rule["source_rule_id"] for rule in discovery["rules"]]

assert inventory["inventory_sha256"] == canonical_json_sha256(inventory["rules"])
assert discovery["inventory_sha256"] == inventory["inventory_sha256"]
assert len(discovery_ids) == len(set(discovery_ids))
assert discovery_ids == inventory_ids
assert len(validated["rules"]) == len(inventory["rules"])

for rule in inventory["rules"]:
    source_text = "\n".join(
        source_lines[rule["start_line"] - 1 : rule["end_line"]]
    )
    normalized = " ".join(source_text.split())
    normalized_sha256 = hashlib.sha256(normalized.encode()).hexdigest()
    assert source_text == rule["text"]
    assert normalized_sha256 == rule["normalized_sha256"]
    assert rule["source_rule_id"] == f"rule-{normalized_sha256}"

print(
    json.dumps(
        {
            "verification_sha256": inventory["verification_sha256"],
            "verification_module": inventory["verification_module"],
            "verification_modules": inventory["verification_modules"],
            "inventory_sha256": inventory["inventory_sha256"],
            "inventory_rule_count": len(inventory["rules"]),
            "discovery_rule_count": len(discovery["rules"]),
            "ordered_identity_match": discovery_ids == inventory_ids,
            "unique_discovery_id_count": len(set(discovery_ids)),
            "contract_validation": "PASS",
            "classification_counts": {
                "DEFINITION": len(validated["definitions"]),
                "OPERATIONAL_RULE": len(validated["operational_rules"]),
                "PROVED_DERIVED_LEMMA": len(validated["proved_derived_lemmas"]),
                "DOMAIN_LEMMA": len(validated["domain_lemmas"]),
            },
            "rules": [
                {
                    **rule,
                    "claimed_classification": discovery["rules"][index][
                        "classification"
                    ],
                    "claimed_rationale": discovery["rules"][index]["rationale"],
                }
                for index, rule in enumerate(inventory["rules"])
            ],
        },
        indent=2,
        sort_keys=True,
    )
)
