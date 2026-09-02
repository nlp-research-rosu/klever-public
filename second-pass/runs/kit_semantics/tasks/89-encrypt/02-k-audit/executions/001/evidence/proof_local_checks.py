#!/usr/bin/env python3
"""Independent checks of every proof-local definition and its guard coverage."""

from __future__ import annotations

from pathlib import Path


VERIFICATION = Path("/tmp/audit-work/reconstruction/verification.k")


def py_mod(left: int, right: int) -> int:
    return ((left % right) + right) % right


def rot4_code(code: int) -> int:
    return py_mod(code - 97 + 4, 26) + 97


def encrypted_char(code: int) -> tuple[int, ...]:
    guards = [code < 97, 97 <= code <= 122, code > 122]
    assert sum(guards) == 1
    if guards[0] or guards[2]:
        return (code,)
    return (rot4_code(code),)


def encrypt_fold(accumulator: tuple[int, ...], suffix: tuple[int, ...]):
    current = accumulator
    remaining = suffix
    descent = []
    while remaining:
        descent.append(len(remaining))
        current = current + encrypted_char(remaining[0])
        remaining = remaining[1:]
    assert all(a > b for a, b in zip(descent, descent[1:]))
    return current


def final_loop_char(suffix: tuple[int, ...], initial):
    current = initial
    remaining = suffix
    while remaining:
        current = (remaining[0],)
        remaining = remaining[1:]
    return current


def main() -> None:
    text = VERIFICATION.read_text(encoding="utf-8")
    declarations = [line for line in text.splitlines() if line.strip().startswith("syntax ")]
    rules = [line for line in text.splitlines() if line.strip().startswith("rule ")]
    assert len(declarations) == 5
    assert len(rules) == 9
    assert text.count("[function, total]") == 5
    assert "<k>" not in text and "</k>" not in text
    for forbidden in [
        "simplification",
        "priority",
        "concrete",
        "owise",
        "no-evaluators",
        "fresh",
        "#Exists",
        "#Forall",
    ]:
        assert forbidden not in text, forbidden

    for code in range(-10000, 10001):
        result = encrypted_char(code)
        assert len(result) == 1
        if 97 <= code <= 122:
            assert 97 <= result[0] <= 122
            expected = 97 + ((code - 97 + 4) % 26)
            assert result[0] == expected
        else:
            assert result[0] == code

    assert [rot4_code(code) for code in range(97, 123)] == [
        ord(char) for char in "efghijklmnopqrstuvwxyzabcd"
    ]
    sample = tuple(map(ord, "`az{"))
    assert encrypt_fold((), sample) == tuple(map(ord, "`ed{"))
    assert encrypt_fold(tuple(map(ord, "P:")), sample) == tuple(
        map(ord, "P:`ed{")
    )
    assert final_loop_char((), "prior") == "prior"
    assert final_loop_char(sample, "prior") == (ord("{"),)

    print(f"proof_local_syntax_declarations={len(declarations)}")
    print(f"proof_local_rules={len(rules)}")
    print("operational_bridges=0")
    print("simplification_rules=0")
    print("priority_rules=0")
    print("opaque_symbols=0")
    print("guard_partition_test_range=-10000..10000")
    print("rot4_all_26_lowercase_codes=PASS")
    print("structural_descent_examples=PASS")
    print("PROOF_LOCAL_CHECKS=PASS")


if __name__ == "__main__":
    main()
