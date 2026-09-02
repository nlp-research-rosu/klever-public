#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

from tools.k_rule_inventory import canonical_json_sha256, inventory_verification


workspace = Path("/reference/k-proof")
manifest_path = Path("/reference/lemma-discovery.json")
inventory = inventory_verification(workspace)
manifest = json.loads(manifest_path.read_text())
verification_lines = (workspace / "verification.k").read_text().splitlines()

canonical_ids = [rule["source_rule_id"] for rule in inventory["rules"]]
manifest_ids = [rule["source_rule_id"] for rule in manifest["rules"]]
checks = {
    "inventory_hash_matches_manifest": (
        inventory["inventory_sha256"] == manifest["inventory_sha256"]
    ),
    "manifest_identity_order_exact": manifest_ids == canonical_ids,
    "manifest_has_no_duplicates": len(manifest_ids) == len(set(manifest_ids)),
    "manifest_has_no_omissions_or_extras": set(manifest_ids) == set(canonical_ids),
    "inventory_hash_recomputed": (
        canonical_json_sha256(inventory["rules"]) == inventory["inventory_sha256"]
    ),
}

rule_checks = []
for rule in inventory["rules"]:
    source_text = "\n".join(
        verification_lines[rule["start_line"] - 1 : rule["end_line"]]
    )
    normalized = " ".join(source_text.split())
    normalized_sha256 = hashlib.sha256(normalized.encode()).hexdigest()
    rule_checks.append(
        {
            "source_rule_id": rule["source_rule_id"],
            "start_line": rule["start_line"],
            "end_line": rule["end_line"],
            "source_span_exact": source_text == rule["text"],
            "normalized_sha256_recomputed": normalized_sha256,
            "normalized_sha256_matches": (
                normalized_sha256 == rule["normalized_sha256"]
            ),
            "source_rule_id_matches": (
                rule["source_rule_id"] == f"rule-{normalized_sha256}"
            ),
        }
    )

result = {
    "checks": checks,
    "canonical_ids": canonical_ids,
    "manifest_ids": manifest_ids,
    "rule_checks": rule_checks,
    "all_pass": all(checks.values())
    and all(
        item["source_span_exact"]
        and item["normalized_sha256_matches"]
        and item["source_rule_id_matches"]
        for item in rule_checks
    ),
}
print(json.dumps(result, indent=2, sort_keys=True))
