#!/usr/bin/env python3
"""Independent Stage 3 inventory reconstruction using the trusted inventory."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from tools.k_rule_inventory import canonical_json_sha256, inventory_verification
from tools.lemma_discovery_contract import validate_trust_boundary


WORKSPACE = Path("/reference/k-proof")
VERIFICATION = WORKSPACE / "verification.k"
MANIFEST = Path("/reference/lemma-discovery.json")


def main() -> None:
    inventory = inventory_verification(WORKSPACE)
    manifest = json.loads(MANIFEST.read_text())
    validated = validate_trust_boundary(WORKSPACE, MANIFEST)
    source_lines = VERIFICATION.read_text().splitlines()

    manual_rule_checks = []
    for rule in inventory["rules"]:
        source_text = "\n".join(
            source_lines[rule["start_line"] - 1 : rule["end_line"]]
        )
        normalized = " ".join(source_text.split())
        normalized_sha256 = hashlib.sha256(normalized.encode()).hexdigest()
        manual_rule_checks.append(
            {
                "source_rule_id": rule["source_rule_id"],
                "source_span": {
                    "start_line": rule["start_line"],
                    "end_line": rule["end_line"],
                },
                "span_text_exact": source_text == rule["text"],
                "normalized_text": normalized,
                "normalized_sha256": normalized_sha256,
                "normalized_hash_exact": (
                    normalized_sha256 == rule["normalized_sha256"]
                ),
                "source_rule_id_exact": (
                    rule["source_rule_id"] == f"rule-{normalized_sha256}"
                ),
            }
        )

    inventory_ids = [rule["source_rule_id"] for rule in inventory["rules"]]
    manifest_ids = [rule["source_rule_id"] for rule in manifest["rules"]]
    document = {
        "trusted_inventory": inventory,
        "manual_rule_checks": manual_rule_checks,
        "manual_inventory_sha256": canonical_json_sha256(inventory["rules"]),
        "manual_inventory_hash_exact": (
            canonical_json_sha256(inventory["rules"])
            == inventory["inventory_sha256"]
        ),
        "manifest_inventory_hash_exact": (
            manifest["inventory_sha256"] == inventory["inventory_sha256"]
        ),
        "manifest_identity_order_exact": manifest_ids == inventory_ids,
        "manifest_unique_identity_count": len(set(manifest_ids)),
        "inventory_identity_count": len(inventory_ids),
        "manifest_identity_count": len(manifest_ids),
        "validated_partition_counts": {
            "definitions": len(validated["definitions"]),
            "operational_rules": len(validated["operational_rules"]),
            "proved_derived_lemmas": len(
                validated["proved_derived_lemmas"]
            ),
            "domain_lemmas": len(validated["domain_lemmas"]),
        },
        "validated_rules_in_canonical_order": [
            {
                "source_rule_id": rule["source_rule_id"],
                "classification": next(
                    entry["classification"]
                    for entry in manifest["rules"]
                    if entry["source_rule_id"] == rule["source_rule_id"]
                ),
            }
            for rule in inventory["rules"]
        ],
    }
    print(json.dumps(document, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
