#!/usr/bin/env bash
set +e

record() {
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf 'EXIT: %d\n' "$status"
  return 0
}

src=/tmp/audit-work/47-median/candidate-src
build=/tmp/audit-work/47-median/build
mkdir -p "$build"

record kompile "$src/semantic.k" \
  --main-module MEDIAN-SEMANTICS \
  --syntax-module MEDIAN-SYNTAX \
  --backend llvm \
  --output-definition "$build/concrete-kompiled"

record kompile "$src/semantic.k" \
  --main-module SEMANTIC \
  --syntax-module MEDIAN-SYNTAX \
  --backend haskell \
  --output-definition "$build/proof-kompiled"

record kprove "$src/spec-main-only.k" \
  --definition "$build/proof-kompiled" \
  --spec-module SPEC-MAIN-ONLY
record kprove "$src/spec-example-odd-only.k" \
  --definition "$build/proof-kompiled" \
  --spec-module SPEC-EXAMPLE-ODD-ONLY
record kprove "$src/spec-example-even-only.k" \
  --definition "$build/proof-kompiled" \
  --spec-module SPEC-EXAMPLE-EVEN-ONLY
record kprove "$src/spec.k" \
  --definition "$build/proof-kompiled" \
  --spec-module SPEC

record python3 /audit-output/evidence/semantics-differential.py
