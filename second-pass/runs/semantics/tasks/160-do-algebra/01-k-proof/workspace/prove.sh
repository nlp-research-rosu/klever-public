#!/usr/bin/env bash
set -euo pipefail

python3 py2mpy.py solution.py > solution.mpy

python3 - <<'PY'
from solution import do_algebra

assert do_algebra(["+", "*", "-"], [2, 3, 4, 5]) == 9
assert do_algebra(["-", "-"], [20, 5, 3]) == 12
assert do_algebra(["//", "//"], [20, 3, 2]) == 3
assert do_algebra(["**", "**"], [2, 3, 2]) == 512
assert do_algebra(["+", "*", "**", "//", "-"], [4, 3, 2, 3, 5, 1]) == 7
PY

kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled

{
  sed '$ s/)$//' solution.mpy
  printf '%s\n' \
    '  Assert(Compare(Call(Name("do_algebra"), ListExpr(Str("+"), Str("*"), Str("-")), ListExpr(Int(2), Int(3), Int(4), Int(5))), CmpOp("==", Int(9))))' \
    '  Assert(Compare(Call(Name("do_algebra"), ListExpr(Str("-"), Str("-")), ListExpr(Int(20), Int(5), Int(3))), CmpOp("==", Int(12))))' \
    '  Assert(Compare(Call(Name("do_algebra"), ListExpr(Str("//"), Str("//")), ListExpr(Int(20), Int(3), Int(2))), CmpOp("==", Int(3))))' \
    '  Assert(Compare(Call(Name("do_algebra"), ListExpr(Str("**"), Str("**")), ListExpr(Int(2), Int(3), Int(2))), CmpOp("==", Int(512))))' \
    '  Assert(Compare(Call(Name("do_algebra"), ListExpr(Str("+"), Str("*"), Str("**"), Str("//"), Str("-")), ListExpr(Int(4), Int(3), Int(2), Int(3), Int(5), Int(1))), CmpOp("==", Int(7))))'
  printf '%s\n' ')'
} > smoke.mpy

krun smoke.mpy --definition runtime-kompiled --output none

kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module VERIFICATION \
  --output-definition verification-kompiled

cmp \
  <(kast --definition verification-kompiled --module VERIFICATION \
      --sort Module --expand-macros --output kore solution.mpy) \
  <(kast --definition verification-kompiled --module VERIFICATION \
      --sort Module --expand-macros --output kore --expression solutionProgram)

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
