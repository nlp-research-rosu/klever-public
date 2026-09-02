#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

from tools.klean_export import target_statement, tree_digest
from tools.pipeline_contract import sha256_tree
from tools.stage6_resolution_contract import canonical_json_sha256


def read_json(path: Path):
    return json.loads(path.read_text())


audit_document = read_json(Path("/audit-input.json"))
audit = audit_document["resolution"]
k_workspace = Path("/reference/k-proof")
generation = Path("/reference/klean-generation")
generated = generation / "generated"
discovery_path = Path("/reference/lemma-discovery.json")
generator_manifest = read_json(generation / "generator-manifest.json")
input_manifest = read_json(generation / "input-manifest.json")
export_result = read_json(generation / "export-result.json")
recorded_preflight = read_json(generation / "preflight.json")
obligation_map_path = generated / "obligation-map.json"
obligation_map = read_json(obligation_map_path)
trust_inventory_path = generation / "trust-inventory.json"
toolchain_lock = read_json(Path("/reference/klean-toolchain.lock.json"))

actual_source_hashes = {
    path.relative_to(k_workspace).as_posix(): hashlib.sha256(
        path.read_bytes()
    ).hexdigest()
    for path in sorted(k_workspace.iterdir())
    if path.is_file() and not path.is_symlink()
}

actual = {
    "k_workspace_pipeline_tree_sha256": sha256_tree(k_workspace),
    "stage1_export_tree_sha256": tree_digest(k_workspace),
    "discovery_manifest_sha256": hashlib.sha256(
        discovery_path.read_bytes()
    ).hexdigest(),
    "k_audit_pipeline_tree_sha256": sha256_tree(
        Path("/reference/k-audit")
    ),
    "klean_generation_pipeline_tree_sha256": sha256_tree(generation),
    "generated_tree_sha256": tree_digest(generated),
    "obligation_map_sha256": hashlib.sha256(
        obligation_map_path.read_bytes()
    ).hexdigest(),
    "trust_inventory_sha256": hashlib.sha256(
        trust_inventory_path.read_bytes()
    ).hexdigest(),
    "verification_sha256": hashlib.sha256(
        (k_workspace / "verification.k").read_bytes()
    ).hexdigest(),
    "resolved_input_sha256": canonical_json_sha256(audit),
    "target_statement": target_statement(generated),
    "candidate_exists": Path("/candidate").exists(),
}
expected = {
    "k_workspace_pipeline_tree_sha256": audit["hashes"][
        "k_workspace_sha256"
    ],
    "stage1_export_tree_sha256": audit["hashes"][
        "stage1_export_sha256"
    ],
    "discovery_manifest_sha256": audit["hashes"][
        "discovery_manifest_sha256"
    ],
    "k_audit_pipeline_tree_sha256": audit["hashes"]["k_audit_sha256"],
    "klean_generation_pipeline_tree_sha256": audit["hashes"][
        "klean_generation_sha256"
    ],
    "generated_tree_sha256": audit["hashes"]["generated_tree_sha256"],
    "obligation_map_sha256": generator_manifest[
        "obligation_map_sha256"
    ],
    "trust_inventory_sha256": export_result["trust_inventory_sha256"],
    "verification_sha256": input_manifest["verification_sha256"],
    "resolved_input_sha256": audit_document["resolved_input_sha256"],
    "target_statement": audit["target"],
    "candidate_exists": False,
}

checks = {
    "all_audit_hashes_match": all(
        actual[key] == expected[key] for key in actual
    ),
    "stage1_source_hashes_match": (
        actual_source_hashes == audit["stage1_source_hashes"]
    ),
    "stage1_hash_cross_records_match": (
        actual["stage1_export_tree_sha256"]
        == input_manifest["frozen_input_sha256"]
        == input_manifest["stage1_workspace_sha256"]
        == generator_manifest["provenance"]["stage1_workspace_sha256"]
        == export_result["frozen_input_sha256"]
        == recorded_preflight["frozen_input_sha256"]
        == recorded_preflight["stage1_workspace_sha256"]
    ),
    "discovery_hash_cross_records_match": (
        actual["discovery_manifest_sha256"]
        == input_manifest["stage3_discovery_manifest_sha256"]
        == generator_manifest["provenance"][
            "stage3_discovery_manifest_sha256"
        ]
        == export_result["stage3_discovery_manifest_sha256"]
        == recorded_preflight["stage3_discovery_manifest_sha256"]
    ),
    "generated_hash_cross_records_match": (
        actual["generated_tree_sha256"]
        == generator_manifest["generated_tree_sha256"]
        == export_result["generated_tree_sha256"]
        == recorded_preflight["generated_tree_sha256"]
    ),
    "verification_hash_cross_records_match": (
        actual["verification_sha256"]
        == input_manifest["verification_sha256"]
        == audit["stage1_source_hashes"]["verification.k"]
    ),
    "toolchain_lock_matches_generator_manifest": (
        toolchain_lock == generator_manifest["toolchain"]
    ),
    "empty_source_rule_bijection": (
        input_manifest["source_rules"]
        == obligation_map["source_rules"]
        == []
        and obligation_map["obligations"] == []
        and obligation_map["trust_parameters"] == []
    ),
    "zero_obligation_counts": (
        generator_manifest["obligation_count"]
        == export_result["obligation_count"]
        == recorded_preflight["obligation_count"]
        == 0
    ),
    "no_target_anywhere": (
        generator_manifest["target"]
        is export_result.get("target")
        is recorded_preflight["target"]
        is audit["target"]
        is actual["target_statement"]
        is None
    ),
    "classification_only_has_no_stage5": (
        audit["mode"] == "CLASSIFICATION_ONLY"
        and audit["lean_workspace"] is None
        and audit["lean_invocation"] is None
        and audit["stage5_result"] is None
        and not actual["candidate_exists"]
    ),
    "status_is_consistently_no_obligations": (
        audit["selections"]["klean_generation"]["status"]
        == export_result["status"]
        == recorded_preflight["status"]
        == "KLEAN_NO_OBLIGATIONS"
    ),
}

report = {
    "actual": actual,
    "expected": expected,
    "actual_stage1_source_hashes": actual_source_hashes,
    "expected_stage1_source_hashes": audit["stage1_source_hashes"],
    "obligation_map": obligation_map,
    "checks": checks,
}
print(json.dumps(report, indent=2, sort_keys=True))
if not all(checks.values()):
    raise SystemExit(1)
