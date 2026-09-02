#!/usr/bin/env python3

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

from tools import klean_export, pipeline_contract
from tools.stage6_resolution_contract import canonical_json_sha256


ROOT = Path("/reference")
WORKSPACE = ROOT / "k-proof"
DISCOVERY = ROOT / "lemma-discovery.json"
GENERATION = ROOT / "klean-generation"
GENERATED = GENERATION / "generated"


def load(path: Path) -> dict:
    value = json.loads(path.read_text())
    assert isinstance(value, dict)
    return value


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


audit_input = load(Path("/audit-input.json"))
resolution = audit_input["resolution"]
input_manifest = load(GENERATION / "input-manifest.json")
generator_manifest = load(GENERATION / "generator-manifest.json")
export_result = load(GENERATION / "export-result.json")
recorded_preflight = load(GENERATION / "preflight.json")
trust_inventory = load(GENERATION / "trust-inventory.json")
obligation_map = load(GENERATED / "obligation-map.json")
toolchain_lock = load(ROOT / "klean-toolchain.lock.json")

# This value comes from the independent semantic classification recorded in
# REVIEW.md, not from the Stage 3 label being audited.
independent_domain_rule_ids: list[str] = []

source_rules = input_manifest["source_rules"]
obligation_source_rules = obligation_map["source_rules"]
obligations = obligation_map["obligations"]
parameters = obligation_map["trust_parameters"]

assert [rule["source_rule_id"] for rule in source_rules] == (
    independent_domain_rule_ids
)
assert source_rules == obligation_source_rules
source_ids = [rule["source_rule_id"] for rule in source_rules]
obligation_ids = [rule["source_rule_id"] for rule in obligations]
assert source_ids == obligation_ids
assert len(source_ids) == len(set(source_ids))
assert len(obligation_ids) == len(set(obligation_ids))
assert source_rules == []
assert obligations == []
assert parameters == []

expected_definition = klean_export.expected_target_definition(obligation_map)
parsed_target = klean_export.target_statement(GENERATED)
all_lean = "\n".join(
    path.read_text() for path in sorted(GENERATED.rglob("*.lean"))
)
raw_target_count = len(
    re.findall(r"(?m)^\s*def\s+targetStatement\b", all_lean)
)
assert expected_definition is None
assert parsed_target is None
assert raw_target_count == 0
assert generator_manifest["target"] is None
assert recorded_preflight["target"] is None
assert resolution["target"] is None
assert resolution["stage4_preflight"]["target"] is None
assert resolution["stage5_result"] is None
assert not Path("/candidate").exists()

generated_tree_hash = klean_export.tree_digest(GENERATED)
stage1_export_hash = klean_export.tree_digest(WORKSPACE)
discovery_hash = file_hash(DISCOVERY)
trust_inventory_hash = file_hash(GENERATION / "trust-inventory.json")
obligation_map_hash = file_hash(GENERATED / "obligation-map.json")
verification_hash = file_hash(WORKSPACE / "verification.k")

assert generator_manifest["generated_tree_sha256"] == generated_tree_hash
assert resolution["hashes"]["generated_tree_sha256"] == generated_tree_hash
assert input_manifest["frozen_input_sha256"] == stage1_export_hash
assert input_manifest["stage1_workspace_sha256"] == stage1_export_hash
assert generator_manifest["provenance"]["stage1_workspace_sha256"] == (
    stage1_export_hash
)
assert export_result["frozen_input_sha256"] == stage1_export_hash
assert recorded_preflight["frozen_input_sha256"] == stage1_export_hash
assert recorded_preflight["stage1_workspace_sha256"] == stage1_export_hash
assert resolution["hashes"]["stage1_export_sha256"] == stage1_export_hash
assert input_manifest["stage3_discovery_manifest_sha256"] == discovery_hash
assert generator_manifest["provenance"][
    "stage3_discovery_manifest_sha256"
] == discovery_hash
assert export_result["stage3_discovery_manifest_sha256"] == discovery_hash
assert recorded_preflight["stage3_discovery_manifest_sha256"] == (
    discovery_hash
)
assert resolution["hashes"]["discovery_manifest_sha256"] == discovery_hash
assert input_manifest["verification_sha256"] == verification_hash
assert generator_manifest["obligation_map_sha256"] == obligation_map_hash
assert export_result["trust_inventory_sha256"] == trust_inventory_hash
assert export_result["generated_tree_sha256"] == generated_tree_hash
assert generator_manifest["toolchain"] == toolchain_lock
assert generator_manifest["obligation_count"] == len(obligations)
assert export_result["obligation_count"] == len(obligations)
assert recorded_preflight["obligation_count"] == len(obligations)
assert resolution["stage4_preflight"]["obligation_count"] == len(obligations)
assert export_result["status"] == "KLEAN_NO_OBLIGATIONS"
assert recorded_preflight["status"] == "KLEAN_NO_OBLIGATIONS"
assert resolution["selections"]["klean_generation"]["status"] == (
    "KLEAN_NO_OBLIGATIONS"
)
assert trust_inventory["designated_sorries"] == 0
assert trust_inventory["other_sorries"] == 0

all_audit_hashes = {
    "k_workspace_sha256": pipeline_contract.sha256_tree(WORKSPACE),
    "k_audit_sha256": pipeline_contract.sha256_tree(ROOT / "k-audit"),
    "klean_generation_sha256": pipeline_contract.sha256_tree(GENERATION),
    "generation_producer_sources_sha256": pipeline_contract.sha256_tree(
        ROOT / "generation-tools"
    ),
    "generated_tree_sha256": generated_tree_hash,
    "stage1_export_sha256": stage1_export_hash,
    "discovery_manifest_sha256": discovery_hash,
    "lean_workspace_sha256": None,
    "lean_invocation_sha256": None,
}
assert all_audit_hashes == resolution["hashes"]
assert canonical_json_sha256(resolution) == audit_input[
    "resolved_input_sha256"
]

report = {
    "status": "PASS",
    "independent_domain_rule_ids": independent_domain_rule_ids,
    "source_rule_ids": source_ids,
    "obligation_ids": obligation_ids,
    "ordered_source_obligation_bijection": True,
    "vacuous_conjuncts": 0,
    "trust_parameters": parameters,
    "expected_target_definition": expected_definition,
    "parsed_target": parsed_target,
    "raw_target_declaration_count": raw_target_count,
    "candidate_absent": not Path("/candidate").exists(),
    "recorded_hashes": {
        **all_audit_hashes,
        "verification_sha256": verification_hash,
        "obligation_map_sha256": obligation_map_hash,
        "trust_inventory_sha256": trust_inventory_hash,
        "resolved_input_sha256": canonical_json_sha256(resolution),
    },
    "statuses": {
        "export_result": export_result["status"],
        "recorded_preflight": recorded_preflight["status"],
        "selected_generation": resolution["selections"]["klean_generation"][
            "status"
        ],
    },
}
print(json.dumps(report, indent=2, sort_keys=True))
