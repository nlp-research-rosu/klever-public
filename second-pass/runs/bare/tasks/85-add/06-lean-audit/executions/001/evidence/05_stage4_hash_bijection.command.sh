#!/usr/bin/env bash
set -euxo pipefail
sha256sum \
  /reference/klean-generation/input-manifest.json \
  /reference/klean-generation/generator-manifest.json \
  /reference/klean-generation/export-result.json \
  /reference/klean-generation/preflight.json \
  /reference/klean-generation/trust-inventory.json \
  /reference/klean-generation/generated/obligation-map.json \
  /reference/klean-toolchain.lock.json
find /reference/klean-generation/generated -printf '%y %P\n' | sort
sed -n '1,360p' /reference/klean-generation/input-manifest.json
sed -n '1,260p' /reference/klean-generation/generator-manifest.json
sed -n '1,220p' /reference/klean-generation/generated/obligation-map.json
sed -n '1,260p' /reference/klean-generation/export-result.json
sed -n '1,300p' /reference/klean-generation/preflight.json
PYTHONPATH=/reference python3 - <<'PY'
import hashlib
import json
from pathlib import Path
from tools import (
    k_rule_inventory,
    klean_export,
    pipeline_contract,
    stage6_resolution_contract,
)

audit = json.loads(Path("/audit-input.json").read_text())
resolution, signed_digest = stage6_resolution_contract.verify_audit_input(audit)
workspace = Path("/reference/k-proof")
discovery_path = Path("/reference/lemma-discovery.json")
generation = Path("/reference/klean-generation")
generated = generation / "generated"
producer_bundle = Path("/reference/generation-tools")

discovery = json.loads(discovery_path.read_text())
inventory = k_rule_inventory.inventory_verification(workspace)
input_manifest = json.loads((generation / "input-manifest.json").read_text())
generator_manifest = json.loads(
    (generation / "generator-manifest.json").read_text()
)
export_result = json.loads((generation / "export-result.json").read_text())
preflight = json.loads((generation / "preflight.json").read_text())
trust_inventory = json.loads(
    (generation / "trust-inventory.json").read_text()
)
obligation_map_path = generated / "obligation-map.json"
obligation_map = json.loads(obligation_map_path.read_text())
toolchain_lock = json.loads(
    Path("/reference/klean-toolchain.lock.json").read_text()
)

def sha256_file(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

actual_stage1_sources = {
    path.relative_to(workspace).as_posix(): pipeline_contract.sha256_file(path)
    for path in pipeline_contract._walk_regular_files(
        workspace, "mounted Stage 1 workspace"
    )
}

actual_hashes = {
    "k_workspace_sha256": pipeline_contract.sha256_tree(workspace),
    "stage1_export_sha256": klean_export.tree_digest(workspace),
    "discovery_manifest_sha256": sha256_file(discovery_path),
    "k_audit_sha256": pipeline_contract.sha256_tree(
        Path("/reference/k-audit")
    ),
    "klean_generation_sha256": pipeline_contract.sha256_tree(generation),
    "generation_producer_sources_sha256": pipeline_contract.sha256_tree(
        producer_bundle
    ),
    "generated_tree_sha256": klean_export.tree_digest(generated),
    "lean_workspace_sha256": None,
    "lean_invocation_sha256": None,
}

classification_by_id = {
    entry["source_rule_id"]: entry
    for entry in discovery["rules"]
}
joined = []
for rule in inventory["rules"]:
    classified = classification_by_id[rule["source_rule_id"]]
    joined.append(
        rule
        | {
            "classification": classified["classification"],
            "rationale": classified["rationale"],
        }
    )
expected_definitions = [
    entry for entry in joined
    if entry["classification"] == "DEFINITION"
]
expected_domain = [
    entry for entry in joined
    if entry["classification"] == "DOMAIN_LEMMA"
]
expected_operational = [
    entry for entry in joined
    if entry["classification"] == "OPERATIONAL_RULE"
]
expected_derived = [
    entry for entry in joined
    if entry["classification"] == "PROVED_DERIVED_LEMMA"
]

target_observed = klean_export.target_statement(generated)
target_expected_definition = klean_export.expected_target_definition(
    obligation_map
)
obligations = obligation_map["obligations"]
source_rules = obligation_map["source_rules"]
obligation_ids = [
    entry["source_rule_id"] for entry in obligations
]
source_rule_ids = [
    entry["source_rule_id"] for entry in source_rules
]

hash_bindings = {
    "audit_resolution_hashes_equal_actual": (
        resolution["hashes"] == actual_hashes
    ),
    "stage1_source_hashes_equal_actual": (
        resolution["stage1_source_hashes"] == actual_stage1_sources
    ),
    "input_frozen_hash": (
        input_manifest["frozen_input_sha256"]
        == actual_hashes["stage1_export_sha256"]
    ),
    "input_stage1_hash": (
        input_manifest["stage1_workspace_sha256"]
        == actual_hashes["stage1_export_sha256"]
    ),
    "input_discovery_hash": (
        input_manifest["stage3_discovery_manifest_sha256"]
        == actual_hashes["discovery_manifest_sha256"]
    ),
    "input_verification_hash": (
        input_manifest["verification_sha256"]
        == sha256_file(workspace / "verification.k")
    ),
    "input_inventory_hash": (
        input_manifest["inventory_sha256"]
        == inventory["inventory_sha256"]
        == discovery["inventory_sha256"]
    ),
    "generator_generated_tree_hash": (
        generator_manifest["generated_tree_sha256"]
        == actual_hashes["generated_tree_sha256"]
    ),
    "generator_stage1_provenance": (
        generator_manifest["provenance"]["stage1_workspace_sha256"]
        == actual_hashes["stage1_export_sha256"]
    ),
    "generator_discovery_provenance": (
        generator_manifest["provenance"][
            "stage3_discovery_manifest_sha256"
        ]
        == actual_hashes["discovery_manifest_sha256"]
    ),
    "generator_inventory_provenance": (
        generator_manifest["provenance"]["inventory_sha256"]
        == inventory["inventory_sha256"]
    ),
    "generator_toolchain_lock": (
        generator_manifest["toolchain"] == toolchain_lock
    ),
    "generator_obligation_map_hash": (
        generator_manifest["obligation_map_sha256"]
        == sha256_file(obligation_map_path)
    ),
    "export_frozen_hash": (
        export_result["frozen_input_sha256"]
        == actual_hashes["stage1_export_sha256"]
    ),
    "export_discovery_hash": (
        export_result["stage3_discovery_manifest_sha256"]
        == actual_hashes["discovery_manifest_sha256"]
    ),
    "export_generated_hash": (
        export_result["generated_tree_sha256"]
        == actual_hashes["generated_tree_sha256"]
    ),
    "export_trust_hash": (
        export_result["trust_inventory_sha256"]
        == sha256_file(generation / "trust-inventory.json")
    ),
    "preflight_frozen_hash": (
        preflight["frozen_input_sha256"]
        == actual_hashes["stage1_export_sha256"]
    ),
    "preflight_discovery_hash": (
        preflight["stage3_discovery_manifest_sha256"]
        == actual_hashes["discovery_manifest_sha256"]
    ),
    "preflight_generated_hash": (
        preflight["generated_tree_sha256"]
        == actual_hashes["generated_tree_sha256"]
    ),
}

classification_bindings = {
    "input_definitions_exact": (
        input_manifest["definitions"] == expected_definitions
    ),
    "input_domain_source_rules_exact": (
        input_manifest["source_rules"] == expected_domain
    ),
    "input_operational_rules_exact": (
        input_manifest["operational_rules"] == expected_operational
    ),
    "input_derived_lemmas_exact": (
        input_manifest["proved_derived_lemmas"] == expected_derived
    ),
    "independent_domain_count": len(expected_domain),
}

bijection = {
    "input_source_rules_equal_obligation_map_source_rules": (
        input_manifest["source_rules"] == source_rules
    ),
    "source_rule_ids": source_rule_ids,
    "obligation_source_rule_ids": obligation_ids,
    "ordered_ids_equal": source_rule_ids == obligation_ids,
    "source_ids_unique": len(source_rule_ids) == len(set(source_rule_ids)),
    "obligation_ids_unique": (
        len(obligation_ids) == len(set(obligation_ids))
    ),
    "source_rule_count": len(source_rules),
    "obligation_count": len(obligations),
    "generator_obligation_count": generator_manifest["obligation_count"],
    "export_obligation_count": export_result["obligation_count"],
    "preflight_obligation_count": preflight["obligation_count"],
    "trust_parameters": obligation_map["trust_parameters"],
}
bijection["exact_bijection"] = (
    source_rule_ids == obligation_ids
    and bijection["source_ids_unique"]
    and bijection["obligation_ids_unique"]
    and len(source_rules)
    == len(obligations)
    == generator_manifest["obligation_count"]
    == export_result["obligation_count"]
    == preflight["obligation_count"]
)

target_identity = {
    "expected_target_definition": target_expected_definition,
    "observed_generated_target": target_observed,
    "generator_manifest_target": generator_manifest["target"],
    "preflight_target": preflight["target"],
    "audit_input_target": resolution["target"],
    "all_targets_absent": (
        target_expected_definition is None
        and target_observed is None
        and generator_manifest["target"] is None
        and preflight["target"] is None
        and resolution["target"] is None
    ),
}

mode_status = {
    "audit_mode_env": __import__("os").environ.get("AUDIT_MODE"),
    "audit_mode_signed": resolution["mode"],
    "export_status": export_result["status"],
    "preflight_status": preflight["status"],
    "selection_status": resolution["selections"][
        "klean_generation"
    ]["status"],
    "candidate_exists": Path("/candidate").exists(),
    "stage5_result": resolution["stage5_result"],
    "lean_workspace": resolution["lean_workspace"],
    "lean_invocation": resolution["lean_invocation"],
}
mode_status["classification_only_consistent"] = (
    mode_status["audit_mode_env"]
    == mode_status["audit_mode_signed"]
    == "CLASSIFICATION_ONLY"
    and mode_status["export_status"]
    == "KLEAN_NO_OBLIGATIONS"
    and mode_status["preflight_status"]
    == "KLEAN_NO_OBLIGATIONS"
    and mode_status["selection_status"]
    == "KLEAN_NO_OBLIGATIONS"
    and not mode_status["candidate_exists"]
    and mode_status["stage5_result"] is None
    and mode_status["lean_workspace"] is None
    and mode_status["lean_invocation"] is None
)

result = {
    "signed_audit_digest": signed_digest,
    "actual_hashes": actual_hashes,
    "hash_bindings": hash_bindings,
    "all_hash_bindings_pass": all(hash_bindings.values()),
    "classification_bindings": classification_bindings,
    "all_classification_bindings_pass": all(
        value is True
        for key, value in classification_bindings.items()
        if key != "independent_domain_count"
    ),
    "bijection": bijection,
    "target_identity": target_identity,
    "mode_status": mode_status,
    "trust_allowlist_count": len(trust_inventory["allowlist"]),
    "trust_designated_sorries": trust_inventory["designated_sorries"],
    "trust_other_sorries": trust_inventory["other_sorries"],
}
print(json.dumps(result, indent=2, sort_keys=True))
assert result["all_hash_bindings_pass"]
assert result["all_classification_bindings_pass"]
assert resolution["hashes"] == actual_hashes
assert resolution["stage1_source_hashes"] == actual_stage1_sources
assert classification_bindings["independent_domain_count"] == 0
assert bijection["exact_bijection"]
assert target_identity["all_targets_absent"]
assert mode_status["classification_only_consistent"]
assert trust_inventory["designated_sorries"] == 0
assert trust_inventory["other_sorries"] == 0
PY
