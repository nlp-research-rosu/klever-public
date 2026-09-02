#!/usr/bin/env python3
"""Independent Stage 4 provenance, hash, obligation, and target checks."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

from tools.klean_export import target_statement, tree_digest
from tools.pipeline_contract import sha256_tree
from tools.stage6_resolution_contract import verify_audit_input


def load(path: Path) -> dict:
    value = json.loads(path.read_text())
    assert isinstance(value, dict)
    return value


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


audit = load(Path("/audit-input.json"))
resolution, envelope_hash = verify_audit_input(audit)
assert resolution["mode"] == "CLASSIFICATION_AND_PROOF"
assert resolution["condition"] == "kit-semantics"
assert resolution["semantics_mode"] == "SUPPLIED_SEMANTICS"
print("audit envelope: OK", envelope_hash)

expected_hashes = resolution["hashes"]
observed_trees = {
    "k_workspace_sha256": sha256_tree(Path("/reference/k-proof")),
    "k_audit_sha256": sha256_tree(Path("/reference/k-audit")),
    "klean_generation_sha256": sha256_tree(
        Path("/reference/klean-generation")
    ),
    "generation_producer_sources_sha256": sha256_tree(
        Path("/reference/generation-tools")
    ),
    "lean_workspace_sha256": sha256_tree(Path("/candidate")),
    "stage1_export_sha256": tree_digest(Path("/reference/k-proof")),
    "generated_tree_sha256": tree_digest(
        Path("/reference/klean-generation/generated")
    ),
    "discovery_manifest_sha256": file_hash(
        Path("/reference/lemma-discovery.json")
    ),
}
for label, observed in observed_trees.items():
    expected = expected_hashes[label]
    assert observed == expected, (label, observed, expected)
    print(label, "OK", observed)

source_root = Path("/reference/k-proof")
recorded_sources = resolution["stage1_source_hashes"]
actual_source_files = sorted(
    p.relative_to(source_root).as_posix()
    for p in source_root.rglob("*")
    if p.is_file()
)
assert sorted(recorded_sources) == actual_source_files
for relative in actual_source_files:
    assert file_hash(source_root / relative) == recorded_sources[relative]
print("stage1 source-file hash bijection: OK", len(actual_source_files))

generation = Path("/reference/klean-generation")
generated = generation / "generated"
input_manifest = load(generation / "input-manifest.json")
generator_manifest = load(generation / "generator-manifest.json")
export_result = load(generation / "export-result.json")
obligation_map = load(generated / "obligation-map.json")
discovery = load(Path("/reference/lemma-discovery.json"))

assert file_hash(generated / "obligation-map.json") == generator_manifest[
    "obligation_map_sha256"
]
assert file_hash(generation / "trust-inventory.json") == export_result[
    "trust_inventory_sha256"
]
assert generator_manifest["generated_tree_sha256"] == observed_trees[
    "generated_tree_sha256"
]
assert input_manifest["frozen_input_sha256"] == observed_trees[
    "stage1_export_sha256"
]
assert export_result["frozen_input_sha256"] == observed_trees[
    "stage1_export_sha256"
]
assert export_result["stage3_discovery_manifest_sha256"] == observed_trees[
    "discovery_manifest_sha256"
]
assert generator_manifest["provenance"]["stage3_discovery_manifest_sha256"] \
    == observed_trees["discovery_manifest_sha256"]
print("sidecar and provenance hashes: OK")

protected_domain = [
    entry
    for entry in discovery["rules"]
    if entry["classification"] == "DOMAIN_LEMMA"
]
domain = input_manifest["source_rules"]
expected_ids = [entry["source_rule_id"] for entry in protected_domain]
assert [entry["source_rule_id"] for entry in domain] == expected_ids
assert expected_ids == [
    "rule-1cad334b6905baf03866113ddd1797f5714a455f71cedf67b42074759ca10ca7",
    "rule-3cb106e69fb9d49b1f6233a47205ceacbe2aee414ced90880b1ceb6cbb0782e5",
]
source_rules = obligation_map["source_rules"]
obligations = obligation_map["obligations"]
assert len(obligations) == len(source_rules) == len(domain) == 2
assert len(set(expected_ids)) == 2
assert [entry["source_rule_id"] for entry in source_rules] == expected_ids
assert [entry["source_rule_id"] for entry in obligations] == expected_ids
for protected, source, obligation in zip(domain, source_rules, obligations):
    for key in (
        "source_rule_id",
        "normalized_sha256",
        "classification",
        "file",
        "module",
        "start_line",
        "end_line",
        "text",
    ):
        if key != "classification":
            assert source[key] == protected[key], (key, source, protected)
    assert source["classification"] == "DOMAIN_LEMMA"
    assert obligation["normalized_sha256"] == protected["normalized_sha256"]
    assert obligation["source_span"] == {
        "start_line": protected["start_line"],
        "end_line": protected["end_line"],
    }
    assert hashlib.sha256(obligation["lean_conjunct"].encode()).hexdigest() \
        == obligation["lean_conjunct_sha256"]
print("source-rule/obligation bijection: OK", expected_ids)

target = target_statement(generated)
assert target is not None
assert target == generator_manifest["target"]
assert target == resolution["target"]
assert target == resolution["stage4_preflight"]["target"]
assert generator_manifest["obligation_count"] == len(obligations)
assert export_result["obligation_count"] == len(obligations)
assert export_result["status"] == "OK"
assert resolution["stage4_preflight"]["status"] == "PASS"

lemma_text = (generated / target["file"]).read_text()
assert len(re.findall(r"(?m)^def targetStatement\b", lemma_text)) == 1
for obligation in obligations:
    assert obligation["lean_conjunct"] in lemma_text
assert lemma_text.count("\n    ∧ ") == 1
assert lemma_text.count("↔ (True)") == 2
assert len(target["parameters"]) == 8
assert target["parameters"] == obligation_map["trust_parameters"]
print("fixed generated target identity: OK")
print(json.dumps(target, indent=2, sort_keys=True))
