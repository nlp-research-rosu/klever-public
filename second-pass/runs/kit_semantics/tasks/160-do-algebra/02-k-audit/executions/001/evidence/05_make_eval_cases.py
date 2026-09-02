#!/usr/bin/env python3
"""Generate bounded concrete K-vs-Python evaluator bridge cases in scratch."""

from __future__ import annotations

import json
import random
from pathlib import Path


scratch = Path("/tmp/audit-work/160-do-algebra")
rng = random.Random(0x160E0A1)
alphabet = ["+", "-", "*", "//", "**"]
cases: list[tuple[list[str], list[int], int]] = [
    (["+", "*", "-"], [2, 3, 4, 5], 9),
    (["**", "**"], [2, 3, 2], 512),
    (["//"], [7, 3], 2),
    (["-"], [0, 7], -7),
]

while len(cases) < 44:
    count = rng.randint(1, 4)
    operators = [rng.choice(alphabet) for _ in range(count)]
    if any(left == right == "**" for left, right in zip(operators, operators[1:])):
        continue
    operands = [rng.randint(0, 5) for _ in range(count + 1)]
    expression = str(operands[0])
    for operator, operand in zip(operators, operands[1:]):
        expression += operator + str(operand)
    try:
        expected = eval(expression)
    except ZeroDivisionError:
        continue
    cases.append((operators, operands, expected))

source_lines = [
    "def do_algebra(operator, operand):",
    '    expression = ""',
    "    oprn = 0",
    '    oprt = ""',
    '    for oprn, oprt in zip(operand, operator + [""]):',
    "        expression += str(oprn) + oprt",
    "    return eval(expression)",
    "",
]
expected: dict[str, int] = {}
inputs: dict[str, dict[str, object]] = {}
for index, (operators, operands, result) in enumerate(cases):
    name = f"case_{index:03d}"
    source_lines.append(f"{name} = do_algebra({operators!r}, {operands!r})")
    expected[name] = result
    inputs[name] = {"operators": operators, "operands": operands}

(scratch / "05_eval_cases.py").write_text("\n".join(source_lines) + "\n")
(scratch / "05_eval_expected.json").write_text(
    json.dumps(expected, indent=2, sort_keys=True) + "\n"
)
Path("/audit-output/evidence/05_eval_inputs.json").write_text(
    json.dumps(inputs, indent=2, sort_keys=True) + "\n"
)
print(f"generated_cases={len(cases)}")
