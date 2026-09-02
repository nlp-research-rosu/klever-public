#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

from tools import klean_export, pipeline_contract


audit_input = json.loads(Path("/audit-input.json").read_text())["resolution"]
expected_hashes = audit_input["hashes"]
stage1 = Path("/reference/k-proof")
generation = Path("/reference/klean-generation")
generated = generation / "generated"
candidate = Path("/candidate")

observed_hashes = {
    "k_workspace_sha256": pipeline_contract.sha256_tree(stage1),
    "stage1_export_sha256": klean_export.tree_digest(stage1),
    "discovery_manifest_sha256": hashlib.sha256(
        Path("/reference/lemma-discovery.json").read_bytes()
    ).hexdigest(),
    "k_audit_sha256": pipeline_contract.sha256_tree(
        Path("/reference/k-audit")
    ),
    "klean_generation_sha256": pipeline_contract.sha256_tree(generation),
    "generation_producer_sources_sha256": pipeline_contract.sha256_tree(
        Path("/reference/generation-tools")
    ),
    "generated_tree_sha256": klean_export.tree_digest(generated),
    "lean_workspace_sha256": pipeline_contract.sha256_tree(candidate),
}

observed_stage1_source_hashes = {
    path.relative_to(stage1).as_posix(): pipeline_contract.sha256_file(path)
    for path in pipeline_contract._walk_regular_files(
        stage1, "mounted Stage 1 workspace"
    )
}

generator_manifest = json.loads(
    (generation / "generator-manifest.json").read_text()
)
input_manifest = json.loads((generation / "input-manifest.json").read_text())
export_result = json.loads((generation / "export-result.json").read_text())
trust_inventory_path = generation / "trust-inventory.json"
obligation_map_path = generated / "obligation-map.json"
obligation_map = json.loads(obligation_map_path.read_text())
target = klean_export.target_statement(generated)
expected_target_definition = klean_export.expected_target_definition(
    obligation_map
)

result = {
    "observed_hashes": observed_hashes,
    "expected_hashes_for_mounted_inputs": {
        key: expected_hashes[key] for key in observed_hashes
    },
    "hash_checks": {
        key: observed_hashes[key] == expected_hashes[key]
        for key in observed_hashes
    },
    "unmounted_recorded_hashes": {
        "lean_invocation_sha256": expected_hashes[
            "lean_invocation_sha256"
        ]
    },
    "stage1_source_hashes_exact": (
        observed_stage1_source_hashes
        == audit_input["stage1_source_hashes"]
    ),
    "stage1_source_file_count": len(observed_stage1_source_hashes),
    "target": target,
    "target_checks": {
        "matches_generator_manifest": target
        == generator_manifest["target"],
        "matches_audit_input": target == audit_input["target"],
        "definition_is_exact_expected_conjunction": (
            target is not None
            and expected_target_definition is not None
            and target["definition_sha256"]
            == klean_export.sha256_text(expected_target_definition)
        ),
        "obligation_map_hash_matches_generator_manifest": (
            hashlib.sha256(obligation_map_path.read_bytes()).hexdigest()
            == generator_manifest["obligation_map_sha256"]
        ),
        "trust_inventory_hash_matches_export_result": (
            hashlib.sha256(trust_inventory_path.read_bytes()).hexdigest()
            == export_result["trust_inventory_sha256"]
        ),
        "generated_tree_matches_generator_manifest": (
            observed_hashes["generated_tree_sha256"]
            == generator_manifest["generated_tree_sha256"]
        ),
        "stage1_export_matches_input_manifest": (
            observed_hashes["stage1_export_sha256"]
            == input_manifest["stage1_workspace_sha256"]
        ),
        "discovery_matches_input_manifest": (
            observed_hashes["discovery_manifest_sha256"]
            == input_manifest["stage3_discovery_manifest_sha256"]
        ),
        "verification_hash_matches_input_manifest": (
            hashlib.sha256((stage1 / "verification.k").read_bytes()).hexdigest()
            == input_manifest["verification_sha256"]
        ),
    },
}

print(json.dumps(result, indent=2, sort_keys=True))
