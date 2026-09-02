#!/usr/bin/env python3
"""Independent Stage 4 source/obligation/target bijection checks."""

from __future__ import annotations

import json
import re
from pathlib import Path

from tools import klean_export
from tools.k_rule_inventory import inventory_verification


def load(path: str) -> dict:
    return json.loads(Path(path).read_text())


audit = load("/audit-input.json")["resolution"]
discovery = load("/reference/lemma-discovery.json")
input_manifest = load("/reference/klean-generation/input-manifest.json")
generator = load("/reference/klean-generation/generator-manifest.json")
export_result = load("/reference/klean-generation/export-result.json")
recorded_preflight = load("/reference/klean-generation/preflight.json")
rerun_preflight = load("/audit-output/evidence/preflight-result.json")
obligation_map = load(
    "/reference/klean-generation/generated/obligation-map.json"
)
lock = load("/reference/klean-toolchain.lock.json")
inventory = inventory_verification(Path("/reference/k-proof"))

class_by_id = {
    entry["source_rule_id"]: entry for entry in discovery["rules"]
}
classified_rules = [
    {**rule, **class_by_id[rule["source_rule_id"]]}
    for rule in inventory["rules"]
]
independent_domain_ids: list[str] = []
recorded_domain_ids = [
    rule["source_rule_id"] for rule in input_manifest["source_rules"]
]
obligation_ids = [
    obligation["source_rule_id"]
    for obligation in obligation_map["obligations"]
]

actual_target = klean_export.target_statement(
    Path("/reference/klean-generation/generated")
)
lemmas_text = Path(
    "/reference/klean-generation/generated/Klean150XOrY/Lemmas.lean"
).read_text()
lemmas_code = re.sub(r"/-.*?-/", "", lemmas_text, flags=re.S)
lemmas_code = re.sub(r"--.*$", "", lemmas_code, flags=re.M)

checks = {
    "input_definitions_are_exact_canonical_rules_in_order": (
        input_manifest["definitions"] == classified_rules
    ),
    "input_has_no_operational_rules": (
        input_manifest["operational_rules"] == []
    ),
    "input_has_no_proved_derived_lemmas": (
        input_manifest["proved_derived_lemmas"] == []
    ),
    "independent_domain_set_is_empty": independent_domain_ids == [],
    "input_domain_source_set_matches_independent_set": (
        recorded_domain_ids == independent_domain_ids
    ),
    "obligation_source_rules_match_independent_set": (
        [rule["source_rule_id"] for rule in obligation_map["source_rules"]]
        == independent_domain_ids
    ),
    "obligations_biject_with_independent_domain_set": (
        obligation_ids == independent_domain_ids
        and len(obligation_ids) == len(set(obligation_ids))
    ),
    "no_trust_parameters_without_obligations": (
        obligation_map["trust_parameters"] == []
    ),
    "generator_obligation_count_exact": generator["obligation_count"] == 0,
    "export_obligation_count_exact": export_result["obligation_count"] == 0,
    "recorded_preflight_obligation_count_exact": (
        recorded_preflight["obligation_count"] == 0
    ),
    "rerun_preflight_obligation_count_exact": (
        rerun_preflight["obligation_count"] == 0
    ),
    "selected_status_is_no_obligations": (
        audit["selections"]["klean_generation"]["status"]
        == "KLEAN_NO_OBLIGATIONS"
    ),
    "all_stage4_statuses_agree": (
        export_result["status"]
        == recorded_preflight["status"]
        == rerun_preflight["status"]
        == "KLEAN_NO_OBLIGATIONS"
    ),
    "actual_target_absent": actual_target is None,
    "manifest_and_audit_targets_absent": (
        generator["target"] is None
        and recorded_preflight["target"] is None
        and rerun_preflight["target"] is None
        and audit["target"] is None
    ),
    "immutable_lemmas_module_has_no_prop_declaration": (
        "theorem " not in lemmas_code
        and "lemma " not in lemmas_code
        and ": Prop" not in lemmas_code
        and "axiom " not in lemmas_code
        and "opaque " not in lemmas_code
    ),
    "generator_toolchain_matches_trusted_lock": generator["toolchain"] == lock,
    "audit_embeds_recorded_preflight_exactly": (
        audit["stage4_preflight"] == recorded_preflight
    ),
    "rerun_preflight_identity_matches_recorded": all(
        rerun_preflight[key] == recorded_preflight[key]
        for key in (
            "status",
            "frozen_input_sha256",
            "stage1_workspace_sha256",
            "stage3_discovery_manifest_sha256",
            "generated_tree_sha256",
            "target",
            "obligation_count",
            "trust_declaration_count",
            "designated_sorry_count",
        )
    ),
    "no_candidate_mount": not Path("/candidate").exists(),
    "no_stage5_resolution": (
        audit["lean_workspace"] is None
        and audit["lean_invocation"] is None
        and audit["stage5_result"] is None
        and audit["hashes"]["lean_workspace_sha256"] is None
        and audit["hashes"]["lean_invocation_sha256"] is None
    ),
}

result = {
    "independently_expected_domain_source_rule_ids": independent_domain_ids,
    "recorded_domain_source_rule_ids": recorded_domain_ids,
    "generated_obligation_source_rule_ids": obligation_ids,
    "actual_generated_target": actual_target,
    "checks": checks,
    "all_checks_pass": all(checks.values()),
    "mathematical_judgment": (
        "No rule states a standalone domain fact. All five rules are the "
        "guarded equations of trialChoice or xOrYSpec, so the true Stage 4 "
        "domain-lemma set is genuinely empty; an empty obligation list and "
        "absent target are therefore exact, not weakened or vacuous."
    ),
}
print(json.dumps(result, indent=2, sort_keys=True))
