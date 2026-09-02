#!/usr/bin/env python3
import json
import re
from pathlib import Path


transcript = Path(
    "/audit-output/evidence/09-fresh-operational-k.txt"
).read_text(errors="replace")
plain = re.sub(r"\x1b\[[0-9;]*m", "", transcript)
observed = {
    int(argument): int(result)
    for argument, result in re.findall(
        r"CASE n=(-?\d+).*?<k>\s*(-?\d+)\s*~>\s*\.K",
        plain,
        re.S,
    )
}


def recurrence(base_zero: int = 0, base_one: int = 1, duplicate=False):
    values = [base_zero, base_one]
    for _n in range(2, 9):
        values.append(
            values[-1] + (values[-1] if duplicate else values[-2])
        )
    return {n: values[n] for n in observed}


expected = recurrence()
counterfactuals = {
    "constant_zero": {n: 0 for n in observed},
    "identity": {n: n for n in observed},
    "wrong_base_zero_is_one": recurrence(base_zero=1),
    "duplicate_n_minus_one": recurrence(duplicate=True),
}
checks = {
    "expected_cases_exact": sorted(observed) == [0, 1, 2, 3, 5, 8],
    "operational_results_match_definition": observed == expected,
    "every_counterfactual_rejected": all(
        values != observed for values in counterfactuals.values()
    ),
}
print(
    json.dumps(
        {
            "observed_operational_results": observed,
            "definition_recurrence_results": expected,
            "counterfactual_results": counterfactuals,
            "checks": checks,
            "all_checks_pass": all(checks.values()),
        },
        indent=2,
        sort_keys=True,
    )
)
raise SystemExit(0 if all(checks.values()) else 1)
