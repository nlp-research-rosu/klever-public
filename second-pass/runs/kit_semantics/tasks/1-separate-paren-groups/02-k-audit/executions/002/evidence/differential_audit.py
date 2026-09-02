#!/usr/bin/env python3
"""Independent canonical/candidate/contract differential audit."""

from __future__ import annotations

import importlib.util
import json
from functools import lru_cache
from pathlib import Path


def load_entry(module_name: str, path: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.separate_paren_groups


canonical = load_entry("trusted_canonical", "/reference/canonical.py")
candidate = load_entry("audited_candidate", "/candidate/solution.py")


def contract_oracle(text: str) -> list[str]:
    """Split a valid balanced-parenthesis input at top-level depth zero."""
    compact = text.replace(" ", "")
    groups: list[str] = []
    start = 0
    depth = 0
    for index, character in enumerate(compact):
        if character == "(":
            depth += 1
        elif character == ")":
            depth -= 1
        else:
            raise AssertionError(f"generated invalid character: {character!r}")
        if depth < 0:
            raise AssertionError(f"generated negative depth: {text!r}")
        if depth == 0:
            groups.append(compact[start : index + 1])
            start = index + 1
    if depth != 0 or start != len(compact):
        raise AssertionError(f"generated unbalanced input: {text!r}")
    return groups


@lru_cache(maxsize=None)
def balanced_words(pairs: int) -> tuple[str, ...]:
    if pairs == 0:
        return ("",)
    words: set[str] = set()
    for inside_pairs in range(pairs):
        outside_pairs = pairs - 1 - inside_pairs
        for inside in balanced_words(inside_pairs):
            for outside in balanced_words(outside_pairs):
                words.add("(" + inside + ")" + outside)
    return tuple(sorted(words))


def spaced_variants(word: str) -> set[str]:
    if not word:
        return {"", " ", "   "}
    return {
        word,
        " " + word,
        word + " ",
        " ".join(word),
        "".join((" " if index % 2 == 0 else "") + char for index, char in enumerate(word)),
        "".join(char + ("  " if index % 3 == 0 else "") for index, char in enumerate(word)),
    }


documented = {
    "( ) (( )) (( )( ))",
    "",
    " ",
    "   ",
    "()",
    "( )",
    "()()",
    "() ()",
    "(())",
    "(()())",
    "((()))",
    "(())(()())",
    " ( ( ) )  ( ) ",
}

generated: set[str] = set(documented)
for pair_count in range(0, 8):
    for word in balanced_words(pair_count):
        generated.update(spaced_variants(word))

records: list[dict[str, object]] = []
mismatches: list[dict[str, object]] = []
for text in sorted(generated, key=lambda value: (len(value), value)):
    expected = contract_oracle(text)
    canonical_result = canonical(text)
    candidate_result = candidate(text)
    record = {
        "input": text,
        "oracle": expected,
        "canonical": canonical_result,
        "candidate": candidate_result,
    }
    records.append(record)
    if not (expected == canonical_result == candidate_result):
        mismatches.append(record)

output_path = Path("/audit-output/evidence/differential_inputs_results.json")
output_path.write_text(
    json.dumps(records, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
    encoding="utf-8",
)

print(f"DOCUMENTED_AND_BOUNDARY_CASES={len(documented)}")
print("GENERATED_PAIR_RANGE=0..7")
print(f"TOTAL_DISTINCT_CASES={len(records)}")
print(f"MISMATCHES={len(mismatches)}")
print(f"RESULT_FILE={output_path}")
for record in mismatches[:10]:
    print(json.dumps(record, ensure_ascii=False, sort_keys=True))
if mismatches:
    raise SystemExit(1)
