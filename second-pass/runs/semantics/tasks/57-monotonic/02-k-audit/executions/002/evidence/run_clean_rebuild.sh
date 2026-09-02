#!/usr/bin/env bash
set -euo pipefail

scratch=/tmp/audit-work/candidate
build_root=/tmp/audit-work/fresh-build

run() {
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  set +e
  "$@"
  status=$?
  set -e
  printf 'EXIT_STATUS=%s\n' "$status"
  return "$status"
}

mkdir -p "$build_root"
cp /audit-output/evidence/spec-claim1.k "$scratch/spec-claim1.k"
cp /audit-output/evidence/spec-claim2.k "$scratch/spec-claim2.k"

run bash -c 'python3 "$1" "$2" > "$3"' _ \
  /reference/py2mpy.py "$scratch/solution.py" "$build_root/regenerated-solution.mpy"
run cmp "$build_root/regenerated-solution.mpy" "$scratch/solution.mpy"
run bash -c 'python3 "$1" "$2" > "$3"' _ \
  /reference/py2mpy.py /audit-output/evidence/concrete_program.py "$build_root/concrete-program.mpy"

run kompile "$scratch/reference-semantics/semantics.k" \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition "$build_root/runtime-kompiled"

run krun "$build_root/concrete-program.mpy" \
  --definition "$build_root/runtime-kompiled"

run kompile "$scratch/verification.k" \
  --backend haskell \
  --main-module MONOTONIC-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition "$build_root/verification-kompiled"

run kprove "$scratch/spec.k" \
  --definition "$build_root/verification-kompiled" \
  --spec-module MONOTONIC-SPEC

run kprove "$scratch/spec-claim1.k" \
  --definition "$build_root/verification-kompiled" \
  --spec-module MONOTONIC-SPEC-CLAIM1

run kprove "$scratch/spec-claim2.k" \
  --definition "$build_root/verification-kompiled" \
  --spec-module MONOTONIC-SPEC-CLAIM2

printf 'CLEAN_REBUILD=PASS\n'
