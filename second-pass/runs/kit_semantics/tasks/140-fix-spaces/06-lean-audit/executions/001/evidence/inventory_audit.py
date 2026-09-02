#!/usr/bin/env python3
"""Reconstruct the canonical verification-module rule inventory and compare it."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from tools import k_rule_inventory


workspace = Path("/reference/k-proof")
discovery = json.loads(Path("/reference/lemma-discovery.json").read_text())
stage4_input = json.loads(
    Path("/reference/klean-generation/input-manifest.json").read_text()
)
inventory = k_rule_inventory.inventory_verification(workspace)

print("CANONICAL INVENTORY")
print(json.dumps(inventory, indent=2, sort_keys=True))

checks: list[dict[str, object]] = []


def check(label: str, condition: bool, detail: object = None) -> None:
    entry = {"label": label, "pass": condition}
    if detail is not None:
        entry["detail"] = detail
    checks.append(entry)
    print(json.dumps(entry, sort_keys=True))


rules = inventory["rules"]
discovery_rules = discovery.get("rules", [])
ids = [entry["source_rule_id"] for entry in rules]
discovery_ids = [entry.get("source_rule_id") for entry in discovery_rules]
check("verification module", inventory["verification_module"] == "VERIFICATION", inventory["verification_module"])
check("local verification-module closure", inventory["verification_modules"] == ["VERIFICATION"], inventory["verification_modules"])
check("verification.k SHA-256 matches Stage 4 input", inventory["verification_sha256"] == stage4_input.get("verification_sha256"), inventory["verification_sha256"])
check("inventory hash matches discovery", inventory["inventory_sha256"] == discovery.get("inventory_sha256"), inventory["inventory_sha256"])
check("inventory hash matches Stage 4 input", inventory["inventory_sha256"] == stage4_input.get("inventory_sha256"), inventory["inventory_sha256"])
check("ordered identity bijection", ids == discovery_ids, {"inventory": ids, "discovery": discovery_ids})
check("no reconstructed duplicate IDs", len(ids) == len(set(ids)), len(ids))
check("no discovery duplicate IDs", len(discovery_ids) == len(set(discovery_ids)), len(discovery_ids))
check("every inventory entry classified exactly once", len(rules) == len(discovery_rules), {"inventory": len(rules), "discovery": len(discovery_rules)})

source_lines = (workspace / "verification.k").read_text().splitlines()
for position, rule in enumerate(rules):
    normalized = " ".join(rule["text"].split())
    digest = hashlib.sha256(normalized.encode()).hexdigest()
    span = "\n".join(source_lines[rule["start_line"] - 1 : rule["end_line"]])
    check(f"rule {position + 1} normalized hash", digest == rule["normalized_sha256"], rule["source_rule_id"])
    check(f"rule {position + 1} source_rule_id", rule["source_rule_id"] == "rule-" + digest, rule["source_rule_id"])
    check(f"rule {position + 1} exact source span", span == rule["text"], {"start": rule["start_line"], "end": rule["end_line"]})

# The deterministic input manifest must contain each reconstructed definition
# with the discovery classification/rationale added, in the same order.
expected_definitions = []
for rule, classified in zip(rules, discovery_rules, strict=True):
    document = dict(rule)
    document["classification"] = classified["classification"]
    document["rationale"] = classified["rationale"]
    expected_definitions.append(document)
check("Stage 4 definition documents exactly match classified inventory", stage4_input.get("definitions") == expected_definitions)

classified_stage4 = []
for key in ("definitions", "operational_rules", "source_rules", "proved_derived_lemmas"):
    for entry in stage4_input.get(key, []):
        classified_stage4.append((entry["source_rule_id"], entry["classification"], key))
check("Stage 4 accounts for every classified rule once", [item[0] for item in classified_stage4] == ids and len({item[0] for item in classified_stage4}) == len(ids), classified_stage4)

failures = [entry["label"] for entry in checks if not entry["pass"]]
print(json.dumps({"SUMMARY": {"check_count": len(checks), "failures": failures, "status": "PASS" if not failures else "FAIL"}}, sort_keys=True))
raise SystemExit(0 if not failures else 1)
