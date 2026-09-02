import hashlib
import json
import os
from pathlib import Path

from tools import klean_export
from tools import pipeline_contract
from tools import stage6_resolution_contract


audit_input = json.loads(Path("/audit-input.json").read_text())
resolution = audit_input["resolution"]
recorded_hashes = resolution["hashes"]
generation_tools = Path("/reference/generation-tools")
generation = Path("/reference/klean-generation")
k_workspace = Path("/reference/k-proof")
source_manifest = json.loads(
    (generation_tools / "source-manifest.json").read_text()
)
generator_manifest = json.loads(
    (generation / "generator-manifest.json").read_text()
)
input_manifest = json.loads((generation / "input-manifest.json").read_text())
export_result = json.loads((generation / "export-result.json").read_text())
preflight = json.loads((generation / "preflight.json").read_text())
trust_inventory = generation / "trust-inventory.json"
discovery = Path("/reference/lemma-discovery.json")
checker_lock_path = Path(
    "/opt/humaneval/data/klean-audit-tools.lock.json"
)
checker_lock = json.loads(checker_lock_path.read_text())


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


producer_exporter = sha256_file(generation_tools / "klean_export.py")
producer_klean = sha256_file(generation_tools / "klean.py")
audit_image = (
    "sha256:" + Path(resolution["generation_producer_sources"]).name
)
_verified_resolution, resolved_digest = (
    stage6_resolution_contract.verify_audit_input(audit_input)
)
checks = {
    "audit_mode_env": (
        os.environ.get("AUDIT_MODE")
        == resolution["mode"]
        == "CLASSIFICATION_ONLY"
    ),
    "resolved_input_sha256": (
        resolved_digest == audit_input["resolved_input_sha256"]
    ),
    "mechanical_checker_lock_sha256": (
        sha256_file(checker_lock_path)
        == audit_input["audit"]["mechanical_checker_lock_sha256"]
    ),
    "mechanical_checker_files_all": all(
        sha256_file(Path("/reference") / relative) == expected
        for relative, expected in checker_lock["files"].items()
    ),
    "k_workspace_sha256": (
        pipeline_contract.sha256_tree(k_workspace)
        == recorded_hashes["k_workspace_sha256"]
    ),
    "stage1_export_sha256": (
        klean_export.tree_digest(k_workspace)
        == recorded_hashes["stage1_export_sha256"]
    ),
    "stage1_source_hash_keyset": (
        sorted(resolution["stage1_source_hashes"])
        == sorted(
            path.relative_to(k_workspace).as_posix()
            for path in k_workspace.rglob("*")
            if path.is_file()
        )
    ),
    "stage1_source_hashes_all": all(
        sha256_file(k_workspace / relative) == expected
        for relative, expected in resolution[
            "stage1_source_hashes"
        ].items()
    ),
    "discovery_manifest_sha256": (
        sha256_file(discovery)
        == recorded_hashes["discovery_manifest_sha256"]
    ),
    "k_audit_sha256": (
        pipeline_contract.sha256_tree(Path("/reference/k-audit"))
        == recorded_hashes["k_audit_sha256"]
    ),
    "klean_generation_sha256": (
        pipeline_contract.sha256_tree(generation)
        == recorded_hashes["klean_generation_sha256"]
    ),
    "generation_producer_sources_sha256": (
        pipeline_contract.sha256_tree(generation_tools)
        == recorded_hashes["generation_producer_sources_sha256"]
    ),
    "generated_tree_sha256": (
        klean_export.tree_digest(generation / "generated")
        == recorded_hashes["generated_tree_sha256"]
    ),
    "producer_export_source_manifest": (
        producer_exporter
        == source_manifest["files"]["klean_export.py"]
    ),
    "producer_export_generator_manifest": (
        producer_exporter == generator_manifest["exporter_sha256"]
    ),
    "producer_klean_source_manifest": (
        producer_klean == source_manifest["files"]["klean.py"]
    ),
    "producer_klean_generator_manifest": (
        producer_klean == generator_manifest["klean_py_sha256"]
    ),
    "generator_image_three_way": (
        source_manifest["generator_image_id"]
        == generator_manifest["provenance"]["generator_image_id"]
        == audit_image
    ),
    "generator_toolchain_lock_exact": (
        generator_manifest["toolchain"]
        == json.loads(
            Path("/reference/klean-toolchain.lock.json").read_text()
        )
    ),
    "generator_obligation_map_sha256": (
        generator_manifest["obligation_map_sha256"]
        == sha256_file(generation / "generated/obligation-map.json")
    ),
    "input_inventory_sha256": (
        input_manifest["inventory_sha256"]
        == generator_manifest["provenance"]["inventory_sha256"]
    ),
    "input_verification_sha256": (
        input_manifest["verification_sha256"]
        == sha256_file(k_workspace / "verification.k")
    ),
    "input_workspace_hashes": (
        input_manifest["frozen_input_sha256"]
        == input_manifest["stage1_workspace_sha256"]
        == klean_export.tree_digest(k_workspace)
    ),
    "input_discovery_hash": (
        input_manifest["stage3_discovery_manifest_sha256"]
        == sha256_file(discovery)
    ),
    "generator_provenance_workspace": (
        generator_manifest["provenance"]["stage1_workspace_sha256"]
        == klean_export.tree_digest(k_workspace)
    ),
    "generator_provenance_discovery": (
        generator_manifest["provenance"][
            "stage3_discovery_manifest_sha256"
        ]
        == sha256_file(discovery)
    ),
    "export_result_workspace": (
        export_result["frozen_input_sha256"]
        == klean_export.tree_digest(k_workspace)
    ),
    "export_result_discovery": (
        export_result["stage3_discovery_manifest_sha256"]
        == sha256_file(discovery)
    ),
    "export_result_generated_tree": (
        export_result["generated_tree_sha256"]
        == klean_export.tree_digest(generation / "generated")
    ),
    "export_result_trust_inventory": (
        export_result["trust_inventory_sha256"]
        == sha256_file(trust_inventory)
    ),
    "preflight_sidecar_matches_audit_input": (
        preflight == resolution["stage4_preflight"]
    ),
    "preflight_hashes": (
        preflight["frozen_input_sha256"]
        == preflight["stage1_workspace_sha256"]
        == klean_export.tree_digest(k_workspace)
        and preflight["stage3_discovery_manifest_sha256"]
        == sha256_file(discovery)
        and preflight["generated_tree_sha256"]
        == klean_export.tree_digest(generation / "generated")
    ),
    "recorded_clean_output_hash": (
        preflight["diagnostics"][0]["output_sha256"]
        == hashlib.sha256(
            preflight["diagnostics"][0]["output_tail"].encode()
        ).hexdigest()
    ),
    "recorded_build_output_hash": (
        preflight["diagnostics"][1]["output_sha256"]
        == hashlib.sha256(
            preflight["diagnostics"][1]["output_tail"].encode()
        ).hexdigest()
    ),
    "no_lean_hashes_in_classification_only": (
        recorded_hashes["lean_workspace_sha256"] is None
        and recorded_hashes["lean_invocation_sha256"] is None
    ),
}

print("producer_export_sha256", producer_exporter)
print("producer_klean_sha256", producer_klean)
print("producer_image_id", source_manifest["generator_image_id"])
print("audit_input_image_binding", audit_image)
print("checks")
for name, passed in checks.items():
    print(name, passed)
print("all_checks", all(checks.values()))
