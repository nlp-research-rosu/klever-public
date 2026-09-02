#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

from tools import klean_export, pipeline_contract, stage6_resolution_contract


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


audit = json.loads(Path("/audit-input.json").read_text())["resolution"]
generation = Path("/reference/klean-generation")
generated = generation / "generated"
k_workspace = Path("/reference/k-proof")
k_audit = Path("/reference/k-audit")
producer = Path("/reference/generation-tools")
discovery = Path("/reference/lemma-discovery.json")

observed_resolution_hashes = {
    "k_workspace_sha256": pipeline_contract.sha256_tree(k_workspace),
    "stage1_export_sha256": klean_export.tree_digest(k_workspace),
    "discovery_manifest_sha256": sha256_file(discovery),
    "k_audit_sha256": pipeline_contract.sha256_tree(k_audit),
    "klean_generation_sha256": pipeline_contract.sha256_tree(generation),
    "generation_producer_sources_sha256": pipeline_contract.sha256_tree(
        producer
    ),
    "generated_tree_sha256": klean_export.tree_digest(generated),
    "lean_workspace_sha256": None,
    "lean_invocation_sha256": None,
}

source_files = sorted(
    path for path in k_workspace.rglob("*") if path.is_file()
)
observed_source_hashes = {
    path.relative_to(k_workspace).as_posix(): sha256_file(path)
    for path in source_files
}

generator_manifest = json.loads(
    (generation / "generator-manifest.json").read_text()
)
input_manifest = json.loads((generation / "input-manifest.json").read_text())
export_result = json.loads((generation / "export-result.json").read_text())
toolchain_lock = json.loads(
    Path("/reference/klean-toolchain.lock.json").read_text()
)

sidecar_observed = {
    "obligation_map_sha256": sha256_file(
        generated / "obligation-map.json"
    ),
    "trust_inventory_sha256": sha256_file(
        generation / "trust-inventory.json"
    ),
    "verification_sha256": sha256_file(
        k_workspace / "verification.k"
    ),
}
sidecar_recorded = {
    "obligation_map_sha256": generator_manifest[
        "obligation_map_sha256"
    ],
    "trust_inventory_sha256": export_result[
        "trust_inventory_sha256"
    ],
    "verification_sha256": input_manifest["verification_sha256"],
}

manifest_bindings = {
    "resolved input digest": (
        stage6_resolution_contract.canonical_json_sha256(audit)
        == json.loads(Path("/audit-input.json").read_text())[
            "resolved_input_sha256"
        ]
    ),
    "selected K audit artifact": (
        audit["selections"]["k_audit"]["artifact_sha256"]
        == observed_resolution_hashes["k_audit_sha256"]
    ),
    "selected Klean generation artifact": (
        audit["selections"]["klean_generation"]["artifact_sha256"]
        == observed_resolution_hashes["klean_generation_sha256"]
    ),
    "generator generated tree": (
        generator_manifest["generated_tree_sha256"]
        == observed_resolution_hashes["generated_tree_sha256"]
    ),
    "generator Stage 1 tree": (
        generator_manifest["provenance"]["stage1_workspace_sha256"]
        == observed_resolution_hashes["stage1_export_sha256"]
    ),
    "input frozen tree": (
        input_manifest["frozen_input_sha256"]
        == observed_resolution_hashes["stage1_export_sha256"]
    ),
    "input Stage 1 tree": (
        input_manifest["stage1_workspace_sha256"]
        == observed_resolution_hashes["stage1_export_sha256"]
    ),
    "generator discovery": (
        generator_manifest["provenance"][
            "stage3_discovery_manifest_sha256"
        ]
        == observed_resolution_hashes["discovery_manifest_sha256"]
    ),
    "input discovery": (
        input_manifest["stage3_discovery_manifest_sha256"]
        == observed_resolution_hashes["discovery_manifest_sha256"]
    ),
    "export Stage 1": (
        export_result["frozen_input_sha256"]
        == observed_resolution_hashes["stage1_export_sha256"]
    ),
    "export discovery": (
        export_result["stage3_discovery_manifest_sha256"]
        == observed_resolution_hashes["discovery_manifest_sha256"]
    ),
    "export generated tree": (
        export_result["generated_tree_sha256"]
        == observed_resolution_hashes["generated_tree_sha256"]
    ),
    "generator toolchain lock": (
        generator_manifest["toolchain"] == toolchain_lock
    ),
    "generator inventory": (
        generator_manifest["provenance"]["inventory_sha256"]
        == input_manifest["inventory_sha256"]
    ),
}

resolution_checks = {
    name: observed_resolution_hashes[name] == expected
    for name, expected in audit["hashes"].items()
}
source_checks = {
    "same_paths": set(observed_source_hashes)
    == set(audit["stage1_source_hashes"]),
    "same_hashes": observed_source_hashes
    == audit["stage1_source_hashes"],
}
sidecar_checks = {
    name: sidecar_observed[name] == sidecar_recorded[name]
    for name in sidecar_observed
}

all_checks = {
    **{f"resolution:{key}": value for key, value in resolution_checks.items()},
    **{f"sources:{key}": value for key, value in source_checks.items()},
    **{f"sidecar:{key}": value for key, value in sidecar_checks.items()},
    **{f"binding:{key}": value for key, value in manifest_bindings.items()},
}

print(
    json.dumps(
        {
            "observed_resolution_hashes": observed_resolution_hashes,
            "recorded_resolution_hashes": audit["hashes"],
            "resolution_checks": resolution_checks,
            "observed_stage1_source_hashes": observed_source_hashes,
            "recorded_stage1_source_hashes": audit[
                "stage1_source_hashes"
            ],
            "source_checks": source_checks,
            "observed_sidecar_hashes": sidecar_observed,
            "recorded_sidecar_hashes": sidecar_recorded,
            "sidecar_checks": sidecar_checks,
            "manifest_bindings": manifest_bindings,
            "all_checks_pass": all(all_checks.values()),
        },
        indent=2,
        sort_keys=True,
    )
)
