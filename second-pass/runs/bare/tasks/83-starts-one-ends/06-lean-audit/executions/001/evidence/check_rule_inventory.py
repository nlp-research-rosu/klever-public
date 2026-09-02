#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

from tools.k_rule_inventory import (
    canonical_json_sha256,
    inventory_verification,
)
from tools.lemma_discovery_contract import validate_trust_boundary


WORKSPACE = Path("/reference/k-proof")
DISCOVERY = Path("/reference/lemma-discovery.json")

inventory = inventory_verification(WORKSPACE)
discovery = json.loads(DISCOVERY.read_text())
validated = validate_trust_boundary(WORKSPACE, DISCOVERY)
rules = inventory["rules"]
entries = discovery["rules"]
source_lines = (WORKSPACE / "verification.k").read_text().splitlines()

assert inventory["verification_modules"] == ["VERIFICATION"]
assert inventory["inventory_sha256"] == canonical_json_sha256(rules)
assert discovery["inventory_sha256"] == inventory["inventory_sha256"]
assert len(rules) == len(entries)

canonical_ids = [rule["source_rule_id"] for rule in rules]
discovery_ids = [entry["source_rule_id"] for entry in entries]
assert canonical_ids == discovery_ids
assert len(canonical_ids) == len(set(canonical_ids))

normalized_hashes = []
for position, (rule, entry) in enumerate(zip(rules, entries), start=1):
    exact_span = "\n".join(
        source_lines[rule["start_line"] - 1 : rule["end_line"]]
    )
    assert exact_span == rule["text"]
    normalized = " ".join(exact_span.split())
    normalized_sha256 = hashlib.sha256(normalized.encode()).hexdigest()
    assert normalized_sha256 == rule["normalized_sha256"]
    assert rule["source_rule_id"] == f"rule-{normalized_sha256}"
    normalized_hashes.append(normalized_sha256)
    print(
        json.dumps(
            {
                "position": position,
                "module": rule["module"],
                "span": f"{rule['start_line']}-{rule['end_line']}",
                "attributes": rule["attributes"],
                "normalized_sha256": normalized_sha256,
                "source_rule_id": rule["source_rule_id"],
                "discovery_id": entry["source_rule_id"],
                "classification": entry["classification"],
                "exact_span_matches": True,
            },
            sort_keys=True,
        )
    )

assert len(normalized_hashes) == len(set(normalized_hashes))
assert not validated["operational_rules"]
assert not validated["proved_derived_lemmas"]
assert not validated["domain_lemmas"]
assert len(validated["definitions"]) == len(rules) == 6

print("verification_sha256 =", inventory["verification_sha256"])
print("verification_modules =", inventory["verification_modules"])
print("canonical_rule_count =", len(rules))
print("discovery_rule_count =", len(entries))
print("ordered_identity_match =", canonical_ids == discovery_ids)
print("inventory_sha256 =", inventory["inventory_sha256"])
print("discovery_inventory_sha256 =", discovery["inventory_sha256"])
print(
    "validated_category_counts =",
    {
        "DEFINITION": len(validated["definitions"]),
        "OPERATIONAL_RULE": len(validated["operational_rules"]),
        "PROVED_DERIVED_LEMMA": len(validated["proved_derived_lemmas"]),
        "DOMAIN_LEMMA": len(validated["domain_lemmas"]),
    },
)
print("RESULT: PASS")
