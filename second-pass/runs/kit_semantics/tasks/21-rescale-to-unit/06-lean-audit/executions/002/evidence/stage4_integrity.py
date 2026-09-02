#!/usr/bin/env python3
"""Read-only independent hash, bijection, and target-identity checks."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from tools import klean_export, pipeline_contract
from tools.k_rule_inventory import inventory_verification


def load(path: str) -> dict:
    return json.loads(Path(path).read_text())


def file_sha256(path: str) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


audit = load("/audit-input.json")["resolution"]
source_manifest = load("/reference/generation-tools/source-manifest.json")
discovery = load("/reference/lemma-discovery.json")
generator = load("/reference/klean-generation/generator-manifest.json")
input_manifest = load("/reference/klean-generation/input-manifest.json")
export_result = load("/reference/klean-generation/export-result.json")
obligation_map = load(
    "/reference/klean-generation/generated/obligation-map.json"
)
inventory = inventory_verification(Path("/reference/k-proof"))

discovery_by_id = {
    entry["source_rule_id"]: entry for entry in discovery["rules"]
}
independent_true_domain_ids = [
    "rule-57727b2acd45f64e74f4c2582f643b13345834dfbe7bf3fe97580d59dcd8ba43",
    "rule-dc58f41e482527dda6d5bd7e29f533ee71f5356475fa5bfad6f9142925059957",
]
expected_source_rules = []
for rule in inventory["rules"]:
    if rule["source_rule_id"] not in independent_true_domain_ids:
        continue
    classified = discovery_by_id[rule["source_rule_id"]]
    expected_source_rules.append(
        {
            **rule,
            "classification": "DOMAIN_LEMMA",
            "rationale": classified["rationale"],
            "inventory_sha256": inventory["inventory_sha256"],
            "discovery_manifest_sha256": file_sha256(
                "/reference/lemma-discovery.json"
            ),
        }
    )

expected_image = source_manifest["generator_image_id"]
launcher_image = (
    "sha256:"
    + Path(audit["generation_producer_sources"]).name
)
actual_target = klean_export.target_statement(
    Path("/reference/klean-generation/generated")
)
expected_definition = klean_export.expected_target_definition(obligation_map)
obligations = obligation_map["obligations"]
obligation_ids = [entry["source_rule_id"] for entry in obligations]

checks = {
    "exporter_file_matches_source_manifest": (
        file_sha256("/reference/generation-tools/klean_export.py")
        == source_manifest["files"]["klean_export.py"]
    ),
    "klean_file_matches_source_manifest": (
        file_sha256("/reference/generation-tools/klean.py")
        == source_manifest["files"]["klean.py"]
    ),
    "exporter_file_matches_generator_manifest": (
        file_sha256("/reference/generation-tools/klean_export.py")
        == generator["exporter_sha256"]
    ),
    "klean_file_matches_generator_manifest": (
        file_sha256("/reference/generation-tools/klean.py")
        == generator["klean_py_sha256"]
    ),
    "producer_tree_matches_audit_input": (
        pipeline_contract.sha256_tree(
            Path("/reference/generation-tools")
        )
        == audit["hashes"]["generation_producer_sources_sha256"]
    ),
    "generator_image_matches_source_manifest_and_audit_input": (
        generator["provenance"]["generator_image_id"]
        == expected_image
        == launcher_image
    ),
    "stage1_export_tree_matches_all_records": (
        klean_export.tree_digest(Path("/reference/k-proof"))
        == audit["hashes"]["stage1_export_sha256"]
        == input_manifest["frozen_input_sha256"]
        == input_manifest["stage1_workspace_sha256"]
        == generator["provenance"]["stage1_workspace_sha256"]
        == export_result["frozen_input_sha256"]
    ),
    "stage1_full_tree_matches_audit_input": (
        pipeline_contract.sha256_tree(Path("/reference/k-proof"))
        == audit["hashes"]["k_workspace_sha256"]
    ),
    "discovery_file_matches_all_records": (
        file_sha256("/reference/lemma-discovery.json")
        == audit["hashes"]["discovery_manifest_sha256"]
        == input_manifest["stage3_discovery_manifest_sha256"]
        == generator["provenance"][
            "stage3_discovery_manifest_sha256"
        ]
        == export_result["stage3_discovery_manifest_sha256"]
    ),
    "inventory_hash_matches_all_records": (
        inventory["inventory_sha256"]
        == discovery["inventory_sha256"]
        == input_manifest["inventory_sha256"]
        == generator["provenance"]["inventory_sha256"]
    ),
    "generated_tree_matches_all_records": (
        klean_export.tree_digest(
            Path("/reference/klean-generation/generated")
        )
        == audit["hashes"]["generated_tree_sha256"]
        == generator["generated_tree_sha256"]
        == export_result["generated_tree_sha256"]
    ),
    "generation_full_tree_matches_audit_input": (
        pipeline_contract.sha256_tree(
            Path("/reference/klean-generation")
        )
        == audit["hashes"]["klean_generation_sha256"]
    ),
    "true_domain_set_nonempty_and_exact": (
        independent_true_domain_ids
        == [
            entry["source_rule_id"]
            for entry in expected_source_rules
        ]
        and len(independent_true_domain_ids) == 2
    ),
    "input_source_rules_exact": (
        input_manifest["source_rules"] == expected_source_rules
    ),
    "obligation_map_source_rules_exact": (
        obligation_map["source_rules"] == expected_source_rules
    ),
    "obligation_ids_exact_order_no_duplicates": (
        obligation_ids == independent_true_domain_ids
        and len(set(obligation_ids)) == len(obligation_ids)
    ),
    "obligation_provenance_exact": all(
        obligation["source_span"]
        == {
            "start_line": source_rule["start_line"],
            "end_line": source_rule["end_line"],
        }
        and obligation["normalized_sha256"]
        == source_rule["normalized_sha256"]
        and obligation["inventory_sha256"]
        == source_rule["inventory_sha256"]
        and obligation["discovery_manifest_sha256"]
        == source_rule["discovery_manifest_sha256"]
        and obligation["lean_conjunct_sha256"]
        == hashlib.sha256(
            obligation["lean_conjunct"].encode()
        ).hexdigest()
        for obligation, source_rule in zip(
            obligations, expected_source_rules, strict=True
        )
    ),
    "obligation_map_hash_matches_generator": (
        file_sha256(
            "/reference/klean-generation/generated/obligation-map.json"
        )
        == generator["obligation_map_sha256"]
    ),
    "obligation_counts_and_status_exact": (
        len(obligations)
        == generator["obligation_count"]
        == export_result["obligation_count"]
        == 2
        and export_result["status"] == "OK"
    ),
    "target_definition_is_exact_generated_conjunction": (
        expected_definition is not None
        and actual_target is not None
        and hashlib.sha256(
            expected_definition.encode()
        ).hexdigest()
        == actual_target["definition_sha256"]
    ),
    "target_matches_generator_manifest": (
        actual_target == generator["target"]
    ),
    "target_matches_both_audit_input_records": (
        actual_target == audit["stage4_preflight"]["target"]
        == audit["target"]
    ),
    "preflight_status_and_counts_match": (
        audit["stage4_preflight"]["status"] == "PASS"
        and audit["stage4_preflight"]["obligation_count"]
        == len(obligations)
    ),
}

print("HASHES")
for path in (
    "/reference/generation-tools/klean_export.py",
    "/reference/generation-tools/klean.py",
    "/reference/generation-tools/source-manifest.json",
    "/reference/lemma-discovery.json",
    "/reference/klean-generation/generator-manifest.json",
    "/reference/klean-generation/generated/obligation-map.json",
    "/reference/klean-generation/trust-inventory.json",
):
    print(f"{file_sha256(path)}  {path}")
print(
    pipeline_contract.sha256_tree(
        Path("/reference/generation-tools")
    ),
    " /reference/generation-tools [pipeline tree]",
)
print(
    klean_export.tree_digest(Path("/reference/k-proof")),
    " /reference/k-proof [export tree]",
)
print(
    pipeline_contract.sha256_tree(Path("/reference/k-proof")),
    " /reference/k-proof [full tree]",
)
print(
    klean_export.tree_digest(
        Path("/reference/klean-generation/generated")
    ),
    " /reference/klean-generation/generated [export tree]",
)
print(
    pipeline_contract.sha256_tree(
        Path("/reference/klean-generation")
    ),
    " /reference/klean-generation [full tree]",
)
print()
print("CHECKS")
for name, result in checks.items():
    print(f"{name}: {result}")
print()
print("INDEPENDENT_TRUE_DOMAIN_IDS")
print(json.dumps(independent_true_domain_ids, indent=2))
print()
print("OBLIGATIONS")
print(json.dumps(obligations, indent=2, sort_keys=True, ensure_ascii=False))
print()
print("EXPECTED_TARGET_DEFINITION")
print(expected_definition)
print()
print("ACTUAL_TARGET_METADATA")
print(json.dumps(actual_target, indent=2, sort_keys=True, ensure_ascii=False))
print()
print("ALL_INTEGRITY_CHECKS_PASS:", all(checks.values()))
