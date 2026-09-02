#!/usr/bin/env python3
"""Independent Stage 4 sidecar, obligation, and target-identity checks."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from tools import klean_export, lemma_discovery_contract


def load(path: Path) -> dict:
    value = json.loads(path.read_text())
    assert isinstance(value, dict)
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


generation = Path("/reference/klean-generation")
generated = generation / "generated"
discovery_path = Path("/reference/lemma-discovery.json")
input_manifest = load(generation / "input-manifest.json")
generator_manifest = load(generation / "generator-manifest.json")
export_result = load(generation / "export-result.json")
obligation_map_path = generated / "obligation-map.json"
obligation_map = load(obligation_map_path)
trust_inventory_path = generation / "trust-inventory.json"
trust_inventory = load(trust_inventory_path)
audit_input = load(Path("/audit-input.json"))["resolution"]
fresh_preflight = load(
    Path("/audit-output/evidence/02_preflight_return.json")
)
validated = lemma_discovery_contract.validate_trust_boundary(
    Path("/reference/k-proof"), discovery_path
)
discovery_hash = sha256(discovery_path)
domain_source_rules = klean_export._domain_source_rules(
    validated, discovery_hash
)

assert domain_source_rules == []
assert validated["domain_lemmas"] == []
assert input_manifest["source_rules"] == domain_source_rules
assert obligation_map["source_rules"] == domain_source_rules
obligations = obligation_map["obligations"]
assert obligations == []
assert obligation_map["trust_parameters"] == []
source_ids = [item["source_rule_id"] for item in domain_source_rules]
obligation_ids = [item["source_rule_id"] for item in obligations]
assert source_ids == obligation_ids
assert len(source_ids) == len(set(source_ids))
assert len(obligation_ids) == len(set(obligation_ids))

expected_definition = klean_export.expected_target_definition(obligation_map)
observed_target = klean_export.target_statement(generated)
assert expected_definition is None
assert observed_target is None
assert generator_manifest["target"] is None
assert audit_input["target"] is None
assert audit_input["stage4_preflight"]["target"] is None
assert fresh_preflight == audit_input["stage4_preflight"]
assert generator_manifest["obligation_count"] == 0
assert export_result["obligation_count"] == 0
assert audit_input["stage4_preflight"]["obligation_count"] == 0
assert export_result["status"] == "KLEAN_NO_OBLIGATIONS"
assert audit_input["selections"]["klean_generation"]["status"] == (
    "KLEAN_NO_OBLIGATIONS"
)
assert generator_manifest["obligation_map_sha256"] == sha256(
    obligation_map_path
)
assert generator_manifest["generated_tree_sha256"] == (
    klean_export.tree_digest(generated)
)
assert export_result["generated_tree_sha256"] == (
    generator_manifest["generated_tree_sha256"]
)
assert export_result["trust_inventory_sha256"] == sha256(
    trust_inventory_path
)
assert input_manifest["inventory_sha256"] == validated["inventory_sha256"]
assert generator_manifest["provenance"]["inventory_sha256"] == (
    validated["inventory_sha256"]
)
assert input_manifest["stage3_discovery_manifest_sha256"] == discovery_hash
assert generator_manifest["provenance"][
    "stage3_discovery_manifest_sha256"
] == discovery_hash
assert trust_inventory["designated_sorries"] == 0
assert trust_inventory["other_sorries"] == 0

lemmas_text = (
    generated / "Klean29FilterByPrefix/Lemmas.lean"
).read_text()
assert "def KleanTarget" not in lemmas_text
assert "theorem KleanTarget" not in lemmas_text

print(
    json.dumps(
        {
            "status": "PASS",
            "classification_domain_rule_ids": source_ids,
            "generated_obligation_ids": obligation_ids,
            "bijection_exact": source_ids == obligation_ids,
            "obligation_count": len(obligations),
            "expected_target_definition": expected_definition,
            "observed_target": observed_target,
            "generator_target": generator_manifest["target"],
            "audit_input_target": audit_input["target"],
            "export_status": export_result["status"],
            "fresh_preflight_matches_audit_input": (
                fresh_preflight == audit_input["stage4_preflight"]
            ),
            "obligation_map_sha256": sha256(obligation_map_path),
            "generated_tree_sha256": klean_export.tree_digest(generated),
            "trust_inventory_sha256": sha256(trust_inventory_path),
        },
        indent=2,
        sort_keys=True,
    )
)
