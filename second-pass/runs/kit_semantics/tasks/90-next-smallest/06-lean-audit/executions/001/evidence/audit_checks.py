#!/usr/bin/env python3
"""Independent structural checks for the Stage 3/4 audit.

This script is audit-authored.  It parses JSON and source text only, and uses
the trusted inventory/hash/target helpers mounted below /reference/tools.
"""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path

from tools.k_rule_inventory import canonical_json_sha256, inventory_verification
from tools.klean_export import (
    expected_target_definition,
    sha256_text,
    target_statement,
    tree_digest,
)
from tools.pipeline_contract import sha256_tree


STAGE1 = Path("/reference/k-proof")
DISCOVERY = Path("/reference/lemma-discovery.json")
GENERATION = Path("/reference/klean-generation")
GENERATED = GENERATION / "generated"
PRODUCERS = Path("/reference/generation-tools")
AUDIT_INPUT = Path("/audit-input.json")


def load(path: Path):
    return json.loads(path.read_text())


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


inventory = inventory_verification(STAGE1)
discovery = load(DISCOVERY)
verification_lines = (STAGE1 / "verification.k").read_text().splitlines()

print("== Stage 3 canonical inventory ==")
print("verification_module:", inventory["verification_module"])
print("verification_modules:", inventory["verification_modules"])
print("rule_count:", len(inventory["rules"]))
print("inventory_sha256:", inventory["inventory_sha256"])
require(
    inventory["inventory_sha256"] == canonical_json_sha256(inventory["rules"]),
    "whole-inventory digest is not canonical digest of reconstructed rules",
)
require(
    inventory["verification_sha256"] == file_sha256(STAGE1 / "verification.k"),
    "verification.k digest mismatch",
)

ids = []
for index, rule in enumerate(inventory["rules"], 1):
    start = rule["start_line"]
    end = rule["end_line"]
    extracted = "\n".join(verification_lines[start - 1 : end])
    normalized = " ".join(extracted.split())
    digest = hashlib.sha256(normalized.encode()).hexdigest()
    require(extracted == rule["text"], f"rule {index} source span/text mismatch")
    require(digest == rule["normalized_sha256"], f"rule {index} normalized hash mismatch")
    require(rule["source_rule_id"] == "rule-" + digest, f"rule {index} ID mismatch")
    ids.append(rule["source_rule_id"])
    print(
        f"{index:02d} lines {start:03d}-{end:03d} "
        f"{rule['source_rule_id']} attrs={rule['attributes']}"
    )
require(len(ids) == len(set(ids)), "canonical inventory contains duplicate rule IDs")

print("\n== Stage 3 manifest bijection and order ==")
manifest_ids = [entry["source_rule_id"] for entry in discovery["rules"]]
require(len(manifest_ids) == len(set(manifest_ids)), "manifest duplicates rule IDs")
require(manifest_ids == ids, "manifest rule identities are omitted, extra, or reordered")
require(
    discovery["inventory_sha256"] == inventory["inventory_sha256"],
    "manifest whole-inventory hash mismatch",
)
classification_by_id = {
    entry["source_rule_id"]: entry["classification"] for entry in discovery["rules"]
}
for rule in inventory["rules"]:
    if any(attribute == "simplification" or attribute.startswith("simplification(")
           for attribute in rule["attributes"]):
        require(
            classification_by_id[rule["source_rule_id"]]
            in {"DEFINITION", "DOMAIN_LEMMA"},
            "simplification rule has forbidden classification",
        )
counts = Counter(entry["classification"] for entry in discovery["rules"])
print("manifest_order_exact: PASS")
print("manifest_identity_bijection: PASS")
print("classification_counts:", dict(sorted(counts.items())))
for index, entry in enumerate(discovery["rules"], 1):
    print(f"{index:02d} {entry['source_rule_id']} {entry['classification']}")

print("\n== Generation producer provenance ==")
source_manifest = load(PRODUCERS / "source-manifest.json")
generator_manifest = load(GENERATION / "generator-manifest.json")
audit = load(AUDIT_INPUT)["resolution"]
exporter_hash = file_sha256(PRODUCERS / "klean_export.py")
klean_hash = file_sha256(PRODUCERS / "klean.py")
image_id = source_manifest["generator_image_id"]
expected_files = {
    "klean.py": klean_hash,
    "klean_export.py": exporter_hash,
}
require(source_manifest["files"] == expected_files, "source manifest file hashes mismatch")
require(generator_manifest["exporter_sha256"] == exporter_hash, "exporter hash mismatch")
require(generator_manifest["klean_py_sha256"] == klean_hash, "klean.py hash mismatch")
require(
    generator_manifest["provenance"]["generator_image_id"] == image_id,
    "generator/source manifest image IDs differ",
)
require(
    Path(audit["generation_producer_sources"]).name == image_id.removeprefix("sha256:"),
    "audit input producer path does not record the same generator image ID",
)
producer_tree = sha256_tree(PRODUCERS)
require(
    audit["hashes"]["generation_producer_sources_sha256"] == producer_tree,
    "audit input producer tree hash mismatch",
)
print("klean_export.py_sha256:", exporter_hash)
print("klean.py_sha256:", klean_hash)
print("generator_image_id:", image_id)
print("pipeline_tree_sha256:", producer_tree)
print("producer_provenance: PASS")

print("\n== Stage 4 sidecars and source/obligation bijection ==")
input_manifest = load(GENERATION / "input-manifest.json")
obligation_map = load(GENERATED / "obligation-map.json")
export_result = load(GENERATION / "export-result.json")
domain_rules = [
    {**rule, "classification": classification_by_id[rule["source_rule_id"]]}
    for rule in inventory["rules"]
    if classification_by_id[rule["source_rule_id"]] == "DOMAIN_LEMMA"
]
source_rules = input_manifest["source_rules"]
require(
    [rule["source_rule_id"] for rule in source_rules]
    == [rule["source_rule_id"] for rule in domain_rules],
    "input-manifest source rules differ from independently selected domain rules",
)
require(obligation_map["source_rules"] == source_rules, "obligation-map source rules differ")
obligations = obligation_map["obligations"]
obligation_ids = [obligation["source_rule_id"] for obligation in obligations]
source_ids = [rule["source_rule_id"] for rule in source_rules]
require(len(obligation_ids) == len(set(obligation_ids)), "duplicate obligation IDs")
require(obligation_ids == source_ids, "source-rule/obligation order or bijection mismatch")
require(len(obligations) == len(domain_rules), "obligation/domain-rule count mismatch")
for source_rule, obligation in zip(source_rules, obligations, strict=True):
    require(
        obligation["source_span"]
        == {"start_line": source_rule["start_line"], "end_line": source_rule["end_line"]},
        f"source span mismatch for {source_rule['source_rule_id']}",
    )
    require(
        obligation["normalized_sha256"] == source_rule["normalized_sha256"],
        f"source hash mismatch for {source_rule['source_rule_id']}",
    )
    require(
        obligation["lean_conjunct_sha256"] == sha256_text(obligation["lean_conjunct"]),
        f"Lean conjunct hash mismatch for {source_rule['source_rule_id']}",
    )
    print(source_rule["source_rule_id"])
    print("  conjunct:", obligation["lean_conjunct"])
require(
    generator_manifest["obligation_map_sha256"]
    == file_sha256(GENERATED / "obligation-map.json"),
    "obligation map file hash mismatch",
)
require(
    generator_manifest["obligation_count"] == len(obligations),
    "generator obligation count mismatch",
)
require(
    export_result["obligation_count"] == len(obligations),
    "export-result obligation count mismatch",
)
require(
    input_manifest["inventory_sha256"] == inventory["inventory_sha256"],
    "input manifest inventory hash mismatch",
)
require(
    generator_manifest["provenance"]["inventory_sha256"] == inventory["inventory_sha256"],
    "generator provenance inventory hash mismatch",
)
require(
    input_manifest["verification_sha256"] == file_sha256(STAGE1 / "verification.k"),
    "input manifest verification hash mismatch",
)
require(
    input_manifest["stage3_discovery_manifest_sha256"] == file_sha256(DISCOVERY),
    "input manifest discovery hash mismatch",
)
stage1_tree = tree_digest(STAGE1)
generated_tree = tree_digest(GENERATED)
require(input_manifest["stage1_workspace_sha256"] == stage1_tree, "Stage 1 tree mismatch")
require(generator_manifest["generated_tree_sha256"] == generated_tree, "generated tree mismatch")
require(audit["hashes"]["stage1_export_sha256"] == stage1_tree, "audit Stage 1 export mismatch")
require(audit["hashes"]["generated_tree_sha256"] == generated_tree, "audit generated tree mismatch")

actual_target = target_statement(GENERATED)
expected_definition = expected_target_definition(obligation_map)
require(actual_target == generator_manifest["target"], "generator target mismatch")
require(actual_target == audit["target"], "audit-input target mismatch")
require(
    actual_target["definition_sha256"] == sha256_text(expected_definition),
    "fixed target is not exact generated conjunction",
)
print("domain_rule_count:", len(domain_rules))
print("obligation_count:", len(obligations))
print("stage1_tree_sha256:", stage1_tree)
print("generated_tree_sha256:", generated_tree)
print("target:", json.dumps(actual_target, sort_keys=True))
print("stage4_structural_checks: PASS")
