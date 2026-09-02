#!/usr/bin/env python3
"""Independent, read-only Stage 3/4 integrity checks for 23-strlen."""

from __future__ import annotations

import hashlib
import json
import os
import re
import stat
from pathlib import Path
from typing import Any

from tools import klean_export
from tools import lemma_discovery_contract
from tools import pipeline_contract
from tools import stage6_resolution_contract
from tools.k_rule_inventory import canonical_json_sha256, inventory_verification


AUDIT_INPUT = Path("/audit-input.json")
AUDIT_INPUT_COPY = Path("/audit-output/audit-input.json")
K_PROOF = Path("/reference/k-proof")
K_AUDIT = Path("/reference/k-audit")
DISCOVERY = Path("/reference/lemma-discovery.json")
GENERATION = Path("/reference/klean-generation")
GENERATED = GENERATION / "generated"
PRODUCERS = Path("/reference/generation-tools")
TOOLCHAIN_LOCK = Path("/reference/klean-toolchain.lock.json")


def load(path: Path) -> dict[str, Any]:
    document = json.loads(path.read_text())
    if not isinstance(document, dict):
        raise AssertionError(f"{path} is not a JSON object")
    return document


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def regular_files(root: Path) -> dict[str, Path]:
    result: dict[str, Path] = {}
    pending = [root]
    while pending:
        directory = pending.pop()
        for entry in os.scandir(directory):
            mode = entry.stat(follow_symlinks=False).st_mode
            path = Path(entry.path)
            if stat.S_ISDIR(mode):
                pending.append(path)
            elif stat.S_ISREG(mode):
                result[path.relative_to(root).as_posix()] = path
            else:
                raise AssertionError(f"non-regular tree entry: {path}")
    return result


checks: dict[str, bool] = {}
details: dict[str, Any] = {}


def check(name: str, condition: bool) -> None:
    checks[name] = bool(condition)


audit_document = load(AUDIT_INPUT)
resolution, resolved_digest = stage6_resolution_contract.verify_audit_input(
    audit_document
)
check("audit_input_signed_resolution_valid", True)
check(
    "audit_input_copy_byte_identical",
    AUDIT_INPUT.read_bytes() == AUDIT_INPUT_COPY.read_bytes(),
)
check("environment_mode_matches_resolution", os.environ.get("AUDIT_MODE") == resolution["mode"])
check("classification_only_mode", resolution["mode"] == "CLASSIFICATION_ONLY")
check("problem_identity", resolution["problem_id"] == "23-strlen")
check("condition_identity", resolution["condition"] == "kit-semantics")
check("semantics_mode_identity", resolution["semantics_mode"] == "SUPPLIED_SEMANTICS")
check("fixed_target_is_null_in_audit_input", resolution["target"] is None)
check("stage5_result_is_null", resolution["stage5_result"] is None)
check("stage5_paths_are_null", resolution["lean_workspace"] is None and resolution["lean_invocation"] is None)
check("candidate_mount_absent", not Path("/candidate").exists() and not Path("/candidate").is_symlink())

actual_stage1_files = regular_files(K_PROOF)
recorded_stage1_hashes = resolution["stage1_source_hashes"]
check(
    "stage1_source_file_set_exact",
    set(actual_stage1_files) == set(recorded_stage1_hashes),
)
stage1_hash_mismatches = {
    relative: {
        "actual": sha256_file(path),
        "expected": recorded_stage1_hashes.get(relative),
    }
    for relative, path in sorted(actual_stage1_files.items())
    if sha256_file(path) != recorded_stage1_hashes.get(relative)
}
check("all_stage1_source_hashes_match", not stage1_hash_mismatches)
details["stage1_source_file_count"] = len(actual_stage1_files)
details["stage1_source_hash_mismatches"] = stage1_hash_mismatches

actual_hashes = {
    "k_workspace_sha256": pipeline_contract.sha256_tree(K_PROOF),
    "stage1_export_sha256": klean_export.tree_digest(K_PROOF),
    "discovery_manifest_sha256": sha256_file(DISCOVERY),
    "k_audit_sha256": pipeline_contract.sha256_tree(K_AUDIT),
    "klean_generation_sha256": pipeline_contract.sha256_tree(GENERATION),
    "generation_producer_sources_sha256": pipeline_contract.sha256_tree(PRODUCERS),
    "generated_tree_sha256": klean_export.tree_digest(GENERATED),
    "lean_workspace_sha256": None,
    "lean_invocation_sha256": None,
}
check("all_launcher_resolution_hashes_match", actual_hashes == resolution["hashes"])
details["actual_resolution_hashes"] = actual_hashes
details["recorded_resolution_hashes"] = resolution["hashes"]
check(
    "selection_hashes_match_resolved_artifacts",
    resolution["selections"]["k_audit"]["artifact_sha256"]
    == actual_hashes["k_audit_sha256"]
    and resolution["selections"]["klean_generation"]["artifact_sha256"]
    == actual_hashes["klean_generation_sha256"],
)
check(
    "selection_status_is_no_obligations",
    resolution["selections"]["klean_generation"]["status"]
    == "KLEAN_NO_OBLIGATIONS",
)

inventory = inventory_verification(K_PROOF)
validated = lemma_discovery_contract.validate_trust_boundary(K_PROOF, DISCOVERY)
discovery = load(DISCOVERY)
independent_empty_inventory_hash = canonical_json_sha256([])
check("verification_module_exact", inventory["verification_module"] == "VERIFICATION")
check("local_verification_closure_exact", inventory["verification_modules"] == ["VERIFICATION"])
check("verification_has_zero_local_rules", inventory["rules"] == [])
check("independent_empty_inventory_hash", inventory["inventory_sha256"] == independent_empty_inventory_hash)
check("discovery_inventory_hash_matches", discovery["inventory_sha256"] == inventory["inventory_sha256"])
check("discovery_rule_sequence_bijective", discovery["rules"] == inventory["rules"] == [])
check(
    "validated_classification_groups_empty",
    all(
        validated[name] == []
        for name in (
            "definitions",
            "operational_rules",
            "proved_derived_lemmas",
            "domain_lemmas",
        )
    ),
)
details["inventory"] = inventory
details["validated_classification_counts"] = {
    name: len(validated[name])
    for name in (
        "definitions",
        "operational_rules",
        "proved_derived_lemmas",
        "domain_lemmas",
    )
}

generator_manifest = load(GENERATION / "generator-manifest.json")
source_manifest = load(PRODUCERS / "source-manifest.json")
input_manifest = load(GENERATION / "input-manifest.json")
obligation_map = load(GENERATED / "obligation-map.json")
export_result = load(GENERATION / "export-result.json")
stored_preflight = load(GENERATION / "preflight.json")
trust_inventory = load(GENERATION / "trust-inventory.json")
toolchain_lock = load(TOOLCHAIN_LOCK)

producer_hashes = {
    "klean_export.py": sha256_file(PRODUCERS / "klean_export.py"),
    "klean.py": sha256_file(PRODUCERS / "klean.py"),
}
expected_producer_hashes = {
    "klean_export.py": generator_manifest["exporter_sha256"],
    "klean.py": generator_manifest["klean_py_sha256"],
}
image_id = generator_manifest["provenance"]["generator_image_id"]
check("producer_bundle_file_set_exact", set(regular_files(PRODUCERS)) == {"source-manifest.json", "klean_export.py", "klean.py"})
check("producer_file_hashes_match_generator_manifest", producer_hashes == expected_producer_hashes)
check("producer_file_hashes_match_source_manifest", producer_hashes == source_manifest["files"])
check("producer_source_manifest_exact_keys", set(source_manifest) == {"schema_version", "generator_image_id", "files"})
check("producer_source_manifest_schema", source_manifest["schema_version"] == 1)
check("generator_image_id_matches_source_manifest", source_manifest["generator_image_id"] == image_id)
check(
    "generator_image_id_matches_audit_input_bundle",
    Path(resolution["generation_producer_sources"]).name
    == image_id.removeprefix("sha256:"),
)
check(
    "producer_bundle_tree_hash_matches_audit_input",
    actual_hashes["generation_producer_sources_sha256"]
    == resolution["hashes"]["generation_producer_sources_sha256"],
)
details["producer_file_hashes"] = producer_hashes
details["generator_image_id"] = image_id

check("generator_toolchain_matches_lock", generator_manifest["toolchain"] == toolchain_lock)
check("generator_generated_tree_hash", generator_manifest["generated_tree_sha256"] == actual_hashes["generated_tree_sha256"])
check("generator_stage1_provenance", generator_manifest["provenance"]["stage1_workspace_sha256"] == actual_hashes["stage1_export_sha256"])
check("generator_stage3_provenance", generator_manifest["provenance"]["stage3_discovery_manifest_sha256"] == actual_hashes["discovery_manifest_sha256"])
check("generator_inventory_provenance", generator_manifest["provenance"]["inventory_sha256"] == inventory["inventory_sha256"])

expected_role_lists = {
    "definitions": validated["definitions"],
    "operational_rules": validated["operational_rules"],
    "proved_derived_lemmas": validated["proved_derived_lemmas"],
    "source_rules": [],
}
check(
    "input_manifest_role_lists_match_independent_classification",
    all(input_manifest[name] == expected for name, expected in expected_role_lists.items()),
)
check("input_manifest_summary_functions_empty", input_manifest["summary_functions"] == [])
check("input_manifest_inventory_hash", input_manifest["inventory_sha256"] == inventory["inventory_sha256"])
check("input_manifest_verification_hash", input_manifest["verification_sha256"] == sha256_file(K_PROOF / "verification.k"))
check("input_manifest_stage1_hash", input_manifest["stage1_workspace_sha256"] == actual_hashes["stage1_export_sha256"])
check("input_manifest_stage3_hash", input_manifest["stage3_discovery_manifest_sha256"] == actual_hashes["discovery_manifest_sha256"])
check("input_manifest_problem", input_manifest["problem"] == "23-strlen")

source_rule_ids = [rule["source_rule_id"] for rule in obligation_map["source_rules"]]
obligation_ids = [obligation["source_rule_id"] for obligation in obligation_map["obligations"]]
check("obligation_map_exact_keys", set(obligation_map) == {"schema_version", "source_rules", "obligations", "trust_parameters"})
check("obligation_map_schema", obligation_map["schema_version"] == 3)
check("source_rule_sequence_exactly_empty", obligation_map["source_rules"] == input_manifest["source_rules"] == [])
check("obligation_sequence_bijective", source_rule_ids == obligation_ids and len(obligation_ids) == len(set(obligation_ids)))
check("obligations_genuinely_empty", obligation_map["obligations"] == [])
check("trust_parameters_genuinely_empty", obligation_map["trust_parameters"] == [])
check("obligation_map_hash", generator_manifest["obligation_map_sha256"] == sha256_file(GENERATED / "obligation-map.json"))
check(
    "zero_obligation_counts_consistent",
    generator_manifest["obligation_count"]
    == export_result["obligation_count"]
    == stored_preflight["obligation_count"]
    == 0,
)

actual_target = klean_export.target_statement(GENERATED)
raw_target_count = sum(
    len(re.findall(r"(?m)^\s*def\s+targetStatement\b", path.read_text()))
    for relative, path in regular_files(GENERATED).items()
    if relative.endswith(".lean")
)
check("actual_generated_target_absent", actual_target is None and raw_target_count == 0)
check("manifest_target_absent", generator_manifest["target"] is None)
check("audit_input_target_absent", resolution["target"] is None)
check("stored_preflight_target_absent", stored_preflight["target"] is None)
check("export_status_no_obligations", export_result["status"] == "KLEAN_NO_OBLIGATIONS")
check("stored_preflight_status_no_obligations", stored_preflight["status"] == "KLEAN_NO_OBLIGATIONS")
check("audit_embedded_preflight_exact", resolution["stage4_preflight"] == stored_preflight)
check("export_frozen_hash", export_result["frozen_input_sha256"] == actual_hashes["stage1_export_sha256"])
check("export_stage3_hash", export_result["stage3_discovery_manifest_sha256"] == actual_hashes["discovery_manifest_sha256"])
check("export_generated_hash", export_result["generated_tree_sha256"] == actual_hashes["generated_tree_sha256"])
check("export_trust_inventory_hash", export_result["trust_inventory_sha256"] == sha256_file(GENERATION / "trust-inventory.json"))
check(
    "trust_inventory_counts_match_preflight",
    len(trust_inventory["allowlist"]) == stored_preflight["trust_declaration_count"]
    and trust_inventory["designated_sorries"] == 0
    and trust_inventory["other_sorries"] == 0,
)
details["actual_target"] = actual_target
details["raw_target_declaration_count"] = raw_target_count
details["obligation_count"] = len(obligation_map["obligations"])
details["domain_lemma_count"] = len(validated["domain_lemmas"])

failed = sorted(name for name, passed in checks.items() if not passed)
report = {
    "schema_version": 1,
    "resolved_input_sha256": resolved_digest,
    "checks": checks,
    "failed_checks": failed,
    "details": details,
}
print(json.dumps(report, indent=2, sort_keys=True))
raise SystemExit(1 if failed else 0)
