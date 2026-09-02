#!/usr/bin/env python3
"""Independent Stage 4 source/obligation/target identity checks."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

from tools import k_rule_inventory, klean_export


WORKSPACE = Path("/reference/k-proof")
DISCOVERY = Path("/reference/lemma-discovery.json")
GENERATION = Path("/reference/klean-generation")
GENERATED = GENERATION / "generated"

DOMAIN_RULE_ID = (
    "rule-0680c25a908725567264bc3a1d17a1d702f13c46cc6da2b783839bbc14a5d477"
)
EXPECTED_CONJUNCT = (
    "∀ (I : SortInt) (N : SortInt), "
    "(«_-Int_» N («_+Int_» I 1) : SortInt) = "
    "(«_+Int_» («_-Int_» N I) (-1) : SortInt)"
)


def sha256_bytes(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    audit_input = json.loads(Path("/audit-input.json").read_text())
    audit_target = audit_input["resolution"]["target"]
    discovery = json.loads(DISCOVERY.read_text())
    input_manifest = json.loads((GENERATION / "input-manifest.json").read_text())
    generator_manifest = json.loads(
        (GENERATION / "generator-manifest.json").read_text()
    )
    obligation_map_path = GENERATED / "obligation-map.json"
    obligation_map = json.loads(obligation_map_path.read_text())
    export_result = json.loads((GENERATION / "export-result.json").read_text())
    inventory = k_rule_inventory.inventory_verification(WORKSPACE)

    independently_domain_ids = [DOMAIN_RULE_ID]
    source_ids = [item["source_rule_id"] for item in obligation_map["source_rules"]]
    obligation_ids = [
        item["source_rule_id"] for item in obligation_map["obligations"]
    ]
    conjuncts = [item["lean_conjunct"] for item in obligation_map["obligations"]]
    parameters = obligation_map["trust_parameters"]

    recomputed_bindings = []
    for parameter in parameters:
        binding = {
            "kore_symbol": parameter["kore_symbol"],
            "name": parameter["name"],
            "type": parameter["type"],
            "source_rule_ids": parameter["source_rule_ids"],
        }
        recomputed_bindings.append(
            {
                **binding,
                "recorded_binding_sha256": parameter["binding_sha256"],
                "recomputed_binding_sha256": klean_export.sha256_text(
                    json.dumps(binding, sort_keys=True, separators=(",", ":"))
                ),
            }
        )

    expected_definition = klean_export.expected_target_definition(obligation_map)
    observed_target = klean_export.target_statement(GENERATED)
    lemma_text = (GENERATED / "Klean63Fibfib/Lemmas.lean").read_text()
    raw_target_definitions = re.findall(
        r"(?m)^\s*def\s+targetStatement\b", lemma_text
    )

    report = {
        "independently_classified_domain_rule_ids": independently_domain_ids,
        "source_rule_ids": source_ids,
        "obligation_rule_ids": obligation_ids,
        "source_obligation_ordered_bijection": (
            independently_domain_ids == source_ids == obligation_ids
            and len(obligation_ids) == len(set(obligation_ids))
        ),
        "input_manifest_source_rules_exact": (
            input_manifest["source_rules"] == obligation_map["source_rules"]
        ),
        "source_rule_matches_inventory": (
            obligation_map["source_rules"][0]["source_rule_id"]
            == inventory["rules"][2]["source_rule_id"]
            and obligation_map["source_rules"][0]["text"]
            == inventory["rules"][2]["text"]
            and obligation_map["source_rules"][0]["normalized_sha256"]
            == inventory["rules"][2]["normalized_sha256"]
            and obligation_map["source_rules"][0]["start_line"]
            == inventory["rules"][2]["start_line"]
            and obligation_map["source_rules"][0]["end_line"]
            == inventory["rules"][2]["end_line"]
        ),
        "conjuncts": conjuncts,
        "expected_exact_conjunct": EXPECTED_CONJUNCT,
        "exact_operational_translation": conjuncts == [EXPECTED_CONJUNCT],
        "conjunct_sha256_recomputed": [
            klean_export.sha256_text(item) for item in conjuncts
        ],
        "conjunct_sha256_recorded": [
            item["lean_conjunct_sha256"]
            for item in obligation_map["obligations"]
        ],
        "conjunct_hashes_match": all(
            klean_export.sha256_text(item["lean_conjunct"])
            == item["lean_conjunct_sha256"]
            for item in obligation_map["obligations"]
        ),
        "nonvacuity_shape_checks": {
            "contains_no_true_or_false_conjunct": not any(
                token in EXPECTED_CONJUNCT for token in ("True", "False")
            ),
            "both_source_variables_occur_on_both_sides": all(
                EXPECTED_CONJUNCT.split("=", 1)[side].count(variable) > 0
                for side in (0, 1)
                for variable in ("I", "N")
            ),
            "lhs_and_rhs_are_syntactically_distinct": (
                EXPECTED_CONJUNCT.split("=", 1)[0].strip()
                != EXPECTED_CONJUNCT.split("=", 1)[1].strip()
            ),
        },
        "trust_parameters": parameters,
        "expected_kore_bindings": [
            {
                "kore_symbol": "Lbl'Unds'-Int'Unds'",
                "name": "«_-Int_»",
                "type": "SortInt → SortInt → SortInt",
                "source_rule_ids": [DOMAIN_RULE_ID],
            },
            {
                "kore_symbol": "Lbl'UndsPlus'Int'Unds'",
                "name": "«_+Int_»",
                "type": "SortInt → SortInt → SortInt",
                "source_rule_ids": [DOMAIN_RULE_ID],
            },
        ],
        "parameter_bindings_exact": [
            {
                key: parameter[key]
                for key in ("kore_symbol", "name", "type", "source_rule_ids")
            }
            for parameter in parameters
        ]
        == [
            {
                "kore_symbol": "Lbl'Unds'-Int'Unds'",
                "name": "«_-Int_»",
                "type": "SortInt → SortInt → SortInt",
                "source_rule_ids": [DOMAIN_RULE_ID],
            },
            {
                "kore_symbol": "Lbl'UndsPlus'Int'Unds'",
                "name": "«_+Int_»",
                "type": "SortInt → SortInt → SortInt",
                "source_rule_ids": [DOMAIN_RULE_ID],
            },
        ],
        "recomputed_parameter_bindings": recomputed_bindings,
        "all_binding_hashes_match": all(
            item["recorded_binding_sha256"] == item["recomputed_binding_sha256"]
            for item in recomputed_bindings
        ),
        "obligation_map_sha256_observed": sha256_bytes(obligation_map_path),
        "obligation_map_sha256_manifest": generator_manifest[
            "obligation_map_sha256"
        ],
        "obligation_map_hash_matches": (
            sha256_bytes(obligation_map_path)
            == generator_manifest["obligation_map_sha256"]
        ),
        "expected_target_definition": expected_definition,
        "expected_target_definition_sha256": klean_export.sha256_text(
            expected_definition
        ),
        "observed_target": observed_target,
        "exactly_one_target_definition": len(raw_target_definitions) == 1,
        "target_exactly_expected_conjunction": (
            observed_target["definition_sha256"]
            == klean_export.sha256_text(expected_definition)
        ),
        "target_matches_generator_manifest": (
            observed_target == generator_manifest["target"]
        ),
        "target_matches_audit_input": observed_target == audit_target,
        "target_matches_recorded_preflight": (
            observed_target
            == audit_input["resolution"]["stage4_preflight"]["target"]
        ),
        "counts": {
            "independent_domain_rules": len(independently_domain_ids),
            "source_rules": len(source_ids),
            "obligations": len(obligation_ids),
            "generator_manifest": generator_manifest["obligation_count"],
            "export_result": export_result["obligation_count"],
            "audit_preflight": audit_input["resolution"]["stage4_preflight"][
                "obligation_count"
            ],
        },
        "fixed_status": {
            "export_result": export_result["status"],
            "fresh_preflight": json.loads(
                Path("/audit-output/evidence/04_preflight.json").read_text()
            )["status"],
        },
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
