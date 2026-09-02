#!/usr/bin/env python3
"""Strict ordered/bijective comparison of reconstructed and recorded rules."""

from __future__ import annotations

import json
from pathlib import Path
import sys

sys.path.insert(0, "/reference")
from tools.k_rule_inventory import canonical_json_sha256, inventory_verification  # noqa: E402
from tools.lemma_discovery_contract import validate_trust_boundary  # noqa: E402


def require(condition: bool, message: str) -> None:
    print(("PASS " if condition else "FAIL ") + message)
    if not condition:
        raise SystemExit(1)


workspace = Path("/reference/k-proof")
inventory = inventory_verification(workspace)
discovery = json.loads(Path("/reference/lemma-discovery.json").read_text())
validated = validate_trust_boundary(workspace, Path("/reference/lemma-discovery.json"))
stage4_input = json.loads(Path("/reference/klean-generation/input-manifest.json").read_text())

rules = inventory["rules"]
entries = discovery["rules"]
canonical_ids = [rule["source_rule_id"] for rule in rules]
classified_ids = [entry["source_rule_id"] for entry in entries]

require(inventory["inventory_sha256"] == canonical_json_sha256(rules), "whole inventory hash recomputes from ordered full records")
require(discovery["inventory_sha256"] == inventory["inventory_sha256"], "protected inventory hash matches reconstruction")
require(len(classified_ids) == len(set(classified_ids)), "protected classifications contain no duplicate identities")
require(classified_ids == canonical_ids, "protected identities are exact, complete, and in canonical source order")
require(len(entries) == len(rules), "no omitted or extra classified rules")

for index, (rule, entry) in enumerate(zip(rules, entries, strict=True)):
    normalized = " ".join(rule["text"].split())
    import hashlib
    digest = hashlib.sha256(normalized.encode()).hexdigest()
    require(rule["normalized_sha256"] == digest, f"rule {index} normalized source hash")
    require(rule["source_rule_id"] == "rule-" + digest, f"rule {index} source_rule_id")
    source_lines = Path("/reference/k-proof/verification.k").read_text().splitlines()
    exact_span = "\n".join(source_lines[rule["start_line"] - 1 : rule["end_line"]])
    require(rule["text"] == exact_span, f"rule {index} exact source span {rule['start_line']}-{rule['end_line']}")
    require(entry["source_rule_id"] == rule["source_rule_id"], f"rule {index} protected identity")

require(stage4_input["inventory_sha256"] == inventory["inventory_sha256"], "Stage 4 input inventory hash")
require(stage4_input["verification_sha256"] == inventory["verification_sha256"], "Stage 4 input verification.k hash")
require(stage4_input["verification_module"] == inventory["verification_module"], "Stage 4 input verification module")

class_to_key = {
    "DEFINITION": "definitions",
    "OPERATIONAL_RULE": "operational_rules",
    "PROVED_DERIVED_LEMMA": "proved_derived_lemmas",
    "DOMAIN_LEMMA": "source_rules",
}
expected_groups = {key: [] for key in class_to_key.values()}
by_id = {entry["source_rule_id"]: entry for entry in entries}
for rule in rules:
    entry = by_id[rule["source_rule_id"]]
    expected_groups[class_to_key[entry["classification"]]].append({**rule, **entry})
for key, expected in expected_groups.items():
    require(stage4_input[key] == expected, f"Stage 4 {key} exact ordered classified records")

require(validated["rules"] == rules, "trusted Stage 3 boundary returns exact canonical rule list")
require(validated["inventory_sha256"] == inventory["inventory_sha256"], "trusted Stage 3 boundary inventory identity")
print(f"RECONSTRUCTED_RULE_COUNT={len(rules)}")
print(f"INVENTORY_SHA256={inventory['inventory_sha256']}")
print("STRICT_INVENTORY_BIJECTION_PASS")
