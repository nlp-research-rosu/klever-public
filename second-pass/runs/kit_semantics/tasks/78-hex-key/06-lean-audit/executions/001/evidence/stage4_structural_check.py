#!/usr/bin/env python3
"""Independent Stage 4 manifest, obligation, and null-target checks."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

from tools import k_rule_inventory, klean_export


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


generation = Path("/reference/klean-generation")
generated = generation / "generated"
frozen = Path("/reference/k-proof")
discovery_path = Path("/reference/lemma-discovery.json")

audit = load(Path("/audit-input.json"))
resolution = audit["resolution"]
discovery = load(discovery_path)
inventory = k_rule_inventory.inventory_verification(frozen)
input_manifest = load(generation / "input-manifest.json")
generator_manifest = load(generation / "generator-manifest.json")
export_result = load(generation / "export-result.json")
recorded_preflight = load(generation / "preflight.json")
trust_inventory = load(generation / "trust-inventory.json")
obligation_map_path = generated / "obligation-map.json"
obligation_map = load(obligation_map_path)
toolchain_lock = load(Path("/reference/klean-toolchain.lock.json"))

classified_by_id = {
    item["source_rule_id"]: item for item in discovery["rules"]
}
expected_definitions = []
for rule in inventory["rules"]:
    item = dict(rule)
    classification = classified_by_id[rule["source_rule_id"]]
    item["classification"] = classification["classification"]
    item["rationale"] = classification["rationale"]
    expected_definitions.append(item)

# This set comes from the independent mathematical reclassification documented
# in REVIEW.md, not from the discovery manifest.
independently_classified_domain_ids: list[str] = []
source_rules = input_manifest.get("source_rules")
obligations = obligation_map.get("obligations")
obligation_ids = [item.get("source_rule_id") for item in obligations]

target_from_sources = klean_export.target_statement(generated)
expected_target_definition = klean_export.expected_target_definition(
    obligation_map
)

lean_declarations = []
for source in sorted(generated.rglob("*.lean")):
    text = source.read_text(encoding="utf-8")
    for match in re.finditer(
        r"(?m)^\s*(theorem|lemma)\s+([^\s:(]+)", text
    ):
        lean_declarations.append(
            {
                "file": source.relative_to(generated).as_posix(),
                "kind": match.group(1),
                "name": match.group(2),
            }
        )

checks = {
    "input_inventory_hash_matches_reconstruction": (
        input_manifest.get("inventory_sha256")
        == inventory["inventory_sha256"]
    ),
    "input_definitions_exactly_match_inventory_and_classification": (
        input_manifest.get("definitions") == expected_definitions
    ),
    "input_source_rules_match_independent_domain_set": (
        source_rules == []
        and independently_classified_domain_ids == []
    ),
    "obligation_map_source_rules_exact": (
        obligation_map.get("source_rules") == source_rules == []
    ),
    "obligation_ids_exact_order_and_unique": (
        obligation_ids == independently_classified_domain_ids
        and len(obligation_ids) == len(set(obligation_ids))
    ),
    "no_obligations": obligations == [],
    "no_trust_parameters": obligation_map.get("trust_parameters") == [],
    "obligation_count_consistent": (
        generator_manifest.get("obligation_count")
        == export_result.get("obligation_count")
        == recorded_preflight.get("obligation_count")
        == 0
    ),
    "obligation_map_hash_matches": (
        generator_manifest.get("obligation_map_sha256")
        == sha256_file(obligation_map_path)
    ),
    "target_parser_returns_none": target_from_sources is None,
    "expected_target_definition_is_none": expected_target_definition is None,
    "all_recorded_targets_are_none": (
        generator_manifest.get("target") is None
        and recorded_preflight.get("target") is None
        and resolution.get("target") is None
    ),
    "no_lean_theorem_or_lemma_declarations": lean_declarations == [],
    "status_is_no_obligations": (
        export_result.get("status") == "KLEAN_NO_OBLIGATIONS"
        and resolution["selections"]["klean_generation"].get("status")
        == "KLEAN_NO_OBLIGATIONS"
    ),
    "toolchain_matches_lock": (
        generator_manifest.get("toolchain") == toolchain_lock
    ),
    "stage1_hash_bindings_match": (
        input_manifest.get("frozen_input_sha256")
        == input_manifest.get("stage1_workspace_sha256")
        == generator_manifest.get("provenance", {}).get(
            "stage1_workspace_sha256"
        )
        == export_result.get("frozen_input_sha256")
        == klean_export.tree_digest(frozen)
    ),
    "discovery_hash_bindings_match": (
        input_manifest.get("stage3_discovery_manifest_sha256")
        == generator_manifest.get("provenance", {}).get(
            "stage3_discovery_manifest_sha256"
        )
        == export_result.get("stage3_discovery_manifest_sha256")
        == sha256_file(discovery_path)
    ),
    "inventory_provenance_matches": (
        generator_manifest.get("provenance", {}).get("inventory_sha256")
        == input_manifest.get("inventory_sha256")
        == inventory["inventory_sha256"]
    ),
    "generated_tree_bindings_match": (
        generator_manifest.get("generated_tree_sha256")
        == export_result.get("generated_tree_sha256")
        == klean_export.tree_digest(generated)
    ),
    "trust_inventory_hash_matches_export": (
        export_result.get("trust_inventory_sha256")
        == sha256_file(generation / "trust-inventory.json")
    ),
    "no_candidate_in_classification_only_mode": (
        resolution.get("mode") == "CLASSIFICATION_ONLY"
        and not Path("/candidate").exists()
    ),
}

report = {
    "independently_classified_domain_ids": independently_classified_domain_ids,
    "source_rules": source_rules,
    "obligations": obligations,
    "obligation_ids": obligation_ids,
    "target_from_sources": target_from_sources,
    "expected_target_definition": expected_target_definition,
    "lean_theorem_or_lemma_declarations": lean_declarations,
    "checks": checks,
    "ALL_CHECKS_PASS": all(checks.values()),
    "trust_inventory_declaration_count": len(trust_inventory.get("allowlist", [])),
}
print(json.dumps(report, indent=2, sort_keys=True))
