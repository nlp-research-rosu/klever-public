#!/usr/bin/env python3
"""Independent Stage 3 inventory reconstruction and bijection report."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from tools.k_rule_inventory import inventory_verification
from tools.lemma_discovery_contract import validate_trust_boundary


WORKSPACE = Path("/reference/k-proof")
DISCOVERY = Path("/reference/lemma-discovery.json")


def canonical_json_sha256(value: object) -> str:
    return hashlib.sha256(
        json.dumps(
            value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
        ).encode()
    ).hexdigest()


inventory = inventory_verification(WORKSPACE)
discovery_bytes = DISCOVERY.read_bytes()
discovery = json.loads(discovery_bytes)
validated = validate_trust_boundary(WORKSPACE, DISCOVERY)

canonical_rules = inventory["rules"]
manifest_rules = discovery["rules"]
canonical_ids = [rule["source_rule_id"] for rule in canonical_rules]
manifest_ids = [rule["source_rule_id"] for rule in manifest_rules]

classification_by_id = {
    entry["source_rule_id"]: entry["classification"] for entry in manifest_rules
}
classified_inventory = [
    {
        **rule,
        "classification": classification_by_id.get(rule["source_rule_id"]),
    }
    for rule in canonical_rules
]

report = {
    "workspace": str(WORKSPACE),
    "discovery_manifest": str(DISCOVERY),
    "discovery_manifest_sha256": hashlib.sha256(discovery_bytes).hexdigest(),
    "verification_sha256": inventory["verification_sha256"],
    "verification_module": inventory["verification_module"],
    "verification_modules_in_source_order": inventory["verification_modules"],
    "rule_count": len(canonical_rules),
    "canonical_inventory_sha256": inventory["inventory_sha256"],
    "recomputed_canonical_json_sha256": canonical_json_sha256(canonical_rules),
    "manifest_inventory_sha256": discovery["inventory_sha256"],
    "manifest_rule_count": len(manifest_rules),
    "manifest_unique_rule_count": len(set(manifest_ids)),
    "canonical_ids_in_source_order": canonical_ids,
    "manifest_ids_in_recorded_order": manifest_ids,
    "exact_ordered_identity_match": canonical_ids == manifest_ids,
    "omitted_ids": [item for item in canonical_ids if item not in set(manifest_ids)],
    "extra_ids": [item for item in manifest_ids if item not in set(canonical_ids)],
    "duplicated_manifest_ids": sorted(
        {item for item in manifest_ids if manifest_ids.count(item) > 1}
    ),
    "trusted_validator_succeeded": True,
    "validated_category_counts": {
        "DEFINITION": len(validated["definitions"]),
        "OPERATIONAL_RULE": len(validated["operational_rules"]),
        "PROVED_DERIVED_LEMMA": len(validated["proved_derived_lemmas"]),
        "DOMAIN_LEMMA": len(validated["domain_lemmas"]),
    },
    "rules_with_recomputed_spans_hashes_and_classifications": classified_inventory,
}

print(json.dumps(report, indent=2, sort_keys=True, ensure_ascii=False))
