#!/usr/bin/env python3
"""Independently recompute every mounted hash recorded in audit-input.json."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from tools import klean_export, pipeline_contract


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


audit_input = json.loads(Path("/audit-input.json").read_text(encoding="utf-8"))
resolution = audit_input["resolution"]
recorded = resolution["hashes"]
generator = json.loads(
    Path("/reference/klean-generation/generator-manifest.json").read_text(
        encoding="utf-8"
    )
)
source_manifest = json.loads(
    Path("/reference/generation-tools/source-manifest.json").read_text(
        encoding="utf-8"
    )
)

producer_hashes = {
    name: file_hash(Path("/reference/generation-tools") / name)
    for name in ("klean_export.py", "klean.py")
}
producer_checks = {
    "actual": producer_hashes,
    "source_manifest": source_manifest["files"],
    "generator_manifest": {
        "klean_export.py": generator["exporter_sha256"],
        "klean.py": generator["klean_py_sha256"],
    },
    "actual_matches_source_manifest": (
        producer_hashes == source_manifest["files"]
    ),
    "actual_matches_generator_manifest": (
        producer_hashes["klean_export.py"] == generator["exporter_sha256"]
        and producer_hashes["klean.py"] == generator["klean_py_sha256"]
    ),
}
image_id_generator = generator["provenance"]["generator_image_id"]
image_id_source = source_manifest["generator_image_id"]
producer_source_path = Path(resolution["generation_producer_sources"])
image_id_audit_path = "sha256:" + producer_source_path.name
producer_checks["generator_image_id"] = {
    "generator_manifest": image_id_generator,
    "source_manifest": image_id_source,
    "audit_input_path_binding": image_id_audit_path,
    "all_match": (
        image_id_generator == image_id_source == image_id_audit_path
    ),
}

recomputed = {
    "k_workspace_sha256": pipeline_contract.sha256_tree(
        Path("/reference/k-proof")
    ),
    "stage1_export_sha256": klean_export.tree_digest(
        Path("/reference/k-proof")
    ),
    "discovery_manifest_sha256": file_hash(
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
    "lean_workspace_sha256": pipeline_contract.sha256_tree(
        Path("/candidate")
    ),
}
hash_checks = {
    key: {
        "recomputed": value,
        "recorded": recorded.get(key),
        "matches": value == recorded.get(key),
    }
    for key, value in recomputed.items()
}

actual_stage1_sources = {
    path.relative_to(Path("/reference/k-proof")).as_posix(): file_hash(path)
    for path in pipeline_contract._walk_regular_files(
        Path("/reference/k-proof"), "mounted Stage 1 workspace"
    )
}
recorded_stage1_sources = resolution["stage1_source_hashes"]
source_checks = {
    "actual_count": len(actual_stage1_sources),
    "recorded_count": len(recorded_stage1_sources),
    "missing_recorded_paths": sorted(
        set(actual_stage1_sources) - set(recorded_stage1_sources)
    ),
    "extra_recorded_paths": sorted(
        set(recorded_stage1_sources) - set(actual_stage1_sources)
    ),
    "content_mismatches": sorted(
        key
        for key in set(actual_stage1_sources) & set(recorded_stage1_sources)
        if actual_stage1_sources[key] != recorded_stage1_sources[key]
    ),
}
source_checks["exact_match"] = (
    actual_stage1_sources == recorded_stage1_sources
)

target_check = {
    "audit_input_equals_generator_manifest": (
        resolution.get("target") == generator.get("target")
    )
}

all_required_match = (
    producer_checks["actual_matches_source_manifest"]
    and producer_checks["actual_matches_generator_manifest"]
    and producer_checks["generator_image_id"]["all_match"]
    and all(item["matches"] for item in hash_checks.values())
    and source_checks["exact_match"]
    and target_check["audit_input_equals_generator_manifest"]
)

print(
    json.dumps(
        {
            "producer_authentication": producer_checks,
            "recorded_hash_checks": hash_checks,
            "stage1_source_hash_checks": source_checks,
            "target_manifest_check": target_check,
            "all_required_mounted_hashes_match": all_required_match,
            "note": (
                "lean_invocation_sha256 is launcher-recorded but its source "
                "invocation tree is not among the mounted audit inputs."
            ),
        },
        indent=2,
        sort_keys=False,
    )
)
