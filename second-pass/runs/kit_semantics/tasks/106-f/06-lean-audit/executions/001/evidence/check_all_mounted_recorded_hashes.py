#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from tools import pipeline_contract, stage6_resolution_contract
from tools.klean_export import tree_digest


def file_sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


document = json.loads(Path("/audit-input.json").read_text())
resolution, resolved_digest = stage6_resolution_contract.verify_audit_input(
    document
)
recorded = resolution["hashes"]

stage1 = Path("/reference/k-proof")
source_hashes = resolution["stage1_source_hashes"]
actual_stage1_files = {
    str(path.relative_to(stage1))
    for path in stage1.rglob("*")
    if path.is_file() and not path.is_symlink()
}
recorded_stage1_files = set(source_hashes)
source_mismatches = []
for relative, expected in source_hashes.items():
    path = stage1 / relative
    actual = file_sha(path) if path.is_file() and not path.is_symlink() else None
    if actual != expected:
        source_mismatches.append(
            {"path": relative, "expected": expected, "actual": actual}
        )

top_level = {
    "k_workspace_sha256": pipeline_contract.sha256_tree(stage1),
    "stage1_export_sha256": tree_digest(stage1),
    "k_audit_sha256": pipeline_contract.sha256_tree(
        Path("/reference/k-audit")
    ),
    "discovery_manifest_sha256": file_sha(
        Path("/reference/lemma-discovery.json")
    ),
    "klean_generation_sha256": pipeline_contract.sha256_tree(
        Path("/reference/klean-generation")
    ),
    "generated_tree_sha256": tree_digest(
        Path("/reference/klean-generation/generated")
    ),
    "generation_producer_sources_sha256": pipeline_contract.sha256_tree(
        Path("/reference/generation-tools")
    ),
    "lean_workspace_sha256": pipeline_contract.sha256_tree(
        Path("/candidate")
    ),
}
top_level_checks = {
    name: actual == recorded[name] for name, actual in top_level.items()
}

preflight = resolution["stage4_preflight"]
cross_checks = {
    "resolved_input_sha256": (
        resolved_digest == document["resolved_input_sha256"]
    ),
    "stage1_file_set_exact": actual_stage1_files
    == recorded_stage1_files,
    "all_777_stage1_file_hashes_match": (
        len(source_hashes) == 777 and not source_mismatches
    ),
    "stage4_preflight_frozen_input_matches": (
        preflight["frozen_input_sha256"]
        == top_level["stage1_export_sha256"]
    ),
    "stage4_preflight_workspace_matches": (
        preflight["stage1_workspace_sha256"]
        == top_level["stage1_export_sha256"]
    ),
    "stage4_preflight_discovery_matches": (
        preflight["stage3_discovery_manifest_sha256"]
        == top_level["discovery_manifest_sha256"]
    ),
    "stage4_preflight_generated_matches": (
        preflight["generated_tree_sha256"]
        == top_level["generated_tree_sha256"]
    ),
    "stage4_preflight_target_matches_resolution": (
        preflight["target"] == resolution["target"]
    ),
    "stage5_workspace_result_matches_resolution": (
        resolution["stage5_result"]["outputs"]["workspace_sha256"]
        == top_level["lean_workspace_sha256"]
    ),
    "selected_k_audit_artifact_matches": (
        resolution["selections"]["k_audit"]["artifact_sha256"]
        == top_level["k_audit_sha256"]
    ),
    "selected_generation_artifact_matches": (
        resolution["selections"]["klean_generation"]["artifact_sha256"]
        == top_level["klean_generation_sha256"]
    ),
}

print(
    "$ PYTHONPATH=/reference python3 "
    "/audit-output/evidence/check_all_mounted_recorded_hashes.py"
)
print("RESOLVED_INPUT")
print(
    json.dumps(
        {
            "actual": resolved_digest,
            "recorded": document["resolved_input_sha256"],
        },
        indent=2,
        sort_keys=True,
    )
)
print("TOP_LEVEL_MOUNTED_HASHES")
print(
    json.dumps(
        {
            name: {
                "actual": top_level[name],
                "recorded": recorded[name],
                "matches": top_level_checks[name],
            }
            for name in sorted(top_level)
        },
        indent=2,
        sort_keys=True,
    )
)
print("STAGE1_FILE_HASH_AUDIT")
print(
    json.dumps(
        {
            "actual_regular_file_count": len(actual_stage1_files),
            "recorded_file_count": len(source_hashes),
            "missing_from_record": sorted(
                actual_stage1_files - recorded_stage1_files
            ),
            "missing_from_mount": sorted(
                recorded_stage1_files - actual_stage1_files
            ),
            "mismatches": source_mismatches,
        },
        indent=2,
        sort_keys=True,
    )
)
print("CROSS_CHECKS")
print(json.dumps(cross_checks, indent=2, sort_keys=True))
print(
    "UNMOUNTED_RECORD="
    + json.dumps(
        {
            "name": "lean_invocation_sha256",
            "recorded": recorded["lean_invocation_sha256"],
            "reason": (
                "the launcher did not mount the Stage 5 invocation directory; "
                "the mounted successful workspace is checked above"
            ),
        },
        sort_keys=True,
    )
)
passed = (
    all(top_level_checks.values())
    and all(cross_checks.values())
    and not source_mismatches
)
print("RESULT=" + ("PASS" if passed else "FAIL"))
raise SystemExit(0 if passed else 1)
