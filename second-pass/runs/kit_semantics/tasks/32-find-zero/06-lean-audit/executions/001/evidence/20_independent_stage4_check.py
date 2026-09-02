#!/usr/bin/env python3
"""Independent Stage 4 bijection, target, and obligation-faithfulness audit."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

from tools.k_rule_inventory import inventory_verification


STAGE1 = Path("/reference/k-proof")
DISCOVERY = Path("/reference/lemma-discovery.json")
GENERATION = Path("/reference/klean-generation")
GENERATED = GENERATION / "generated"
AUDIT_INPUT = Path("/audit-input.json")
FRESH_PREFLIGHT = Path("/audit-output/evidence/17_preflight_rerun_result.json")

DOMAIN_IDS = [
    "rule-0dfb3ea463a2e10ce61e8445bcf95e2aa2d4748b432b47ccd1f9825f8cca2630",
    "rule-f684bfbef1c0219f754e562f1888c8a1b7236498affdcf8c5681f52ef8e6175f",
    "rule-4f3a4fc13d02a156f3a8d695f13fdac54badb56cceabf4cbe100c7ea4aca4d57",
    "rule-f2662dddafe1054c19c3ddaf31b8c9e9a8971c2baafdf6d7f8bfb1785b1ff321",
]

PARAMETER_NAME = "«numVals(_)_VERIFICATION-SYNTAX_ValSeq_NumSeq»"
PARAMETER_TYPE = "SortNumSeq → SortValSeq"
KORE_SYMBOL = (
    "LblnumVals'LParUndsRParUnds'VERIFICATION-SYNTAX"
    "'Unds'ValSeq'Unds'NumSeq"
)

# Written independently from the four frozen K rules. These are exact
# total-function formulations of the K simplifications; ↔ is required because
# a simplification must preserve truth in both rewrite directions.
EXPECTED_CONJUNCTS = [
    (
        f"∀ (NS : SortNumSeq), (({PARAMETER_NAME} NS : SortValSeq) = "
        "(SortValSeq.«.ValSeq_MPY-CORE_ValSeq» : SortValSeq)) ↔ "
        "((NS : SortNumSeq) = "
        "(SortNumSeq.«.NumSeq_VERIFICATION-SYNTAX_NumSeq» : SortNumSeq))"
    ),
    (
        f"∀ (NS2 : SortNumSeq) (NS1 : SortNumSeq), "
        f"(({PARAMETER_NAME} NS1 : SortValSeq) = "
        f"({PARAMETER_NAME} NS2 : SortValSeq)) ↔ "
        "((NS1 : SortNumSeq) = (NS2 : SortNumSeq))"
    ),
    (
        f"∀ (R : SortNumSeq) (I : SortInt) (NS : SortNumSeq), "
        f"(({PARAMETER_NAME} NS : SortValSeq) = "
        "(SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» "
        f"(SortVal.inj_SortInt I) ({PARAMETER_NAME} R) : SortValSeq)) ↔ "
        "((NS : SortNumSeq) = "
        "(SortNumSeq.«nInt(_,_)_VERIFICATION-SYNTAX_NumSeq_Int_NumSeq» "
        "I R : SortNumSeq))"
    ),
    (
        f"∀ (R : SortNumSeq) (F : SortFloat) (NS : SortNumSeq), "
        f"(({PARAMETER_NAME} NS : SortValSeq) = "
        "(SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» "
        f"(SortVal.inj_SortFloat F) ({PARAMETER_NAME} R) : SortValSeq)) ↔ "
        "((NS : SortNumSeq) = "
        "(SortNumSeq.«nFloat(_,_)_VERIFICATION-SYNTAX_NumSeq_Float_NumSeq» "
        "F R : SortNumSeq))"
    ),
]


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def target_definition_from_file(path: Path) -> str:
    text = path.read_text()
    matches = list(
        re.finditer(
            r"(?ms)^\s*def\s+targetStatement\b.*?(?=^\s*end\s+\S+\s*$)",
            text,
        )
    )
    if len(matches) != 1:
        raise RuntimeError(f"expected one target definition, found {len(matches)}")
    return matches[0].group(0).strip()


def expected_target_definition() -> str:
    return "\n".join(
        [
            "def targetStatement",
            f"    ({PARAMETER_NAME} : {PARAMETER_TYPE})",
            "    : Prop :=",
            "    "
            + "\n    ∧ ".join(f"({conjunct})" for conjunct in EXPECTED_CONJUNCTS),
        ]
    )


def main() -> None:
    inventory = inventory_verification(STAGE1)
    discovery = json.loads(DISCOVERY.read_text())
    input_manifest = json.loads((GENERATION / "input-manifest.json").read_text())
    generator = json.loads((GENERATION / "generator-manifest.json").read_text())
    obligation_map = json.loads((GENERATED / "obligation-map.json").read_text())
    audit_input = json.loads(AUDIT_INPUT.read_text())
    recorded_preflight = json.loads((GENERATION / "preflight.json").read_text())
    fresh_preflight = json.loads(FRESH_PREFLIGHT.read_text())

    discovery_by_id = {
        entry["source_rule_id"]: entry for entry in discovery["rules"]
    }
    inventory_by_id = {
        entry["source_rule_id"]: entry for entry in inventory["rules"]
    }
    expected_source_rules = []
    expected_definitions = []
    discovery_hash = sha256_text(DISCOVERY.read_text())
    for source_rule in inventory["rules"]:
        source_rule_id = source_rule["source_rule_id"]
        classified = discovery_by_id[source_rule_id]
        combined = {
            **source_rule,
            "classification": classified["classification"],
            "rationale": classified["rationale"],
        }
        if classified["classification"] == "DOMAIN_LEMMA":
            expected_source_rules.append(
                {
                    **combined,
                    "discovery_manifest_sha256": discovery_hash,
                    "inventory_sha256": inventory["inventory_sha256"],
                }
            )
        elif classified["classification"] == "DEFINITION":
            expected_definitions.append(combined)

    obligations = obligation_map["obligations"]
    obligation_ids = [entry["source_rule_id"] for entry in obligations]
    obligation_conjuncts = [entry["lean_conjunct"] for entry in obligations]
    source_rule_ids = [
        entry["source_rule_id"] for entry in obligation_map["source_rules"]
    ]

    binding = {
        "kore_symbol": KORE_SYMBOL,
        "name": PARAMETER_NAME,
        "type": PARAMETER_TYPE,
        "source_rule_ids": DOMAIN_IDS,
    }
    expected_binding = {
        **binding,
        "binding_sha256": sha256_text(
            json.dumps(binding, sort_keys=True, separators=(",", ":"))
        ),
    }

    actual_definition = target_definition_from_file(
        GENERATED / "Klean32FindZero/Lemmas.lean"
    )
    expected_definition = expected_target_definition()
    target = generator["target"]
    expected_statement = (
        "Klean32FindZero.Lemmas.targetStatement " + PARAMETER_NAME
    )

    all_lean_text = "\n".join(
        path.read_text() for path in sorted(GENERATED.rglob("*.lean"))
    )
    checks: dict[str, object] = {
        "independent_domain_rule_count": len(DOMAIN_IDS),
        "stage4_status_is_pass_not_no_obligations": (
            audit_input["resolution"]["selections"]["klean_generation"]["status"]
            == "PASS"
        ),
        "input_manifest_source_rules_exact": (
            input_manifest["source_rules"] == expected_source_rules
        ),
        "input_manifest_definitions_exact": (
            input_manifest["definitions"] == expected_definitions
        ),
        "input_manifest_no_operational_rules": (
            input_manifest["operational_rules"] == []
        ),
        "input_manifest_no_proved_derived_lemmas": (
            input_manifest["proved_derived_lemmas"] == []
        ),
        "obligation_source_rules_exact": (
            obligation_map["source_rules"] == expected_source_rules
        ),
        "source_rule_id_order_bijection": source_rule_ids == DOMAIN_IDS,
        "obligation_id_order_bijection": obligation_ids == DOMAIN_IDS,
        "source_rule_ids_unique": len(source_rule_ids) == len(set(source_rule_ids)),
        "obligation_ids_unique": len(obligation_ids) == len(set(obligation_ids)),
        "exact_independent_conjuncts": obligation_conjuncts == EXPECTED_CONJUNCTS,
        "conjunct_hashes_all_match": all(
            entry["lean_conjunct_sha256"] == sha256_text(entry["lean_conjunct"])
            for entry in obligations
        ),
        "obligation_provenance_all_match": all(
            entry["inventory_sha256"] == inventory["inventory_sha256"]
            and entry["discovery_manifest_sha256"] == discovery_hash
            and entry["normalized_sha256"]
            == inventory_by_id[entry["source_rule_id"]]["normalized_sha256"]
            and entry["source_span"]
            == {
                "start_line": inventory_by_id[entry["source_rule_id"]][
                    "start_line"
                ],
                "end_line": inventory_by_id[entry["source_rule_id"]]["end_line"],
            }
            for entry in obligations
        ),
        "trust_parameter_exact": (
            obligation_map["trust_parameters"] == [expected_binding]
        ),
        "target_definition_exact": actual_definition == expected_definition,
        "target_definition_sha256": sha256_text(actual_definition),
        "target_definition_hash_matches_manifest": (
            sha256_text(actual_definition) == target["definition_sha256"]
        ),
        "target_statement_exact": target["statement"] == expected_statement,
        "target_statement_hash_matches_manifest": (
            sha256_text(expected_statement) == target["statement_sha256"]
        ),
        "target_parameter_exact": target["parameters"] == [expected_binding],
        "target_identity_matches_audit_input": (
            target == audit_input["resolution"]["target"]
        ),
        "target_identity_matches_recorded_preflight": (
            target == recorded_preflight["target"]
        ),
        "target_identity_matches_fresh_preflight": (
            target == fresh_preflight["target"]
        ),
        "exactly_one_generated_target": len(
            re.findall(r"(?m)^\s*def\s+targetStatement\b", all_lean_text)
        )
        == 1,
        "no_literal_true_false_or_empty_conjunct": all(
            conjunct.strip()
            and conjunct.strip() not in {"True", "False"}
            and "∀" in conjunct
            and "↔" in conjunct
            for conjunct in obligation_conjuncts
        ),
        "all_domain_rules_covered_once": (
            len(obligations) == len(expected_source_rules) == len(DOMAIN_IDS) == 4
        ),
    }

    errors = [
        name
        for name, result in checks.items()
        if isinstance(result, bool) and not result
    ]
    print(
        json.dumps(
            {
                "status": "PASS" if not errors else "FAIL",
                "errors": errors,
                "checks": checks,
                "mathematical_judgment": {
                    "rule_1": (
                        "Empty-image inversion: exact universal biconditional "
                        "for source lines 57-59."
                    ),
                    "rule_2": (
                        "Full embedding injectivity: exact universal "
                        "biconditional for source lines 60-62."
                    ),
                    "rule_3": (
                        "Integer-head inversion: exact constructor/injection "
                        "biconditional for source lines 63-66."
                    ),
                    "rule_4": (
                        "Float-head inversion: exact constructor/injection "
                        "biconditional for source lines 67-70."
                    ),
                    "non_vacuity": (
                        "SortNumSeq and SortValSeq are nonempty inductives; "
                        "each conjunct universally constrains image equality "
                        "and its converse. No hypotheses, True literals, "
                        "unused source obligation, or duplicate conjunct exist."
                    ),
                },
            },
            indent=2,
            sort_keys=True,
        )
    )
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
