#!/usr/bin/env python3
import hashlib
import json
import os
import re
from pathlib import Path

from tools import klean_export
from tools.lemma_discovery_contract import validate_trust_boundary
from tools.pipeline_contract import _walk_regular_files, sha256_tree
from tools.stage6_resolution_contract import (
    canonical_json_sha256,
    verify_audit_input,
)


stage1 = Path("/reference/k-proof")
k_audit = Path("/reference/k-audit")
discovery_path = Path("/reference/lemma-discovery.json")
generation = Path("/reference/klean-generation")
generated = generation / "generated"
producer_sources = Path("/reference/generation-tools")
audit = json.loads(Path("/audit-input.json").read_text())
resolution = audit["resolution"]
recorded_hashes = resolution["hashes"]
verified_resolution, verified_resolution_sha256 = verify_audit_input(audit)

discovery = json.loads(discovery_path.read_text())
validated = validate_trust_boundary(stage1, discovery_path)
input_manifest = json.loads((generation / "input-manifest.json").read_text())
generator_manifest = json.loads(
    (generation / "generator-manifest.json").read_text()
)
export_result = json.loads((generation / "export-result.json").read_text())
preflight = json.loads((generation / "preflight.json").read_text())
trust_inventory_path = generation / "trust-inventory.json"
trust_inventory = json.loads(trust_inventory_path.read_text())
obligation_map_path = generated / "obligation-map.json"
obligation_map = json.loads(obligation_map_path.read_text())

pipeline_hashes = {
    "k_workspace_sha256": sha256_tree(stage1),
    "k_audit_sha256": sha256_tree(k_audit),
    "klean_generation_sha256": sha256_tree(generation),
    "generation_producer_sources_sha256": sha256_tree(producer_sources),
}
klean_hashes = {
    "stage1_export_sha256": klean_export.tree_digest(stage1),
    "generated_tree_sha256": klean_export.tree_digest(generated),
}
discovery_sha256 = hashlib.sha256(discovery_path.read_bytes()).hexdigest()

source_hashes = {
    path.relative_to(stage1).as_posix(): hashlib.sha256(
        path.read_bytes()
    ).hexdigest()
    for path in _walk_regular_files(stage1, "Stage 1 source workspace")
}

# Independent semantic classification recorded in the audit: the only local
# rule defines the fresh proof term #sameChars; no local rule is a domain lemma.
independent_domain_source_rule_ids = []
validated_domain_source_rule_ids = [
    rule["source_rule_id"] for rule in validated["domain_lemmas"]
]
expected_source_rules = klean_export._domain_source_rules(
    validated, discovery_sha256
)
obligations = obligation_map["obligations"]
observed_obligation_ids = [
    obligation["source_rule_id"] for obligation in obligations
]
expected_obligation_ids = [
    source_rule["source_rule_id"] for source_rule in expected_source_rules
]

target = klean_export.target_statement(generated)
expected_target_definition = klean_export.expected_target_definition(
    obligation_map
)
raw_target_declaration_count = 0
for path in generated.rglob("*.lean"):
    raw_target_declaration_count += len(
        re.findall(r"(?m)^\s*def\s+targetStatement\b", path.read_text())
    )

checks = {
    "audit_input_envelope_hash": (
        verified_resolution == resolution
        and verified_resolution_sha256 == audit["resolved_input_sha256"]
        and canonical_json_sha256(resolution)
        == audit["resolved_input_sha256"]
    ),
    "environment_mode_matches_signed_resolution": (
        os.environ.get("AUDIT_MODE") == resolution["mode"]
        == "CLASSIFICATION_ONLY"
    ),
    "pipeline_hashes_match_audit_input": {
        name: value == recorded_hashes[name]
        for name, value in pipeline_hashes.items()
    },
    "klean_hashes_match_audit_input": {
        name: value == recorded_hashes[name]
        for name, value in klean_hashes.items()
    },
    "discovery_hash_matches_audit_input": (
        discovery_sha256 == recorded_hashes["discovery_manifest_sha256"]
    ),
    "stage1_source_hash_map_exact": (
        source_hashes == resolution["stage1_source_hashes"]
    ),
    "lean_hashes_are_null_in_classification_only": (
        recorded_hashes["lean_workspace_sha256"] is None
        and recorded_hashes["lean_invocation_sha256"] is None
    ),
    "input_manifest_stage1_hashes": (
        input_manifest["frozen_input_sha256"]
        == klean_hashes["stage1_export_sha256"]
        == input_manifest["stage1_workspace_sha256"]
    ),
    "input_manifest_discovery_hash": (
        input_manifest["stage3_discovery_manifest_sha256"]
        == discovery_sha256
    ),
    "input_manifest_inventory_hash": (
        input_manifest["inventory_sha256"] == validated["inventory_sha256"]
    ),
    "input_manifest_verification_hash": (
        input_manifest["verification_sha256"]
        == hashlib.sha256((stage1 / "verification.k").read_bytes()).hexdigest()
    ),
    "generator_generated_tree_hash": (
        generator_manifest["generated_tree_sha256"]
        == klean_hashes["generated_tree_sha256"]
    ),
    "generator_provenance_stage1": (
        generator_manifest["provenance"]["stage1_workspace_sha256"]
        == klean_hashes["stage1_export_sha256"]
    ),
    "generator_provenance_discovery": (
        generator_manifest["provenance"][
            "stage3_discovery_manifest_sha256"
        ]
        == discovery_sha256
    ),
    "generator_provenance_inventory": (
        generator_manifest["provenance"]["inventory_sha256"]
        == validated["inventory_sha256"]
    ),
    "independent_domain_set_matches_stage3": (
        independent_domain_source_rule_ids
        == validated_domain_source_rule_ids
        == []
    ),
    "input_source_rules_exact": (
        input_manifest["source_rules"] == expected_source_rules == []
    ),
    "obligation_map_source_rules_exact": (
        obligation_map["source_rules"] == expected_source_rules == []
    ),
    "ordered_source_obligation_ids_exact": (
        observed_obligation_ids == expected_obligation_ids == []
    ),
    "obligation_ids_unique": (
        len(observed_obligation_ids) == len(set(observed_obligation_ids))
    ),
    "zero_obligations": (
        obligations == []
        and generator_manifest["obligation_count"] == 0
        and export_result["obligation_count"] == 0
        and preflight["obligation_count"] == 0
        and resolution["stage4_preflight"]["obligation_count"] == 0
    ),
    "zero_trust_parameters": obligation_map["trust_parameters"] == [],
    "obligation_map_hash": (
        generator_manifest["obligation_map_sha256"]
        == hashlib.sha256(obligation_map_path.read_bytes()).hexdigest()
    ),
    "no_generated_target": (
        target is None
        and expected_target_definition is None
        and generator_manifest["target"] is None
        and preflight["target"] is None
        and resolution["target"] is None
        and resolution["stage4_preflight"]["target"] is None
        and raw_target_declaration_count == 0
    ),
    "no_candidate": not Path("/candidate").exists(),
    "classification_only_mode": (
        resolution["mode"] == "CLASSIFICATION_ONLY"
        and resolution["stage5_result"] is None
    ),
    "no_obligation_status_consistent": (
        export_result["status"] == "KLEAN_NO_OBLIGATIONS"
        and preflight["status"] == "KLEAN_NO_OBLIGATIONS"
        and resolution["stage4_preflight"]["status"]
        == "KLEAN_NO_OBLIGATIONS"
        and resolution["selections"]["klean_generation"]["status"]
        == "KLEAN_NO_OBLIGATIONS"
    ),
    "export_hash_bindings": (
        export_result["frozen_input_sha256"]
        == klean_hashes["stage1_export_sha256"]
        and export_result["stage3_discovery_manifest_sha256"]
        == discovery_sha256
        and export_result["generated_tree_sha256"]
        == klean_hashes["generated_tree_sha256"]
        and export_result["trust_inventory_sha256"]
        == hashlib.sha256(trust_inventory_path.read_bytes()).hexdigest()
    ),
    "recorded_preflight_document_exact": (
        preflight == resolution["stage4_preflight"]
    ),
    "recorded_preflight_output_hashes": all(
        hashlib.sha256(diagnostic["output_tail"].encode()).hexdigest()
        == diagnostic["output_sha256"]
        for diagnostic in preflight["diagnostics"]
    ),
    "trust_inventory_no_sorries": (
        trust_inventory["designated_sorries"] == 0
        and trust_inventory["other_sorries"] == 0
    ),
}

print(
    json.dumps(
        {
            "pipeline_hashes": pipeline_hashes,
            "klean_hashes": klean_hashes,
            "discovery_sha256": discovery_sha256,
            "source_hash_count": len(source_hashes),
            "inventory_sha256": validated["inventory_sha256"],
            "independent_domain_source_rule_ids": (
                independent_domain_source_rule_ids
            ),
            "expected_source_rules": expected_source_rules,
            "obligation_map": obligation_map,
            "target": target,
            "expected_target_definition": expected_target_definition,
            "raw_target_declaration_count": raw_target_declaration_count,
            "checks": checks,
        },
        indent=2,
        sort_keys=True,
    )
)

for name, value in checks.items():
    if isinstance(value, dict):
        assert all(value.values()), (name, value)
    else:
        assert value is True, (name, value)
