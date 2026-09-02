#!/usr/bin/env python3
"""Generate mechanical pin and body-sensitivity artifacts from solution.mpy."""

from __future__ import annotations

import argparse
from pathlib import Path


PROGRAM_PATH = Path("/tmp/audit-work/candidate-src/solution.mpy")


def normalized_program(program: str) -> str:
    """Make the parser's omitted empty Stmts arguments explicit inside a rule."""
    import re

    normalized, replacements = re.subn(
        r",(\n[ \t]*)\)", r", .Stmts\1)", program
    )
    if replacements != 4:
        raise SystemExit(
            f"expected four omitted empty statement lists, got {replacements}"
        )
    return normalized


def pin_check(program: str) -> str:
    program = normalized_program(program)
    return f'''requires "verification.k"

module PIN-CHECK-SPEC
  imports VERIFICATION

  // The RHS below is read verbatim from the trusted-translator regeneration.
  claim <k>
          solutionProgram
          => {program.strip()}
        </k>
endmodule
'''


def body_mutation_definition(program: str) -> str:
    program = normalized_program(program)
    old = 'Return(Str("YES"))'
    prefix, separator, suffix = program.rpartition(old)
    if not separator or old in prefix or old in suffix:
        raise SystemExit("expected exactly one final YES return in solution.mpy")
    mutated = prefix + 'Return(Str("NO"))' + suffix
    return f'''requires "verification.k"

module BODY-MUTATION
  imports VERIFICATION

  syntax Program ::= "mutatedSolutionProgram" [function]
  // Material body mutation: the real final YES return is changed to NO.
  rule mutatedSolutionProgram => {mutated.strip()}
endmodule
'''


def body_mutation_spec() -> str:
    return '''requires "verification-body-mutation.k"

module BODY-MUTATION-SPEC
  imports BODY-MUTATION

  // Both intervals are [0,2], so the intersection length is the prime 2.
  // The mutated body returns NO, making this expected YES obligation false.
  claim <mpy>
          <k>
            mutatedSolutionProgram
            ~> runWith(
                 TupleExpr(Int(0), Int(2)),
                 TupleExpr(Int(0), Int(2)))
            => strVal("YES")
          </k>
          <functions> .Map => ?_FUNCTIONS:Map </functions>
          <env> .Map => ?_ENV:Map </env>
        </mpy>
endmodule
'''


parser = argparse.ArgumentParser()
parser.add_argument(
    "artifact", choices=["pin", "body-definition", "body-spec"]
)
arguments = parser.parse_args()
program_text = PROGRAM_PATH.read_text()

if arguments.artifact == "pin":
    print(pin_check(program_text), end="")
elif arguments.artifact == "body-definition":
    print(body_mutation_definition(program_text), end="")
else:
    print(body_mutation_spec(), end="")
