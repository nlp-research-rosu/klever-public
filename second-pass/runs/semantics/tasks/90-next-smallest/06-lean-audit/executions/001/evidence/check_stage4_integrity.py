#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

from tools import klean_export
from tools.lemma_discovery_contract import validate_trust_boundary
from tools.pipeline_contract import sha256_tree


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


audit = json.loads(Path("/audit-input.json").read_text())
resolution = audit["resolution"]
generation = Path("/reference/klean-generation")
generated = generation / "generated"
workspace = Path("/reference/k-proof")
discovery_path = Path("/reference/lemma-discovery.json")
validated = validate_trust_boundary(workspace, discovery_path)
input_manifest = json.loads((generation / "input-manifest.json").read_text())
generator_manifest = json.loads(
    (generation / "generator-manifest.json").read_text()
)
obligation_map_path = generated / "obligation-map.json"
obligation_map = json.loads(obligation_map_path.read_text())

domain_rules = validated["domain_lemmas"]
obligations = obligation_map["obligations"]
source_rules = obligation_map["source_rules"]
domain_ids = [rule["source_rule_id"] for rule in domain_rules]
source_ids = [rule["source_rule_id"] for rule in source_rules]
obligation_ids = [item["source_rule_id"] for item in obligations]
discovery_sha256 = file_sha256(discovery_path)
expected_definition = klean_export.expected_target_definition(obligation_map)
actual_target = klean_export.target_statement(generated)

stage1_source_mismatches = {}
for relative, expected in resolution["stage1_source_hashes"].items():
    path = workspace / relative
    observed = file_sha256(path) if path.is_file() else None
    if observed != expected:
        stage1_source_mismatches[relative] = {
            "expected": expected,
            "observed": observed,
        }

binding_checks = []
for parameter in obligation_map["trust_parameters"]:
    binding = {
        "kore_symbol": parameter["kore_symbol"],
        "name": parameter["name"],
        "source_rule_ids": parameter["source_rule_ids"],
        "type": parameter["type"],
    }
    binding_checks.append(
        {
            "name": parameter["name"],
            "binding_sha256_exact": (
                parameter["binding_sha256"]
                == klean_export.sha256_text(
                    json.dumps(
                        binding,
                        sort_keys=True,
                        separators=(",", ":"),
                    )
                )
            ),
            "bound_exactly_to_domain_rule": (
                parameter["source_rule_ids"] == domain_ids
            ),
        }
    )

obligation_checks = []
for source, obligation in zip(source_rules, obligations):
    obligation_checks.append(
        {
            "source_rule_id": obligation["source_rule_id"],
            "normalized_sha256_exact": (
                obligation["normalized_sha256"]
                == source["normalized_sha256"]
            ),
            "inventory_sha256_exact": (
                obligation["inventory_sha256"]
                == source["inventory_sha256"]
                == validated["inventory_sha256"]
            ),
            "discovery_sha256_exact": (
                obligation["discovery_manifest_sha256"]
                == source["discovery_manifest_sha256"]
                == discovery_sha256
            ),
            "source_span_exact": (
                obligation["source_span"]
                == {
                    "start_line": source["start_line"],
                    "end_line": source["end_line"],
                }
            ),
            "conjunct_sha256_exact": (
                obligation["lean_conjunct_sha256"]
                == klean_export.sha256_text(obligation["lean_conjunct"])
            ),
            "not_literal_true_or_false": (
                obligation["lean_conjunct"].strip() not in {"True", "False"}
            ),
            "is_universal_rewrite_obligation": (
                obligation["lean_conjunct"].lstrip().startswith("∀ ")
                and ", Rewrites " in obligation["lean_conjunct"]
            ),
        }
    )

recorded_hash_checks = {
    "stage1_pipeline_tree": (
        sha256_tree(workspace)
        == resolution["hashes"]["k_workspace_sha256"]
    ),
    "stage1_export_tree": (
        klean_export.tree_digest(workspace)
        == resolution["hashes"]["stage1_export_sha256"]
    ),
    "stage2_pipeline_tree": (
        sha256_tree(Path("/reference/k-audit"))
        == resolution["hashes"]["k_audit_sha256"]
    ),
    "discovery_file": (
        discovery_sha256
        == resolution["hashes"]["discovery_manifest_sha256"]
    ),
    "generation_pipeline_tree": (
        sha256_tree(generation)
        == resolution["hashes"]["klean_generation_sha256"]
    ),
    "generated_export_tree": (
        klean_export.tree_digest(generated)
        == resolution["hashes"]["generated_tree_sha256"]
    ),
    "candidate_pipeline_tree": (
        sha256_tree(Path("/candidate"))
        == resolution["hashes"]["lean_workspace_sha256"]
    ),
}

checks = {
    "all_stage1_source_hashes_exact": not stage1_source_mismatches,
    "all_recorded_mounted_tree_hashes_exact": all(
        recorded_hash_checks.values()
    ),
    "one_genuine_domain_rule": len(domain_rules) == 1,
    "source_rule_bijection_exact_order": (
        domain_ids == source_ids == obligation_ids
        and len(set(obligation_ids)) == len(obligation_ids)
    ),
    "all_obligation_provenance_exact": all(
        all(
            value
            for key, value in item.items()
            if key != "source_rule_id"
        )
        for item in obligation_checks
    ),
    "all_binding_hashes_and_links_exact": all(
        item["binding_sha256_exact"]
        and item["bound_exactly_to_domain_rule"]
        for item in binding_checks
    ),
    "input_manifest_source_rules_exact": (
        input_manifest["source_rules"] == source_rules
    ),
    "obligation_map_hash_exact": (
        generator_manifest["obligation_map_sha256"]
        == file_sha256(obligation_map_path)
    ),
    "target_definition_is_exact_conjunction": (
        expected_definition is not None
        and actual_target is not None
        and actual_target["definition_sha256"]
        == klean_export.sha256_text(expected_definition)
    ),
    "target_matches_generator_manifest": (
        actual_target == generator_manifest["target"]
    ),
    "target_matches_audit_input_resolution": (
        actual_target == resolution["target"]
    ),
    "target_matches_recorded_preflight": (
        actual_target == resolution["stage4_preflight"]["target"]
    ),
    "obligation_count_exact": (
        len(obligations)
        == generator_manifest["obligation_count"]
        == resolution["stage4_preflight"]["obligation_count"]
        == 1
    ),
}

result = {
    "recorded_hash_checks": recorded_hash_checks,
    "stage1_source_mismatches": stage1_source_mismatches,
    "domain_rule_ids": domain_ids,
    "source_rule_ids": source_ids,
    "obligation_rule_ids": obligation_ids,
    "obligation_checks": obligation_checks,
    "binding_checks": binding_checks,
    "actual_target": actual_target,
    "expected_target_definition_sha256": (
        klean_export.sha256_text(expected_definition)
        if expected_definition is not None
        else None
    ),
    "checks": checks,
    "status": "PASS" if all(checks.values()) else "FAIL",
}
print(json.dumps(result, indent=2, sort_keys=True))
