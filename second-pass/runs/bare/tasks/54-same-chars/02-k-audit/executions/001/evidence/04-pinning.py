#!/usr/bin/env python3
"""Check that the proof's solutionProgram is exactly the submitted translation."""

from __future__ import annotations

import importlib.util
from pathlib import Path


WORK = Path("/tmp/audit-work/reconstruction")
MPY = WORK / "solution.mpy"
HELPER = WORK / "solution-program.k"


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def expected_helper(program: str) -> str:
    return (
        'requires "semantic.k"\n'
        "\n"
        "module SOLUTION\n"
        "  imports MPY\n"
        '  syntax Program ::= "solutionProgram" [function]\n'
        f"  rule solutionProgram => {program.strip()}\n"
        "endmodule\n"
    )


def main() -> int:
    actual_helper = HELPER.read_text(encoding="utf-8")
    program = MPY.read_text(encoding="utf-8")
    expected = expected_helper(program)
    helper_match = actual_helper == expected

    canonical = load(
        Path("/tmp/audit-work/trusted/canonical.py"), "trusted_canonical_pinning"
    ).same_chars
    subject = load(WORK / "solution.py", "candidate_solution_pinning").same_chars
    witnesses = [
        ("ab", "ba"),
        ("ab", "aa"),
        ("", ""),
        ("", "a"),
    ]

    print(f"solution_mpy={MPY}")
    print(f"solution_program_helper={HELPER}")
    print(f"helper_is_exact_wrapper={helper_match}")
    print("universal_entry_precondition_has_no_requires_clause")
    print(
        "entry_state_shape=<k> solutionProgram </k>, "
        "<s0> S0:String </s0>, <s1> S1:String </s1>, "
        "<env> .Map </env>, <result> noResult </result>"
    )
    for left, right in witnesses:
        canonical_result = canonical(left, right)
        subject_result = subject(left, right)
        mathematical_result = set(left) == set(right)
        print(
            f"witness={left!r},{right!r} "
            f"set_left={sorted(set(left))!r} set_right={sorted(set(right))!r} "
            f"claimed_result={mathematical_result!r} "
            f"canonical={canonical_result!r} solution={subject_result!r}"
        )

    return 0 if (
        helper_match
        and all(canonical(a, b) == subject(a, b) == (set(a) == set(b))
                for a, b in witnesses)
    ) else 1


if __name__ == "__main__":
    raise SystemExit(main())
