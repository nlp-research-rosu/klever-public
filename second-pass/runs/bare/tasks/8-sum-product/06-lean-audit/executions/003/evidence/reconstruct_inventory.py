#!/usr/bin/env python3
"""Independently reconstruct and compare the frozen Stage 1 rule inventory."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from tools import k_rule_inventory, lemma_discovery_contract


WORKSPACE = Path("/reference/k-proof")
DISCOVERY = Path("/reference/lemma-discovery.json")


inventory = k_rule_inventory.inventory_verification(WORKSPACE)
discovery_bytes = DISCOVERY.read_bytes()
discovery = json.loads(discovery_bytes)
validated = lemma_discovery_contract.validate_trust_boundary(
    WORKSPACE, DISCOVERY
)

inventory_ids = [rule["source_rule_id"] for rule in inventory["rules"]]
discovery_rules = discovery.get("rules")
if not isinstance(discovery_rules, list):
    raise SystemExit("FAIL: discovery rules is not a list")
discovery_ids = [rule.get("source_rule_id") for rule in discovery_rules]

checks = {
    "verification_sha256_matches_recomputed": (
        inventory["verification_sha256"]
        == hashlib.sha256((WORKSPACE / "verification.k").read_bytes()).hexdigest()
    ),
    "inventory_sha256_matches_recomputed": (
        inventory["inventory_sha256"]
        == k_rule_inventory.canonical_json_sha256(inventory["rules"])
    ),
    "discovery_inventory_sha256_matches": (
        discovery.get("inventory_sha256") == inventory["inventory_sha256"]
    ),
    "inventory_ids_unique": len(inventory_ids) == len(set(inventory_ids)),
    "discovery_ids_unique": len(discovery_ids) == len(set(discovery_ids)),
    "identity_order_exact": discovery_ids == inventory_ids,
    "identity_sets_exact": set(discovery_ids) == set(inventory_ids),
    "counts_exact": len(discovery_ids) == len(inventory_ids),
    "validated_contract_inventory_exact": (
        validated["inventory_sha256"] == inventory["inventory_sha256"]
        and validated["rules"] == inventory["rules"]
    ),
}

print("DISCOVERY_SHA256", hashlib.sha256(discovery_bytes).hexdigest())
print("RECONSTRUCTED_INVENTORY")
print(json.dumps(inventory, indent=2, sort_keys=True))
print("DISCOVERY_IDENTITIES")
print(json.dumps(discovery_ids, indent=2))
print("CHECKS")
print(json.dumps(checks, indent=2, sort_keys=True))
if not all(checks.values()):
    raise SystemExit("FAIL: inventory/discovery comparison is not bijective")
print("RESULT PASS: exact ordered bijection and hashes confirmed")
