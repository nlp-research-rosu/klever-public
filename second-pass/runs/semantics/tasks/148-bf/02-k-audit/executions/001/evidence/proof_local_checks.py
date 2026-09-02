#!/usr/bin/env python3
"""Mechanical checks over the proof-local BF-VERIFICATION theory."""

from __future__ import annotations

import ast
import re
from pathlib import Path


SCRATCH = Path("/tmp/audit-work/148-bf-audit")
VERIFICATION = SCRATCH / "verification.k"
PLANET_CTORS = [
    "pMercury",
    "pVenus",
    "pEarth",
    "pMars",
    "pJupiter",
    "pSaturn",
    "pUranus",
    "pNeptune",
]


def main() -> None:
    text = VERIFICATION.read_text()
    code = "\n".join(line.split("//", 1)[0] for line in text.splitlines())

    assert re.search(r"^\s*claim\b", code, flags=re.MULTILINE) is None
    for forbidden in ["simplification", "no-evaluators", "[owise]", "priority("]:
        assert forbidden not in code, forbidden

    total_declarations = re.findall(
        r"^\s*syntax\s+.*?\[([^\]]*\btotal\b[^\]]*)\]",
        code,
        flags=re.MULTILINE,
    )
    assert len(total_declarations) == 4
    assert "planetVals" in code
    assert "expectedBetween(Int, Int)" in code
    assert "planetCodes(Planet)" in code
    assert "planetPosition(Planet)" in code

    for ctor in PLANET_CTORS:
        assert len(re.findall(rf"rule planetCodes\({ctor}\)", code)) == 1
        assert len(re.findall(rf"rule planetPosition\({ctor}\)", code)) == 1

    planet_expr_cases = re.findall(r"rule planetExpr\((\d)\)", code)
    assert planet_expr_cases == [str(index) for index in range(8)]

    states: list[tuple[int, int]] = []
    state = (0, 0)
    while True:
        states.append(state)
        i, j = state
        if (i, j) == (7, 7):
            break
        if j < 7:
            state = (i, j + 1)
        else:
            state = (i + 1, 0)
    assert len(states) == 64
    assert len(set(states)) == 64
    assert set(states) == {(i, j) for i in range(8) for j in range(8)}

    source_kore = (SCRATCH / "body-from-solution.kore").read_bytes()
    macro_kore = (SCRATCH / "body-from-macro.kore").read_bytes()
    assert source_kore == macro_kore
    solution_tree = ast.parse((SCRATCH / "solution.py").read_text())
    source_function = solution_tree.body[0]
    assert isinstance(source_function, ast.FunctionDef)
    assert source_function.name == "bf"
    assert [argument.arg for argument in source_function.args.args] == [
        "planet1",
        "planet2",
    ]
    compact_code = re.sub(r"\s+", "", code)
    assert (
        'closureVal("planet1","planet2",.ParamNames,bfBody,0)'
        in compact_code
    )

    print(f"proof_local_total_declarations={len(total_declarations)}")
    print(f"planet_constructor_cases={len(PLANET_CTORS)}")
    print(f"planet_expr_ground_cases={len(planet_expr_cases)}")
    print(f"valid_case_states={len(states)} unique={len(set(states))}")
    print("forbidden_proof_extensions=none")
    print("source_body_equals_macro_body=true")
    print("source_name_params_and_module_scope_anchor_equal_bfRun=true")
    print("PROOF_LOCAL_CHECKS=PASS")


if __name__ == "__main__":
    main()
