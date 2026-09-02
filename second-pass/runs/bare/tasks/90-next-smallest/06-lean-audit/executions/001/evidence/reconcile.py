#!/usr/bin/env python3
"""Read-only hash, inventory, and Stage 4 reconciliation for this audit."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from typing import Any

from tools import (
    klean_export,
    lemma_discovery_contract,
    pipeline_contract,
    stage6_resolution_contract,
)
from tools.k_rule_inventory import inventory_verification


def read_json(path: str) -> dict[str, Any]:
    document = json.loads(Path(path).read_text())
    if not isinstance(document, dict):
        raise TypeError(f"expected JSON object: {path}")
    return document


def file_sha256(path: str | Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


checks: dict[str, dict[str, Any]] = {}


def check(name: str, observed: Any, expected: Any) -> None:
    checks[name] = {
        "expected": expected,
        "observed": observed,
        "match": observed == expected,
    }


audit_input = read_json("/audit-input.json")
resolution, resolved_digest = stage6_resolution_contract.verify_audit_input(
    audit_input
)
generator_manifest = read_json(
    "/reference/klean-generation/generator-manifest.json"
)
input_manifest = read_json("/reference/klean-generation/input-manifest.json")
export_result = read_json("/reference/klean-generation/export-result.json")
recorded_preflight = read_json("/reference/klean-generation/preflight.json")
source_manifest = read_json(
    "/reference/generation-tools/source-manifest.json"
)
discovery = read_json("/reference/lemma-discovery.json")
obligation_map = read_json(
    "/reference/klean-generation/generated/obligation-map.json"
)
toolchain_lock = read_json("/reference/klean-toolchain.lock.json")

inventory = inventory_verification(Path("/reference/k-proof"))
validated = lemma_discovery_contract.validate_trust_boundary(
    Path("/reference/k-proof"),
    Path("/reference/lemma-discovery.json"),
)

check("audit_mode_env", os.environ.get("AUDIT_MODE"), resolution["mode"])
check(
    "audit_input_copy_sha256",
    file_sha256("/audit-output/audit-input.json"),
    file_sha256("/audit-input.json"),
)
check(
    "resolved_input_sha256",
    resolved_digest,
    stage6_resolution_contract.canonical_json_sha256(resolution),
)

resolution_hashes = resolution["hashes"]
check(
    "k_workspace_pipeline_tree_sha256",
    pipeline_contract.sha256_tree(Path("/reference/k-proof")),
    resolution_hashes["k_workspace_sha256"],
)
check(
    "stage1_export_klean_tree_sha256",
    klean_export.tree_digest(Path("/reference/k-proof")),
    resolution_hashes["stage1_export_sha256"],
)
check(
    "k_audit_pipeline_tree_sha256",
    pipeline_contract.sha256_tree(Path("/reference/k-audit")),
    resolution_hashes["k_audit_sha256"],
)
check(
    "discovery_manifest_sha256",
    file_sha256("/reference/lemma-discovery.json"),
    resolution_hashes["discovery_manifest_sha256"],
)
check(
    "klean_generation_pipeline_tree_sha256",
    pipeline_contract.sha256_tree(Path("/reference/klean-generation")),
    resolution_hashes["klean_generation_sha256"],
)
check(
    "generation_producer_sources_pipeline_tree_sha256",
    pipeline_contract.sha256_tree(Path("/reference/generation-tools")),
    resolution_hashes["generation_producer_sources_sha256"],
)
check(
    "generated_klean_tree_sha256",
    klean_export.tree_digest(
        Path("/reference/klean-generation/generated")
    ),
    resolution_hashes["generated_tree_sha256"],
)
check(
    "selected_k_audit_artifact_sha256",
    pipeline_contract.sha256_tree(Path("/reference/k-audit")),
    resolution["selections"]["k_audit"]["artifact_sha256"],
)
check(
    "selected_klean_generation_artifact_sha256",
    pipeline_contract.sha256_tree(Path("/reference/klean-generation")),
    resolution["selections"]["klean_generation"]["artifact_sha256"],
)

observed_stage1_sources = {
    path.relative_to("/reference/k-proof").as_posix():
    pipeline_contract.sha256_file(path)
    for path in pipeline_contract._walk_regular_files(
        Path("/reference/k-proof"), "mounted Stage 1 workspace"
    )
}
check(
    "stage1_source_hash_map",
    observed_stage1_sources,
    resolution["stage1_source_hashes"],
)

producer_files = {
    name: file_sha256(Path("/reference/generation-tools") / name)
    for name in ("klean.py", "klean_export.py")
}
check("producer_files_vs_source_manifest", producer_files, source_manifest["files"])
check(
    "producer_exporter_vs_generator_manifest",
    producer_files["klean_export.py"],
    generator_manifest["exporter_sha256"],
)
check(
    "producer_klean_vs_generator_manifest",
    producer_files["klean.py"],
    generator_manifest["klean_py_sha256"],
)
generator_image_id = generator_manifest["provenance"]["generator_image_id"]
check(
    "producer_image_id_vs_source_manifest",
    source_manifest["generator_image_id"],
    generator_image_id,
)
check(
    "producer_image_id_vs_audit_input_path",
    Path(resolution["generation_producer_sources"]).name,
    generator_image_id.removeprefix("sha256:"),
)
check(
    "producer_bundle_exact_files",
    sorted(
        path.relative_to("/reference/generation-tools").as_posix()
        for path in pipeline_contract._walk_regular_files(
            Path("/reference/generation-tools"),
            "mounted Stage 4 producer source bundle",
        )
    ),
    ["klean.py", "klean_export.py", "source-manifest.json"],
)

check(
    "verification_sha256_vs_audit_input",
    inventory["verification_sha256"],
    resolution["stage1_source_hashes"]["verification.k"],
)
check(
    "verification_sha256_vs_input_manifest",
    inventory["verification_sha256"],
    input_manifest["verification_sha256"],
)
check(
    "inventory_sha256_vs_discovery",
    inventory["inventory_sha256"],
    discovery["inventory_sha256"],
)
check(
    "inventory_sha256_vs_input_manifest",
    inventory["inventory_sha256"],
    input_manifest["inventory_sha256"],
)
check(
    "inventory_sha256_vs_generator_provenance",
    inventory["inventory_sha256"],
    generator_manifest["provenance"]["inventory_sha256"],
)
canonical_ids = [rule["source_rule_id"] for rule in inventory["rules"]]
classified_ids = [rule["source_rule_id"] for rule in discovery["rules"]]
check("stage3_rule_identity_order", classified_ids, canonical_ids)
check("stage3_rule_identity_uniqueness", len(set(classified_ids)), len(classified_ids))
check("stage3_rule_count", len(classified_ids), len(canonical_ids))

expected_domain_source_rules = klean_export._domain_source_rules(
    validated,
    file_sha256("/reference/lemma-discovery.json"),
)
check(
    "input_manifest_domain_source_rules",
    input_manifest["source_rules"],
    expected_domain_source_rules,
)
check(
    "obligation_map_source_rules",
    obligation_map["source_rules"],
    expected_domain_source_rules,
)
check(
    "obligation_source_rule_identity_order",
    [
        obligation.get("source_rule_id")
        for obligation in obligation_map["obligations"]
    ],
    [rule["source_rule_id"] for rule in expected_domain_source_rules],
)
check(
    "obligation_source_rule_identity_uniqueness",
    len(
        {
            obligation.get("source_rule_id")
            for obligation in obligation_map["obligations"]
        }
    ),
    len(obligation_map["obligations"]),
)
check(
    "generator_obligation_count",
    generator_manifest["obligation_count"],
    len(obligation_map["obligations"]),
)
check(
    "export_obligation_count",
    export_result["obligation_count"],
    len(obligation_map["obligations"]),
)
check(
    "obligation_map_sha256",
    file_sha256(
        "/reference/klean-generation/generated/obligation-map.json"
    ),
    generator_manifest["obligation_map_sha256"],
)
check(
    "trust_inventory_sha256",
    file_sha256("/reference/klean-generation/trust-inventory.json"),
    export_result["trust_inventory_sha256"],
)

generated_target = klean_export.target_statement(
    Path("/reference/klean-generation/generated")
)
expected_target_definition = klean_export.expected_target_definition(
    obligation_map
)
raw_target_occurrences = 0
for source in Path("/reference/klean-generation/generated").rglob("*.lean"):
    raw_target_occurrences += sum(
        1
        for line in source.read_text().splitlines()
        if line.lstrip().startswith("def targetStatement")
    )
check("expected_target_definition", expected_target_definition, None)
check("generated_target", generated_target, None)
check("generator_manifest_target", generator_manifest["target"], None)
check("audit_input_target", resolution["target"], None)
check("recorded_preflight_target", recorded_preflight["target"], None)
check("raw_target_occurrences", raw_target_occurrences, 0)
check("obligation_map_trust_parameters", obligation_map["trust_parameters"], [])
check("candidate_absent", Path("/candidate").exists(), False)
check("lean_workspace_hash_absent", resolution_hashes["lean_workspace_sha256"], None)
check("lean_invocation_hash_absent", resolution_hashes["lean_invocation_sha256"], None)
check("stage5_result_absent", resolution["stage5_result"], None)

check(
    "generator_generated_tree_sha256",
    generator_manifest["generated_tree_sha256"],
    resolution_hashes["generated_tree_sha256"],
)
check(
    "input_frozen_tree_sha256",
    input_manifest["frozen_input_sha256"],
    resolution_hashes["stage1_export_sha256"],
)
check(
    "input_stage1_tree_sha256",
    input_manifest["stage1_workspace_sha256"],
    resolution_hashes["stage1_export_sha256"],
)
check(
    "generator_stage1_tree_sha256",
    generator_manifest["provenance"]["stage1_workspace_sha256"],
    resolution_hashes["stage1_export_sha256"],
)
check(
    "input_discovery_sha256",
    input_manifest["stage3_discovery_manifest_sha256"],
    resolution_hashes["discovery_manifest_sha256"],
)
check(
    "generator_discovery_sha256",
    generator_manifest["provenance"][
        "stage3_discovery_manifest_sha256"
    ],
    resolution_hashes["discovery_manifest_sha256"],
)
check(
    "export_frozen_tree_sha256",
    export_result["frozen_input_sha256"],
    resolution_hashes["stage1_export_sha256"],
)
check(
    "export_generated_tree_sha256",
    export_result["generated_tree_sha256"],
    resolution_hashes["generated_tree_sha256"],
)
check(
    "export_discovery_sha256",
    export_result["stage3_discovery_manifest_sha256"],
    resolution_hashes["discovery_manifest_sha256"],
)
check(
    "generator_toolchain_lock",
    generator_manifest["toolchain"],
    toolchain_lock,
)
check(
    "recorded_preflight_vs_audit_input",
    recorded_preflight,
    resolution["stage4_preflight"],
)
check(
    "recorded_status_vs_selection",
    recorded_preflight["status"],
    resolution["selections"]["klean_generation"]["status"],
)
check("recorded_preflight_obligation_count", recorded_preflight["obligation_count"], 0)
check("export_status", export_result["status"], "KLEAN_NO_OBLIGATIONS")

document = {
    "schema_version": 1,
    "audit_mode": os.environ.get("AUDIT_MODE"),
    "inventory": inventory,
    "validated_classification_counts": {
        "definitions": len(validated["definitions"]),
        "operational_rules": len(validated["operational_rules"]),
        "proved_derived_lemmas": len(validated["proved_derived_lemmas"]),
        "domain_lemmas": len(validated["domain_lemmas"]),
    },
    "expected_domain_source_rules": expected_domain_source_rules,
    "checks": checks,
    "all_checks_pass": all(entry["match"] for entry in checks.values()),
}
print(json.dumps(document, indent=2, sort_keys=True))
