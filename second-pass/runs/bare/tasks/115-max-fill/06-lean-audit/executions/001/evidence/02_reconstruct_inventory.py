#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from tools import klean_export, lemma_discovery_contract, pipeline_contract
from tools.k_rule_inventory import inventory_verification


def load(path: Path) -> object:
    return json.loads(path.read_text())


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


workspace = Path("/reference/k-proof")
discovery_path = Path("/reference/lemma-discovery.json")
generation = Path("/reference/klean-generation")
generated = generation / "generated"
producer = Path("/reference/generation-tools")
audit_input = load(Path("/audit-input.json"))
discovery = load(discovery_path)
generator = load(generation / "generator-manifest.json")
input_manifest = load(generation / "input-manifest.json")
source_manifest = load(producer / "source-manifest.json")

inventory = inventory_verification(workspace)
validated = lemma_discovery_contract.validate_trust_boundary(
    workspace, discovery_path
)

print("=== canonical inventory_verification result ===")
print(json.dumps(inventory, indent=2, sort_keys=True))
print("=== protected Stage 3 manifest ===")
print(json.dumps(discovery, indent=2, sort_keys=True))

canonical_ids = [rule["source_rule_id"] for rule in inventory["rules"]]
manifest_entries = discovery["rules"]
manifest_ids = [entry["source_rule_id"] for entry in manifest_entries]
print("=== independent bijection/order checks ===")
print(f"canonical_count={len(canonical_ids)}")
print(f"manifest_count={len(manifest_ids)}")
print(f"canonical_ids_unique={len(canonical_ids) == len(set(canonical_ids))}")
print(f"manifest_ids_unique={len(manifest_ids) == len(set(manifest_ids))}")
print(f"same_set={set(canonical_ids) == set(manifest_ids)}")
print(f"same_order={canonical_ids == manifest_ids}")
print(
    "inventory_hash_matches_manifest="
    f"{inventory['inventory_sha256'] == discovery['inventory_sha256']}"
)
for index, canonical in enumerate(inventory["rules"]):
    manifest = manifest_entries[index] if index < len(manifest_entries) else {}
    print(
        json.dumps(
            {
                "index": index,
                "canonical": canonical,
                "manifest": manifest,
                "id_at_same_position": (
                    canonical["source_rule_id"]
                    == manifest.get("source_rule_id")
                ),
            },
            sort_keys=True,
        )
    )

print("=== validated classifications and counts ===")
for key in (
    "definitions",
    "operational_rules",
    "proved_derived_lemmas",
    "domain_lemmas",
):
    print(f"{key}={len(validated[key])}")
    for rule in validated[key]:
        print(
            f"{key}: {rule['source_rule_id']} "
            f"lines={rule['start_line']}-{rule['end_line']} "
            f"attributes={rule['attributes']}"
        )

resolved = audit_input["resolution"]
print("=== recomputed hashes and provenance identities ===")
producer_export_sha = sha(producer / "klean_export.py")
producer_klean_sha = sha(producer / "klean.py")
producer_tree_sha = pipeline_contract.sha256_tree(producer)
stage1_export_sha = klean_export.tree_digest(workspace)
stage1_pipeline_sha = pipeline_contract.sha256_tree(workspace)
generated_export_sha = klean_export.tree_digest(generated)
generation_pipeline_sha = pipeline_contract.sha256_tree(generation)
discovery_sha = sha(discovery_path)
image_id = generator["provenance"]["generator_image_id"]
audit_image_key = Path(
    resolved["generation_producer_sources"]
).name
checks = {
    "klean_export_sha256": producer_export_sha,
    "klean_sha256": producer_klean_sha,
    "producer_tree_sha256": producer_tree_sha,
    "stage1_export_sha256": stage1_export_sha,
    "stage1_pipeline_tree_sha256": stage1_pipeline_sha,
    "generated_export_sha256": generated_export_sha,
    "generation_pipeline_tree_sha256": generation_pipeline_sha,
    "discovery_sha256": discovery_sha,
    "generator_image_id": image_id,
    "audit_path_image_key": audit_image_key,
    "producer_export_matches_source_manifest": (
        producer_export_sha == source_manifest["files"]["klean_export.py"]
    ),
    "producer_export_matches_generator_manifest": (
        producer_export_sha == generator["exporter_sha256"]
    ),
    "producer_klean_matches_source_manifest": (
        producer_klean_sha == source_manifest["files"]["klean.py"]
    ),
    "producer_klean_matches_generator_manifest": (
        producer_klean_sha == generator["klean_py_sha256"]
    ),
    "image_matches_source_manifest": (
        image_id == source_manifest["generator_image_id"]
    ),
    "image_matches_audit_input_path": (
        image_id == f"sha256:{audit_image_key}"
    ),
    "producer_tree_matches_audit_input": (
        producer_tree_sha
        == resolved["hashes"]["generation_producer_sources_sha256"]
    ),
    "stage1_export_matches_audit_input": (
        stage1_export_sha == resolved["hashes"]["stage1_export_sha256"]
    ),
    "stage1_export_matches_generator": (
        stage1_export_sha
        == generator["provenance"]["stage1_workspace_sha256"]
    ),
    "stage1_export_matches_input_manifest": (
        stage1_export_sha == input_manifest["stage1_workspace_sha256"]
    ),
    "stage1_pipeline_matches_audit_input": (
        stage1_pipeline_sha == resolved["hashes"]["k_workspace_sha256"]
    ),
    "generated_matches_audit_input": (
        generated_export_sha == resolved["hashes"]["generated_tree_sha256"]
    ),
    "generated_matches_generator": (
        generated_export_sha == generator["generated_tree_sha256"]
    ),
    "generation_pipeline_matches_audit_input": (
        generation_pipeline_sha
        == resolved["hashes"]["klean_generation_sha256"]
    ),
    "discovery_matches_audit_input": (
        discovery_sha == resolved["hashes"]["discovery_manifest_sha256"]
    ),
    "discovery_matches_generator": (
        discovery_sha
        == generator["provenance"]["stage3_discovery_manifest_sha256"]
    ),
    "inventory_matches_generator": (
        inventory["inventory_sha256"]
        == generator["provenance"]["inventory_sha256"]
    ),
    "inventory_matches_input_manifest": (
        inventory["inventory_sha256"] == input_manifest["inventory_sha256"]
    ),
}
print(json.dumps(checks, indent=2, sort_keys=True))

print("=== Stage 1 per-file hashes vs audit input ===")
observed_stage1_files = {
    path.relative_to(workspace).as_posix(): sha(path)
    for path in pipeline_contract._walk_regular_files(
        workspace, "Stage 1 workspace"
    )
}
expected_stage1_files = resolved["stage1_source_hashes"]
print(f"same_file_set={set(observed_stage1_files) == set(expected_stage1_files)}")
for name in sorted(set(observed_stage1_files) | set(expected_stage1_files)):
    print(
        f"{name}: observed={observed_stage1_files.get(name)} "
        f"expected={expected_stage1_files.get(name)} "
        f"match={observed_stage1_files.get(name) == expected_stage1_files.get(name)}"
    )

print("=== generation sidecar/file hashes ===")
for path in sorted(
    (path for path in generation.rglob("*") if path.is_file()),
    key=lambda path: path.relative_to(generation).as_posix(),
):
    print(f"{sha(path)}  {path.relative_to(generation).as_posix()}")
