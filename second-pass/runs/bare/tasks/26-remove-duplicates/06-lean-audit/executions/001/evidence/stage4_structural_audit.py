#!/usr/bin/env python3
"""Independent Stage 3-to-Stage 4 mapping and no-target audit."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

from tools import (
    k_rule_inventory,
    klean_export,
    lemma_discovery_contract,
)


WORKSPACE = Path("/reference/k-proof")
DISCOVERY = Path("/reference/lemma-discovery.json")
GENERATION = Path("/reference/klean-generation")
GENERATED = GENERATION / "generated"

INDEPENDENT_CLASSIFICATIONS = {
    "rule-eead64180cce1cdc54b47266673a3b5fdf72418beb97f8d7bc07df03affe9237":
        "DEFINITION",
    "rule-4b2e81eee048157b7718fb38321ccd6a0df2d72177e63dbc46d4d028c48dffff":
        "DEFINITION",
    "rule-21d0f4e4939c7bf24a8212763a583e9e9f1d7cc35fcef917a31103579967b976":
        "DEFINITION",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")
    print(f"MATCH: {message}")


def load(path: Path) -> dict:
    return json.loads(path.read_bytes())


inventory = k_rule_inventory.inventory_verification(WORKSPACE)
discovery = load(DISCOVERY)
validated = lemma_discovery_contract.validate_trust_boundary(
    WORKSPACE, DISCOVERY
)
input_manifest = load(GENERATION / "input-manifest.json")
generator_manifest = load(GENERATION / "generator-manifest.json")
export_result = load(GENERATION / "export-result.json")
recorded_preflight = load(GENERATION / "preflight.json")
obligation_map_path = GENERATED / "obligation-map.json"
obligation_map = load(obligation_map_path)

observed_classifications = {
    entry["source_rule_id"]: entry["classification"]
    for entry in discovery["rules"]
}
require(
    observed_classifications == INDEPENDENT_CLASSIFICATIONS,
    "Stage 3 categories exactly equal the independent per-rule categories",
)
require(
    [rule["source_rule_id"] for rule in inventory["rules"]]
    == list(INDEPENDENT_CLASSIFICATIONS),
    "independent categories cover the exact ordered inventory",
)
require(
    not validated["domain_lemmas"],
    "independently confirmed DOMAIN_LEMMA set is empty",
)
require(
    input_manifest["definitions"] == validated["definitions"],
    "Stage 4 input carries every classified definition exactly",
)
require(
    input_manifest["operational_rules"] == validated["operational_rules"] == [],
    "Stage 4 input has no operational-rule classifications",
)
require(
    input_manifest["proved_derived_lemmas"]
    == validated["proved_derived_lemmas"]
    == [],
    "Stage 4 input has no proved-derived-lemma classifications",
)
require(
    input_manifest["source_rules"] == validated["domain_lemmas"] == [],
    "eligible source-rule set is exactly the empty true domain set",
)

source_rule_ids = [
    item["source_rule_id"] for item in obligation_map["source_rules"]
]
obligation_ids = [
    item["source_rule_id"] for item in obligation_map["obligations"]
]
require(
    source_rule_ids == obligation_ids == [],
    "source-rule/obligation ID bijection is exact and empty",
)
require(
    len(source_rule_ids) == len(set(source_rule_ids))
    and len(obligation_ids) == len(set(obligation_ids)),
    "source-rule and obligation identities have no duplicates",
)
require(
    obligation_map["trust_parameters"] == [],
    "zero obligations have zero target trust parameters",
)
require(
    generator_manifest["obligation_count"]
    == export_result["obligation_count"]
    == recorded_preflight["obligation_count"]
    == len(obligation_ids)
    == 0,
    "all obligation counts are exactly zero",
)
require(
    hashlib.sha256(obligation_map_path.read_bytes()).hexdigest()
    == generator_manifest["obligation_map_sha256"],
    "obligation-map byte hash matches the generator manifest",
)

expected_definition = klean_export.expected_target_definition(obligation_map)
observed_target = klean_export.target_statement(GENERATED)
raw_target_count = 0
for path in sorted(GENERATED.rglob("*.lean")):
    raw_target_count += len(
        re.findall(r"(?m)^\s*def\s+targetStatement\b", path.read_text())
    )
require(expected_definition is None, "empty obligations imply no target definition")
require(observed_target is None, "trusted target parser finds no generated target")
require(raw_target_count == 0, "raw Lean sources contain no targetStatement")
require(
    generator_manifest["target"]
    == recorded_preflight["target"]
    == observed_target
    is None,
    "generator, preflight, and source agree on a null fixed target",
)
require(
    export_result["status"]
    == recorded_preflight["status"]
    == "KLEAN_NO_OBLIGATIONS",
    "Stage 4 status exactly matches the empty obligation set",
)
require(
    not Path("/candidate").exists(),
    "classification-only no-obligation run has no Stage 5 candidate",
)

print()
print("PASS: exact empty bijection, no obligation conjuncts, and no target exist")
