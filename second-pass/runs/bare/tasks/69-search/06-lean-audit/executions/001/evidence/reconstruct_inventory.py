#!/usr/bin/env python3
"""Independent Stage 3 inventory reconstruction using the trusted inventory code."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from tools.k_rule_inventory import canonical_json_sha256, inventory_verification
from tools.lemma_discovery_contract import validate_trust_boundary


WORKSPACE = Path("/reference/k-proof")
MANIFEST = Path("/reference/lemma-discovery.json")


inventory = inventory_verification(WORKSPACE)
manifest = json.loads(MANIFEST.read_bytes())
verification_text = (WORKSPACE / "verification.k").read_text()

recomputed_rules = []
for position, rule in enumerate(inventory["rules"]):
    normalized = " ".join(rule["text"].split())
    normalized_sha256 = hashlib.sha256(normalized.encode()).hexdigest()
    source_rule_id = f"rule-{normalized_sha256}"
    source_span = "\n".join(
        verification_text.splitlines()[
            rule["start_line"] - 1 : rule["end_line"]
        ]
    )
    checks = {
        "text_equals_source_span": rule["text"] == source_span,
        "normalized_sha256_matches": (
            rule["normalized_sha256"] == normalized_sha256
        ),
        "source_rule_id_matches": rule["source_rule_id"] == source_rule_id,
    }
    if not all(checks.values()):
        raise SystemExit(f"rule {position} reconstruction failed: {checks}")
    recomputed_rules.append(rule)

recomputed_inventory_sha256 = canonical_json_sha256(recomputed_rules)
manifest_ids = [entry["source_rule_id"] for entry in manifest["rules"]]
inventory_ids = [entry["source_rule_id"] for entry in inventory["rules"]]
comparison = {
    "manifest_schema_version": manifest.get("schema_version"),
    "inventory_rule_count": len(inventory_ids),
    "manifest_rule_count": len(manifest_ids),
    "manifest_has_duplicate_ids": len(manifest_ids) != len(set(manifest_ids)),
    "inventory_has_duplicate_ids": len(inventory_ids) != len(set(inventory_ids)),
    "ordered_ids_equal": manifest_ids == inventory_ids,
    "identity_sets_equal": set(manifest_ids) == set(inventory_ids),
    "recomputed_inventory_sha256": recomputed_inventory_sha256,
    "trusted_inventory_sha256": inventory["inventory_sha256"],
    "manifest_inventory_sha256": manifest.get("inventory_sha256"),
    "inventory_hashes_equal": (
        recomputed_inventory_sha256
        == inventory["inventory_sha256"]
        == manifest.get("inventory_sha256")
    ),
}
if not (
    comparison["ordered_ids_equal"]
    and comparison["identity_sets_equal"]
    and comparison["inventory_hashes_equal"]
    and not comparison["manifest_has_duplicate_ids"]
    and not comparison["inventory_has_duplicate_ids"]
):
    raise SystemExit(f"inventory/manifest comparison failed: {comparison}")

validated = validate_trust_boundary(WORKSPACE, MANIFEST)
result = {
    "inventory": inventory,
    "comparison": comparison,
    "trusted_contract_counts": {
        "definitions": len(validated["definitions"]),
        "operational_rules": len(validated["operational_rules"]),
        "proved_derived_lemmas": len(validated["proved_derived_lemmas"]),
        "domain_lemmas": len(validated["domain_lemmas"]),
    },
}
print(json.dumps(result, indent=2, sort_keys=True))
