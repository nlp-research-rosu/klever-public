#!/usr/bin/env python3
"""Ground interpretations of the entry postcondition for satisfying StrList inputs."""

from __future__ import annotations

import importlib.util
import json


def load(name: str, path: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.sorted_list_sum


canonical = load("canonical_ground", "/reference/canonical.py")
candidate = load("candidate_ground", "/candidate/solution.py")


def interpret_entry_postcondition(words: list[str]) -> list[str]:
    # evenAppend(.ValSeq, INPUT), then sortVS, then stable sortKeyVS(..., len).
    even_append = [word for word in words if len(word) % 2 == 0]
    sort_vs = sorted(even_append)
    sort_key_vs = sorted(sort_vs, key=len)
    return sort_key_vs


cases = [
    [],
    ["aa"],
    ["aa", "a", "aaa"],
    ["zz", "a", "bbbb", "aa", "cc", "odd"],
    ["bb", "aa", "bb", "x"],
]
failures = []
for words in cases:
    formal = interpret_entry_postcondition(words)
    canonical_result = canonical(words.copy())
    candidate_result = candidate(words.copy())
    record = {
        "input": words,
        "formal_postcondition_interpretation": formal,
        "trusted_canonical": canonical_result,
        "candidate_python": candidate_result,
    }
    print(json.dumps(record, ensure_ascii=False, sort_keys=True))
    if not (formal == canonical_result == candidate_result):
        failures.append(record)

print(f"satisfying_ground_states={len(cases)}")
print(f"mismatches={len(failures)}")
raise SystemExit(1 if failures else 0)
