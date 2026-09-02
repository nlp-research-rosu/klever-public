#!/usr/bin/env python3
"""Generate a material SFTest-body mutation and its expected-failing claim."""

from __future__ import annotations

import argparse
from pathlib import Path


parser = argparse.ArgumentParser()
parser.add_argument("kind", choices=("verification", "spec"))
args = parser.parse_args()

if args.kind == "verification":
    text = Path(
        "/tmp/audit-work/candidate-src/verification.k"
    ).read_text(encoding="utf-8")
    text = text.replace(
        "module VERIFICATION\n", "module VERIFICATION-BODY-MUTANT\n", 1
    )
    needle = 'If(Compare(Name("num"), CmpOp(">", Int(10))),'
    replacement = 'If(Compare(Name("num"), CmpOp(">", Int(100))),'
    assert text.count(needle) == 1
    text = text.replace(needle, replacement, 1)
    print(text, end="")
else:
    print(
        '''requires "verification-body-mutant.k"

module SPEC-BODY-MUTANT
  imports VERIFICATION-BODY-MUTANT

  claim [body-sensitive]: <py>
          <k> SFTest(ListExpr(Int(15), Int(-73), Int(14), Int(-15)))
              => intVal(1) </k>
          <functions> .Map </functions>
          <env> .Map </env>
        </py>
endmodule
'''
    )
