#!/usr/bin/env python3
"""Independent cross-check of immutable Stage 3/4 audit bindings."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from tools import (
    klean_export,
    pipeline_contract,
    stage6_resolution_contract,
)
from tools.k_rule_inventory import inventory_verification


def load(path: str) -> dict:
    return json.loads(Path(path).read_text())


def digest(path: str) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


audit = load("/audit-input.json")
resolution = audit["resolution"]
discovery = load("/reference/lemma-discovery.json")
inventory = inventory_verification(Path("/reference/k-proof"))
source_manifest = load("/reference/generation-tools/source-manifest.json")
generator = load("/reference/klean-generation/generator-manifest.json")
input_manifest = load("/reference/klean-generation/input-manifest.json")
export_result = load("/reference/klean-generation/export-result.json")
preflight = load("/reference/klean-generation/preflight.json")
obligation_map = load(
    "/reference/klean-generation/generated/obligation-map.json"
)

inventory_ids = [rule["source_rule_id"] for rule in inventory["rules"]]
discovery_ids = [rule["source_rule_id"] for rule in discovery["rules"]]
classifications = [
    rule["classification"] for rule in discovery["rules"]
]
producer_image = generator["provenance"]["generator_image_id"]
producer_image_key = producer_image.removeprefix("sha256:")
producer_path_key = Path(
    resolution["generation_producer_sources"]
).name

checks = {
    "audit_envelope_digest": (
        audit["resolved_input_sha256"]
        == stage6_resolution_contract.canonical_json_sha256(
            resolution
        )
    ),
    "audit_mode_environment": (
        resolution["mode"] == "CLASSIFICATION_ONLY"
    ),
    "audit_semantics_mode": (
        resolution["semantics_mode"] == "GENERATED_SEMANTICS"
    ),
    "stage1_pipeline_tree_hash": (
        pipeline_contract.sha256_tree(Path("/reference/k-proof"))
        == resolution["hashes"]["k_workspace_sha256"]
    ),
    "stage1_export_tree_hash": (
        klean_export.tree_digest(Path("/reference/k-proof"))
        == resolution["hashes"]["stage1_export_sha256"]
    ),
    "stage1_source_hash_map": (
        {
            path.relative_to("/reference/k-proof").as_posix(): digest(
                str(path)
            )
            for path in pipeline_contract._walk_regular_files(
                Path("/reference/k-proof"), "Stage 1 workspace"
            )
        }
        == resolution["stage1_source_hashes"]
    ),
    "stage2_pipeline_tree_hash": (
        pipeline_contract.sha256_tree(Path("/reference/k-audit"))
        == resolution["hashes"]["k_audit_sha256"]
        == resolution["selections"]["k_audit"]["artifact_sha256"]
    ),
    "discovery_file_hash": (
        digest("/reference/lemma-discovery.json")
        == resolution["hashes"]["discovery_manifest_sha256"]
    ),
    "generation_pipeline_tree_hash": (
        pipeline_contract.sha256_tree(
            Path("/reference/klean-generation")
        )
        == resolution["hashes"]["klean_generation_sha256"]
        == resolution["selections"]["klean_generation"][
            "artifact_sha256"
        ]
    ),
    "generated_export_tree_hash": (
        klean_export.tree_digest(
            Path("/reference/klean-generation/generated")
        )
        == resolution["hashes"]["generated_tree_sha256"]
        == generator["generated_tree_sha256"]
        == export_result["generated_tree_sha256"]
        == preflight["generated_tree_sha256"]
    ),
    "producer_bundle_pipeline_tree_hash": (
        pipeline_contract.sha256_tree(
            Path("/reference/generation-tools")
        )
        == resolution["hashes"][
            "generation_producer_sources_sha256"
        ]
    ),
    "producer_exporter_file_hash": (
        digest("/reference/generation-tools/klean_export.py")
        == generator["exporter_sha256"]
        == source_manifest["files"]["klean_export.py"]
    ),
    "producer_klean_file_hash": (
        digest("/reference/generation-tools/klean.py")
        == generator["klean_py_sha256"]
        == source_manifest["files"]["klean.py"]
    ),
    "producer_manifest_exact_file_set": (
        {
            path.name
            for path in Path("/reference/generation-tools").iterdir()
        }
        == {"klean_export.py", "klean.py", "source-manifest.json"}
    ),
    "generator_image_binding": (
        producer_image
        == source_manifest["generator_image_id"]
        and producer_image_key == producer_path_key
    ),
    "inventory_file_hash": (
        inventory["verification_sha256"]
        == resolution["stage1_source_hashes"]["verification.k"]
        == input_manifest["verification_sha256"]
    ),
    "inventory_hash_binding": (
        inventory["inventory_sha256"]
        == discovery["inventory_sha256"]
        == input_manifest["inventory_sha256"]
        == generator["provenance"]["inventory_sha256"]
    ),
    "inventory_ordered_bijection": (
        inventory_ids == discovery_ids
        and len(inventory_ids) == len(set(inventory_ids))
        and len(discovery_ids) == len(set(discovery_ids))
    ),
    "all_classifications_definitions": (
        classifications == ["DEFINITION"] * len(inventory_ids)
    ),
    "no_simplification_attributes": all(
        "simplification" not in rule["attributes"]
        for rule in inventory["rules"]
    ),
    "no_stage4_domain_sources": (
        input_manifest["source_rules"] == []
        and obligation_map["source_rules"] == []
    ),
    "empty_obligation_bijection": (
        obligation_map["obligations"] == []
        and obligation_map["trust_parameters"] == []
        and generator["obligation_count"] == 0
        and export_result["obligation_count"] == 0
        and preflight["obligation_count"] == 0
    ),
    "obligation_map_file_hash": (
        digest(
            "/reference/klean-generation/generated/obligation-map.json"
        )
        == generator["obligation_map_sha256"]
    ),
    "trust_inventory_file_hash": (
        digest("/reference/klean-generation/trust-inventory.json")
        == export_result["trust_inventory_sha256"]
    ),
    "discovery_hash_binding": (
        digest("/reference/lemma-discovery.json")
        == input_manifest["stage3_discovery_manifest_sha256"]
        == generator["provenance"][
            "stage3_discovery_manifest_sha256"
        ]
        == export_result["stage3_discovery_manifest_sha256"]
        == preflight["stage3_discovery_manifest_sha256"]
    ),
    "stage1_export_hash_binding": (
        klean_export.tree_digest(Path("/reference/k-proof"))
        == input_manifest["frozen_input_sha256"]
        == input_manifest["stage1_workspace_sha256"]
        == generator["provenance"]["stage1_workspace_sha256"]
        == export_result["frozen_input_sha256"]
        == preflight["frozen_input_sha256"]
        == preflight["stage1_workspace_sha256"]
    ),
    "fixed_null_target": (
        klean_export.target_statement(
            Path("/reference/klean-generation/generated")
        )
        is None
        and generator["target"] is None
        and preflight["target"] is None
        and resolution["target"] is None
    ),
    "classification_only_has_no_stage5": (
        resolution["lean_workspace"] is None
        and resolution["lean_invocation"] is None
        and resolution["stage5_result"] is None
        and resolution["hashes"]["lean_workspace_sha256"] is None
        and resolution["hashes"]["lean_invocation_sha256"] is None
        and not Path("/candidate").exists()
    ),
    "toolchain_lock_exact": (
        generator["toolchain"]
        == load("/reference/klean-toolchain.lock.json")
    ),
    "export_status_no_obligations": (
        export_result["status"] == "KLEAN_NO_OBLIGATIONS"
        and preflight["status"] == "KLEAN_NO_OBLIGATIONS"
        and resolution["stage4_preflight"]["status"]
        == "KLEAN_NO_OBLIGATIONS"
    ),
    "mounted_preflight_equals_audit_input": (
        preflight == resolution["stage4_preflight"]
    ),
}

failed = [name for name, passed in checks.items() if not passed]
print(
    json.dumps(
        {
            "checks": checks,
            "failed": failed,
            "observed": {
                "inventory_ids": inventory_ids,
                "discovery_ids": discovery_ids,
                "classifications": classifications,
                "inventory_sha256": inventory["inventory_sha256"],
                "producer_image_id": producer_image,
                "producer_path_key": producer_path_key,
                "target_statement": klean_export.target_statement(
                    Path("/reference/klean-generation/generated")
                ),
            },
            "status": "PASS" if not failed else "FAIL",
        },
        indent=2,
        sort_keys=True,
    )
)

raise SystemExit(1 if failed else 0)
