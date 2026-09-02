#!/usr/bin/env python3
"""Independent Stage 4 manifest, obligation, target, and launcher hash checks."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

from tools import k_rule_inventory, klean_export, pipeline_contract


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


workspace = Path("/reference/k-proof")
discovery_path = Path("/reference/lemma-discovery.json")
generation = Path("/reference/klean-generation")
generated = generation / "generated"
candidate = Path("/candidate")
audit_path = Path("/audit-input.json")

discovery = json.loads(discovery_path.read_text())
audit_input = json.loads(audit_path.read_text())
resolution = audit_input["resolution"]
input_manifest = json.loads((generation / "input-manifest.json").read_text())
generator_manifest = json.loads(
    (generation / "generator-manifest.json").read_text()
)
export_result = json.loads((generation / "export-result.json").read_text())
obligation_map_path = generated / "obligation-map.json"
obligation_map = json.loads(obligation_map_path.read_text())

inventory = k_rule_inventory.inventory_verification(workspace)
canonical_by_id = {
    rule["source_rule_id"]: rule for rule in inventory["rules"]
}
manifest_by_id = {
    rule["source_rule_id"]: rule for rule in discovery["rules"]
}
independent_domain_ids = [
    "rule-0312858a8718cb93d212cdb7b679a2875534dc14191dff8edf7bccf9a96d8b43",
    "rule-5a57a342f46c274d8d94d5f1c7eda4683981fbe24087e787e4a8ce7782c03167",
]
independent_definition_ids = [
    rule["source_rule_id"]
    for rule in inventory["rules"]
    if rule["source_rule_id"] not in set(independent_domain_ids)
]
discovery_sha256 = sha256_file(discovery_path)

expected_source_rules = []
for source_rule_id in independent_domain_ids:
    expected_source_rules.append(
        {
            **canonical_by_id[source_rule_id],
            **{
                "classification": "DOMAIN_LEMMA",
                "rationale": manifest_by_id[source_rule_id]["rationale"],
            },
            "discovery_manifest_sha256": discovery_sha256,
            "inventory_sha256": inventory["inventory_sha256"],
        }
    )

obligations = obligation_map["obligations"]
observed_obligation_ids = [
    obligation["source_rule_id"] for obligation in obligations
]
expected_conjuncts = {
    independent_domain_ids[0]: (
        "∀ (V : SortVal), ((«project:Int?» (SortK.kseq "
        "((@inj SortVal SortKItem) V) SortK.dotk)).isSome = true) ↔ "
        "(((«definedProjectInt(_)_VERIFICATION_Bool_Val» V : SortBool) "
        "= (true : SortBool)) ∧ (True))"
    ),
    independent_domain_ids[1]: (
        "∀ (I : SortInt) (V : SortVal) "
        "(h : («definedProjectInt(_)_VERIFICATION_Bool_Val» V) = true), "
        "(«applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val» \"+\" V "
        "(SortVal.inj_SortInt I) : SortVal) = "
        "(SortVal.inj_SortInt («_+Int_» (projectIntTotal V) I) : SortVal)"
    ),
}

obligation_checks = {
    "source_rules_exactly_independent_domain_set": (
        obligation_map["source_rules"] == expected_source_rules
        == input_manifest["source_rules"]
    ),
    "ordered_source_rule_obligation_bijection": (
        observed_obligation_ids == independent_domain_ids
    ),
    "obligation_ids_unique": (
        len(observed_obligation_ids) == len(set(observed_obligation_ids))
    ),
    "obligation_count_exactly_two": len(obligations) == 2,
    "every_obligation_span_and_hash_match_frozen_source": all(
        obligation["source_span"]
        == {
            "start_line": canonical_by_id[obligation["source_rule_id"]][
                "start_line"
            ],
            "end_line": canonical_by_id[obligation["source_rule_id"]][
                "end_line"
            ],
        }
        and obligation["normalized_sha256"]
        == canonical_by_id[obligation["source_rule_id"]]["normalized_sha256"]
        and obligation["inventory_sha256"] == inventory["inventory_sha256"]
        and obligation["discovery_manifest_sha256"] == discovery_sha256
        for obligation in obligations
    ),
    "every_conjunct_hash_is_exact": all(
        obligation["lean_conjunct_sha256"]
        == klean_export.sha256_text(obligation["lean_conjunct"])
        for obligation in obligations
    ),
    "conjuncts_match_independent_rule_translation": all(
        obligation["lean_conjunct"]
        == expected_conjuncts[obligation["source_rule_id"]]
        for obligation in obligations
    ),
    "no_empty_or_duplicate_conjunct": (
        all(obligation["lean_conjunct"] for obligation in obligations)
        and len({item["lean_conjunct"] for item in obligations})
        == len(obligations)
    ),
    "first_conjunct_retains_material_cast_definedness_equivalence": (
        "«project:Int?»" in obligations[0]["lean_conjunct"]
        and ".isSome = true" in obligations[0]["lean_conjunct"]
        and "«definedProjectInt(" in obligations[0]["lean_conjunct"]
        and "↔" in obligations[0]["lean_conjunct"]
    ),
    "first_true_atom_is_exact_translation_of_source_ceil_variable": (
        "#Ceil(@V)" in canonical_by_id[independent_domain_ids[0]]["text"]
        and "∧ (True)" in obligations[0]["lean_conjunct"]
    ),
    "second_conjunct_is_universal_guarded_applybin_equality": (
        obligations[1]["lean_conjunct"].startswith(
            "∀ (I : SortInt) (V : SortVal) (h : "
        )
        and "«applyBin(" in obligations[1]["lean_conjunct"]
        and "projectIntTotal V" in obligations[1]["lean_conjunct"]
        and "«_+Int_»" in obligations[1]["lean_conjunct"]
    ),
}

target_observed = klean_export.target_statement(generated)
target_expected_definition = klean_export.expected_target_definition(
    obligation_map
)
lemmas_text = (generated / "Klean68Pluck/Lemmas.lean").read_text()
target_matches = re.findall(
    r"(?ms)^\s*def\s+targetStatement\b.*?(?=^\s*end\s+\S+\s*$)",
    lemmas_text,
)
target_definition = target_matches[0].strip() if len(target_matches) == 1 else None
target_checks = {
    "one_target_definition": len(target_matches) == 1,
    "target_is_exact_conjunction_of_obligations": (
        target_definition == target_expected_definition
    ),
    "target_definition_hash_recomputed": (
        target_observed["definition_sha256"]
        == klean_export.sha256_text(target_definition)
    ),
    "target_statement_hash_recomputed": (
        target_observed["statement_sha256"]
        == klean_export.sha256_text(target_observed["statement"])
    ),
    "target_identical_across_generator_and_audit_input": (
        target_observed
        == generator_manifest["target"]
        == resolution["target"]
        == resolution["stage4_preflight"]["target"]
    ),
    "target_parameter_bindings_recomputed": all(
        parameter["binding_sha256"]
        == klean_export.sha256_text(
            json.dumps(
                {
                    key: parameter[key]
                    for key in (
                        "kore_symbol",
                        "name",
                        "type",
                        "source_rule_ids",
                    )
                },
                sort_keys=True,
                separators=(",", ":"),
            )
        )
        for parameter in target_observed["parameters"]
    ),
}

input_classification_checks = {
    "twenty_definitions": (
        [rule["source_rule_id"] for rule in input_manifest["definitions"]]
        == independent_definition_ids
    ),
    "no_operational_rules": input_manifest["operational_rules"] == [],
    "no_proved_derived_lemmas": (
        input_manifest["proved_derived_lemmas"] == []
    ),
    "two_domain_lemmas": (
        [rule["source_rule_id"] for rule in input_manifest["source_rules"]]
        == independent_domain_ids
    ),
}

recorded_hashes = resolution["hashes"]
observed_hashes = {
    "k_workspace_sha256": pipeline_contract.sha256_tree(workspace),
    "stage1_export_sha256": klean_export.tree_digest(workspace),
    "discovery_manifest_sha256": discovery_sha256,
    "k_audit_sha256": pipeline_contract.sha256_tree(
        Path("/reference/k-audit")
    ),
    "klean_generation_sha256": pipeline_contract.sha256_tree(generation),
    "generation_producer_sources_sha256": pipeline_contract.sha256_tree(
        Path("/reference/generation-tools")
    ),
    "generated_tree_sha256": klean_export.tree_digest(generated),
    "lean_workspace_sha256": pipeline_contract.sha256_tree(candidate),
}
hash_checks = {
    key: observed == recorded_hashes[key]
    for key, observed in observed_hashes.items()
}
hash_checks.update(
    {
        "obligation_map_sha256": (
            sha256_file(obligation_map_path)
            == generator_manifest["obligation_map_sha256"]
        ),
        "generator_generated_tree_sha256": (
            observed_hashes["generated_tree_sha256"]
            == generator_manifest["generated_tree_sha256"]
        ),
        "export_result_generated_tree_sha256": (
            observed_hashes["generated_tree_sha256"]
            == export_result["generated_tree_sha256"]
        ),
        "export_result_discovery_sha256": (
            discovery_sha256
            == export_result["stage3_discovery_manifest_sha256"]
        ),
        "export_result_trust_inventory_sha256": (
            sha256_file(generation / "trust-inventory.json")
            == export_result["trust_inventory_sha256"]
        ),
    }
)

stage1_source_hashes = {
    path.relative_to(workspace).as_posix(): sha256_file(path)
    for path in pipeline_contract._walk_regular_files(
        workspace, "Stage 1 source workspace"
    )
}
hash_checks["all_stage1_source_file_hashes_exact"] = (
    stage1_source_hashes == resolution["stage1_source_hashes"]
)

all_boolean_groups = (
    obligation_checks,
    target_checks,
    input_classification_checks,
    hash_checks,
)
result = {
    "independent_domain_ids": independent_domain_ids,
    "obligation_checks": obligation_checks,
    "target": target_observed,
    "target_checks": target_checks,
    "input_classification_checks": input_classification_checks,
    "observed_hashes": observed_hashes,
    "recorded_hashes_for_mounted_inputs": {
        key: recorded_hashes[key] for key in observed_hashes
    },
    "hash_checks": hash_checks,
    "unmounted_recorded_hash_not_recomputable": {
        "lean_invocation_sha256": recorded_hashes["lean_invocation_sha256"],
        "reason": (
            "The launcher did not mount the Stage 5 invocation directory; "
            "only its candidate workspace is mounted at /candidate."
        ),
    },
    "all_checks_pass": all(
        value for group in all_boolean_groups for value in group.values()
    ),
}
print(json.dumps(result, indent=2, sort_keys=True))
