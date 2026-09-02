#!/usr/bin/env python3
"""Fresh Stage 3 inventory reconstruction using the trusted inventory code."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from tools import k_rule_inventory, lemma_discovery_contract


WORKSPACE = Path("/reference/k-proof")
MANIFEST_PATH = Path("/reference/lemma-discovery.json")
OUTPUT = Path("/audit-output/evidence/01_reconstructed_inventory.json")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


inventory = k_rule_inventory.inventory_verification(WORKSPACE)
validated = lemma_discovery_contract.validate_trust_boundary(
    WORKSPACE, MANIFEST_PATH
)
manifest = json.loads(MANIFEST_PATH.read_text())
verification_lines = (WORKSPACE / "verification.k").read_text().splitlines()

inventory_ids = [rule["source_rule_id"] for rule in inventory["rules"]]
manifest_ids = [rule["source_rule_id"] for rule in manifest["rules"]]
manifest_by_id = {
    rule["source_rule_id"]: rule for rule in manifest["rules"]
}

rule_checks = []
for position, rule in enumerate(inventory["rules"]):
    span_text = "\n".join(
        verification_lines[rule["start_line"] - 1 : rule["end_line"]]
    )
    normalized = " ".join(span_text.split())
    normalized_sha256 = sha256_bytes(normalized.encode())
    classified = manifest_by_id.get(rule["source_rule_id"])
    rule_checks.append(
        {
            "position": position,
            "source_rule_id": rule["source_rule_id"],
            "module": rule["module"],
            "source_span": {
                "start_line": rule["start_line"],
                "end_line": rule["end_line"],
            },
            "attributes": rule["attributes"],
            "text": rule["text"],
            "span_text_matches": span_text == rule["text"],
            "normalized_text": normalized,
            "recorded_normalized_sha256": rule["normalized_sha256"],
            "recomputed_normalized_sha256": normalized_sha256,
            "normalized_hash_matches": (
                normalized_sha256 == rule["normalized_sha256"]
            ),
            "source_rule_id_matches_hash": (
                rule["source_rule_id"] == f"rule-{normalized_sha256}"
            ),
            "classification": (
                None if classified is None else classified["classification"]
            ),
            "rationale": (
                None if classified is None else classified["rationale"]
            ),
        }
    )

recomputed_inventory_sha256 = k_rule_inventory.canonical_json_sha256(
    inventory["rules"]
)
result = {
    "command": (
        "PYTHONPATH=/reference python3 "
        "/audit-output/evidence/01_reconstruct_inventory.py"
    ),
    "trusted_inventory_tool": {
        "path": "/reference/tools/k_rule_inventory.py",
        "sha256": sha256_bytes(
            Path("/reference/tools/k_rule_inventory.py").read_bytes()
        ),
    },
    "inventory": inventory,
    "checks": {
        "verification_closure": inventory["verification_modules"],
        "inventory_rule_count": len(inventory_ids),
        "manifest_rule_count": len(manifest_ids),
        "inventory_ids_unique": len(inventory_ids) == len(set(inventory_ids)),
        "manifest_ids_unique": len(manifest_ids) == len(set(manifest_ids)),
        "identity_sets_match": set(inventory_ids) == set(manifest_ids),
        "identity_order_matches": inventory_ids == manifest_ids,
        "manifest_inventory_sha256": manifest["inventory_sha256"],
        "tool_inventory_sha256": inventory["inventory_sha256"],
        "recomputed_inventory_sha256": recomputed_inventory_sha256,
        "all_inventory_hashes_match": (
            manifest["inventory_sha256"]
            == inventory["inventory_sha256"]
            == recomputed_inventory_sha256
        ),
        "all_spans_match": all(x["span_text_matches"] for x in rule_checks),
        "all_normalized_hashes_match": all(
            x["normalized_hash_matches"] for x in rule_checks
        ),
        "all_source_rule_ids_match_hash": all(
            x["source_rule_id_matches_hash"] for x in rule_checks
        ),
        "trusted_contract_validation_succeeded": True,
        "validated_partition_counts": {
            "definitions": len(validated["definitions"]),
            "operational_rules": len(validated["operational_rules"]),
            "proved_derived_lemmas": len(
                validated["proved_derived_lemmas"]
            ),
            "domain_lemmas": len(validated["domain_lemmas"]),
        },
    },
    "rule_checks": rule_checks,
}

OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
print(json.dumps(result, indent=2, sort_keys=True))
