#!/usr/bin/env python3
"""Generate K wrappers and the exhaustive proof partition."""

from pathlib import Path


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


def k_string(value):
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def tuple_expr(values):
    items = ", ".join("Str(" + k_string(value) + ")" for value in values)
    if not items:
        items = ".Exprs"
    return "TupleExpr(" + items + ")"


def tuple_value(values):
    items = ", ".join(k_string(value) for value in values)
    if not items:
        items = ".StringValues"
    return "tupleValue(" + items + ")"


def claim(first, second, expected, requires=None):
    lines = [
        "  claim",
        "    <k> verifyBF(" + first + ", " + second + ") => .K </k>",
        '    <planet1> "" => ' + first + " </planet1>",
        '    <planet2> "" => ' + second + " </planet2>",
        "    <result> noResult => " + tuple_value(expected) + " </result>",
    ]
    if requires:
        lines.append("    requires " + requires)
    return "\n".join(lines)


mpy_lines = Path("solution.mpy").read_text(encoding="utf-8").rstrip().splitlines()
# The standalone program parser infers an empty Stmts list from `, )`. Inside
# a K rule, the term parser requires the explicit list unit.
for index, line in enumerate(mpy_lines):
    if (
        line.strip() == ")"
        and index > 0
        and mpy_lines[index - 1].rstrip().endswith(",")
    ):
        mpy_lines[index] = line[: len(line) - len(line.lstrip())] + ".Stmts)"
mpy = "\n".join(mpy_lines).replace("TupleExpr()", "TupleExpr(.Exprs)")
program_module = (
    'requires "semantic.k"\n\n'
    "module SOLUTION-PROGRAM\n"
    "  imports MPY-SYNTAX\n\n"
    '  syntax Program ::= "solutionProgram"\n'
    "  rule solutionProgram =>\n"
    + "\n".join("    " + line for line in mpy.splitlines())
    + "\n"
    "endmodule\n"
)
Path("solution-program.k").write_text(program_module, encoding="utf-8")

claims = []
for first_index, first in enumerate(PLANETS):
    for second_index, second in enumerate(PLANETS):
        lo = min(first_index, second_index) + 1
        hi = max(first_index, second_index)
        claims.append(
            claim(
                k_string(first),
                k_string(second),
                PLANETS[lo:hi],
            )
        )

not_a_planet_1 = " andBool ".join(
    "P1 =/=String " + k_string(planet) for planet in PLANETS
)
claims.append(claim("P1", "P2", (), not_a_planet_1))

not_a_planet_2 = " andBool ".join(
    "P2 =/=String " + k_string(planet) for planet in PLANETS
)
for first in PLANETS:
    claims.append(claim(k_string(first), "P2", (), not_a_planet_2))

spec = (
    'requires "verification.k"\n\n'
    "module BF-SPEC\n"
    "  imports VERIFICATION\n\n"
    + "\n\n".join(claims)
    + "\nendmodule\n"
)
Path("spec.k").write_text(spec, encoding="utf-8")

mutation_spec = (
    'requires "verification.k"\n\n'
    "module MUTATION-SPEC\n"
    "  imports VERIFICATION\n\n"
    + claim(
        k_string("Mercury"),
        k_string("Neptune"),
        (),
    )
    + "\nendmodule\n"
)
Path("mutation-spec.k").write_text(mutation_spec, encoding="utf-8")
