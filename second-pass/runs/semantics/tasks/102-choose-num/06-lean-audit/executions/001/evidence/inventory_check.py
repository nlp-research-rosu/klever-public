#!/usr/bin/env python3
"""Reconstruct and compare the canonical local verification-rule inventory."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from tools import k_rule_inventory, lemma_discovery_contract


WORKSPACE = Path("/reference/k-proof")
DISCOVERY = Path("/reference/lemma-discovery.json")
INPUT_MANIFEST = Path("/reference/klean-generation/input-manifest.json")


def main() -> int:
    inventory = k_rule_inventory.inventory_verification(WORKSPACE)
    discovery = json.loads(DISCOVERY.read_text())
    generated_input = json.loads(INPUT_MANIFEST.read_text())
    validated = lemma_discovery_contract.validate_trust_boundary(
        WORKSPACE, DISCOVERY
    )
    lines = (WORKSPACE / "verification.k").read_text().splitlines()
    checks: dict[str, dict[str, Any]] = {}

    def check(name: str, observed: Any, expected: Any) -> None:
        checks[name] = {
            "observed": observed,
            "expected": expected,
            "match": observed == expected,
        }

    manual_rule_checks: list[dict[str, Any]] = []
    for rule in inventory["rules"]:
        exact_span = "\n".join(
            lines[rule["start_line"] - 1 : rule["end_line"]]
        )
        normalized_hash = hashlib.sha256(
            " ".join(exact_span.split()).encode()
        ).hexdigest()
        manual_rule_checks.append(
            {
                "source_rule_id": rule["source_rule_id"],
                "module": rule["module"],
                "start_line": rule["start_line"],
                "end_line": rule["end_line"],
                "span_text_exact": exact_span == rule["text"],
                "normalized_sha256_observed": normalized_hash,
                "normalized_sha256_expected": rule["normalized_sha256"],
                "normalized_sha256_match": (
                    normalized_hash == rule["normalized_sha256"]
                ),
                "source_rule_id_match": (
                    rule["source_rule_id"] == f"rule-{normalized_hash}"
                ),
                "attributes": rule["attributes"],
                "text": rule["text"],
            }
        )

    check(
        "verification_sha256",
        inventory["verification_sha256"],
        hashlib.sha256(
            (WORKSPACE / "verification.k").read_bytes()
        ).hexdigest(),
    )
    check(
        "verification_module",
        inventory["verification_module"],
        "CHOOSE-NUM-VERIFICATION",
    )
    check(
        "local_module_closure",
        inventory["verification_modules"],
        ["CHOOSE-NUM-VERIFICATION"],
    )
    check(
        "inventory_sha256_manual",
        k_rule_inventory.canonical_json_sha256(inventory["rules"]),
        inventory["inventory_sha256"],
    )
    check(
        "discovery.inventory_sha256",
        discovery["inventory_sha256"],
        inventory["inventory_sha256"],
    )
    canonical_ids = [
        rule["source_rule_id"] for rule in inventory["rules"]
    ]
    discovery_ids = [
        rule["source_rule_id"] for rule in discovery["rules"]
    ]
    check("discovery.ordered_source_rule_ids", discovery_ids, canonical_ids)
    check(
        "discovery.no_duplicate_source_rule_ids",
        len(discovery_ids),
        len(set(discovery_ids)),
    )
    check("discovery.rule_count", len(discovery_ids), len(canonical_ids))
    check(
        "generated_input.inventory_sha256",
        generated_input["inventory_sha256"],
        inventory["inventory_sha256"],
    )
    check(
        "generated_input.ordered_classified_source_rule_ids",
        [
            entry["source_rule_id"]
            for bucket in ("definitions", "operational_rules")
            for entry in generated_input[bucket]
        ],
        canonical_ids,
    )
    check(
        "all_manual_rule_checks",
        all(
            item["span_text_exact"]
            and item["normalized_sha256_match"]
            and item["source_rule_id_match"]
            for item in manual_rule_checks
        ),
        True,
    )
    simplification_misclassifications = []
    classifications = {
        rule["source_rule_id"]: rule["classification"]
        for rule in discovery["rules"]
    }
    for rule in inventory["rules"]:
        classification = classifications[rule["source_rule_id"]]
        if (
            "simplification" in rule["attributes"]
            and classification not in {"DEFINITION", "DOMAIN_LEMMA"}
        ):
            simplification_misclassifications.append(
                rule["source_rule_id"]
            )
    check(
        "simplification_classification_policy",
        simplification_misclassifications,
        [],
    )

    partition = {
        name: [item["source_rule_id"] for item in validated[name]]
        for name in (
            "definitions",
            "operational_rules",
            "proved_derived_lemmas",
            "domain_lemmas",
        )
    }
    failures = [name for name, item in checks.items() if not item["match"]]
    print(
        json.dumps(
            {
                "schema_version": 1,
                "inventory": inventory,
                "manual_rule_checks": manual_rule_checks,
                "validated_partition": partition,
                "checks": checks,
                "failure_count": len(failures),
                "failures": failures,
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
