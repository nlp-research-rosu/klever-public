#!/usr/bin/env python3
import hashlib
import json
import re
from pathlib import Path

from tools import klean_export
from tools.k_rule_inventory import inventory_verification


ROOT = Path("/reference/klean-generation")
GENERATED = ROOT / "generated"
DISCOVERY_PATH = Path("/reference/lemma-discovery.json")
AUDIT_PATH = Path("/audit-input.json")

discovery = json.loads(DISCOVERY_PATH.read_text())
audit = json.loads(AUDIT_PATH.read_text())["resolution"]
input_manifest = json.loads((ROOT / "input-manifest.json").read_text())
generator_manifest = json.loads((ROOT / "generator-manifest.json").read_text())
export_result = json.loads((ROOT / "export-result.json").read_text())
obligation_map_path = GENERATED / "obligation-map.json"
obligation_map = json.loads(obligation_map_path.read_text())
inventory = inventory_verification(Path("/reference/k-proof"))

domain_ids = [
    entry["source_rule_id"]
    for entry in discovery["rules"]
    if entry["classification"] == "DOMAIN_LEMMA"
]
manifest_definition_ids = [
    entry["source_rule_id"] for entry in input_manifest["definitions"]
]
canonical_ids = [entry["source_rule_id"] for entry in inventory["rules"]]
lean_texts = {
    path.relative_to(GENERATED).as_posix(): path.read_text()
    for path in sorted(GENERATED.rglob("*.lean"))
}
combined_lean = "\n".join(lean_texts.values())
target = klean_export.target_statement(GENERATED)
expected_target = klean_export.expected_target_definition(obligation_map)

source_rule_ids = [
    entry["source_rule_id"] for entry in obligation_map["source_rules"]
]
obligation_ids = [
    entry["source_rule_id"] for entry in obligation_map["obligations"]
]
vacuous_conjuncts = [
    entry
    for entry in obligation_map["obligations"]
    if entry.get("lean_conjunct", "").strip() in {"True", "(True)"}
]

checks = {
    "independently_classified_domain_set_empty": domain_ids == [],
    "all_19_rules_exported_as_definitions_in_canonical_order": (
        manifest_definition_ids == canonical_ids and len(canonical_ids) == 19
    ),
    "input_manifest_domain_source_rules_exact": input_manifest["source_rules"] == [],
    "obligation_map_source_rules_exact": obligation_map["source_rules"] == [],
    "obligation_map_obligations_exact": obligation_map["obligations"] == [],
    "obligation_map_trust_parameters_exact": obligation_map["trust_parameters"] == [],
    "source_rule_obligation_id_bijection": (
        source_rule_ids == obligation_ids
        and len(source_rule_ids) == len(set(source_rule_ids))
    ),
    "no_vacuous_true_conjunct": vacuous_conjuncts == [],
    "generator_obligation_count_zero": generator_manifest["obligation_count"] == 0,
    "export_obligation_count_zero": export_result["obligation_count"] == 0,
    "generator_target_null": generator_manifest["target"] is None,
    "audit_target_null": audit["target"] is None,
    "preflight_target_null": audit["stage4_preflight"]["target"] is None,
    "trusted_target_parser_finds_no_target": target is None,
    "expected_target_definition_is_none": expected_target is None,
    "no_target_or_final_declaration_in_lean": re.search(
        r"(?m)^\s*(?:def|theorem|lemma|axiom|opaque)\s+(?:KleanTarget|target|final)\b",
        combined_lean,
    ) is None,
    "lemmas_namespace_has_no_declarations": (
        lean_texts["Klean11StringXor/Lemmas.lean"].strip()
        == (
            "import Klean11StringXor.Inj\n\n"
            "/- K trust-boundary goals. The second-pass agent must replace every\n"
            "   writable opaque stub with an honest definition and prove this\n"
            "   immutable proposition in the separate Proof.lean workspace. -/\n\n"
            "namespace Klean11StringXor.Lemmas\n\n"
            "end Klean11StringXor.Lemmas"
        )
    ),
    "obligation_map_hash_matches_generator": (
        hashlib.sha256(obligation_map_path.read_bytes()).hexdigest()
        == generator_manifest["obligation_map_sha256"]
    ),
    "audit_mode_classification_only": audit["mode"] == "CLASSIFICATION_ONLY",
    "audit_stage5_result_absent": audit["stage5_result"] is None,
    "audit_lean_paths_absent": (
        audit["lean_workspace"] is None and audit["lean_invocation"] is None
    ),
    "candidate_mount_absent": not Path("/candidate").exists(),
}

result = {
    "canonical_rule_count": len(canonical_ids),
    "independent_domain_rule_ids": domain_ids,
    "obligation_map_source_rule_ids": source_rule_ids,
    "obligation_ids": obligation_ids,
    "target_statement": target,
    "expected_target_definition": expected_target,
    "vacuous_conjuncts": vacuous_conjuncts,
    "checks": checks,
    "all_checks_pass": all(checks.values()),
}
print(json.dumps(result, indent=2, sort_keys=True))
