#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

from tools import klean_export


generation = Path("/reference/klean-generation")
generated = generation / "generated"
obligation_map_path = generated / "obligation-map.json"
obligation_map = json.loads(obligation_map_path.read_text())
input_manifest = json.loads((generation / "input-manifest.json").read_text())
generator_manifest = json.loads(
    (generation / "generator-manifest.json").read_text()
)
export_result = json.loads((generation / "export-result.json").read_text())
audit_input = json.loads(Path("/audit-input.json").read_text())
resolution = audit_input["resolution"]

actual_source_rules = obligation_map["source_rules"]
actual_obligations = obligation_map["obligations"]
actual_ids = [item["source_rule_id"] for item in actual_source_rules]
obligation_ids = [item["source_rule_id"] for item in actual_obligations]
target = klean_export.target_statement(generated)
expected_domain_ids = [
    "rule-b25203fce8fc32addea6c7671ce933b1a9ee841e26d4b5263e1113d6ed4ffaed"
]

checks = {
    "obligation_map_hash_matches_generator_manifest": (
        hashlib.sha256(obligation_map_path.read_bytes()).hexdigest()
        == generator_manifest["obligation_map_sha256"]
    ),
    "recorded_stage3_source_rules_match_obligation_map": (
        input_manifest["source_rules"] == actual_source_rules
    ),
    "recorded_source_ids_unique": len(actual_ids) == len(set(actual_ids)),
    "recorded_obligation_ids_unique": (
        len(obligation_ids) == len(set(obligation_ids))
    ),
    "recorded_source_obligation_ordered_bijection": (
        actual_ids == obligation_ids
    ),
    "generator_obligation_count_exact": (
        generator_manifest["obligation_count"] == len(actual_obligations)
    ),
    "export_obligation_count_exact": (
        export_result["obligation_count"] == len(actual_obligations)
    ),
    "generated_target_matches_generator_manifest": (
        target == generator_manifest["target"]
    ),
    "generated_target_matches_audit_input": target == resolution["target"],
    "generated_target_matches_recorded_preflight": (
        target == resolution["stage4_preflight"]["target"]
    ),
    "zero_recorded_obligations_have_no_target": (
        not actual_obligations and target is None
    ),
    "classification_only_mode": resolution["mode"] == "CLASSIFICATION_ONLY",
    "no_stage5_result": resolution["stage5_result"] is None,
    "no_candidate_mount": not Path("/candidate").exists(),
    "independent_domain_set_matches_generated_source_rules": (
        expected_domain_ids == actual_ids
    ),
}

for label, passed in checks.items():
    print(f"{label}: {'PASS' if passed else 'FAIL'}")
print(f"recorded_source_rule_ids={json.dumps(actual_ids)}")
print(f"recorded_obligation_ids={json.dumps(obligation_ids)}")
print(f"independent_domain_rule_ids={json.dumps(expected_domain_ids)}")
print(f"target={json.dumps(target, sort_keys=True)}")
print(
    "recorded_structural_checks_pass="
    + str(
        all(
            passed
            for label, passed in checks.items()
            if label != "independent_domain_set_matches_generated_source_rules"
        )
    )
)
print(
    "independent_semantic_completeness_pass="
    + str(checks["independent_domain_set_matches_generated_source_rules"])
)
