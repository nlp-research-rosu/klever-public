#!/usr/bin/env python3
"""Independent provenance and Stage 1/Stage 3 inventory checks for this audit."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from tools import k_rule_inventory, pipeline_contract


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


audit_input_path = Path("/audit-input.json")
producer_dir = Path("/reference/generation-tools")
generation_dir = Path("/reference/klean-generation")
workspace = Path("/reference/k-proof")
discovery_path = Path("/reference/lemma-discovery.json")

audit_input = json.loads(audit_input_path.read_text())
source_manifest = json.loads((producer_dir / "source-manifest.json").read_text())
generator_manifest = json.loads(
    (generation_dir / "generator-manifest.json").read_text()
)
discovery = json.loads(discovery_path.read_text())

physical_producer_hashes = {
    name: sha256_file(producer_dir / name)
    for name in ("klean_export.py", "klean.py")
}
audit_resolution = audit_input["resolution"]
audit_producer_image = (
    "sha256:" + Path(audit_resolution["generation_producer_sources"]).name
)
producer_tree_sha256 = pipeline_contract.sha256_tree(producer_dir)
producer_checks = {
    "physical_hashes_match_source_manifest": (
        physical_producer_hashes == source_manifest["files"]
    ),
    "exporter_matches_generator_manifest": (
        physical_producer_hashes["klean_export.py"]
        == generator_manifest["exporter_sha256"]
    ),
    "klean_py_matches_generator_manifest": (
        physical_producer_hashes["klean.py"]
        == generator_manifest["klean_py_sha256"]
    ),
    "source_and_generator_image_match": (
        source_manifest["generator_image_id"]
        == generator_manifest["provenance"]["generator_image_id"]
    ),
    "audit_image_path_matches_manifests": (
        audit_producer_image
        == source_manifest["generator_image_id"]
        == generator_manifest["provenance"]["generator_image_id"]
    ),
    "producer_tree_matches_audit_input": (
        producer_tree_sha256
        == audit_resolution["hashes"]["generation_producer_sources_sha256"]
    ),
}

inventory = k_rule_inventory.inventory_verification(workspace)
rules = inventory["rules"]
manifest_rules = discovery["rules"]
inventory_ids = [rule["source_rule_id"] for rule in rules]
manifest_ids = [rule["source_rule_id"] for rule in manifest_rules]
inventory_checks = {
    "verification_module": inventory["verification_module"],
    "verification_modules": inventory["verification_modules"],
    "verification_sha256": inventory["verification_sha256"],
    "inventory_sha256": inventory["inventory_sha256"],
    "manifest_inventory_sha256": discovery["inventory_sha256"],
    "inventory_hash_matches": (
        inventory["inventory_sha256"] == discovery["inventory_sha256"]
    ),
    "ordered_identity_bijection": inventory_ids == manifest_ids,
    "inventory_id_count": len(inventory_ids),
    "manifest_id_count": len(manifest_ids),
    "inventory_ids_unique": len(inventory_ids) == len(set(inventory_ids)),
    "manifest_ids_unique": len(manifest_ids) == len(set(manifest_ids)),
    "all_source_ids_bind_normalized_hash": all(
        rule["source_rule_id"] == "rule-" + rule["normalized_sha256"]
        for rule in rules
    ),
    "all_rules_classified_once": (
        len(manifest_rules) == len(inventory_ids)
        and all(
            isinstance(rule.get("classification"), str)
            and bool(rule["classification"])
            for rule in manifest_rules
        )
    ),
}

reconstructed_rules = []
for inventory_rule, manifest_rule in zip(rules, manifest_rules, strict=True):
    reconstructed_rules.append(
        {
            **inventory_rule,
            "manifest_classification": manifest_rule["classification"],
            "manifest_rationale": manifest_rule["rationale"],
        }
    )

result = {
    "producer": {
        "physical_hashes": physical_producer_hashes,
        "source_manifest": source_manifest,
        "generator_manifest_provenance": generator_manifest["provenance"],
        "audit_producer_image_from_path": audit_producer_image,
        "producer_tree_sha256": producer_tree_sha256,
        "audit_producer_tree_sha256": audit_resolution["hashes"][
            "generation_producer_sources_sha256"
        ],
        "checks": producer_checks,
    },
    "inventory": {
        "checks": inventory_checks,
        "rules": reconstructed_rules,
    },
    "all_checks_pass": (
        all(producer_checks.values())
        and all(
            value
            for key, value in inventory_checks.items()
            if key
            not in {
                "verification_module",
                "verification_modules",
                "verification_sha256",
                "inventory_sha256",
                "manifest_inventory_sha256",
                "inventory_id_count",
                "manifest_id_count",
            }
        )
    ),
}
print(json.dumps(result, indent=2, sort_keys=True))
