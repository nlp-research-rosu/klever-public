#!/usr/bin/env python3
"""Check the empty-domain Stage 3 result against every Stage 4 binding."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from tools import klean_export
from tools.lemma_discovery_contract import validate_trust_boundary


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


# Independently established by source/semantics review:
# both canonical rules define named structural proof terms.
independent_domain_ids: list[str] = []

validated = validate_trust_boundary(
    Path("/reference/k-proof"),
    Path("/reference/lemma-discovery.json"),
)
input_manifest = load_json(
    Path("/reference/klean-generation/input-manifest.json")
)
generator_manifest = load_json(
    Path("/reference/klean-generation/generator-manifest.json")
)
export_result = load_json(
    Path("/reference/klean-generation/export-result.json")
)
preflight = load_json(Path("/reference/klean-generation/preflight.json"))
obligation_map = load_json(
    Path("/reference/klean-generation/generated/obligation-map.json")
)
audit_input = load_json(Path("/audit-input.json"))

stage3_domain_ids = [
    rule["source_rule_id"] for rule in validated["domain_lemmas"]
]
input_source_ids = [
    rule["source_rule_id"] for rule in input_manifest["source_rules"]
]
mapped_source_ids = [
    rule["source_rule_id"] for rule in obligation_map["source_rules"]
]
obligation_ids = [
    obligation["source_rule_id"]
    for obligation in obligation_map["obligations"]
]

for name, observed in (
    ("independent_to_stage3_domain_ids", stage3_domain_ids),
    ("independent_to_input_manifest_source_ids", input_source_ids),
    ("independent_to_obligation_map_source_ids", mapped_source_ids),
    ("independent_to_obligation_ids", obligation_ids),
):
    check(name, observed, independent_domain_ids)

check(
    "obligation_ids_unique",
    len(obligation_ids),
    len(set(obligation_ids)),
)
check(
    "obligation_order_bijection",
    obligation_ids,
    mapped_source_ids,
)
check(
    "trust_parameters",
    obligation_map["trust_parameters"],
    [],
)
for name, observed in (
    ("generator_manifest.obligation_count", generator_manifest[
        "obligation_count"
    ]),
    ("export_result.obligation_count", export_result["obligation_count"]),
    ("preflight.obligation_count", preflight["obligation_count"]),
    (
        "audit_input.stage4_preflight.obligation_count",
        audit_input["resolution"]["stage4_preflight"]["obligation_count"],
    ),
):
    check(name, observed, 0)

check("export_result.status", export_result["status"], "KLEAN_NO_OBLIGATIONS")
check("preflight.status", preflight["status"], "KLEAN_NO_OBLIGATIONS")
check(
    "audit_input.selection.status",
    audit_input["resolution"]["selections"]["klean_generation"]["status"],
    "KLEAN_NO_OBLIGATIONS",
)

expected_definition = klean_export.expected_target_definition(obligation_map)
observed_target = klean_export.target_statement(
    Path("/reference/klean-generation/generated")
)
check("expected_target_definition", expected_definition, None)
check("mechanically_observed_target", observed_target, None)
check("generator_manifest.target", generator_manifest["target"], None)
check("preflight.target", preflight["target"], None)
check("audit_input.target", audit_input["resolution"]["target"], None)
check(
    "candidate_absent",
    Path("/candidate").exists(),
    False,
)

result = {
    "status": "PASS" if not failures else "FAIL",
    "failure_count": len(failures),
    "failures": failures,
    "independent_classification": {
        "definition_ids": [
            "rule-07b2e76171363735048d516894c0106df978020141671339aaa271a5d5e0d8e7",
            "rule-5e130f83335a10b2992b3283bceb5cbf4e9d208c0b150ab3918d09173e3f7ad7",
        ],
        "operational_rule_ids": [],
        "proved_derived_lemma_ids": [],
        "domain_lemma_ids": independent_domain_ids,
    },
    "checks": checks,
}
print(json.dumps(result, indent=2, sort_keys=True))
raise SystemExit(0 if not failures else 1)
