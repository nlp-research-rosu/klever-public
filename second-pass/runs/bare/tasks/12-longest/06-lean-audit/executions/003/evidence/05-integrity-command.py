import hashlib
import json
import os
from pathlib import Path

from tools import klean_export, pipeline_contract, stage6_resolution_contract
from tools.lemma_discovery_contract import validate_trust_boundary


def file_sha(path: str | Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


audit = json.loads(Path("/audit-input.json").read_text())
resolution, resolved_digest = stage6_resolution_contract.verify_audit_input(audit)
generation = Path("/reference/klean-generation")
generated = generation / "generated"
generator = json.loads((generation / "generator-manifest.json").read_text())
input_manifest = json.loads((generation / "input-manifest.json").read_text())
export_result = json.loads((generation / "export-result.json").read_text())
preflight = json.loads((generation / "preflight.json").read_text())
obligation_map_path = generated / "obligation-map.json"
obligation_map = json.loads(obligation_map_path.read_text())
trust_path = generation / "trust-inventory.json"
source_manifest = json.loads(
    Path("/reference/generation-tools/source-manifest.json").read_text()
)
validated = validate_trust_boundary(
    Path("/reference/k-proof"), Path("/reference/lemma-discovery.json")
)
lock = json.loads(Path("/reference/klean-toolchain.lock.json").read_text())

observed_resolution_hashes = {
    "k_workspace_sha256": pipeline_contract.sha256_tree(
        Path("/reference/k-proof")
    ),
    "stage1_export_sha256": klean_export.tree_digest(
        Path("/reference/k-proof")
    ),
    "discovery_manifest_sha256": file_sha("/reference/lemma-discovery.json"),
    "k_audit_sha256": pipeline_contract.sha256_tree(
        Path("/reference/k-audit")
    ),
    "klean_generation_sha256": pipeline_contract.sha256_tree(generation),
    "generation_producer_sources_sha256": pipeline_contract.sha256_tree(
        Path("/reference/generation-tools")
    ),
    "generated_tree_sha256": klean_export.tree_digest(generated),
    "lean_workspace_sha256": None,
    "lean_invocation_sha256": None,
}
observed_source_hashes = {
    path.relative_to("/reference/k-proof").as_posix():
        pipeline_contract.sha256_file(path)
    for path in pipeline_contract._walk_regular_files(
        Path("/reference/k-proof"), "Stage 1"
    )
}
canonical_ids = [rule["source_rule_id"] for rule in validated["rules"]]
classified_ids = [
    rule["source_rule_id"]
    for rule in json.loads(
        Path("/reference/lemma-discovery.json").read_text()
    )["rules"]
]
producer_files = sorted(
    path.relative_to("/reference/generation-tools").as_posix()
    for path in pipeline_contract._walk_regular_files(
        Path("/reference/generation-tools"), "producer bundle"
    )
)
manifest_hash_checks = {
    "input_frozen": input_manifest["frozen_input_sha256"]
        == observed_resolution_hashes["stage1_export_sha256"],
    "input_stage1": input_manifest["stage1_workspace_sha256"]
        == observed_resolution_hashes["stage1_export_sha256"],
    "input_stage3": input_manifest["stage3_discovery_manifest_sha256"]
        == observed_resolution_hashes["discovery_manifest_sha256"],
    "input_verification": input_manifest["verification_sha256"]
        == file_sha("/reference/k-proof/verification.k"),
    "input_inventory": input_manifest["inventory_sha256"]
        == validated["inventory_sha256"],
    "generator_stage1": generator["provenance"]["stage1_workspace_sha256"]
        == observed_resolution_hashes["stage1_export_sha256"],
    "generator_stage3":
        generator["provenance"]["stage3_discovery_manifest_sha256"]
        == observed_resolution_hashes["discovery_manifest_sha256"],
    "generator_inventory": generator["provenance"]["inventory_sha256"]
        == validated["inventory_sha256"],
    "generator_generated_tree": generator["generated_tree_sha256"]
        == observed_resolution_hashes["generated_tree_sha256"],
    "generator_obligation_map": generator["obligation_map_sha256"]
        == file_sha(obligation_map_path),
    "generator_toolchain": generator["toolchain"] == lock,
    "export_frozen": export_result["frozen_input_sha256"]
        == observed_resolution_hashes["stage1_export_sha256"],
    "export_stage3": export_result["stage3_discovery_manifest_sha256"]
        == observed_resolution_hashes["discovery_manifest_sha256"],
    "export_generated_tree": export_result["generated_tree_sha256"]
        == observed_resolution_hashes["generated_tree_sha256"],
    "export_trust_inventory": export_result["trust_inventory_sha256"]
        == file_sha(trust_path),
    "preflight_sidecar_equals_launcher":
        preflight == resolution["stage4_preflight"],
}
producer_checks = {
    "exact_file_set": producer_files
        == ["klean.py", "klean_export.py", "source-manifest.json"],
    "image_id_three_way":
        source_manifest["generator_image_id"]
        == generator["provenance"]["generator_image_id"]
        == "sha256:" + Path(
            resolution["generation_producer_sources"]
        ).name,
    "exporter_three_way":
        file_sha("/reference/generation-tools/klean_export.py")
        == source_manifest["files"]["klean_export.py"]
        == generator["exporter_sha256"],
    "klean_py_three_way":
        file_sha("/reference/generation-tools/klean.py")
        == source_manifest["files"]["klean.py"]
        == generator["klean_py_sha256"],
}
structural_checks = {
    "ordered_identity_bijection": classified_ids == canonical_ids,
    "unique_identity_count": len(set(classified_ids)) == len(canonical_ids),
    "input_source_rules_empty": input_manifest["source_rules"] == [],
    "map_source_rules_equal_input":
        obligation_map["source_rules"] == input_manifest["source_rules"],
    "obligations_empty": obligation_map["obligations"] == [],
    "trust_parameters_empty": obligation_map["trust_parameters"] == [],
    "counts_zero":
        generator["obligation_count"]
        == export_result["obligation_count"]
        == preflight["obligation_count"]
        == 0,
    "target_definition_absent":
        klean_export.expected_target_definition(obligation_map) is None,
    "target_source_absent":
        klean_export.target_statement(generated) is None,
    "targets_null":
        generator["target"]
        is resolution["target"]
        is preflight["target"]
        is None,
    "statuses_no_obligations":
        export_result["status"]
        == preflight["status"]
        == resolution["selections"]["klean_generation"]["status"]
        == "KLEAN_NO_OBLIGATIONS",
    "stage5_absent":
        resolution["lean_workspace"]
        is resolution["lean_invocation"]
        is resolution["stage5_result"]
        is None
        and not Path("/candidate").exists(),
}

result = {
    "audit_mode": {
        "environment": os.environ.get("AUDIT_MODE"),
        "recorded": resolution["mode"],
        "match": os.environ.get("AUDIT_MODE") == resolution["mode"],
    },
    "resolved_input_digest": {
        "observed": stage6_resolution_contract.canonical_json_sha256(
            resolution
        ),
        "recorded": resolved_digest,
    },
    "resolution_hashes": {
        "observed": observed_resolution_hashes,
        "recorded": resolution["hashes"],
        "match": observed_resolution_hashes == resolution["hashes"],
    },
    "stage1_source_hashes": {
        "observed": observed_source_hashes,
        "recorded": resolution["stage1_source_hashes"],
        "match": observed_source_hashes == resolution["stage1_source_hashes"],
    },
    "producer_checks": producer_checks,
    "manifest_hash_checks": manifest_hash_checks,
    "structural_checks": structural_checks,
}
result["all_ok"] = all(
    [
        result["audit_mode"]["match"],
        result["resolved_input_digest"]["observed"]
            == result["resolved_input_digest"]["recorded"],
        result["resolution_hashes"]["match"],
        result["stage1_source_hashes"]["match"],
        *producer_checks.values(),
        *manifest_hash_checks.values(),
        *structural_checks.values(),
    ]
)
print(json.dumps(result, indent=2, sort_keys=True))
