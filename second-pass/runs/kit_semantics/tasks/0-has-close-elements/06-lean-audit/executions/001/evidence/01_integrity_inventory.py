#!/usr/bin/env python3
"""Independent mounted-input integrity checks and canonical K rule inventory."""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path

from tools.k_rule_inventory import inventory_verification
from tools.klean_audit_contract import _stage1_source_hashes
from tools.klean_export import tree_digest
from tools.pipeline_contract import sha256_tree


def load(path: str) -> dict:
    return json.loads(Path(path).read_text())


def file_sha(path: str) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


audit = load("/audit-input.json")
resolution = audit["resolution"]
recorded = resolution["hashes"]
discovery = load("/reference/lemma-discovery.json")
generator = load("/reference/klean-generation/generator-manifest.json")
source_manifest = load("/reference/generation-tools/source-manifest.json")

observed_hashes = {
    "k_workspace_sha256": sha256_tree(Path("/reference/k-proof")),
    "stage1_export_sha256": tree_digest(Path("/reference/k-proof")),
    "discovery_manifest_sha256": file_sha("/reference/lemma-discovery.json"),
    "k_audit_sha256": sha256_tree(Path("/reference/k-audit")),
    "klean_generation_sha256": sha256_tree(
        Path("/reference/klean-generation")
    ),
    "generation_producer_sources_sha256": sha256_tree(
        Path("/reference/generation-tools")
    ),
    "generated_tree_sha256": tree_digest(
        Path("/reference/klean-generation/generated")
    ),
    "lean_workspace_sha256": sha256_tree(Path("/candidate")),
}
hash_comparison = {
    name: {
        "recorded": recorded.get(name),
        "observed": observed,
        "match": recorded.get(name) == observed,
    }
    for name, observed in observed_hashes.items()
}

recorded_sources = resolution["stage1_source_hashes"]
observed_sources = _stage1_source_hashes(Path("/reference/k-proof"))
source_hash_comparison = {
    "recorded_file_count": len(recorded_sources),
    "observed_file_count": len(observed_sources),
    "missing_from_mount": sorted(set(recorded_sources) - set(observed_sources)),
    "extra_in_mount": sorted(set(observed_sources) - set(recorded_sources)),
    "hash_mismatches": sorted(
        name
        for name in set(recorded_sources) & set(observed_sources)
        if recorded_sources[name] != observed_sources[name]
    ),
}

producer_observed = {
    "klean_export.py": file_sha(
        "/reference/generation-tools/klean_export.py"
    ),
    "klean.py": file_sha("/reference/generation-tools/klean.py"),
}
producer_expected_from_generator = {
    "klean_export.py": generator.get("exporter_sha256"),
    "klean.py": generator.get("klean_py_sha256"),
}
producer_image = generator.get("provenance", {}).get("generator_image_id")
audit_image_key = Path(
    resolution["generation_producer_sources"]
).name
producer_comparison = {
    "observed_files": producer_observed,
    "source_manifest_files": source_manifest.get("files"),
    "generator_manifest_files": producer_expected_from_generator,
    "all_file_hashes_match": (
        producer_observed
        == source_manifest.get("files")
        == producer_expected_from_generator
    ),
    "generator_manifest_image_id": producer_image,
    "source_manifest_image_id": source_manifest.get("generator_image_id"),
    "audit_input_bundle_key": audit_image_key,
    "all_image_ids_match": (
        producer_image == source_manifest.get("generator_image_id")
        and producer_image == f"sha256:{audit_image_key}"
    ),
    "source_manifest_exact_keys": sorted(source_manifest)
    == ["files", "generator_image_id", "schema_version"],
    "bundle_files": sorted(
        p.relative_to("/reference/generation-tools").as_posix()
        for p in Path("/reference/generation-tools").iterdir()
    ),
}

inventory = inventory_verification(Path("/reference/k-proof"))
inventory_ids = [rule["source_rule_id"] for rule in inventory["rules"]]
discovery_ids = [rule["source_rule_id"] for rule in discovery["rules"]]
inventory_counts = Counter(inventory_ids)
discovery_counts = Counter(discovery_ids)
inventory_comparison = {
    "inventory_sha256_recorded": discovery.get("inventory_sha256"),
    "inventory_sha256_reconstructed": inventory["inventory_sha256"],
    "inventory_hash_match": (
        discovery.get("inventory_sha256") == inventory["inventory_sha256"]
    ),
    "inventory_rule_count": len(inventory_ids),
    "discovery_rule_count": len(discovery_ids),
    "inventory_duplicate_ids": sorted(
        key for key, count in inventory_counts.items() if count != 1
    ),
    "discovery_duplicate_ids": sorted(
        key for key, count in discovery_counts.items() if count != 1
    ),
    "omitted_from_discovery": sorted(set(inventory_ids) - set(discovery_ids)),
    "extra_in_discovery": sorted(set(discovery_ids) - set(inventory_ids)),
    "identity_order_match": inventory_ids == discovery_ids,
}

class_by_id = {
    entry["source_rule_id"]: {
        "classification": entry["classification"],
        "rationale": entry["rationale"],
    }
    for entry in discovery["rules"]
}
reconstructed_with_classification = [
    {**rule, **class_by_id.get(rule["source_rule_id"], {})}
    for rule in inventory["rules"]
]

target_comparison = {
    "generator_equals_audit_input": (
        generator.get("target") == resolution.get("target")
    ),
    "generator_equals_recorded_preflight": (
        generator.get("target")
        == resolution.get("stage4_preflight", {}).get("target")
    ),
}

result = {
    "audit_mode_env_expected": resolution["mode"],
    "recorded_vs_observed_hashes": hash_comparison,
    "stage1_source_hash_comparison": source_hash_comparison,
    "producer_comparison": producer_comparison,
    "target_manifest_comparison": target_comparison,
    "inventory_comparison": inventory_comparison,
    "inventory": inventory,
    "reconstructed_rules_with_stage3_classification": (
        reconstructed_with_classification
    ),
}
print(json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False))
