#!/usr/bin/env python3

import hashlib
import json
from pathlib import Path

from tools import klean_export
from tools.pipeline_contract import sha256_tree
from tools.stage6_resolution_contract import canonical_json_sha256


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


audit_input = json.loads(Path("/audit-input.json").read_text())
resolution = audit_input["resolution"]
audit_hashes = resolution["hashes"]
generation = Path("/reference/klean-generation")
generated = generation / "generated"
stage1 = Path("/reference/k-proof")
stage3 = Path("/reference/lemma-discovery.json")
producer_root = Path("/reference/generation-tools")

input_manifest = json.loads((generation / "input-manifest.json").read_text())
generator_manifest = json.loads((generation / "generator-manifest.json").read_text())
export_result = json.loads((generation / "export-result.json").read_text())
stored_preflight = json.loads((generation / "preflight.json").read_text())
obligation_map = json.loads((generated / "obligation-map.json").read_text())
source_manifest = json.loads((producer_root / "source-manifest.json").read_text())
toolchain_lock = json.loads(
    Path("/reference/klean-toolchain.lock.json").read_text()
)
mechanical_lock_path = Path(
    "/opt/humaneval/data/klean-audit-tools.lock.json"
)
mechanical_lock = json.loads(mechanical_lock_path.read_text())

stage1_pipeline_hash = sha256_tree(stage1)
stage1_export_hash = klean_export.tree_digest(stage1)
stage3_hash = file_sha256(stage3)
generated_hash = klean_export.tree_digest(generated)
generation_pipeline_hash = sha256_tree(generation)
producer_pipeline_hash = sha256_tree(producer_root)
k_audit_pipeline_hash = sha256_tree(Path("/reference/k-audit"))
obligation_map_hash = file_sha256(generated / "obligation-map.json")
trust_inventory_hash = file_sha256(generation / "trust-inventory.json")

producer_hashes = {
    name: file_sha256(producer_root / name)
    for name in ("klean.py", "klean_export.py")
}
generator_expected_producers = {
    "klean.py": generator_manifest["klean_py_sha256"],
    "klean_export.py": generator_manifest["exporter_sha256"],
}
audit_path_image = "sha256:" + Path(
    resolution["generation_producer_sources"]
).name

actual_stage1_files = sorted(
    path.relative_to(stage1).as_posix()
    for path in stage1.rglob("*")
    if path.is_file() and not path.is_symlink()
)
recorded_stage1_files = sorted(resolution["stage1_source_hashes"])
stage1_file_hashes = {
    relative: file_sha256(stage1 / relative)
    for relative in recorded_stage1_files
}
mechanical_locked_file_hashes = {
    relative: file_sha256(Path("/reference") / relative)
    for relative in mechanical_lock["files"]
}

checks = {
    "audit.resolved_input_sha256": (
        canonical_json_sha256(resolution)
        == audit_input["resolved_input_sha256"]
    ),
    "audit.mechanical_checker_lock_sha256": (
        file_sha256(mechanical_lock_path)
        == audit_input["audit"]["mechanical_checker_lock_sha256"]
    ),
    "audit.mechanical_checker_locked_files": (
        mechanical_locked_file_hashes == mechanical_lock["files"]
    ),
    "audit.discovery_manifest_sha256": (
        stage3_hash == audit_hashes["discovery_manifest_sha256"]
    ),
    "audit.generated_tree_sha256": (
        generated_hash == audit_hashes["generated_tree_sha256"]
    ),
    "audit.generation_producer_sources_sha256": (
        producer_pipeline_hash
        == audit_hashes["generation_producer_sources_sha256"]
    ),
    "audit.k_audit_sha256": (
        k_audit_pipeline_hash == audit_hashes["k_audit_sha256"]
    ),
    "audit.k_workspace_sha256": (
        stage1_pipeline_hash == audit_hashes["k_workspace_sha256"]
    ),
    "audit.klean_generation_sha256": (
        generation_pipeline_hash == audit_hashes["klean_generation_sha256"]
    ),
    "audit.stage1_export_sha256": (
        stage1_export_hash == audit_hashes["stage1_export_sha256"]
    ),
    "audit.stage1_source_file_set": (
        actual_stage1_files == recorded_stage1_files
    ),
    "audit.stage1_source_hashes": (
        stage1_file_hashes == resolution["stage1_source_hashes"]
    ),
    "producer.file_hashes.source_manifest": (
        producer_hashes == source_manifest["files"]
    ),
    "producer.file_hashes.generator_manifest": (
        producer_hashes == generator_expected_producers
    ),
    "producer.image_ids": (
        generator_manifest["provenance"]["generator_image_id"]
        == source_manifest["generator_image_id"]
        == audit_path_image
    ),
    "input_manifest.frozen_input_sha256": (
        input_manifest["frozen_input_sha256"] == stage1_export_hash
    ),
    "input_manifest.stage1_workspace_sha256": (
        input_manifest["stage1_workspace_sha256"] == stage1_export_hash
    ),
    "input_manifest.stage3_discovery_manifest_sha256": (
        input_manifest["stage3_discovery_manifest_sha256"] == stage3_hash
    ),
    "input_manifest.verification_sha256": (
        input_manifest["verification_sha256"]
        == file_sha256(stage1 / "verification.k")
    ),
    "generator_manifest.generated_tree_sha256": (
        generator_manifest["generated_tree_sha256"] == generated_hash
    ),
    "generator_manifest.obligation_map_sha256": (
        generator_manifest["obligation_map_sha256"] == obligation_map_hash
    ),
    "generator_manifest.toolchain": (
        generator_manifest["toolchain"] == toolchain_lock
    ),
    "generator_manifest.provenance.stage1": (
        generator_manifest["provenance"]["stage1_workspace_sha256"]
        == stage1_export_hash
    ),
    "generator_manifest.provenance.stage3": (
        generator_manifest["provenance"][
            "stage3_discovery_manifest_sha256"
        ]
        == stage3_hash
    ),
    "generator_manifest.provenance.inventory": (
        generator_manifest["provenance"]["inventory_sha256"]
        == input_manifest["inventory_sha256"]
    ),
    "export_result.frozen_input_sha256": (
        export_result["frozen_input_sha256"] == stage1_export_hash
    ),
    "export_result.generated_tree_sha256": (
        export_result["generated_tree_sha256"] == generated_hash
    ),
    "export_result.stage3_discovery_manifest_sha256": (
        export_result["stage3_discovery_manifest_sha256"] == stage3_hash
    ),
    "export_result.trust_inventory_sha256": (
        export_result["trust_inventory_sha256"] == trust_inventory_hash
    ),
    "stored_preflight.generated_tree_sha256": (
        stored_preflight["generated_tree_sha256"] == generated_hash
    ),
    "stored_preflight.stage1_workspace_sha256": (
        stored_preflight["stage1_workspace_sha256"] == stage1_export_hash
    ),
    "stored_preflight.stage3_discovery_manifest_sha256": (
        stored_preflight["stage3_discovery_manifest_sha256"] == stage3_hash
    ),
    "audit.stage4_preflight_exact": (
        resolution["stage4_preflight"] == stored_preflight
    ),
    "empty_obligation_map": (
        obligation_map
        == {
            "obligations": [],
            "schema_version": 3,
            "source_rules": [],
            "trust_parameters": [],
        }
    ),
    "no_generated_target": (
        generator_manifest["target"] is None
        and stored_preflight["target"] is None
        and resolution["target"] is None
        and klean_export.target_statement(generated) is None
    ),
    "no_stage5_candidate": (
        resolution["mode"] == "CLASSIFICATION_ONLY"
        and resolution["stage5_result"] is None
        and resolution["lean_workspace"] is None
        and not Path("/candidate").exists()
    ),
}

result = {
    "all_checks_pass": all(checks.values()),
    "checks": checks,
    "computed": {
        "discovery_manifest_sha256": stage3_hash,
        "generated_tree_sha256": generated_hash,
        "generation_producer_sources_sha256": producer_pipeline_hash,
        "k_audit_sha256": k_audit_pipeline_hash,
        "k_workspace_sha256": stage1_pipeline_hash,
        "klean_generation_sha256": generation_pipeline_hash,
        "stage1_export_sha256": stage1_export_hash,
        "obligation_map_sha256": obligation_map_hash,
        "trust_inventory_sha256": trust_inventory_hash,
        "producer_file_sha256": producer_hashes,
        "producer_image_id": audit_path_image,
        "resolved_input_sha256": canonical_json_sha256(resolution),
        "mechanical_checker_lock_sha256": file_sha256(
            mechanical_lock_path
        ),
    },
}
print(json.dumps(result, indent=2, sort_keys=True))
