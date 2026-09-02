#!/usr/bin/env python3
"""Reconstruct and bijectively compare the frozen verification rule inventory."""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path

from tools import k_rule_inventory, lemma_discovery_contract


WORKSPACE = Path("/reference/k-proof")
VERIFICATION = WORKSPACE / "verification.k"
MANIFEST = Path("/reference/lemma-discovery.json")

inventory = k_rule_inventory.inventory_verification(WORKSPACE)
discovery = json.loads(MANIFEST.read_text())
validated = lemma_discovery_contract.validate_trust_boundary(WORKSPACE, MANIFEST)
source_lines = VERIFICATION.read_text().splitlines()

recomputed_rules = []
for rule in inventory["rules"]:
    normalized = " ".join(rule["text"].split())
    normalized_sha256 = hashlib.sha256(normalized.encode()).hexdigest()
    span_text = "\n".join(
        source_lines[rule["start_line"] - 1 : rule["end_line"]]
    )
    recomputed_rules.append(
        {
            **rule,
            "span_text_matches": span_text == rule["text"],
            "recomputed_normalized_sha256": normalized_sha256,
            "normalized_sha256_matches": (
                normalized_sha256 == rule["normalized_sha256"]
            ),
            "recomputed_source_rule_id": f"rule-{normalized_sha256}",
            "source_rule_id_matches": (
                rule["source_rule_id"] == f"rule-{normalized_sha256}"
            ),
        }
    )

canonical_ids = [rule["source_rule_id"] for rule in inventory["rules"]]
manifest_ids = [entry["source_rule_id"] for entry in discovery["rules"]]
canonical_counts = Counter(canonical_ids)
manifest_counts = Counter(manifest_ids)
classification_by_id = {
    entry["source_rule_id"]: entry["classification"]
    for entry in discovery["rules"]
}

checks = {
    "verification_sha256_matches_reconstruction": (
        inventory["verification_sha256"]
        == hashlib.sha256(VERIFICATION.read_bytes()).hexdigest()
    ),
    "inventory_hash_recomputed": (
        inventory["inventory_sha256"]
        == k_rule_inventory.canonical_json_sha256(inventory["rules"])
    ),
    "inventory_hash_matches_manifest": (
        inventory["inventory_sha256"] == discovery["inventory_sha256"]
    ),
    "exact_ordered_identity_match": canonical_ids == manifest_ids,
    "canonical_ids_unique": all(count == 1 for count in canonical_counts.values()),
    "manifest_ids_unique": all(count == 1 for count in manifest_counts.values()),
    "no_omitted_ids": not (set(canonical_ids) - set(manifest_ids)),
    "no_extra_ids": not (set(manifest_ids) - set(canonical_ids)),
    "all_rules_accounted": (
        set(classification_by_id) == set(canonical_ids)
        and len(classification_by_id) == len(canonical_ids)
    ),
    "all_spans_and_hashes_match": all(
        rule["span_text_matches"]
        and rule["normalized_sha256_matches"]
        and rule["source_rule_id_matches"]
        for rule in recomputed_rules
    ),
    "trusted_contract_rule_count_matches": (
        len(validated["rules"]) == len(inventory["rules"])
    ),
}

result = {
    "all_structural_checks_pass": all(checks.values()),
    "checks": checks,
    "verification_file": inventory["verification_file"],
    "verification_sha256": inventory["verification_sha256"],
    "verification_module": inventory["verification_module"],
    "verification_modules_local_closure": inventory["verification_modules"],
    "inventory_sha256": inventory["inventory_sha256"],
    "ordered_manifest_ids": manifest_ids,
    "rules": recomputed_rules,
    "manifest_classifications_in_source_order": [
        {
            "source_rule_id": rule_id,
            "classification": classification_by_id[rule_id],
        }
        for rule_id in canonical_ids
    ],
}
print(json.dumps(result, indent=2, sort_keys=True))
