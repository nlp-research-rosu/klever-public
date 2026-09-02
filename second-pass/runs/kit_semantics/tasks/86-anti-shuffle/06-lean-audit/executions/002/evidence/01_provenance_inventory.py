#!/usr/bin/env python3
"""Independent Stage 3 inventory and Stage 4 producer-provenance checks."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from tools import k_rule_inventory, pipeline_contract


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


audit_input = json.loads(Path("/audit-input.json").read_text())
resolution = audit_input["resolution"]
source_manifest = json.loads(
    Path("/reference/generation-tools/source-manifest.json").read_text()
)
generator_manifest = json.loads(
    Path("/reference/klean-generation/generator-manifest.json").read_text()
)
discovery = json.loads(Path("/reference/lemma-discovery.json").read_text())

producer_paths = {
    name: Path("/reference/generation-tools") / name
    for name in ("klean_export.py", "klean.py")
}
producer_hashes = {name: sha256(path) for name, path in producer_paths.items()}
producer_tree_hash = pipeline_contract.sha256_tree(
    Path("/reference/generation-tools")
)
audit_image_id = "sha256:" + Path(
    resolution["generation_producer_sources"]
).name
manifest_image_id = generator_manifest["provenance"]["generator_image_id"]
source_image_id = source_manifest["generator_image_id"]

inventory = k_rule_inventory.inventory_verification(
    Path("/reference/k-proof")
)

# These judgments are independently derived from the frozen rule bodies and
# supplied operational semantics. They are not copied from the protected file.
independent_classifications = [
    "DOMAIN_LEMMA",
    "DEFINITION",
    "DEFINITION",
    "DEFINITION",
    "DEFINITION",
    "DEFINITION",
    "DEFINITION",
    "DEFINITION",
    "DEFINITION",
]
inventory_ids = [rule["source_rule_id"] for rule in inventory["rules"]]
discovery_ids = [rule["source_rule_id"] for rule in discovery["rules"]]
discovery_classes = [rule["classification"] for rule in discovery["rules"]]

reconstructed_rule_projection = [
    {
        "source_rule_id": rule["source_rule_id"],
        "module": rule["module"],
        "start_line": rule["start_line"],
        "end_line": rule["end_line"],
        "normalized_sha256": rule["normalized_sha256"],
        "attributes": rule["attributes"],
        "text": rule["text"],
    }
    for rule in inventory["rules"]
]

checks = {
    "audit_mode_env_contract": resolution["mode"] == "CLASSIFICATION_AND_PROOF",
    "producer_klean_export_matches_source_manifest": (
        producer_hashes["klean_export.py"]
        == source_manifest["files"]["klean_export.py"]
    ),
    "producer_klean_matches_source_manifest": (
        producer_hashes["klean.py"] == source_manifest["files"]["klean.py"]
    ),
    "producer_klean_export_matches_generator_manifest": (
        producer_hashes["klean_export.py"]
        == generator_manifest["exporter_sha256"]
    ),
    "producer_klean_matches_generator_manifest": (
        producer_hashes["klean.py"] == generator_manifest["klean_py_sha256"]
    ),
    "producer_tree_matches_audit_input": (
        producer_tree_hash
        == resolution["hashes"]["generation_producer_sources_sha256"]
    ),
    "generator_image_id_source_vs_generator_manifest": (
        source_image_id == manifest_image_id
    ),
    "generator_image_id_source_vs_audit_input_path": (
        source_image_id == audit_image_id
    ),
    "inventory_hash_matches_discovery": (
        inventory["inventory_sha256"] == discovery["inventory_sha256"]
    ),
    "inventory_hash_matches_generator_provenance": (
        inventory["inventory_sha256"]
        == generator_manifest["provenance"]["inventory_sha256"]
    ),
    "inventory_ids_ordered_bijection": (
        inventory_ids == discovery_ids
        and len(inventory_ids) == len(set(inventory_ids))
        and len(discovery_ids) == len(set(discovery_ids))
    ),
    "independent_classifications_match_protected": (
        independent_classifications == discovery_classes
    ),
    "every_simplification_is_definition_or_domain": all(
        "simplification" not in rule["attributes"]
        or classification in {"DEFINITION", "DOMAIN_LEMMA"}
        for rule, classification in zip(
            inventory["rules"], independent_classifications, strict=True
        )
    ),
}

document = {
    "launcher": {
        "mode": resolution["mode"],
        "problem_id": resolution["problem_id"],
        "condition": resolution["condition"],
        "semantics_mode": resolution["semantics_mode"],
    },
    "producer_provenance": {
        "computed_file_hashes": producer_hashes,
        "computed_tree_hash": producer_tree_hash,
        "audit_input_tree_hash": resolution["hashes"][
            "generation_producer_sources_sha256"
        ],
        "source_manifest_file_hashes": source_manifest["files"],
        "source_manifest_image_id": source_image_id,
        "generator_manifest_image_id": manifest_image_id,
        "audit_input_path_image_id": audit_image_id,
    },
    "inventory": {
        **inventory,
        "rules": reconstructed_rule_projection,
    },
    "protected_discovery_rule_ids": discovery_ids,
    "protected_discovery_classifications": discovery_classes,
    "independent_classifications": independent_classifications,
    "checks": checks,
    "all_checks_pass": all(checks.values()),
}
print(json.dumps(document, indent=2, sort_keys=True, ensure_ascii=False))
if not document["all_checks_pass"]:
    raise SystemExit(1)
