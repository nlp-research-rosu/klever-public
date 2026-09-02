#!/usr/bin/env python3
"""Independent Stage 4 hash, bijection, and fixed-target verification."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from tools import klean_export
from tools.lemma_discovery_contract import validate_trust_boundary


FROZEN = Path("/reference/k-proof")
DISCOVERY = Path("/reference/lemma-discovery.json")
GENERATION = Path("/reference/klean-generation")
GENERATED = GENERATION / "generated"


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    discovery_hash = file_sha256(DISCOVERY)
    validated = validate_trust_boundary(FROZEN, DISCOVERY)
    expected_source_rules = [
        {
            **rule,
            "inventory_sha256": validated["inventory_sha256"],
            "discovery_manifest_sha256": discovery_hash,
        }
        for rule in validated["domain_lemmas"]
    ]
    obligation_map_path = GENERATED / "obligation-map.json"
    obligation_map = json.loads(obligation_map_path.read_text())
    input_manifest = json.loads((GENERATION / "input-manifest.json").read_text())
    generator_manifest = json.loads(
        (GENERATION / "generator-manifest.json").read_text()
    )
    preflight = json.loads((GENERATION / "preflight.json").read_text())
    export_result = json.loads((GENERATION / "export-result.json").read_text())
    audit_input = json.loads(Path("/audit-input.json").read_text())

    obligations = obligation_map["obligations"]
    source_rules = obligation_map["source_rules"]
    expected_ids = [rule["source_rule_id"] for rule in expected_source_rules]
    source_ids = [rule["source_rule_id"] for rule in source_rules]
    obligation_ids = [item["source_rule_id"] for item in obligations]
    obligation_checks = []
    for source, obligation in zip(expected_source_rules, obligations):
        lean_conjunct = obligation["lean_conjunct"]
        obligation_checks.append(
            {
                "source_rule_id": source["source_rule_id"],
                "id_matches": (
                    obligation["source_rule_id"] == source["source_rule_id"]
                ),
                "source_span_matches": obligation["source_span"]
                == {
                    "start_line": source["start_line"],
                    "end_line": source["end_line"],
                },
                "normalized_hash_matches": (
                    obligation["normalized_sha256"]
                    == source["normalized_sha256"]
                ),
                "inventory_hash_matches": (
                    obligation["inventory_sha256"]
                    == source["inventory_sha256"]
                ),
                "discovery_hash_matches": (
                    obligation["discovery_manifest_sha256"]
                    == source["discovery_manifest_sha256"]
                ),
                "conjunct_hash_matches": (
                    obligation["lean_conjunct_sha256"]
                    == hashlib.sha256(lean_conjunct.encode()).hexdigest()
                ),
                "lean_conjunct": lean_conjunct,
            }
        )

    parsed_target = klean_export.target_statement(GENERATED)
    expected_definition = klean_export.expected_target_definition(obligation_map)
    expected_definition_sha256 = (
        hashlib.sha256(expected_definition.encode()).hexdigest()
        if expected_definition is not None
        else None
    )
    recorded_targets = {
        "generator_manifest": generator_manifest.get("target"),
        "preflight": preflight.get("target"),
        "audit_input_target": audit_input["resolution"].get("target"),
        "audit_input_stage4_preflight": audit_input["resolution"][
            "stage4_preflight"
        ].get("target"),
    }
    target_identity_match = all(
        target == parsed_target for target in recorded_targets.values()
    )
    generated_tree_hash = klean_export.tree_digest(GENERATED)
    report = {
        "expected_domain_rule_ids": expected_ids,
        "mapped_source_rule_ids": source_ids,
        "obligation_rule_ids": obligation_ids,
        "source_rule_records_exact": source_rules == expected_source_rules,
        "source_rule_order_exact": source_ids == expected_ids,
        "obligation_order_exact": obligation_ids == expected_ids,
        "source_rule_ids_unique": len(source_ids) == len(set(source_ids)),
        "obligation_ids_unique": (
            len(obligation_ids) == len(set(obligation_ids))
        ),
        "obligation_count": len(obligations),
        "generator_obligation_count": generator_manifest.get(
            "obligation_count"
        ),
        "obligation_checks": obligation_checks,
        "obligation_map_actual_sha256": file_sha256(obligation_map_path),
        "obligation_map_manifest_sha256": generator_manifest.get(
            "obligation_map_sha256"
        ),
        "generated_tree_actual_sha256": generated_tree_hash,
        "generated_tree_manifest_sha256": generator_manifest.get(
            "generated_tree_sha256"
        ),
        "generated_tree_audit_input_sha256": audit_input["resolution"][
            "hashes"
        ]["generated_tree_sha256"],
        "parsed_target": parsed_target,
        "recorded_targets": recorded_targets,
        "target_identity_match": target_identity_match,
        "expected_target_definition": expected_definition,
        "expected_target_definition_sha256": expected_definition_sha256,
        "target_definition_hash_exact": (
            parsed_target is not None
            and parsed_target["definition_sha256"]
            == expected_definition_sha256
        ),
        "target_statement_hash_exact": (
            parsed_target is not None
            and parsed_target["statement_sha256"]
            == hashlib.sha256(parsed_target["statement"].encode()).hexdigest()
        ),
        "input_manifest_source_rules_exact": (
            input_manifest.get("source_rules") == expected_source_rules
        ),
        "export_status": export_result.get("status"),
        "preflight_status": preflight.get("status"),
    }
    report["stage4_structural_pass"] = all(
        (
            report["source_rule_records_exact"],
            report["source_rule_order_exact"],
            report["obligation_order_exact"],
            report["source_rule_ids_unique"],
            report["obligation_ids_unique"],
            len(obligations) == len(expected_ids),
            generator_manifest.get("obligation_count") == len(expected_ids),
            all(
                all(value for key, value in check.items() if key.endswith("matches"))
                for check in obligation_checks
            ),
            report["obligation_map_actual_sha256"]
            == report["obligation_map_manifest_sha256"],
            report["generated_tree_actual_sha256"]
            == report["generated_tree_manifest_sha256"]
            == report["generated_tree_audit_input_sha256"],
            report["target_identity_match"],
            report["target_definition_hash_exact"],
            report["target_statement_hash_exact"],
            report["input_manifest_source_rules_exact"],
            report["export_status"] == "OK",
            report["preflight_status"] == "PASS",
        )
    )
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
