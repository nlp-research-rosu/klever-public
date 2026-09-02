#!/usr/bin/env python3
"""Independent structural and hash checks for the Stage 3/4 audit."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

from tools import (
    klean_export,
    lemma_discovery_contract,
    pipeline_contract,
    stage6_resolution_contract,
)
from tools.k_rule_inventory import canonical_json_sha256, inventory_verification


ROOT_AUDIT_INPUT = Path("/audit-input.json")
WORKSPACE = Path("/reference/k-proof")
DISCOVERY = Path("/reference/lemma-discovery.json")
K_AUDIT = Path("/reference/k-audit")
GENERATION = Path("/reference/klean-generation")
GENERATED = GENERATION / "generated"
PRODUCERS = Path("/reference/generation-tools")


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_json(path: Path) -> dict:
    value = json.loads(path.read_text())
    assert isinstance(value, dict), path
    return value


def main() -> None:
    evidence = Path("/audit-output/evidence")
    audit_input = load_json(ROOT_AUDIT_INPUT)
    resolution, signed_digest = stage6_resolution_contract.verify_audit_input(
        audit_input
    )
    discovery = load_json(DISCOVERY)
    generator = load_json(GENERATION / "generator-manifest.json")
    source_manifest = load_json(PRODUCERS / "source-manifest.json")
    input_manifest = load_json(GENERATION / "input-manifest.json")
    export_result = load_json(GENERATION / "export-result.json")
    recorded_preflight = load_json(GENERATION / "preflight.json")
    obligation_map = load_json(GENERATED / "obligation-map.json")

    inventory = inventory_verification(WORKSPACE)
    (evidence / "inventory-reconstruction.json").write_text(
        json.dumps(inventory, indent=2, sort_keys=True) + "\n"
    )

    verification_lines = (WORKSPACE / "verification.k").read_text().splitlines()
    per_rule_checks: list[dict] = []
    for rule in inventory["rules"]:
        normalized = " ".join(rule["text"].split())
        normalized_sha256 = hashlib.sha256(normalized.encode()).hexdigest()
        source_rule_id = f"rule-{normalized_sha256}"
        source_span = "\n".join(
            verification_lines[rule["start_line"] - 1 : rule["end_line"]]
        )
        per_rule_checks.append(
            {
                "source_rule_id": rule["source_rule_id"],
                "source_span": {
                    "start_line": rule["start_line"],
                    "end_line": rule["end_line"],
                },
                "normalized_hash_recomputed": normalized_sha256,
                "normalized_hash_matches": (
                    normalized_sha256 == rule["normalized_sha256"]
                ),
                "source_rule_id_matches": source_rule_id == rule["source_rule_id"],
                "source_span_text_matches": source_span == rule["text"],
            }
        )

    canonical_rules_hash = canonical_json_sha256(inventory["rules"])
    canonical_ids = [rule["source_rule_id"] for rule in inventory["rules"]]
    classified_ids = [rule["source_rule_id"] for rule in discovery["rules"]]
    trust_boundary = lemma_discovery_contract.validate_trust_boundary(
        WORKSPACE, DISCOVERY
    )
    discovery_hash = sha256_file(DISCOVERY)
    expected_domain_source_rules = klean_export._domain_source_rules(
        trust_boundary, discovery_hash
    )
    inventory_comparison = {
        "verification_module": inventory["verification_module"],
        "verification_modules": inventory["verification_modules"],
        "rule_count": len(inventory["rules"]),
        "manifest_rule_count": len(discovery["rules"]),
        "manifest_ids_unique": len(classified_ids) == len(set(classified_ids)),
        "ids_exact_order_match": classified_ids == canonical_ids,
        "missing_ids": [value for value in canonical_ids if value not in classified_ids],
        "extra_ids": [value for value in classified_ids if value not in canonical_ids],
        "inventory_hash_recomputed": canonical_rules_hash,
        "inventory_hash_tool": inventory["inventory_sha256"],
        "inventory_hash_manifest": discovery["inventory_sha256"],
        "inventory_hash_all_match": (
            canonical_rules_hash
            == inventory["inventory_sha256"]
            == discovery["inventory_sha256"]
        ),
        "verification_sha256": inventory["verification_sha256"],
        "per_rule_checks": per_rule_checks,
        "contract_definition_count": len(trust_boundary["definitions"]),
        "contract_operational_rule_count": len(
            trust_boundary["operational_rules"]
        ),
        "contract_proved_derived_lemma_count": len(
            trust_boundary["proved_derived_lemmas"]
        ),
        "contract_domain_lemma_count": len(trust_boundary["domain_lemmas"]),
    }
    (evidence / "inventory-comparison.json").write_text(
        json.dumps(inventory_comparison, indent=2, sort_keys=True) + "\n"
    )

    producer_observed = {
        name: sha256_file(PRODUCERS / name)
        for name in ("klean_export.py", "klean.py")
    }
    producer_expected = {
        "klean_export.py": generator["exporter_sha256"],
        "klean.py": generator["klean_py_sha256"],
    }
    image_id = generator["provenance"]["generator_image_id"]
    audit_image_key = Path(
        resolution["generation_producer_sources"]
    ).name
    producer_authentication = {
        "observed_file_hashes": producer_observed,
        "generator_manifest_file_hashes": producer_expected,
        "source_manifest_file_hashes": source_manifest["files"],
        "all_file_hashes_match": (
            producer_observed == producer_expected == source_manifest["files"]
        ),
        "generator_manifest_image_id": image_id,
        "source_manifest_image_id": source_manifest["generator_image_id"],
        "audit_input_producer_path_basename": audit_image_key,
        "image_id_all_match": (
            image_id == source_manifest["generator_image_id"]
            and image_id == f"sha256:{audit_image_key}"
        ),
        "producer_tree_sha256": pipeline_contract.sha256_tree(PRODUCERS),
        "producer_tree_sha256_audit_input": resolution["hashes"][
            "generation_producer_sources_sha256"
        ],
    }
    producer_authentication["producer_tree_hash_matches"] = (
        producer_authentication["producer_tree_sha256"]
        == producer_authentication["producer_tree_sha256_audit_input"]
    )
    (evidence / "producer-authentication.json").write_text(
        json.dumps(producer_authentication, indent=2, sort_keys=True) + "\n"
    )

    stage1_source_hashes = {
        path.relative_to(WORKSPACE).as_posix(): pipeline_contract.sha256_file(path)
        for path in pipeline_contract._walk_regular_files(
            WORKSPACE, "Stage 1 source workspace"
        )
    }
    observed_hashes = {
        "k_workspace_sha256": pipeline_contract.sha256_tree(WORKSPACE),
        "stage1_export_sha256": klean_export.tree_digest(WORKSPACE),
        "discovery_manifest_sha256": sha256_file(DISCOVERY),
        "k_audit_sha256": pipeline_contract.sha256_tree(K_AUDIT),
        "klean_generation_sha256": pipeline_contract.sha256_tree(GENERATION),
        "generation_producer_sources_sha256": pipeline_contract.sha256_tree(
            PRODUCERS
        ),
        "generated_tree_sha256": klean_export.tree_digest(GENERATED),
        "lean_workspace_sha256": None,
        "lean_invocation_sha256": None,
    }
    hash_checks = {
        "signed_resolution_digest_recomputed": signed_digest,
        "signed_resolution_digest_recorded": audit_input["resolved_input_sha256"],
        "signed_resolution_digest_matches": (
            signed_digest == audit_input["resolved_input_sha256"]
        ),
        "observed_resolution_hashes": observed_hashes,
        "recorded_resolution_hashes": resolution["hashes"],
        "resolution_hashes_match": observed_hashes == resolution["hashes"],
        "stage1_source_hashes_match": (
            stage1_source_hashes == resolution["stage1_source_hashes"]
        ),
        "observed_stage1_source_hashes": stage1_source_hashes,
        "selection_k_audit_hash_matches": (
            observed_hashes["k_audit_sha256"]
            == resolution["selections"]["k_audit"]["artifact_sha256"]
        ),
        "selection_generation_hash_matches": (
            observed_hashes["klean_generation_sha256"]
            == resolution["selections"]["klean_generation"]["artifact_sha256"]
        ),
        "generator_generated_tree_hash_matches": (
            observed_hashes["generated_tree_sha256"]
            == generator["generated_tree_sha256"]
        ),
        "input_stage1_tree_hash_matches": (
            observed_hashes["stage1_export_sha256"]
            == input_manifest["stage1_workspace_sha256"]
            == input_manifest["frozen_input_sha256"]
        ),
        "discovery_hash_matches_manifests": (
            observed_hashes["discovery_manifest_sha256"]
            == input_manifest["stage3_discovery_manifest_sha256"]
            == generator["provenance"]["stage3_discovery_manifest_sha256"]
            == export_result["stage3_discovery_manifest_sha256"]
        ),
        "recorded_preflight_exactly_matches_audit_input": (
            recorded_preflight == resolution["stage4_preflight"]
        ),
        "root_and_output_audit_input_identical": (
            ROOT_AUDIT_INPUT.read_bytes()
            == Path("/audit-output/audit-input.json").read_bytes()
        ),
    }
    (evidence / "hash-verification.json").write_text(
        json.dumps(hash_checks, indent=2, sort_keys=True) + "\n"
    )

    obligations = obligation_map.get("obligations")
    source_rules = obligation_map.get("source_rules")
    target = klean_export.target_statement(GENERATED)
    expected_target = klean_export.expected_target_definition(obligation_map)
    definition_resolution = klean_export.resolve_definition_closure(WORKSPACE)
    observed_required_relatives = [
        path.relative_to(WORKSPACE.resolve()).as_posix()
        for path in definition_resolution.required_files
    ]
    recorded_required_relatives = [
        value.removeprefix("/frozen-k/")
        for value in input_manifest["required_k_files"]
    ]
    trust_inventory_hash = sha256_file(
        GENERATION / "trust-inventory.json"
    )
    lock = load_json(Path("/reference/klean-toolchain.lock.json"))
    structural = {
        "audit_mode_env": os.environ.get("AUDIT_MODE"),
        "audit_mode_signed": resolution["mode"],
        "selected_status": resolution["selections"]["klean_generation"]["status"],
        "manifest_status": export_result["status"],
        "input_manifest_source_rule_count": len(input_manifest["source_rules"]),
        "input_manifest_definitions_exact": (
            input_manifest["definitions"] == trust_boundary["definitions"]
        ),
        "input_manifest_operational_rules_exact": (
            input_manifest["operational_rules"]
            == trust_boundary["operational_rules"]
        ),
        "input_manifest_proved_derived_lemmas_exact": (
            input_manifest["proved_derived_lemmas"]
            == trust_boundary["proved_derived_lemmas"]
        ),
        "input_manifest_domain_source_rules_exact": (
            input_manifest["source_rules"] == expected_domain_source_rules
        ),
        "obligation_map_domain_source_rules_exact": (
            source_rules == expected_domain_source_rules
        ),
        "input_inventory_hash_matches_reconstruction": (
            input_manifest["inventory_sha256"]
            == inventory["inventory_sha256"]
        ),
        "generator_inventory_hash_matches_reconstruction": (
            generator["provenance"]["inventory_sha256"]
            == inventory["inventory_sha256"]
        ),
        "input_verification_hash_matches_reconstruction": (
            input_manifest["verification_sha256"]
            == inventory["verification_sha256"]
        ),
        "input_verification_module_matches_reconstruction": (
            input_manifest["verification_module"]
            == inventory["verification_module"]
            == definition_resolution.verification_module
        ),
        "input_syntax_module_matches_resolution": (
            input_manifest["syntax_module"]
            == definition_resolution.syntax_module
        ),
        "required_k_file_closure_exact": (
            recorded_required_relatives == observed_required_relatives
        ),
        "required_k_file_count": len(observed_required_relatives),
        "obligation_map_source_rule_count": len(source_rules),
        "obligation_count": len(obligations),
        "source_rule_ids": [item["source_rule_id"] for item in source_rules],
        "obligation_source_rule_ids": [
            item["source_rule_id"] for item in obligations
        ],
        "source_ids_unique": (
            len(source_rules)
            == len({item["source_rule_id"] for item in source_rules})
        ),
        "obligation_ids_unique": (
            len(obligations)
            == len({item["source_rule_id"] for item in obligations})
        ),
        "obligation_map_sha256_observed": sha256_file(
            GENERATED / "obligation-map.json"
        ),
        "obligation_map_sha256_manifest": generator["obligation_map_sha256"],
        "generator_obligation_count": generator["obligation_count"],
        "export_obligation_count": export_result["obligation_count"],
        "recorded_preflight_obligation_count": recorded_preflight[
            "obligation_count"
        ],
        "generator_toolchain_matches_lock": generator["toolchain"] == lock,
        "generator_stage1_hash_matches": (
            generator["provenance"]["stage1_workspace_sha256"]
            == observed_hashes["stage1_export_sha256"]
        ),
        "export_stage1_hash_matches": (
            export_result["frozen_input_sha256"]
            == observed_hashes["stage1_export_sha256"]
        ),
        "export_generated_tree_hash_matches": (
            export_result["generated_tree_sha256"]
            == observed_hashes["generated_tree_sha256"]
        ),
        "export_trust_inventory_hash_observed": trust_inventory_hash,
        "export_trust_inventory_hash_recorded": export_result[
            "trust_inventory_sha256"
        ],
        "export_trust_inventory_hash_matches": (
            trust_inventory_hash == export_result["trust_inventory_sha256"]
        ),
        "preflight_exactly_matches_successful_rerun": (
            recorded_preflight
            == load_json(evidence / "preflight-rerun-success.json")
        ),
        "target_statement_observed": target,
        "target_definition_expected": expected_target,
        "generator_target": generator["target"],
        "audit_input_target": resolution["target"],
        "preflight_target": recorded_preflight["target"],
        "candidate_path_exists": Path("/candidate").exists(),
        "all_manifest_bijection_and_provenance_checks_hold": (
            input_manifest["definitions"] == trust_boundary["definitions"]
            and input_manifest["operational_rules"]
            == trust_boundary["operational_rules"]
            and input_manifest["proved_derived_lemmas"]
            == trust_boundary["proved_derived_lemmas"]
            and input_manifest["source_rules"] == expected_domain_source_rules
            and source_rules == expected_domain_source_rules
            and input_manifest["inventory_sha256"]
            == inventory["inventory_sha256"]
            and generator["provenance"]["inventory_sha256"]
            == inventory["inventory_sha256"]
            and input_manifest["verification_sha256"]
            == inventory["verification_sha256"]
            and input_manifest["verification_module"]
            == inventory["verification_module"]
            == definition_resolution.verification_module
            and input_manifest["syntax_module"]
            == definition_resolution.syntax_module
            and recorded_required_relatives == observed_required_relatives
            and generator["toolchain"] == lock
            and generator["provenance"]["stage1_workspace_sha256"]
            == observed_hashes["stage1_export_sha256"]
            and export_result["frozen_input_sha256"]
            == observed_hashes["stage1_export_sha256"]
            and export_result["generated_tree_sha256"]
            == observed_hashes["generated_tree_sha256"]
            and trust_inventory_hash == export_result[
                "trust_inventory_sha256"
            ]
            and recorded_preflight
            == load_json(evidence / "preflight-rerun-success.json")
        ),
        "all_zero_obligation_target_conditions_hold": (
            not input_manifest["source_rules"]
            and not source_rules
            and not obligations
            and generator["obligation_count"] == 0
            and export_result["obligation_count"] == 0
            and recorded_preflight["obligation_count"] == 0
            and target is None
            and expected_target is None
            and generator["target"] is None
            and resolution["target"] is None
            and recorded_preflight["target"] is None
            and not Path("/candidate").exists()
        ),
    }
    (evidence / "stage4-structural-checks.json").write_text(
        json.dumps(structural, indent=2, sort_keys=True) + "\n"
    )

    print(
        json.dumps(
            {
                "inventory_comparison": inventory_comparison,
                "producer_authentication": producer_authentication,
                "hash_summary": {
                    key: value
                    for key, value in hash_checks.items()
                    if not isinstance(value, dict)
                },
                "stage4_structural_checks": structural,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
