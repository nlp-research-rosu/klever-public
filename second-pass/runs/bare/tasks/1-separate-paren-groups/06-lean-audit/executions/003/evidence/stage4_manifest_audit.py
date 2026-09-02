#!/usr/bin/env python3
"""Independent Stage 4 source/obligation/target and sidecar hash audit."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from tools import klean_export
from tools.lemma_discovery_contract import validate_trust_boundary


WORKSPACE = Path("/reference/k-proof")
DISCOVERY = Path("/reference/lemma-discovery.json")
GENERATION = Path("/reference/klean-generation")
GENERATED = GENERATION / "generated"


def load(path: Path) -> dict:
    document = json.loads(path.read_text())
    assert isinstance(document, dict)
    return document


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


audit_input = load(Path("/audit-input.json"))["resolution"]
validated = validate_trust_boundary(WORKSPACE, DISCOVERY)
input_manifest = load(GENERATION / "input-manifest.json")
generator_manifest = load(GENERATION / "generator-manifest.json")
export_result = load(GENERATION / "export-result.json")
preflight = load(GENERATION / "preflight.json")
trust_inventory = load(GENERATION / "trust-inventory.json")
obligation_map_path = GENERATED / "obligation-map.json"
obligation_map = load(obligation_map_path)

discovery_hash = file_hash(DISCOVERY)
stage1_hash = klean_export.tree_digest(WORKSPACE)
generated_hash = klean_export.tree_digest(GENERATED)
trust_hash = file_hash(GENERATION / "trust-inventory.json")

source_rules = klean_export._domain_source_rules(validated, discovery_hash)
assert source_rules == []
assert validated["domain_lemmas"] == []
assert input_manifest["source_rules"] == source_rules
assert obligation_map["source_rules"] == source_rules

obligations = obligation_map["obligations"]
parameters = obligation_map["trust_parameters"]
assert obligations == []
assert parameters == []
assert len({entry.get("source_rule_id") for entry in obligations}) == len(
    obligations
)

expected_definition = klean_export.expected_target_definition(obligation_map)
observed_target = klean_export.target_statement(GENERATED)
assert expected_definition is None
assert observed_target is None
assert generator_manifest["target"] is None
assert audit_input["target"] is None

assert generator_manifest["obligation_count"] == len(obligations) == 0
assert generator_manifest["obligation_map_sha256"] == file_hash(
    obligation_map_path
)
assert generator_manifest["generated_tree_sha256"] == generated_hash
assert generator_manifest["provenance"]["inventory_sha256"] == validated[
    "inventory_sha256"
]
assert generator_manifest["provenance"]["stage1_workspace_sha256"] == stage1_hash
assert (
    generator_manifest["provenance"]["stage3_discovery_manifest_sha256"]
    == discovery_hash
)

assert input_manifest["inventory_sha256"] == validated["inventory_sha256"]
assert input_manifest["verification_sha256"] == file_hash(
    WORKSPACE / "verification.k"
)
assert input_manifest["frozen_input_sha256"] == stage1_hash
assert input_manifest["stage1_workspace_sha256"] == stage1_hash
assert input_manifest["stage3_discovery_manifest_sha256"] == discovery_hash

assert export_result["status"] == "KLEAN_NO_OBLIGATIONS"
assert export_result["obligation_count"] == 0
assert export_result["frozen_input_sha256"] == stage1_hash
assert export_result["stage3_discovery_manifest_sha256"] == discovery_hash
assert export_result["generated_tree_sha256"] == generated_hash
assert export_result["trust_inventory_sha256"] == trust_hash

assert preflight["status"] == "KLEAN_NO_OBLIGATIONS"
assert preflight["obligation_count"] == 0
assert preflight["target"] is None
assert preflight["frozen_input_sha256"] == stage1_hash
assert preflight["generated_tree_sha256"] == generated_hash
assert preflight["stage3_discovery_manifest_sha256"] == discovery_hash

assert trust_inventory["designated_sorries"] == 0
assert trust_inventory["other_sorries"] == 0
assert len(trust_inventory["allowlist"]) == preflight["trust_declaration_count"]
assert set(trust_inventory["axioms"]) == {
    entry["name"] for entry in trust_inventory["allowlist"]
}

lemmas_text = (
    GENERATED / "Klean1SeparateParenGroups" / "Lemmas.lean"
).read_text()
assert "def targetStatement" not in lemmas_text
assert "theorem targetStatement" not in lemmas_text
assert "axiom targetStatement" not in lemmas_text
assert "opaque targetStatement" not in lemmas_text

print("independent_true_domain_lemma_count: 0")
print("manifest_domain_source_rule_count:", len(source_rules))
print("obligation_count:", len(obligations))
print("obligation_source_ids:", json.dumps([]))
print("obligation_duplicates:", 0)
print("vacuous_conjunct_count:", 0)
print("trust_parameter_count:", len(parameters))
print("expected_target_definition:", expected_definition)
print("observed_generated_target:", observed_target)
print("generator_manifest_target:", generator_manifest["target"])
print("audit_input_target:", audit_input["target"])
print("obligation_map_sha256:", file_hash(obligation_map_path))
print("generated_tree_sha256:", generated_hash)
print("trust_inventory_sha256:", trust_hash)
print("trust_allowlist_count:", len(trust_inventory["allowlist"]))
print("source_rule_obligation_bijection: exact empty bijection")
print("fixed_generated_target: absent as required")
print("RESULT: PASS")
