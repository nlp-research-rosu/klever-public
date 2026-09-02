#!/usr/bin/env python3
"""Generate a constructor-level equality claim from submitted solution.mpy.

This intentionally parses only the trusted translator's top-level shape for
this artifact: Module(FuncDef(name, Params(...), statements)).
"""

from __future__ import annotations

import re
from pathlib import Path


SOURCE = Path("/tmp/audit-work/65-circular-shift/solution.mpy")
OUTPUT = Path("/tmp/audit-work/65-circular-shift/audit-pinning.k")


def matching_open(text: str, close_index: int) -> int:
    depth = 0
    in_string = False
    escaped = False
    for index in range(close_index, -1, -1):
        char = text[index]
        if in_string:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
            continue
        if char == '"':
            in_string = True
        elif char == ")":
            depth += 1
        elif char == "(":
            depth -= 1
            if depth == 0:
                return index
    raise ValueError("unmatched closing parenthesis")


def main() -> None:
    text = SOURCE.read_text()
    compact = " ".join(text.split())
    outer = re.fullmatch(r'Module\(\s*(FuncDef\(.*\))\s*\)', compact)
    assert outer is not None, "solution.mpy is not one top-level FuncDef"
    function = outer.group(1)

    prefix = 'FuncDef("circular_shift", Params("x", "shift"), '
    assert function.startswith(prefix), "unexpected function name or parameters"
    assert function.endswith(")")
    body = function[len(prefix) : -1]

    # Check that the extracted suffix is a statement sequence, not a truncated
    # child. Both top-level statements must be balanced constructor terms.
    assert body.startswith("Assign(")
    assert ") Return(" in body
    assert body.endswith(")")
    matching_open(body, len(body) - 1)

    rendered = f'''requires "verification.k"

module AUDIT-PINNING
  imports VERIFICATION

  // Generated mechanically from the submitted solution.mpy FuncDef.
  claim [submitted-constructor-equality]:
    <k>
      circularShiftClosure
      => closureVal(
           ("x", "shift", .ParamNames),
           {body}
           .Stmts,
           0)
    </k>
endmodule
'''
    OUTPUT.write_text(rendered)
    print(f"source={SOURCE}")
    print(f"output={OUTPUT}")
    print(f"function_name=circular_shift")
    print('parameters=("x", "shift")')
    print(f"body={body}")
    print("PINNING_CLAIM_GENERATION: PASS")


if __name__ == "__main__":
    main()
