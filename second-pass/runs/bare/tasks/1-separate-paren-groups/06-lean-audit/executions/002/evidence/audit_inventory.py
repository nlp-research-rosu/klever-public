#!/usr/bin/env python3
"""Independent strict comparison around the trusted K rule inventory."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from tools.k_rule_inventory import canonical_json_sha256, inventory_verification
from tools.lemma_discovery_contract import validate_trust_boundary


WORKSPACE = Path("/reference/k-proof")
MANIFEST = Path("/reference/lemma-discovery.json")


def main() -> None:
    inventory = inventory_verification(WORKSPACE)
    discovery = json.loads(MANIFEST.read_text())
    validated = validate_trust_boundary(WORKSPACE, MANIFEST)

    canonical_rules = inventory["rules"]
    manifest_rules = discovery["rules"]
    canonical_ids = [rule["source_rule_id"] for rule in canonical_rules]
    manifest_ids = [rule["source_rule_id"] for rule in manifest_rules]

    positional = []
    for index in range(max(len(canonical_ids), len(manifest_ids))):
        expected = canonical_ids[index] if index < len(canonical_ids) else None
        observed = manifest_ids[index] if index < len(manifest_ids) else None
        positional.append(
            {
                "index": index,
                "expected_source_rule_id": expected,
                "manifest_source_rule_id": observed,
                "matches": expected == observed,
            }
        )

    manifest_counts = {
        source_rule_id: manifest_ids.count(source_rule_id)
        for source_rule_id in sorted(set(manifest_ids))
    }
    report = {
        "inventory": inventory,
        "recomputed_inventory_sha256_from_rules": canonical_json_sha256(
            canonical_rules
        ),
        "manifest_file_sha256": hashlib.sha256(MANIFEST.read_bytes()).hexdigest(),
        "manifest_inventory_sha256": discovery.get("inventory_sha256"),
        "manifest_rule_count": len(manifest_rules),
        "canonical_rule_count": len(canonical_rules),
        "manifest_ids_in_canonical_order": manifest_ids == canonical_ids,
        "missing_ids": sorted(set(canonical_ids) - set(manifest_ids)),
        "extra_ids": sorted(set(manifest_ids) - set(canonical_ids)),
        "duplicate_manifest_ids": sorted(
            source_rule_id
            for source_rule_id, count in manifest_counts.items()
            if count != 1
        ),
        "positional_comparison": positional,
        "trusted_contract_validated": True,
        "validated_classification_counts": {
            "DEFINITION": len(validated["definitions"]),
            "OPERATIONAL_RULE": len(validated["operational_rules"]),
            "PROVED_DERIVED_LEMMA": len(validated["proved_derived_lemmas"]),
            "DOMAIN_LEMMA": len(validated["domain_lemmas"]),
        },
        "manifest_entries": manifest_rules,
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
