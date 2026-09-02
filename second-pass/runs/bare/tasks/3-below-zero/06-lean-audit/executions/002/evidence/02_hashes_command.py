#!/usr/bin/env python3
"""Recompute launcher, tree, source, sidecar, and trusted-tool hashes."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from tools import klean_export, pipeline_contract, stage6_resolution_contract


audit_input_path = Path("/audit-input.json")
document = json.loads(audit_input_path.read_text())
resolution = document["resolution"]
recorded = resolution["hashes"]

mounted = {
    "k_workspace_sha256": pipeline_contract.sha256_tree(
        Path("/reference/k-proof")
    ),
    "stage1_export_sha256": klean_export.tree_digest(
        Path("/reference/k-proof")
    ),
    "discovery_manifest_sha256": hashlib.sha256(
        Path("/reference/lemma-discovery.json").read_bytes()
    ).hexdigest(),
    "k_audit_sha256": pipeline_contract.sha256_tree(
        Path("/reference/k-audit")
    ),
    "klean_generation_sha256": pipeline_contract.sha256_tree(
        Path("/reference/klean-generation")
    ),
    "generated_tree_sha256": klean_export.tree_digest(
        Path("/reference/klean-generation/generated")
    ),
    "lean_workspace_sha256": None,
    "lean_invocation_sha256": None,
}

source_root = Path("/reference/k-proof")
source_hashes = {
    path.relative_to(source_root).as_posix(): pipeline_contract.sha256_file(path)
    for path in pipeline_contract._walk_regular_files(
        source_root, "mounted Stage 1 workspace"
    )
}
recorded_source_hashes = resolution["stage1_source_hashes"]

generation = Path("/reference/klean-generation")
sidecar_names = [
    "input-manifest.json",
    "generator-manifest.json",
    "export-result.json",
    "trust-inventory.json",
    "preflight.json",
    "generated/obligation-map.json",
]
sidecar_hashes = {
    name: hashlib.sha256((generation / name).read_bytes()).hexdigest()
    for name in sidecar_names
}

tool_lock_path = Path("/opt/humaneval/data/klean-audit-tools.lock.json")
tool_lock = json.loads(tool_lock_path.read_text())
tool_hashes = {
    relative: hashlib.sha256((Path("/reference") / relative).read_bytes()).hexdigest()
    for relative in tool_lock["files"]
}
recorded_tool_hashes = tool_lock["files"]
tool_lock_sha256 = hashlib.sha256(tool_lock_path.read_bytes()).hexdigest()

toolchain_lock = Path("/reference/klean-toolchain.lock.json")
system_toolchain_lock = Path("/opt/humaneval/data/klean-toolchain.lock.json")

result = {
    "command": (
        "PYTHONPATH=/reference python3 "
        "/audit-output/evidence/02_hashes_command.py"
    ),
    "audit_input_sha256": hashlib.sha256(audit_input_path.read_bytes()).hexdigest(),
    "resolved_input": {
        "recorded": document["resolved_input_sha256"],
        "recomputed": stage6_resolution_contract.canonical_json_sha256(resolution),
        "matches": (
            document["resolved_input_sha256"]
            == stage6_resolution_contract.canonical_json_sha256(resolution)
        ),
    },
    "resolution_hashes": {
        key: {
            "recorded": recorded[key],
            "recomputed": mounted[key],
            "matches": recorded[key] == mounted[key],
        }
        for key in recorded
    },
    "stage1_source_hashes": {
        "recorded_count": len(recorded_source_hashes),
        "recomputed_count": len(source_hashes),
        "same_paths": set(recorded_source_hashes) == set(source_hashes),
        "mismatches": {
            path: {
                "recorded": recorded_source_hashes.get(path),
                "recomputed": source_hashes.get(path),
            }
            for path in sorted(set(recorded_source_hashes) | set(source_hashes))
            if recorded_source_hashes.get(path) != source_hashes.get(path)
        },
    },
    "sidecar_sha256": sidecar_hashes,
    "trusted_mechanical_checker": {
        "recorded_lock_sha256": document["audit"][
            "mechanical_checker_lock_sha256"
        ],
        "recomputed_lock_sha256": tool_lock_sha256,
        "lock_hash_matches": (
            document["audit"]["mechanical_checker_lock_sha256"]
            == tool_lock_sha256
        ),
        "recorded_tool_hashes": recorded_tool_hashes,
        "recomputed_tool_hashes": tool_hashes,
        "all_tool_hashes_match": recorded_tool_hashes == tool_hashes,
    },
    "toolchain_lock": {
        "reference_sha256": hashlib.sha256(toolchain_lock.read_bytes()).hexdigest(),
        "system_sha256": hashlib.sha256(
            system_toolchain_lock.read_bytes()
        ).hexdigest(),
        "byte_identical": toolchain_lock.read_bytes()
        == system_toolchain_lock.read_bytes(),
    },
    "candidate_absent": not Path("/candidate").exists(),
    "recorded_mode": resolution["mode"],
    "environment_mode_checked_separately": True,
}
print(json.dumps(result, indent=2, sort_keys=True))
