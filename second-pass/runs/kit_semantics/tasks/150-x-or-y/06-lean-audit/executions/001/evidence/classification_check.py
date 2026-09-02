#!/usr/bin/env python3
"""Independent semantic checks supporting the five-rule classification."""

from __future__ import annotations

import json
from pathlib import Path

from tools.k_rule_inventory import inventory_verification


workspace = Path("/reference/k-proof")
inventory = inventory_verification(workspace)
protected = json.loads(Path("/reference/lemma-discovery.json").read_text())
protected_by_id = {
    entry["source_rule_id"]: entry for entry in protected["rules"]
}


def py_mod(n: int, i: int) -> int:
    return ((n % i) + i) % i


def trial_choice(n: int, i: int, result: object, y: object) -> object:
    if i >= n and i >= 2:
        return result
    if i >= 2 and i < n and py_mod(n, i) == 0:
        return trial_choice(n, i + 1, y, y)
    if i >= 2 and i < n and py_mod(n, i) != 0:
        return trial_choice(n, i + 1, result, y)
    raise ValueError("outside the declared trialChoice domain")


def summary(n: int, x: object, y: object) -> object:
    if n < 2:
        return y
    return trial_choice(n, 2, x, y)


def frozen_operational_body(n: int, x: object, y: object) -> object:
    if n < 2:
        return y
    i = 2
    result = x
    while i < n:
        if n % i == 0:
            result = y
        i = i + 1
    return result


def counterfactual_body(n: int, x: object, y: object) -> object:
    """Flip the divisor test to demonstrate source-body sensitivity."""
    if n < 2:
        return y
    i = 2
    result = x
    while i < n:
        if n % i != 0:
            result = y
        i = i + 1
    return result


independent = {
    inventory["rules"][0]["source_rule_id"]: {
        "classification": "DEFINITION",
        "judgment": (
            "Guarded base equation of the named trialChoice recurrence; "
            "it returns the carried result after the scan reaches N."
        ),
    },
    inventory["rules"][1]["source_rule_id"]: {
        "classification": "DEFINITION",
        "judgment": (
            "Guarded recursive equation of trialChoice for a divisor; it "
            "increments I and changes the carried result to Y."
        ),
    },
    inventory["rules"][2]["source_rule_id"]: {
        "classification": "DEFINITION",
        "judgment": (
            "Guarded recursive equation of trialChoice for a non-divisor; "
            "it increments I and preserves the carried result."
        ),
    },
    inventory["rules"][3]["source_rule_id"]: {
        "classification": "DEFINITION",
        "judgment": (
            "Disjoint base branch of the named xOrYSpec summary for N < 2."
        ),
    },
    inventory["rules"][4]["source_rule_id"]: {
        "classification": "DEFINITION",
        "judgment": (
            "Disjoint recursive-summary branch of xOrYSpec for N >= 2; it "
            "starts trialChoice at divisor 2 with X carried."
        ),
    },
}

guard_failures: list[dict[str, object]] = []
for n in range(-8, 21):
    for i in range(2, 25):
        base = i >= n and i >= 2
        divisor = i >= 2 and i < n and py_mod(n, i) == 0
        nondivisor = i >= 2 and i < n and py_mod(n, i) != 0
        if sum((base, divisor, nondivisor)) != 1:
            guard_failures.append(
                {
                    "n": n,
                    "i": i,
                    "base": base,
                    "divisor": divisor,
                    "nondivisor": nondivisor,
                }
            )

differential_failures: list[dict[str, object]] = []
for n in range(-25, 101):
    x = ("distinct-X", n)
    y = ("distinct-Y", n)
    observed = frozen_operational_body(n, x, y)
    expected = summary(n, x, y)
    if observed != expected:
        differential_failures.append(
            {"n": n, "operational": observed, "summary": expected}
        )

witnesses = []
for n in (-5, 0, 1, 2, 3, 4, 7, 15, 49):
    witnesses.append(
        {
            "n": n,
            "operational": frozen_operational_body(n, "X", "Y"),
            "summary": summary(n, "X", "Y"),
        }
    )

checks = {
    "five_local_rules": len(inventory["rules"]) == 5,
    "every_rule_independently_classified": (
        set(independent)
        == {rule["source_rule_id"] for rule in inventory["rules"]}
    ),
    "all_independent_classes_are_definition": all(
        entry["classification"] == "DEFINITION"
        for entry in independent.values()
    ),
    "protected_classes_match_independent_judgment": all(
        protected_by_id[source_rule_id]["classification"]
        == entry["classification"]
        for source_rule_id, entry in independent.items()
    ),
    "no_simplification_rules": all(
        "simplification" not in rule["attributes"]
        for rule in inventory["rules"]
    ),
    "all_lhs_are_named_summary_terms": all(
        rule["text"].lstrip().startswith(("rule trialChoice(", "rule xOrYSpec("))
        for rule in inventory["rules"]
    ),
    "no_operational_configuration_bridge": all(
        "<k>" not in rule["text"] and "<scopes>" not in rule["text"]
        for rule in inventory["rules"]
    ),
    "trialChoice_guards_disjoint_and_cover_declared_i_domain": (
        guard_failures == []
    ),
    "summary_matches_frozen_operational_body_on_test_range": (
        differential_failures == []
    ),
    "counterfactual_body_is_detected": (
        counterfactual_body(7, "X", "Y")
        != summary(7, "X", "Y")
    ),
}

result = {
    "independent_classification": independent,
    "checks": checks,
    "all_checks_pass": all(checks.values()),
    "guard_failures": guard_failures,
    "differential_range": {"n_min": -25, "n_max": 100},
    "differential_failures": differential_failures,
    "adversarial_witnesses": witnesses,
    "counterfactual_witness": {
        "n": 7,
        "frozen": frozen_operational_body(7, "X", "Y"),
        "summary": summary(7, "X", "Y"),
        "flipped_divisor_test": counterfactual_body(7, "X", "Y"),
    },
    "mathematical_note": (
        "For N >= 2, trialChoice scans exactly 2 through N-1, changing "
        "the carried value from X to Y iff a divisor is encountered. Thus "
        "the summary returns X exactly when that range contains no divisor; "
        "for N < 2, xOrYSpec returns Y directly."
    ),
}
print(json.dumps(result, indent=2, sort_keys=True))
