#!/usr/bin/env python3
"""Recompute signed-input, tree, source, manifest, and target bindings."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from pathlib import Path
from typing import Any

from tools import klean_export, klean_preflight, pipeline_contract
from tools.k_rule_inventory import inventory_verification
from tools.stage6_resolution_contract import canonical_json_sha256


AUDIT_INPUT = Path("/audit-input.json")
K_WORKSPACE = Path("/reference/k-proof")
K_AUDIT = Path("/reference/k-audit")
DISCOVERY = Path("/reference/lemma-discovery.json")
GENERATION = Path("/reference/klean-generation")
GENERATED = GENERATION / "generated"
LOCK = Path("/reference/klean-toolchain.lock.json")


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def regular_files(root: Path) -> list[Path]:
    files: list[Path] = []
    pending = [root]
    while pending:
        directory = pending.pop()
        for entry in os.scandir(directory):
            path = Path(entry.path)
            mode = entry.stat(follow_symlinks=False).st_mode
            if stat.S_ISDIR(mode):
                pending.append(path)
            elif stat.S_ISREG(mode):
                files.append(path)
            else:
                raise RuntimeError(f"linked or unsupported entry: {path}")
    return sorted(files)


def main() -> None:
    envelope = json.loads(AUDIT_INPUT.read_text())
    resolution = envelope["resolution"]
    hashes = resolution["hashes"]
    discovery = json.loads(DISCOVERY.read_text())
    inventory = inventory_verification(K_WORKSPACE)
    input_manifest = json.loads((GENERATION / "input-manifest.json").read_text())
    generator_manifest = json.loads(
        (GENERATION / "generator-manifest.json").read_text()
    )
    obligation_map = json.loads(
        (GENERATED / "obligation-map.json").read_text()
    )
    export_result = json.loads((GENERATION / "export-result.json").read_text())
    selected_preflight = json.loads((GENERATION / "preflight.json").read_text())
    trust_inventory = json.loads(
        (GENERATION / "trust-inventory.json").read_text()
    )
    lock = json.loads(LOCK.read_text())

    computed_stage1_sources = {
        path.relative_to(K_WORKSPACE).as_posix(): file_sha256(path)
        for path in regular_files(K_WORKSPACE)
    }
    computed = {
        "resolved_input_sha256": canonical_json_sha256(resolution),
        "k_workspace_sha256": pipeline_contract.sha256_tree(K_WORKSPACE),
        "stage1_export_sha256": klean_export.tree_digest(K_WORKSPACE),
        "discovery_manifest_sha256": file_sha256(DISCOVERY),
        "k_audit_sha256": pipeline_contract.sha256_tree(K_AUDIT),
        "klean_generation_sha256": pipeline_contract.sha256_tree(GENERATION),
        "generated_tree_sha256": klean_export.tree_digest(GENERATED),
        "verification_sha256": file_sha256(K_WORKSPACE / "verification.k"),
        "obligation_map_sha256": file_sha256(
            GENERATED / "obligation-map.json"
        ),
        "trust_inventory_sha256": file_sha256(
            GENERATION / "trust-inventory.json"
        ),
        "exporter_sha256": file_sha256(
            Path("/reference/tools/klean_export.py")
        ),
        "klean_py_sha256": file_sha256(Path("/reference/tools/klean.py")),
    }

    checks: dict[str, bool] = {}
    checks["audit_mode_matches_environment"] = (
        resolution["mode"] == os.environ.get("AUDIT_MODE")
    )
    checks["resolved_input_envelope_hash"] = (
        computed["resolved_input_sha256"]
        == envelope["resolved_input_sha256"]
    )
    for name in (
        "k_workspace_sha256",
        "stage1_export_sha256",
        "discovery_manifest_sha256",
        "k_audit_sha256",
        "klean_generation_sha256",
        "generated_tree_sha256",
    ):
        checks[f"audit_input_{name}"] = computed[name] == hashes[name]
    checks["audit_input_stage1_source_hashes"] = (
        computed_stage1_sources == resolution["stage1_source_hashes"]
    )
    checks["selected_k_audit_artifact_hash"] = (
        computed["k_audit_sha256"]
        == resolution["selections"]["k_audit"]["artifact_sha256"]
    )
    checks["selected_generation_artifact_hash"] = (
        computed["klean_generation_sha256"]
        == resolution["selections"]["klean_generation"]["artifact_sha256"]
    )
    checks["classification_only_null_lean_hashes"] = (
        hashes["lean_workspace_sha256"] is None
        and hashes["lean_invocation_sha256"] is None
    )
    checks["candidate_absent"] = not Path("/candidate").exists()

    checks["input_manifest_stage1_tree_hashes"] = (
        input_manifest["frozen_input_sha256"]
        == computed["stage1_export_sha256"]
        == input_manifest["stage1_workspace_sha256"]
    )
    checks["input_manifest_discovery_hash"] = (
        input_manifest["stage3_discovery_manifest_sha256"]
        == computed["discovery_manifest_sha256"]
    )
    checks["input_manifest_inventory_hash"] = (
        input_manifest["inventory_sha256"]
        == inventory["inventory_sha256"]
        == discovery["inventory_sha256"]
    )
    checks["input_manifest_verification_hash"] = (
        input_manifest["verification_sha256"]
        == computed["verification_sha256"]
        == inventory["verification_sha256"]
    )
    expected_definitions: list[dict[str, Any]] = []
    discovery_by_id = {
        entry["source_rule_id"]: entry for entry in discovery["rules"]
    }
    for rule in inventory["rules"]:
        entry = dict(rule)
        entry["classification"] = discovery_by_id[rule["source_rule_id"]][
            "classification"
        ]
        entry["rationale"] = discovery_by_id[rule["source_rule_id"]][
            "rationale"
        ]
        expected_definitions.append(entry)
    checks["input_manifest_definitions_exact"] = (
        input_manifest["definitions"] == expected_definitions
    )
    checks["input_manifest_other_class_buckets_empty"] = (
        input_manifest["source_rules"] == []
        and input_manifest["operational_rules"] == []
        and input_manifest["proved_derived_lemmas"] == []
    )

    checks["generator_generated_tree_hash"] = (
        generator_manifest["generated_tree_sha256"]
        == computed["generated_tree_sha256"]
    )
    checks["generator_obligation_map_hash"] = (
        generator_manifest["obligation_map_sha256"]
        == computed["obligation_map_sha256"]
    )
    checks["generator_toolchain_lock_exact"] = (
        generator_manifest["toolchain"] == lock
    )
    checks["generator_provenance_exact"] = (
        generator_manifest["provenance"]["stage1_workspace_sha256"]
        == computed["stage1_export_sha256"]
        and generator_manifest["provenance"][
            "stage3_discovery_manifest_sha256"
        ]
        == computed["discovery_manifest_sha256"]
        and generator_manifest["provenance"]["inventory_sha256"]
        == inventory["inventory_sha256"]
    )

    source_rules = input_manifest["source_rules"]
    obligations = obligation_map["obligations"]
    source_rule_ids = [entry["source_rule_id"] for entry in source_rules]
    obligation_rule_ids = [
        entry.get("source_rule_id") for entry in obligations
    ]
    checks["obligation_map_source_rules_exact"] = (
        obligation_map["source_rules"] == source_rules
    )
    checks["source_rule_obligation_ordered_bijection"] = (
        source_rule_ids == obligation_rule_ids
        and len(source_rule_ids) == len(set(source_rule_ids))
        and len(obligation_rule_ids) == len(set(obligation_rule_ids))
    )
    checks["genuinely_empty_generated_domain_set"] = (
        source_rules == []
        and obligations == []
        and obligation_map["trust_parameters"] == []
    )
    checks["obligation_counts_zero"] = (
        generator_manifest["obligation_count"] == 0
        and export_result["obligation_count"] == 0
        and selected_preflight["obligation_count"] == 0
    )

    actual_target = klean_export.target_statement(GENERATED)
    expected_target_definition = klean_export.expected_target_definition(
        obligation_map
    )
    checks["fixed_generated_target_absent"] = (
        actual_target is None
        and expected_target_definition is None
        and generator_manifest["target"] is None
        and resolution["target"] is None
        and selected_preflight["target"] is None
    )
    checks["no_stage5_result"] = resolution["stage5_result"] is None
    checks["no_generated_lemma_target_source"] = (
        "def Target : Prop :="
        not in (
            GENERATED / "Klean1SeparateParenGroups/Lemmas.lean"
        ).read_text()
    )

    checks["export_result_stage1_hash"] = (
        export_result["frozen_input_sha256"]
        == computed["stage1_export_sha256"]
    )
    checks["export_result_discovery_hash"] = (
        export_result["stage3_discovery_manifest_sha256"]
        == computed["discovery_manifest_sha256"]
    )
    checks["export_result_generated_tree_hash"] = (
        export_result["generated_tree_sha256"]
        == computed["generated_tree_sha256"]
    )
    checks["export_result_trust_inventory_hash"] = (
        export_result["trust_inventory_sha256"]
        == computed["trust_inventory_sha256"]
    )
    checks["export_status_no_obligations"] = (
        export_result["status"] == "KLEAN_NO_OBLIGATIONS"
        and selected_preflight["status"] == "KLEAN_NO_OBLIGATIONS"
        and resolution["selections"]["klean_generation"]["status"]
        == "KLEAN_NO_OBLIGATIONS"
    )
    checks["selected_preflight_hash_bindings"] = (
        selected_preflight["frozen_input_sha256"]
        == computed["stage1_export_sha256"]
        == selected_preflight["stage1_workspace_sha256"]
        and selected_preflight["stage3_discovery_manifest_sha256"]
        == computed["discovery_manifest_sha256"]
        and selected_preflight["generated_tree_sha256"]
        == computed["generated_tree_sha256"]
    )
    checks["audit_input_embeds_selected_preflight_exactly"] = (
        resolution["stage4_preflight"] == selected_preflight
    )
    checks["trust_inventory_counts_match_selected_preflight"] = (
        len(trust_inventory["allowlist"])
        == selected_preflight["trust_declaration_count"]
        and trust_inventory["designated_sorries"] == 0
        and trust_inventory["other_sorries"] == 0
    )
    lean_sources = klean_preflight._lean_sources(GENERATED)
    declared_trust = klean_preflight._trust_declarations(lean_sources)
    allowed_trust = {
        entry["name"]: (entry["kind"], entry["type"])
        for entry in trust_inventory["allowlist"]
    }
    checks["actual_trust_declarations_match_allowlist"] = (
        declared_trust == allowed_trust
    )
    generated_text = "\n".join(path.read_text() for path in lean_sources)
    checks["generated_has_no_proof_holes_or_unsafe"] = all(
        token not in generated_text
        for token in ("\nsorry", "\nadmit", "\nunsafe")
    )

    result = {
        "computed_hashes": computed,
        "computed_stage1_source_hashes": computed_stage1_sources,
        "counts": {
            "inventory_rules": len(inventory["rules"]),
            "definitions": len(input_manifest["definitions"]),
            "domain_source_rules": len(source_rules),
            "generated_obligations": len(obligations),
            "trust_parameters": len(obligation_map["trust_parameters"]),
            "trust_allowlist": len(trust_inventory["allowlist"]),
        },
        "target": {
            "expected_definition": expected_target_definition,
            "actual": actual_target,
            "generator_manifest": generator_manifest["target"],
            "audit_input": resolution["target"],
        },
        "generator_tool_provenance_observation": {
            "manifest_exporter_sha256": generator_manifest["exporter_sha256"],
            "current_audit_tool_exporter_sha256": computed["exporter_sha256"],
            "matches_current_audit_tool": (
                generator_manifest["exporter_sha256"]
                == computed["exporter_sha256"]
            ),
            "manifest_klean_py_sha256": generator_manifest["klean_py_sha256"],
            "current_audit_tool_klean_py_sha256": computed["klean_py_sha256"],
            "matches_current_audit_tool_klean_py": (
                generator_manifest["klean_py_sha256"]
                == computed["klean_py_sha256"]
            ),
            "note": (
                "The manifest hashes the generator-image tool sources; those "
                "source files are not mounted. The current trusted audit tools "
                "are compared transparently but are not claimed to be those files."
            ),
        },
        "checks": checks,
        "status": "PASS" if all(checks.values()) else "FAIL",
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
