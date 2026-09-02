#!/usr/bin/env python3
"""Independent Stage 4 source-rule/obligation and target-identity checks."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

from tools.k_rule_inventory import inventory_verification
from tools.klean_export import expected_target_definition, target_statement


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


workspace = Path("/reference/k-proof")
generation = Path("/reference/klean-generation")
generated = generation / "generated"
discovery = json.loads(Path("/reference/lemma-discovery.json").read_text())
obligation_map = json.loads((generated / "obligation-map.json").read_text())
generator_manifest = json.loads(
    (generation / "generator-manifest.json").read_text()
)
audit_input = json.loads(Path("/audit-input.json").read_text())
inventory = inventory_verification(workspace)

domain_ids = [
    entry["source_rule_id"]
    for entry in discovery["rules"]
    if entry["classification"] == "DOMAIN_LEMMA"
]
source_rule_ids = [
    entry["source_rule_id"] for entry in obligation_map["source_rules"]
]
obligation_ids = [
    entry["source_rule_id"] for entry in obligation_map["obligations"]
]

inventory_by_id = {
    entry["source_rule_id"]: entry for entry in inventory["rules"]
}
obligation_source_records_match = True
conjunct_hashes_match = True
for obligation in obligation_map["obligations"]:
    source = inventory_by_id[obligation["source_rule_id"]]
    obligation_source_records_match &= (
        obligation["normalized_sha256"] == source["normalized_sha256"]
        and obligation["source_span"]
        == {
            "start_line": source["start_line"],
            "end_line": source["end_line"],
        }
        and obligation["inventory_sha256"] == inventory["inventory_sha256"]
    )
    conjunct_hashes_match &= (
        sha256_text(obligation["lean_conjunct"])
        == obligation["lean_conjunct_sha256"]
    )

lemmas_path = generated / "Klean43PairsSumToZero/Lemmas.lean"
lemmas_text = lemmas_path.read_text()
match = re.search(
    r"(?ms)^\s*def\s+targetStatement\b.*?"
    r"(?=^\s*end\s+\S+\s*$)",
    lemmas_text,
)
if match is None:
    raise SystemExit("TARGET_IDENTITY: missing targetStatement")
actual_definition = match.group(0).strip()
expected_definition = expected_target_definition(obligation_map)
computed_target = target_statement(generated)
assert computed_target is not None

audit_target = audit_input["resolution"]["target"]
preflight_target = audit_input["resolution"]["stage4_preflight"]["target"]
manifest_target = generator_manifest["target"]

parameter_source_union = sorted(
    {
        source_rule_id
        for parameter in obligation_map["trust_parameters"]
        for source_rule_id in parameter["source_rule_ids"]
    }
)

facts = {
    "independent_domain_rule_ids": domain_ids,
    "obligation_map_source_rule_ids": source_rule_ids,
    "obligation_ids": obligation_ids,
    "domain_ids_unique": len(domain_ids) == len(set(domain_ids)),
    "source_rule_ids_unique": len(source_rule_ids) == len(set(source_rule_ids)),
    "obligation_ids_unique": len(obligation_ids) == len(set(obligation_ids)),
    "ordered_domain_source_bijection": domain_ids == source_rule_ids,
    "ordered_domain_obligation_bijection": domain_ids == obligation_ids,
    "obligation_source_records_match_inventory": (
        obligation_source_records_match
    ),
    "lean_conjunct_hashes_match": conjunct_hashes_match,
    "expected_target_definition_matches_source": (
        expected_definition == actual_definition
    ),
    "computed_target": computed_target,
    "generator_manifest_target_matches": manifest_target == computed_target,
    "audit_input_target_matches": audit_target == computed_target,
    "audit_preflight_target_matches": preflight_target == computed_target,
    "parameter_source_rule_union": parameter_source_union,
    "parameters_bound_only_to_domain_rules": (
        parameter_source_union == sorted(domain_ids)
    ),
    "target_conjunct_count": actual_definition.count("\n    ∧ "),
    "obligation_count": len(obligation_ids),
}

print(json.dumps(facts, indent=2, sort_keys=True))
checks = (
    facts["domain_ids_unique"],
    facts["source_rule_ids_unique"],
    facts["obligation_ids_unique"],
    facts["ordered_domain_source_bijection"],
    facts["ordered_domain_obligation_bijection"],
    facts["obligation_source_records_match_inventory"],
    facts["lean_conjunct_hashes_match"],
    facts["expected_target_definition_matches_source"],
    facts["generator_manifest_target_matches"],
    facts["audit_input_target_matches"],
    facts["audit_preflight_target_matches"],
    facts["parameters_bound_only_to_domain_rules"],
    facts["target_conjunct_count"] == facts["obligation_count"] - 1,
)
if not all(checks):
    raise SystemExit("STAGE4_BIJECTION_AND_TARGET: FAIL")
print("STAGE4_BIJECTION_AND_TARGET: PASS")
