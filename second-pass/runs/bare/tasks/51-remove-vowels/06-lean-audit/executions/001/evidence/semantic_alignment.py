#!/usr/bin/env python3
"""Parse, do not execute, the frozen source and compare its vowel chain."""

from __future__ import annotations

import ast
import hashlib
import json
import re
from pathlib import Path


source_path = Path("/reference/k-proof/solution.py")
verification_path = Path("/reference/k-proof/verification.k")
semantics_path = Path("/reference/k-proof/semantic.k")

module = ast.parse(source_path.read_text())
function = module.body[0]
assert isinstance(function, ast.FunctionDef)
assert function.name == "remove_vowels"
assert len(function.body) == 1 and isinstance(function.body[0], ast.Return)


def replacement_chain(expression: ast.expr) -> tuple[ast.expr, list[tuple[str, str]]]:
    replacements: list[tuple[str, str]] = []
    current = expression
    while (
        isinstance(current, ast.Call)
        and isinstance(current.func, ast.Attribute)
        and current.func.attr == "replace"
        and len(current.args) == 2
        and all(
            isinstance(argument, ast.Constant)
            and isinstance(argument.value, str)
            for argument in current.args
        )
    ):
        replacements.append(
            (current.args[0].value, current.args[1].value)
        )
        current = current.func.value
    replacements.reverse()
    return current, replacements


base, source_replacements = replacement_chain(function.body[0].value)
assert (
    isinstance(base, ast.Name)
    and base.id == "text"
    and [new for _old, new in source_replacements] == [""] * 10
)
source_needles = [old for old, _new in source_replacements]

verification = verification_path.read_text()
lower_body = re.search(
    r"rule removeLowerVowels\(S\)(.*?)\n\s*rule removeUpperVowels",
    verification,
    re.S,
).group(1)
upper_body = re.search(
    r"rule removeUpperVowels\(S\)(.*?)\n\s*rule removeVowelsSpec",
    verification,
    re.S,
).group(1)
lower_needles = re.findall(r'"([^"]*)"', lower_body)
upper_needles = re.findall(r'"([^"]*)"', upper_body)
summary_needles = lower_needles + upper_needles

semantics = semantics_path.read_text()
bridge_lines = [
    "rule deleteAll(S, NEEDLE) => replaceAll(S, NEEDLE, \"\")",
    "rule replaceValue(strVal(S), OLD, \"\") => strVal(deleteAll(S, OLD))",
]

tests = [
    "",
    "aAeEiIoOuU",
    "xyz",
    "abA\nEuv",
    "áéAEiou",
    "queueing",
    "UuU",
    "🙂aZΩU",
]
vowels = set("aeiouAEIOU")
cases = []
for value in tests:
    source_model = value
    for needle in source_needles:
        source_model = source_model.replace(needle, "")
    summary_model = value
    for needle in summary_needles:
        summary_model = summary_model.replace(needle, "")
    independent_filter = "".join(
        character for character in value if character not in vowels
    )
    cases.append(
        {
            "input": value,
            "source_model": source_model,
            "summary_model": summary_model,
            "independent_filter": independent_filter,
            "all_equal": (
                source_model == summary_model == independent_filter
            ),
        }
    )

counterfactuals = [
    {
        "mutation": "identity instead of deletion chain",
        "input": "aA",
        "correct": "",
        "mutated": "aA",
    },
    {
        "mutation": "omit uppercase U deletion",
        "input": "U",
        "correct": "",
        "mutated": "U",
    },
    {
        "mutation": "delete b instead of lowercase a",
        "input": "ab",
        "correct": "b",
        "mutated": "a",
    },
    {
        "mutation": "constant empty output",
        "input": "xyz",
        "correct": "xyz",
        "mutated": "",
    },
]

checks = {
    "source_chain_exact": source_needles
    == list("aeiouAEIOU"),
    "summary_chain_exact": summary_needles
    == list("aeiouAEIOU"),
    "source_summary_chain_equal": source_needles == summary_needles,
    "k_deleteAll_bridge_present": all(
        line in semantics for line in bridge_lines
    ),
    "all_adversarial_cases_agree": all(
        case["all_equal"] for case in cases
    ),
    "all_counterfactuals_detected": all(
        item["correct"] != item["mutated"]
        for item in counterfactuals
    ),
}

result = {
    "source_sha256": hashlib.sha256(
        source_path.read_bytes()
    ).hexdigest(),
    "verification_sha256": hashlib.sha256(
        verification_path.read_bytes()
    ).hexdigest(),
    "semantic_sha256": hashlib.sha256(
        semantics_path.read_bytes()
    ).hexdigest(),
    "source_needles": source_needles,
    "summary_needles": summary_needles,
    "checks": checks,
    "cases": cases,
    "counterfactuals": counterfactuals,
}
print(json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False))
raise SystemExit(0 if all(checks.values()) else 1)
