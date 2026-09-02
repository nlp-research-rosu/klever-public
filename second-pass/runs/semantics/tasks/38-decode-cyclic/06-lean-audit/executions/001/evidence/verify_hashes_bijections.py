#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

from tools import klean_export, pipeline_contract
from tools.k_rule_inventory import inventory_verification
from tools.lemma_discovery_contract import validate_trust_boundary


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


audit = json.loads(Path("/audit-input.json").read_text())["resolution"]
workspace = Path("/reference/k-proof")
discovery_path = Path("/reference/lemma-discovery.json")
generation = Path("/reference/klean-generation")
generated = generation / "generated"
generator_manifest = json.loads(
    (generation / "generator-manifest.json").read_text()
)
input_manifest = json.loads((generation / "input-manifest.json").read_text())
obligation_map = json.loads((generated / "obligation-map.json").read_text())
discovery_raw = json.loads(discovery_path.read_text())

inventory = inventory_verification(workspace)
validated = validate_trust_boundary(workspace, discovery_path)
discovery_hash = file_hash(discovery_path)
expected_source_rules = klean_export._domain_source_rules(
    validated, discovery_hash
)
canonical_ids = [rule["source_rule_id"] for rule in inventory["rules"]]
discovery_ids = [rule["source_rule_id"] for rule in discovery_raw["rules"]]
domain_ids = [rule["source_rule_id"] for rule in validated["domain_lemmas"]]
obligation_ids = [
    obligation["source_rule_id"] for obligation in obligation_map["obligations"]
]

source_hashes = {
    path.relative_to(workspace).as_posix(): pipeline_contract.sha256_file(path)
    for path in pipeline_contract._walk_regular_files(
        workspace, "Stage 1 source workspace"
    )
}

actual_target = klean_export.target_statement(generated)
expected_definition = klean_export.expected_target_definition(obligation_map)
expected_definition_hash = (
    klean_export.sha256_text(expected_definition)
    if expected_definition is not None
    else None
)

source_by_id = {
    rule["source_rule_id"]: rule for rule in obligation_map["source_rules"]
}
obligation_details = []
for obligation in obligation_map["obligations"]:
    source = source_by_id.get(obligation["source_rule_id"])
    obligation_details.append(
        {
            "source_rule_id": obligation["source_rule_id"],
            "source_exists_once": source is not None,
            "span_matches": source is not None
            and obligation["source_span"]
            == {
                "start_line": source["start_line"],
                "end_line": source["end_line"],
            },
            "normalized_hash_matches": source is not None
            and obligation["normalized_sha256"] == source["normalized_sha256"],
            "inventory_hash_matches": source is not None
            and obligation["inventory_sha256"] == source["inventory_sha256"],
            "discovery_hash_matches": source is not None
            and obligation["discovery_manifest_sha256"]
            == source["discovery_manifest_sha256"],
            "lean_conjunct_hash_matches": obligation[
                "lean_conjunct_sha256"
            ]
            == klean_export.sha256_text(obligation["lean_conjunct"]),
        }
    )

hashes = audit["hashes"]
checks = {
    "audit_mode_matches_environment": audit["mode"]
    == "CLASSIFICATION_AND_PROOF",
    "stage1_pipeline_tree": {
        "actual": pipeline_contract.sha256_tree(workspace),
        "expected": hashes["k_workspace_sha256"],
    },
    "stage1_export_tree": {
        "actual": klean_export.tree_digest(workspace),
        "expected": hashes["stage1_export_sha256"],
    },
    "stage1_all_source_file_hashes_match": source_hashes
    == audit["stage1_source_hashes"],
    "k_audit_pipeline_tree": {
        "actual": pipeline_contract.sha256_tree(Path("/reference/k-audit")),
        "expected": hashes["k_audit_sha256"],
    },
    "discovery_file": {
        "actual": file_hash(discovery_path),
        "expected": hashes["discovery_manifest_sha256"],
    },
    "generation_pipeline_tree": {
        "actual": pipeline_contract.sha256_tree(generation),
        "expected": hashes["klean_generation_sha256"],
    },
    "generated_export_tree": {
        "actual": klean_export.tree_digest(generated),
        "expected": hashes["generated_tree_sha256"],
    },
    "producer_pipeline_tree": {
        "actual": pipeline_contract.sha256_tree(
            Path("/reference/generation-tools")
        ),
        "expected": hashes["generation_producer_sources_sha256"],
    },
    "candidate_pipeline_tree": {
        "actual": pipeline_contract.sha256_tree(Path("/candidate")),
        "expected": hashes["lean_workspace_sha256"],
    },
    "inventory_hash_matches_discovery": inventory["inventory_sha256"]
    == discovery_raw["inventory_sha256"],
    "discovery_rule_order_exact": canonical_ids == discovery_ids,
    "discovery_rule_ids_unique": len(discovery_ids) == len(set(discovery_ids)),
    "input_source_rules_exact": input_manifest["source_rules"]
    == expected_source_rules,
    "obligation_map_source_rules_exact": obligation_map["source_rules"]
    == expected_source_rules,
    "domain_obligation_order_exact": domain_ids == obligation_ids,
    "domain_obligation_ids_unique": len(obligation_ids)
    == len(set(obligation_ids)),
    "obligation_count_matches": len(obligation_ids)
    == generator_manifest["obligation_count"],
    "obligation_map_hash_matches": file_hash(
        generated / "obligation-map.json"
    )
    == generator_manifest["obligation_map_sha256"],
    "target_actual_equals_generator_manifest": actual_target
    == generator_manifest["target"],
    "target_actual_equals_audit_input": actual_target == audit["target"],
    "target_definition_is_exact_conjunction": actual_target is not None
    and actual_target["definition_sha256"] == expected_definition_hash,
    "target_statement_hash_matches_audit": actual_target is not None
    and actual_target["statement_sha256"]
    == audit["target"]["statement_sha256"],
}

for label, value in list(checks.items()):
    if isinstance(value, dict) and set(value) == {"actual", "expected"}:
        value["match"] = value["actual"] == value["expected"]

print(
    json.dumps(
        {
            "checks": checks,
            "canonical_rule_ids": canonical_ids,
            "discovery_rule_ids": discovery_ids,
            "domain_rule_ids": domain_ids,
            "obligation_rule_ids": obligation_ids,
            "obligation_details": obligation_details,
            "actual_target": actual_target,
            "expected_target_definition": expected_definition,
            "expected_target_definition_sha256": expected_definition_hash,
        },
        indent=2,
        sort_keys=True,
    )
)
