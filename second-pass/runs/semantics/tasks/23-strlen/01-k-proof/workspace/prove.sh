#!/usr/bin/env bash
set -euo pipefail

python3 py2mpy.py solution.py > solution.mpy

kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled

krun solution.mpy --definition runtime-kompiled

krun \
  --definition runtime-kompiled \
  -cPGM='Module(
    FuncDef(
      "strlen",
      Params("string"),
      Return(Call(Name("len"), Name("string")))
    )
    Assert(
      Compare(
        Call(Name("strlen"), Str("")),
        CmpOp("==", Int(0))
      )
    )
    Assert(
      Compare(
        Call(Name("strlen"), Str("abc")),
        CmpOp("==", Int(3))
      )
    )
    Assert(
      Compare(
        Call(Name("strlen"), Str("HumanEval")),
        CmpOp("==", Int(9))
      )
    )
  )'

kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled

kprove spec.k --definition verification-kompiled
