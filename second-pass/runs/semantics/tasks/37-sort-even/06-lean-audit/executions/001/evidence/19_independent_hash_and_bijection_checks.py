#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from tools.k_rule_inventory import inventory_verification
from tools.klean_export import target_statement, tree_digest
from tools.pipeline_contract import sha256_tree


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


audit_input = json.loads(Path("/audit-input.json").read_text())
resolution = audit_input["resolution"]
discovery = json.loads(Path("/reference/lemma-discovery.json").read_text())
inventory = inventory_verification(Path("/reference/k-proof"))
generator = json.loads(
    Path("/reference/klean-generation/generator-manifest.json").read_text()
)
source_manifest = json.loads(
    Path("/reference/generation-tools/source-manifest.json").read_text()
)
obligation_map = json.loads(
    Path(
        "/reference/klean-generation/generated/obligation-map.json"
    ).read_text()
)

reconstructed_ids = [
    rule["source_rule_id"] for rule in inventory["rules"]
]
classified_ids = [
    rule["source_rule_id"] for rule in discovery["rules"]
]
domain_ids = [
    rule["source_rule_id"]
    for rule in discovery["rules"]
    if rule["classification"] == "DOMAIN_LEMMA"
]
obligation_ids = [
    obligation["source_rule_id"]
    for obligation in obligation_map["obligations"]
]
source_rule_ids = [
    rule["source_rule_id"] for rule in obligation_map["source_rules"]
]

stage1_hashes = {
    str(path.relative_to("/reference/k-proof")): sha256_file(path)
    for path in sorted(Path("/reference/k-proof").rglob("*"))
    if path.is_file()
}

producer_files = {
    name: sha256_file(Path("/reference/generation-tools") / name)
    for name in ("klean.py", "klean_export.py")
}
launcher_generator_image = (
    Path(resolution["generation_producer_sources"]).name
)

tree_hashes = {
    "generation_producer_sources_pipeline": sha256_tree(
        Path("/reference/generation-tools")
    ),
    "k_workspace_pipeline": sha256_tree(Path("/reference/k-proof")),
    "k_workspace_klean": tree_digest(Path("/reference/k-proof")),
    "k_audit_pipeline": sha256_tree(Path("/reference/k-audit")),
    "klean_generation_pipeline": sha256_tree(
        Path("/reference/klean-generation")
    ),
    "generated_project_klean": tree_digest(
        Path("/reference/klean-generation/generated")
    ),
    "candidate_pipeline": sha256_tree(Path("/candidate")),
}

result = {
    "producer_authentication": {
        "actual_files": producer_files,
        "source_manifest_files": source_manifest["files"],
        "generator_manifest_files": {
            "klean.py": generator["klean_py_sha256"],
            "klean_export.py": generator["exporter_sha256"],
        },
        "all_file_hashes_match": (
            producer_files == source_manifest["files"]
            and producer_files["klean.py"] == generator["klean_py_sha256"]
            and producer_files["klean_export.py"]
            == generator["exporter_sha256"]
        ),
        "source_manifest_image_id": source_manifest["generator_image_id"],
        "generator_manifest_image_id": generator["provenance"][
            "generator_image_id"
        ],
        "launcher_generator_image_directory": launcher_generator_image,
        "all_image_ids_match": (
            source_manifest["generator_image_id"]
            == generator["provenance"]["generator_image_id"]
            == f"sha256:{launcher_generator_image}"
        ),
    },
    "inventory_bijection": {
        "reconstructed_rule_count": len(reconstructed_ids),
        "classified_rule_count": len(classified_ids),
        "reconstructed_unique": len(set(reconstructed_ids))
        == len(reconstructed_ids),
        "classified_unique": len(set(classified_ids)) == len(classified_ids),
        "ordered_ids_equal": reconstructed_ids == classified_ids,
        "inventory_hash_actual": inventory["inventory_sha256"],
        "inventory_hash_discovery": discovery["inventory_sha256"],
        "inventory_hash_equal": inventory["inventory_sha256"]
        == discovery["inventory_sha256"],
        "verification_sha256": inventory["verification_sha256"],
        "verification_module": inventory["verification_module"],
        "verification_modules": inventory["verification_modules"],
    },
    "stage4_bijection": {
        "domain_ids": domain_ids,
        "source_rule_ids": source_rule_ids,
        "obligation_ids": obligation_ids,
        "ordered_domain_source_equal": domain_ids == source_rule_ids,
        "ordered_domain_obligation_equal": domain_ids == obligation_ids,
        "unique_obligations": len(set(obligation_ids))
        == len(obligation_ids),
        "target_actual": target_statement(
            Path("/reference/klean-generation/generated")
        ),
        "target_manifest": generator["target"],
        "target_exactly_equal": target_statement(
            Path("/reference/klean-generation/generated")
        )
        == generator["target"]
        == resolution["target"],
    },
    "tree_hashes": tree_hashes,
    "tree_hash_comparisons": {
        "generation_producer_sources": (
            tree_hashes["generation_producer_sources_pipeline"]
            == resolution["hashes"][
                "generation_producer_sources_sha256"
            ]
        ),
        "k_workspace_pipeline": (
            tree_hashes["k_workspace_pipeline"]
            == resolution["hashes"]["k_workspace_sha256"]
        ),
        "k_workspace_klean": (
            tree_hashes["k_workspace_klean"]
            == resolution["hashes"]["stage1_export_sha256"]
        ),
        "k_audit_pipeline": (
            tree_hashes["k_audit_pipeline"]
            == resolution["hashes"]["k_audit_sha256"]
        ),
        "klean_generation_pipeline": (
            tree_hashes["klean_generation_pipeline"]
            == resolution["hashes"]["klean_generation_sha256"]
        ),
        "generated_project_klean": (
            tree_hashes["generated_project_klean"]
            == resolution["hashes"]["generated_tree_sha256"]
        ),
        "candidate_pipeline": (
            tree_hashes["candidate_pipeline"]
            == resolution["hashes"]["lean_workspace_sha256"]
        ),
    },
    "stage1_source_hashes": {
        "actual_count": len(stage1_hashes),
        "recorded_count": len(resolution["stage1_source_hashes"]),
        "exactly_equal": stage1_hashes
        == resolution["stage1_source_hashes"],
        "actual": stage1_hashes,
    },
    "mounted_file_hashes": {
        "discovery_manifest": sha256_file(
            Path("/reference/lemma-discovery.json")
        ),
        "discovery_manifest_matches": sha256_file(
            Path("/reference/lemma-discovery.json")
        )
        == resolution["hashes"]["discovery_manifest_sha256"],
    },
}

print(json.dumps(result, indent=2, sort_keys=True))
