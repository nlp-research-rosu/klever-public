#!/usr/bin/env python3
"""Independent hash, obligation-bijection, and fixed-target audit for Stage 4."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

from tools import (
    k_rule_inventory,
    klean_export,
    lemma_discovery_contract,
    pipeline_contract,
    stage6_resolution_contract,
)


K_PROOF = Path("/reference/k-proof")
K_AUDIT = Path("/reference/k-audit")
DISCOVERY = Path("/reference/lemma-discovery.json")
GENERATION = Path("/reference/klean-generation")
GENERATED = GENERATION / "generated"
PRODUCERS = Path("/reference/generation-tools")
AUDIT_INPUT = Path("/audit-output/audit-input.json")
LOCK = Path("/reference/klean-toolchain.lock.json")


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check(label: str, condition: bool) -> None:
    print(f"CHECK {label}: {'PASS' if condition else 'FAIL'}")
    if not condition:
        raise SystemExit(1)


def canonical_digest(document: object) -> str:
    return stage6_resolution_contract.canonical_json_sha256(document)


envelope = json.loads(AUDIT_INPUT.read_text())
resolution, resolved_digest = stage6_resolution_contract.verify_audit_input(envelope)
validated = lemma_discovery_contract.validate_trust_boundary(K_PROOF, DISCOVERY)
input_manifest = json.loads((GENERATION / "input-manifest.json").read_text())
generator_manifest = json.loads((GENERATION / "generator-manifest.json").read_text())
export_result = json.loads((GENERATION / "export-result.json").read_text())
trust_inventory = json.loads((GENERATION / "trust-inventory.json").read_text())
preflight = json.loads((GENERATION / "preflight.json").read_text())
obligation_map = json.loads((GENERATED / "obligation-map.json").read_text())
toolchain_lock = json.loads(LOCK.read_text())

observed_resolution_hash = canonical_digest(resolution)
observed_pipeline_hashes = {
    "k_workspace_sha256": pipeline_contract.sha256_tree(K_PROOF),
    "stage1_export_sha256": klean_export.tree_digest(K_PROOF),
    "discovery_manifest_sha256": file_sha256(DISCOVERY),
    "k_audit_sha256": pipeline_contract.sha256_tree(K_AUDIT),
    "klean_generation_sha256": pipeline_contract.sha256_tree(GENERATION),
    "generation_producer_sources_sha256": pipeline_contract.sha256_tree(PRODUCERS),
    "generated_tree_sha256": klean_export.tree_digest(GENERATED),
    "lean_workspace_sha256": None,
    "lean_invocation_sha256": None,
}

observed_stage1_sources = {
    path.relative_to(K_PROOF).as_posix(): file_sha256(path)
    for path in pipeline_contract._walk_regular_files(
        K_PROOF, "frozen Stage 1 workspace"
    )
}
expected_stage1_sources = resolution["stage1_source_hashes"]
source_key_diff = sorted(
    set(observed_stage1_sources) ^ set(expected_stage1_sources)
)
source_value_diff = sorted(
    name
    for name in set(observed_stage1_sources) & set(expected_stage1_sources)
    if observed_stage1_sources[name] != expected_stage1_sources[name]
)

print(f"resolved_input_sha256.recorded={resolved_digest}")
print(f"resolved_input_sha256.observed={observed_resolution_hash}")
print(f"pipeline_hashes.recorded={json.dumps(resolution['hashes'], sort_keys=True)}")
print(f"pipeline_hashes.observed={json.dumps(observed_pipeline_hashes, sort_keys=True)}")
print(f"stage1_source_file_count.recorded={len(expected_stage1_sources)}")
print(f"stage1_source_file_count.observed={len(observed_stage1_sources)}")
print(f"stage1_source_map_digest.recorded={canonical_digest(expected_stage1_sources)}")
print(f"stage1_source_map_digest.observed={canonical_digest(observed_stage1_sources)}")
print(f"stage1_source_key_diff={source_key_diff!r}")
print(f"stage1_source_value_diff={source_value_diff!r}")

check("resolved-input canonical hash", observed_resolution_hash == resolved_digest)
check("all signed top-level artifact hashes", observed_pipeline_hashes == resolution["hashes"])
check("all signed Stage 1 per-file hashes", not source_key_diff and not source_value_diff)

inventory_hash = k_rule_inventory.canonical_json_sha256(validated["rules"])
discovery_hash = file_sha256(DISCOVERY)
verification_hash = file_sha256(K_PROOF / "verification.k")
stage1_export_hash = klean_export.tree_digest(K_PROOF)
generated_hash = klean_export.tree_digest(GENERATED)
obligation_map_hash = file_sha256(GENERATED / "obligation-map.json")
trust_inventory_hash = file_sha256(GENERATION / "trust-inventory.json")
exporter_hash = file_sha256(PRODUCERS / "klean_export.py")
klean_py_hash = file_sha256(PRODUCERS / "klean.py")

print(f"inventory_sha256.observed={inventory_hash}")
print(f"verification_sha256.observed={verification_hash}")
print(f"obligation_map_sha256.observed={obligation_map_hash}")
print(f"trust_inventory_sha256.observed={trust_inventory_hash}")

check("input manifest frozen Stage 1 hash", input_manifest["frozen_input_sha256"] == stage1_export_hash)
check("input manifest Stage 1 hash", input_manifest["stage1_workspace_sha256"] == stage1_export_hash)
check("input manifest discovery hash", input_manifest["stage3_discovery_manifest_sha256"] == discovery_hash)
check("input manifest inventory hash", input_manifest["inventory_sha256"] == inventory_hash)
check("input manifest verification hash", input_manifest["verification_sha256"] == verification_hash)

check("generator generated-tree hash", generator_manifest["generated_tree_sha256"] == generated_hash)
check("generator obligation-map hash", generator_manifest["obligation_map_sha256"] == obligation_map_hash)
check("generator exporter hash", generator_manifest["exporter_sha256"] == exporter_hash)
check("generator klean.py hash", generator_manifest["klean_py_sha256"] == klean_py_hash)
check("generator toolchain lock identity", generator_manifest["toolchain"] == toolchain_lock)
check("generator Stage 1 provenance", generator_manifest["provenance"]["stage1_workspace_sha256"] == stage1_export_hash)
check("generator Stage 3 provenance", generator_manifest["provenance"]["stage3_discovery_manifest_sha256"] == discovery_hash)
check("generator inventory provenance", generator_manifest["provenance"]["inventory_sha256"] == inventory_hash)

check("export-result frozen hash", export_result["frozen_input_sha256"] == stage1_export_hash)
check("export-result generated hash", export_result["generated_tree_sha256"] == generated_hash)
check("export-result discovery hash", export_result["stage3_discovery_manifest_sha256"] == discovery_hash)
check("export-result trust-inventory hash", export_result["trust_inventory_sha256"] == trust_inventory_hash)
check("signed preflight document identity", resolution["stage4_preflight"] == preflight)

for index, diagnostic in enumerate(preflight["diagnostics"]):
    tail = diagnostic["output_tail"]
    # These recorded outputs are shorter than the 4000-character retention
    # limit and their hashes equal the retained strings, so no prefix was lost.
    check(
        f"recorded preflight diagnostic {index} output hash",
        len(tail) < 4000
        and hashlib.sha256(tail.encode()).hexdigest()
        == diagnostic["output_sha256"],
    )

domain_source_rules = klean_export._domain_source_rules(validated, discovery_hash)
expected_ids = [rule["source_rule_id"] for rule in domain_source_rules]
mapped_ids = [
    obligation.get("source_rule_id")
    for obligation in obligation_map["obligations"]
]
all_lean_text = "\n".join(
    path.read_text()
    for path in sorted(GENERATED.rglob("*.lean"))
)
target = klean_export.target_statement(GENERATED)
expected_target_definition = klean_export.expected_target_definition(obligation_map)

print(f"domain_source_rules={json.dumps(domain_source_rules, sort_keys=True)}")
print(f"input_manifest.source_rules={json.dumps(input_manifest['source_rules'], sort_keys=True)}")
print(f"obligation_map={json.dumps(obligation_map, sort_keys=True)}")
print(f"target_statement.observed={target!r}")
print(f"target_definition.expected={expected_target_definition!r}")
print(f"trust_allowlist_count={len(trust_inventory['allowlist'])}")

check("independent DOMAIN_LEMMA source set empty", domain_source_rules == [])
check("input source-rule set exact", input_manifest["source_rules"] == domain_source_rules)
check("obligation-map source-rule set exact", obligation_map["source_rules"] == domain_source_rules)
check("ordered source-rule/obligation identity bijection", mapped_ids == expected_ids)
check("no duplicate obligation identity", len(mapped_ids) == len(set(mapped_ids)))
check("zero generated obligations", obligation_map["obligations"] == [])
check("zero trust parameters", obligation_map["trust_parameters"] == [])
check("generator obligation count", generator_manifest["obligation_count"] == 0)
check("export obligation count", export_result["obligation_count"] == 0)
check("preflight obligation count", preflight["obligation_count"] == 0)
check("no generated target declaration", re.search(r"(?m)^\s*def\s+targetStatement\b", all_lean_text) is None)
check("trusted target parser reports no target", target is None)
check("no expected target for empty conjunction", expected_target_definition is None)
check("generator target fixed to null", generator_manifest["target"] is None)
check("signed target fixed to null", resolution["target"] is None)
check("preflight target fixed to null", preflight["target"] is None)
check("export status is no-obligations", export_result["status"] == "KLEAN_NO_OBLIGATIONS")
check("preflight status is no-obligations", preflight["status"] == "KLEAN_NO_OBLIGATIONS")
check("selected status is no-obligations", resolution["selections"]["klean_generation"]["status"] == "KLEAN_NO_OBLIGATIONS")
check("no Stage 5 candidate", not Path("/candidate").exists())

print("MATHEMATICAL JUDGMENT: no obligation is omitted, weakened, duplicated, irrelevant, or vacuous because the independently classified domain set and generated conjunction are both empty")
print("RESULT: PASS")
