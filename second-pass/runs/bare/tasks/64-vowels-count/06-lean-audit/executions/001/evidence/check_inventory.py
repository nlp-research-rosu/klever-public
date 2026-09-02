#!/usr/bin/env python3
"""Independent Stage 3 inventory and identity checks for this audit."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, "/reference")

from tools.k_rule_inventory import canonical_json_sha256, inventory_verification


workspace = Path("/reference/k-proof")
manifest_path = Path("/reference/lemma-discovery.json")
verification_path = workspace / "verification.k"

inventory = inventory_verification(workspace)
manifest = json.loads(manifest_path.read_text())
source_lines = verification_path.read_text().splitlines()

checks: dict[str, object] = {}
checks["manifest_rule_count"] = len(manifest["rules"])
checks["inventory_rule_count"] = len(inventory["rules"])
checks["manifest_inventory_sha256_matches"] = (
    manifest["inventory_sha256"] == inventory["inventory_sha256"]
)
checks["manifest_ids_exact_order_match"] = [
    entry["source_rule_id"] for entry in manifest["rules"]
] == [rule["source_rule_id"] for rule in inventory["rules"]]
checks["manifest_ids_unique"] = len(
    {entry["source_rule_id"] for entry in manifest["rules"]}
) == len(manifest["rules"])
checks["inventory_ids_unique"] = len(
    {rule["source_rule_id"] for rule in inventory["rules"]}
) == len(inventory["rules"])

rule_recomputations: list[dict[str, object]] = []
for rule in inventory["rules"]:
    normalized = " ".join(rule["text"].split())
    normalized_sha256 = hashlib.sha256(normalized.encode()).hexdigest()
    span_text = "\n".join(
        source_lines[rule["start_line"] - 1 : rule["end_line"]]
    ).rstrip(" \t\r\n")
    rule_recomputations.append(
        {
            "source_rule_id": rule["source_rule_id"],
            "module": rule["module"],
            "start_line": rule["start_line"],
            "end_line": rule["end_line"],
            "attributes": rule["attributes"],
            "text": rule["text"],
            "span_text": span_text,
            "span_text_exact_match": span_text == rule["text"],
            "recorded_normalized_sha256": rule["normalized_sha256"],
            "recomputed_normalized_sha256": normalized_sha256,
            "normalized_sha256_match": (
                normalized_sha256 == rule["normalized_sha256"]
            ),
            "recomputed_source_rule_id": f"rule-{normalized_sha256}",
            "source_rule_id_match": (
                rule["source_rule_id"] == f"rule-{normalized_sha256}"
            ),
        }
    )

independent_inventory_sha256 = hashlib.sha256(
    json.dumps(
        inventory["rules"],
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode()
).hexdigest()
checks["trusted_inventory_sha256"] = inventory["inventory_sha256"]
checks["trusted_canonical_recomputation"] = canonical_json_sha256(
    inventory["rules"]
)
checks["independent_inventory_sha256"] = independent_inventory_sha256
checks["whole_inventory_hash_match"] = (
    independent_inventory_sha256 == inventory["inventory_sha256"]
)
checks["all_rule_recomputations_match"] = all(
    item["span_text_exact_match"]
    and item["normalized_sha256_match"]
    and item["source_rule_id_match"]
    for item in rule_recomputations
)
checks["bijection_and_order_pass"] = all(
    checks[name]
    for name in (
        "manifest_inventory_sha256_matches",
        "manifest_ids_exact_order_match",
        "manifest_ids_unique",
        "inventory_ids_unique",
        "whole_inventory_hash_match",
        "all_rule_recomputations_match",
    )
)

print(
    json.dumps(
        {
            "inventory": inventory,
            "rule_recomputations": rule_recomputations,
            "checks": checks,
        },
        indent=2,
        sort_keys=True,
    )
)
