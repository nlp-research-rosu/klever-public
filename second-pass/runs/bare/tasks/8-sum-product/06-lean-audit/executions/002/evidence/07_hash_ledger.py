#!/usr/bin/env python3
import hashlib
import json
import os
from pathlib import Path

from tools import klean_export, pipeline_contract
from tools.stage6_resolution_contract import canonical_json_sha256, verify_audit_input

audit_path = Path("/audit-input.json")
audit = json.loads(audit_path.read_text())
resolution, verified_resolution_digest = verify_audit_input(audit)
recorded = resolution["hashes"]

actual = {
    "k_workspace_sha256": pipeline_contract.sha256_tree(Path("/reference/k-proof")),
    "stage1_export_sha256": klean_export.tree_digest(Path("/reference/k-proof")),
    "discovery_manifest_sha256": pipeline_contract.sha256_file(
        Path("/reference/lemma-discovery.json")
    ),
    "k_audit_sha256": pipeline_contract.sha256_tree(Path("/reference/k-audit")),
    "klean_generation_sha256": pipeline_contract.sha256_tree(
        Path("/reference/klean-generation")
    ),
    "generated_tree_sha256": klean_export.tree_digest(
        Path("/reference/klean-generation/generated")
    ),
    "lean_workspace_sha256": (
        pipeline_contract.sha256_tree(Path("/candidate"))
        if Path("/candidate").is_dir()
        else None
    ),
    "lean_invocation_sha256": None,
}

source_hashes = {
    path.relative_to("/reference/k-proof").as_posix(): hashlib.sha256(
        path.read_bytes()
    ).hexdigest()
    for path in sorted(Path("/reference/k-proof").rglob("*"))
    if path.is_file() and not path.is_symlink()
}

generation = Path("/reference/klean-generation")
generated = generation / "generated"
generator_manifest = json.loads((generation / "generator-manifest.json").read_text())
input_manifest = json.loads((generation / "input-manifest.json").read_text())
export_result = json.loads((generation / "export-result.json").read_text())
stored_preflight = json.loads((generation / "preflight.json").read_text())
toolchain = json.loads(Path("/reference/klean-toolchain.lock.json").read_text())

sidecar_actual = {
    name: hashlib.sha256((generation / name).read_bytes()).hexdigest()
    for name in (
        "input-manifest.json",
        "generator-manifest.json",
        "export-result.json",
        "preflight.json",
        "trust-inventory.json",
    )
}
generated_sidecar_actual = {
    "obligation-map.json": hashlib.sha256(
        (generated / "obligation-map.json").read_bytes()
    ).hexdigest()
}

checks = {
    "resolution_digest": verified_resolution_digest
    == audit["resolved_input_sha256"]
    == canonical_json_sha256(resolution),
    "audit_mode_env": os.environ.get("AUDIT_MODE") == resolution["mode"],
    "all_launcher_tree_and_file_hashes": actual == recorded,
    "all_stage1_source_hashes": source_hashes == resolution["stage1_source_hashes"],
    "stage2_selection_hash": resolution["selections"]["k_audit"]["artifact_sha256"]
    == actual["k_audit_sha256"],
    "stage4_selection_hash": resolution["selections"]["klean_generation"][
        "artifact_sha256"
    ]
    == actual["klean_generation_sha256"],
    "stage4_generated_tree_manifest": generator_manifest["generated_tree_sha256"]
    == actual["generated_tree_sha256"],
    "stage4_input_workspace_bindings": input_manifest["frozen_input_sha256"]
    == input_manifest["stage1_workspace_sha256"]
    == actual["stage1_export_sha256"],
    "stage4_discovery_bindings": input_manifest[
        "stage3_discovery_manifest_sha256"
    ]
    == generator_manifest["provenance"]["stage3_discovery_manifest_sha256"]
    == export_result["stage3_discovery_manifest_sha256"]
    == actual["discovery_manifest_sha256"],
    "stage4_workspace_provenance": generator_manifest["provenance"][
        "stage1_workspace_sha256"
    ]
    == actual["stage1_export_sha256"],
    "obligation_map_file_hash": generator_manifest["obligation_map_sha256"]
    == generated_sidecar_actual["obligation-map.json"],
    "trust_inventory_file_hash": export_result["trust_inventory_sha256"]
    == sidecar_actual["trust-inventory.json"],
    "export_generated_tree_binding": export_result["generated_tree_sha256"]
    == actual["generated_tree_sha256"],
    "export_workspace_binding": export_result["frozen_input_sha256"]
    == actual["stage1_export_sha256"],
    "toolchain_lock_document": generator_manifest["toolchain"] == toolchain,
    "stored_preflight_equals_launcher": stored_preflight
    == resolution["stage4_preflight"],
    "classification_only_has_no_candidate": resolution["mode"]
    == "CLASSIFICATION_ONLY"
    and not Path("/candidate").exists()
    and resolution["lean_workspace"] is None
    and resolution["lean_invocation"] is None
    and recorded["lean_workspace_sha256"] is None
    and recorded["lean_invocation_sha256"] is None,
    "target_null_everywhere": resolution["target"] is None
    and resolution["stage4_preflight"]["target"] is None
    and generator_manifest["target"] is None,
}

print(
    json.dumps(
        {
            "audit_input_sha256": hashlib.sha256(audit_path.read_bytes()).hexdigest(),
            "recorded_hashes": recorded,
            "actual_hashes": actual,
            "recorded_stage1_source_hashes": resolution["stage1_source_hashes"],
            "actual_stage1_source_hashes": source_hashes,
            "sidecar_actual_sha256": sidecar_actual,
            "generated_sidecar_actual_sha256": generated_sidecar_actual,
            "resolved_input_sha256_recorded": audit["resolved_input_sha256"],
            "resolved_input_sha256_recomputed": canonical_json_sha256(resolution),
            "audit_metadata_mechanical_checker_lock_sha256": audit["audit"][
                "mechanical_checker_lock_sha256"
            ],
            "generator_historical_code_identities": {
                "exporter_sha256": generator_manifest["exporter_sha256"],
                "klean_py_sha256": generator_manifest["klean_py_sha256"],
            },
            "checks": checks,
        },
        indent=2,
        sort_keys=True,
    )
)
