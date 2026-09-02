#!/usr/bin/env python3
import hashlib
import json
import os
import re
from pathlib import Path

from tools import klean_export, lemma_discovery_contract, pipeline_contract
from tools.stage6_resolution_contract import (
    canonical_json_sha256,
    verify_audit_input,
)


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


audit_document = json.loads(Path("/audit-input.json").read_text())
resolution, resolved_digest = verify_audit_input(audit_document)
audit_hashes = resolution["hashes"]
generation = Path("/reference/klean-generation")
generated = generation / "generated"
k_workspace = Path("/reference/k-proof")
k_audit = Path("/reference/k-audit")
discovery_path = Path("/reference/lemma-discovery.json")
producer_sources = Path("/reference/generation-tools")

input_manifest = json.loads((generation / "input-manifest.json").read_text())
generator_manifest = json.loads(
    (generation / "generator-manifest.json").read_text()
)
export_result = json.loads((generation / "export-result.json").read_text())
recorded_preflight = json.loads((generation / "preflight.json").read_text())
rerun_preflight = json.loads(
    Path("/audit-output/evidence/preflight-rerun.json").read_text()
)
trust_inventory_path = generation / "trust-inventory.json"
obligation_map_path = generated / "obligation-map.json"
obligation_map = json.loads(obligation_map_path.read_text())
validated = lemma_discovery_contract.validate_trust_boundary(
    k_workspace, discovery_path
)

pipeline_tree_hashes = {
    "k_workspace_sha256": pipeline_contract.sha256_tree(k_workspace),
    "k_audit_sha256": pipeline_contract.sha256_tree(k_audit),
    "klean_generation_sha256": pipeline_contract.sha256_tree(generation),
    "generation_producer_sources_sha256": pipeline_contract.sha256_tree(
        producer_sources
    ),
}
klean_stage1_hash = klean_export.tree_digest(k_workspace)
generated_hash = klean_export.tree_digest(generated)
discovery_hash = file_sha256(discovery_path)
trust_inventory_hash = file_sha256(trust_inventory_path)
obligation_map_hash = file_sha256(obligation_map_path)
verification_hash = file_sha256(k_workspace / "verification.k")

stage1_source_hashes = {
    path.relative_to(k_workspace).as_posix(): file_sha256(path)
    for path in pipeline_contract._walk_regular_files(
        k_workspace, "audit Stage 1 source workspace"
    )
}

expected_source_rules = klean_export._domain_source_rules(
    validated, discovery_hash
)
target = klean_export.target_statement(generated)
expected_target_definition = klean_export.expected_target_definition(
    obligation_map
)
raw_target_count = sum(
    len(re.findall(r"(?m)^\s*def\s+targetStatement\b", path.read_text()))
    for path in generated.rglob("*.lean")
)

checks = {
    "audit_envelope_digest": resolved_digest
    == canonical_json_sha256(resolution)
    == audit_document["resolved_input_sha256"],
    "audit_mode_matches_environment": resolution["mode"]
    == os.environ.get("AUDIT_MODE")
    == "CLASSIFICATION_ONLY",
    "audit_pipeline_tree_hashes": all(
        audit_hashes[name] == observed
        for name, observed in pipeline_tree_hashes.items()
    ),
    "audit_stage1_export_hash": audit_hashes["stage1_export_sha256"]
    == klean_stage1_hash,
    "audit_discovery_hash": audit_hashes["discovery_manifest_sha256"]
    == discovery_hash,
    "audit_generated_tree_hash": audit_hashes["generated_tree_sha256"]
    == generated_hash,
    "audit_lean_hashes_null": audit_hashes["lean_workspace_sha256"] is None
    and audit_hashes["lean_invocation_sha256"] is None,
    "audit_stage1_file_hashes_exact": resolution["stage1_source_hashes"]
    == stage1_source_hashes,
    "selection_hashes_match": resolution["selections"]["k_audit"][
        "artifact_sha256"
    ]
    == pipeline_tree_hashes["k_audit_sha256"]
    and resolution["selections"]["klean_generation"]["artifact_sha256"]
    == pipeline_tree_hashes["klean_generation_sha256"],
    "selected_status_no_obligations": resolution["selections"][
        "klean_generation"
    ]["status"]
    == "KLEAN_NO_OBLIGATIONS",
    "input_manifest_stage1_hashes": input_manifest["frozen_input_sha256"]
    == input_manifest["stage1_workspace_sha256"]
    == klean_stage1_hash,
    "input_manifest_discovery_hash": input_manifest[
        "stage3_discovery_manifest_sha256"
    ]
    == discovery_hash,
    "input_manifest_inventory_hash": input_manifest["inventory_sha256"]
    == validated["inventory_sha256"],
    "input_manifest_verification_hash": input_manifest["verification_sha256"]
    == verification_hash,
    "input_manifest_definitions_exact": input_manifest["definitions"]
    == validated["definitions"],
    "input_manifest_non_definition_sets_exact": input_manifest["source_rules"]
    == expected_source_rules
    == []
    and input_manifest["operational_rules"] == validated["operational_rules"]
    == []
    and input_manifest["proved_derived_lemmas"]
    == validated["proved_derived_lemmas"]
    == [],
    "generator_generated_tree_hash": generator_manifest[
        "generated_tree_sha256"
    ]
    == generated_hash,
    "generator_obligation_map_hash": generator_manifest[
        "obligation_map_sha256"
    ]
    == obligation_map_hash,
    "generator_inventory_provenance": generator_manifest["provenance"][
        "inventory_sha256"
    ]
    == validated["inventory_sha256"],
    "generator_stage1_provenance": generator_manifest["provenance"][
        "stage1_workspace_sha256"
    ]
    == klean_stage1_hash,
    "generator_discovery_provenance": generator_manifest["provenance"][
        "stage3_discovery_manifest_sha256"
    ]
    == discovery_hash,
    "generator_toolchain_lock_exact": generator_manifest["toolchain"]
    == json.loads(Path("/reference/klean-toolchain.lock.json").read_text()),
    "obligation_source_rules_exact": obligation_map["source_rules"]
    == expected_source_rules
    == [],
    "obligation_list_exactly_empty": obligation_map["obligations"] == [],
    "trust_parameters_exactly_empty": obligation_map["trust_parameters"] == [],
    "obligation_count_exact": generator_manifest["obligation_count"]
    == export_result["obligation_count"]
    == rerun_preflight["obligation_count"]
    == 0,
    "export_status_exact": export_result["status"]
    == rerun_preflight["status"]
    == "KLEAN_NO_OBLIGATIONS",
    "export_stage1_hash": export_result["frozen_input_sha256"]
    == klean_stage1_hash,
    "export_discovery_hash": export_result[
        "stage3_discovery_manifest_sha256"
    ]
    == discovery_hash,
    "export_generated_tree_hash": export_result["generated_tree_sha256"]
    == generated_hash,
    "export_trust_inventory_hash": export_result["trust_inventory_sha256"]
    == trust_inventory_hash,
    "preflight_rerun_exact": rerun_preflight == recorded_preflight
    == resolution["stage4_preflight"],
    "target_absent_everywhere": target is None
    and expected_target_definition is None
    and raw_target_count == 0
    and generator_manifest["target"] is None
    and recorded_preflight["target"] is None
    and resolution["target"] is None,
    "stage5_absent": not os.path.lexists("/candidate")
    and resolution["lean_workspace"] is None
    and resolution["lean_invocation"] is None
    and resolution["stage5_result"] is None,
}

print(
    json.dumps(
        {
            "observed": {
                "resolved_input_sha256": resolved_digest,
                "pipeline_tree_hashes": pipeline_tree_hashes,
                "stage1_export_sha256": klean_stage1_hash,
                "stage1_source_file_count": len(stage1_source_hashes),
                "discovery_manifest_sha256": discovery_hash,
                "generated_tree_sha256": generated_hash,
                "trust_inventory_sha256": trust_inventory_hash,
                "obligation_map_sha256": obligation_map_hash,
                "verification_sha256": verification_hash,
                "canonical_domain_rule_count": len(
                    validated["domain_lemmas"]
                ),
                "mapped_source_rule_count": len(
                    obligation_map["source_rules"]
                ),
                "mapped_obligation_count": len(
                    obligation_map["obligations"]
                ),
                "raw_target_declaration_count": raw_target_count,
                "target": target,
                "candidate_lexists": os.path.lexists("/candidate"),
            },
            "checks": checks,
            "all_checks_pass": all(checks.values()),
        },
        indent=2,
        sort_keys=True,
    )
)
raise SystemExit(0 if all(checks.values()) else 1)
