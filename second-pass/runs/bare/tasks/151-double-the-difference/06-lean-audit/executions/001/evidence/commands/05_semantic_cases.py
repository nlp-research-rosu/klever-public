#!/usr/bin/env python3
import json


def selected_square(value: int) -> int:
    return value * value if value >= 0 and value % 2 == 1 else 0


def operational_contribution(tag: str, value):
    is_int = tag in {"int", "bool"}
    if not is_int:
        return 0
    integer = int(value)
    if integer < 0:
        return 0
    if integer % 2 != 1:
        return 0
    return integer * integer


def summary_contribution(tag: str, value):
    if tag == "int":
        return selected_square(value)
    if tag == "bool":
        return 1 if value is True else 0
    if tag in {"float", "list"}:
        return 0
    raise ValueError(tag)


cases = [
    *[("int", value) for value in range(-11, 12)],
    ("int", 10**30 + 1),
    ("int", -(10**30 + 1)),
    ("bool", True),
    ("bool", False),
    ("float", 1.5),
    ("float", -3.0),
    ("list", []),
    ("list", [7]),
]
results = [
    {
        "tag": tag,
        "value": value,
        "operational_contribution": operational_contribution(tag, value),
        "summary_contribution": summary_contribution(tag, value),
        "match": operational_contribution(tag, value)
        == summary_contribution(tag, value),
    }
    for tag, value in cases
]
mutations = {
    "constant_zero_detected": any(
        summary_contribution(tag, value) != 0 for tag, value in cases
    ),
    "identity_detected": any(
        summary_contribution(tag, value) != int(value)
        for tag, value in cases
        if tag in {"int", "bool"}
    ),
    "square_every_integer_detected": any(
        summary_contribution("int", value) != value * value
        for value in range(-11, 12)
    ),
    "exclude_bool_detected": summary_contribution("bool", True) != 0,
}
print(
    json.dumps(
        {
            "scope": (
                "Finite adversarial corroboration only. The universal "
                "classification judgment follows separately from the five "
                "Vals constructors and complementary integer guards in the "
                "frozen K source."
            ),
            "all_cases_match": all(result["match"] for result in results),
            "cases": results,
            "counterfactual_mutations": mutations,
            "all_counterfactuals_detected": all(mutations.values()),
        },
        indent=2,
        sort_keys=True,
    )
)
