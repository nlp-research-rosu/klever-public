#!/usr/bin/env python3
"""Independent structural/hash check for the selected Stage 4 artifacts."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

import sys

sys.path.insert(0, "/reference")
from tools.k_rule_inventory import inventory_verification


K_WORKSPACE = Path("/reference/k-proof")
DISCOVERY = Path("/reference/lemma-discovery.json")
GENERATION = Path("/reference/klean-generation")
GENERATED = GENERATION / "generated"
AUDIT_INPUT = Path("/audit-input.json")

DOMAIN_IDS = [
    "rule-2944c4d3c7bc5a2d260f24ca8fd4234701fa8f82f00db7ca3317fa06458082b5",
    "rule-7749c9857edd14009417bdaa86b5d4b1c229fa0013cc411eaf35ed3a49ed0842",
]
DEFINITION_IDS = [
    "rule-8277b118773512287e2b2b20da4dbf45607f85956623bafa9028b50596471d08",
    "rule-6316a60ea115abdbe8e03d39d302e43ceea73cd9fedd27a98872c76b5b811b42",
    "rule-537b55658be09522e9ef565d2ec69183fd6fbd782b54c8d1b5dd24667acbd3aa",
    "rule-a4eb647db56262adb78bb0c7a909b63ee0acc886d9d451ca5de28976ba45ea55",
    "rule-0fb2ff70d1d771be4491e1d1d3d07c7bb4778cb5ac74c239f4b9ade2421d3d71",
    "rule-db274c9f572feeb0ce3aedc0579c3303eb84577ca9baa4e5034eed5a969803f6",
]


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_text(text: str) -> str:
    return sha256_bytes(text.encode())


def load(path: Path) -> dict:
    return json.loads(path.read_text())


def check(label: str, condition: bool) -> None:
    print(f"{label}: {condition}")
    if not condition:
        raise AssertionError(label)


inventory = inventory_verification(K_WORKSPACE)
discovery = load(DISCOVERY)
input_manifest = load(GENERATION / "input-manifest.json")
generator_manifest = load(GENERATION / "generator-manifest.json")
obligation_map_path = GENERATED / "obligation-map.json"
obligation_map = load(obligation_map_path)
audit_input = load(AUDIT_INPUT)

inventory_ids = [rule["source_rule_id"] for rule in inventory["rules"]]
discovery_ids = [rule["source_rule_id"] for rule in discovery["rules"]]
discovery_by_id = {
    rule["source_rule_id"]: rule for rule in discovery["rules"]
}
inventory_by_id = {
    rule["source_rule_id"]: rule for rule in inventory["rules"]
}

check("inventory/discovery exact order", inventory_ids == discovery_ids)
check("inventory identities unique", len(set(inventory_ids)) == len(inventory_ids))
check("independent domain set is exact", [
    source_rule_id
    for source_rule_id in inventory_ids
    if discovery_by_id[source_rule_id]["classification"] == "DOMAIN_LEMMA"
] == DOMAIN_IDS)
check("independent definition set is exact", [
    source_rule_id
    for source_rule_id in inventory_ids
    if discovery_by_id[source_rule_id]["classification"] == "DEFINITION"
] == DEFINITION_IDS)
check("no operational classifications", not any(
    discovery_by_id[source_rule_id]["classification"] == "OPERATIONAL_RULE"
    for source_rule_id in inventory_ids
))
check("no claimed derived lemmas", not any(
    discovery_by_id[source_rule_id]["classification"] == "PROVED_DERIVED_LEMMA"
    for source_rule_id in inventory_ids
))

expected_source_rules = []
for source_rule_id in DOMAIN_IDS:
    expected_source_rules.append({
        **inventory_by_id[source_rule_id],
        **discovery_by_id[source_rule_id],
        "inventory_sha256": inventory["inventory_sha256"],
        "discovery_manifest_sha256": sha256_bytes(DISCOVERY.read_bytes()),
    })

check("input manifest source-rule identity", input_manifest["source_rules"] == expected_source_rules)
check("obligation map source-rule identity", obligation_map["source_rules"] == expected_source_rules)
check("input manifest definitions", [
    entry["source_rule_id"] for entry in input_manifest["definitions"]
] == DEFINITION_IDS)
check("input manifest operational list empty", input_manifest["operational_rules"] == [])
check("input manifest derived list empty", input_manifest["proved_derived_lemmas"] == [])

obligations = obligation_map["obligations"]
obligation_ids = [obligation["source_rule_id"] for obligation in obligations]
check("obligation IDs exact and ordered", obligation_ids == DOMAIN_IDS)
check("obligation IDs unique", len(set(obligation_ids)) == len(obligation_ids))
for obligation, expected in zip(obligations, expected_source_rules, strict=True):
    check(
        f"{obligation['source_rule_id']} exact source span",
        obligation["source_span"] == {
            "start_line": expected["start_line"],
            "end_line": expected["end_line"],
        },
    )
    check(
        f"{obligation['source_rule_id']} normalized source hash",
        obligation["normalized_sha256"] == expected["normalized_sha256"],
    )
    check(
        f"{obligation['source_rule_id']} inventory hash",
        obligation["inventory_sha256"] == inventory["inventory_sha256"],
    )
    check(
        f"{obligation['source_rule_id']} discovery hash",
        obligation["discovery_manifest_sha256"] == sha256_bytes(DISCOVERY.read_bytes()),
    )
    check(
        f"{obligation['source_rule_id']} conjunct hash",
        obligation["lean_conjunct_sha256"] == sha256_text(obligation["lean_conjunct"]),
    )
    print(f"{obligation['source_rule_id']} conjunct:\n{obligation['lean_conjunct']}")

first = obligations[0]["lean_conjunct"]
second = obligations[1]["lean_conjunct"]
check("addition obligation retains guard", "h : (isInt " in first and ") = true" in first)
check("addition obligation retains dispatch", "applyBin" in first and '"+"' in first)
check("addition obligation retains result", "«_+Int_» I" in first and "«project:Int»" in first)
check("min obligation retains guard", "h : (isInt " in second and ") = true" in second)
check("min obligation retains dispatch", "applyBuiltin" in second and '"min"' in second)
check("min obligation retains both arguments", " V " in second and "inj_SortInt I" in second)
check("min obligation retains result", "«minInt(" in second and "«project:Int»" in second)

check(
    "obligation map file hash",
    generator_manifest["obligation_map_sha256"] == sha256_bytes(obligation_map_path.read_bytes()),
)
check("generator obligation count", generator_manifest["obligation_count"] == len(obligations))

lemma_path = GENERATED / generator_manifest["target"]["file"]
lemma_text = lemma_path.read_text()
matches = list(re.finditer(
    r"(?ms)^\s*def\s+targetStatement\b.*?(?=^\s*end\s+\S+\s*$)",
    lemma_text,
))
check("one generated target declaration", len(matches) == 1)
definition = matches[0].group(0).strip()

expected_lines = ["def targetStatement"]
for parameter in obligation_map["trust_parameters"]:
    expected_lines.append(f"    ({parameter['name']} : {parameter['type']})")
expected_lines.extend((
    "    : Prop :=",
    "    " + "\n    ∧ ".join(
        f"({obligation['lean_conjunct']})" for obligation in obligations
    ),
))
expected_definition = "\n".join(expected_lines)
check("target is exact conjunction", definition == expected_definition)
check("target has exactly one conjunction", definition.count("\n    ∧ ") == 1)
check("target definition hash", sha256_text(definition) == generator_manifest["target"]["definition_sha256"])

declaration = "Klean114Minsubarraysum.Lemmas.targetStatement"
statement = " ".join(
    [declaration] + [parameter["name"] for parameter in obligation_map["trust_parameters"]]
)
check("target declaration", generator_manifest["target"]["declaration"] == declaration)
check("target statement", generator_manifest["target"]["statement"] == statement)
check("target statement hash", generator_manifest["target"]["statement_sha256"] == sha256_text(statement))
check("target parameters", generator_manifest["target"]["parameters"] == obligation_map["trust_parameters"])
for parameter in obligation_map["trust_parameters"]:
    binding = {
        "kore_symbol": parameter["kore_symbol"],
        "name": parameter["name"],
        "source_rule_ids": parameter["source_rule_ids"],
        "type": parameter["type"],
    }
    check(
        f"{parameter['name']} binding hash",
        parameter["binding_sha256"]
        == sha256_text(json.dumps(binding, sort_keys=True, separators=(",", ":"))),
    )
    check(
        f"{parameter['name']} only binds domain obligations",
        bool(parameter["source_rule_ids"])
        and set(parameter["source_rule_ids"]) <= set(DOMAIN_IDS),
    )
check("launcher target identity", audit_input["resolution"]["target"] == generator_manifest["target"])

print("INDEPENDENT_STAGE4_CHECK=PASS")
