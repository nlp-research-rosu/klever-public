#!/usr/bin/env python3
"""Recompute mounted-input, producer, manifest, and tree bindings."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from tools import klean_export, pipeline_contract, stage6_resolution_contract


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


audit = json.loads(Path("/audit-input.json").read_text(encoding="utf-8"))
resolution = audit["resolution"]
recorded = resolution["hashes"]
source_manifest = json.loads(
    Path("/reference/generation-tools/source-manifest.json").read_text(
        encoding="utf-8"
    )
)
generator_manifest = json.loads(
    Path("/reference/klean-generation/generator-manifest.json").read_text(
        encoding="utf-8"
    )
)

actual = {
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

producer_actual = {
    name: file_sha256(Path("/reference/generation-tools") / name)
    for name in ("klean_export.py", "klean.py")
}
producer_generator_recorded = {
    "klean_export.py": generator_manifest.get("exporter_sha256"),
    "klean.py": generator_manifest.get("klean_py_sha256"),
}

image_from_audit_path = "sha256:" + Path(
    resolution["generation_producer_sources"]
).name
image_checks = {
    "source_manifest_equals_generator_manifest": (
        source_manifest.get("generator_image_id")
        == generator_manifest.get("provenance", {}).get("generator_image_id")
    ),
    "source_manifest_equals_audit_path_binding": (
        source_manifest.get("generator_image_id") == image_from_audit_path
    ),
}

stage1_recorded = resolution["stage1_source_hashes"]
stage1_root = Path("/reference/k-proof")
stage1_actual_files = sorted(
    path.relative_to(stage1_root).as_posix()
    for path in stage1_root.rglob("*")
    if path.is_file() and not path.is_symlink()
)
stage1_mismatches = {
    relative: {
        "recorded": expected,
        "actual": (
            file_sha256(stage1_root / relative)
            if (stage1_root / relative).is_file()
            else None
        ),
    }
    for relative, expected in stage1_recorded.items()
    if not (stage1_root / relative).is_file()
    or file_sha256(stage1_root / relative) != expected
}
stage1_missing_from_record = sorted(
    set(stage1_actual_files) - set(stage1_recorded)
)
stage1_missing_from_mount = sorted(
    set(stage1_recorded) - set(stage1_actual_files)
)

verified_resolution, verified_digest = (
    stage6_resolution_contract.verify_audit_input(audit)
)

report = {
    "audit_mode_env_note": "checked separately in launcher transcript",
    "recorded_hashes": recorded,
    "actual_hashes": actual,
    "hashes_match": actual == recorded,
    "selection_hash_checks": {
        "k_audit": (
            actual["k_audit_sha256"]
            == resolution["selections"]["k_audit"]["artifact_sha256"]
        ),
        "klean_generation": (
            actual["klean_generation_sha256"]
            == resolution["selections"]["klean_generation"][
                "artifact_sha256"
            ]
        ),
    },
    "producer_actual": producer_actual,
    "producer_source_manifest_recorded": source_manifest.get("files"),
    "producer_generator_manifest_recorded": producer_generator_recorded,
    "producer_hashes_match_source_manifest": (
        producer_actual == source_manifest.get("files")
    ),
    "producer_hashes_match_generator_manifest": (
        producer_actual == producer_generator_recorded
    ),
    "image_from_audit_path": image_from_audit_path,
    "image_checks": image_checks,
    "stage1_source_hash_count_recorded": len(stage1_recorded),
    "stage1_source_file_count_actual": len(stage1_actual_files),
    "stage1_source_hash_mismatches": stage1_mismatches,
    "stage1_files_missing_from_record": stage1_missing_from_record,
    "stage1_files_missing_from_mount": stage1_missing_from_mount,
    "resolved_input_digest_recorded": audit["resolved_input_sha256"],
    "resolved_input_digest_verified": verified_digest,
    "resolved_input_digest_matches": (
        verified_digest == audit["resolved_input_sha256"]
        and verified_resolution == resolution
    ),
}
print(json.dumps(report, indent=2, sort_keys=True))
