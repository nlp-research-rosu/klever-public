#!/usr/bin/env python3
"""Read-only independent hash, provenance, and K-rule inventory checks."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

from tools import (
    k_rule_inventory,
    klean_export,
    lemma_discovery_contract,
    pipeline_contract,
    stage6_resolution_contract,
)


AUDIT_INPUT = Path("/audit-input.json")
K_WORKSPACE = Path("/reference/k-proof")
K_AUDIT = Path("/reference/k-audit")
DISCOVERY = Path("/reference/lemma-discovery.json")
GENERATION = Path("/reference/klean-generation")
GENERATED = GENERATION / "generated"
PRODUCERS = Path("/reference/generation-tools")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: Path) -> dict:
    document = json.loads(path.read_text())
    if not isinstance(document, dict):
        raise RuntimeError(f"expected JSON object: {path}")
    return document


def equality(name: str, observed: object, expected: object) -> dict:
    return {
        "name": name,
        "observed": observed,
        "expected": expected,
        "match": observed == expected,
    }


audit_document = load(AUDIT_INPUT)
resolution, resolved_input_sha256 = stage6_resolution_contract.verify_audit_input(
    audit_document
)
hashes = resolution["hashes"]
generator_manifest = load(GENERATION / "generator-manifest.json")
input_manifest = load(GENERATION / "input-manifest.json")
export_result = load(GENERATION / "export-result.json")
source_manifest = load(PRODUCERS / "source-manifest.json")
obligation_map = load(GENERATED / "obligation-map.json")
recorded_preflight = load(GENERATION / "preflight.json")

checks: list[dict] = []
checks.append(equality("AUDIT_MODE", os.environ.get("AUDIT_MODE"), resolution["mode"]))
checks.append(equality("semantics_mode", resolution["semantics_mode"], "SUPPLIED_SEMANTICS"))
checks.append(
    equality(
        "resolved_input_sha256",
        stage6_resolution_contract.canonical_json_sha256(resolution),
        resolved_input_sha256,
    )
)
checks.append(
    equality(
        "k_workspace_sha256",
        pipeline_contract.sha256_tree(K_WORKSPACE),
        hashes["k_workspace_sha256"],
    )
)
stage1_export_sha256 = klean_export.tree_digest(K_WORKSPACE)
checks.append(
    equality(
        "stage1_export_sha256",
        stage1_export_sha256,
        hashes["stage1_export_sha256"],
    )
)
checks.append(
    equality(
        "discovery_manifest_sha256",
        sha256(DISCOVERY),
        hashes["discovery_manifest_sha256"],
    )
)
checks.append(
    equality(
        "k_audit_sha256",
        pipeline_contract.sha256_tree(K_AUDIT),
        hashes["k_audit_sha256"],
    )
)
checks.append(
    equality(
        "klean_generation_sha256",
        pipeline_contract.sha256_tree(GENERATION),
        hashes["klean_generation_sha256"],
    )
)
checks.append(
    equality(
        "generation_producer_sources_sha256",
        pipeline_contract.sha256_tree(PRODUCERS),
        hashes["generation_producer_sources_sha256"],
    )
)
generated_tree_sha256 = klean_export.tree_digest(GENERATED)
checks.append(
    equality(
        "generated_tree_sha256",
        generated_tree_sha256,
        hashes["generated_tree_sha256"],
    )
)

observed_source_hashes = {
    path.relative_to(K_WORKSPACE).as_posix(): sha256(path)
    for path in pipeline_contract._walk_regular_files(
        K_WORKSPACE, "Stage 1 source workspace"
    )
}
expected_source_hashes = resolution["stage1_source_hashes"]
checks.append(
    equality(
        "stage1_source_hashes",
        {
            "file_count": len(observed_source_hashes),
            "missing": sorted(set(expected_source_hashes) - set(observed_source_hashes)),
            "extra": sorted(set(observed_source_hashes) - set(expected_source_hashes)),
            "mismatched": sorted(
                name
                for name in set(observed_source_hashes) & set(expected_source_hashes)
                if observed_source_hashes[name] != expected_source_hashes[name]
            ),
        },
        {
            "file_count": len(expected_source_hashes),
            "missing": [],
            "extra": [],
            "mismatched": [],
        },
    )
)

producer_expected = {
    "klean_export.py": generator_manifest.get("exporter_sha256"),
    "klean.py": generator_manifest.get("klean_py_sha256"),
}
producer_observed = {
    name: sha256(PRODUCERS / name) for name in sorted(producer_expected)
}
checks.append(equality("producer_file_hashes_vs_generator", producer_observed, producer_expected))
checks.append(equality("producer_file_hashes_vs_source_manifest", producer_observed, source_manifest.get("files")))
generator_image_id = generator_manifest.get("provenance", {}).get("generator_image_id")
checks.append(equality("producer_image_vs_source_manifest", source_manifest.get("generator_image_id"), generator_image_id))
checks.append(
    equality(
        "producer_image_address",
        generator_image_id,
        "sha256:" + str(resolution["generation_producer_sources"]).rstrip("/").split("/")[-1],
    )
)
producer_names = sorted(
    path.relative_to(PRODUCERS).as_posix()
    for path in pipeline_contract._walk_regular_files(
        PRODUCERS, "Stage 4 producer source bundle"
    )
)
checks.append(
    equality(
        "producer_bundle_exact_files",
        producer_names,
        ["klean.py", "klean_export.py", "source-manifest.json"],
    )
)

inventory = k_rule_inventory.inventory_verification(K_WORKSPACE)
validated = lemma_discovery_contract.validate_trust_boundary(K_WORKSPACE, DISCOVERY)
discovery_document = load(DISCOVERY)
checks.append(equality("inventory_sha256_vs_discovery", inventory["inventory_sha256"], discovery_document["inventory_sha256"]))
checks.append(equality("inventory_sha256_vs_input_manifest", inventory["inventory_sha256"], input_manifest["inventory_sha256"]))
checks.append(equality("validated_inventory_rules", validated["rules"], inventory["rules"]))
checks.append(
    equality(
        "discovery_rule_order",
        [rule["source_rule_id"] for rule in discovery_document["rules"]],
        [rule["source_rule_id"] for rule in inventory["rules"]],
    )
)
checks.append(
    equality(
        "discovery_rule_identity_unique",
        len({rule["source_rule_id"] for rule in discovery_document["rules"]}),
        len(inventory["rules"]),
    )
)

checks.extend(
    [
        equality("source_manifest_exact_keys", sorted(source_manifest), ["files", "generator_image_id", "schema_version"]),
        equality("source_manifest_schema", source_manifest.get("schema_version"), 1),
        equality("selection_k_audit_hash", resolution["selections"]["k_audit"]["artifact_sha256"], hashes["k_audit_sha256"]),
        equality("selection_generation_hash", resolution["selections"]["klean_generation"]["artifact_sha256"], hashes["klean_generation_sha256"]),
        equality("selection_generation_status", resolution["selections"]["klean_generation"]["status"], "KLEAN_NO_OBLIGATIONS"),
        equality("audit_recorded_preflight", resolution["stage4_preflight"], recorded_preflight),
        equality("generator_stage1_hash", generator_manifest["provenance"]["stage1_workspace_sha256"], stage1_export_sha256),
        equality("input_stage1_hash", input_manifest["stage1_workspace_sha256"], stage1_export_sha256),
        equality("input_frozen_hash", input_manifest["frozen_input_sha256"], stage1_export_sha256),
        equality("export_frozen_hash", export_result["frozen_input_sha256"], stage1_export_sha256),
        equality("generator_discovery_hash", generator_manifest["provenance"]["stage3_discovery_manifest_sha256"], sha256(DISCOVERY)),
        equality("input_discovery_hash", input_manifest["stage3_discovery_manifest_sha256"], sha256(DISCOVERY)),
        equality("export_discovery_hash", export_result["stage3_discovery_manifest_sha256"], sha256(DISCOVERY)),
        equality("generator_generated_tree_hash", generator_manifest["generated_tree_sha256"], generated_tree_sha256),
        equality("export_generated_tree_hash", export_result["generated_tree_sha256"], generated_tree_sha256),
        equality("input_verification_hash", input_manifest["verification_sha256"], sha256(K_WORKSPACE / "verification.k")),
        equality("generator_obligation_map_hash", generator_manifest["obligation_map_sha256"], sha256(GENERATED / "obligation-map.json")),
        equality("export_trust_inventory_hash", export_result["trust_inventory_sha256"], sha256(GENERATION / "trust-inventory.json")),
        equality("obligation_count_generator", generator_manifest["obligation_count"], len(obligation_map["obligations"])),
        equality("obligation_count_export", export_result["obligation_count"], len(obligation_map["obligations"])),
        equality("source_rules_input_vs_map", input_manifest["source_rules"], obligation_map["source_rules"]),
        equality("source_rules_map_vs_obligations", len(obligation_map["source_rules"]), len(obligation_map["obligations"])),
        equality("obligation_ids_unique", len({item.get("source_rule_id") for item in obligation_map["obligations"]}), len(obligation_map["obligations"])),
        equality("no_vacuous_conjuncts", [item for item in obligation_map["obligations"] if item.get("lean_conjunct") in {"True", "true", "(True)"}], []),
        equality("target_statement_scan", klean_export.target_statement(GENERATED), None),
        equality("expected_target_definition", klean_export.expected_target_definition(obligation_map), None),
        equality("zero_obligation_target", generator_manifest["target"], None),
        equality("audit_target", resolution["target"], generator_manifest["target"]),
        equality("audit_lean_workspace", resolution["lean_workspace"], None),
        equality("audit_lean_invocation", resolution["lean_invocation"], None),
        equality("audit_stage5_result", resolution["stage5_result"], None),
        equality("no_candidate_in_classification_only", Path("/candidate").exists(), False),
    ]
)

failed = [check["name"] for check in checks if not check["match"]]
result = {
    "status": "PASS" if not failed else "FAIL",
    "failed_checks": failed,
    "check_count": len(checks),
    "checks": checks,
    "canonical_inventory": inventory,
    "validated_classifications": [
        {
            "source_rule_id": rule["source_rule_id"],
            "classification": rule["classification"],
            "start_line": rule["start_line"],
            "end_line": rule["end_line"],
            "normalized_sha256": rule["normalized_sha256"],
            "attributes": rule["attributes"],
            "text": rule["text"],
        }
        for category in (
            "definitions",
            "operational_rules",
            "proved_derived_lemmas",
            "domain_lemmas",
        )
        for rule in validated[category]
    ],
    "obligation_map": obligation_map,
}
print(json.dumps(result, indent=2, sort_keys=True))
raise SystemExit(0 if not failed else 1)
