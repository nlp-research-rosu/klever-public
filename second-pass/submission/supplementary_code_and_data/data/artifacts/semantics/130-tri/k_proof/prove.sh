#!/usr/bin/env bash
set -euo pipefail

python3 py2mpy.py solution.py > solution.mpy

kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled

smoke_file="$(mktemp ./tri-smoke.XXXXXX.mpy)"
trap 'rm -f -- "$smoke_file"' EXIT
{
  sed '$s/)$//' solution.mpy
  printf '%s\n' \
    '  Assert(Compare(Call(Name("tri"), Int(0)), CmpOp("==", ListExpr(Int(1)))))' \
    '  Assert(Compare(Call(Name("tri"), Int(3)), CmpOp("==", ListExpr(Int(1), Int(3), Int(2), Int(8)))))' \
    '  Assert(Compare(Call(Name("tri"), Int(10)), CmpOp("==", ListExpr(Int(1), Int(3), Int(2), Int(8), Int(3), Int(15), Int(4), Int(24), Int(5), Int(35), Int(6)))))' \
    ')'
} > "$smoke_file"
krun "$smoke_file" --definition runtime-kompiled --output none

kompile verification.k \
  --backend haskell \
  --main-module TRI-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled

kprove spec.k \
  --definition verification-kompiled \
  --spec-module TRI-LOOP-SPEC \
  --output pretty

kprove spec.k \
  --definition verification-kompiled \
  --spec-module TRI-CORRECT-SPEC \
  --output pretty
