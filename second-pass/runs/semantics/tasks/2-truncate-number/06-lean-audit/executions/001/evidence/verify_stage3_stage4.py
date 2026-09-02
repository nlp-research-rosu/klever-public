#!/usr/bin/env python3

import hashlib
import json
from pathlib import Path

from tools import klean_export
from tools import lemma_discovery_contract
from tools import pipeline_contract
from tools import stage6_resolution_contract
from tools.k_rule_inventory import inventory_verification


def load(path: Path) -> dict:
    return json.loads(path.read_text())


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


audit_document = load(Path("/audit-input.json"))
resolution, resolved_digest = stage6_resolution_contract.verify_audit_input(
    audit_document
)
workspace = Path("/reference/k-proof")
discovery_path = Path("/reference/lemma-discovery.json")
generation = Path("/reference/klean-generation")
generated = generation / "generated"
producer = Path("/reference/generation-tools")

discovery = load(discovery_path)
inventory = inventory_verification(workspace)
validated = lemma_discovery_contract.validate_trust_boundary(
    workspace, discovery_path
)
input_manifest = load(generation / "input-manifest.json")
generator_manifest = load(generation / "generator-manifest.json")
export_result = load(generation / "export-result.json")
recorded_preflight = load(generation / "preflight.json")
trust_inventory = load(generation / "trust-inventory.json")
obligation_map_path = generated / "obligation-map.json"
obligation_map = load(obligation_map_path)
source_manifest = load(producer / "source-manifest.json")

actual_pipeline_trees = {
    "k_workspace_sha256": pipeline_contract.sha256_tree(workspace),
    "k_audit_sha256": pipeline_contract.sha256_tree(
        Path("/reference/k-audit")
    ),
    "klean_generation_sha256": pipeline_contract.sha256_tree(generation),
    "generation_producer_sources_sha256": pipeline_contract.sha256_tree(
        producer
    ),
}
actual_stage1_export = klean_export.tree_digest(workspace)
actual_generated_tree = klean_export.tree_digest(generated)
actual_discovery_hash = file_sha256(discovery_path)
actual_verification_hash = file_sha256(workspace / "verification.k")
actual_trust_inventory_hash = file_sha256(
    generation / "trust-inventory.json"
)
actual_obligation_map_hash = file_sha256(obligation_map_path)
actual_stage1_source_hashes = {
    relative: file_sha256(workspace / relative)
    for relative in resolution["stage1_source_hashes"]
}
actual_stage1_files = sorted(
    path.relative_to(workspace).as_posix()
    for path in workspace.rglob("*")
    if path.is_file()
)

observed_producer_files = {
    name: file_sha256(producer / name)
    for name in ("klean_export.py", "klean.py")
}
manifest_producer_files = {
    "klean_export.py": generator_manifest["exporter_sha256"],
    "klean.py": generator_manifest["klean_py_sha256"],
}
producer_image_ids = {
    "source_manifest": source_manifest["generator_image_id"],
    "generator_manifest": generator_manifest["provenance"][
        "generator_image_id"
    ],
    "audit_input_path": "sha256:"
    + Path(resolution["generation_producer_sources"]).name,
}

discovery_ids = [entry["source_rule_id"] for entry in discovery["rules"]]
inventory_ids = [entry["source_rule_id"] for entry in inventory["rules"]]
independent_classifications = {
    "rule-9f2dfdab6d05b03a483926083949b77353f4d59ab6455390118d3ed077036f67":
        "DEFINITION"
}
observed_classifications = {
    entry["source_rule_id"]: entry["classification"]
    for entry in discovery["rules"]
}
accounted = (
    validated["definitions"]
    + validated["operational_rules"]
    + validated["proved_derived_lemmas"]
    + validated["domain_lemmas"]
)
accounted_ids = [entry["source_rule_id"] for entry in accounted]
independent_domain_ids = [
    source_rule_id
    for source_rule_id, classification in independent_classifications.items()
    if classification == "DOMAIN_LEMMA"
]
generated_source_ids = [
    entry["source_rule_id"] for entry in obligation_map["source_rules"]
]
obligation_ids = [
    entry["source_rule_id"] for entry in obligation_map["obligations"]
]
target_from_tree = klean_export.target_statement(generated)
expected_target_definition = klean_export.expected_target_definition(
    obligation_map
)

checks = {
    "audit_input_envelope_digest_valid": (
        resolved_digest == audit_document["resolved_input_sha256"]
    ),
    "audit_mode_classification_only": (
        resolution["mode"] == "CLASSIFICATION_ONLY"
    ),
    "pipeline_tree_hashes_match_audit_input": (
        all(
            actual_pipeline_trees[key] == resolution["hashes"][key]
            for key in actual_pipeline_trees
        )
    ),
    "selection_artifact_hashes_match_mounted_trees": (
        actual_pipeline_trees["k_audit_sha256"]
        == resolution["selections"]["k_audit"]["artifact_sha256"]
        and actual_pipeline_trees["klean_generation_sha256"]
        == resolution["selections"]["klean_generation"]["artifact_sha256"]
    ),
    "all_stage1_source_hashes_and_file_set_match": (
        actual_stage1_source_hashes == resolution["stage1_source_hashes"]
        and actual_stage1_files
        == sorted(resolution["stage1_source_hashes"])
    ),
    "stage1_export_hash_matches_all_layers": (
        actual_stage1_export
        == resolution["hashes"]["stage1_export_sha256"]
        == input_manifest["frozen_input_sha256"]
        == input_manifest["stage1_workspace_sha256"]
        == generator_manifest["provenance"]["stage1_workspace_sha256"]
        == export_result["frozen_input_sha256"]
        == recorded_preflight["stage1_workspace_sha256"]
    ),
    "generated_tree_hash_matches_all_layers": (
        actual_generated_tree
        == resolution["hashes"]["generated_tree_sha256"]
        == generator_manifest["generated_tree_sha256"]
        == export_result["generated_tree_sha256"]
        == recorded_preflight["generated_tree_sha256"]
    ),
    "discovery_hash_matches_all_layers": (
        actual_discovery_hash
        == resolution["hashes"]["discovery_manifest_sha256"]
        == input_manifest["stage3_discovery_manifest_sha256"]
        == generator_manifest["provenance"][
            "stage3_discovery_manifest_sha256"
        ]
        == export_result["stage3_discovery_manifest_sha256"]
        == recorded_preflight["stage3_discovery_manifest_sha256"]
    ),
    "verification_hash_matches_all_layers": (
        actual_verification_hash
        == inventory["verification_sha256"]
        == input_manifest["verification_sha256"]
        == resolution["stage1_source_hashes"]["verification.k"]
    ),
    "inventory_hash_matches_all_layers": (
        inventory["inventory_sha256"]
        == discovery["inventory_sha256"]
        == input_manifest["inventory_sha256"]
        == generator_manifest["provenance"]["inventory_sha256"]
    ),
    "producer_file_hashes_match_all_layers": (
        observed_producer_files
        == source_manifest["files"]
        == manifest_producer_files
    ),
    "producer_image_ids_match_all_layers": (
        len(set(producer_image_ids.values())) == 1
    ),
    "producer_bundle_hash_matches_audit_input": (
        actual_pipeline_trees["generation_producer_sources_sha256"]
        == resolution["hashes"]["generation_producer_sources_sha256"]
    ),
    "toolchain_lock_matches_generator": (
        load(Path("/reference/klean-toolchain.lock.json"))
        == generator_manifest["toolchain"]
    ),
    "inventory_discovery_ordered_bijection": (
        discovery_ids == inventory_ids
        and len(discovery_ids) == len(set(discovery_ids))
    ),
    "every_inventory_rule_accounted_once": (
        sorted(accounted_ids) == sorted(inventory_ids)
        and len(accounted_ids) == len(set(accounted_ids))
    ),
    "independent_classification_matches_stage3": (
        independent_classifications == observed_classifications
    ),
    "simplification_policy_satisfied": all(
        "simplification" not in entry["attributes"]
        or independent_classifications[entry["source_rule_id"]]
        in {"DEFINITION", "DOMAIN_LEMMA"}
        for entry in inventory["rules"]
    ),
    "independent_domain_set_empty": independent_domain_ids == [],
    "source_rule_obligation_bijection_exact_and_empty": (
        generated_source_ids
        == independent_domain_ids
        == obligation_ids
        and len(obligation_ids) == len(set(obligation_ids))
        and input_manifest["source_rules"] == obligation_map["source_rules"]
    ),
    "trust_parameter_set_empty": obligation_map["trust_parameters"] == [],
    "obligation_map_hash_matches_generator": (
        actual_obligation_map_hash
        == generator_manifest["obligation_map_sha256"]
    ),
    "trust_inventory_hash_matches_export": (
        actual_trust_inventory_hash
        == export_result["trust_inventory_sha256"]
    ),
    "all_obligation_counts_zero": (
        generator_manifest["obligation_count"]
        == export_result["obligation_count"]
        == recorded_preflight["obligation_count"]
        == resolution["stage4_preflight"]["obligation_count"]
        == len(obligation_map["obligations"])
        == 0
    ),
    "all_statuses_no_obligations": (
        export_result["status"]
        == recorded_preflight["status"]
        == resolution["stage4_preflight"]["status"]
        == resolution["selections"]["klean_generation"]["status"]
        == "KLEAN_NO_OBLIGATIONS"
    ),
    "recorded_preflight_exactly_bound_into_audit_input": (
        recorded_preflight == resolution["stage4_preflight"]
    ),
    "recorded_preflight_diagnostic_hashes_self_consistent": all(
        len(entry["output_tail"].encode()) < 4000
        and hashlib.sha256(entry["output_tail"].encode()).hexdigest()
        == entry["output_sha256"]
        for entry in recorded_preflight["diagnostics"]
    ),
    "fixed_target_absent_at_every_layer": (
        target_from_tree is None
        and expected_target_definition is None
        and generator_manifest["target"] is None
        and recorded_preflight["target"] is None
        and resolution["stage4_preflight"]["target"] is None
        and resolution["target"] is None
    ),
    "no_stage5_candidate_or_binding": (
        not Path("/candidate").exists()
        and resolution["lean_workspace"] is None
        and resolution["lean_invocation"] is None
        and resolution["stage5_result"] is None
        and resolution["hashes"]["lean_workspace_sha256"] is None
        and resolution["hashes"]["lean_invocation_sha256"] is None
    ),
    "generated_trust_inventory_has_no_sorries": (
        trust_inventory["designated_sorries"] == 0
        and trust_inventory["other_sorries"] == 0
    ),
}

report = {
    "checks": checks,
    "all_checks_pass": all(checks.values()),
    "inventory_ids": inventory_ids,
    "independent_classifications": independent_classifications,
    "independent_domain_ids": independent_domain_ids,
    "generated_source_ids": generated_source_ids,
    "obligation_ids": obligation_ids,
    "producer_image_ids": producer_image_ids,
    "observed_producer_files": observed_producer_files,
    "actual_pipeline_trees": actual_pipeline_trees,
    "actual_stage1_export_sha256": actual_stage1_export,
    "actual_generated_tree_sha256": actual_generated_tree,
    "actual_discovery_manifest_sha256": actual_discovery_hash,
    "actual_inventory_sha256": inventory["inventory_sha256"],
    "target_from_tree": target_from_tree,
}
print(json.dumps(report, indent=2, sort_keys=True))
if not report["all_checks_pass"]:
    raise SystemExit(1)
