#!/usr/bin/env python3
"""Reconstruct and compare the Stage 3 rule inventory with trusted tooling."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from tools import k_rule_inventory, lemma_discovery_contract


WORKSPACE = Path("/reference/k-proof")
MANIFEST_PATH = Path("/reference/lemma-discovery.json")


def main() -> None:
    inventory = k_rule_inventory.inventory_verification(WORKSPACE)
    manifest = json.loads(MANIFEST_PATH.read_text())
    validated = lemma_discovery_contract.validate_trust_boundary(
        WORKSPACE, MANIFEST_PATH
    )
    verification_lines = (WORKSPACE / "verification.k").read_text().splitlines()

    canonical_ids = [rule["source_rule_id"] for rule in inventory["rules"]]
    manifest_ids = [rule["source_rule_id"] for rule in manifest["rules"]]
    per_rule = []
    for rule in inventory["rules"]:
        start = rule["start_line"]
        end = rule["end_line"]
        source_slice = "\n".join(verification_lines[start - 1 : end])
        normalized = " ".join(source_slice.split())
        normalized_sha256 = hashlib.sha256(normalized.encode()).hexdigest()
        per_rule.append(
            {
                "source_rule_id": rule["source_rule_id"],
                "module": rule["module"],
                "start_line": start,
                "end_line": end,
                "attributes": rule["attributes"],
                "text": rule["text"],
                "source_slice_exact": source_slice == rule["text"],
                "recomputed_normalized_sha256": normalized_sha256,
                "normalized_sha256_matches": (
                    normalized_sha256 == rule["normalized_sha256"]
                ),
                "source_rule_id_matches": (
                    rule["source_rule_id"] == f"rule-{normalized_sha256}"
                ),
            }
        )

    classification_counts = {
        name: len(validated[name])
        for name in (
            "definitions",
            "operational_rules",
            "proved_derived_lemmas",
            "domain_lemmas",
        )
    }
    result = {
        "verification_file": inventory["verification_file"],
        "verification_sha256": inventory["verification_sha256"],
        "verification_module": inventory["verification_module"],
        "verification_modules": inventory["verification_modules"],
        "canonical_rule_count": len(canonical_ids),
        "manifest_rule_count": len(manifest_ids),
        "canonical_ids": canonical_ids,
        "manifest_ids": manifest_ids,
        "ordered_identity_match": manifest_ids == canonical_ids,
        "canonical_ids_unique": len(canonical_ids) == len(set(canonical_ids)),
        "manifest_ids_unique": len(manifest_ids) == len(set(manifest_ids)),
        "inventory_sha256": inventory["inventory_sha256"],
        "manifest_inventory_sha256": manifest["inventory_sha256"],
        "inventory_hash_match": (
            inventory["inventory_sha256"] == manifest["inventory_sha256"]
        ),
        "trusted_contract_validation": "PASS",
        "classification_counts": classification_counts,
        "explicit_simplification_rule_ids": [
            rule["source_rule_id"]
            for rule in inventory["rules"]
            if "simplification" in rule["attributes"]
        ],
        "per_rule": per_rule,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
