#!/usr/bin/env python3
import hashlib
import json
import re
from pathlib import Path

workspace = Path("/reference/k-proof")
generation = Path("/reference/klean-generation")
generated = generation / "generated"
discovery = json.loads(Path("/reference/lemma-discovery.json").read_text())
input_manifest = json.loads((generation / "input-manifest.json").read_text())
generator_manifest = json.loads((generation / "generator-manifest.json").read_text())
export_result = json.loads((generation / "export-result.json").read_text())
obligation_map = json.loads((generated / "obligation-map.json").read_text())

independent_classification = [
    {
        "source_rule_id": (
            "rule-08e473cc777c3fe3dfbffc47a89f7ed00a323ab5af8be120c20538dd19dbc3e1"
        ),
        "classification": "DEFINITION",
        "source_span": {"start_line": 9, "end_line": 10},
        "semantic_judgment": (
            "The rule is the sole defining equation of the fresh total function "
            "expectedSumProduct : Ints -> PyVal. It expands that named proof term "
            "to the tuple of the existing sumInts/productInts recurrences. It "
            "does not match a configuration cell or a source-program execution "
            "term, and it is used directly as the spec's result postcondition."
        ),
        "not_domain_lemma": (
            "It introduces/defines a named summary rather than asserting an "
            "independent mathematical theorem needed to discharge the program."
        ),
        "attributes": [],
    }
]
independent_domain_ids = [
    item["source_rule_id"]
    for item in independent_classification
    if item["classification"] == "DOMAIN_LEMMA"
]
manifest_classifications = [
    {
        "source_rule_id": entry["source_rule_id"],
        "classification": entry["classification"],
    }
    for entry in discovery["rules"]
]
expected_classifications = [
    {
        "source_rule_id": entry["source_rule_id"],
        "classification": entry["classification"],
    }
    for entry in independent_classification
]

target_declarations = []
for path in sorted(generated.rglob("*.lean")):
    for match in re.finditer(r"(?m)^\s*def\s+targetStatement\b", path.read_text()):
        target_declarations.append(
            {
                "file": path.relative_to(generated).as_posix(),
                "offset": match.start(),
            }
        )

all_obligation_ids = [
    item.get("source_rule_id") for item in obligation_map["obligations"]
]
lean_conjuncts = [
    item.get("lean_conjunct") for item in obligation_map["obligations"]
]
checks = {
    "stage3_matches_independent_classification": (
        manifest_classifications == expected_classifications
    ),
    "every_simplification_is_definition_or_domain": all(
        entry["classification"] in {"DEFINITION", "DOMAIN_LEMMA"}
        for entry in independent_classification
        if "simplification" in entry["attributes"]
    ),
    "genuine_domain_set_empty": independent_domain_ids == [],
    "input_source_rule_set_exact": input_manifest["source_rules"] == [],
    "obligation_source_rule_set_exact": obligation_map["source_rules"] == [],
    "obligation_id_order_and_bijection": all_obligation_ids
    == independent_domain_ids
    and len(all_obligation_ids) == len(set(all_obligation_ids)),
    "no_omitted_or_extra_obligations": obligation_map["obligations"] == [],
    "no_trust_parameters_without_obligations": obligation_map["trust_parameters"]
    == [],
    "no_vacuous_or_weakened_conjuncts": lean_conjuncts == [],
    "generator_obligation_count_exact": generator_manifest["obligation_count"] == 0,
    "export_obligation_count_exact": export_result["obligation_count"] == 0,
    "export_status_exact": export_result["status"] == "KLEAN_NO_OBLIGATIONS",
    "generator_target_null": generator_manifest["target"] is None,
    "no_generated_target_declaration": target_declarations == [],
    "lemmas_module_contains_no_proposition_declaration": re.search(
        r"(?m)^\s*(?:def|theorem|lemma|axiom|opaque)\s+",
        (generated / "Klean8SumProduct/Lemmas.lean").read_text(),
    )
    is None,
    "obligation_map_hash_exact": generator_manifest["obligation_map_sha256"]
    == hashlib.sha256((generated / "obligation-map.json").read_bytes()).hexdigest(),
}

print(
    json.dumps(
        {
            "independent_classification": independent_classification,
            "independent_domain_ids": independent_domain_ids,
            "manifest_classifications": manifest_classifications,
            "input_manifest_source_rules": input_manifest["source_rules"],
            "obligation_map": obligation_map,
            "target_declarations": target_declarations,
            "checks": checks,
        },
        indent=2,
        sort_keys=True,
    )
)
