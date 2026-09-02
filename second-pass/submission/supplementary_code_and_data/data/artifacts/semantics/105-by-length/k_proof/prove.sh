#!/usr/bin/env bash
set -euo pipefail

# Recreate the submitted constructor term from the Python source.
python3 py2mpy.py solution.py > solution.mpy

# Concrete execution uses exactly the required LLVM main and syntax modules.
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled

# Add smoke-test assertions to the generated module without duplicating the
# implementation.  concrete-tests.mpy is a derived test artifact.
python3 - <<'PY'
from pathlib import Path
from random import Random


def integer(value):
    if value < 0:
        return f'UnaryOp("-", Int({-value}))'
    return f"Int({value})"


def integer_list(values):
    return "ListExpr(" + ", ".join(integer(value) for value in values) + ")"


def string_list(values):
    return "ListExpr(" + ", ".join(f'Str("{value}")' for value in values) + ")"


cases = [
    (
        [2, 1, 1, 4, 5, 8, 2, 3],
        ["Eight", "Five", "Four", "Three", "Two", "Two", "One", "One"],
    ),
    ([], []),
    ([1, -1, 55], ["One"]),
    ([9, 1, 10, 0, 9, 4], ["Nine", "Nine", "Four", "One"]),
]

# Deterministic differential coverage for MPY-SORT's trusted concrete leg.
words = {
    1: "One",
    2: "Two",
    3: "Three",
    4: "Four",
    5: "Five",
    6: "Six",
    7: "Seven",
    8: "Eight",
    9: "Nine",
}
random = Random(105)
for _ in range(24):
    arguments = [random.randint(-20, 30) for _ in range(random.randint(0, 12))]
    expected = [
        words[value]
        for value in sorted(
            (value for value in arguments if 1 <= value <= 9),
            reverse=True,
        )
    ]
    cases.append((arguments, expected))

program = Path("solution.mpy").read_text(encoding="utf-8").rstrip()
if not program.startswith("Module(") or not program.endswith(")"):
    raise SystemExit("solution.mpy is not a Module term")

claims = []
for arguments, expected in cases:
    claims.append(
        "Assert(Compare("
        f'Call(Name("by_length"), {integer_list(arguments)}), '
        f'CmpOp("==", {string_list(expected)})))'
    )

Path("concrete-tests.mpy").write_text(
    program[:-1] + "\n  " + "\n  ".join(claims) + ")\n",
    encoding="utf-8",
)
PY

krun concrete-tests.mpy \
  --definition runtime-kompiled \
  --output none

# The proof definition imports MPY (not MPY-KRUN / MPY-CONCRETE), as required.
kompile verification.k \
  --backend haskell \
  --main-module BY-LENGTH-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled

kprove spec.k \
  --definition verification-kompiled \
  --spec-module BY-LENGTH-SPEC
