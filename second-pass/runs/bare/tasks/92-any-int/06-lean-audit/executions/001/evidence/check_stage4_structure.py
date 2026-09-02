#!/usr/bin/env python3
import json
from pathlib import Path

from tools.klean_export import expected_target_definition, target_statement


generation = Path("/reference/klean-generation")
generated = generation / "generated"
audit = json.loads(Path("/audit-input.json").read_text())
discovery = json.loads(
    Path("/reference/lemma-discovery.json").read_text()
)
input_manifest = json.loads(
    (generation / "input-manifest.json").read_text()
)
generator = json.loads(
    (generation / "generator-manifest.json").read_text()
)
export_result = json.loads(
    (generation / "export-result.json").read_text()
)
obligation_map = json.loads(
    (generated / "obligation-map.json").read_text()
)

# Independent semantic classification, justified in REVIEW.md from the exact
# frozen rule bodies: both rules are structural macros/definitions.
independent_classification = {
    discovery["rules"][0]["source_rule_id"]: "DEFINITION",
    discovery["rules"][1]["source_rule_id"]: "DEFINITION",
}
independent_domain_ids = [
    source_rule_id
    for source_rule_id, classification in independent_classification.items()
    if classification == "DOMAIN_LEMMA"
]
source_rule_ids = [
    rule["source_rule_id"] for rule in input_manifest["source_rules"]
]
map_source_rule_ids = [
    rule["source_rule_id"] for rule in obligation_map["source_rules"]
]
obligation_ids = [
    obligation["source_rule_id"]
    for obligation in obligation_map["obligations"]
]
observed_target = target_statement(generated)
expected_definition = expected_target_definition(obligation_map)

checks = {
    "independent_domain_set_is_empty": independent_domain_ids == [],
    "input_manifest_domain_set_is_exact": (
        source_rule_ids == independent_domain_ids
    ),
    "obligation_map_source_set_is_exact": (
        map_source_rule_ids == independent_domain_ids
    ),
    "obligation_bijection_is_exact": (
        obligation_ids == independent_domain_ids
        and len(obligation_ids) == len(set(obligation_ids))
    ),
    "no_trust_parameters_without_obligations": (
        obligation_map["trust_parameters"] == []
    ),
    "no_expected_target_definition": expected_definition is None,
    "no_generated_target": observed_target is None,
    "generator_target_is_null": generator["target"] is None,
    "audit_input_target_is_null": audit["resolution"]["target"] is None,
    "all_obligation_counts_zero": (
        generator["obligation_count"] == 0
        and export_result["obligation_count"] == 0
        and audit["resolution"]["stage4_preflight"][
            "obligation_count"
        ]
        == 0
    ),
    "all_stage4_statuses_no_obligations": (
        export_result["status"] == "KLEAN_NO_OBLIGATIONS"
        and audit["resolution"]["stage4_preflight"]["status"]
        == "KLEAN_NO_OBLIGATIONS"
        and audit["resolution"]["selections"]["klean_generation"][
            "status"
        ]
        == "KLEAN_NO_OBLIGATIONS"
    ),
    "classification_only_mode": (
        audit["resolution"]["mode"] == "CLASSIFICATION_ONLY"
    ),
    "no_stage5_result_or_paths": (
        audit["resolution"]["stage5_result"] is None
        and audit["resolution"]["lean_workspace"] is None
        and audit["resolution"]["lean_invocation"] is None
    ),
    "no_candidate_mount": not Path("/candidate").exists(),
}

print(
    json.dumps(
        {
            "independent_classification": independent_classification,
            "independent_domain_ids": independent_domain_ids,
            "input_manifest_source_rule_ids": source_rule_ids,
            "obligation_map_source_rule_ids": map_source_rule_ids,
            "obligation_ids": obligation_ids,
            "expected_target_definition": expected_definition,
            "observed_target": observed_target,
            "checks": checks,
            "all_checks_pass": all(checks.values()),
        },
        indent=2,
        sort_keys=True,
    )
)
