#!/usr/bin/env python3
"""Canonical Stage 1 inventory reconstruction and Stage 3 bijection checks."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from tools.k_rule_inventory import canonical_json_sha256, inventory_verification
from tools.lemma_discovery_contract import validate_trust_boundary


workspace = Path("/reference/k-proof")
manifest_path = Path("/reference/lemma-discovery.json")
verification_path = workspace / "verification.k"

inventory = inventory_verification(workspace)
validated = validate_trust_boundary(workspace, manifest_path)
manifest = json.loads(manifest_path.read_text())

canonical_ids = [entry["source_rule_id"] for entry in inventory["rules"]]
manifest_ids = [entry["source_rule_id"] for entry in manifest["rules"]]
canonical_by_id = {
    entry["source_rule_id"]: entry for entry in inventory["rules"]
}
manifest_by_id = {
    entry["source_rule_id"]: entry for entry in manifest["rules"]
}

per_rule_checks = []
source_lines = verification_path.read_text().splitlines()
for entry in inventory["rules"]:
    source_rule_id = entry["source_rule_id"]
    exact_span = "\n".join(
        source_lines[entry["start_line"] - 1 : entry["end_line"]]
    )
    normalized = " ".join(exact_span.split())
    normalized_sha256 = hashlib.sha256(normalized.encode()).hexdigest()
    per_rule_checks.append(
        {
            "source_rule_id": source_rule_id,
            "exact_span_matches_inventory_text": exact_span == entry["text"],
            "normalized_sha256_recomputed": normalized_sha256,
            "normalized_sha256_matches": (
                normalized_sha256 == entry["normalized_sha256"]
            ),
            "source_rule_id_matches_normalized_hash": (
                source_rule_id == f"rule-{normalized_sha256}"
            ),
            "classification": manifest_by_id[source_rule_id][
                "classification"
            ],
        }
    )

checks = {
    "verification_source_sha256_matches_inventory": (
        hashlib.sha256(verification_path.read_bytes()).hexdigest()
        == inventory["verification_sha256"]
    ),
    "inventory_hash_recomputed_from_ordered_rules": (
        canonical_json_sha256(inventory["rules"])
        == inventory["inventory_sha256"]
    ),
    "inventory_hash_matches_stage3": (
        inventory["inventory_sha256"] == manifest["inventory_sha256"]
    ),
    "ordered_source_rule_ids_match_exactly": canonical_ids == manifest_ids,
    "no_canonical_duplicate_ids": len(canonical_ids) == len(set(canonical_ids)),
    "no_stage3_duplicate_ids": len(manifest_ids) == len(set(manifest_ids)),
    "same_id_set": set(canonical_ids) == set(manifest_ids),
    "same_rule_count": len(canonical_ids) == len(manifest_ids),
    "trusted_contract_validation_succeeded": (
        validated["inventory_sha256"] == inventory["inventory_sha256"]
    ),
    "all_spans_and_hashes_recompute": all(
        entry["exact_span_matches_inventory_text"]
        and entry["normalized_sha256_matches"]
        and entry["source_rule_id_matches_normalized_hash"]
        for entry in per_rule_checks
    ),
    "all_inventory_rules_accounted_once": (
        len(validated["definitions"])
        + len(validated["operational_rules"])
        + len(validated["proved_derived_lemmas"])
        + len(validated["domain_lemmas"])
        == len(inventory["rules"])
    ),
}

result = {
    "checks": checks,
    "all_checks_pass": all(checks.values()),
    "inventory": inventory,
    "ordered_stage3_source_rule_ids": manifest_ids,
    "per_rule_checks": per_rule_checks,
    "validated_classification_counts": {
        "DEFINITION": len(validated["definitions"]),
        "OPERATIONAL_RULE": len(validated["operational_rules"]),
        "PROVED_DERIVED_LEMMA": len(
            validated["proved_derived_lemmas"]
        ),
        "DOMAIN_LEMMA": len(validated["domain_lemmas"]),
    },
}
print(json.dumps(result, indent=2, sort_keys=True))
