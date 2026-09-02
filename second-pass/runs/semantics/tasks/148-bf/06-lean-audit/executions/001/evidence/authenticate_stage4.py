#!/usr/bin/env python3
"""Authenticate Stage 4 producer sources and immutable input bindings."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from tools.klean_export import tree_digest
from tools.pipeline_contract import sha256_tree


AUDIT_INPUT = Path("/audit-input.json")
PRODUCERS = Path("/reference/generation-tools")
GENERATION = Path("/reference/klean-generation")
STAGE1 = Path("/reference/k-proof")
DISCOVERY = Path("/reference/lemma-discovery.json")


audit = json.loads(AUDIT_INPUT.read_text())["resolution"]
source_manifest = json.loads((PRODUCERS / "source-manifest.json").read_text())
generator_manifest = json.loads(
    (GENERATION / "generator-manifest.json").read_text()
)
input_manifest = json.loads((GENERATION / "input-manifest.json").read_text())
export_result = json.loads((GENERATION / "export-result.json").read_text())

producer_file_hashes = {
    name: hashlib.sha256((PRODUCERS / name).read_bytes()).hexdigest()
    for name in ("klean_export.py", "klean.py")
}
observed_files = sorted(
    path.relative_to(PRODUCERS).as_posix()
    for path in PRODUCERS.rglob("*")
    if path.is_file()
)
producer_tree_hash = sha256_tree(PRODUCERS)
stage1_export_hash = tree_digest(STAGE1)
stage1_pipeline_hash = sha256_tree(STAGE1)
generated_tree_hash = tree_digest(GENERATION / "generated")
generation_pipeline_hash = sha256_tree(GENERATION)
discovery_hash = hashlib.sha256(DISCOVERY.read_bytes()).hexdigest()
image_id = generator_manifest["provenance"]["generator_image_id"]
audit_bundle_key = Path(audit["generation_producer_sources"]).name

checks = {
    "producer_bundle_exact_files": observed_files
    == ["klean.py", "klean_export.py", "source-manifest.json"],
    "source_manifest_exact_keys": set(source_manifest)
    == {"schema_version", "generator_image_id", "files"},
    "source_manifest_schema": source_manifest.get("schema_version") == 1,
    "exporter_hash_matches_source_manifest": producer_file_hashes[
        "klean_export.py"
    ]
    == source_manifest.get("files", {}).get("klean_export.py"),
    "klean_hash_matches_source_manifest": producer_file_hashes["klean.py"]
    == source_manifest.get("files", {}).get("klean.py"),
    "exporter_hash_matches_generator_manifest": producer_file_hashes[
        "klean_export.py"
    ]
    == generator_manifest.get("exporter_sha256"),
    "klean_hash_matches_generator_manifest": producer_file_hashes["klean.py"]
    == generator_manifest.get("klean_py_sha256"),
    "image_matches_source_and_generator_manifests": image_id
    == source_manifest.get("generator_image_id"),
    "image_matches_audit_bundle_path": image_id.removeprefix("sha256:")
    == audit_bundle_key,
    "producer_tree_matches_audit_input": producer_tree_hash
    == audit["hashes"]["generation_producer_sources_sha256"],
    "stage1_export_matches_audit_input": stage1_export_hash
    == audit["hashes"]["stage1_export_sha256"],
    "stage1_export_matches_stage4_manifests": stage1_export_hash
    == input_manifest.get("frozen_input_sha256")
    == input_manifest.get("stage1_workspace_sha256")
    == generator_manifest.get("provenance", {}).get("stage1_workspace_sha256")
    == export_result.get("frozen_input_sha256"),
    "stage1_pipeline_tree_matches_audit_input": stage1_pipeline_hash
    == audit["hashes"]["k_workspace_sha256"],
    "discovery_hash_matches_every_binding": discovery_hash
    == audit["hashes"]["discovery_manifest_sha256"]
    == input_manifest.get("stage3_discovery_manifest_sha256")
    == generator_manifest.get("provenance", {}).get(
        "stage3_discovery_manifest_sha256"
    )
    == export_result.get("stage3_discovery_manifest_sha256"),
    "generated_tree_matches_every_binding": generated_tree_hash
    == audit["hashes"]["generated_tree_sha256"]
    == generator_manifest.get("generated_tree_sha256")
    == export_result.get("generated_tree_sha256"),
    "generation_pipeline_tree_matches_audit_input": generation_pipeline_hash
    == audit["hashes"]["klean_generation_sha256"],
}

result = {
    "status": "PASS" if all(checks.values()) else "AUDIT_ERROR",
    "checks": checks,
    "producer_file_hashes": producer_file_hashes,
    "producer_tree_sha256": producer_tree_hash,
    "producer_image_id": image_id,
    "audit_bundle_key": audit_bundle_key,
    "stage1_export_sha256": stage1_export_hash,
    "stage1_pipeline_tree_sha256": stage1_pipeline_hash,
    "discovery_manifest_sha256": discovery_hash,
    "generated_tree_sha256": generated_tree_hash,
    "generation_pipeline_tree_sha256": generation_pipeline_hash,
}
print(json.dumps(result, indent=2, sort_keys=True))
raise SystemExit(0 if result["status"] == "PASS" else 2)
