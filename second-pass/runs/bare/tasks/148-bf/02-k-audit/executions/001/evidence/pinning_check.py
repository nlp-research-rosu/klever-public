#!/usr/bin/env python3
"""Mechanical source-term pinning and claim-partition adequacy checks."""

from __future__ import annotations

import hashlib
import importlib.util
import itertools
import re
from pathlib import Path


ROOT = Path("/tmp/audit-work/candidate-src")
PLANETS = (
    "Mercury",
    "Venus",
    "Earth",
    "Mars",
    "Jupiter",
    "Saturn",
    "Uranus",
    "Neptune",
)


def load_function(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.bf


def expected_between(first: str, second: str) -> tuple[str, ...]:
    first_index = PLANETS.index(first)
    second_index = PLANETS.index(second)
    lo = min(first_index, second_index) + 1
    hi = max(first_index, second_index)
    return PLANETS[lo:hi]


def normalized_translated_program() -> str:
    lines = (ROOT / "solution.mpy").read_text().rstrip().splitlines()
    normalized = list(lines)
    for index, line in enumerate(normalized):
        if (
            line.strip() == ")"
            and index > 0
            and normalized[index - 1].rstrip().endswith(",")
        ):
            indentation = line[: len(line) - len(line.lstrip())]
            normalized[index] = indentation + ".Stmts)"
    return "\n".join(normalized).replace("TupleExpr()", "TupleExpr(.Exprs)")


def executed_program_rhs() -> str:
    text = (ROOT / "solution-program.k").read_text()
    prefix = '  rule solutionProgram =>\n'
    assert text.count(prefix) == 1
    rhs = text.split(prefix, 1)[1].rsplit("\nendmodule", 1)[0]
    return "\n".join(
        line[4:] if line.startswith("    ") else line for line in rhs.splitlines()
    )


def main() -> None:
    translated = normalized_translated_program()
    executed = executed_program_rhs()
    assert translated == executed
    print("normalized trusted-translator term exactly equals solutionProgram rule RHS")
    print(f"normalized constructor bytes={len(translated.encode())}")
    print(f"normalized constructor sha256={hashlib.sha256(translated.encode()).hexdigest()}")
    assert translated.startswith(
        'Module(\n  FuncDef("bf", Params("planet1", "planet2"),'
    )
    print("binding pinned: one Module-level bf with exact two parameter names and body")

    spec_text = (ROOT / "spec.k").read_text()
    blocks = re.findall(r"  claim\n(.*?)(?=\n\n  claim|\nendmodule)", spec_text, re.S)
    assert len(blocks) == 73
    print("claim_count=73")

    canonical = load_function("pinning_canonical", Path("/reference/canonical.py"))
    candidate = load_function("pinning_candidate", ROOT / "solution.py")

    # First 64 claims are the complete 8x8 ground partition in product order.
    for index, (first, second) in enumerate(itertools.product(PLANETS, repeat=2)):
        block = blocks[index]
        expected = expected_between(first, second)
        assert f'verifyBF("{first}", "{second}")' in block
        rendered = (
            "tupleValue(.StringValues)"
            if not expected
            else "tupleValue(" + ", ".join(f'"{item}"' for item in expected) + ")"
        )
        assert f"<result> noResult => {rendered} </result>" in block
        assert canonical(first, second) == expected
        assert candidate(first, second) == expected
        print(
            f"witness claim={index + 1:02d} inputs=({first!r},{second!r}) "
            f"claimed={expected!r} both_python_match=True"
        )

    inequalities_p1 = " andBool ".join(
        f'P1 =/=String "{planet}"' for planet in PLANETS
    )
    assert "verifyBF(P1, P2)" in blocks[64]
    assert f"requires {inequalities_p1}" in blocks[64]
    assert canonical("Pluto", "Mercury") == ()
    assert candidate("Pluto", "Mercury") == ()
    print(
        "witness claim=65 inputs=('Pluto','Mercury') "
        "precondition=P1-not-any-planet claimed=() both_python_match=True"
    )

    inequalities_p2 = " andBool ".join(
        f'P2 =/=String "{planet}"' for planet in PLANETS
    )
    for offset, first in enumerate(PLANETS, start=65):
        block = blocks[offset]
        assert f'verifyBF("{first}", P2)' in block
        assert f"requires {inequalities_p2}" in block
        assert canonical(first, "Pluto") == ()
        assert candidate(first, "Pluto") == ()
        print(
            f"witness claim={offset + 1:02d} inputs=({first!r},'Pluto') "
            "precondition=P2-not-any-planet claimed=() both_python_match=True"
        )

    print(
        "coverage partition: valid×valid=64; invalid-P1×all=1 symbolic; "
        "valid-P1×invalid-P2=8 symbolic"
    )
    print("all 73 entry preconditions have exhibited satisfying witnesses")
    print("all exhibited claims agree with trusted canonical and candidate Python")


if __name__ == "__main__":
    main()
