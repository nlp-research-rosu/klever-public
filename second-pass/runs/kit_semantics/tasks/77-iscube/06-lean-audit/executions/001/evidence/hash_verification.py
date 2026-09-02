#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

from tools import klean_export, pipeline_contract, stage6_resolution_contract


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


audit = json.loads(Path("/audit-input.json").read_text())
resolution, signed_digest = stage6_resolution_contract.verify_audit_input(audit)
hashes = resolution["hashes"]

stage1_files = {
    path.relative_to("/reference/k-proof").as_posix(): sha256_file(path)
    for path in pipeline_contract._walk_regular_files(
        Path("/reference/k-proof"), "mounted Stage 1 workspace"
    )
}
recorded_stage1_files = resolution["stage1_source_hashes"]

generator_manifest = json.loads(
    Path("/reference/klean-generation/generator-manifest.json").read_text()
)
input_manifest = json.loads(
    Path("/reference/klean-generation/input-manifest.json").read_text()
)
export_result = json.loads(
    Path("/reference/klean-generation/export-result.json").read_text()
)
source_manifest = json.loads(
    Path("/reference/generation-tools/source-manifest.json").read_text()
)

observed = {
    "k_workspace_sha256": pipeline_contract.sha256_tree(
        Path("/reference/k-proof")
    ),
    "stage1_export_sha256": klean_export.tree_digest(
        Path("/reference/k-proof")
    ),
    "discovery_manifest_sha256": sha256_file(
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
    "lean_workspace_sha256": None,
    "lean_invocation_sha256": None,
}

producer_files = {
    name: sha256_file(Path("/reference/generation-tools") / name)
    for name in ("klean.py", "klean_export.py")
}
audit_image_key = Path(
    resolution["generation_producer_sources"]
).name

checks = {
    "signed_audit_input": signed_digest
    == audit["resolved_input_sha256"],
    "resolution_hashes": {
        name: observed[name] == hashes[name] for name in sorted(hashes)
    },
    "selection_hashes": {
        "k_audit": observed["k_audit_sha256"]
        == resolution["selections"]["k_audit"]["artifact_sha256"],
        "klean_generation": observed["klean_generation_sha256"]
        == resolution["selections"]["klean_generation"]["artifact_sha256"],
    },
    "stage1_source_hashes": {
        "recorded_count": len(recorded_stage1_files),
        "observed_count": len(stage1_files),
        "missing_from_mount": sorted(set(recorded_stage1_files) - set(stage1_files)),
        "extra_in_mount": sorted(set(stage1_files) - set(recorded_stage1_files)),
        "content_mismatches": sorted(
            name
            for name in set(recorded_stage1_files) & set(stage1_files)
            if recorded_stage1_files[name] != stage1_files[name]
        ),
    },
    "producer_sources": {
        "observed": producer_files,
        "source_manifest": source_manifest["files"],
        "generator_manifest": {
            "klean.py": generator_manifest["klean_py_sha256"],
            "klean_export.py": generator_manifest["exporter_sha256"],
        },
        "source_manifest_image": source_manifest["generator_image_id"],
        "generator_manifest_image": generator_manifest["provenance"][
            "generator_image_id"
        ],
        "audit_input_image_key": f"sha256:{audit_image_key}",
        "all_file_hashes_match": producer_files
        == source_manifest["files"]
        == {
            "klean.py": generator_manifest["klean_py_sha256"],
            "klean_export.py": generator_manifest["exporter_sha256"],
        },
        "all_image_ids_match": source_manifest["generator_image_id"]
        == generator_manifest["provenance"]["generator_image_id"]
        == f"sha256:{audit_image_key}",
    },
    "sidecar_bindings": {
        "input_stage1": input_manifest["stage1_workspace_sha256"]
        == observed["stage1_export_sha256"],
        "input_discovery": input_manifest[
            "stage3_discovery_manifest_sha256"
        ]
        == observed["discovery_manifest_sha256"],
        "input_verification": input_manifest["verification_sha256"]
        == sha256_file(Path("/reference/k-proof/verification.k")),
        "generator_generated_tree": generator_manifest[
            "generated_tree_sha256"
        ]
        == observed["generated_tree_sha256"],
        "generator_obligation_map": generator_manifest[
            "obligation_map_sha256"
        ]
        == sha256_file(
            Path(
                "/reference/klean-generation/generated/obligation-map.json"
            )
        ),
        "export_stage1": export_result["frozen_input_sha256"]
        == observed["stage1_export_sha256"],
        "export_discovery": export_result[
            "stage3_discovery_manifest_sha256"
        ]
        == observed["discovery_manifest_sha256"],
        "export_generated_tree": export_result["generated_tree_sha256"]
        == observed["generated_tree_sha256"],
        "export_trust_inventory": export_result["trust_inventory_sha256"]
        == sha256_file(
            Path("/reference/klean-generation/trust-inventory.json")
        ),
    },
}

print(
    json.dumps(
        {
            "recorded_resolution_hashes": hashes,
            "observed_resolution_hashes": observed,
            "checks": checks,
        },
        indent=2,
        sort_keys=True,
    )
)
