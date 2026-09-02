#!/usr/bin/env python3
"""Read-only independent reconstruction and bijection check for this audit."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from tools.k_rule_inventory import canonical_json_sha256, inventory_verification


WORKSPACE = Path("/reference/k-proof")
DISCOVERY = Path("/reference/lemma-discovery.json")


inventory = inventory_verification(WORKSPACE)
discovery = json.loads(DISCOVERY.read_text())
rules = inventory["rules"]
classified = discovery["rules"]

checks: dict[str, object] = {}
checks["verification_sha256_recomputed"] = (
    hashlib.sha256((WORKSPACE / "verification.k").read_bytes()).hexdigest()
    == inventory["verification_sha256"]
)
checks["inventory_sha256_recomputed"] = (
    canonical_json_sha256(rules) == inventory["inventory_sha256"]
)
checks["manifest_inventory_sha256_matches"] = (
    discovery["inventory_sha256"] == inventory["inventory_sha256"]
)

inventory_ids = [rule["source_rule_id"] for rule in rules]
manifest_ids = [entry["source_rule_id"] for entry in classified]
checks["inventory_ids_unique"] = len(inventory_ids) == len(set(inventory_ids))
checks["manifest_ids_unique"] = len(manifest_ids) == len(set(manifest_ids))
checks["same_rule_count"] = len(inventory_ids) == len(manifest_ids)
checks["ordered_identity_bijection"] = inventory_ids == manifest_ids
checks["set_bijection"] = set(inventory_ids) == set(manifest_ids)
checks["ids_embed_normalized_sha256"] = all(
    rule["source_rule_id"] == f"rule-{rule['normalized_sha256']}"
    for rule in rules
)
checks["valid_source_spans"] = all(
    isinstance(rule["start_line"], int)
    and isinstance(rule["end_line"], int)
    and 1 <= rule["start_line"] <= rule["end_line"]
    for rule in rules
)

print("RECONSTRUCTED INVENTORY")
print(json.dumps(inventory, indent=2, sort_keys=True, ensure_ascii=False))
print("\nDISCOVERY ORDER AND CLASSIFICATIONS")
print(json.dumps(classified, indent=2, sort_keys=True, ensure_ascii=False))
print("\nBIJECTION CHECKS")
print(json.dumps(checks, indent=2, sort_keys=True))

if not all(value is True for value in checks.values()):
    raise SystemExit(1)
