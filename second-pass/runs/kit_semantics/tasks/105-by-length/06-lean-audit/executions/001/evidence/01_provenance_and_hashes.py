#!/usr/bin/env python3
"""Re-hash the mounted audit inputs and Stage 4 producer provenance."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from typing import Any

from tools import klean_export, pipeline_contract, stage6_resolution_contract


AUDIT_INPUT = Path("/audit-input.json")
OUTPUT = Path("/audit-output/evidence/01-provenance-and-hashes.json")


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def equality(actual: Any, expected: Any) -> dict[str, Any]:
    return {
        "actual": actual,
        "expected": expected,
        "match": actual == expected,
    }


audit_document = json.loads(AUDIT_INPUT.read_text())
resolution, resolved_input_sha256 = stage6_resolution_contract.verify_audit_input(
    audit_document
)
hashes = resolution["hashes"]
generator_manifest = json.loads(
    Path("/reference/klean-generation/generator-manifest.json").read_text()
)
source_manifest = json.loads(
    Path("/reference/generation-tools/source-manifest.json").read_text()
)

producer_path = Path(resolution["generation_producer_sources"])
audit_image_key = producer_path.name
audit_image_id = f"sha256:{audit_image_key}"
manifest_image_id = generator_manifest["provenance"]["generator_image_id"]
expected_source_files = {
    "klean_export.py": generator_manifest["exporter_sha256"],
    "klean.py": generator_manifest["klean_py_sha256"],
}
observed_source_files = {
    name: file_sha256(Path("/reference/generation-tools") / name)
    for name in ("klean_export.py", "klean.py")
}

available_tree_hashes = {
    "k_workspace_sha256": pipeline_contract.sha256_tree(
        Path("/reference/k-proof")
    ),
    "stage1_export_sha256": klean_export.tree_digest(
        Path("/reference/k-proof")
    ),
    "k_audit_sha256": pipeline_contract.sha256_tree(
        Path("/reference/k-audit")
    ),
    "klean_generation_sha256": pipeline_contract.sha256_tree(
        Path("/reference/klean-generation")
    ),
    "lean_workspace_sha256": pipeline_contract.sha256_tree(Path("/candidate")),
    "generated_tree_sha256": klean_export.tree_digest(
        Path("/reference/klean-generation/generated")
    ),
    "generation_producer_sources_sha256": pipeline_contract.sha256_tree(
        Path("/reference/generation-tools")
    ),
}

recorded_stage1_files = resolution["stage1_source_hashes"]
observed_stage1_files = {
    relative: file_sha256(Path("/reference/k-proof") / relative)
    for relative in recorded_stage1_files
}
missing_stage1_files = sorted(
    relative
    for relative in recorded_stage1_files
    if not (Path("/reference/k-proof") / relative).is_file()
)
stage1_file_mismatches = sorted(
    relative
    for relative, expected in recorded_stage1_files.items()
    if observed_stage1_files.get(relative) != expected
)

recorded_target = resolution["target"]
manifest_target = generator_manifest["target"]
checks = {
    "audit_mode_environment": equality(
        os.environ.get("AUDIT_MODE"), resolution["mode"]
    ),
    "semantics_mode": equality(
        resolution["semantics_mode"], "SUPPLIED_SEMANTICS"
    ),
    "producer_file_hashes": equality(
        observed_source_files, expected_source_files
    ),
    "producer_source_manifest_files": equality(
        source_manifest.get("files"), expected_source_files
    ),
    "producer_image_source_to_generator": equality(
        source_manifest.get("generator_image_id"), manifest_image_id
    ),
    "producer_image_audit_path_to_generator": equality(
        audit_image_id, manifest_image_id
    ),
    "producer_manifest_exact_keys": equality(
        sorted(source_manifest),
        ["files", "generator_image_id", "schema_version"],
    ),
    "producer_bundle_exact_files": equality(
        sorted(path.name for path in Path("/reference/generation-tools").iterdir()),
        ["klean.py", "klean_export.py", "source-manifest.json"],
    ),
    "discovery_manifest_sha256": equality(
        file_sha256(Path("/reference/lemma-discovery.json")),
        hashes["discovery_manifest_sha256"],
    ),
    "target_identity_audit_to_generator": equality(
        recorded_target, manifest_target
    ),
    "stage1_source_files_missing": equality(missing_stage1_files, []),
    "stage1_source_file_hash_mismatches": equality(
        stage1_file_mismatches, []
    ),
}
for key, actual in available_tree_hashes.items():
    checks[key] = equality(actual, hashes[key])

unavailable_recorded_hashes = {
    "lean_invocation_sha256": {
        "expected": hashes["lean_invocation_sha256"],
        "reason": (
            "The Stage 5 invocation directory is not among the mounted "
            "read-only inputs; the mounted /candidate workspace is checked "
            "against lean_workspace_sha256 instead."
        ),
    }
}

failed_checks = sorted(
    name for name, result in checks.items() if not result["match"]
)
result = {
    "resolved_input_sha256": resolved_input_sha256,
    "audit_input_sha256": file_sha256(AUDIT_INPUT),
    "checks": checks,
    "failed_checks": failed_checks,
    "recorded_hash_without_mounted_input": unavailable_recorded_hashes,
    "stage1_source_file_count": len(recorded_stage1_files),
    "producer_source_manifest": source_manifest,
    "generator_producer_fields": {
        "exporter_sha256": generator_manifest["exporter_sha256"],
        "klean_py_sha256": generator_manifest["klean_py_sha256"],
        "generator_image_id": manifest_image_id,
    },
}
OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
print(json.dumps(result, indent=2, sort_keys=True))
if failed_checks:
    raise SystemExit(1)
