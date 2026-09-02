#!/usr/bin/env python3
"""Independent Stage 4 hash, bijection, status, and target checks."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from tools import klean_export, lemma_discovery_contract


STAGE1 = Path("/reference/k-proof")
DISCOVERY = Path("/reference/lemma-discovery.json")
GENERATION = Path("/reference/klean-generation")
GENERATED = GENERATION / "generated"


def load(path: Path) -> dict:
    return json.loads(path.read_text())


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def report(name: str, observed: object, expected: object) -> bool:
    matched = observed == expected
    print(
        f"{name}: matched={matched} observed={observed!r} expected={expected!r}"
    )
    return matched


audit = load(Path("/audit-input.json"))["resolution"]
input_manifest = load(GENERATION / "input-manifest.json")
generator_manifest = load(GENERATION / "generator-manifest.json")
export_result = load(GENERATION / "export-result.json")
trust_inventory = load(GENERATION / "trust-inventory.json")
obligation_map = load(GENERATED / "obligation-map.json")
selected_preflight = load(GENERATION / "preflight.json")
lock = load(Path("/reference/klean-toolchain.lock.json"))
validated = lemma_discovery_contract.validate_trust_boundary(STAGE1, DISCOVERY)
domain_source_rules = klean_export._domain_source_rules(validated, sha(DISCOVERY))

# These are the independent semantic classifications justified in REVIEW.md.
independent_roles = {
    "rule-c81ca83083d7457acd8bc03869be055c6f82860af5fcb6ab0df7413577ec1931": "DEFINITION",
    "rule-424ad9bede59bccdcf23851333637603f57a311d80fcb5fef99140e39aae7991": "DEFINITION",
    "rule-738ed76d501e1fe77a5aa4c3808cc7f2254b9f6b94e6b2a6378b84afed317e55": "DEFINITION",
}
canonical_ids = [rule["source_rule_id"] for rule in validated["rules"]]
independent_domain_ids = [
    source_rule_id
    for source_rule_id in canonical_ids
    if independent_roles[source_rule_id] == "DOMAIN_LEMMA"
]

checks: list[bool] = []
checks.append(report("independent_roles_exact_inventory", list(independent_roles), canonical_ids))
checks.append(report("independent_domain_ids", independent_domain_ids, []))
checks.append(report("contract_domain_source_rules", domain_source_rules, []))
checks.append(report("input_source_rules", input_manifest["source_rules"], domain_source_rules))
checks.append(report("map_source_rules", obligation_map["source_rules"], domain_source_rules))
checks.append(report("map_obligations", obligation_map["obligations"], []))
checks.append(report("map_trust_parameters", obligation_map["trust_parameters"], []))

checks.append(report("generator_obligation_count", generator_manifest["obligation_count"], 0))
checks.append(report("export_obligation_count", export_result["obligation_count"], 0))
checks.append(report("selected_preflight_obligation_count", selected_preflight["obligation_count"], 0))
checks.append(report("export_status", export_result["status"], "KLEAN_NO_OBLIGATIONS"))
checks.append(report("selected_preflight_status", selected_preflight["status"], "KLEAN_NO_OBLIGATIONS"))
checks.append(
    report(
        "audit_selected_status",
        audit["selections"]["klean_generation"]["status"],
        "KLEAN_NO_OBLIGATIONS",
    )
)

stage1_tree = klean_export.tree_digest(STAGE1)
generated_tree = klean_export.tree_digest(GENERATED)
discovery_hash = sha(DISCOVERY)
verification_hash = sha(STAGE1 / "verification.k")
inventory_hash = validated["inventory_sha256"]
checks.append(report("input_frozen_hash", input_manifest["frozen_input_sha256"], stage1_tree))
checks.append(report("input_stage1_hash", input_manifest["stage1_workspace_sha256"], stage1_tree))
checks.append(report("input_discovery_hash", input_manifest["stage3_discovery_manifest_sha256"], discovery_hash))
checks.append(report("input_verification_hash", input_manifest["verification_sha256"], verification_hash))
checks.append(report("input_inventory_hash", input_manifest["inventory_sha256"], inventory_hash))
checks.append(report("generator_tree_hash", generator_manifest["generated_tree_sha256"], generated_tree))
checks.append(report("generator_toolchain_lock", generator_manifest["toolchain"], lock))
checks.append(report("generator_obligation_map_hash", generator_manifest["obligation_map_sha256"], sha(GENERATED / "obligation-map.json")))
checks.append(report("generator_inventory_provenance", generator_manifest["provenance"]["inventory_sha256"], inventory_hash))
checks.append(report("export_frozen_hash", export_result["frozen_input_sha256"], stage1_tree))
checks.append(report("export_discovery_hash", export_result["stage3_discovery_manifest_sha256"], discovery_hash))
checks.append(report("export_generated_hash", export_result["generated_tree_sha256"], generated_tree))
checks.append(report("export_trust_hash", export_result["trust_inventory_sha256"], sha(GENERATION / "trust-inventory.json")))

expected_definition = klean_export.expected_target_definition(obligation_map)
observed_target = klean_export.target_statement(GENERATED)
checks.append(report("expected_target_definition", expected_definition, None))
checks.append(report("observed_generated_target", observed_target, None))
checks.append(report("generator_target", generator_manifest["target"], None))
checks.append(report("audit_input_target", audit["target"], None))
checks.append(report("candidate_absent", Path("/candidate").exists(), False))

print(f"definitions_count={len(input_manifest['definitions'])}")
print(f"operational_rules_count={len(input_manifest['operational_rules'])}")
print(f"proved_derived_lemmas_count={len(input_manifest['proved_derived_lemmas'])}")
print(f"domain_rules_count={len(domain_source_rules)}")
print(f"trust_allowlist_count={len(trust_inventory['allowlist'])}")
print(f"ALL_INDEPENDENT_STAGE4_CHECKS_PASS={all(checks)}")
