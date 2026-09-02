#!/usr/bin/env bash
set -euo pipefail

# Regenerate the submitted constructor program with the fixed translator.
python3 py2mpy.py solution.py > solution.mpy

# Guard the constructor tree duplicated by the GcdDef/GcdBody proof macros.
python3 - <<'PY'
from pathlib import Path

actual = "".join(Path("solution.mpy").read_text().split())
expected = "".join("""Module(
  FuncDef("greatest_common_divisor", Params("a", "b"),
    Assign(Name("a"), Call(Name("abs"), Name("a")))
    Assign(Name("b"), Call(Name("abs"), Name("b")))
    While(Compare(Name("b"), CmpOp("!=", Int(0))),
      Assign(
        TupleExpr(Name("a"), Name("b")),
        TupleExpr(Name("b"), BinOp("%", Name("a"), Name("b")))))
    Return(Name("a"))))
""".split())
if actual != expected:
    raise SystemExit("solution.mpy no longer matches the program tree in verification.k")
PY

# Concrete LLVM definition and execution through the supplied semantics.
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled \
  --warnings none
python3 py2mpy.py concrete_tests.py > concrete_tests.mpy
krun concrete_tests.mpy --definition runtime-kompiled

# Symbolic definition: GCD-VERIFICATION imports MPY, not MPY-KRUN.
kompile verification.k \
  --backend haskell \
  --main-module GCD-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled \
  --warnings none

# Universal symbolic theorem.
kprove spec.k \
  --definition verification-kompiled \
  --spec-module GCD-SPEC \
  --claims euclid-step \
  --warnings none

kprove spec.k \
  --definition verification-kompiled \
  --spec-module GCD-SPEC \
  --claims program-correct \
  --warnings none

# Both exact-value claims supplied by the prompt.
kprove spec.k \
  --definition verification-kompiled \
  --spec-module GCD-SPEC \
  --claims example-3-5,example-25-15 \
  --warnings none
