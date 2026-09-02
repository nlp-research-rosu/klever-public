#!/usr/bin/env python3

import hashlib
import json
import os
from pathlib import Path

from tools import klean_export, pipeline_contract
from tools.k_rule_inventory import inventory_verification
from tools.lemma_discovery_contract import validate_trust_boundary
from tools.stage6_resolution_contract import (
    canonical_json_sha256,
    verify_audit_input,
)


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_hashes(root: Path) -> dict[str, str]:
    return {
        path.relative_to(root).as_posix(): file_sha256(path)
        for path in pipeline_contract._walk_regular_files(
            root, "independent source-hash check"
        )
    }


audit_input = json.loads(Path("/audit-input.json").read_text())
resolution, resolved_digest = verify_audit_input(audit_input)
recorded = resolution["hashes"]

observed = {
    "k_workspace_sha256": pipeline_contract.sha256_tree(
        Path("/reference/k-proof")
    ),
    "stage1_export_sha256": klean_export.tree_digest(
        Path("/reference/k-proof")
    ),
    "discovery_manifest_sha256": file_sha256(
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

producer_manifest = json.loads(
    Path("/reference/generation-tools/source-manifest.json").read_text()
)
generator_manifest = json.loads(
    Path("/reference/klean-generation/generator-manifest.json").read_text()
)
input_manifest = json.loads(
    Path("/reference/klean-generation/input-manifest.json").read_text()
)
export_result = json.loads(
    Path("/reference/klean-generation/export-result.json").read_text()
)
preflight = json.loads(
    Path("/reference/klean-generation/preflight.json").read_text()
)
obligation_map_path = Path(
    "/reference/klean-generation/generated/obligation-map.json"
)
obligation_map = json.loads(obligation_map_path.read_text())
trust_inventory_path = Path(
    "/reference/klean-generation/trust-inventory.json"
)
toolchain_lock = json.loads(
    Path("/reference/klean-toolchain.lock.json").read_text()
)

inventory = inventory_verification(Path("/reference/k-proof"))
validated = validate_trust_boundary(
    Path("/reference/k-proof"), Path("/reference/lemma-discovery.json")
)
canonical_ids = [
    rule["source_rule_id"] for rule in inventory["rules"]
]
discovery = json.loads(Path("/reference/lemma-discovery.json").read_text())
discovery_ids = [
    rule["source_rule_id"] for rule in discovery["rules"]
]

producer_file_hashes = {
    name: file_sha256(Path("/reference/generation-tools") / name)
    for name in ("klean.py", "klean_export.py")
}
producer_image_from_audit_path = (
    "sha256:"
    + Path(resolution["generation_producer_sources"]).name
)

structure_checks = {
    "audit_mode_env_matches_resolution": (
        os.environ.get("AUDIT_MODE") == resolution["mode"]
    ),
    "resolved_input_sha256": {
        "recorded": audit_input["resolved_input_sha256"],
        "observed": canonical_json_sha256(resolution),
        "matches": resolved_digest
        == audit_input["resolved_input_sha256"],
    },
    "stage1_source_hashes": {
        "recorded": resolution["stage1_source_hashes"],
        "observed": source_hashes(Path("/reference/k-proof")),
        "matches": resolution["stage1_source_hashes"]
        == source_hashes(Path("/reference/k-proof")),
    },
    "producer_file_hashes": {
        "observed": producer_file_hashes,
        "source_manifest": producer_manifest["files"],
        "generator_manifest": {
            "klean.py": generator_manifest["klean_py_sha256"],
            "klean_export.py": generator_manifest["exporter_sha256"],
        },
        "matches_all": (
            producer_file_hashes == producer_manifest["files"]
            == {
                "klean.py": generator_manifest["klean_py_sha256"],
                "klean_export.py": generator_manifest[
                    "exporter_sha256"
                ],
            }
        ),
    },
    "producer_image_id": {
        "audit_path": producer_image_from_audit_path,
        "source_manifest": producer_manifest["generator_image_id"],
        "generator_manifest": generator_manifest["provenance"][
            "generator_image_id"
        ],
        "matches_all": (
            producer_image_from_audit_path
            == producer_manifest["generator_image_id"]
            == generator_manifest["provenance"]["generator_image_id"]
        ),
    },
    "toolchain_lock_matches_generator": (
        generator_manifest["toolchain"] == toolchain_lock
    ),
    "canonical_rule_ids": canonical_ids,
    "discovery_rule_ids": discovery_ids,
    "canonical_discovery_same_order": canonical_ids == discovery_ids,
    "canonical_unique": len(canonical_ids) == len(set(canonical_ids)),
    "discovery_unique": len(discovery_ids) == len(set(discovery_ids)),
    "inventory_hash_matches_discovery": (
        inventory["inventory_sha256"]
        == discovery["inventory_sha256"]
    ),
    "inventory_hash_matches_input_manifest": (
        inventory["inventory_sha256"]
        == input_manifest["inventory_sha256"]
    ),
    "verification_hash_matches_input_manifest": (
        inventory["verification_sha256"]
        == input_manifest["verification_sha256"]
    ),
    "independent_domain_rule_ids": [
        rule["source_rule_id"] for rule in validated["domain_lemmas"]
    ],
    "obligation_map_source_rule_ids": [
        rule["source_rule_id"]
        for rule in obligation_map["source_rules"]
    ],
    "obligation_source_rule_ids": [
        obligation["source_rule_id"]
        for obligation in obligation_map["obligations"]
    ],
    "input_manifest_source_rule_ids": [
        rule["source_rule_id"]
        for rule in input_manifest["source_rules"]
    ],
    "obligation_count_consistent": (
        len(obligation_map["obligations"])
        == generator_manifest["obligation_count"]
        == export_result["obligation_count"]
        == preflight["obligation_count"]
        == resolution["stage4_preflight"]["obligation_count"]
        == 0
    ),
    "empty_trust_parameters": (
        obligation_map["trust_parameters"] == []
    ),
    "obligation_map_sha256": {
        "recorded": generator_manifest["obligation_map_sha256"],
        "observed": file_sha256(obligation_map_path),
        "matches": generator_manifest["obligation_map_sha256"]
        == file_sha256(obligation_map_path),
    },
    "target_statement": klean_export.target_statement(
        Path("/reference/klean-generation/generated")
    ),
    "expected_target_definition": klean_export.expected_target_definition(
        obligation_map
    ),
    "all_recorded_targets_null": (
        generator_manifest["target"] is None
        and preflight["target"] is None
        and resolution["target"] is None
        and resolution["stage4_preflight"]["target"] is None
    ),
    "status_consistent": (
        export_result["status"]
        == preflight["status"]
        == resolution["selections"]["klean_generation"]["status"]
        == "KLEAN_NO_OBLIGATIONS"
    ),
    "preflight_exactly_bound_in_audit_input": (
        preflight == resolution["stage4_preflight"]
    ),
    "trust_inventory_sha256": {
        "recorded": export_result["trust_inventory_sha256"],
        "observed": file_sha256(trust_inventory_path),
        "matches": export_result["trust_inventory_sha256"]
        == file_sha256(trust_inventory_path),
    },
    "generator_provenance": {
        "stage1_matches": generator_manifest["provenance"][
            "stage1_workspace_sha256"
        ]
        == observed["stage1_export_sha256"],
        "stage3_matches": generator_manifest["provenance"][
            "stage3_discovery_manifest_sha256"
        ]
        == observed["discovery_manifest_sha256"],
        "inventory_matches": generator_manifest["provenance"][
            "inventory_sha256"
        ]
        == inventory["inventory_sha256"],
    },
    "input_manifest_bindings": {
        "frozen_input_matches": input_manifest["frozen_input_sha256"]
        == observed["stage1_export_sha256"],
        "stage1_matches": input_manifest["stage1_workspace_sha256"]
        == observed["stage1_export_sha256"],
        "stage3_matches": input_manifest[
            "stage3_discovery_manifest_sha256"
        ]
        == observed["discovery_manifest_sha256"],
        "verification_matches": input_manifest["verification_sha256"]
        == inventory["verification_sha256"],
    },
    "export_result_bindings": {
        "frozen_input_matches": export_result["frozen_input_sha256"]
        == observed["stage1_export_sha256"],
        "stage3_matches": export_result[
            "stage3_discovery_manifest_sha256"
        ]
        == observed["discovery_manifest_sha256"],
        "generated_tree_matches": export_result[
            "generated_tree_sha256"
        ]
        == observed["generated_tree_sha256"],
    },
    "classification_only_has_no_candidate": (
        not Path("/candidate").exists()
    ),
    "classification_only_has_no_stage5_result": (
        resolution["stage5_result"] is None
    ),
    "selection_hashes_match_resolution": {
        "k_audit": resolution["selections"]["k_audit"][
            "artifact_sha256"
        ]
        == observed["k_audit_sha256"],
        "klean_generation": resolution["selections"][
            "klean_generation"
        ]["artifact_sha256"]
        == observed["klean_generation_sha256"],
    },
}

print("RECORDED HASHES")
print(json.dumps(recorded, indent=2, sort_keys=True))
print("OBSERVED HASHES")
print(json.dumps(observed, indent=2, sort_keys=True))
print("HASH MATCHES")
print(
    json.dumps(
        {
            key: observed[key] == recorded[key]
            for key in sorted(recorded)
        },
        indent=2,
        sort_keys=True,
    )
)
print("STRUCTURE CHECKS")
print(json.dumps(structure_checks, indent=2, sort_keys=True))
