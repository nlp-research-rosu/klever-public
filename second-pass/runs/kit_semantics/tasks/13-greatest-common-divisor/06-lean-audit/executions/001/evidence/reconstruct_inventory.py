#!/usr/bin/env python3
"""Independent Stage 3 inventory reconstruction using the trusted inventory code."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from tools.k_rule_inventory import canonical_json_sha256, inventory_verification


WORKSPACE = Path("/reference/k-proof")
MANIFEST = Path("/reference/lemma-discovery.json")


def main() -> None:
    inventory = inventory_verification(WORKSPACE)
    manifest = json.loads(MANIFEST.read_text())
    verification_lines = (WORKSPACE / "verification.k").read_text().splitlines()

    rules = inventory["rules"]
    manifest_rules = manifest["rules"]
    inventory_ids = [rule["source_rule_id"] for rule in rules]
    manifest_ids = [rule["source_rule_id"] for rule in manifest_rules]

    checks: dict[str, bool] = {
        "manifest_schema_version_2": manifest.get("schema_version") == 2,
        "inventory_schema_version_2": inventory.get("schema_version") == 2,
        "manifest_inventory_hash_matches": (
            manifest.get("inventory_sha256") == inventory["inventory_sha256"]
        ),
        "manifest_identity_order_matches": manifest_ids == inventory_ids,
        "inventory_ids_unique": len(inventory_ids) == len(set(inventory_ids)),
        "manifest_ids_unique": len(manifest_ids) == len(set(manifest_ids)),
        "same_identity_set": set(manifest_ids) == set(inventory_ids),
        "same_identity_count": len(manifest_ids) == len(inventory_ids),
        "whole_inventory_hash_recomputed": (
            canonical_json_sha256(rules) == inventory["inventory_sha256"]
        ),
    }

    reconstructed_rules: list[dict[str, object]] = []
    for rule in rules:
        normalized = " ".join(rule["text"].split())
        normalized_sha256 = hashlib.sha256(normalized.encode()).hexdigest()
        source_slice = "\n".join(
            verification_lines[rule["start_line"] - 1 : rule["end_line"]]
        )
        rule_checks = {
            "normalized_sha256_recomputed": (
                normalized_sha256 == rule["normalized_sha256"]
            ),
            "source_rule_id_recomputed": (
                rule["source_rule_id"] == f"rule-{normalized_sha256}"
            ),
            "source_span_text_matches": source_slice == rule["text"],
        }
        checks[f"{rule['source_rule_id']}:all_rule_checks"] = all(
            rule_checks.values()
        )
        reconstructed_rules.append(
            {
                **rule,
                "normalized_source": normalized,
                "recomputed_normalized_sha256": normalized_sha256,
                "recomputed_source_rule_id": f"rule-{normalized_sha256}",
                "source_slice": source_slice,
                "checks": rule_checks,
            }
        )

    result = {
        "trusted_tool": "/reference/tools/k_rule_inventory.py",
        "workspace": str(WORKSPACE),
        "manifest": str(MANIFEST),
        "verification_module": inventory["verification_module"],
        "verification_modules": inventory["verification_modules"],
        "verification_sha256": inventory["verification_sha256"],
        "inventory_sha256": inventory["inventory_sha256"],
        "inventory_rule_ids": inventory_ids,
        "manifest_rule_ids": manifest_ids,
        "checks": checks,
        "all_checks_pass": all(checks.values()),
        "rules": reconstructed_rules,
        "manifest_classifications": manifest_rules,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    if not result["all_checks_pass"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
