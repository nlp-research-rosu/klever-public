#!/usr/bin/env python3
"""Independent read-only structural checks for the Stage 3/4 audit."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from typing import Any

from tools import klean_export
from tools import pipeline_contract
from tools import stage6_resolution_contract
from tools.k_rule_inventory import canonical_json_sha256, inventory_verification


K_PROOF = Path("/reference/k-proof")
K_AUDIT = Path("/reference/k-audit")
DISCOVERY = Path("/reference/lemma-discovery.json")
GENERATION = Path("/reference/klean-generation")
GENERATED = GENERATION / "generated"
AUDIT_INPUT = Path("/audit-input.json")
TOOLCHAIN_LOCK = Path("/reference/klean-toolchain.lock.json")


def load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text())
    if not isinstance(value, dict):
        raise AssertionError(f"expected JSON object: {path}")
    return value


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def regular_file_hashes(root: Path) -> dict[str, str]:
    hashes: dict[str, str] = {}
    for directory, directory_names, file_names in os.walk(root):
        directory_names.sort()
        file_names.sort()
        base = Path(directory)
        for name in file_names:
            path = base / name
            if path.is_symlink() or not path.is_file():
                raise AssertionError(f"non-regular tree entry: {path}")
            relative = path.relative_to(root).as_posix()
            hashes[relative] = sha256_file(path)
    return hashes


def check(condition: bool, label: str, checks: dict[str, bool]) -> None:
    checks[label] = bool(condition)
    if not condition:
        raise AssertionError(label)


def main() -> None:
    checks: dict[str, bool] = {}
    audit_envelope = load(AUDIT_INPUT)
    resolution, resolved_digest = stage6_resolution_contract.verify_audit_input(
        audit_envelope
    )
    check(
        resolved_digest == audit_envelope["resolved_input_sha256"],
        "signed audit resolution digest",
        checks,
    )
    check(
        resolution["mode"] == os.environ.get("AUDIT_MODE")
        == "CLASSIFICATION_ONLY",
        "launcher mode and AUDIT_MODE agree",
        checks,
    )
    check(
        resolution["semantics_mode"] == "GENERATED_SEMANTICS",
        "semantics mode is GENERATED_SEMANTICS",
        checks,
    )
    check(
        resolution["problem_id"] == "136-largest-smallest-integers"
        and resolution["condition"] == "bare",
        "problem and condition identity",
        checks,
    )

    inventory = inventory_verification(K_PROOF)
    discovery = load(DISCOVERY)
    inventory_rules = inventory["rules"]
    discovery_rules = discovery["rules"]
    inventory_ids = [rule["source_rule_id"] for rule in inventory_rules]
    discovery_ids = [rule["source_rule_id"] for rule in discovery_rules]

    check(len(inventory_rules) == 11, "canonical inventory has 11 rules", checks)
    check(
        len(inventory_ids) == len(set(inventory_ids)),
        "canonical inventory IDs are unique",
        checks,
    )
    check(
        len(discovery_ids) == len(set(discovery_ids)),
        "Stage 3 IDs are unique",
        checks,
    )
    check(
        inventory_ids == discovery_ids,
        "Stage 3 is an ordered source-rule bijection",
        checks,
    )
    check(
        inventory["inventory_sha256"] == discovery["inventory_sha256"],
        "whole-inventory hash agrees with Stage 3",
        checks,
    )
    check(
        inventory["inventory_sha256"] == canonical_json_sha256(inventory_rules),
        "whole-inventory hash independently recomputes",
        checks,
    )
    check(
        inventory["verification_modules"] == ["VERIFICATION"],
        "local verification-module closure is exactly VERIFICATION",
        checks,
    )

    source_lines = (K_PROOF / "verification.k").read_text().splitlines()
    span_records: list[dict[str, Any]] = []
    for index, rule in enumerate(inventory_rules):
        normalized = " ".join(rule["text"].split())
        normalized_hash = hashlib.sha256(normalized.encode()).hexdigest()
        source_text = "\n".join(
            source_lines[rule["start_line"] - 1 : rule["end_line"]]
        ).rstrip(" \t\r\n")
        check(
            source_text == rule["text"],
            f"rule {index + 1} exact source span",
            checks,
        )
        check(
            normalized_hash == rule["normalized_sha256"],
            f"rule {index + 1} normalized source hash",
            checks,
        )
        check(
            rule["source_rule_id"] == f"rule-{normalized_hash}",
            f"rule {index + 1} source_rule_id",
            checks,
        )
        span_records.append(
            {
                "ordinal": index + 1,
                "start_line": rule["start_line"],
                "end_line": rule["end_line"],
                "normalized_sha256": normalized_hash,
                "source_rule_id": rule["source_rule_id"],
                "attributes": rule["attributes"],
                "stage3_classification": discovery_rules[index]["classification"],
            }
        )

    allowed = {
        "DEFINITION",
        "OPERATIONAL_RULE",
        "PROVED_DERIVED_LEMMA",
        "DOMAIN_LEMMA",
    }
    classifications = [rule["classification"] for rule in discovery_rules]
    check(
        all(classification in allowed for classification in classifications),
        "all Stage 3 classifications are accounted categories",
        checks,
    )
    check(
        classifications == ["DEFINITION"] * len(inventory_rules),
        "all 11 Stage 3 entries are classified DEFINITION",
        checks,
    )
    simplification_ids = [
        rule["source_rule_id"]
        for rule in inventory_rules
        if "simplification" in rule["attributes"]
    ]
    check(
        not simplification_ids,
        "inventory contains no simplification-attributed rule",
        checks,
    )

    hashes = resolution["hashes"]
    observed_pipeline_hashes = {
        "k_workspace_sha256": pipeline_contract.sha256_tree(K_PROOF),
        "k_audit_sha256": pipeline_contract.sha256_tree(K_AUDIT),
        "klean_generation_sha256": pipeline_contract.sha256_tree(GENERATION),
    }
    for key, observed in observed_pipeline_hashes.items():
        check(observed == hashes[key], f"audit-input {key}", checks)
    stage1_export_hash = klean_export.tree_digest(K_PROOF)
    generated_tree_hash = klean_export.tree_digest(GENERATED)
    check(
        stage1_export_hash == hashes["stage1_export_sha256"],
        "audit-input stage1_export_sha256",
        checks,
    )
    check(
        generated_tree_hash == hashes["generated_tree_sha256"],
        "audit-input generated_tree_sha256",
        checks,
    )
    check(
        sha256_file(DISCOVERY) == hashes["discovery_manifest_sha256"],
        "audit-input discovery manifest hash",
        checks,
    )
    check(
        hashes["lean_workspace_sha256"] is None
        and hashes["lean_invocation_sha256"] is None,
        "proof-mode hashes are absent",
        checks,
    )

    recorded_stage1_hashes = resolution["stage1_source_hashes"]
    observed_stage1_hashes = regular_file_hashes(K_PROOF)
    check(
        observed_stage1_hashes == recorded_stage1_hashes,
        "Stage 1 source-file hash map is exact and complete",
        checks,
    )
    check(
        observed_stage1_hashes["verification.k"]
        == inventory["verification_sha256"],
        "verification.k hash agrees with inventory",
        checks,
    )

    selections = resolution["selections"]
    check(
        selections["k_audit"]["artifact_sha256"]
        == observed_pipeline_hashes["k_audit_sha256"],
        "selected Stage 2 artifact hash",
        checks,
    )
    check(
        selections["klean_generation"]["artifact_sha256"]
        == observed_pipeline_hashes["klean_generation_sha256"],
        "selected Stage 4 artifact hash",
        checks,
    )
    check(
        selections["klean_generation"]["status"] == "KLEAN_NO_OBLIGATIONS",
        "selected Stage 4 status",
        checks,
    )

    input_manifest = load(GENERATION / "input-manifest.json")
    generator_manifest = load(GENERATION / "generator-manifest.json")
    obligation_map = load(GENERATED / "obligation-map.json")
    export_result = load(GENERATION / "export-result.json")
    preflight = load(GENERATION / "preflight.json")
    trust_inventory = load(GENERATION / "trust-inventory.json")
    toolchain_lock = load(TOOLCHAIN_LOCK)

    check(
        input_manifest["frozen_input_sha256"]
        == input_manifest["stage1_workspace_sha256"]
        == stage1_export_hash,
        "Stage 4 frozen Stage 1 tree binding",
        checks,
    )
    check(
        input_manifest["stage3_discovery_manifest_sha256"]
        == sha256_file(DISCOVERY),
        "Stage 4 Stage 3 manifest binding",
        checks,
    )
    check(
        input_manifest["inventory_sha256"] == inventory["inventory_sha256"],
        "Stage 4 inventory binding",
        checks,
    )
    check(
        input_manifest["verification_sha256"]
        == inventory["verification_sha256"],
        "Stage 4 verification.k binding",
        checks,
    )
    check(
        generator_manifest["generated_tree_sha256"] == generated_tree_hash,
        "generator generated-tree hash",
        checks,
    )
    check(
        generator_manifest["obligation_map_sha256"]
        == sha256_file(GENERATED / "obligation-map.json"),
        "generator obligation-map hash",
        checks,
    )
    current_generator_tool_hashes = {
        "exporter_sha256": sha256_file(
            Path("/reference/tools/klean_export.py")
        ),
        "klean_py_sha256": sha256_file(Path("/reference/tools/klean.py")),
    }
    historical_generator_hashes_match_current_tools = {
        key: generator_manifest[key] == current_generator_tool_hashes[key]
        for key in current_generator_tool_hashes
    }
    check(
        generator_manifest["toolchain"] == toolchain_lock,
        "generator pinned toolchain",
        checks,
    )
    check(
        generator_manifest["provenance"]
        == {
            "generator_image_id": generator_manifest["provenance"][
                "generator_image_id"
            ],
            "inventory_sha256": inventory["inventory_sha256"],
            "stage1_workspace_sha256": stage1_export_hash,
            "stage3_discovery_manifest_sha256": sha256_file(DISCOVERY),
        },
        "generator provenance bindings",
        checks,
    )

    independently_classified_domain_ids: list[str] = []
    stage4_source_ids = [
        rule["source_rule_id"] for rule in input_manifest["source_rules"]
    ]
    mapped_source_ids = [
        rule["source_rule_id"] for rule in obligation_map["source_rules"]
    ]
    obligation_ids = [
        obligation["source_rule_id"]
        for obligation in obligation_map["obligations"]
    ]
    check(
        independently_classified_domain_ids
        == stage4_source_ids
        == mapped_source_ids
        == obligation_ids
        == [],
        "independent domain set and Stage 4 source/obligation bijection are empty",
        checks,
    )
    check(
        input_manifest["operational_rules"] == []
        and input_manifest["proved_derived_lemmas"] == []
        and input_manifest["summary_functions"] == [],
        "non-definition Stage 4 input partitions are empty",
        checks,
    )
    check(
        [entry["source_rule_id"] for entry in input_manifest["definitions"]]
        == inventory_ids,
        "Stage 4 definitions preserve exact ordered inventory identities",
        checks,
    )
    for source, exported in zip(inventory_rules, input_manifest["definitions"]):
        for key in (
            "source_rule_id",
            "module",
            "start_line",
            "end_line",
            "normalized_sha256",
            "attributes",
            "text",
        ):
            check(
                source[key] == exported[key],
                f"Stage 4 definition {source['source_rule_id']} field {key}",
                checks,
            )
        check(
            exported["classification"] == "DEFINITION",
            f"Stage 4 definition {source['source_rule_id']} classification",
            checks,
        )
    check(
        obligation_map["trust_parameters"] == [],
        "zero obligations have zero trust parameters",
        checks,
    )
    check(
        generator_manifest["obligation_count"]
        == export_result["obligation_count"]
        == preflight["obligation_count"]
        == 0,
        "all Stage 4 obligation counts are zero",
        checks,
    )
    check(
        generator_manifest["target"] is None
        and preflight["target"] is None
        and resolution["target"] is None
        and klean_export.target_statement(GENERATED) is None,
        "fixed generated target is absent everywhere",
        checks,
    )
    check(
        export_result["status"] == preflight["status"]
        == resolution["stage4_preflight"]["status"]
        == "KLEAN_NO_OBLIGATIONS",
        "Stage 4 no-obligations status is consistent",
        checks,
    )
    check(
        export_result["frozen_input_sha256"] == stage1_export_hash
        and export_result["generated_tree_sha256"] == generated_tree_hash
        and export_result["stage3_discovery_manifest_sha256"]
        == sha256_file(DISCOVERY)
        and export_result["trust_inventory_sha256"]
        == sha256_file(GENERATION / "trust-inventory.json"),
        "export-result hash bindings",
        checks,
    )
    check(
        resolution["stage4_preflight"] == preflight,
        "audit-input embeds the exact Stage 4 preflight",
        checks,
    )
    check(
        len(trust_inventory["allowlist"])
        == len(trust_inventory["axioms"])
        == preflight["trust_declaration_count"]
        == 47,
        "generated trust inventory count",
        checks,
    )
    check(
        trust_inventory["designated_sorries"] == 0
        and trust_inventory["other_sorries"] == 0,
        "generated trust inventory has no proof holes",
        checks,
    )
    check(
        resolution["stage5_result"] is None
        and resolution["lean_workspace"] is None
        and resolution["lean_invocation"] is None
        and not Path("/candidate").exists(),
        "Stage 5 candidate and result are absent",
        checks,
    )

    report = {
        "status": "PASS",
        "check_count": len(checks),
        "checks": checks,
        "inventory": {
            "verification_module": inventory["verification_module"],
            "verification_modules": inventory["verification_modules"],
            "verification_sha256": inventory["verification_sha256"],
            "inventory_sha256": inventory["inventory_sha256"],
            "rule_count": len(inventory_rules),
            "rules": span_records,
        },
        "observed_hashes": {
            **observed_pipeline_hashes,
            "stage1_export_sha256": stage1_export_hash,
            "discovery_manifest_sha256": sha256_file(DISCOVERY),
            "generated_tree_sha256": generated_tree_hash,
            "obligation_map_sha256": sha256_file(
                GENERATED / "obligation-map.json"
            ),
            "trust_inventory_sha256": sha256_file(
                GENERATION / "trust-inventory.json"
            ),
        },
        "historical_generator_tool_hashes": {
            "recorded": {
                key: generator_manifest[key]
                for key in current_generator_tool_hashes
            },
            "current_trusted_tools": current_generator_tool_hashes,
            "match": historical_generator_hashes_match_current_tools,
            "note": (
                "The selected manifest records a separate generator image; "
                "these historical source objects are not mounted in "
                "/reference/tools and therefore are not asserted as current "
                "gate-tool bindings."
            ),
        },
        "stage1_source_file_count": len(observed_stage1_hashes),
        "independently_classified_domain_ids": independently_classified_domain_ids,
        "stage4_obligation_ids": obligation_ids,
        "target": klean_export.target_statement(GENERATED),
        "stage5_candidate_exists": Path("/candidate").exists(),
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
