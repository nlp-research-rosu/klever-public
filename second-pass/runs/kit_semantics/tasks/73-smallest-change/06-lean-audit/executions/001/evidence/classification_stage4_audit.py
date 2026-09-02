#!/usr/bin/env python3
"""Reviewer-authored inventory, classification, and Stage 4 bijection checks."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import re
import sys
from pathlib import Path

from tools import k_rule_inventory, lemma_discovery_contract


WORKSPACE = Path("/reference/k-proof")
DISCOVERY = Path("/reference/lemma-discovery.json")
GENERATION = Path("/reference/klean-generation")
GENERATED = GENERATION / "generated"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text())


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


producer_path = Path("/reference/generation-tools/klean_export.py")
spec = importlib.util.spec_from_file_location(
    "authenticated_generation_klean_export", producer_path
)
assert spec is not None and spec.loader is not None
producer = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = producer
spec.loader.exec_module(producer)

inventory = k_rule_inventory.inventory_verification(WORKSPACE)
manifest = load_json(DISCOVERY)
validated = lemma_discovery_contract.validate_trust_boundary(WORKSPACE, DISCOVERY)
canonical_rules = inventory["rules"]
manifest_rules = manifest["rules"]
canonical_ids = [entry["source_rule_id"] for entry in canonical_rules]
manifest_ids = [entry["source_rule_id"] for entry in manifest_rules]

print(f"verification_module={inventory['verification_module']}")
print(f"verification_modules={json.dumps(inventory['verification_modules'])}")
print(f"verification_sha256={inventory['verification_sha256']}")
print(f"inventory_rule_count={len(canonical_rules)}")
print(f"inventory_sha256_reconstructed={inventory['inventory_sha256']}")
print(f"inventory_sha256_manifest={manifest['inventory_sha256']}")
print(f"inventory_hash_match={inventory['inventory_sha256'] == manifest['inventory_sha256']}")
print(f"canonical_ids={json.dumps(canonical_ids)}")
print(f"manifest_ids={json.dumps(manifest_ids)}")
print(f"identity_order_exact={canonical_ids == manifest_ids}")
print(f"identity_unique={len(manifest_ids) == len(set(manifest_ids))}")
print(f"identity_bijection={set(canonical_ids) == set(manifest_ids)}")

verification_lines = (WORKSPACE / "verification.k").read_text().splitlines()
for index, rule in enumerate(canonical_rules):
    span_text = "\n".join(
        verification_lines[rule["start_line"] - 1 : rule["end_line"]]
    )
    normalized = " ".join(span_text.split())
    normalized_hash = hashlib.sha256(normalized.encode()).hexdigest()
    expected_id = "rule-" + normalized_hash
    manifest_entry = manifest_rules[index]
    print(f"rule[{index}].module={rule['module']}")
    print(f"rule[{index}].span={rule['start_line']}:{rule['end_line']}")
    print(f"rule[{index}].attributes={json.dumps(rule['attributes'])}")
    print(f"rule[{index}].normalized_sha256_recomputed={normalized_hash}")
    print(f"rule[{index}].normalized_sha256_inventory={rule['normalized_sha256']}")
    print(f"rule[{index}].source_rule_id_recomputed={expected_id}")
    print(f"rule[{index}].source_rule_id_inventory={rule['source_rule_id']}")
    print(
        f"rule[{index}].span_hash_id_match="
        f"{normalized_hash == rule['normalized_sha256'] and expected_id == rule['source_rule_id']}"
    )
    print(f"rule[{index}].protected_classification={manifest_entry['classification']}")

print(f"validated_definitions={len(validated['definitions'])}")
print(f"validated_operational_rules={len(validated['operational_rules'])}")
print(f"validated_proved_derived_lemmas={len(validated['proved_derived_lemmas'])}")
print(f"validated_domain_lemmas={len(validated['domain_lemmas'])}")

# Independent classification mandated by the audit prompt. The sole rule is a
# whole-loop program summary. It is neither a defining equation nor an ordinary
# execution/observation rule. Stage 1 proved a strict generalization with free
# C and I, not this exact source rule, before installing the specialization.
independent_classifications = {
    canonical_rules[0]["source_rule_id"]: "DOMAIN_LEMMA"
}
print(f"independent_classifications={json.dumps(independent_classifications, sort_keys=True)}")
classification_mismatches = [
    {
        "source_rule_id": entry["source_rule_id"],
        "protected": entry["classification"],
        "independent": independent_classifications[entry["source_rule_id"]],
    }
    for entry in manifest_rules
    if entry["classification"]
    != independent_classifications[entry["source_rule_id"]]
]
print(f"classification_mismatches={json.dumps(classification_mismatches, sort_keys=True)}")

input_manifest = load_json(GENERATION / "input-manifest.json")
generator_manifest = load_json(GENERATION / "generator-manifest.json")
export_result = load_json(GENERATION / "export-result.json")
trust_inventory = load_json(GENERATION / "trust-inventory.json")
obligation_map = load_json(GENERATED / "obligation-map.json")

recorded_source_rules = obligation_map["source_rules"]
recorded_obligations = obligation_map["obligations"]
recorded_obligation_ids = [entry["source_rule_id"] for entry in recorded_obligations]
recorded_source_ids = [entry["source_rule_id"] for entry in recorded_source_rules]
independent_domain_rules = [
    rule
    for rule in canonical_rules
    if independent_classifications[rule["source_rule_id"]] == "DOMAIN_LEMMA"
]
independent_domain_ids = [rule["source_rule_id"] for rule in independent_domain_rules]

print(f"recorded_source_rule_ids={json.dumps(recorded_source_ids)}")
print(f"recorded_obligation_ids={json.dumps(recorded_obligation_ids)}")
print(f"recorded_source_obligation_bijection={recorded_source_ids == recorded_obligation_ids and len(recorded_obligation_ids) == len(set(recorded_obligation_ids))}")
print(f"independent_domain_rule_ids={json.dumps(independent_domain_ids)}")
print(f"independent_domain_rule_count={len(independent_domain_ids)}")
print(f"independent_obligation_bijection={independent_domain_ids == recorded_obligation_ids}")
print(f"omitted_independent_obligation_ids={json.dumps([rule_id for rule_id in independent_domain_ids if rule_id not in recorded_obligation_ids])}")

target = producer.target_statement(GENERATED)
expected_recorded_definition = producer.expected_target_definition(obligation_map)
raw_target_count = sum(
    len(re.findall(r"(?m)^\s*def\s+targetStatement\b", path.read_text()))
    for path in GENERATED.rglob("*.lean")
)
print(f"recorded_target={json.dumps(target, sort_keys=True)}")
print(f"expected_target_from_recorded_map={json.dumps(expected_recorded_definition)}")
print(f"raw_target_declaration_count={raw_target_count}")
print(f"generator_manifest_target={json.dumps(generator_manifest['target'], sort_keys=True)}")
print(f"export_status={export_result['status']}")
print(f"generator_obligation_count={generator_manifest['obligation_count']}")
print(f"export_obligation_count={export_result['obligation_count']}")
print(f"obligation_map_sha256_observed={sha256(GENERATED / 'obligation-map.json')}")
print(f"obligation_map_sha256_manifest={generator_manifest['obligation_map_sha256']}")
print(f"trust_inventory_sha256_observed={sha256(GENERATION / 'trust-inventory.json')}")
print(f"trust_inventory_sha256_export={export_result['trust_inventory_sha256']}")
print(f"trust_allowlist_count={len(trust_inventory['allowlist'])}")
print(f"input_source_rules_equal_obligation_map={input_manifest['source_rules'] == recorded_source_rules}")
print(f"candidate_exists={Path('/candidate').exists() or Path('/candidate').is_symlink()}")

sidecar_consistency = (
    generator_manifest["obligation_count"] == len(recorded_obligations)
    and export_result["obligation_count"] == len(recorded_obligations)
    and generator_manifest["obligation_map_sha256"]
    == sha256(GENERATED / "obligation-map.json")
    and export_result["trust_inventory_sha256"]
    == sha256(GENERATION / "trust-inventory.json")
    and generator_manifest["target"] == target
)
print(f"mechanical_sidecar_consistency={sidecar_consistency}")
print(f"mathematical_stage4_status_valid={len(independent_domain_ids) == 0}")
