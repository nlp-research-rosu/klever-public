#!/usr/bin/env python3
"""Independent hash, obligation-bijection, and target-identity audit."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from tools import (
    k_rule_inventory,
    klean_export,
    pipeline_contract,
    stage6_resolution_contract,
)


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


audit_document = json.loads(Path("/audit-input.json").read_text())
resolution, resolved_digest = stage6_resolution_contract.verify_audit_input(
    audit_document
)
generator = json.loads(
    Path("/reference/klean-generation/generator-manifest.json").read_text()
)
input_manifest = json.loads(
    Path("/reference/klean-generation/input-manifest.json").read_text()
)
export_result = json.loads(
    Path("/reference/klean-generation/export-result.json").read_text()
)
stored_preflight = json.loads(
    Path("/reference/klean-generation/preflight.json").read_text()
)
obligation_map_path = Path(
    "/reference/klean-generation/generated/obligation-map.json"
)
obligation_map = json.loads(obligation_map_path.read_text())
generated = Path("/reference/klean-generation/generated")
inventory = k_rule_inventory.inventory_verification(
    Path("/reference/k-proof")
)

actual_hashes = {
    "k_workspace_sha256": pipeline_contract.sha256_tree(
        Path("/reference/k-proof")
    ),
    "stage1_export_sha256": klean_export.tree_digest(
        Path("/reference/k-proof")
    ),
    "discovery_manifest_sha256": file_hash(
        Path("/reference/lemma-discovery.json")
    ),
    "k_audit_sha256": pipeline_contract.sha256_tree(
        Path("/reference/k-audit")
    ),
    "klean_generation_sha256": pipeline_contract.sha256_tree(
        Path("/reference/klean-generation")
    ),
    "generation_producer_sources_sha256": pipeline_contract.sha256_tree(
        Path("/reference/generation-tools")
    ),
    "generated_tree_sha256": klean_export.tree_digest(generated),
    "lean_workspace_sha256": pipeline_contract.sha256_tree(
        Path("/candidate")
    ),
}
recorded_hashes = {
    key: resolution["hashes"][key] for key in actual_hashes
}

actual_stage1_files = {
    path.relative_to(Path("/reference/k-proof")).as_posix(): file_hash(path)
    for path in pipeline_contract._walk_regular_files(
        Path("/reference/k-proof"), "mounted Stage 1 workspace"
    )
}
recorded_stage1_files = resolution["stage1_source_hashes"]

domain_rule = inventory["rules"][0]
expected_source_rule = {
    **domain_rule,
    "classification": "DOMAIN_LEMMA",
    "rationale": obligation_map["source_rules"][0]["rationale"],
    "inventory_sha256": inventory["inventory_sha256"],
    "discovery_manifest_sha256": actual_hashes[
        "discovery_manifest_sha256"
    ],
}
expected_conjunct = (
    "∀ (D : SortInt) (C : SortInt), "
    "(«strLt(_,_)_MPY-STR_Bool_IntSeq_IntSeq» "
    "(SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C "
    "SortIntSeq.«.IntSeq_MPY-CORE_IntSeq») "
    "(SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» D "
    "SortIntSeq.«.IntSeq_MPY-CORE_IntSeq») : SortBool) = "
    "(«_<Int_» C D : SortBool)"
)
obligations = obligation_map["obligations"]
source_rules = obligation_map["source_rules"]
obligation_ids = [item["source_rule_id"] for item in obligations]
source_ids = [item["source_rule_id"] for item in source_rules]
expected_definition = klean_export.expected_target_definition(obligation_map)
actual_target = klean_export.target_statement(generated)

checks = {
    "audit_input_signature_digest_valid": (
        resolved_digest == audit_document["resolved_input_sha256"]
    ),
    "all_mounted_resolution_hashes_match": actual_hashes == recorded_hashes,
    "stage1_file_hash_map_exact": actual_stage1_files == recorded_stage1_files,
    "stage1_file_hash_map_has_no_duplicate_paths": (
        len(actual_stage1_files) == len(set(actual_stage1_files))
    ),
    "input_manifest_stage1_hash": (
        input_manifest["stage1_workspace_sha256"]
        == actual_hashes["stage1_export_sha256"]
        == input_manifest["frozen_input_sha256"]
    ),
    "input_manifest_discovery_hash": (
        input_manifest["stage3_discovery_manifest_sha256"]
        == actual_hashes["discovery_manifest_sha256"]
    ),
    "input_manifest_inventory_hash": (
        input_manifest["inventory_sha256"] == inventory["inventory_sha256"]
    ),
    "input_manifest_verification_hash": (
        input_manifest["verification_sha256"]
        == inventory["verification_sha256"]
    ),
    "generator_provenance_stage1_hash": (
        generator["provenance"]["stage1_workspace_sha256"]
        == actual_hashes["stage1_export_sha256"]
    ),
    "generator_provenance_discovery_hash": (
        generator["provenance"]["stage3_discovery_manifest_sha256"]
        == actual_hashes["discovery_manifest_sha256"]
    ),
    "generator_provenance_inventory_hash": (
        generator["provenance"]["inventory_sha256"]
        == inventory["inventory_sha256"]
    ),
    "generator_generated_tree_hash": (
        generator["generated_tree_sha256"]
        == actual_hashes["generated_tree_sha256"]
    ),
    "generator_obligation_map_hash": (
        generator["obligation_map_sha256"] == file_hash(obligation_map_path)
    ),
    "export_result_hashes": (
        export_result["frozen_input_sha256"]
        == actual_hashes["stage1_export_sha256"]
        and export_result["stage3_discovery_manifest_sha256"]
        == actual_hashes["discovery_manifest_sha256"]
        and export_result["generated_tree_sha256"]
        == actual_hashes["generated_tree_sha256"]
        and export_result["trust_inventory_sha256"]
        == file_hash(Path("/reference/klean-generation/trust-inventory.json"))
    ),
    "stored_preflight_matches_audit_input": (
        stored_preflight == resolution["stage4_preflight"]
    ),
    "one_nonempty_domain_obligation": (
        len(source_rules) == len(obligations) == generator["obligation_count"] == 1
        and export_result["status"] == "OK"
        and stored_preflight["status"] == "PASS"
    ),
    "source_rule_is_exact_reconstructed_domain_rule": (
        source_rules == [expected_source_rule]
    ),
    "source_obligation_ordered_bijection": (
        source_ids == obligation_ids == [domain_rule["source_rule_id"]]
        and len(set(source_ids)) == len(source_ids)
        and len(set(obligation_ids)) == len(obligation_ids)
    ),
    "obligation_provenance_exact": (
        obligations[0]["source_span"]
        == {
            "start_line": domain_rule["start_line"],
            "end_line": domain_rule["end_line"],
        }
        and obligations[0]["normalized_sha256"]
        == domain_rule["normalized_sha256"]
        and obligations[0]["inventory_sha256"]
        == inventory["inventory_sha256"]
        and obligations[0]["discovery_manifest_sha256"]
        == actual_hashes["discovery_manifest_sha256"]
    ),
    "obligation_is_exact_nonvacuous_rule_translation": (
        obligations[0]["lean_conjunct"] == expected_conjunct
        and obligations[0]["lean_conjunct_sha256"]
        == klean_export.sha256_text(expected_conjunct)
        and "True" not in expected_conjunct
        and "False" not in expected_conjunct
    ),
    "target_is_exact_generated_conjunction": (
        expected_definition is not None
        and actual_target is not None
        and actual_target["definition_sha256"]
        == klean_export.sha256_text(expected_definition)
    ),
    "target_matches_generator_manifest": actual_target == generator["target"],
    "target_matches_audit_input": actual_target == resolution["target"],
    "target_matches_recorded_preflight": (
        actual_target == stored_preflight["target"]
    ),
}

result = {
    "resolved_input_sha256": resolved_digest,
    "actual_resolution_hashes": actual_hashes,
    "recorded_resolution_hashes": recorded_hashes,
    "unmounted_hash_note": {
        "lean_invocation_sha256": resolution["hashes"][
            "lean_invocation_sha256"
        ],
        "reason": (
            "The launcher did not mount the Stage 5 invocation directory; "
            "its hash is signed but cannot be recomputed from available inputs."
        ),
    },
    "stage1_file_count": len(actual_stage1_files),
    "source_rule_ids": source_ids,
    "obligation_ids": obligation_ids,
    "exact_lean_conjunct": obligations[0]["lean_conjunct"],
    "expected_target_definition": expected_definition,
    "actual_target": actual_target,
    "checks": checks,
    "all_checks_pass": all(checks.values()),
}
print(json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False))
if not result["all_checks_pass"]:
    raise SystemExit(1)
