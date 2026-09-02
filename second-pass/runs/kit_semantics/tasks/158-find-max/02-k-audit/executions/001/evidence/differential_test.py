#!/usr/bin/env python3
"""Independent canonical-vs-generated differential test for HumanEval 158."""

import importlib.util
import json
import random
from itertools import permutations
from pathlib import Path


def import_from(path, module_name):
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


trusted = import_from(Path("/reference/canonical.py"), "trusted_canonical_158")
generated = import_from(
    Path("/tmp/audit-work/reconstruct-001/solution.py"),
    "generated_solution_158",
)


def outcome(function, words):
    try:
        return {"kind": "return", "value": function(list(words))}
    except Exception as error:
        return {
            "kind": "exception",
            "type": type(error).__name__,
            "message": str(error),
        }


named_cases = [
    ("example_score", ["name", "of", "string"]),
    ("example_tie", ["name", "enam", "game"]),
    ("example_repeat_chars", ["aaaaaaa", "bb", "cc"]),
    ("empty_list_boundary", []),
    ("single_empty_word", [""]),
    ("single_nonempty_word", ["abc"]),
    ("greater_score_replaces", ["z", "ab"]),
    ("lower_score_does_not_replace", ["ab", "z"]),
    ("equal_score_lex_smaller_replaces", ["ba", "ab"]),
    ("equal_score_lex_larger_does_not_replace", ["ab", "ba"]),
    ("equal_zero_score", [""]),
    ("unicode_codepoint_order", ["é", "e", "😀"]),
    ("unicode_composed_decomposed", ["é", "e\u0301"]),
    ("long_string_boundary", ["a" * 500, "ab" * 250]),
]

pool = ["", "a", "b", "aa", "ab", "ba", "abc"]
cases = list(named_cases)
for size in range(1, 5):
    for words in permutations(pool, size):
        cases.append((f"small_permutation_{size}", list(words)))

rng = random.Random(1580729)
alphabet = "abcxyzé😀"
universe = {""}
for _ in range(100):
    length = rng.randrange(0, 18)
    universe.add("".join(rng.choice(alphabet) for _ in range(length)))
universe = sorted(universe)
for index in range(750):
    size = rng.randrange(1, min(16, len(universe)) + 1)
    cases.append((f"generated_distinct_{index}", rng.sample(universe, size)))

records = []
intended_mismatches = []
empty_divergences = []
for name, words in cases:
    canonical_result = outcome(trusted.find_max, words)
    generated_result = outcome(generated.find_max, words)
    record = {
        "name": name,
        "words": words,
        "canonical": canonical_result,
        "generated": generated_result,
        "equal": canonical_result == generated_result,
    }
    records.append(record)
    if not record["equal"]:
        if words:
            intended_mismatches.append(record)
        else:
            empty_divergences.append(record)

output_path = Path("/audit-output/evidence/differential_cases.json")
output_path.write_text(
    json.dumps(records, ensure_ascii=False, indent=2) + "\n",
    encoding="utf-8",
)

print(f"total_cases={len(records)}")
print(f"nonempty_cases={sum(bool(record['words']) for record in records)}")
print(f"nonempty_mismatches={len(intended_mismatches)}")
print(f"empty_divergences={len(empty_divergences)}")
if empty_divergences:
    print(
        "empty_boundary="
        + json.dumps(empty_divergences[0], ensure_ascii=False, sort_keys=True)
    )
print(f"case_manifest={output_path}")

for required_name, _ in named_cases:
    selected = next(record for record in records if record["name"] == required_name)
    print(
        "named_case="
        + json.dumps(selected, ensure_ascii=False, sort_keys=True)
    )

if intended_mismatches:
    print(
        "first_nonempty_mismatch="
        + json.dumps(intended_mismatches[0], ensure_ascii=False, sort_keys=True)
    )
    raise SystemExit(1)
