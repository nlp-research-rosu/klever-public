#!/usr/bin/env python3
"""Recompute signed-input, source, tree, and Stage 4 manifest bindings."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from tools import (
    klean_export,
    pipeline_contract,
    stage6_resolution_contract,
)


AUDIT_INPUT = Path("/audit-input.json")
WORKSPACE = Path("/reference/k-proof")
K_AUDIT = Path("/reference/k-audit")
DISCOVERY = Path("/reference/lemma-discovery.json")
GENERATION = Path("/reference/klean-generation")
GENERATED = GENERATION / "generated"
PRODUCERS = Path("/reference/generation-tools")
TOOLCHAIN_LOCK = Path("/reference/klean-toolchain.lock.json")


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    envelope = json.loads(AUDIT_INPUT.read_text())
    resolution, resolved_digest = (
        stage6_resolution_contract.verify_audit_input(envelope)
    )
    hashes = resolution["hashes"]
    generator_manifest = json.loads(
        (GENERATION / "generator-manifest.json").read_text()
    )
    input_manifest = json.loads(
        (GENERATION / "input-manifest.json").read_text()
    )
    source_manifest = json.loads(
        (PRODUCERS / "source-manifest.json").read_text()
    )
    export_result = json.loads(
        (GENERATION / "export-result.json").read_text()
    )
    recorded_preflight = json.loads(
        (GENERATION / "preflight.json").read_text()
    )
    obligation_map_path = GENERATED / "obligation-map.json"
    obligation_map = json.loads(obligation_map_path.read_text())
    trust_inventory_path = GENERATION / "trust-inventory.json"
    lock = json.loads(TOOLCHAIN_LOCK.read_text())

    observed_resolution_hashes = {
        "k_workspace_sha256": pipeline_contract.sha256_tree(WORKSPACE),
        "stage1_export_sha256": klean_export.tree_digest(WORKSPACE),
        "discovery_manifest_sha256": sha256_file(DISCOVERY),
        "k_audit_sha256": pipeline_contract.sha256_tree(K_AUDIT),
        "klean_generation_sha256": pipeline_contract.sha256_tree(GENERATION),
        "generation_producer_sources_sha256": (
            pipeline_contract.sha256_tree(PRODUCERS)
        ),
        "generated_tree_sha256": klean_export.tree_digest(GENERATED),
        "lean_workspace_sha256": None,
        "lean_invocation_sha256": None,
    }
    resolution_hash_checks = {
        key: {
            "recorded": hashes.get(key),
            "observed": observed,
            "match": hashes.get(key) == observed,
        }
        for key, observed in observed_resolution_hashes.items()
    }

    stage1_source_hashes = resolution["stage1_source_hashes"]
    observed_stage1_sources = {
        path.relative_to(WORKSPACE).as_posix(): sha256_file(path)
        for path in pipeline_contract._walk_regular_files(
            WORKSPACE, "Stage 1 workspace"
        )
    }
    source_missing = sorted(
        set(stage1_source_hashes) - set(observed_stage1_sources)
    )
    source_extra = sorted(
        set(observed_stage1_sources) - set(stage1_source_hashes)
    )
    source_mismatches = sorted(
        key
        for key in set(stage1_source_hashes) & set(observed_stage1_sources)
        if stage1_source_hashes[key] != observed_stage1_sources[key]
    )

    producer_hashes = {
        name: sha256_file(PRODUCERS / name)
        for name in ("klean_export.py", "klean.py")
    }
    expected_producer_hashes = {
        "klean_export.py": generator_manifest["exporter_sha256"],
        "klean.py": generator_manifest["klean_py_sha256"],
    }
    generator_image_id = generator_manifest["provenance"][
        "generator_image_id"
    ]
    audit_input_image_key = Path(
        resolution["generation_producer_sources"]
    ).name
    producer_file_set = sorted(
        path.relative_to(PRODUCERS).as_posix()
        for path in pipeline_contract._walk_regular_files(
            PRODUCERS, "producer source bundle"
        )
    )

    target = klean_export.target_statement(GENERATED)
    expected_target_definition = klean_export.expected_target_definition(
        obligation_map
    )
    checks = {
        "audit_envelope": {
            "status": "PASS",
            "resolved_input_sha256": resolved_digest,
        },
        "audit_input_copy_sha256": {
            "/audit-input.json": sha256_file(AUDIT_INPUT),
            "/audit-output/audit-input.json": sha256_file(
                Path("/audit-output/audit-input.json")
            ),
            "match": (
                sha256_file(AUDIT_INPUT)
                == sha256_file(Path("/audit-output/audit-input.json"))
            ),
        },
        "resolution_hashes": resolution_hash_checks,
        "stage1_source_hashes": {
            "recorded_count": len(stage1_source_hashes),
            "observed_count": len(observed_stage1_sources),
            "missing": source_missing,
            "extra": source_extra,
            "mismatches": source_mismatches,
            "all_match": not (
                source_missing or source_extra or source_mismatches
            ),
        },
        "producer_provenance": {
            "observed_hashes": producer_hashes,
            "generator_manifest_hashes": expected_producer_hashes,
            "source_manifest_hashes": source_manifest["files"],
            "file_hashes_match_both_manifests": (
                producer_hashes
                == expected_producer_hashes
                == source_manifest["files"]
            ),
            "file_set": producer_file_set,
            "file_set_exact": producer_file_set
            == ["klean.py", "klean_export.py", "source-manifest.json"],
            "generator_manifest_image_id": generator_image_id,
            "source_manifest_image_id": source_manifest[
                "generator_image_id"
            ],
            "audit_input_producer_path_key": audit_input_image_key,
            "image_identity_match": (
                generator_image_id
                == source_manifest["generator_image_id"]
                == f"sha256:{audit_input_image_key}"
            ),
            "tree_hash_match": (
                pipeline_contract.sha256_tree(PRODUCERS)
                == hashes["generation_producer_sources_sha256"]
            ),
        },
        "stage4_bindings": {
            "verification_sha256_observed": sha256_file(
                WORKSPACE / "verification.k"
            ),
            "verification_sha256_recorded": input_manifest[
                "verification_sha256"
            ],
            "verification_sha256_match": (
                sha256_file(WORKSPACE / "verification.k")
                == input_manifest["verification_sha256"]
            ),
            "discovery_sha256_observed": sha256_file(DISCOVERY),
            "input_manifest_discovery_sha256": input_manifest[
                "stage3_discovery_manifest_sha256"
            ],
            "generator_provenance_discovery_sha256": generator_manifest[
                "provenance"
            ]["stage3_discovery_manifest_sha256"],
            "discovery_hashes_match": (
                sha256_file(DISCOVERY)
                == input_manifest["stage3_discovery_manifest_sha256"]
                == generator_manifest["provenance"][
                    "stage3_discovery_manifest_sha256"
                ]
            ),
            "stage1_export_hashes_match": (
                klean_export.tree_digest(WORKSPACE)
                == input_manifest["stage1_workspace_sha256"]
                == input_manifest["frozen_input_sha256"]
                == generator_manifest["provenance"][
                    "stage1_workspace_sha256"
                ]
            ),
            "inventory_hashes_match": (
                input_manifest["inventory_sha256"]
                == generator_manifest["provenance"]["inventory_sha256"]
            ),
            "generated_tree_hashes_match": (
                klean_export.tree_digest(GENERATED)
                == generator_manifest["generated_tree_sha256"]
                == export_result["generated_tree_sha256"]
                == recorded_preflight["generated_tree_sha256"]
                == hashes["generated_tree_sha256"]
            ),
            "obligation_map_sha256_observed": sha256_file(
                obligation_map_path
            ),
            "obligation_map_sha256_recorded": generator_manifest[
                "obligation_map_sha256"
            ],
            "obligation_map_hash_match": (
                sha256_file(obligation_map_path)
                == generator_manifest["obligation_map_sha256"]
            ),
            "trust_inventory_sha256_observed": sha256_file(
                trust_inventory_path
            ),
            "trust_inventory_sha256_recorded": export_result[
                "trust_inventory_sha256"
            ],
            "trust_inventory_hash_match": (
                sha256_file(trust_inventory_path)
                == export_result["trust_inventory_sha256"]
            ),
            "toolchain_manifest_equals_lock": (
                generator_manifest["toolchain"] == lock
            ),
            "toolchain_lock_sha256": sha256_file(TOOLCHAIN_LOCK),
            "audit_input_stage4_preflight_equals_sidecar": (
                resolution["stage4_preflight"] == recorded_preflight
            ),
            "selection_generation_artifact_hash_match": (
                resolution["selections"]["klean_generation"][
                    "artifact_sha256"
                ]
                == pipeline_contract.sha256_tree(GENERATION)
            ),
            "selection_k_audit_artifact_hash_match": (
                resolution["selections"]["k_audit"]["artifact_sha256"]
                == pipeline_contract.sha256_tree(K_AUDIT)
            ),
        },
        "obligation_and_target_shape": {
            "input_manifest_source_rules": input_manifest["source_rules"],
            "obligation_map_source_rules": obligation_map["source_rules"],
            "obligations": obligation_map["obligations"],
            "trust_parameters": obligation_map["trust_parameters"],
            "generator_obligation_count": generator_manifest[
                "obligation_count"
            ],
            "export_obligation_count": export_result["obligation_count"],
            "preflight_obligation_count": recorded_preflight[
                "obligation_count"
            ],
            "target_statement_observed": target,
            "expected_target_definition": expected_target_definition,
            "generator_target": generator_manifest["target"],
            "audit_input_target": resolution["target"],
            "export_status": export_result["status"],
            "preflight_status": recorded_preflight["status"],
            "selected_status": resolution["selections"][
                "klean_generation"
            ]["status"],
            "candidate_present": Path("/candidate").exists(),
        },
    }
    print(json.dumps(checks, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
