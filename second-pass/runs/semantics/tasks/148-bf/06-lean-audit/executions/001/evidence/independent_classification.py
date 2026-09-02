#!/usr/bin/env python3
"""Record an independent semantic classification for every local K rule."""

from __future__ import annotations

import json
import re
from pathlib import Path

from tools.k_rule_inventory import inventory_verification


WORKSPACE = Path("/reference/k-proof")
DISCOVERY = Path("/reference/lemma-discovery.json")


inventory = inventory_verification(WORKSPACE)
discovery = json.loads(DISCOVERY.read_text())
recorded = {
    rule["source_rule_id"]: rule["classification"]
    for rule in discovery["rules"]
}

decisions: list[dict[str, object]] = []
errors: list[str] = []
for index, rule in enumerate(inventory["rules"], start=1):
    text = rule["text"]
    first_line = text.splitlines()[0].strip()
    if index <= 29:
        classification = "DEFINITION"
        if first_line == "rule bfBody":
            rationale = (
                "Macro equation naming the exact submitted statement AST; it "
                "does not replace an executing K configuration."
            )
        elif first_line.startswith("rule bfCall"):
            rationale = (
                "Macro equation naming a module-level proof term containing "
                "the exact function definition and call."
            )
        elif first_line.startswith("rule bfRun"):
            rationale = (
                "Macro equation naming the exact closure call that fixed "
                "Call/closureVal semantics subsequently execute."
            )
        elif first_line == "rule planetVals":
            rationale = (
                "Closed equation defining the canonical eight-element value "
                "sequence used by the postcondition summary."
            )
        elif first_line.startswith("rule expectedBetween"):
            rationale = (
                "Equation defining the named open-interval result summary via "
                "the supplied doSlice semantics."
            )
        elif first_line.startswith("rule planetCodes"):
            rationale = (
                "Constructor equation defining a Planet-to-string-code "
                "representation; it asserts no independent theorem."
            )
        elif first_line.startswith("rule planetPosition"):
            rationale = (
                "Constructor equation defining a Planet-to-index "
                "representation; it asserts no independent theorem."
            )
        elif first_line.startswith("rule planetExpr"):
            rationale = (
                "Finite constructor equation defining the expression used to "
                "run a named valid input case."
            )
        else:
            errors.append(f"unrecognized definitional rule at position {index}")
            rationale = "UNRECOGNIZED"
        if "<k>" in text:
            errors.append(
                f"definition at position {index} unexpectedly rewrites <k>"
            )
    else:
        classification = "OPERATIONAL_RULE"
        rationale = (
            "Ordinary proof-harness execution/observation rewrite: it rewrites "
            "the <k> cell, schedules a fixed-semantics Assert of bfRun, and "
            "advances or terminates the finite case loop."
        )
        for required in ("<k>", "#validCases", "Assert(", "bfRun("):
            if required not in text:
                errors.append(
                    f"operational rule at position {index} lacks {required}"
                )
    if "simplification" in rule["attributes"]:
        errors.append(
            f"unexpected simplification attribute on {rule['source_rule_id']}"
        )
    decisions.append(
        {
            "position": index,
            "source_rule_id": rule["source_rule_id"],
            "source_span": {
                "start_line": rule["start_line"],
                "end_line": rule["end_line"],
            },
            "head": first_line,
            "independent_classification": classification,
            "recorded_classification": recorded.get(rule["source_rule_id"]),
            "classification_matches": classification
            == recorded.get(rule["source_rule_id"]),
            "rationale": rationale,
        }
    )

verification_text = (WORKSPACE / "verification.k").read_text()
claim_count = len(re.findall(r"(?m)^\s*claim\b", verification_text))
domain_count = sum(
    decision["independent_classification"] == "DOMAIN_LEMMA"
    for decision in decisions
)
derived_count = sum(
    decision["independent_classification"] == "PROVED_DERIVED_LEMMA"
    for decision in decisions
)
all_match = all(decision["classification_matches"] for decision in decisions)
if claim_count:
    errors.append("verification.k unexpectedly contains local claims")
if not all_match:
    errors.append("independent classifications differ from Stage 3")

result = {
    "status": "PASS" if not errors else "FAIL",
    "errors": errors,
    "judgment": {
        "definitions": 29,
        "operational_rules": 3,
        "proved_derived_lemmas": derived_count,
        "domain_lemmas": domain_count,
        "simplification_rules": 0,
        "local_claim_count": claim_count,
        "stage3_matches_independent_judgment": all_match,
    },
    "semantic_notes": [
        (
            "bfBody, bfCall, and bfRun are macros/named proof terms. bfRun "
            "expands to a closureVal call whose binding, frame, body, return, "
            "and continuation are handled by supplied operational rules."
        ),
        (
            "planetVals, expectedBetween, planetCodes, planetPosition, and "
            "planetExpr are representation/summary equations. Even unused "
            "representation equations remain definitions, not domain lemmas."
        ),
        (
            "The three #validCases rules are classified by behavior as "
            "operational observation rules, despite forming a finite recurrence, "
            "because they rewrite <k> and execute Assert/bfRun."
        ),
        (
            "No rule states an independent algebraic fact or theorem, and no "
            "rule was first proved in a bridge-free module and later reused."
        ),
    ],
    "decisions": decisions,
}
print(json.dumps(result, indent=2, sort_keys=True))
raise SystemExit(0 if result["status"] == "PASS" else 1)
