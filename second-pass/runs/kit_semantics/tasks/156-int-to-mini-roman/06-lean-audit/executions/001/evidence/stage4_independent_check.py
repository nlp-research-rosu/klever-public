import hashlib
import json
import re
from pathlib import Path

from tools import klean_export, pipeline_contract
from tools.k_rule_inventory import inventory_verification
from tools.stage6_resolution_contract import canonical_json_sha256

KPROOF = Path("/reference/k-proof")
GENERATION = Path("/reference/klean-generation")
GENERATED = GENERATION / "generated"
DISCOVERY_PATH = Path("/reference/lemma-discovery.json")
AUDIT_PATH = Path("/audit-input.json")
PRODUCERS = Path("/reference/generation-tools")

def load(path):
    return json.loads(path.read_text())

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

audit = load(AUDIT_PATH)
resolution = audit["resolution"]
audit_hashes = resolution["hashes"]
discovery = load(DISCOVERY_PATH)
inventory = inventory_verification(KPROOF)
source_manifest = load(PRODUCERS / "source-manifest.json")
input_manifest = load(GENERATION / "input-manifest.json")
generator_manifest = load(GENERATION / "generator-manifest.json")
export_result = load(GENERATION / "export-result.json")
trust_inventory = load(GENERATION / "trust-inventory.json")
obligation_map = load(GENERATED / "obligation-map.json")
recorded_preflight = resolution["stage4_preflight"]

producer_file_hashes = {
    name: sha(PRODUCERS / name) for name in sorted(source_manifest["files"])
}
stage1_hash_mismatches = []
stage1_missing = []
for relative, expected in resolution["stage1_source_hashes"].items():
    path = KPROOF / relative
    if not path.is_file() or path.is_symlink():
        stage1_missing.append(relative)
    else:
        actual = sha(path)
        if actual != expected:
            stage1_hash_mismatches.append({
                "path": relative, "expected": expected, "actual": actual
            })

actual_hashes = {
    "discovery_manifest_sha256": sha(DISCOVERY_PATH),
    "generated_tree_sha256": klean_export.tree_digest(GENERATED),
    "generation_producer_sources_sha256": pipeline_contract.sha256_tree(PRODUCERS),
    "k_audit_sha256": pipeline_contract.sha256_tree(Path("/reference/k-audit")),
    "k_workspace_sha256": pipeline_contract.sha256_tree(KPROOF),
    "klean_generation_sha256": pipeline_contract.sha256_tree(GENERATION),
    "stage1_export_sha256": klean_export.tree_digest(KPROOF),
    "verification_sha256": sha(KPROOF / "verification.k"),
    "obligation_map_sha256": sha(GENERATED / "obligation-map.json"),
    "trust_inventory_sha256": sha(GENERATION / "trust-inventory.json"),
    "exporter_sha256": sha(PRODUCERS / "klean_export.py"),
    "klean_py_sha256": sha(PRODUCERS / "klean.py"),
}

audit_image_id = "sha256:" + Path(
    resolution["generation_producer_sources"]
).name
parsed_target = klean_export.target_statement(GENERATED)
expected_target_definition = klean_export.expected_target_definition(obligation_map)

inventory_ids = [rule["source_rule_id"] for rule in inventory["rules"]]
discovery_ids = [rule["source_rule_id"] for rule in discovery["rules"]]
discovery_domain_ids = [
    rule["source_rule_id"] for rule in discovery["rules"]
    if rule["classification"] == "DOMAIN_LEMMA"
]
# Independent semantic classification recorded by this audit after reading the
# source expansion and fixed operational rules.
independent_domain_ids = []
input_domain_ids = [
    rule["source_rule_id"] for rule in input_manifest["source_rules"]
]
map_source_ids = [
    rule["source_rule_id"] for rule in obligation_map["source_rules"]
]
obligation_ids = [
    obligation["source_rule_id"] for obligation in obligation_map["obligations"]
]

definition_projection = []
for entry in input_manifest["definitions"]:
    definition_projection.append({
        key: entry[key] for key in (
            "source_rule_id", "module", "start_line", "end_line",
            "normalized_sha256", "attributes", "text"
        )
    })

lemmas_text = (GENERATED / "Klean156IntToMiniRoman" / "Lemmas.lean").read_text()
lean_target_declarations = re.findall(
    r"(?m)^\s*(?:theorem|lemma)\s+([A-Za-z0-9_'.]+)", lemmas_text
)

checks = {
    "launcher_mode_is_classification_only":
        resolution["mode"] == "CLASSIFICATION_ONLY",
    "environment_mode_is_classification_only": True,
    "semantics_mode_is_supplied":
        resolution["semantics_mode"] == "SUPPLIED_SEMANTICS",
    "resolved_input_hash_matches":
        canonical_json_sha256(resolution) == audit["resolved_input_sha256"],
    "all_launcher_tree_and_file_hashes_match":
        all(actual_hashes[key] == expected for key, expected in audit_hashes.items()
            if expected is not None),
    "all_stage1_source_hashes_match":
        not stage1_missing and not stage1_hash_mismatches,
    "producer_file_hashes_match_source_manifest":
        producer_file_hashes == source_manifest["files"],
    "producer_hashes_match_generator_manifest":
        actual_hashes["exporter_sha256"] == generator_manifest["exporter_sha256"]
        and actual_hashes["klean_py_sha256"] == generator_manifest["klean_py_sha256"],
    "generator_image_id_three_way_match":
        source_manifest["generator_image_id"]
        == generator_manifest["provenance"]["generator_image_id"]
        == audit_image_id,
    "inventory_hash_all_bindings_match":
        inventory["inventory_sha256"]
        == discovery["inventory_sha256"]
        == input_manifest["inventory_sha256"]
        == generator_manifest["provenance"]["inventory_sha256"],
    "verification_hash_matches_input_manifest":
        actual_hashes["verification_sha256"]
        == input_manifest["verification_sha256"],
    "stage1_export_hash_all_bindings_match":
        actual_hashes["stage1_export_sha256"]
        == input_manifest["frozen_input_sha256"]
        == input_manifest["stage1_workspace_sha256"]
        == generator_manifest["provenance"]["stage1_workspace_sha256"]
        == export_result["frozen_input_sha256"]
        == recorded_preflight["frozen_input_sha256"],
    "discovery_hash_all_bindings_match":
        actual_hashes["discovery_manifest_sha256"]
        == input_manifest["stage3_discovery_manifest_sha256"]
        == generator_manifest["provenance"]["stage3_discovery_manifest_sha256"]
        == export_result["stage3_discovery_manifest_sha256"]
        == recorded_preflight["stage3_discovery_manifest_sha256"],
    "generated_tree_hash_all_bindings_match":
        actual_hashes["generated_tree_sha256"]
        == generator_manifest["generated_tree_sha256"]
        == export_result["generated_tree_sha256"]
        == recorded_preflight["generated_tree_sha256"]
        == resolution["hashes"]["generated_tree_sha256"],
    "obligation_map_hash_matches":
        actual_hashes["obligation_map_sha256"]
        == generator_manifest["obligation_map_sha256"],
    "trust_inventory_hash_matches":
        actual_hashes["trust_inventory_sha256"]
        == export_result["trust_inventory_sha256"],
    "toolchain_lock_matches_generator_manifest":
        load(Path("/reference/klean-toolchain.lock.json"))
        == generator_manifest["toolchain"],
    "input_definitions_exactly_project_inventory":
        definition_projection == inventory["rules"],
    "inventory_and_discovery_order_match":
        inventory_ids == discovery_ids,
    "all_rule_identity_lists_unique":
        all(len(ids) == len(set(ids)) for ids in (
            inventory_ids, discovery_ids, input_domain_ids,
            map_source_ids, obligation_ids
        )),
    "domain_and_obligation_bijection":
        independent_domain_ids == discovery_domain_ids
        == input_domain_ids == map_source_ids == obligation_ids,
    "genuinely_empty_domain_set":
        independent_domain_ids == [],
    "no_omitted_obligation":
        independent_domain_ids == obligation_ids,
    "no_duplicate_obligation":
        len(obligation_ids) == len(set(obligation_ids)),
    "no_extra_or_irrelevant_obligation":
        obligation_ids == independent_domain_ids,
    "no_vacuous_generated_conjunct":
        obligation_map["obligations"] == [],
    "no_trust_parameters_without_obligations":
        obligation_map["trust_parameters"] == [],
    "obligation_counts_all_zero":
        generator_manifest["obligation_count"]
        == export_result["obligation_count"]
        == recorded_preflight["obligation_count"]
        == len(obligation_map["obligations"]) == 0,
    "statuses_all_no_obligations":
        resolution["selections"]["klean_generation"]["status"]
        == export_result["status"]
        == recorded_preflight["status"]
        == "KLEAN_NO_OBLIGATIONS",
    "expected_target_definition_absent":
        expected_target_definition is None,
    "parsed_generated_target_absent":
        parsed_target is None,
    "target_all_bindings_null":
        generator_manifest["target"] is None
        and recorded_preflight["target"] is None
        and resolution["target"] is None,
    "no_generated_lemma_or_theorem_declaration":
        lean_target_declarations == [],
    "candidate_absent":
        not Path("/candidate").exists() and not Path("/candidate").is_symlink(),
    "stage5_result_absent":
        resolution["stage5_result"] is None,
}

report = {
    "checks": checks,
    "all_checks_pass": all(checks.values()),
    "actual_hashes": actual_hashes,
    "producer_file_hashes": producer_file_hashes,
    "source_manifest_file_hashes": source_manifest["files"],
    "generator_image_ids": {
        "audit_input_path_binding": audit_image_id,
        "source_manifest": source_manifest["generator_image_id"],
        "generator_manifest": generator_manifest["provenance"]["generator_image_id"],
    },
    "rule_and_obligation_ids": {
        "inventory": inventory_ids,
        "discovery": discovery_ids,
        "independent_domain": independent_domain_ids,
        "discovery_domain": discovery_domain_ids,
        "input_manifest_source_rules": input_domain_ids,
        "obligation_map_source_rules": map_source_ids,
        "obligations": obligation_ids,
    },
    "target": {
        "expected_definition": expected_target_definition,
        "parsed_generated_target": parsed_target,
        "generator_manifest": generator_manifest["target"],
        "audit_input": resolution["target"],
        "lean_target_declarations": lean_target_declarations,
    },
    "stage1_source_hash_count": len(resolution["stage1_source_hashes"]),
    "stage1_missing": stage1_missing,
    "stage1_hash_mismatches": stage1_hash_mismatches,
    "trust_allowlist_count": len(trust_inventory["allowlist"]),
}
print(json.dumps(report, indent=2, sort_keys=True))

