#!/usr/bin/env python3
"""Independent Stage 3 category and Stage 4 empty-bijection checks."""

from __future__ import annotations

import json
from pathlib import Path

from tools import klean_export


ROOT = Path("/reference")
GENERATION = ROOT / "klean-generation"
GENERATED = GENERATION / "generated"

# Human classification from the frozen source and supplied operational
# semantics. These are deliberately fixed here rather than copied from Stage 3.
OPERATIONAL_IDS = {
    "rule-5b53e5e1e7c389a2532855b2ec7b9b198ac32e2c188993cc5f36766b5113bf5f"
}


def main() -> int:
    inventory = json.loads(
        Path("/audit-output/evidence/reconstructed-inventory.json").read_text()
    )
    discovery = json.loads((ROOT / "lemma-discovery.json").read_text())
    input_manifest = json.loads((GENERATION / "input-manifest.json").read_text())
    generator_manifest = json.loads(
        (GENERATION / "generator-manifest.json").read_text()
    )
    export_result = json.loads((GENERATION / "export-result.json").read_text())
    obligation_map = json.loads(
        (GENERATED / "obligation-map.json").read_text()
    )
    audit = json.loads(Path("/audit-input.json").read_text())

    independent: list[dict[str, str]] = []
    for rule in inventory["rules"]:
        source_rule_id = rule["source_rule_id"]
        classification = (
            "OPERATIONAL_RULE"
            if source_rule_id in OPERATIONAL_IDS
            else "DEFINITION"
        )
        independent.append(
            {
                "source_rule_id": source_rule_id,
                "classification": classification,
            }
        )

    stage3_categories = [
        {
            "source_rule_id": entry["source_rule_id"],
            "classification": entry["classification"],
        }
        for entry in discovery["rules"]
    ]
    independent_domain_ids = [
        entry["source_rule_id"]
        for entry in independent
        if entry["classification"] == "DOMAIN_LEMMA"
    ]

    discovery_by_id = {
        entry["source_rule_id"]: entry for entry in discovery["rules"]
    }
    expected_full = [
        {**rule, **discovery_by_id[rule["source_rule_id"]]}
        for rule in inventory["rules"]
    ]
    expected_definitions = [
        entry for entry in expected_full if entry["classification"] == "DEFINITION"
    ]
    expected_operational = [
        entry
        for entry in expected_full
        if entry["classification"] == "OPERATIONAL_RULE"
    ]
    expected_derived = [
        entry
        for entry in expected_full
        if entry["classification"] == "PROVED_DERIVED_LEMMA"
    ]

    observed_target = klean_export.target_statement(GENERATED)
    expected_target_definition = klean_export.expected_target_definition(
        obligation_map
    )
    launcher = audit["resolution"]
    checks: list[dict[str, object]] = []

    def check(label: str, actual: object, expected: object) -> None:
        checks.append(
            {
                "label": label,
                "actual": actual,
                "expected": expected,
                "match": actual == expected,
            }
        )

    check(
        "all 26 Stage 3 categories equal independent categories in source order",
        stage3_categories,
        independent,
    )
    check("independent DOMAIN_LEMMA set", independent_domain_ids, [])
    check(
        "input-manifest definitions",
        input_manifest["definitions"],
        expected_definitions,
    )
    check(
        "input-manifest operational rules",
        input_manifest["operational_rules"],
        expected_operational,
    )
    check(
        "input-manifest proved derived lemmas",
        input_manifest["proved_derived_lemmas"],
        expected_derived,
    )
    check("input-manifest source rules", input_manifest["source_rules"], [])
    check("obligation-map source rules", obligation_map["source_rules"], [])
    check("obligation-map obligations", obligation_map["obligations"], [])
    check("obligation-map trust parameters", obligation_map["trust_parameters"], [])
    check(
        "empty independent domain set maps bijectively to zero obligations",
        {
            "source_rule_ids": obligation_map["source_rules"],
            "obligation_source_rule_ids": [
                entry.get("source_rule_id")
                for entry in obligation_map["obligations"]
            ],
        },
        {"source_rule_ids": [], "obligation_source_rule_ids": []},
    )
    check(
        "no expected target definition for zero obligations",
        expected_target_definition,
        None,
    )
    check("generated target declaration", observed_target, None)
    check("generator-manifest target", generator_manifest["target"], None)
    check("launcher target", launcher["target"], None)
    check(
        "generator obligation count",
        generator_manifest["obligation_count"],
        0,
    )
    check("export obligation count", export_result["obligation_count"], 0)
    check("export status", export_result["status"], "KLEAN_NO_OBLIGATIONS")
    check(
        "selected Stage 4 status",
        launcher["selections"]["klean_generation"]["status"],
        "KLEAN_NO_OBLIGATIONS",
    )
    check("Stage 5 result absent", launcher["stage5_result"], None)
    check(
        "Stage 5 candidate directory absent",
        Path("/candidate").exists() or Path("/candidate").is_symlink(),
        False,
    )

    mismatches = [entry for entry in checks if not entry["match"]]
    report = {
        "independent_counts": {
            "DEFINITION": sum(
                entry["classification"] == "DEFINITION" for entry in independent
            ),
            "OPERATIONAL_RULE": sum(
                entry["classification"] == "OPERATIONAL_RULE"
                for entry in independent
            ),
            "PROVED_DERIVED_LEMMA": sum(
                entry["classification"] == "PROVED_DERIVED_LEMMA"
                for entry in independent
            ),
            "DOMAIN_LEMMA": len(independent_domain_ids),
        },
        "check_count": len(checks),
        "mismatch_count": len(mismatches),
        "checks": checks,
        "status": "PASS" if not mismatches else "FAIL",
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    return 1 if mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
