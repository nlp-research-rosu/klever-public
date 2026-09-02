#!/usr/bin/env python3
"""Concrete satisfying states and result substitutions for both positive claims."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path


def load(path: str, name: str):
    spec = importlib.util.spec_from_file_location(name, Path(path))
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.all_prefixes


canonical = load("/reference/canonical.py", "canonical_for_adequacy")
candidate = load(
    "/tmp/audit-work/proof-audit.Dl0nBZ/candidate/solution.py",
    "candidate_for_adequacy",
)


def prefixes_acc(value: str, end: int, stop: int, acc: list[str]) -> list[str]:
    result = list(acc)
    while end < stop:
        result.append(value[:end])
        end += 1
    return result


entry_witnesses = []
for value in ("", "abc", "é🙂"):
    formal = prefixes_acc(value, 1, len(value) + 1, [])
    entry_witnesses.append(
        {
            "S": [ord(ch) for ch in value],
            "python_string": value,
            "precondition": "none beyond S:IntSeq",
            "formal_allPrefixes": formal,
            "canonical": canonical(value),
            "candidate": candidate(value),
            "return": "ref(0)",
            "heap_0": formal,
            "all_equal": formal == canonical(value) == candidate(value),
        }
    )

loop_value = "ab"
loop_formal = prefixes_acc(loop_value, 1, 3, [])
loop_witness = {
    "S": [97, 98],
    "END": 1,
    "STOP": 3,
    "ACC": [],
    "L": 0,
    "H": 0,
    "SC": {},
    "HP": {},
    "PREV": 0,
    "P": "parent(-1)",
    "CONT": ".K",
    "requires_END_le_STOP": 1 <= 3,
    "formal_prefixesAcc": loop_formal,
    "canonical": canonical(loop_value),
    "candidate": candidate(loop_value),
    "all_equal": loop_formal == canonical(loop_value) == candidate(loop_value),
}

result = {
    "loop_claim_satisfying_state": loop_witness,
    "entry_claim_satisfying_states": entry_witnesses,
}
print(json.dumps(result, ensure_ascii=True, indent=2, sort_keys=True))
if not loop_witness["all_equal"]:
    raise SystemExit(1)
if not all(witness["all_equal"] for witness in entry_witnesses):
    raise SystemExit(1)

