#!/usr/bin/env python3
"""Independently verify the empty source-rule/obligation/target bijection."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any

from tools import klean_export, lemma_discovery_contract


WORKSPACE = Path("/reference/k-proof")
DISCOVERY = Path("/reference/lemma-discovery.json")
GENERATION = Path("/reference/klean-generation")
GENERATED = GENERATION / "generated"
CLASSIFICATION = Path(
    "/audit-output/evidence/independent-classification.json"
)


def main() -> int:
    validated = lemma_discovery_contract.validate_trust_boundary(
        WORKSPACE, DISCOVERY
    )
    discovery_hash = hashlib.sha256(DISCOVERY.read_bytes()).hexdigest()
    source_rules = klean_export._domain_source_rules(
        validated, discovery_hash
    )
    obligation_map = json.loads(
        (GENERATED / "obligation-map.json").read_text()
    )
    input_manifest = json.loads(
        (GENERATION / "input-manifest.json").read_text()
    )
    generator_manifest = json.loads(
        (GENERATION / "generator-manifest.json").read_text()
    )
    export_result = json.loads(
        (GENERATION / "export-result.json").read_text()
    )
    audit_input = json.loads(Path("/audit-input.json").read_text())
    independent = json.loads(CLASSIFICATION.read_text())
    independent_domain_ids = [
        rule["source_rule_id"]
        for rule in independent["rules"]
        if rule["classification"] == "DOMAIN_LEMMA"
    ]
    obligations = obligation_map["obligations"]
    generated_target = klean_export.target_statement(GENERATED)
    expected_target_definition = klean_export.expected_target_definition(
        obligation_map
    )
    lean_files = sorted(GENERATED.rglob("*.lean"))
    lean_text = "\n".join(path.read_text() for path in lean_files)

    checks: dict[str, dict[str, Any]] = {}

    def check(name: str, observed: Any, expected: Any) -> None:
        checks[name] = {
            "observed": observed,
            "expected": expected,
            "match": observed == expected,
        }

    source_ids = [rule["source_rule_id"] for rule in source_rules]
    mapped_source_ids = [
        rule["source_rule_id"] for rule in obligation_map["source_rules"]
    ]
    obligation_ids = [
        obligation["source_rule_id"] for obligation in obligations
    ]
    check("independent_domain_rule_ids", independent_domain_ids, [])
    check("validated_domain_rule_ids", source_ids, independent_domain_ids)
    check("input_manifest.source_rules", input_manifest["source_rules"], source_rules)
    check("obligation_map.source_rules", obligation_map["source_rules"], source_rules)
    check("ordered_source_rule_ids", mapped_source_ids, source_ids)
    check("ordered_obligation_ids", obligation_ids, source_ids)
    check(
        "unique_obligation_ids",
        len(obligation_ids),
        len(set(obligation_ids)),
    )
    check("obligation_count", len(obligations), 0)
    check(
        "generator.obligation_count",
        generator_manifest["obligation_count"],
        len(obligations),
    )
    check(
        "export_result.obligation_count",
        export_result["obligation_count"],
        len(obligations),
    )
    check("trust_parameters", obligation_map["trust_parameters"], [])
    check("expected_target_definition", expected_target_definition, None)
    check("generated_target", generated_target, None)
    check("generator.target", generator_manifest["target"], None)
    check("audit_input.target", audit_input["resolution"]["target"], None)
    check("export_result.status", export_result["status"], "KLEAN_NO_OBLIGATIONS")
    check(
        "selected_stage4_status",
        audit_input["resolution"]["selections"]["klean_generation"]["status"],
        "KLEAN_NO_OBLIGATIONS",
    )
    check(
        "generated_target_declaration_absent",
        bool(
            re.search(
                r"(?m)^\s*(?:def|theorem)\s+GeneratedTarget\b",
                lean_text,
            )
        ),
        False,
    )
    check("candidate_absent", Path("/candidate").exists(), False)
    check(
        "no_vacuous_or_empty_conjuncts",
        [
            obligation.get("source_rule_id")
            for obligation in obligations
            if not isinstance(obligation.get("lean_conjunct"), str)
            or not obligation["lean_conjunct"].strip()
            or obligation["lean_conjunct"].strip() in {"True", "(True)"}
        ],
        [],
    )

    failures = [name for name, item in checks.items() if not item["match"]]
    print(
        json.dumps(
            {
                "schema_version": 1,
                "source_rules": source_rules,
                "obligations": obligations,
                "lean_files": [
                    path.relative_to(GENERATED).as_posix()
                    for path in lean_files
                ],
                "checks": checks,
                "failure_count": len(failures),
                "failures": failures,
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
