#!/usr/bin/env python3
"""Ground witnesses for each reachability claim and its result expression."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def load_entry(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.remove_vowels


canonical = load_entry(Path("/reference/canonical.py"), "witness_canonical")
generated = load_entry(
    Path("/tmp/audit-work/reconstruction/solution.py"), "witness_generated"
)
vowels = {ord(char) for char in "aeiouAEIOU"}


def text(codes: list[int]) -> str:
    return "".join(map(chr, codes))


def summary(acc: list[int], remaining: list[int]) -> list[int]:
    return acc + [code for code in remaining if code not in vowels]


# All loop witnesses use CALLEE=1, OUTER=.Map, TEXT=[116,120,116],
# CHAR=str(.IntSeq), and otherwise exactly the scope shape in spec.k.
witnesses = [
    ("loop-empty", [120], [], None, True),
    ("loop-vowel", [120], [97, 98], 97, 97 in vowels),
    ("loop-consonant", [120], [98, 97, 99], 98, 98 not in vowels),
]

for name, acc, remaining, head, precondition in witnesses:
    assert precondition
    claimed = text(summary(acc, remaining))
    canonical_result = text(acc) + canonical(text(remaining))
    generated_result = text(acc) + generated(text(remaining))
    assert claimed == canonical_result == generated_result
    print(
        f"{name}: CALLEE=1 ACC={acc} remaining={remaining} head={head} "
        f"precondition=true claimed={claimed!r} "
        f"canonical_acc_result={canonical_result!r} "
        f"generated_acc_result={generated_result!r}"
    )

entry_codes = [97, 66, 233, 69, 10, 117, 122]
entry_input = text(entry_codes)
entry_claimed = text(summary([], entry_codes))
entry_canonical = canonical(entry_input)
entry_generated = generated(entry_input)
assert entry_claimed == entry_canonical == entry_generated
print(
    f"entry: CODES={entry_codes} initial configuration exactly as spec.k; "
    f"claimed={entry_claimed!r} canonical={entry_canonical!r} "
    f"generated={entry_generated!r}"
)
print("ALL FOUR CLAIM PRECONDITIONS HAVE SATISFYING GROUND WITNESSES")
