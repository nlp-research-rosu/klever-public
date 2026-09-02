#!/usr/bin/env python3
import hashlib
import json
import re
from pathlib import Path

from tools import klean_export, lemma_discovery_contract


def load(path: Path) -> dict:
    return json.loads(path.read_text())


stage1 = Path("/reference/k-proof")
discovery_path = Path("/reference/lemma-discovery.json")
generation = Path("/reference/klean-generation")
generated = generation / "generated"
input_manifest = load(generation / "input-manifest.json")
generator_manifest = load(generation / "generator-manifest.json")
export_result = load(generation / "export-result.json")
recorded_preflight = load(generation / "preflight.json")
obligation_map_path = generated / "obligation-map.json"
obligation_map = load(obligation_map_path)
audit_input = load(Path("/audit-input.json"))
resolution = audit_input["resolution"]
validated = lemma_discovery_contract.validate_trust_boundary(
    stage1, discovery_path
)

discovery_hash = hashlib.sha256(discovery_path.read_bytes()).hexdigest()
expected_source_rules = klean_export._domain_source_rules(
    validated, discovery_hash
)
observed_source_rules = obligation_map["source_rules"]
obligations = obligation_map["obligations"]
obligation_ids = [
    obligation.get("source_rule_id") for obligation in obligations
]
expected_ids = [
    source_rule["source_rule_id"] for source_rule in expected_source_rules
]

target_occurrences = []
for relative, kind, path in klean_export._tree_entries(generated):
    if kind != "file" or path.suffix != ".lean":
        continue
    for line_number, line in enumerate(path.read_text().splitlines(), 1):
        if re.search(r"\btargetStatement\b", line):
            target_occurrences.append(
                {"file": relative, "line": line_number, "text": line}
            )

observed_target = klean_export.target_statement(generated)
expected_target_definition = klean_export.expected_target_definition(
    obligation_map
)

checks = {
    "independent_domain_rule_count": len(validated["domain_lemmas"]),
    "independent_domain_source_rules": expected_source_rules,
    "input_manifest_source_rules": input_manifest["source_rules"],
    "obligation_map_source_rules": observed_source_rules,
    "source_rule_lists_exact": expected_source_rules
    == input_manifest["source_rules"]
    == observed_source_rules,
    "source_rule_ids_expected": expected_ids,
    "obligation_ids_observed": obligation_ids,
    "source_rule_obligation_order_exact": expected_ids == obligation_ids,
    "source_rule_obligation_bijective": len(expected_ids)
    == len(obligation_ids)
    == len(set(obligation_ids))
    and set(expected_ids) == set(obligation_ids),
    "obligations": obligations,
    "obligation_count": len(obligations),
    "trust_parameters": obligation_map["trust_parameters"],
    "no_vacuous_or_weakened_conjunct_exists": len(obligations) == 0,
    "input_definitions_match_independent_inventory": input_manifest[
        "definitions"
    ]
    == validated["definitions"],
    "input_operational_rules_match_independent_inventory": input_manifest[
        "operational_rules"
    ]
    == validated["operational_rules"],
    "input_derived_lemmas_match_independent_inventory": input_manifest[
        "proved_derived_lemmas"
    ]
    == validated["proved_derived_lemmas"],
    "obligation_map_sha256": hashlib.sha256(
        obligation_map_path.read_bytes()
    ).hexdigest(),
    "obligation_map_hash_matches_generator": hashlib.sha256(
        obligation_map_path.read_bytes()
    ).hexdigest()
    == generator_manifest["obligation_map_sha256"],
    "generator_obligation_count": generator_manifest["obligation_count"],
    "export_obligation_count": export_result["obligation_count"],
    "recorded_preflight_obligation_count": recorded_preflight[
        "obligation_count"
    ],
    "all_obligation_counts_exact": len(obligations)
    == generator_manifest["obligation_count"]
    == export_result["obligation_count"]
    == recorded_preflight["obligation_count"],
    "expected_target_definition": expected_target_definition,
    "observed_target": observed_target,
    "generator_target": generator_manifest["target"],
    "recorded_preflight_target": recorded_preflight["target"],
    "audit_input_target": resolution["target"],
    "target_occurrences": target_occurrences,
    "fixed_null_target_exact": expected_target_definition is None
    and observed_target is None
    and generator_manifest["target"] is None
    and recorded_preflight["target"] is None
    and resolution["target"] is None
    and not target_occurrences,
    "export_status": export_result["status"],
    "recorded_preflight_status": recorded_preflight["status"],
    "selected_status": resolution["selections"]["klean_generation"][
        "status"
    ],
    "all_statuses_no_obligations": {
        export_result["status"],
        recorded_preflight["status"],
        resolution["selections"]["klean_generation"]["status"],
    }
    == {"KLEAN_NO_OBLIGATIONS"},
    "audit_mode": resolution["mode"],
    "audit_lean_workspace": resolution["lean_workspace"],
    "audit_lean_invocation": resolution["lean_invocation"],
    "audit_stage5_result": resolution["stage5_result"],
    "candidate_mount_exists": Path("/candidate").exists(),
    "classification_only_has_no_stage5": resolution["mode"]
    == "CLASSIFICATION_ONLY"
    and resolution["lean_workspace"] is None
    and resolution["lean_invocation"] is None
    and resolution["stage5_result"] is None
    and not Path("/candidate").exists(),
}

print(json.dumps(checks, indent=2, sort_keys=True))
