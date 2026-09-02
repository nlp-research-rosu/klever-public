#!/usr/bin/env python3
"""Problem-specific Stage 4 obligation, target, and binding audit."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from tools import klean_export
from tools.k_rule_inventory import inventory_verification


workspace = Path("/reference/k-proof")
generation = Path("/reference/klean-generation")
generated = generation / "generated"
discovery_path = Path("/reference/lemma-discovery.json")
audit_input = json.loads(Path("/audit-input.json").read_text())
discovery = json.loads(discovery_path.read_text())
inventory = inventory_verification(workspace)
obligation_map_path = generated / "obligation-map.json"
obligation_map = json.loads(obligation_map_path.read_text())
generator_manifest = json.loads(
    (generation / "generator-manifest.json").read_text()
)

classification_by_id = {
    entry["source_rule_id"]: entry["classification"]
    for entry in discovery["rules"]
}
domain_rules = [
    rule
    for rule in inventory["rules"]
    if classification_by_id[rule["source_rule_id"]] == "DOMAIN_LEMMA"
]
domain_ids = [rule["source_rule_id"] for rule in domain_rules]
mapped_source_ids = [
    rule["source_rule_id"] for rule in obligation_map["source_rules"]
]
obligation_ids = [
    obligation["source_rule_id"]
    for obligation in obligation_map["obligations"]
]

expected_conjunct = (
    "∀ (I : SortInt) (h : («_>=Int_» I 0) = true), "
    "(«_+Int_» («_+Int_» "
    "(«fibfibSpec(_)_VERIFICATION-SYNTAX_Int_Int» I) "
    "(«fibfibSpec(_)_VERIFICATION-SYNTAX_Int_Int» («_+Int_» I 1))) "
    "(«fibfibSpec(_)_VERIFICATION-SYNTAX_Int_Int» («_+Int_» I 2)) "
    ": SortInt) = "
    "(«fibfibSpec(_)_VERIFICATION-SYNTAX_Int_Int» («_+Int_» I 3) "
    ": SortInt)"
)
actual_conjuncts = [
    obligation["lean_conjunct"]
    for obligation in obligation_map["obligations"]
]

source_by_id = {
    rule["source_rule_id"]: rule for rule in inventory["rules"]
}
source_rule_exact = []
for mapped in obligation_map["source_rules"]:
    canonical = source_by_id[mapped["source_rule_id"]]
    source_rule_exact.append(
        {
            "source_rule_id": mapped["source_rule_id"],
            "same_text": mapped["text"] == canonical["text"],
            "same_span": (
                mapped["start_line"] == canonical["start_line"]
                and mapped["end_line"] == canonical["end_line"]
            ),
            "same_normalized_sha256": (
                mapped["normalized_sha256"]
                == canonical["normalized_sha256"]
            ),
            "classification": mapped["classification"],
        }
    )

parameter_hash_results = []
for parameter in obligation_map["trust_parameters"]:
    binding = {
        "kore_symbol": parameter["kore_symbol"],
        "name": parameter["name"],
        "type": parameter["type"],
        "source_rule_ids": parameter["source_rule_ids"],
    }
    recomputed = hashlib.sha256(
        json.dumps(
            binding, sort_keys=True, separators=(",", ":")
        ).encode()
    ).hexdigest()
    parameter_hash_results.append(
        {
            "name": parameter["name"],
            "recorded": parameter["binding_sha256"],
            "recomputed": recomputed,
            "matches": recomputed == parameter["binding_sha256"],
            "source_rule_ids": parameter["source_rule_ids"],
        }
    )

actual_target = klean_export.target_statement(generated)
expected_definition = klean_export.expected_target_definition(
    obligation_map
)
expected_definition_sha256 = hashlib.sha256(
    expected_definition.encode()
).hexdigest()
expected_statement = (
    "Klean63Fibfib.Lemmas.targetStatement "
    "«_>=Int_» «_+Int_» "
    "«fibfibSpec(_)_VERIFICATION-SYNTAX_Int_Int»"
)

checks = {
    "one_genuine_domain_rule": len(domain_rules) == 1,
    "ordered_source_obligation_bijection": (
        domain_ids == mapped_source_ids == obligation_ids
        and len(domain_ids) == len(set(domain_ids))
        and len(obligation_ids) == len(set(obligation_ids))
    ),
    "mapped_source_records_exact": all(
        entry["same_text"]
        and entry["same_span"]
        and entry["same_normalized_sha256"]
        and entry["classification"] == "DOMAIN_LEMMA"
        for entry in source_rule_exact
    ),
    "exact_problem_specific_conjunct": (
        actual_conjuncts == [expected_conjunct]
    ),
    "conjunct_hash_exact": all(
        hashlib.sha256(obligation["lean_conjunct"].encode()).hexdigest()
        == obligation["lean_conjunct_sha256"]
        for obligation in obligation_map["obligations"]
    ),
    "guard_is_preserved": (
        "(h : («_>=Int_» I 0) = true)" in expected_conjunct
    ),
    "no_vacuous_boolean_or_extra_connective": (
        "True" not in expected_conjunct
        and "False" not in expected_conjunct
        and " ∨ " not in expected_conjunct
        and " ∧ " not in expected_conjunct
    ),
    "all_parameter_bindings_hash_exact": all(
        result["matches"] for result in parameter_hash_results
    ),
    "all_parameters_bound_to_only_domain_rule": all(
        result["source_rule_ids"] == domain_ids
        for result in parameter_hash_results
    ),
    "fixed_target_definition_exact": (
        actual_target["definition_sha256"]
        == expected_definition_sha256
        == generator_manifest["target"]["definition_sha256"]
        == audit_input["resolution"]["target"]["definition_sha256"]
    ),
    "fixed_target_statement_exact": (
        actual_target["statement"] == expected_statement
        and actual_target["statement_sha256"]
        == hashlib.sha256(expected_statement.encode()).hexdigest()
        == generator_manifest["target"]["statement_sha256"]
        == audit_input["resolution"]["target"]["statement_sha256"]
    ),
    "fixed_target_manifest_exact": (
        actual_target
        == generator_manifest["target"]
        == audit_input["resolution"]["target"]
    ),
    "obligation_map_hash_exact": (
        hashlib.sha256(obligation_map_path.read_bytes()).hexdigest()
        == generator_manifest["obligation_map_sha256"]
    ),
}
checks["all_checks_pass"] = all(checks.values())
result = {
    "checks": checks,
    "domain_rule_ids": domain_ids,
    "actual_conjuncts": actual_conjuncts,
    "expected_conjunct": expected_conjunct,
    "source_rule_exact": source_rule_exact,
    "parameter_hash_results": parameter_hash_results,
    "actual_target": actual_target,
    "expected_definition_sha256": expected_definition_sha256,
}
print(json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False))
raise SystemExit(0 if checks["all_checks_pass"] else 1)
