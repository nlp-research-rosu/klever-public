#!/usr/bin/env python3
"""Independent hash, obligation-bijection, and target-identity checks."""

from __future__ import annotations

import hashlib
import json
import os
import re
import stat
from pathlib import Path

from tools.k_rule_inventory import inventory_verification
from tools.klean_export import (
    expected_target_definition,
    target_statement,
    tree_digest,
)
from tools.pipeline_contract import sha256_tree


STAGE1 = Path("/reference/k-proof")
DISCOVERY = Path("/reference/lemma-discovery.json")
GENERATION = Path("/reference/klean-generation")
GENERATED = GENERATION / "generated"
AUDIT = json.loads(Path("/audit-input.json").read_text())["resolution"]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def regular_file_hashes(root: Path) -> dict[str, str]:
    result: dict[str, str] = {}
    for directory, dirnames, filenames in os.walk(root, followlinks=False):
        directory_path = Path(directory)
        for name in [*dirnames, *filenames]:
            path = directory_path / name
            mode = path.stat(follow_symlinks=False).st_mode
            if stat.S_ISLNK(mode) or not (
                stat.S_ISDIR(mode) or stat.S_ISREG(mode)
            ):
                raise RuntimeError(f"unsupported tree entry: {path}")
        for name in filenames:
            path = directory_path / name
            result[path.relative_to(root).as_posix()] = sha256(path)
    return dict(sorted(result.items()))


inventory = inventory_verification(STAGE1)
discovery = json.loads(DISCOVERY.read_text())
input_manifest = json.loads((GENERATION / "input-manifest.json").read_text())
generator_manifest = json.loads(
    (GENERATION / "generator-manifest.json").read_text()
)
export_result = json.loads((GENERATION / "export-result.json").read_text())
obligation_path = GENERATED / "obligation-map.json"
obligation_map = json.loads(obligation_path.read_text())
trust_path = GENERATION / "trust-inventory.json"
toolchain_lock = json.loads(
    Path("/reference/klean-toolchain.lock.json").read_text()
)

classification_by_id = {
    entry["source_rule_id"]: entry["classification"]
    for entry in discovery["rules"]
}
independent_domain_ids = [
    rule["source_rule_id"]
    for rule in inventory["rules"]
    if classification_by_id[rule["source_rule_id"]] == "DOMAIN_LEMMA"
]
input_source_ids = [
    rule["source_rule_id"] for rule in input_manifest["source_rules"]
]
map_source_ids = [
    rule["source_rule_id"] for rule in obligation_map["source_rules"]
]
obligation_ids = [
    obligation["source_rule_id"] for obligation in obligation_map["obligations"]
]

lean_sources = sorted(GENERATED.rglob("*.lean"))
raw_target_count = sum(
    len(re.findall(r"(?m)^\s*def\s+targetStatement\b", path.read_text()))
    for path in lean_sources
)
observed_target = target_statement(GENERATED)
expected_target = expected_target_definition(obligation_map)

observed_stage1_source_hashes = regular_file_hashes(STAGE1)
recorded_stage1_source_hashes = AUDIT["stage1_source_hashes"]
stage1_missing = sorted(
    set(recorded_stage1_source_hashes) - set(observed_stage1_source_hashes)
)
stage1_extra = sorted(
    set(observed_stage1_source_hashes) - set(recorded_stage1_source_hashes)
)
stage1_mismatched = sorted(
    name
    for name in set(recorded_stage1_source_hashes)
    & set(observed_stage1_source_hashes)
    if recorded_stage1_source_hashes[name]
    != observed_stage1_source_hashes[name]
)

checks = {
    "audit_mode_is_classification_only": AUDIT["mode"] == "CLASSIFICATION_ONLY",
    "problem_condition_semantics_mode_exact": (
        AUDIT["problem_id"],
        AUDIT["condition"],
        AUDIT["semantics_mode"],
    )
    == ("148-bf", "semantics", "SUPPLIED_SEMANTICS"),
    "stage1_source_file_set_and_hashes_exact": not (
        stage1_missing or stage1_extra or stage1_mismatched
    ),
    "stage1_pipeline_tree_hash_exact": sha256_tree(STAGE1)
    == AUDIT["hashes"]["k_workspace_sha256"],
    "stage1_export_tree_hash_exact": tree_digest(STAGE1)
    == AUDIT["hashes"]["stage1_export_sha256"],
    "stage2_pipeline_tree_hash_exact": sha256_tree(Path("/reference/k-audit"))
    == AUDIT["hashes"]["k_audit_sha256"],
    "discovery_hash_exact": sha256(DISCOVERY)
    == AUDIT["hashes"]["discovery_manifest_sha256"],
    "generation_pipeline_tree_hash_exact": sha256_tree(GENERATION)
    == AUDIT["hashes"]["klean_generation_sha256"],
    "generated_tree_hash_exact": tree_digest(GENERATED)
    == AUDIT["hashes"]["generated_tree_sha256"],
    "selection_hashes_match_resolution_hashes": (
        AUDIT["selections"]["k_audit"]["artifact_sha256"]
        == AUDIT["hashes"]["k_audit_sha256"]
        and AUDIT["selections"]["klean_generation"]["artifact_sha256"]
        == AUDIT["hashes"]["klean_generation_sha256"]
    ),
    "inventory_hash_bound_exactly": input_manifest["inventory_sha256"]
    == inventory["inventory_sha256"]
    == discovery["inventory_sha256"]
    == generator_manifest["provenance"]["inventory_sha256"],
    "verification_hash_bound_exactly": input_manifest["verification_sha256"]
    == inventory["verification_sha256"],
    "stage1_export_bound_exactly": input_manifest["frozen_input_sha256"]
    == input_manifest["stage1_workspace_sha256"]
    == generator_manifest["provenance"]["stage1_workspace_sha256"]
    == export_result["frozen_input_sha256"]
    == tree_digest(STAGE1),
    "discovery_bound_exactly": (
        input_manifest["stage3_discovery_manifest_sha256"]
        == generator_manifest["provenance"][
            "stage3_discovery_manifest_sha256"
        ]
        == export_result["stage3_discovery_manifest_sha256"]
        == sha256(DISCOVERY)
    ),
    "generated_tree_bound_exactly": generator_manifest["generated_tree_sha256"]
    == export_result["generated_tree_sha256"]
    == tree_digest(GENERATED),
    "toolchain_lock_exact": generator_manifest["toolchain"] == toolchain_lock,
    "obligation_map_hash_exact": generator_manifest["obligation_map_sha256"]
    == sha256(obligation_path),
    "trust_inventory_hash_exact": export_result["trust_inventory_sha256"]
    == sha256(trust_path),
    "independent_domain_set_empty": independent_domain_ids == [],
    "domain_to_source_rule_bijection_exact": input_source_ids
    == independent_domain_ids,
    "source_rule_map_bijection_exact": map_source_ids
    == independent_domain_ids,
    "source_rule_obligation_bijection_exact": obligation_ids
    == independent_domain_ids,
    "no_duplicate_obligations": len(obligation_ids) == len(set(obligation_ids)),
    "no_trust_parameters_without_obligations": obligation_map[
        "trust_parameters"
    ]
    == [],
    "zero_obligation_counts_exact": generator_manifest["obligation_count"]
    == export_result["obligation_count"]
    == len(obligation_map["obligations"])
    == 0,
    "status_exact": (
        export_result["status"],
        AUDIT["selections"]["klean_generation"]["status"],
    )
    == ("KLEAN_NO_OBLIGATIONS", "KLEAN_NO_OBLIGATIONS"),
    "expected_target_absent": expected_target is None,
    "observed_target_absent": observed_target is None,
    "manifest_target_absent": generator_manifest["target"] is None,
    "no_raw_target_declaration": raw_target_count == 0,
    "candidate_absent": not Path("/candidate").exists(),
    "lean_workspace_and_invocation_absent": AUDIT["lean_workspace"] is None
    and AUDIT["lean_invocation"] is None
    and AUDIT["hashes"]["lean_workspace_sha256"] is None
    and AUDIT["hashes"]["lean_invocation_sha256"] is None,
}

result = {
    "status": "PASS" if all(checks.values()) else "FAIL",
    "checks": checks,
    "stage1_source_hash_count_recorded": len(recorded_stage1_source_hashes),
    "stage1_source_hash_count_observed": len(observed_stage1_source_hashes),
    "stage1_source_missing": stage1_missing,
    "stage1_source_extra": stage1_extra,
    "stage1_source_mismatched": stage1_mismatched,
    "independent_domain_rule_ids": independent_domain_ids,
    "input_source_rule_ids": input_source_ids,
    "mapped_source_rule_ids": map_source_ids,
    "obligation_ids": obligation_ids,
    "obligation_count": len(obligation_ids),
    "raw_target_declaration_count": raw_target_count,
    "observed_target": observed_target,
    "expected_target_definition": expected_target,
    "generator_manifest_target": generator_manifest["target"],
}
print(json.dumps(result, indent=2, sort_keys=True))
raise SystemExit(0 if result["status"] == "PASS" else 1)
