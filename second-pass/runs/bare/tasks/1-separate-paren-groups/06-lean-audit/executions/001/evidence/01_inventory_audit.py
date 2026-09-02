#!/usr/bin/env python3
"""Independent Stage 3 inventory reconstruction and ordered comparison."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from tools.k_rule_inventory import canonical_json_sha256, inventory_verification


WORKSPACE = Path("/reference/k-proof")
DISCOVERY = Path("/reference/lemma-discovery.json")


def main() -> None:
    inventory = inventory_verification(WORKSPACE)
    discovery = json.loads(DISCOVERY.read_text())
    source = (WORKSPACE / "verification.k").read_text()
    source_lines = source.splitlines()
    rules = inventory["rules"]
    discovered = discovery["rules"]

    checks: dict[str, bool] = {}
    checks["inventory_schema_v2"] = inventory["schema_version"] == 2
    checks["verification_module_exact"] = (
        inventory["verification_module"] == "MPY-VERIFICATION"
    )
    checks["local_module_closure_exact"] = (
        inventory["verification_modules"] == ["MPY-VERIFICATION"]
    )
    checks["verification_sha256_recomputed"] = (
        inventory["verification_sha256"]
        == hashlib.sha256((WORKSPACE / "verification.k").read_bytes()).hexdigest()
    )
    checks["inventory_sha256_recomputed"] = (
        inventory["inventory_sha256"] == canonical_json_sha256(rules)
    )
    checks["inventory_hash_matches_discovery"] = (
        inventory["inventory_sha256"] == discovery["inventory_sha256"]
    )
    checks["rule_count_matches"] = len(rules) == len(discovered)

    rule_details: list[dict[str, object]] = []
    per_rule_ok: list[bool] = []
    for index, rule in enumerate(rules):
        normalized = " ".join(rule["text"].split())
        normalized_sha256 = hashlib.sha256(normalized.encode()).hexdigest()
        source_rule_id = f"rule-{normalized_sha256}"
        source_span = "\n".join(
            source_lines[rule["start_line"] - 1 : rule["end_line"]]
        )
        discovery_rule = discovered[index] if index < len(discovered) else {}
        local_checks = {
            "source_span_exact": source_span == rule["text"],
            "normalized_sha256_exact": (
                normalized_sha256 == rule["normalized_sha256"]
            ),
            "source_rule_id_exact": source_rule_id == rule["source_rule_id"],
            "ordered_discovery_identity_exact": (
                discovery_rule.get("source_rule_id") == rule["source_rule_id"]
            ),
            "classification_accounted": discovery_rule.get("classification")
            in {
                "DEFINITION",
                "OPERATIONAL_RULE",
                "PROVED_DERIVED_LEMMA",
                "DOMAIN_LEMMA",
            },
        }
        per_rule_ok.extend(local_checks.values())
        rule_details.append(
            {
                "ordinal": index + 1,
                "module": rule["module"],
                "source_span": {
                    "start_line": rule["start_line"],
                    "end_line": rule["end_line"],
                },
                "attributes": rule["attributes"],
                "text": rule["text"],
                "normalized_source": normalized,
                "normalized_sha256": normalized_sha256,
                "source_rule_id": source_rule_id,
                "discovery_classification": discovery_rule.get("classification"),
                "discovery_rationale": discovery_rule.get("rationale"),
                "checks": local_checks,
            }
        )

    inventory_ids = [rule["source_rule_id"] for rule in rules]
    discovery_ids = [rule.get("source_rule_id") for rule in discovered]
    normalized_hashes = [rule["normalized_sha256"] for rule in rules]
    checks["all_per_rule_recomputations_pass"] = all(per_rule_ok)
    checks["no_inventory_duplicate_ids"] = len(inventory_ids) == len(
        set(inventory_ids)
    )
    checks["no_discovery_duplicate_ids"] = len(discovery_ids) == len(
        set(discovery_ids)
    )
    checks["no_duplicate_normalized_hashes"] = len(normalized_hashes) == len(
        set(normalized_hashes)
    )
    checks["ordered_identity_bijection"] = inventory_ids == discovery_ids
    checks["no_unaccounted_classifications"] = all(
        rule.get("classification")
        in {
            "DEFINITION",
            "OPERATIONAL_RULE",
            "PROVED_DERIVED_LEMMA",
            "DOMAIN_LEMMA",
        }
        for rule in discovered
    )
    checks["no_simplification_rules"] = all(
        "simplification" not in rule["attributes"] for rule in rules
    )

    result = {
        "command_intent": (
            "inventory_verification(/reference/k-proof), followed by independent "
            "span/hash/ID/inventory-hash recomputation and ordered manifest comparison"
        ),
        "inventory_header": {
            key: inventory[key]
            for key in (
                "schema_version",
                "verification_file",
                "verification_sha256",
                "verification_module",
                "verification_modules",
                "inventory_sha256",
            )
        },
        "counts": {
            "inventory_rules": len(rules),
            "discovery_rules": len(discovered),
        },
        "checks": checks,
        "rules": rule_details,
        "status": "PASS" if all(checks.values()) else "FAIL",
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
