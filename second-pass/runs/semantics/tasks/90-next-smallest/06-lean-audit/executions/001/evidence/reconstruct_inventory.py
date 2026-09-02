#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

from tools.k_rule_inventory import (
    canonical_json_sha256,
    inventory_verification,
)


workspace = Path("/reference/k-proof")
verification = workspace / "verification.k"
source_lines = verification.read_text().splitlines()

# Reconstruct first, before loading the protected classification.
inventory = inventory_verification(workspace)
recomputed_rules = []
span_checks = []
for rule in inventory["rules"]:
    span_text = "\n".join(
        source_lines[rule["start_line"] - 1 : rule["end_line"]]
    )
    normalized = " ".join(span_text.split())
    normalized_sha256 = hashlib.sha256(normalized.encode()).hexdigest()
    check = {
        "source_rule_id": rule["source_rule_id"],
        "span_text_exact": span_text == rule["text"],
        "normalized_sha256_exact": (
            normalized_sha256 == rule["normalized_sha256"]
        ),
        "source_rule_id_exact": (
            rule["source_rule_id"] == "rule-" + normalized_sha256
        ),
    }
    span_checks.append(check)
    recomputed_rules.append(rule)

recomputed_inventory_sha256 = canonical_json_sha256(recomputed_rules)

# Only after reconstruction, compare the protected Stage 3 document.
discovery = json.loads(Path("/reference/lemma-discovery.json").read_text())
inventory_ids = [rule["source_rule_id"] for rule in inventory["rules"]]
discovery_ids = [rule["source_rule_id"] for rule in discovery["rules"]]
checks = {
    "schema_version_2": discovery.get("schema_version") == 2,
    "verification_sha256_exact": (
        inventory["verification_sha256"]
        == hashlib.sha256(verification.read_bytes()).hexdigest()
    ),
    "inventory_hash_recomputed": (
        inventory["inventory_sha256"] == recomputed_inventory_sha256
    ),
    "manifest_inventory_hash_exact": (
        discovery.get("inventory_sha256") == inventory["inventory_sha256"]
    ),
    "same_count": len(inventory_ids) == len(discovery_ids),
    "no_inventory_duplicates": len(inventory_ids) == len(set(inventory_ids)),
    "no_manifest_duplicates": len(discovery_ids) == len(set(discovery_ids)),
    "ordered_identity_bijection": discovery_ids == inventory_ids,
    "all_spans_and_rule_hashes_exact": all(
        all(value for key, value in item.items() if key != "source_rule_id")
        for item in span_checks
    ),
}
manifest_by_id = {
    item["source_rule_id"]: item for item in discovery["rules"]
}
rules = [
    {
        **rule,
        "manifest_classification": manifest_by_id[
            rule["source_rule_id"]
        ]["classification"],
        "manifest_rationale": manifest_by_id[
            rule["source_rule_id"]
        ]["rationale"],
    }
    for rule in inventory["rules"]
]
result = {
    "verification_module": inventory["verification_module"],
    "verification_modules": inventory["verification_modules"],
    "verification_sha256": inventory["verification_sha256"],
    "rule_count": len(rules),
    "inventory_sha256": inventory["inventory_sha256"],
    "recomputed_inventory_sha256": recomputed_inventory_sha256,
    "checks": checks,
    "span_checks": span_checks,
    "rules": rules,
    "status": "PASS" if all(checks.values()) else "FAIL",
}
print(json.dumps(result, indent=2, sort_keys=True))
