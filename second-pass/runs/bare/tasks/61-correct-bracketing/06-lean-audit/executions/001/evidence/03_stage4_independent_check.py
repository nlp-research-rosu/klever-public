#!/usr/bin/env python3
"""Independent Stage 4 hash, obligation, trust, and target checks."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from tools import (
    k_rule_inventory,
    klean_export,
    lemma_discovery_contract,
    stage6_resolution_contract,
)


WORKSPACE = Path("/reference/k-proof")
DISCOVERY = Path("/reference/lemma-discovery.json")
GENERATION = Path("/reference/klean-generation")
GENERATED = GENERATION / "generated"
AUDIT_INPUT = Path("/audit-input.json")
LOCK = Path("/reference/klean-toolchain.lock.json")


def load(path: Path) -> dict:
    return json.loads(path.read_text())


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


audit = load(AUDIT_INPUT)
resolution, _ = stage6_resolution_contract.verify_audit_input(audit)
validated = lemma_discovery_contract.validate_trust_boundary(
    WORKSPACE, DISCOVERY
)
inventory = k_rule_inventory.inventory_verification(WORKSPACE)
input_manifest = load(GENERATION / "input-manifest.json")
generator_manifest = load(GENERATION / "generator-manifest.json")
export_result = load(GENERATION / "export-result.json")
recorded_preflight = load(GENERATION / "preflight.json")
trust_inventory = load(GENERATION / "trust-inventory.json")
obligation_map = load(GENERATED / "obligation-map.json")
lock = load(LOCK)

workspace_export_hash = klean_export.tree_digest(WORKSPACE)
discovery_hash = digest(DISCOVERY)
generated_hash = klean_export.tree_digest(GENERATED)
verification_hash = digest(WORKSPACE / "verification.k")
obligation_map_hash = digest(GENERATED / "obligation-map.json")
trust_inventory_hash = digest(GENERATION / "trust-inventory.json")

checks = {
    "input.frozen_input_sha256": (
        input_manifest["frozen_input_sha256"],
        workspace_export_hash,
    ),
    "input.stage1_workspace_sha256": (
        input_manifest["stage1_workspace_sha256"],
        workspace_export_hash,
    ),
    "input.stage3_discovery_manifest_sha256": (
        input_manifest["stage3_discovery_manifest_sha256"],
        discovery_hash,
    ),
    "input.verification_sha256": (
        input_manifest["verification_sha256"],
        verification_hash,
    ),
    "input.inventory_sha256": (
        input_manifest["inventory_sha256"],
        inventory["inventory_sha256"],
    ),
    "generator.generated_tree_sha256": (
        generator_manifest["generated_tree_sha256"],
        generated_hash,
    ),
    "generator.obligation_map_sha256": (
        generator_manifest["obligation_map_sha256"],
        obligation_map_hash,
    ),
    "generator.provenance.stage1_workspace_sha256": (
        generator_manifest["provenance"]["stage1_workspace_sha256"],
        workspace_export_hash,
    ),
    "generator.provenance.stage3_discovery_manifest_sha256": (
        generator_manifest["provenance"][
            "stage3_discovery_manifest_sha256"
        ],
        discovery_hash,
    ),
    "generator.provenance.inventory_sha256": (
        generator_manifest["provenance"]["inventory_sha256"],
        inventory["inventory_sha256"],
    ),
    "export.frozen_input_sha256": (
        export_result["frozen_input_sha256"],
        workspace_export_hash,
    ),
    "export.stage3_discovery_manifest_sha256": (
        export_result["stage3_discovery_manifest_sha256"],
        discovery_hash,
    ),
    "export.generated_tree_sha256": (
        export_result["generated_tree_sha256"],
        generated_hash,
    ),
    "export.trust_inventory_sha256": (
        export_result["trust_inventory_sha256"],
        trust_inventory_hash,
    ),
}
for label, (expected, actual) in checks.items():
    print(f"{label}: recorded={expected} actual={actual} match={expected == actual}")
    assert expected == actual

assert input_manifest["definitions"] == validated["definitions"]
assert input_manifest["operational_rules"] == validated["operational_rules"]
assert input_manifest["proved_derived_lemmas"] == validated[
    "proved_derived_lemmas"
]
print("classified_inventory_export_exact=PASS")

domain_rules = validated["domain_lemmas"]
expected_source_rules = klean_export._domain_source_rules(
    validated, discovery_hash
)
assert domain_rules == []
assert expected_source_rules == []
assert input_manifest["source_rules"] == expected_source_rules
assert obligation_map["source_rules"] == expected_source_rules
print("independent_true_domain_set=[]")
print("source_rule_bijection=empty_exact")

obligations = obligation_map["obligations"]
assert obligations == []
assert obligation_map["trust_parameters"] == []
assert generator_manifest["obligation_count"] == 0
assert export_result["obligation_count"] == 0
assert recorded_preflight["obligation_count"] == 0
print("obligation_set=[]")
print("duplicates=0 omissions=0 extras=0 vacuous_conjuncts=0")

expected_definition = klean_export.expected_target_definition(obligation_map)
observed_target = klean_export.target_statement(GENERATED)
assert expected_definition is None
assert observed_target is None
assert generator_manifest["target"] is None
assert recorded_preflight["target"] is None
assert resolution["target"] is None
print("expected_target_definition=None")
print("observed_generated_target=None")
print("fixed_target_identity=PASS")

assert generator_manifest["toolchain"] == lock
assert export_result["status"] == "KLEAN_NO_OBLIGATIONS"
assert recorded_preflight["status"] == "KLEAN_NO_OBLIGATIONS"
assert resolution["selections"]["klean_generation"][
    "status"
] == "KLEAN_NO_OBLIGATIONS"
print("toolchain_lock_exact=PASS")
print("no_obligation_status_consistent=PASS")

sources = [
    path
    for _relative, kind, path in klean_export._tree_entries(GENERATED)
    if kind == "file" and path.suffix == ".lean"
]
declared = {}
for source in sources:
    for declaration in klean_export.lean_trust_declarations(source):
        name = declaration["name"]
        assert name not in declared
        declared[name] = (declaration["kind"], declaration["type"])
allowlisted = {}
for entry in trust_inventory["allowlist"]:
    name = entry["name"]
    assert name not in allowlisted
    allowlisted[name] = (entry["kind"], entry["type"])
assert declared == allowlisted
assert trust_inventory["designated_sorries"] == 0
assert trust_inventory["other_sorries"] == 0
print(f"generated_trust_declarations={len(declared)}")
print("generated_trust_inventory_exact=PASS")

assert not Path("/candidate").exists()
assert resolution["lean_workspace"] is None
assert resolution["lean_invocation"] is None
assert resolution["stage5_result"] is None
print("stage5_absence=PASS")
print("OVERALL=PASS")
