#!/usr/bin/env python3
"""Reconstruct and cross-check the frozen Stage 1 rule inventory."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from tools.k_rule_inventory import canonical_json_sha256, inventory_verification


workspace = Path("/reference/k-proof")
verification = workspace / "verification.k"
manifest_path = Path("/reference/lemma-discovery.json")

inventory = inventory_verification(workspace)
manifest = json.loads(manifest_path.read_text())
source_lines = verification.read_text().splitlines()

per_rule_checks = []
for rule in inventory["rules"]:
    source_span_text = "\n".join(
        source_lines[rule["start_line"] - 1 : rule["end_line"]]
    )
    normalized_sha256 = hashlib.sha256(
        " ".join(rule["text"].split()).encode()
    ).hexdigest()
    per_rule_checks.append(
        {
            "source_rule_id": rule["source_rule_id"],
            "source_span": {
                "start_line": rule["start_line"],
                "end_line": rule["end_line"],
            },
            "span_text_exact": source_span_text == rule["text"],
            "normalized_sha256_recomputed": normalized_sha256,
            "normalized_sha256_matches": (
                normalized_sha256 == rule["normalized_sha256"]
            ),
            "source_rule_id_recomputed": f"rule-{normalized_sha256}",
            "source_rule_id_matches": (
                f"rule-{normalized_sha256}" == rule["source_rule_id"]
            ),
        }
    )

inventory_ids = [rule["source_rule_id"] for rule in inventory["rules"]]
manifest_ids = [rule["source_rule_id"] for rule in manifest["rules"]]
manifest_id_set = set(manifest_ids)
inventory_id_set = set(inventory_ids)
inventory_hash_recomputed = canonical_json_sha256(inventory["rules"])

result = {
    "inventory": inventory,
    "cross_checks": {
        "verification_sha256_recomputed": hashlib.sha256(
            verification.read_bytes()
        ).hexdigest(),
        "inventory_sha256_recomputed": inventory_hash_recomputed,
        "inventory_sha256_self_matches": (
            inventory_hash_recomputed == inventory["inventory_sha256"]
        ),
        "manifest_inventory_sha256_matches": (
            manifest["inventory_sha256"] == inventory["inventory_sha256"]
        ),
        "manifest_rule_ids_in_exact_order": manifest_ids == inventory_ids,
        "manifest_rule_count": len(manifest_ids),
        "inventory_rule_count": len(inventory_ids),
        "manifest_has_duplicate_ids": len(manifest_ids) != len(manifest_id_set),
        "inventory_has_duplicate_ids": len(inventory_ids) != len(inventory_id_set),
        "omitted_from_manifest": sorted(inventory_id_set - manifest_id_set),
        "extra_in_manifest": sorted(manifest_id_set - inventory_id_set),
        "per_rule": per_rule_checks,
    },
}

print(json.dumps(result, indent=2, sort_keys=True))
