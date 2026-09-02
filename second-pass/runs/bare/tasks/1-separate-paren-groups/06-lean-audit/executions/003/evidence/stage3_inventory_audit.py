#!/usr/bin/env python3
"""Independent Stage 3 inventory/order/hash comparison using trusted tooling."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from tools.k_rule_inventory import canonical_json_sha256, inventory_verification
from tools.lemma_discovery_contract import validate_trust_boundary


WORKSPACE = Path("/reference/k-proof")
VERIFICATION = WORKSPACE / "verification.k"
DISCOVERY = Path("/reference/lemma-discovery.json")


inventory = inventory_verification(WORKSPACE)
validated = validate_trust_boundary(WORKSPACE, DISCOVERY)
manifest = json.loads(DISCOVERY.read_text())
source_lines = VERIFICATION.read_text().splitlines(keepends=True)

canonical = inventory["rules"]
classified = manifest["rules"]
canonical_ids = [entry["source_rule_id"] for entry in canonical]
classified_ids = [entry["source_rule_id"] for entry in classified]

assert len(canonical_ids) == len(set(canonical_ids)), "canonical duplicate"
assert len(classified_ids) == len(set(classified_ids)), "manifest duplicate"
assert classified_ids == canonical_ids, "manifest identities reordered or changed"
assert manifest["inventory_sha256"] == inventory["inventory_sha256"]
assert inventory["inventory_sha256"] == canonical_json_sha256(canonical)

print("verification_file:", inventory["verification_file"])
print("verification_sha256:", inventory["verification_sha256"])
print("verification_module:", inventory["verification_module"])
print("verification_modules:", json.dumps(inventory["verification_modules"]))
print("inventory_rule_count:", len(canonical))
print("inventory_sha256:", inventory["inventory_sha256"])
print("manifest_rule_count:", len(classified))
print("manifest_order_exact:", classified_ids == canonical_ids)
print("manifest_bijection_exact:", set(classified_ids) == set(canonical_ids))
print("trusted_contract_validation: PASS")
print()

for index, (rule, classification) in enumerate(zip(canonical, classified)):
    source_text = "".join(
        source_lines[rule["start_line"] - 1 : rule["end_line"]]
    ).rstrip(" \t\r\n")
    assert source_text == rule["text"], (
        f"source span mismatch for {rule['source_rule_id']}"
    )
    normalized = " ".join(source_text.split())
    digest = hashlib.sha256(normalized.encode()).hexdigest()
    assert digest == rule["normalized_sha256"]
    assert rule["source_rule_id"] == f"rule-{digest}"
    assert classification["source_rule_id"] == rule["source_rule_id"]
    print(f"RULE {index}")
    print("  module:", rule["module"])
    print("  span:", f"{rule['start_line']}:{rule['end_line']}")
    print("  attributes:", json.dumps(rule["attributes"]))
    print("  normalized_sha256:", digest)
    print("  source_rule_id:", rule["source_rule_id"])
    print("  classification:", classification["classification"])
    print("  text:", json.dumps(rule["text"]))

print()
print(
    "validated_category_counts:",
    json.dumps(
        {
            "definitions": len(validated["definitions"]),
            "operational_rules": len(validated["operational_rules"]),
            "proved_derived_lemmas": len(validated["proved_derived_lemmas"]),
            "domain_lemmas": len(validated["domain_lemmas"]),
        },
        sort_keys=True,
    ),
)
print("RESULT: PASS")
