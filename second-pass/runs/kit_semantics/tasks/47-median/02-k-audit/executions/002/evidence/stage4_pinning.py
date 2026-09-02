#!/usr/bin/env python3
"""Mechanical program-term pinning and concrete precondition witnesses."""

from __future__ import annotations

import ast
import hashlib
import importlib.util
import symtable
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable


SCRATCH = Path("/tmp/audit-work/median47")
sys.path.insert(0, str(SCRATCH))
import py2mpy  # type: ignore  # Trusted mounted translator copied to scratch.


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load_function(path: Path, name: str) -> Callable[[list], Any]:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.median


def expected_program_k() -> tuple[str, str, str]:
    source_path = SCRATCH / "solution.py"
    source = source_path.read_text()
    tree = ast.parse(source, filename=str(source_path))
    assert len(tree.body) == 1 and isinstance(tree.body[0], ast.FunctionDef)
    function = tree.body[0]
    assert function.name == "median"
    py2mpy.SCOPES.clear()
    py2mpy._walk_symtable(symtable.symtable(source, str(source_path), "exec"))
    term = py2mpy.emit_stmt(function)
    assert term.name == "FuncDef" and len(term.args) == 3
    assert term.args[0] == '"median"'
    params = term.args[1]
    body = term.args[2]
    assert params.name == "Params" and len(params.args) == 1
    assert params.args[0] == '"l"'
    param_text = py2mpy.render(params.args[0])
    body_text = py2mpy.render(body, 2)
    indented_body = "\n".join("      " + line for line in body_text.splitlines())
    expected = "\n".join(
        [
            'requires "reference-semantics/semantics.k"',
            "",
            "module MEDIAN-PROGRAM",
            "  imports MPY",
            "",
            '  syntax Val ::= "solutionMedianClosure" [function, total]',
            "  rule solutionMedianClosure",
            "    => closureVal(",
            f"      {param_text},",
            indented_body + ",",
            "      0)",
            "endmodule",
            "",
        ]
    )
    return expected, param_text, body_text


@dataclass(frozen=True)
class Witness:
    claim: str
    values: list[Any]
    center_types: tuple[type, type] | None
    rhs_k: str


def typename(value: Any) -> str:
    return type(value).__name__


def main() -> int:
    expected, parameter, body = expected_program_k()
    actual = (SCRATCH / "program.k").read_text()
    print(
        "PROGRAM_K_COMPARE "
        f"expected_sha256={sha256(expected.encode())} "
        f"actual_sha256={sha256(actual.encode())} byte_equal={expected == actual}"
    )
    print(
        f"CONSTRUCTOR_BINDING function=median parameter={parameter!r} "
        f"body_sha256={sha256(body.encode())} capture_env=0"
    )

    functions_semantics = (
        SCRATCH / "reference-semantics/semantics/functions.k"
    ).read_text()
    funcdef_bridge_fragments = [
        "FuncDef(F:String, Params(PNS:ParamNames), BODY:Stmts) => .K",
        "F <- closureVal(PNS, BODY, L)",
    ]
    bridge_present = all(
        fragment in functions_semantics for fragment in funcdef_bridge_fragments
    )
    print(
        f"SUPPLIED_FUNCDEF_BINDING_PATTERN_PRESENT={bridge_present} "
        f"fragments={funcdef_bridge_fragments}"
    )

    candidate = load_function(SCRATCH / "solution.py", "pin_candidate")
    canonical = load_function(SCRATCH / "canonical.py", "pin_canonical")
    witnesses = [
        Witness("median-odd", [3, 1, 2, 4, 5], None,
                "valSeqAt(sortVS(VS), (vsLen(sortVS(VS))-1)/2)"),
        Witness("median-even-int-int", [1, 3], (int, int),
                "divII(1 +Int 3, 2)"),
        Witness("median-even-int-bool", [0, True], (int, bool),
                "divII(0 +Int boolAsInt(true), 2)"),
        Witness("median-even-bool-int", [False, 2], (bool, int),
                "divII(boolAsInt(false) +Int 2, 2)"),
        Witness("median-even-bool-bool", [False, True], (bool, bool),
                "divII(boolAsInt(false) +Int boolAsInt(true), 2)"),
        Witness("median-even-float-float", [1.0, 3.0], (float, float),
                "divFloatIntV(addF(1.0, 3.0), 2)"),
        Witness("median-even-int-float", [1, 2.0], (int, float),
                "divFloatIntV(addF(intToF(1), 2.0), 2)"),
        Witness("median-even-float-int", [1.5, 2], (float, int),
                "divFloatIntV(addF(1.5, intToF(2)), 2)"),
        Witness("median-even-bool-float", [False, 2.0], (bool, float),
                "divFloatIntV(addF(intToF(boolAsInt(false)), 2.0), 2)"),
        Witness("median-even-float-bool", [0.5, True], (float, bool),
                "divFloatIntV(addF(0.5, intToF(boolAsInt(true))), 2)"),
    ]

    witness_ok = True
    for witness in witnesses:
        sorted_values = sorted(witness.values)
        length = len(sorted_values)
        odd = length % 2 == 1
        if odd:
            center_pair = None
            expected_value = sorted_values[length // 2]
        else:
            centers = (
                sorted_values[length // 2 - 1],
                sorted_values[length // 2],
            )
            center_pair = (type(centers[0]), type(centers[1]))
            expected_value = (centers[0] + centers[1]) / 2
        candidate_value = candidate(list(witness.values))
        canonical_value = canonical(list(witness.values))
        types_match = (
            witness.center_types is None or center_pair == witness.center_types
        )
        result_match = candidate_value == expected_value == canonical_value
        fresh = 0 not in {}
        precondition = length > 0 and fresh and (
            (witness.center_types is None and odd)
            or (witness.center_types is not None and not odd and types_match)
        )
        witness_ok &= precondition and result_match
        print(
            f"WITNESS claim={witness.claim} VS={witness.values!r} "
            f"sort={sorted_values!r} length={length} parity={'odd' if odd else 'even'} "
            f"center_types={None if center_pair is None else tuple(t.__name__ for t in center_pair)} "
            f"HP={{}} HL=0 fresh={fresh} precondition={precondition} "
            f"rhs_k={witness.rhs_k!r} expected={expected_value!r} "
            f"candidate={candidate_value!r} canonical={canonical_value!r} "
            f"result_match={result_match}"
        )

    ok = expected == actual and bridge_present and witness_ok
    print(f"OVERALL_PINNING_AND_WITNESSES_OK={ok}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
