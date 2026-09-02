#!/usr/bin/env python3
"""Recompute signed-input, provenance, manifest, and target hashes."""

from __future__ import annotations

import hashlib
import json
import os
import stat
import sys
from pathlib import Path

sys.path.insert(0, "/reference")

from tools import (
    klean_export,
    pipeline_contract,
    stage6_resolution_contract,
)


AUDIT_INPUT = Path("/audit-input.json")
K_WORKSPACE = Path("/reference/k-proof")
K_AUDIT = Path("/reference/k-audit")
DISCOVERY = Path("/reference/lemma-discovery.json")
GENERATION = Path("/reference/klean-generation")
GENERATED = GENERATION / "generated"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def regular_source_hashes(root: Path) -> dict[str, str]:
    result: dict[str, str] = {}
    pending = [root]
    while pending:
        directory = pending.pop()
        for entry in os.scandir(directory):
            mode = entry.stat(follow_symlinks=False).st_mode
            path = Path(entry.path)
            if stat.S_ISDIR(mode):
                pending.append(path)
            elif stat.S_ISREG(mode):
                result[path.relative_to(root).as_posix()] = sha256(path)
            else:
                raise AssertionError(f"unsupported Stage 1 entry: {path}")
    return dict(sorted(result.items()))


document = json.loads(AUDIT_INPUT.read_text())
resolution, signed_digest = stage6_resolution_contract.verify_audit_input(
    document
)
expected_hashes = resolution["hashes"]

observed_hashes = {
    "k_workspace_sha256": pipeline_contract.sha256_tree(K_WORKSPACE),
    "stage1_export_sha256": klean_export.tree_digest(K_WORKSPACE),
    "discovery_manifest_sha256": sha256(DISCOVERY),
    "k_audit_sha256": pipeline_contract.sha256_tree(K_AUDIT),
    "klean_generation_sha256": pipeline_contract.sha256_tree(GENERATION),
    "generated_tree_sha256": klean_export.tree_digest(GENERATED),
    "lean_workspace_sha256": None,
    "lean_invocation_sha256": None,
}

input_manifest = json.loads((GENERATION / "input-manifest.json").read_text())
generator_manifest = json.loads(
    (GENERATION / "generator-manifest.json").read_text()
)
export_result = json.loads((GENERATION / "export-result.json").read_text())
preflight = json.loads((GENERATION / "preflight.json").read_text())
trust_inventory = json.loads(
    (GENERATION / "trust-inventory.json").read_text()
)
obligation_map = json.loads(
    (GENERATED / "obligation-map.json").read_text()
)
toolchain_lock = json.loads(
    Path("/reference/klean-toolchain.lock.json").read_text()
)
target = klean_export.target_statement(GENERATED)
expected_target_definition = klean_export.expected_target_definition(
    obligation_map
)

source_hashes = regular_source_hashes(K_WORKSPACE)
checks = {
    "audit_mode_env_matches_signed_mode": (
        os.environ.get("AUDIT_MODE") == resolution["mode"]
    ),
    "problem_exact": resolution["problem_id"] == "12-longest",
    "condition_exact": resolution["condition"] == "bare",
    "semantics_mode_exact": (
        resolution["semantics_mode"] == "GENERATED_SEMANTICS"
    ),
    "signed_digest_exact": (
        stage6_resolution_contract.canonical_json_sha256(resolution)
        == signed_digest
    ),
    "all_resolution_hashes_exact": observed_hashes == expected_hashes,
    "all_stage1_source_hashes_exact": (
        source_hashes == resolution["stage1_source_hashes"]
    ),
    "k_audit_selection_hash_exact": (
        observed_hashes["k_audit_sha256"]
        == resolution["selections"]["k_audit"]["artifact_sha256"]
    ),
    "generation_selection_hash_exact": (
        observed_hashes["klean_generation_sha256"]
        == resolution["selections"]["klean_generation"]["artifact_sha256"]
    ),
    "signed_preflight_exact": preflight == resolution["stage4_preflight"],
    "input_frozen_hash_exact": (
        input_manifest["frozen_input_sha256"]
        == observed_hashes["stage1_export_sha256"]
        == input_manifest["stage1_workspace_sha256"]
    ),
    "input_discovery_hash_exact": (
        input_manifest["stage3_discovery_manifest_sha256"]
        == observed_hashes["discovery_manifest_sha256"]
    ),
    "generator_tree_hash_exact": (
        generator_manifest["generated_tree_sha256"]
        == observed_hashes["generated_tree_sha256"]
    ),
    "generator_inventory_provenance_exact": (
        generator_manifest["provenance"]["inventory_sha256"]
        == input_manifest["inventory_sha256"]
    ),
    "generator_stage1_provenance_exact": (
        generator_manifest["provenance"]["stage1_workspace_sha256"]
        == observed_hashes["stage1_export_sha256"]
    ),
    "generator_stage3_provenance_exact": (
        generator_manifest["provenance"][
            "stage3_discovery_manifest_sha256"
        ]
        == observed_hashes["discovery_manifest_sha256"]
    ),
    "generator_toolchain_exact": (
        generator_manifest["toolchain"] == toolchain_lock
    ),
    "exporter_hash_exact": (
        generator_manifest["exporter_sha256"]
        == sha256(Path("/reference/tools/klean_export.py"))
    ),
    "klean_tool_hash_exact": (
        generator_manifest["klean_py_sha256"]
        == sha256(Path("/reference/tools/klean.py"))
    ),
    "obligation_map_hash_exact": (
        generator_manifest["obligation_map_sha256"]
        == sha256(GENERATED / "obligation-map.json")
    ),
    "export_trust_inventory_hash_exact": (
        export_result["trust_inventory_sha256"]
        == sha256(GENERATION / "trust-inventory.json")
    ),
    "export_frozen_hash_exact": (
        export_result["frozen_input_sha256"]
        == observed_hashes["stage1_export_sha256"]
    ),
    "export_discovery_hash_exact": (
        export_result["stage3_discovery_manifest_sha256"]
        == observed_hashes["discovery_manifest_sha256"]
    ),
    "export_generated_hash_exact": (
        export_result["generated_tree_sha256"]
        == observed_hashes["generated_tree_sha256"]
    ),
    "independent_domain_source_set_empty": input_manifest["source_rules"] == [],
    "obligation_source_set_empty": obligation_map["source_rules"] == [],
    "obligation_set_empty": obligation_map["obligations"] == [],
    "trust_parameter_set_empty": obligation_map["trust_parameters"] == [],
    "generator_obligation_count_zero": (
        generator_manifest["obligation_count"] == 0
    ),
    "export_obligation_count_zero": export_result["obligation_count"] == 0,
    "preflight_obligation_count_zero": preflight["obligation_count"] == 0,
    "export_status_no_obligations": (
        export_result["status"] == "KLEAN_NO_OBLIGATIONS"
    ),
    "preflight_status_no_obligations": (
        preflight["status"] == "KLEAN_NO_OBLIGATIONS"
    ),
    "selection_status_no_obligations": (
        resolution["selections"]["klean_generation"]["status"]
        == "KLEAN_NO_OBLIGATIONS"
    ),
    "target_absent_everywhere": (
        target is None
        and expected_target_definition is None
        and generator_manifest["target"] is None
        and preflight["target"] is None
        and resolution["target"] is None
    ),
    "stage5_absent_in_signed_input": (
        resolution["stage5_result"] is None
        and resolution["lean_workspace"] is None
        and resolution["lean_invocation"] is None
    ),
    "candidate_mount_absent": not Path("/candidate").exists(),
    "designated_sorries_zero": (
        preflight["designated_sorry_count"] == 0
        and trust_inventory["designated_sorries"] == 0
        and trust_inventory["other_sorries"] == 0
    ),
}

result = {
    "signed_mode": resolution["mode"],
    "signed_digest": signed_digest,
    "expected_hashes": expected_hashes,
    "observed_hashes": observed_hashes,
    "stage1_source_hashes": source_hashes,
    "inventory_sha256": input_manifest["inventory_sha256"],
    "obligation_map": obligation_map,
    "target": target,
    "expected_target_definition": expected_target_definition,
    "trust_allowlist_count": len(trust_inventory["allowlist"]),
    "generation_tool_hash_attestations": {
        "exporter_sha256": {
            "recorded_generation_time": generator_manifest[
                "exporter_sha256"
            ],
            "mounted_audit_tool": sha256(
                Path("/reference/tools/klean_export.py")
            ),
            "equal": checks["exporter_hash_exact"],
        },
        "klean_py_sha256": {
            "recorded_generation_time": generator_manifest[
                "klean_py_sha256"
            ],
            "mounted_audit_tool": sha256(
                Path("/reference/tools/klean.py")
            ),
            "equal": checks["klean_tool_hash_exact"],
        },
        "recorded_generator_image_id": generator_manifest["provenance"][
            "generator_image_id"
        ],
    },
    "checks": checks,
    "all_checks_pass": all(checks.values()),
    "all_signed_input_and_structural_hash_checks_pass": all(
        value
        for name, value in checks.items()
        if name not in {"exporter_hash_exact", "klean_tool_hash_exact"}
    ),
}
print(json.dumps(result, indent=2, sort_keys=True))
