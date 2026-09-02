#!/usr/bin/env python3
"""Concrete satisfying witnesses for every entry claim precondition."""

from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path("/tmp/audit-work/87-get-row-review")


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


candidate = load("candidate_witness", ROOT / "solution.py").get_row
canonical = load("canonical_witness", ROOT / "trusted_canonical.py").get_row


def expected_flags(a_hit: bool, b_hit: bool, c_hit: bool):
    answer = []
    if b_hit:
        answer.append((0, 1))
    if a_hit:
        answer.append((0, 0))
    if c_hit:
        answer.append((1, 0))
    return answer


def check(label, rows, key, expected):
    generated = candidate(rows, key)
    trusted = canonical(rows, key)
    ok = generated == trusted == expected
    print(
        f"{label}: input={rows!r}, x={key}, expected={expected!r}, "
        f"generated={generated!r}, canonical={trusted!r}, equal={ok}"
    )
    if not ok:
        raise AssertionError(label)


def main() -> None:
    check(
        "example-prompt",
        [[1, 2, 3, 4, 5, 6], [1, 2, 3, 4, 1, 6], [1, 2, 3, 4, 5, 1]],
        1,
        [(0, 0), (1, 4), (1, 0), (2, 5), (2, 0)],
    )
    check("example-empty", [], 1, [])
    check("example-third", [[], [1], [1, 2, 3]], 3, [(2, 2)])

    for a_hit in (False, True):
        for b_hit in (False, True):
            for c_hit in (False, True):
                key = 0
                a = key if a_hit else 1
                b = key if b_hit else 1
                c = key if c_hit else 1
                assert (a == key) == a_hit
                assert (b == key) == b_hit
                assert (c == key) == c_hit
                bits = f"{int(a_hit)}{int(b_hit)}{int(c_hit)}"
                check(
                    f"symbolic-{bits}",
                    [[a, b], [c]],
                    key,
                    expected_flags(a_hit, b_hit, c_hit),
                )
    print("satisfying_entry_witnesses=11")


if __name__ == "__main__":
    main()
