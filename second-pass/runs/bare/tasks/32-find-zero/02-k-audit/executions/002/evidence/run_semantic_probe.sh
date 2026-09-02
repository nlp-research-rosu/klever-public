#!/usr/bin/env bash
set -euo pipefail

probe=$1
semantic_definition=/tmp/audit-work/32-find-zero/semantic-concrete-haskell-kompiled
verification_definition=/tmp/audit-work/32-find-zero/verification-proof-kompiled

case "$probe" in
  compare-negative-denominator)
    definition=$semantic_definition
    term='Module(FuncDef("dummy", Params("x"), Return(Name("x")))) ;; Compare(rat(1, -1), CmpOp(">", rat(0, 1)))'
    ;;
  abs-negative-denominator)
    definition=$verification_definition
    term='Module(FuncDef("dummy", Params("x"), Return(Name("x")))) ;; absRat(rat(1, -1))'
    ;;
  le-negative-denominator)
    definition=$verification_definition
    term='Module(FuncDef("dummy", Params("x"), Return(Name("x")))) ;; bool(leRat(rat(1, -1), rat(0, 1)))'
    ;;
  total-add-non-rational)
    definition=$semantic_definition
    term='Module(FuncDef("dummy", Params("x"), Return(Name("x")))) ;; addRat(bool(true), rat(1, 1))'
    ;;
  total-make-zero-denominator)
    definition=$semantic_definition
    term='Module(FuncDef("dummy", Params("x"), Return(Name("x")))) ;; makeRat(1, 0)'
    ;;
  *)
    printf 'unknown probe: %s\n' "$probe" >&2
    exit 64
    ;;
esac

krun --definition "$definition" -cPGM="$term" --output pretty
