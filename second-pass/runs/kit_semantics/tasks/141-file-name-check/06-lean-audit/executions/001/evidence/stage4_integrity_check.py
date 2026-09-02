#!/usr/bin/env python3
import hashlib
import importlib.util
import json
import sys
from pathlib import Path

from tools.lemma_discovery_contract import validate_trust_boundary


def load_producer():
    path = Path("/reference/generation-tools/klean_export.py")
    spec = importlib.util.spec_from_file_location(
        "generation_time_klean_export", path
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def sha256_bytes(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


producer = load_producer()
workspace = Path("/reference/k-proof")
discovery_path = Path("/reference/lemma-discovery.json")
generation = Path("/reference/klean-generation")
generated = generation / "generated"
audit = json.loads(Path("/audit-input.json").read_text())["resolution"]
input_manifest = json.loads((generation / "input-manifest.json").read_text())
generator_manifest = json.loads(
    (generation / "generator-manifest.json").read_text()
)
export_result = json.loads((generation / "export-result.json").read_text())
obligation_map_path = generated / "obligation-map.json"
obligation_map = json.loads(obligation_map_path.read_text())

validated = validate_trust_boundary(workspace, discovery_path)
discovery_hash = sha256_bytes(discovery_path)
expected_source_rules = [
    {
        **rule,
        "inventory_sha256": validated["inventory_sha256"],
        "discovery_manifest_sha256": discovery_hash,
    }
    for rule in validated["domain_lemmas"]
]
obligations = obligation_map["obligations"]
source_ids = [item["source_rule_id"] for item in expected_source_rules]
obligation_ids = [item["source_rule_id"] for item in obligations]
expected_definition = producer.expected_target_definition(obligation_map)
actual_target = producer.target_statement(generated)
expected_definition_hash = producer.sha256_text(expected_definition)

obligation_hash_checks = [
    item["lean_conjunct_sha256"] == producer.sha256_text(item["lean_conjunct"])
    for item in obligations
]
span_and_provenance_checks = [
    obligation["source_span"]
    == {
        "start_line": source["start_line"],
        "end_line": source["end_line"],
    }
    and all(
        obligation[key] == source[key]
        for key in (
            "source_rule_id",
            "normalized_sha256",
            "inventory_sha256",
            "discovery_manifest_sha256",
        )
    )
    for source, obligation in zip(expected_source_rules, obligations)
]
checks = {
    "input_manifest_source_rules_exact": (
        input_manifest["source_rules"] == expected_source_rules
    ),
    "obligation_map_source_rules_exact": (
        obligation_map["source_rules"] == expected_source_rules
    ),
    "source_rule_ids_unique": len(source_ids) == len(set(source_ids)),
    "obligation_ids_unique": len(obligation_ids) == len(set(obligation_ids)),
    "ordered_source_obligation_bijection": (
        source_ids == obligation_ids
        and len(expected_source_rules) == len(obligations)
    ),
    "all_obligation_conjunct_hashes_match": all(obligation_hash_checks),
    "all_obligation_spans_and_provenance_match": (
        len(span_and_provenance_checks) == len(obligations)
        and all(span_and_provenance_checks)
    ),
    "obligation_map_hash_matches_generator": (
        sha256_bytes(obligation_map_path)
        == generator_manifest["obligation_map_sha256"]
    ),
    "obligation_count_matches_generator": (
        len(obligations) == generator_manifest["obligation_count"]
    ),
    "obligation_count_matches_export_result": (
        len(obligations) == export_result["obligation_count"]
    ),
    "actual_target_matches_generator_manifest": (
        actual_target == generator_manifest["target"]
    ),
    "actual_target_matches_audit_resolution": (
        actual_target == audit["target"]
    ),
    "actual_target_matches_audit_preflight": (
        actual_target == audit["stage4_preflight"]["target"]
    ),
    "target_definition_is_exact_generated_conjunction": (
        actual_target["definition_sha256"] == expected_definition_hash
    ),
    "generated_tree_matches_generator": (
        producer.tree_digest(generated)
        == generator_manifest["generated_tree_sha256"]
    ),
    "generated_tree_matches_audit_input": (
        producer.tree_digest(generated)
        == audit["hashes"]["generated_tree_sha256"]
    ),
}

result = {
    "expected_source_rules": expected_source_rules,
    "obligations": obligations,
    "source_rule_ids": source_ids,
    "obligation_ids": obligation_ids,
    "expected_target_definition": expected_definition,
    "expected_target_definition_sha256": expected_definition_hash,
    "actual_target": actual_target,
    "checks": checks,
    "overall": "PASS" if all(checks.values()) else "FAIL",
}
print(json.dumps(result, indent=2, sort_keys=True))
raise SystemExit(0 if all(checks.values()) else 1)
