#!/usr/bin/env python3
"""Recompute signed-resolution and Stage 4 structural bindings."""

from __future__ import annotations

import hashlib
import json
import os
import re
from pathlib import Path
from typing import Any

from tools import klean_export, pipeline_contract, stage6_resolution_contract
from tools.k_rule_inventory import inventory_verification
from tools.lemma_discovery_contract import validate_trust_boundary


AUDIT_INPUT = Path("/audit-input.json")
K_WORKSPACE = Path("/reference/k-proof")
K_AUDIT = Path("/reference/k-audit")
DISCOVERY = Path("/reference/lemma-discovery.json")
GENERATION = Path("/reference/klean-generation")
GENERATED = GENERATION / "generated"
TOOLS = Path("/reference/tools")


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def comparison(expected: Any, actual: Any) -> dict[str, Any]:
    return {
        "expected": expected,
        "actual": actual,
        "matches": expected == actual,
    }


def source_hashes(root: Path) -> dict[str, str]:
    return {
        path.relative_to(root).as_posix(): file_sha256(path)
        for path in sorted(path for path in root.rglob("*") if path.is_file())
    }


def main() -> None:
    envelope = json.loads(AUDIT_INPUT.read_text())
    resolution, resolved_digest = stage6_resolution_contract.verify_audit_input(
        envelope
    )
    expected_hashes = resolution["hashes"]
    actual_hashes = {
        "k_workspace_sha256": pipeline_contract.sha256_tree(K_WORKSPACE),
        "stage1_export_sha256": klean_export.tree_digest(K_WORKSPACE),
        "discovery_manifest_sha256": file_sha256(DISCOVERY),
        "k_audit_sha256": pipeline_contract.sha256_tree(K_AUDIT),
        "klean_generation_sha256": pipeline_contract.sha256_tree(GENERATION),
        "generated_tree_sha256": klean_export.tree_digest(GENERATED),
        "lean_workspace_sha256": None,
        "lean_invocation_sha256": None,
    }

    stage1_actual = source_hashes(K_WORKSPACE)
    inventory = inventory_verification(K_WORKSPACE)
    validated = validate_trust_boundary(K_WORKSPACE, DISCOVERY)
    input_manifest = json.loads((GENERATION / "input-manifest.json").read_text())
    generator_manifest = json.loads(
        (GENERATION / "generator-manifest.json").read_text()
    )
    export_result = json.loads((GENERATION / "export-result.json").read_text())
    recorded_preflight = json.loads((GENERATION / "preflight.json").read_text())
    toolchain_lock = json.loads(
        Path("/reference/klean-toolchain.lock.json").read_text()
    )
    obligation_map_path = GENERATED / "obligation-map.json"
    obligation_map = json.loads(obligation_map_path.read_text())
    trust_inventory_path = GENERATION / "trust-inventory.json"
    source_rules = klean_export._domain_source_rules(
        validated, actual_hashes["discovery_manifest_sha256"]
    )
    target = klean_export.target_statement(GENERATED)
    expected_target_definition = klean_export.expected_target_definition(
        obligation_map
    )

    lean_sources = sorted(GENERATED.rglob("*.lean"))
    raw_target_occurrences = []
    forbidden_occurrences: dict[str, list[str]] = {
        "sorry": [],
        "admit": [],
        "unsafe": [],
    }
    for source in lean_sources:
        text = source.read_text()
        relative = source.relative_to(GENERATED).as_posix()
        for match in re.finditer(r"(?m)^\s*def\s+targetStatement\b", text):
            raw_target_occurrences.append(f"{relative}:{text.count(chr(10), 0, match.start()) + 1}")
        for token in forbidden_occurrences:
            for match in re.finditer(rf"\b{token}\b", text):
                forbidden_occurrences[token].append(
                    f"{relative}:{text.count(chr(10), 0, match.start()) + 1}"
                )

    recorded_source_rules = obligation_map.get("source_rules")
    obligations = obligation_map.get("obligations")
    obligation_ids = (
        [entry.get("source_rule_id") for entry in obligations]
        if isinstance(obligations, list)
        else None
    )
    expected_ids = [entry["source_rule_id"] for entry in source_rules]

    sidecar_checks = {
        "exporter_sha256": comparison(
            generator_manifest.get("exporter_sha256"),
            file_sha256(TOOLS / "klean_export.py"),
        ),
        "klean_py_sha256": comparison(
            generator_manifest.get("klean_py_sha256"),
            file_sha256(TOOLS / "klean.py"),
        ),
        "obligation_map_sha256": comparison(
            generator_manifest.get("obligation_map_sha256"),
            file_sha256(obligation_map_path),
        ),
        "generated_tree_sha256": comparison(
            generator_manifest.get("generated_tree_sha256"),
            actual_hashes["generated_tree_sha256"],
        ),
        "trust_inventory_sha256": comparison(
            export_result.get("trust_inventory_sha256"),
            file_sha256(trust_inventory_path),
        ),
        "input_verification_sha256": comparison(
            input_manifest.get("verification_sha256"),
            file_sha256(K_WORKSPACE / "verification.k"),
        ),
        "input_inventory_sha256": comparison(
            input_manifest.get("inventory_sha256"),
            inventory["inventory_sha256"],
        ),
        "input_stage1_workspace_sha256": comparison(
            input_manifest.get("stage1_workspace_sha256"),
            actual_hashes["stage1_export_sha256"],
        ),
        "input_discovery_manifest_sha256": comparison(
            input_manifest.get("stage3_discovery_manifest_sha256"),
            actual_hashes["discovery_manifest_sha256"],
        ),
        "input_frozen_sha256": comparison(
            input_manifest.get("frozen_input_sha256"),
            actual_hashes["stage1_export_sha256"],
        ),
        "generator_provenance_stage1_sha256": comparison(
            generator_manifest.get("provenance", {}).get(
                "stage1_workspace_sha256"
            ),
            actual_hashes["stage1_export_sha256"],
        ),
        "generator_provenance_discovery_sha256": comparison(
            generator_manifest.get("provenance", {}).get(
                "stage3_discovery_manifest_sha256"
            ),
            actual_hashes["discovery_manifest_sha256"],
        ),
        "generator_provenance_inventory_sha256": comparison(
            generator_manifest.get("provenance", {}).get("inventory_sha256"),
            inventory["inventory_sha256"],
        ),
        "generator_toolchain_lock": comparison(
            generator_manifest.get("toolchain"), toolchain_lock
        ),
        "export_frozen_sha256": comparison(
            export_result.get("frozen_input_sha256"),
            actual_hashes["stage1_export_sha256"],
        ),
        "export_discovery_sha256": comparison(
            export_result.get("stage3_discovery_manifest_sha256"),
            actual_hashes["discovery_manifest_sha256"],
        ),
        "export_generated_tree_sha256": comparison(
            export_result.get("generated_tree_sha256"),
            actual_hashes["generated_tree_sha256"],
        ),
    }

    report = {
        "audit_input_envelope_valid": True,
        "resolved_input_sha256": comparison(
            envelope["resolved_input_sha256"], resolved_digest
        ),
        "audit_mode": comparison(resolution["mode"], os.environ.get("AUDIT_MODE")),
        "signed_resolution_hashes": {
            key: comparison(expected_hashes.get(key), actual_hashes.get(key))
            for key in expected_hashes
        },
        "stage1_source_hashes": {
            "expected_count": len(resolution["stage1_source_hashes"]),
            "actual_count": len(stage1_actual),
            "missing_paths": sorted(
                set(resolution["stage1_source_hashes"]) - set(stage1_actual)
            ),
            "extra_paths": sorted(
                set(stage1_actual) - set(resolution["stage1_source_hashes"])
            ),
            "changed_paths": sorted(
                path
                for path in (
                    set(stage1_actual) & set(resolution["stage1_source_hashes"])
                )
                if stage1_actual[path] != resolution["stage1_source_hashes"][path]
            ),
            "all_match": stage1_actual == resolution["stage1_source_hashes"],
            "actual": stage1_actual,
        },
        "selection_artifact_hashes": {
            "k_audit": comparison(
                resolution["selections"]["k_audit"]["artifact_sha256"],
                actual_hashes["k_audit_sha256"],
            ),
            "klean_generation": comparison(
                resolution["selections"]["klean_generation"]["artifact_sha256"],
                actual_hashes["klean_generation_sha256"],
            ),
        },
        "sidecar_checks": sidecar_checks,
        "classification_array_checks": {
            "definitions": comparison(
                input_manifest.get("definitions"), validated["definitions"]
            ),
            "operational_rules": comparison(
                input_manifest.get("operational_rules"),
                validated["operational_rules"],
            ),
            "proved_derived_lemmas": comparison(
                input_manifest.get("proved_derived_lemmas"),
                validated["proved_derived_lemmas"],
            ),
            "domain_source_rules": comparison(
                input_manifest.get("source_rules"), source_rules
            ),
        },
        "status_checks": {
            "export_status": comparison(
                export_result.get("status"), "KLEAN_NO_OBLIGATIONS"
            ),
            "recorded_preflight_status": comparison(
                recorded_preflight.get("status"), "KLEAN_NO_OBLIGATIONS"
            ),
            "selected_status": comparison(
                resolution["selections"]["klean_generation"]["status"],
                "KLEAN_NO_OBLIGATIONS",
            ),
            "audit_input_stage4_preflight": comparison(
                resolution["stage4_preflight"], recorded_preflight
            ),
        },
        "source_rule_obligation_bijection": {
            "independently_classified_domain_source_rules": source_rules,
            "obligation_map_source_rules": recorded_source_rules,
            "obligations": obligations,
            "expected_ids": expected_ids,
            "obligation_ids": obligation_ids,
            "source_rules_exactly_match": recorded_source_rules == source_rules,
            "ids_exactly_match_in_order": obligation_ids == expected_ids,
            "obligation_ids_unique": (
                obligation_ids is not None
                and len(obligation_ids) == len(set(obligation_ids))
            ),
            "obligation_count": len(obligations) if isinstance(obligations, list) else None,
            "manifest_obligation_count": generator_manifest.get("obligation_count"),
            "export_obligation_count": export_result.get("obligation_count"),
        },
        "fixed_target": {
            "computed_target": target,
            "expected_target_definition": expected_target_definition,
            "generator_manifest_target": generator_manifest.get("target"),
            "audit_input_target": resolution.get("target"),
            "target_declaration_occurrences": raw_target_occurrences,
            "all_target_records_exactly_match": (
                target
                == generator_manifest.get("target")
                == resolution.get("target")
            ),
        },
        "generated_forbidden_occurrences": forbidden_occurrences,
        "candidate_absent": not Path("/candidate").exists(),
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
