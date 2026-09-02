#!/usr/bin/env python3

import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, "/reference")

from tools import k_rule_inventory, klean_export, pipeline_contract


def load(path: Path):
    return json.loads(path.read_text())


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


audit = load(Path("/audit-input.json"))
resolution = audit["resolution"]
expected_hashes = resolution["hashes"]

k_workspace = Path("/reference/k-proof")
k_audit = Path("/reference/k-audit")
discovery_path = Path("/reference/lemma-discovery.json")
generation = Path("/reference/klean-generation")
generated = generation / "generated"
producer_sources = Path("/reference/generation-tools")

generator = load(generation / "generator-manifest.json")
input_manifest = load(generation / "input-manifest.json")
export_result = load(generation / "export-result.json")
preflight = load(generation / "preflight.json")
obligation_map = load(generated / "obligation-map.json")
source_manifest = load(producer_sources / "source-manifest.json")
toolchain_lock = load(Path("/reference/klean-toolchain.lock.json"))
discovery = load(discovery_path)

observed_hashes = {
    "k_workspace_sha256": pipeline_contract.sha256_tree(k_workspace),
    "stage1_export_sha256": klean_export.tree_digest(k_workspace),
    "discovery_manifest_sha256": sha256(discovery_path),
    "k_audit_sha256": pipeline_contract.sha256_tree(k_audit),
    "klean_generation_sha256": pipeline_contract.sha256_tree(generation),
    "generation_producer_sources_sha256": pipeline_contract.sha256_tree(producer_sources),
    "generated_tree_sha256": klean_export.tree_digest(generated),
    "lean_workspace_sha256": None,
    "lean_invocation_sha256": None,
}

recorded_source_hashes = resolution["stage1_source_hashes"]
observed_source_hashes = {
    path.relative_to(k_workspace).as_posix(): sha256(path)
    for path in pipeline_contract._walk_regular_files(k_workspace, "frozen Stage 1")
}
source_hash_mismatches = sorted(
    name
    for name in set(recorded_source_hashes) | set(observed_source_hashes)
    if recorded_source_hashes.get(name) != observed_source_hashes.get(name)
)

reconstructed = k_rule_inventory.inventory_verification(k_workspace)
producer_file_hashes = {
    name: sha256(producer_sources / name)
    for name in ("klean_export.py", "klean.py")
}
expected_producer_hashes = {
    "klean_export.py": generator["exporter_sha256"],
    "klean.py": generator["klean_py_sha256"],
}
audit_image_key = Path(resolution["generation_producer_sources"]).name
generator_image_id = generator["provenance"]["generator_image_id"]
generator_image_key = generator_image_id.removeprefix("sha256:")

target_statement = klean_export.target_statement(generated)
expected_target_definition = klean_export.expected_target_definition(obligation_map)

checks = {
    "launcher_mode_is_classification_only": resolution["mode"] == "CLASSIFICATION_ONLY",
    "environment_semantics_mode_is_supplied": resolution["semantics_mode"] == "SUPPLIED_SEMANTICS",
    "launcher_problem_and_condition_match": (
        resolution["problem_id"] == "101-words-string"
        and resolution["condition"] == "kit-semantics"
    ),
    "every_launcher_resolution_hash_matches": observed_hashes == expected_hashes,
    "every_stage1_source_file_and_hash_matches": not source_hash_mismatches,
    "stage1_source_file_count_matches": len(recorded_source_hashes) == len(observed_source_hashes),
    "selected_k_audit_artifact_hash_matches": (
        resolution["selections"]["k_audit"]["artifact_sha256"]
        == observed_hashes["k_audit_sha256"]
    ),
    "selected_generation_artifact_hash_matches": (
        resolution["selections"]["klean_generation"]["artifact_sha256"]
        == observed_hashes["klean_generation_sha256"]
    ),
    "protected_discovery_matches_reconstruction": (
        discovery["inventory_sha256"] == reconstructed["inventory_sha256"]
        and discovery["rules"] == reconstructed["rules"]
    ),
    "producer_file_hashes_match_both_manifests": (
        producer_file_hashes == expected_producer_hashes == source_manifest["files"]
    ),
    "producer_bundle_has_exact_file_set": (
        {path.relative_to(producer_sources).as_posix()
         for path in pipeline_contract._walk_regular_files(producer_sources, "producer bundle")}
        == {"klean_export.py", "klean.py", "source-manifest.json"}
    ),
    "immutable_generator_image_id_matches_source_manifest_and_audit_path": (
        source_manifest["generator_image_id"] == generator_image_id
        and audit_image_key == generator_image_key
    ),
    "generator_toolchain_matches_pinned_lock": generator["toolchain"] == toolchain_lock,
    "generator_generated_tree_hash_matches": (
        generator["generated_tree_sha256"] == observed_hashes["generated_tree_sha256"]
    ),
    "generator_obligation_map_hash_matches": (
        generator["obligation_map_sha256"] == sha256(generated / "obligation-map.json")
    ),
    "generator_provenance_stage1_matches": (
        generator["provenance"]["stage1_workspace_sha256"]
        == observed_hashes["stage1_export_sha256"]
    ),
    "generator_provenance_stage3_matches": (
        generator["provenance"]["stage3_discovery_manifest_sha256"]
        == observed_hashes["discovery_manifest_sha256"]
    ),
    "generator_provenance_inventory_matches": (
        generator["provenance"]["inventory_sha256"] == reconstructed["inventory_sha256"]
    ),
    "input_manifest_hashes_match": (
        input_manifest["frozen_input_sha256"] == observed_hashes["stage1_export_sha256"]
        and input_manifest["stage1_workspace_sha256"] == observed_hashes["stage1_export_sha256"]
        and input_manifest["stage3_discovery_manifest_sha256"] == observed_hashes["discovery_manifest_sha256"]
        and input_manifest["verification_sha256"] == reconstructed["verification_sha256"]
        and input_manifest["inventory_sha256"] == reconstructed["inventory_sha256"]
    ),
    "export_result_hashes_match": (
        export_result["frozen_input_sha256"] == observed_hashes["stage1_export_sha256"]
        and export_result["stage3_discovery_manifest_sha256"] == observed_hashes["discovery_manifest_sha256"]
        and export_result["generated_tree_sha256"] == observed_hashes["generated_tree_sha256"]
        and export_result["trust_inventory_sha256"] == sha256(generation / "trust-inventory.json")
    ),
    "recorded_preflight_hashes_match": (
        preflight["frozen_input_sha256"] == observed_hashes["stage1_export_sha256"]
        and preflight["stage1_workspace_sha256"] == observed_hashes["stage1_export_sha256"]
        and preflight["stage3_discovery_manifest_sha256"] == observed_hashes["discovery_manifest_sha256"]
        and preflight["generated_tree_sha256"] == observed_hashes["generated_tree_sha256"]
    ),
    "exact_empty_source_rule_obligation_bijection": (
        discovery["rules"] == []
        and input_manifest["source_rules"] == []
        and obligation_map["source_rules"] == []
        and obligation_map["obligations"] == []
        and obligation_map["trust_parameters"] == []
        and generator["obligation_count"] == 0
        and export_result["obligation_count"] == 0
        and preflight["obligation_count"] == 0
    ),
    "no_generated_target": (
        generator["target"] is None
        and preflight["target"] is None
        and target_statement is None
        and expected_target_definition is None
    ),
    "no_stage5_candidate_or_launcher_paths": (
        not Path("/candidate").exists()
        and resolution["lean_workspace"] is None
        and resolution["lean_invocation"] is None
        and resolution["target"] is None
    ),
    "selected_stage4_status_is_no_obligations": (
        resolution["selections"]["klean_generation"]["status"] == "KLEAN_NO_OBLIGATIONS"
        and export_result["status"] == "KLEAN_NO_OBLIGATIONS"
        and preflight["status"] == "KLEAN_NO_OBLIGATIONS"
    ),
}

report = {
    "checks": checks,
    "expected_resolution_hashes": expected_hashes,
    "observed_resolution_hashes": observed_hashes,
    "recorded_stage1_source_file_count": len(recorded_source_hashes),
    "observed_stage1_source_file_count": len(observed_source_hashes),
    "stage1_source_hash_mismatches": source_hash_mismatches,
    "reconstructed_rule_count": len(reconstructed["rules"]),
    "mapped_obligation_count": len(obligation_map["obligations"]),
    "observed_target": target_statement,
    "expected_target_definition": expected_target_definition,
    "producer_file_hashes": producer_file_hashes,
    "generator_image_id": generator_image_id,
    "audit_image_key": audit_image_key,
    "all_checks_pass": all(checks.values()),
}
print(json.dumps(report, indent=2, sort_keys=True))
raise SystemExit(0 if report["all_checks_pass"] else 1)
