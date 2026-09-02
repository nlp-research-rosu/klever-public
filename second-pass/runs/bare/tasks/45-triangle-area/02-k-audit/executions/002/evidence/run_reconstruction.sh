#!/usr/bin/env bash
set -u

run() {
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  local status=$?
  printf '[exit %d]\n' "$status"
  return "$status"
}

cd /tmp/audit-work/candidate || exit 1

run kompile --version
run kprove --version
run krun --version

run kompile semantic.k \
  --backend llvm \
  --main-module TINY-PYTHON \
  --syntax-module TINY-PYTHON-SYNTAX \
  --output-definition concrete-kompiled

run kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module TINY-PYTHON-SYNTAX \
  --output-definition proof-kompiled

run krun solution.mpy --definition concrete-kompiled '-cARGS=Args(5, 3)'
run krun solution.mpy --definition concrete-kompiled '-cARGS=Args(0, 0)'
run krun solution.mpy --definition concrete-kompiled '-cARGS=Args(-4, 3)'
run python3 /audit-output/evidence/concrete_compare.py

run kprove spec.k --definition proof-kompiled --spec-module SPEC
run kprove spec-positive-1.k --definition proof-kompiled --spec-module SPEC-POSITIVE-1
run kprove spec-positive-2.k --definition proof-kompiled --spec-module SPEC-POSITIVE-2
run kprove spec-positive-3.k --definition proof-kompiled --spec-module SPEC-POSITIVE-3
