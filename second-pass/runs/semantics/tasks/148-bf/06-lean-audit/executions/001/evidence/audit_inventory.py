#!/usr/bin/env python3
"""Independent structural comparison of Stage 1 rules and Stage 3 labels."""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path

from tools.k_rule_inventory import canonical_json_sha256, inventory_verification
from tools.lemma_discovery_contract import validate_trust_boundary


WORKSPACE = Path("/reference/k-proof")
DISCOVERY = Path("/reference/lemma-discovery.json")


inventory = inventory_verification(WORKSPACE)
discovery = json.loads(DISCOVERY.read_text())
validated = validate_trust_boundary(WORKSPACE, DISCOVERY)
source_lines = (WORKSPACE / "verification.k").read_text().splitlines()

errors: list[str] = []
rule_checks: list[dict[str, object]] = []
for position, rule in enumerate(inventory["rules"], start=1):
    spanned_text = "\n".join(
        source_lines[rule["start_line"] - 1 : rule["end_line"]]
    )
    normalized = " ".join(rule["text"].split())
    normalized_sha256 = hashlib.sha256(normalized.encode()).hexdigest()
    expected_id = f"rule-{normalized_sha256}"
    checks = {
        "position": position,
        "span_matches_source": spanned_text == rule["text"],
        "normalized_sha256_matches": normalized_sha256
        == rule["normalized_sha256"],
        "source_rule_id_matches": expected_id == rule["source_rule_id"],
    }
    if not all(value for key, value in checks.items() if key != "position"):
        errors.append(f"rule {position} has a reconstruction mismatch")
    rule_checks.append(
        {
            "source_rule_id": rule["source_rule_id"],
            "module": rule["module"],
            "start_line": rule["start_line"],
            "end_line": rule["end_line"],
            "normalized_sha256": rule["normalized_sha256"],
            "attributes": rule["attributes"],
            **checks,
        }
    )

reconstructed_ids = [rule["source_rule_id"] for rule in inventory["rules"]]
classified_ids = [rule.get("source_rule_id") for rule in discovery.get("rules", [])]
validated_ids = [rule["source_rule_id"] for rule in validated["rules"]]
duplicate_discovery_ids = sorted(
    rule_id
    for rule_id, count in Counter(classified_ids).items()
    if count > 1
)
missing_ids = sorted(set(reconstructed_ids) - set(classified_ids))
extra_ids = sorted(set(classified_ids) - set(reconstructed_ids))
ordered_identity_match = classified_ids == reconstructed_ids
enriched_rules = [
    {
        **source_rule,
        "classification": classified_rule["classification"],
        "rationale": classified_rule["rationale"],
    }
    for source_rule, classified_rule in zip(
        inventory["rules"], discovery["rules"], strict=True
    )
]
validated_rule_match = validated["rules"] == inventory["rules"]
category_key = {
    "DEFINITION": "definitions",
    "OPERATIONAL_RULE": "operational_rules",
    "PROVED_DERIVED_LEMMA": "proved_derived_lemmas",
    "DOMAIN_LEMMA": "domain_lemmas",
}
validated_categories_match = all(
    validated[key]
    == [rule for rule in enriched_rules if rule["classification"] == classification]
    for classification, key in category_key.items()
)
inventory_hash_recomputed = canonical_json_sha256(inventory["rules"])

if duplicate_discovery_ids:
    errors.append("discovery contains duplicate rule IDs")
if missing_ids:
    errors.append("discovery omits reconstructed rules")
if extra_ids:
    errors.append("discovery contains extra rules")
if not ordered_identity_match:
    errors.append("discovery rule identities are reordered or changed")
if discovery.get("inventory_sha256") != inventory["inventory_sha256"]:
    errors.append("discovery inventory hash differs from reconstruction")
if inventory_hash_recomputed != inventory["inventory_sha256"]:
    errors.append("recomputed whole-inventory hash differs")
if (
    validated_ids != reconstructed_ids
    or not validated_rule_match
    or not validated_categories_match
):
    errors.append("trusted contract reconstruction/categories are not exact")

result = {
    "status": "PASS" if not errors else "FAIL",
    "errors": errors,
    "verification_sha256": inventory["verification_sha256"],
    "verification_module": inventory["verification_module"],
    "verification_modules": inventory["verification_modules"],
    "reconstructed_rule_count": len(reconstructed_ids),
    "discovery_rule_count": len(classified_ids),
    "unique_discovery_rule_count": len(set(classified_ids)),
    "duplicate_discovery_ids": duplicate_discovery_ids,
    "missing_ids": missing_ids,
    "extra_ids": extra_ids,
    "ordered_identity_match": ordered_identity_match,
    "inventory_sha256_reconstructed": inventory["inventory_sha256"],
    "inventory_sha256_recomputed": inventory_hash_recomputed,
    "inventory_sha256_discovery": discovery.get("inventory_sha256"),
    "validated_inventory_exact": validated_rule_match,
    "validated_categories_exact": validated_categories_match,
    "classification_counts": dict(
        sorted(Counter(rule["classification"] for rule in enriched_rules).items())
    ),
    "simplification_rule_ids": [
        rule["source_rule_id"]
        for rule in enriched_rules
        if "simplification" in rule["attributes"]
    ],
    "rule_checks": rule_checks,
}
print(json.dumps(result, indent=2, sort_keys=True))
