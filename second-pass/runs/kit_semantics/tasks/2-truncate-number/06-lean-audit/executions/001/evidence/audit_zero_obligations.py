#!/usr/bin/env python3
"""Independent Stage 4 identity and zero-obligation consistency checks."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

from tools import klean_export
from tools.k_rule_inventory import inventory_verification
from tools.lemma_discovery_contract import validate_trust_boundary


K_PROOF = Path("/reference/k-proof")
DISCOVERY = Path("/reference/lemma-discovery.json")
GENERATION = Path("/reference/klean-generation")
GENERATED = GENERATION / "generated"
AUDIT_INPUT = Path("/audit-input.json")


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    inventory = inventory_verification(K_PROOF)
    classified = validate_trust_boundary(K_PROOF, DISCOVERY)
    audit = json.loads(AUDIT_INPUT.read_text())["resolution"]
    input_manifest = json.loads((GENERATION / "input-manifest.json").read_text())
    generator = json.loads((GENERATION / "generator-manifest.json").read_text())
    export_result = json.loads((GENERATION / "export-result.json").read_text())
    preflight = json.loads((GENERATION / "preflight.json").read_text())
    toolchain_lock = json.loads(
        Path("/reference/klean-toolchain.lock.json").read_text()
    )
    obligation_map_path = GENERATED / "obligation-map.json"
    obligation_map = json.loads(obligation_map_path.read_text())

    source_rule_sets = {
        "canonical_inventory": inventory["rules"],
        "classified_domain_lemmas": classified["domain_lemmas"],
        "input_manifest_source_rules": input_manifest["source_rules"],
        "obligation_map_source_rules": obligation_map["source_rules"],
    }
    source_id_lists = {
        name: [entry["source_rule_id"] for entry in entries]
        for name, entries in source_rule_sets.items()
    }
    obligation_ids = [
        entry["source_rule_id"] for entry in obligation_map["obligations"]
    ]
    expected_definition = klean_export.expected_target_definition(
        obligation_map
    )
    observed_target = klean_export.target_statement(GENERATED)

    checks = {
        "all_canonical_rules_classified": len(inventory["rules"])
        == sum(
            len(classified[name])
            for name in (
                "definitions",
                "operational_rules",
                "proved_derived_lemmas",
                "domain_lemmas",
            )
        ),
        "canonical_rule_ids_unique": len(source_id_lists["canonical_inventory"])
        == len(set(source_id_lists["canonical_inventory"])),
        "domain_source_ids_unique": len(
            source_id_lists["classified_domain_lemmas"]
        )
        == len(set(source_id_lists["classified_domain_lemmas"])),
        "obligation_ids_unique": len(obligation_ids)
        == len(set(obligation_ids)),
        "domain_to_input_bijection": source_id_lists[
            "classified_domain_lemmas"
        ]
        == source_id_lists["input_manifest_source_rules"],
        "domain_to_map_source_bijection": source_id_lists[
            "classified_domain_lemmas"
        ]
        == source_id_lists["obligation_map_source_rules"],
        "domain_to_obligation_bijection": source_id_lists[
            "classified_domain_lemmas"
        ]
        == obligation_ids,
        "domain_set_genuinely_empty": not classified["domain_lemmas"],
        "obligations_genuinely_empty": not obligation_map["obligations"],
        "trust_parameters_empty": not obligation_map["trust_parameters"],
        "expected_target_absent": expected_definition is None,
        "observed_target_absent": observed_target is None,
        "generator_target_absent": generator["target"] is None,
        "audit_input_target_absent": audit["target"] is None,
        "generator_obligation_count_zero": generator["obligation_count"] == 0,
        "export_obligation_count_zero": export_result["obligation_count"] == 0,
        "export_status_no_obligations": export_result["status"]
        == "KLEAN_NO_OBLIGATIONS",
        "recorded_preflight_status_no_obligations": preflight["status"]
        == "KLEAN_NO_OBLIGATIONS",
        "selected_status_no_obligations": audit["selections"][
            "klean_generation"
        ]["status"]
        == "KLEAN_NO_OBLIGATIONS",
        "audit_mode_classification_only": audit["mode"]
        == "CLASSIFICATION_ONLY",
        "no_candidate_mount": not Path("/candidate").exists(),
        "no_stage5_paths": audit["lean_workspace"] is None
        and audit["lean_invocation"] is None,
        "obligation_map_hash_matches": sha256_file(obligation_map_path)
        == generator["obligation_map_sha256"],
        "trust_inventory_hash_matches": sha256_file(
            GENERATION / "trust-inventory.json"
        )
        == export_result["trust_inventory_sha256"],
        "generator_toolchain_matches_lock": generator["toolchain"]
        == toolchain_lock,
        "recorded_preflight_matches_audit_input": preflight
        == audit["stage4_preflight"],
        "inventory_hash_matches_generator": inventory["inventory_sha256"]
        == generator["provenance"]["inventory_sha256"],
        "inventory_hash_matches_input": inventory["inventory_sha256"]
        == input_manifest["inventory_sha256"],
        "verification_hash_matches_input": inventory["verification_sha256"]
        == input_manifest["verification_sha256"],
        "export_stage1_hash_matches_audit": export_result[
            "frozen_input_sha256"
        ]
        == audit["hashes"]["stage1_export_sha256"],
        "export_discovery_hash_matches_audit": export_result[
            "stage3_discovery_manifest_sha256"
        ]
        == audit["hashes"]["discovery_manifest_sha256"],
        "export_generated_hash_matches_audit": export_result[
            "generated_tree_sha256"
        ]
        == audit["hashes"]["generated_tree_sha256"],
    }
    result = {
        "checks": checks,
        "source_id_lists": source_id_lists,
        "obligation_ids": obligation_ids,
        "expected_target_definition": expected_definition,
        "observed_target": observed_target,
        "all_pass": all(checks.values()),
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["all_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
