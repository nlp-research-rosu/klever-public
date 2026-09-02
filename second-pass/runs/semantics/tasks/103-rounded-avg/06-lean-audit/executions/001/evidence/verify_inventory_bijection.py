#!/usr/bin/env python3
"""Explicit ordered/bijective Stage 1-to-Stage 3 inventory reconciliation."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from tools.k_rule_inventory import (
    canonical_json_sha256,
    inventory_verification,
)


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text())
    if not isinstance(value, dict):
        raise AssertionError(f"{path} is not a JSON object")
    return value


checks: dict[str, dict[str, Any]] = {}
failures: list[str] = []


def check(name: str, observed: Any, expected: Any) -> None:
    passed = observed == expected
    checks[name] = {
        "observed": observed,
        "expected": expected,
        "pass": passed,
    }
    if not passed:
        failures.append(name)


inventory = inventory_verification(Path("/reference/k-proof"))
discovery = load_json(Path("/reference/lemma-discovery.json"))
verification_lines = Path(
    "/reference/k-proof/verification.k"
).read_text().splitlines()
rules = inventory["rules"]
entries = discovery["rules"]

inventory_ids = [rule["source_rule_id"] for rule in rules]
discovery_ids = [entry["source_rule_id"] for entry in entries]
check("rule_count", len(rules), 2)
check("manifest_rule_count", len(entries), len(rules))
check("ordered_identities", discovery_ids, inventory_ids)
check("inventory_id_uniqueness", len(set(inventory_ids)), len(inventory_ids))
check("manifest_id_uniqueness", len(set(discovery_ids)), len(discovery_ids))
check("identity_set", sorted(discovery_ids), sorted(inventory_ids))
check(
    "inventory_hash",
    canonical_json_sha256(rules),
    discovery["inventory_sha256"],
)
check(
    "verification_module_closure",
    inventory["verification_modules"],
    ["ROUNDED-AVG-VERIFICATION"],
)

for index, rule in enumerate(rules):
    prefix = f"rule_{index}"
    normalized = " ".join(rule["text"].split())
    normalized_hash = hashlib.sha256(normalized.encode()).hexdigest()
    check(
        f"{prefix}.normalized_sha256",
        normalized_hash,
        rule["normalized_sha256"],
    )
    check(
        f"{prefix}.source_rule_id",
        rule["source_rule_id"],
        "rule-" + normalized_hash,
    )
    source_span = "\n".join(
        verification_lines[rule["start_line"] - 1 : rule["end_line"]]
    )
    check(f"{prefix}.source_span_text", source_span, rule["text"])

classifications = {
    entry["source_rule_id"]: entry["classification"] for entry in entries
}
independent_classifications = {
    "rule-07b2e76171363735048d516894c0106df978020141671339aaa271a5d5e0d8e7":
        "DEFINITION",
    "rule-5e130f83335a10b2992b3283bceb5cbf4e9d208c0b150ab3918d09173e3f7ad7":
        "DEFINITION",
}
check(
    "classification_totality",
    sorted(classifications),
    sorted(inventory_ids),
)
check(
    "independent_classification_agreement",
    classifications,
    independent_classifications,
)
check(
    "simplification_class_policy",
    [
        {
            "source_rule_id": rule["source_rule_id"],
            "classification": classifications[rule["source_rule_id"]],
        }
        for rule in rules
        if "simplification" in rule["attributes"]
        and classifications[rule["source_rule_id"]]
        not in {"DEFINITION", "DOMAIN_LEMMA"}
    ],
    [],
)

result = {
    "status": "PASS" if not failures else "FAIL",
    "failure_count": len(failures),
    "failures": failures,
    "checks": checks,
}
print(json.dumps(result, indent=2, sort_keys=True))
raise SystemExit(0 if not failures else 1)
