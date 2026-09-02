#!/usr/bin/env python3
"""Independent prompt-oracle differential for HumanEval 95.

The candidate and trusted canonical modules are loaded from explicit paths.
The prompt oracle is written independently from either implementation.
"""

from __future__ import annotations

import importlib.util
import itertools
import json
from pathlib import Path
from typing import Any, Callable


SCRATCH = Path("/tmp/audit-work/candidate-src")


def load_entry(path: Path, module_name: str) -> Callable[[dict[Any, Any]], bool]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.check_dict_case


def prompt_oracle(mapping: dict[Any, Any]) -> bool:
    if not mapping:
        return False
    keys = list(mapping)
    if not all(isinstance(key, str) for key in keys):
        return False
    return all(key.islower() for key in keys) or all(
        key.isupper() for key in keys
    )


generated = load_entry(SCRATCH / "solution.py", "audited_solution")
canonical = load_entry(SCRATCH / "canonical.py", "trusted_canonical")

documented = [
    ("example_lower", {"a": "apple", "b": "banana"}),
    ("example_mixed", {"a": "apple", "A": "banana", "B": "banana"}),
    ("example_non_string", {"a": "apple", 8: "banana"}),
    ("example_title", {"Name": "John", "Age": "36", "City": "Houston"}),
    ("example_upper", {"STATE": "NC", "ZIP": "12345"}),
]

boundaries = [
    ("empty", {}),
    ("one_lower", {"a": 0}),
    ("one_upper", {"A": 0}),
    ("one_uncased", {"123": 0}),
    ("punctuated_lower", {"abc-123": 0, "z9": 0}),
    ("punctuated_upper", {"ABC-123": 0, "Z9": 0}),
    ("mixed_in_one", {"aA": 0}),
    ("non_string_first", {8: 0, "a": 0}),
    ("non_string_middle", {"a": 0, 8: 0, "b": 0}),
    ("non_string_late", {"a": 0, "b": 0, 8: 0}),
    ("mixed_at_second", {"a": 0, "B": 0}),
    ("mixed_late", {"a": 0, "b": 0, "C": 0}),
    ("unicode_lower", {"é": 0, "ß": 0}),
    ("unicode_upper", {"É": 0, "İ": 0}),
    ("unicode_mixed", {"é": 0, "É": 0}),
    ("unicode_uncased", {"中": 0}),
    ("emoji_uncased", {"🙂": 0}),
]

# Exhaustive ordered dictionaries induced by key sequences of length 0..4
# over this small pool. Duplicate/equal keys receive ordinary Python dict
# normalization, including True == 1.
pool: tuple[Any, ...] = ("a", "b", "A", "B", "1", "aA", "é", "É", 0, True)
generated_cases: dict[tuple[Any, ...], dict[Any, int]] = {}
for length in range(5):
    for seq in itertools.product(pool, repeat=length):
        mapping = {key: index for index, key in enumerate(seq)}
        normalized = tuple(mapping.keys())
        generated_cases.setdefault(normalized, mapping)

records: list[dict[str, Any]] = []


def record(label: str, mapping: dict[Any, Any], category: str) -> None:
    expected = prompt_oracle(mapping)
    candidate_result = generated(mapping)
    canonical_result = canonical(mapping)
    records.append(
        {
            "category": category,
            "label": label,
            "keys_repr": repr(list(mapping)),
            "prompt_oracle": expected,
            "generated": candidate_result,
            "canonical": canonical_result,
        }
    )


for label, mapping in documented:
    record(label, mapping, "documented")
for label, mapping in boundaries:
    record(label, mapping, "boundary")
for index, mapping in enumerate(generated_cases.values()):
    record(f"generated_{index:05d}", mapping, "generated")

generated_mismatches = [
    item for item in records if item["generated"] != item["prompt_oracle"]
]
canonical_mismatches = [
    item for item in records if item["canonical"] != item["prompt_oracle"]
]
pair_mismatches = [
    item for item in records if item["canonical"] != item["generated"]
]

summary = {
    "documented_cases": len(documented),
    "boundary_cases": len(boundaries),
    "generated_normalized_cases": len(generated_cases),
    "total_records": len(records),
    "generated_vs_prompt_mismatches": len(generated_mismatches),
    "canonical_vs_prompt_mismatches": len(canonical_mismatches),
    "generated_vs_canonical_mismatches": len(pair_mismatches),
}
print(json.dumps(summary, indent=2, sort_keys=True))

for heading, mismatches in (
    ("GENERATED_VS_PROMPT", generated_mismatches),
    ("CANONICAL_VS_PROMPT", canonical_mismatches),
    ("GENERATED_VS_CANONICAL", pair_mismatches),
):
    print(f"{heading}_FIRST_20:")
    for item in mismatches[:20]:
        print(json.dumps(item, ensure_ascii=False, sort_keys=True))

if generated_mismatches:
    raise SystemExit("candidate solution.py diverges from the prompt oracle")
