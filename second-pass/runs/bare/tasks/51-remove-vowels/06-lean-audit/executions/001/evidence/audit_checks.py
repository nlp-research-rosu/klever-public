#!/usr/bin/env python3
"""Independent structural/hash checks over the read-only Stage 3/4 inputs."""

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


def load(path: str) -> dict:
    return json.loads(Path(path).read_text())


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


audit = load("/audit-input.json")
resolution, resolved_digest = stage6_resolution_contract.verify_audit_input(audit)
discovery = load("/reference/lemma-discovery.json")
generator = load("/reference/klean-generation/generator-manifest.json")
input_manifest = load("/reference/klean-generation/input-manifest.json")
source_manifest = load("/reference/generation-tools/source-manifest.json")
export_result = load("/reference/klean-generation/export-result.json")
preflight = load("/reference/klean-generation/preflight.json")
obligation_map = load(
    "/reference/klean-generation/generated/obligation-map.json"
)
lock = load("/reference/klean-toolchain.lock.json")

checks: dict[str, bool] = {}
observed: dict[str, object] = {}

checks["mode_env_matches_signed_resolution"] = (
    os.environ.get("AUDIT_MODE") == resolution["mode"] == "CLASSIFICATION_ONLY"
)
checks["audit_input_digest"] = (
    resolved_digest == audit["resolved_input_sha256"]
)

inventory = k_rule_inventory.inventory_verification(
    Path("/reference/k-proof")
)
validated = lemma_discovery_contract.validate_trust_boundary(
    Path("/reference/k-proof"),
    Path("/reference/lemma-discovery.json"),
)
observed["inventory"] = inventory

verification_lines = Path(
    "/reference/k-proof/verification.k"
).read_text().splitlines()
rule_local_checks = []
for rule in inventory["rules"]:
    exact_span = "\n".join(
        verification_lines[rule["start_line"] - 1 : rule["end_line"]]
    )
    normalized = " ".join(exact_span.split())
    digest = hashlib.sha256(normalized.encode()).hexdigest()
    rule_local_checks.append(
        {
            "source_rule_id": rule["source_rule_id"],
            "span_text_exact": exact_span == rule["text"],
            "normalized_sha256_exact": digest
            == rule["normalized_sha256"],
            "source_rule_id_exact": rule["source_rule_id"]
            == f"rule-{digest}",
        }
    )
checks["every_rule_span_hash_and_id_recomputed"] = all(
    all(value for key, value in item.items() if key != "source_rule_id")
    for item in rule_local_checks
)
observed["rule_local_checks"] = rule_local_checks
checks["inventory_hash_recomputed"] = (
    k_rule_inventory.canonical_json_sha256(inventory["rules"])
    == inventory["inventory_sha256"]
    == discovery["inventory_sha256"]
)

inventory_ids = [rule["source_rule_id"] for rule in inventory["rules"]]
manifest_ids = [rule["source_rule_id"] for rule in discovery["rules"]]
checks["manifest_rule_order_is_exact"] = manifest_ids == inventory_ids
checks["manifest_rule_ids_are_unique"] = (
    len(manifest_ids) == len(set(manifest_ids))
)
checks["manifest_rule_bijection"] = (
    len(manifest_ids) == len(inventory_ids)
    and set(manifest_ids) == set(inventory_ids)
)
checks["manifest_contract_validation"] = (
    validated["inventory_sha256"] == inventory["inventory_sha256"]
)

checks["input_manifest_inventory"] = (
    input_manifest["inventory_sha256"] == inventory["inventory_sha256"]
)
checks["input_manifest_definitions_exact"] = (
    input_manifest["definitions"] == validated["definitions"]
)
checks["input_manifest_operational_rules_exact"] = (
    input_manifest["operational_rules"] == validated["operational_rules"]
)
checks["input_manifest_proved_derived_lemmas_exact"] = (
    input_manifest["proved_derived_lemmas"]
    == validated["proved_derived_lemmas"]
)
checks["input_manifest_domain_rules_exact"] = (
    input_manifest["source_rules"] == validated["domain_lemmas"]
)

producer_file_hashes = {
    name: file_hash(Path("/reference/generation-tools") / name)
    for name in ("klean_export.py", "klean.py")
}
observed["producer_file_hashes"] = producer_file_hashes
expected_producer_files = {
    "klean_export.py": generator["exporter_sha256"],
    "klean.py": generator["klean_py_sha256"],
}
checks["producer_source_manifest_exact_keys"] = set(source_manifest) == {
    "schema_version",
    "generator_image_id",
    "files",
}
checks["producer_source_manifest_files_exact"] = (
    source_manifest["files"] == expected_producer_files
)
checks["producer_file_hashes_exact"] = (
    producer_file_hashes
    == source_manifest["files"]
    == expected_producer_files
)
producer_names = sorted(
    path.relative_to("/reference/generation-tools").as_posix()
    for path in Path("/reference/generation-tools").iterdir()
)
checks["producer_bundle_file_set_exact"] = producer_names == [
    "klean.py",
    "klean_export.py",
    "source-manifest.json",
]
generator_image = generator["provenance"]["generator_image_id"]
source_image = source_manifest["generator_image_id"]
audit_image_key = Path(
    resolution["generation_producer_sources"]
).name
checks["producer_image_id_exact"] = (
    generator_image
    == source_image
    == f"sha256:{audit_image_key}"
)

hashes = resolution["hashes"]
tree_hashes = {
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
    "generated_tree_sha256": klean_export.tree_digest(
        Path("/reference/klean-generation/generated")
    ),
}
observed["resolution_hashes_recomputed"] = tree_hashes
for name, digest in tree_hashes.items():
    checks[f"resolution_hash_{name}"] = hashes[name] == digest
checks["classification_only_null_lean_hashes"] = (
    hashes["lean_workspace_sha256"] is None
    and hashes["lean_invocation_sha256"] is None
)

stage1_files = {
    path.relative_to("/reference/k-proof").as_posix(): file_hash(path)
    for path in sorted(Path("/reference/k-proof").rglob("*"))
    if path.is_file()
}
observed["stage1_source_hashes_recomputed"] = stage1_files
checks["stage1_source_hashes_exact"] = (
    stage1_files == resolution["stage1_source_hashes"]
)
checks["verification_hash_cross_binding"] = (
    stage1_files["verification.k"]
    == inventory["verification_sha256"]
    == input_manifest["verification_sha256"]
)
checks["selection_k_audit_hash"] = (
    resolution["selections"]["k_audit"]["artifact_sha256"]
    == tree_hashes["k_audit_sha256"]
)
checks["selection_generation_hash"] = (
    resolution["selections"]["klean_generation"]["artifact_sha256"]
    == tree_hashes["klean_generation_sha256"]
)
checks["generator_generated_tree_hash"] = (
    generator["generated_tree_sha256"]
    == tree_hashes["generated_tree_sha256"]
)
checks["generator_stage1_provenance"] = (
    generator["provenance"]["stage1_workspace_sha256"]
    == tree_hashes["stage1_export_sha256"]
)
checks["generator_stage3_provenance"] = (
    generator["provenance"]["stage3_discovery_manifest_sha256"]
    == tree_hashes["discovery_manifest_sha256"]
)
checks["generator_inventory_provenance"] = (
    generator["provenance"]["inventory_sha256"]
    == inventory["inventory_sha256"]
)
checks["generator_toolchain_lock_exact"] = generator["toolchain"] == lock
checks["input_manifest_stage1_bindings"] = (
    input_manifest["frozen_input_sha256"]
    == tree_hashes["stage1_export_sha256"]
    and input_manifest["stage1_workspace_sha256"]
    == tree_hashes["stage1_export_sha256"]
)
checks["input_manifest_stage3_binding"] = (
    input_manifest["stage3_discovery_manifest_sha256"]
    == tree_hashes["discovery_manifest_sha256"]
)
trust_inventory_hash = file_hash(
    Path("/reference/klean-generation/trust-inventory.json")
)
checks["export_result_hash_bindings"] = (
    export_result["frozen_input_sha256"]
    == tree_hashes["stage1_export_sha256"]
    and export_result["stage3_discovery_manifest_sha256"]
    == tree_hashes["discovery_manifest_sha256"]
    and export_result["generated_tree_sha256"]
    == tree_hashes["generated_tree_sha256"]
    and export_result["trust_inventory_sha256"]
    == trust_inventory_hash
)
checks["preflight_hash_bindings"] = (
    preflight["frozen_input_sha256"]
    == tree_hashes["stage1_export_sha256"]
    and preflight["stage1_workspace_sha256"]
    == tree_hashes["stage1_export_sha256"]
    and preflight["stage3_discovery_manifest_sha256"]
    == tree_hashes["discovery_manifest_sha256"]
    and preflight["generated_tree_sha256"]
    == tree_hashes["generated_tree_sha256"]
)
checks["obligation_map_hash"] = (
    generator["obligation_map_sha256"]
    == file_hash(
        Path(
            "/reference/klean-generation/generated/obligation-map.json"
        )
    )
)
checks["obligation_map_source_rules_exact"] = (
    obligation_map["source_rules"] == input_manifest["source_rules"] == []
)
checks["obligation_map_obligations_empty"] = (
    obligation_map["obligations"] == []
)
checks["obligation_map_parameters_empty"] = (
    obligation_map["trust_parameters"] == []
)
checks["no_fixed_target"] = (
    generator["target"] is None
    and resolution["target"] is None
    and preflight["target"] is None
    and klean_export.target_statement(
        Path("/reference/klean-generation/generated")
    )
    is None
    and klean_export.expected_target_definition(obligation_map) is None
)
checks["zero_obligation_status_consistent"] = (
    generator["obligation_count"] == 0
    and export_result["obligation_count"] == 0
    and export_result["status"] == "KLEAN_NO_OBLIGATIONS"
    and preflight["obligation_count"] == 0
    and preflight["status"] == "KLEAN_NO_OBLIGATIONS"
    and resolution["selections"]["klean_generation"]["status"]
    == "KLEAN_NO_OBLIGATIONS"
)
checks["audit_embedded_preflight_exact"] = (
    resolution["stage4_preflight"] == preflight
)
checks["no_stage5_binding_or_candidate"] = (
    resolution["stage5_result"] is None
    and resolution["lean_workspace"] is None
    and resolution["lean_invocation"] is None
    and not Path("/candidate").exists()
)

observed["checks"] = checks
observed["all_checks_pass"] = all(checks.values())
print(json.dumps(observed, indent=2, sort_keys=True))
raise SystemExit(0 if observed["all_checks_pass"] else 1)
