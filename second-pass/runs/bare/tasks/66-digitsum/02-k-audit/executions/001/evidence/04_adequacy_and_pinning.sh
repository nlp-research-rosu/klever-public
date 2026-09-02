#!/usr/bin/env bash
set -u

run() {
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf '[exit %d]\n' "$status"
  return 0
}

cd /tmp/audit-work/reconstruction || exit 125
run cp /audit-output/evidence/claimed-program.mpy claimed-program.mpy
run cp /audit-output/evidence/spec-ground.k spec-ground.k

printf '%s\n' '$ kast solution.mpy --definition audit-concrete-llvm-kompiled --output kast > submitted.kast'
kast solution.mpy \
  --definition audit-concrete-llvm-kompiled \
  --output kast > submitted.kast
printf '[exit %d]\n' "$?"

printf '%s\n' '$ kast claimed-program.mpy --definition audit-concrete-llvm-kompiled --output kast > claimed.kast'
kast claimed-program.mpy \
  --definition audit-concrete-llvm-kompiled \
  --output kast > claimed.kast
printf '[exit %d]\n' "$?"

run cmp -s submitted.kast claimed.kast
run sha256sum submitted.kast claimed.kast
run python3 /audit-output/evidence/adequacy_witnesses.py
run kprove spec-ground.k \
  --definition audit-proof-haskell-kompiled \
  --spec-module SPEC-GROUND
