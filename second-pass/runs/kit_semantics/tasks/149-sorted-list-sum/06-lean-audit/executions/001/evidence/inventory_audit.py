#!/usr/bin/env python3
"""Reconstruct and compare the Stage 3 rule inventory and ordering."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from tools import k_rule_inventory, lemma_discovery_contract


WORKSPACE = Path("/reference/k-proof")
DISCOVERY = Path("/reference/lemma-discovery.json")

inventory = k_rule_inventory.inventory_verification(WORKSPACE)
validated = lemma_discovery_contract.validate_trust_boundary(
    WORKSPACE, DISCOVERY
)
manifest = json.loads(DISCOVERY.read_text())
verification_lines = (WORKSPACE / "verification.k").read_text().splitlines()

canonical_ids = [rule["source_rule_id"] for rule in inventory["rules"]]
manifest_ids = [rule["source_rule_id"] for rule in manifest["rules"]]
per_rule = []
for rule in inventory["rules"]:
    normalized = " ".join(rule["text"].split())
    recomputed = hashlib.sha256(normalized.encode()).hexdigest()
    spanned = "\n".join(
        verification_lines[rule["start_line"] - 1 : rule["end_line"]]
    )
    per_rule.append(
        {
            "source_rule_id": rule["source_rule_id"],
            "module": rule["module"],
            "span": [rule["start_line"], rule["end_line"]],
            "attributes": rule["attributes"],
            "normalized_sha256": rule["normalized_sha256"],
            "recomputed_normalized_sha256": recomputed,
            "normalized_hash_matches": recomputed == rule["normalized_sha256"],
            "source_rule_id_matches": (
                rule["source_rule_id"] == f"rule-{recomputed}"
            ),
            "source_span_matches_text": spanned == rule["text"],
            "text": rule["text"],
        }
    )

report = {
    "inventory": inventory,
    "comparison": {
        "contract_validation_succeeded": (
            validated["inventory_sha256"] == inventory["inventory_sha256"]
        ),
        "manifest_inventory_sha256": manifest["inventory_sha256"],
        "recomputed_inventory_sha256": inventory["inventory_sha256"],
        "inventory_hash_matches": (
            manifest["inventory_sha256"] == inventory["inventory_sha256"]
        ),
        "canonical_rule_count": len(canonical_ids),
        "manifest_rule_count": len(manifest_ids),
        "manifest_duplicate_ids": sorted(
            {identifier for identifier in manifest_ids if manifest_ids.count(identifier) > 1}
        ),
        "omitted_ids": [
            identifier for identifier in canonical_ids if identifier not in manifest_ids
        ],
        "extra_ids": [
            identifier for identifier in manifest_ids if identifier not in canonical_ids
        ],
        "exact_ordered_identity_match": manifest_ids == canonical_ids,
        "all_rule_hashes_ids_and_spans_match": all(
            item["normalized_hash_matches"]
            and item["source_rule_id_matches"]
            and item["source_span_matches_text"]
            for item in per_rule
        ),
    },
    "per_rule_recomputation": per_rule,
}

print(json.dumps(report, indent=2, sort_keys=True))
