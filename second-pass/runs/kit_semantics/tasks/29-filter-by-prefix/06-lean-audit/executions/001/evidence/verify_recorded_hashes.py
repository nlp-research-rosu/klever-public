import hashlib
import json
from pathlib import Path

from tools.k_rule_inventory import inventory_verification
from tools.klean_export import target_statement, tree_digest
from tools.pipeline_contract import (
    _walk_regular_files,
    sha256_file,
    sha256_tree,
)


AUDIT = Path("/audit-input.json")
K_WORKSPACE = Path("/reference/k-proof")
K_AUDIT = Path("/reference/k-audit")
DISCOVERY = Path("/reference/lemma-discovery.json")
GENERATION = Path("/reference/klean-generation")
GENERATED = GENERATION / "generated"
PRODUCERS = Path("/reference/generation-tools")


audit = json.loads(AUDIT.read_text())
resolution = audit["resolution"]
hashes = resolution["hashes"]
input_manifest = json.loads((GENERATION / "input-manifest.json").read_text())
generator_manifest = json.loads(
    (GENERATION / "generator-manifest.json").read_text()
)
export_result = json.loads((GENERATION / "export-result.json").read_text())
preflight = json.loads((GENERATION / "preflight.json").read_text())
obligation_map_path = GENERATED / "obligation-map.json"
obligation_map = json.loads(obligation_map_path.read_text())
lock = json.loads(Path("/reference/klean-toolchain.lock.json").read_text())
inventory = inventory_verification(K_WORKSPACE)

actual_stage1_sources = {
    path.relative_to(K_WORKSPACE).as_posix(): sha256_file(path)
    for path in _walk_regular_files(K_WORKSPACE, "Stage 1 workspace")
}
recorded_stage1_sources = resolution["stage1_source_hashes"]
stage1_source_mismatches = sorted(
    name
    for name in set(actual_stage1_sources) | set(recorded_stage1_sources)
    if actual_stage1_sources.get(name) != recorded_stage1_sources.get(name)
)

actual = {
    "discovery_manifest_sha256": sha256_file(DISCOVERY),
    "generated_tree_sha256": tree_digest(GENERATED),
    "generation_producer_sources_sha256": sha256_tree(PRODUCERS),
    "k_audit_sha256": sha256_tree(K_AUDIT),
    "k_workspace_sha256": sha256_tree(K_WORKSPACE),
    "klean_generation_sha256": sha256_tree(GENERATION),
    "stage1_export_sha256": tree_digest(K_WORKSPACE),
}

checks = {
    "resolution_hashes": {
        name: {
            "actual": value,
            "recorded": hashes[name],
            "match": value == hashes[name],
        }
        for name, value in actual.items()
    },
    "selected_k_audit_artifact": (
        actual["k_audit_sha256"]
        == resolution["selections"]["k_audit"]["artifact_sha256"]
    ),
    "selected_generation_artifact": (
        actual["klean_generation_sha256"]
        == resolution["selections"]["klean_generation"]["artifact_sha256"]
    ),
    "stage1_source_hash_count_actual": len(actual_stage1_sources),
    "stage1_source_hash_count_recorded": len(recorded_stage1_sources),
    "stage1_source_hash_mismatches": stage1_source_mismatches,
    "input_manifest_stage1_hashes": (
        input_manifest["frozen_input_sha256"]
        == input_manifest["stage1_workspace_sha256"]
        == actual["stage1_export_sha256"]
    ),
    "input_manifest_discovery_hash": (
        input_manifest["stage3_discovery_manifest_sha256"]
        == actual["discovery_manifest_sha256"]
    ),
    "input_manifest_verification_hash": (
        input_manifest["verification_sha256"]
        == sha256_file(K_WORKSPACE / "verification.k")
    ),
    "inventory_hash_chain": (
        inventory["inventory_sha256"]
        == json.loads(DISCOVERY.read_text())["inventory_sha256"]
        == input_manifest["inventory_sha256"]
        == generator_manifest["provenance"]["inventory_sha256"]
    ),
    "generator_stage1_hash": (
        generator_manifest["provenance"]["stage1_workspace_sha256"]
        == actual["stage1_export_sha256"]
    ),
    "generator_discovery_hash": (
        generator_manifest["provenance"][
            "stage3_discovery_manifest_sha256"
        ]
        == actual["discovery_manifest_sha256"]
    ),
    "generator_generated_tree_hash": (
        generator_manifest["generated_tree_sha256"]
        == actual["generated_tree_sha256"]
    ),
    "generator_obligation_map_hash": (
        generator_manifest["obligation_map_sha256"]
        == sha256_file(obligation_map_path)
    ),
    "generator_toolchain_lock": generator_manifest["toolchain"] == lock,
    "export_result_stage1_hash": (
        export_result["frozen_input_sha256"]
        == actual["stage1_export_sha256"]
    ),
    "export_result_discovery_hash": (
        export_result["stage3_discovery_manifest_sha256"]
        == actual["discovery_manifest_sha256"]
    ),
    "export_result_generated_hash": (
        export_result["generated_tree_sha256"]
        == actual["generated_tree_sha256"]
    ),
    "export_result_trust_inventory_hash": (
        export_result["trust_inventory_sha256"]
        == sha256_file(GENERATION / "trust-inventory.json")
    ),
    "recorded_preflight_structural_hashes": (
        preflight["frozen_input_sha256"]
        == preflight["stage1_workspace_sha256"]
        == actual["stage1_export_sha256"]
        and preflight["stage3_discovery_manifest_sha256"]
        == actual["discovery_manifest_sha256"]
        and preflight["generated_tree_sha256"]
        == actual["generated_tree_sha256"]
    ),
    "obligation_map_source_rules": obligation_map["source_rules"],
    "obligation_map_obligations": obligation_map["obligations"],
    "obligation_map_trust_parameters": obligation_map["trust_parameters"],
    "target_statement": target_statement(GENERATED),
    "candidate_absent": not Path("/candidate").exists(),
    "audit_lean_hashes_are_null": (
        hashes["lean_invocation_sha256"] is None
        and hashes["lean_workspace_sha256"] is None
    ),
}

boolean_failures = [
    key
    for key, value in checks.items()
    if isinstance(value, bool) and not value
]
resolution_failures = [
    key
    for key, value in checks["resolution_hashes"].items()
    if not value["match"]
]
checks["all_recorded_hashes_match"] = (
    not boolean_failures
    and not resolution_failures
    and not stage1_source_mismatches
)

print(json.dumps(checks, indent=2, sort_keys=True))
raise SystemExit(0 if checks["all_recorded_hashes_match"] else 1)
