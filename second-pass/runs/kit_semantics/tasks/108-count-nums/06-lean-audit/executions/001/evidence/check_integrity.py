#!/usr/bin/env python3
"""Independent mechanical integrity checks using the trusted audit modules."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from tools import k_rule_inventory, pipeline_contract


OUTPUT = Path("/audit-output/evidence")
AUDIT_INPUT = Path("/audit-input.json")
WORKSPACE = Path("/reference/k-proof")
DISCOVERY = Path("/reference/lemma-discovery.json")
GENERATION = Path("/reference/klean-generation")
PRODUCERS = Path("/reference/generation-tools")


def load(path: Path) -> dict:
    return json.loads(path.read_text())


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


audit = load(AUDIT_INPUT)["resolution"]
generator = load(GENERATION / "generator-manifest.json")
source_manifest = load(PRODUCERS / "source-manifest.json")
discovery = load(DISCOVERY)

producer_observed = {
    name: file_sha256(PRODUCERS / name)
    for name in ("klean.py", "klean_export.py")
}
producer_expected_generator = {
    "klean.py": generator.get("klean_py_sha256"),
    "klean_export.py": generator.get("exporter_sha256"),
}
generator_image_id = generator.get("provenance", {}).get("generator_image_id")
audit_producer_key = Path(audit["generation_producer_sources"]).name

producer_checks = {
    "observed_files": sorted(
        path.relative_to(PRODUCERS).as_posix()
        for path in pipeline_contract._walk_regular_files(
            PRODUCERS, "mounted producer bundle"
        )
    ),
    "observed_hashes": producer_observed,
    "source_manifest": source_manifest,
    "generator_manifest_expected_hashes": producer_expected_generator,
    "generator_manifest_image_id": generator_image_id,
    "audit_input_producer_path": audit["generation_producer_sources"],
    "audit_input_producer_tree_sha256": audit["hashes"][
        "generation_producer_sources_sha256"
    ],
    "observed_producer_tree_sha256": pipeline_contract.sha256_tree(PRODUCERS),
}
producer_checks["all_match"] = all(
    [
        producer_checks["observed_files"]
        == ["klean.py", "klean_export.py", "source-manifest.json"],
        producer_observed == source_manifest.get("files"),
        producer_observed == producer_expected_generator,
        source_manifest.get("generator_image_id") == generator_image_id,
        generator_image_id == f"sha256:{audit_producer_key}",
        producer_checks["observed_producer_tree_sha256"]
        == producer_checks["audit_input_producer_tree_sha256"],
    ]
)

inventory = k_rule_inventory.inventory_verification(WORKSPACE)
inventory_ids = [rule["source_rule_id"] for rule in inventory["rules"]]
discovery_ids = [rule["source_rule_id"] for rule in discovery["rules"]]
comparison = {
    "inventory_rule_count": len(inventory_ids),
    "discovery_rule_count": len(discovery_ids),
    "inventory_rule_ids": inventory_ids,
    "discovery_rule_ids": discovery_ids,
    "inventory_unique_ids": len(inventory_ids) == len(set(inventory_ids)),
    "discovery_unique_ids": len(discovery_ids) == len(set(discovery_ids)),
    "ordered_ids_equal": inventory_ids == discovery_ids,
    "omitted_from_discovery": sorted(set(inventory_ids) - set(discovery_ids)),
    "extra_in_discovery": sorted(set(discovery_ids) - set(inventory_ids)),
    "recomputed_inventory_sha256": inventory["inventory_sha256"],
    "discovery_inventory_sha256": discovery.get("inventory_sha256"),
    "inventory_hash_equal": (
        inventory["inventory_sha256"] == discovery.get("inventory_sha256")
    ),
}
comparison["bijective_ordered_match"] = all(
    [
        comparison["inventory_unique_ids"],
        comparison["discovery_unique_ids"],
        comparison["ordered_ids_equal"],
        not comparison["omitted_from_discovery"],
        not comparison["extra_in_discovery"],
        comparison["inventory_hash_equal"],
    ]
)

observed_stage1_files = {
    path.relative_to(WORKSPACE).as_posix(): pipeline_contract.sha256_file(path)
    for path in pipeline_contract._walk_regular_files(
        WORKSPACE, "mounted Stage 1 workspace"
    )
}
expected_stage1_files = audit["stage1_source_hashes"]
stage1_hash_check = {
    "observed_file_count": len(observed_stage1_files),
    "expected_file_count": len(expected_stage1_files),
    "missing": sorted(set(expected_stage1_files) - set(observed_stage1_files)),
    "extra": sorted(set(observed_stage1_files) - set(expected_stage1_files)),
    "mismatched": sorted(
        name
        for name in set(observed_stage1_files) & set(expected_stage1_files)
        if observed_stage1_files[name] != expected_stage1_files[name]
    ),
    "observed_workspace_tree_sha256": pipeline_contract.sha256_tree(WORKSPACE),
    "audit_workspace_tree_sha256": audit["hashes"]["k_workspace_sha256"],
}
stage1_hash_check["all_match"] = all(
    [
        not stage1_hash_check["missing"],
        not stage1_hash_check["extra"],
        not stage1_hash_check["mismatched"],
        stage1_hash_check["observed_workspace_tree_sha256"]
        == stage1_hash_check["audit_workspace_tree_sha256"],
    ]
)

(OUTPUT / "producer-authentication.json").write_text(
    json.dumps(producer_checks, indent=2, sort_keys=True) + "\n"
)
(OUTPUT / "inventory-reconstruction.json").write_text(
    json.dumps(inventory, indent=2, sort_keys=True) + "\n"
)
(OUTPUT / "inventory-comparison.json").write_text(
    json.dumps(comparison, indent=2, sort_keys=True) + "\n"
)
(OUTPUT / "stage1-source-hash-check.json").write_text(
    json.dumps(stage1_hash_check, indent=2, sort_keys=True) + "\n"
)

print(json.dumps({
    "producer_authentication": producer_checks["all_match"],
    "inventory_comparison": comparison,
    "stage1_source_hash_check": stage1_hash_check,
}, indent=2, sort_keys=True))

if not producer_checks["all_match"]:
    raise SystemExit("producer source authentication failed")
if not comparison["bijective_ordered_match"]:
    raise SystemExit("Stage 3 inventory comparison failed")
if not stage1_hash_check["all_match"]:
    raise SystemExit("mounted Stage 1 workspace differs from audit input")
