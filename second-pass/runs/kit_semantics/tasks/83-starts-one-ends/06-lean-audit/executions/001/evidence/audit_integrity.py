#!/usr/bin/env python3

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

from tools import klean_export, lemma_discovery_contract, pipeline_contract
from tools.k_rule_inventory import inventory_verification


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


audit = json.loads(Path("/audit-input.json").read_text())
resolution = audit["resolution"]
recorded_hashes = resolution["hashes"]

k_workspace = Path("/reference/k-proof")
k_audit = Path("/reference/k-audit")
discovery_path = Path("/reference/lemma-discovery.json")
generation = Path("/reference/klean-generation")
generated = generation / "generated"
producer = Path("/reference/generation-tools")

discovery = json.loads(discovery_path.read_text())
generator_manifest = json.loads((generation / "generator-manifest.json").read_text())
input_manifest = json.loads((generation / "input-manifest.json").read_text())
obligation_map = json.loads((generated / "obligation-map.json").read_text())
source_manifest = json.loads((producer / "source-manifest.json").read_text())
export_result = json.loads((generation / "export-result.json").read_text())
recorded_preflight = json.loads((generation / "preflight.json").read_text())

computed_hashes = {
    "k_workspace_sha256": pipeline_contract.sha256_tree(k_workspace),
    "stage1_export_sha256": klean_export.tree_digest(k_workspace),
    "discovery_manifest_sha256": sha256_file(discovery_path),
    "k_audit_sha256": pipeline_contract.sha256_tree(k_audit),
    "klean_generation_sha256": pipeline_contract.sha256_tree(generation),
    "generation_producer_sources_sha256": pipeline_contract.sha256_tree(producer),
    "generated_tree_sha256": klean_export.tree_digest(generated),
    "lean_workspace_sha256": None,
    "lean_invocation_sha256": None,
}

observed_stage1_sources = {
    path.relative_to(k_workspace).as_posix(): pipeline_contract.sha256_file(path)
    for path in pipeline_contract._walk_regular_files(
        k_workspace, "mounted Stage 1 workspace"
    )
}
recorded_stage1_sources = resolution["stage1_source_hashes"]

inventory = inventory_verification(k_workspace)
validated_discovery = lemma_discovery_contract.validate_trust_boundary(
    k_workspace, discovery_path
)

producer_files = {
    path.relative_to(producer).as_posix()
    for path in pipeline_contract._walk_regular_files(
        producer, "mounted Stage 4 producer bundle"
    )
}
producer_hashes = {
    "klean.py": sha256_file(producer / "klean.py"),
    "klean_export.py": sha256_file(producer / "klean_export.py"),
}
generator_image_id = generator_manifest["provenance"]["generator_image_id"]
audit_image_key = Path(resolution["generation_producer_sources"]).name

target = klean_export.target_statement(generated)
expected_target_definition = klean_export.expected_target_definition(obligation_map)
target_module_text = (generated / "Klean83StartsOneEnds.lean").read_text()
target_declarations = re.findall(
    r"(?m)^\s*(?:def|theorem|lemma|axiom|opaque)\s+([^\s:(]+)",
    target_module_text,
)

checks = {
    "audit_mode_classification_only": resolution["mode"] == "CLASSIFICATION_ONLY",
    "audit_semantics_mode_supplied": resolution["semantics_mode"] == "SUPPLIED_SEMANTICS",
    "all_recorded_top_hashes_match": computed_hashes == recorded_hashes,
    "stage1_source_file_set_and_hashes_match": observed_stage1_sources
    == recorded_stage1_sources,
    "stage2_selection_artifact_matches": resolution["selections"]["k_audit"]["artifact_sha256"]
    == computed_hashes["k_audit_sha256"],
    "stage4_selection_artifact_matches": resolution["selections"]["klean_generation"]["artifact_sha256"]
    == computed_hashes["klean_generation_sha256"],
    "stage4_selection_no_obligations": resolution["selections"]["klean_generation"]["status"]
    == "KLEAN_NO_OBLIGATIONS",
    "recorded_preflight_matches_audit_input": recorded_preflight
    == resolution["stage4_preflight"],
    "inventory_hash_matches_discovery": inventory["inventory_sha256"]
    == discovery["inventory_sha256"],
    "inventory_rules_bijectively_match_discovery": inventory["rules"]
    == discovery["rules"],
    "inventory_rules_unique": len(
        {entry["source_rule_id"] for entry in inventory["rules"]}
    )
    == len(inventory["rules"]),
    "validated_discovery_rules_match": validated_discovery["rules"]
    == discovery["rules"],
    "verification_hash_matches_input_manifest": sha256_file(
        k_workspace / "verification.k"
    )
    == input_manifest["verification_sha256"],
    "producer_bundle_exact_file_set": producer_files
    == {"klean.py", "klean_export.py", "source-manifest.json"},
    "producer_file_hashes_match_source_manifest": producer_hashes
    == source_manifest["files"],
    "producer_file_hashes_match_generator_manifest": producer_hashes
    == {
        "klean.py": generator_manifest["klean_py_sha256"],
        "klean_export.py": generator_manifest["exporter_sha256"],
    },
    "producer_image_matches_source_manifest": generator_image_id
    == source_manifest["generator_image_id"],
    "producer_image_matches_audit_input_content_address": generator_image_id
    == f"sha256:{audit_image_key}",
    "stage1_export_hash_matches_manifests": computed_hashes["stage1_export_sha256"]
    == input_manifest["stage1_workspace_sha256"]
    == input_manifest["frozen_input_sha256"]
    == generator_manifest["provenance"]["stage1_workspace_sha256"],
    "discovery_hash_matches_manifests": computed_hashes["discovery_manifest_sha256"]
    == input_manifest["stage3_discovery_manifest_sha256"]
    == generator_manifest["provenance"]["stage3_discovery_manifest_sha256"],
    "inventory_hash_matches_stage4_manifests": inventory["inventory_sha256"]
    == input_manifest["inventory_sha256"]
    == generator_manifest["provenance"]["inventory_sha256"],
    "generated_tree_matches_manifests": computed_hashes["generated_tree_sha256"]
    == generator_manifest["generated_tree_sha256"]
    == export_result["generated_tree_sha256"],
    "obligation_map_hash_matches_manifest": sha256_file(
        generated / "obligation-map.json"
    )
    == generator_manifest["obligation_map_sha256"],
    "source_rule_bijection_is_exactly_empty": input_manifest["source_rules"]
    == obligation_map["source_rules"]
    == [],
    "obligation_list_is_exactly_empty": obligation_map["obligations"] == [],
    "trust_parameter_list_is_exactly_empty": obligation_map["trust_parameters"]
    == [],
    "obligation_counts_are_zero": generator_manifest["obligation_count"]
    == export_result["obligation_count"]
    == recorded_preflight["obligation_count"]
    == 0,
    "expected_target_is_none": expected_target_definition is None,
    "observed_target_is_none": target is None,
    "manifest_target_is_none": generator_manifest["target"] is None,
    "audit_input_target_is_none": resolution["target"] is None,
    "target_module_has_no_declarations": target_declarations == [],
    "no_stage5_candidate_mount": not Path("/candidate").exists(),
    "no_stage5_paths_in_audit_input": resolution["lean_workspace"] is None
    and resolution["lean_invocation"] is None
    and resolution["stage5_result"] is None,
    "export_status_no_obligations": export_result["status"]
    == "KLEAN_NO_OBLIGATIONS",
}

report = {
    "checks": checks,
    "all_checks_pass": all(checks.values()),
    "computed_hashes": computed_hashes,
    "recorded_hashes": recorded_hashes,
    "stage1_source_hash_summary": {
        "observed_count": len(observed_stage1_sources),
        "recorded_count": len(recorded_stage1_sources),
        "missing": sorted(set(recorded_stage1_sources) - set(observed_stage1_sources)),
        "extra": sorted(set(observed_stage1_sources) - set(recorded_stage1_sources)),
        "mismatched": sorted(
            path
            for path in set(observed_stage1_sources) & set(recorded_stage1_sources)
            if observed_stage1_sources[path] != recorded_stage1_sources[path]
        ),
    },
    "reconstructed_inventory": inventory,
    "producer": {
        "audit_image_key": audit_image_key,
        "generator_image_id": generator_image_id,
        "files": sorted(producer_files),
        "hashes": producer_hashes,
        "tree_sha256": computed_hashes["generation_producer_sources_sha256"],
    },
    "stage4": {
        "input_source_rules": input_manifest["source_rules"],
        "mapped_source_rules": obligation_map["source_rules"],
        "obligations": obligation_map["obligations"],
        "trust_parameters": obligation_map["trust_parameters"],
        "target": target,
        "target_declarations": target_declarations,
    },
}

print(json.dumps(report, indent=2, sort_keys=True))
raise SystemExit(0 if report["all_checks_pass"] else 1)
