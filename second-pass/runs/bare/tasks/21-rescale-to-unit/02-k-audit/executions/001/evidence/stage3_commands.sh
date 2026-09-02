#!/usr/bin/env bash
set +e

run() {
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf '[exit %d]\n' "$status"
  return 0
}

src=/tmp/audit-work/source
build=/tmp/audit-work/build

run mkdir -p "$build"
run rm -rf \
  "$build/semantic-kompiled" \
  "$build/verification-kompiled"
run find "$src" -maxdepth 1 -printf '%y %f\n'
run test ! -e "$src/semantic-kompiled"
run test ! -e "$src/verification-kompiled"

run kompile "$src/semantic.k" \
  --backend llvm \
  --main-module SEMANTIC \
  --syntax-module MPY-SYNTAX \
  --output-definition "$build/semantic-kompiled"

run kompile "$src/verification.k" \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition "$build/verification-kompiled"

run krun "$src/solution.mpy" \
  --definition "$build/semantic-kompiled" \
  -cARGS='vlist(1, 2, 3, 4, 5)' \
  --output pretty
run krun "$src/solution.mpy" \
  --definition "$build/semantic-kompiled" \
  -cARGS='vlist(8, -3)' \
  --output pretty
run krun "$src/solution.mpy" \
  --definition "$build/semantic-kompiled" \
  -cARGS='vlist(-5, -5, 0, 5, 5)' \
  --output pretty
run krun "$src/solution.mpy" \
  --definition "$build/semantic-kompiled" \
  -cARGS='vlist(1)' \
  --output pretty
run krun "$src/solution.mpy" \
  --definition "$build/semantic-kompiled" \
  -cARGS='vlist(2, 2)' \
  --output pretty
run krun "$src/solution.mpy" \
  --definition "$build/semantic-kompiled" \
  -cARGS='vlist()' \
  --output pretty
run python3 /audit-output/evidence/python_k_cases.py

for claim in c1 c2 c3 c4 c5 c6 c7; do
  run kprove "$src/spec-labeled.k" \
    --definition "$build/verification-kompiled" \
    --spec-module SPEC-LABELED \
    --claims "SPEC-LABELED.$claim"
done
