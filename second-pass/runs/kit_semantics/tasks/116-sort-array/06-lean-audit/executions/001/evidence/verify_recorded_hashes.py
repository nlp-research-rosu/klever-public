#!/usr/bin/env python3
"""Recompute recorded file and tree hashes using the trusted hash routines."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from tools import klean_export, pipeline_contract, stage6_resolution_contract


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


audit_document = json.loads(Path("/audit-input.json").read_text())
audit = audit_document["resolution"]
recorded = audit["hashes"]
generation = Path("/reference/klean-generation")
generator_manifest = json.loads((generation / "generator-manifest.json").read_text())
input_manifest = json.loads((generation / "input-manifest.json").read_text())
export_result = json.loads((generation / "export-result.json").read_text())
source_manifest = json.loads(
    Path("/reference/generation-tools/source-manifest.json").read_text()
)

computed = {
    "discovery_manifest_sha256": file_sha256(Path("/reference/lemma-discovery.json")),
    "generated_tree_sha256": klean_export.tree_digest(generation / "generated"),
    "generation_producer_sources_sha256": pipeline_contract.sha256_tree(
        Path("/reference/generation-tools")
    ),
    "k_audit_sha256": pipeline_contract.sha256_tree(Path("/reference/k-audit")),
    "k_workspace_sha256": pipeline_contract.sha256_tree(Path("/reference/k-proof")),
    "klean_generation_sha256": pipeline_contract.sha256_tree(generation),
    "stage1_export_sha256": klean_export.tree_digest(Path("/reference/k-proof")),
}

top_level_checks = {
    key: {"recorded": recorded[key], "computed": value, "match": recorded[key] == value}
    for key, value in computed.items()
}

source_hash_mismatches = []
for relative, expected in audit["stage1_source_hashes"].items():
    path = Path("/reference/k-proof") / relative
    actual = file_sha256(path) if path.is_file() and not path.is_symlink() else None
    if actual != expected:
        source_hash_mismatches.append(
            {"path": relative, "recorded": expected, "computed": actual}
        )

producer_hashes = {
    name: file_sha256(Path("/reference/generation-tools") / name)
    for name in ("klean_export.py", "klean.py")
}
producer_checks = {
    "klean_export_matches_source_manifest": (
        producer_hashes["klean_export.py"] == source_manifest["files"]["klean_export.py"]
    ),
    "klean_export_matches_generator_manifest": (
        producer_hashes["klean_export.py"] == generator_manifest["exporter_sha256"]
    ),
    "klean_matches_source_manifest": (
        producer_hashes["klean.py"] == source_manifest["files"]["klean.py"]
    ),
    "klean_matches_generator_manifest": (
        producer_hashes["klean.py"] == generator_manifest["klean_py_sha256"]
    ),
    "image_id_manifest_agreement": (
        source_manifest["generator_image_id"]
        == generator_manifest["provenance"]["generator_image_id"]
    ),
    "image_id_bound_by_audit_input_path": (
        Path(audit["generation_producer_sources"]).name
        == source_manifest["generator_image_id"].removeprefix("sha256:")
    ),
}

sidecar_checks = {
    "resolved_input_sha256": (
        stage6_resolution_contract.canonical_json_sha256(audit)
        == audit_document["resolved_input_sha256"]
    ),
    "selected_k_audit_hash_matches_resolution": (
        audit["selections"]["k_audit"]["artifact_sha256"]
        == recorded["k_audit_sha256"]
    ),
    "selected_generation_hash_matches_resolution": (
        audit["selections"]["klean_generation"]["artifact_sha256"]
        == recorded["klean_generation_sha256"]
    ),
    "verification_file_sha256": (
        file_sha256(Path("/reference/k-proof/verification.k"))
        == input_manifest["verification_sha256"]
    ),
    "obligation_map_sha256": (
        file_sha256(generation / "generated/obligation-map.json")
        == generator_manifest["obligation_map_sha256"]
    ),
    "trust_inventory_sha256": (
        file_sha256(generation / "trust-inventory.json")
        == export_result["trust_inventory_sha256"]
    ),
    "stage1_hash_manifest_agreement": (
        computed["stage1_export_sha256"]
        == input_manifest["stage1_workspace_sha256"]
        == input_manifest["frozen_input_sha256"]
        == generator_manifest["provenance"]["stage1_workspace_sha256"]
        == export_result["frozen_input_sha256"]
    ),
    "discovery_hash_manifest_agreement": (
        computed["discovery_manifest_sha256"]
        == input_manifest["stage3_discovery_manifest_sha256"]
        == generator_manifest["provenance"]["stage3_discovery_manifest_sha256"]
        == export_result["stage3_discovery_manifest_sha256"]
    ),
    "generated_hash_manifest_agreement": (
        computed["generated_tree_sha256"]
        == generator_manifest["generated_tree_sha256"]
        == export_result["generated_tree_sha256"]
    ),
}

report = {
    "top_level_hashes": top_level_checks,
    "stage1_source_hash_count": len(audit["stage1_source_hashes"]),
    "stage1_source_hash_mismatches": source_hash_mismatches,
    "producer_hashes": producer_hashes,
    "producer_checks": producer_checks,
    "sidecar_checks": sidecar_checks,
}
report["overall"] = (
    all(item["match"] for item in top_level_checks.values())
    and not source_hash_mismatches
    and all(producer_checks.values())
    and all(sidecar_checks.values())
)
print(json.dumps(report, indent=2, sort_keys=True))
