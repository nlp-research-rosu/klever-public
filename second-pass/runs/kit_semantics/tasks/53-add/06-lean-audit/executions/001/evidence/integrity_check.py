#!/usr/bin/env python3
import hashlib
import json
import os
import re
from pathlib import Path

from tools import klean_export, pipeline_contract
from tools.k_rule_inventory import inventory_verification
from tools.lemma_discovery_contract import validate_trust_boundary


def load(path: Path):
    return json.loads(path.read_text())


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


audit_path = Path("/audit-input.json")
audit_copy_path = Path("/audit-output/audit-input.json")
audit = load(audit_path)
resolution = audit["resolution"]
recorded = resolution["hashes"]

k_workspace = Path("/reference/k-proof")
k_audit = Path("/reference/k-audit")
discovery_path = Path("/reference/lemma-discovery.json")
generation = Path("/reference/klean-generation")
generated = generation / "generated"
producer = Path("/reference/generation-tools")

input_manifest = load(generation / "input-manifest.json")
generator_manifest = load(generation / "generator-manifest.json")
export_result = load(generation / "export-result.json")
published_preflight = load(generation / "preflight.json")
trust_inventory = load(generation / "trust-inventory.json")
obligation_map_path = generated / "obligation-map.json"
obligation_map = load(obligation_map_path)
toolchain_lock = load(Path("/reference/klean-toolchain.lock.json"))
source_manifest = load(producer / "source-manifest.json")
discovery = load(discovery_path)

actual_hashes = {
    "k_workspace_sha256": pipeline_contract.sha256_tree(k_workspace),
    "stage1_export_sha256": klean_export.tree_digest(k_workspace),
    "discovery_manifest_sha256": sha(discovery_path),
    "k_audit_sha256": pipeline_contract.sha256_tree(k_audit),
    "klean_generation_sha256": pipeline_contract.sha256_tree(generation),
    "generation_producer_sources_sha256": pipeline_contract.sha256_tree(producer),
    "generated_tree_sha256": klean_export.tree_digest(generated),
    "lean_workspace_sha256": None,
    "lean_invocation_sha256": None,
}

expected_source_hashes = resolution["stage1_source_hashes"]
actual_source_hashes = {
    path.relative_to(k_workspace).as_posix(): sha(path)
    for path in pipeline_contract._walk_regular_files(
        k_workspace, "mounted Stage 1 workspace"
    )
}
source_missing = sorted(set(expected_source_hashes) - set(actual_source_hashes))
source_extra = sorted(set(actual_source_hashes) - set(expected_source_hashes))
source_changed = sorted(
    name
    for name in set(expected_source_hashes) & set(actual_source_hashes)
    if expected_source_hashes[name] != actual_source_hashes[name]
)

inventory = inventory_verification(k_workspace)
validated = validate_trust_boundary(k_workspace, discovery_path)
canonical_ids = [entry["source_rule_id"] for entry in inventory["rules"]]
manifest_ids = [entry["source_rule_id"] for entry in discovery["rules"]]
domain_ids = [entry["source_rule_id"] for entry in validated["domain_lemmas"]]
source_rule_ids = [entry["source_rule_id"] for entry in input_manifest["source_rules"]]
mapped_source_ids = [entry["source_rule_id"] for entry in obligation_map["source_rules"]]
obligation_ids = [entry["source_rule_id"] for entry in obligation_map["obligations"]]

actual_target = klean_export.target_statement(generated)
expected_target_definition = klean_export.expected_target_definition(obligation_map)

lean_sources = [
    path
    for _relative, kind, path in klean_export._tree_entries(generated)
    if kind == "file" and path.suffix == ".lean"
]
target_like_lines = []
for path in lean_sources:
    for line_number, line in enumerate(path.read_text().splitlines(), 1):
        if re.search(r"\b(?:target|final)\b", line, re.IGNORECASE):
            target_like_lines.append(
                f"{path.relative_to(generated)}:{line_number}:{line.strip()}"
            )

producer_expected = {
    "klean_export.py": generator_manifest["exporter_sha256"],
    "klean.py": generator_manifest["klean_py_sha256"],
}
producer_actual = {
    name: sha(producer / name) for name in producer_expected
}
producer_image_from_audit_path = (
    "sha256:" + Path(resolution["generation_producer_sources"]).name
)

checks = {
    "audit_input_copy_byte_identical": audit_path.read_bytes()
    == audit_copy_path.read_bytes(),
    "audit_mode_environment_matches": os.environ.get("AUDIT_MODE")
    == resolution["mode"],
    "all_resolution_hashes_match": actual_hashes == recorded,
    "selection_k_audit_hash_matches": resolution["selections"]["k_audit"][
        "artifact_sha256"
    ]
    == actual_hashes["k_audit_sha256"],
    "selection_generation_hash_matches": resolution["selections"][
        "klean_generation"
    ]["artifact_sha256"]
    == actual_hashes["klean_generation_sha256"],
    "all_stage1_per_file_hashes_match": not (
        source_missing or source_extra or source_changed
    ),
    "inventory_hash_matches_discovery": inventory["inventory_sha256"]
    == discovery["inventory_sha256"],
    "inventory_ordered_bijection": canonical_ids == manifest_ids
    and len(canonical_ids) == len(set(canonical_ids))
    and len(manifest_ids) == len(set(manifest_ids)),
    "independent_domain_set_equals_export_source_rules": domain_ids
    == source_rule_ids,
    "source_rule_obligation_ordered_bijection": source_rule_ids
    == mapped_source_ids
    == obligation_ids
    and len(obligation_ids) == len(set(obligation_ids)),
    "obligation_count_fields_match": len(obligation_ids)
    == generator_manifest["obligation_count"]
    == export_result["obligation_count"]
    == published_preflight["obligation_count"]
    == resolution["stage4_preflight"]["obligation_count"],
    "obligation_map_hash_matches": sha(obligation_map_path)
    == generator_manifest["obligation_map_sha256"],
    "target_is_fixed_and_consistent": actual_target
    == generator_manifest["target"]
    == published_preflight["target"]
    == resolution["target"]
    == resolution["stage4_preflight"]["target"],
    "expected_target_definition_absent": expected_target_definition is None,
    "no_target_declaration_found": actual_target is None
    and not target_like_lines,
    "no_candidate_for_classification_only": resolution["mode"]
    == "CLASSIFICATION_ONLY"
    and not Path("/candidate").exists()
    and resolution["lean_workspace"] is None
    and resolution["lean_invocation"] is None
    and resolution["stage5_result"] is None,
    "producer_files_match_generator": producer_actual == producer_expected,
    "producer_files_match_source_manifest": source_manifest["files"]
    == producer_expected,
    "producer_image_id_matches_all_views": generator_manifest["provenance"][
        "generator_image_id"
    ]
    == source_manifest["generator_image_id"]
    == producer_image_from_audit_path,
    "toolchain_lock_matches_generator": toolchain_lock
    == generator_manifest["toolchain"],
    "stage1_hash_cross_fields_match": actual_hashes["stage1_export_sha256"]
    == input_manifest["frozen_input_sha256"]
    == input_manifest["stage1_workspace_sha256"]
    == generator_manifest["provenance"]["stage1_workspace_sha256"]
    == export_result["frozen_input_sha256"]
    == published_preflight["frozen_input_sha256"]
    == published_preflight["stage1_workspace_sha256"],
    "discovery_hash_cross_fields_match": actual_hashes[
        "discovery_manifest_sha256"
    ]
    == input_manifest["stage3_discovery_manifest_sha256"]
    == generator_manifest["provenance"]["stage3_discovery_manifest_sha256"]
    == export_result["stage3_discovery_manifest_sha256"]
    == published_preflight["stage3_discovery_manifest_sha256"],
    "inventory_hash_cross_fields_match": inventory["inventory_sha256"]
    == input_manifest["inventory_sha256"]
    == generator_manifest["provenance"]["inventory_sha256"],
    "generated_hash_cross_fields_match": actual_hashes[
        "generated_tree_sha256"
    ]
    == generator_manifest["generated_tree_sha256"]
    == export_result["generated_tree_sha256"]
    == published_preflight["generated_tree_sha256"],
    "trust_inventory_hash_matches_export": sha(
        generation / "trust-inventory.json"
    )
    == export_result["trust_inventory_sha256"],
    "published_preflight_matches_launcher_copy": published_preflight
    == resolution["stage4_preflight"],
    "export_status_is_no_obligations": export_result["status"]
    == "KLEAN_NO_OBLIGATIONS",
    "published_status_is_no_obligations": published_preflight["status"]
    == resolution["selections"]["klean_generation"]["status"]
    == "KLEAN_NO_OBLIGATIONS",
    "trust_inventory_counts_consistent": trust_inventory["designated_sorries"]
    == trust_inventory["other_sorries"]
    == 0
    and len(trust_inventory["allowlist"])
    == len(trust_inventory["axioms"])
    == published_preflight["trust_declaration_count"],
}

output = {
    "actual_hashes": actual_hashes,
    "recorded_hashes": recorded,
    "stage1_per_file_hash_summary": {
        "actual_count": len(actual_source_hashes),
        "recorded_count": len(expected_source_hashes),
        "missing": source_missing,
        "extra": source_extra,
        "changed": source_changed,
    },
    "inventory_and_bijection": {
        "canonical_ids": canonical_ids,
        "manifest_ids": manifest_ids,
        "independent_domain_ids": domain_ids,
        "input_manifest_source_rule_ids": source_rule_ids,
        "obligation_map_source_rule_ids": mapped_source_ids,
        "obligation_ids": obligation_ids,
    },
    "target": {
        "actual": actual_target,
        "expected_definition": expected_target_definition,
        "generator_manifest": generator_manifest["target"],
        "launcher": resolution["target"],
        "target_like_lines": target_like_lines,
    },
    "producer": {
        "actual_hashes": producer_actual,
        "expected_hashes": producer_expected,
        "image_from_audit_path": producer_image_from_audit_path,
    },
    "checks": checks,
    "all_checks_true": all(checks.values()),
}
print(json.dumps(output, indent=2, sort_keys=True))
if not output["all_checks_true"]:
    raise SystemExit(1)
