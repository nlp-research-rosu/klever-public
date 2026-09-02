#!/usr/bin/env bash
set -uo pipefail

cd /tmp/audit-work/candidate || exit 99
overall=0

run() {
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf 'EXIT_STATUS: %s\n' "$status"
  if (( status != 0 )); then
    overall=1
  fi
}

run kompile --version
run kprove --version

for generated in runtime-audit-kompiled verification-audit-kompiled; do
  if [[ -e "$generated" ]]; then
    printf 'PREEXISTING_BUILD_ARTIFACT: %s\n' "$generated"
    overall=1
  else
    printf 'PREEXISTING_BUILD_ARTIFACT: %s absent\n' "$generated"
  fi
done

run kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-audit-kompiled

run krun solution.mpy \
  --definition runtime-audit-kompiled \
  --output none

run krun concrete_tests.mpy \
  --definition runtime-audit-kompiled \
  --output none

run kompile verification.k \
  --backend haskell \
  --main-module ISCube-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-audit-kompiled \
  -I .

run kprove spec.k \
  --definition verification-audit-kompiled \
  --spec-module ISCube-SPEC \
  --output pretty \
  --warnings none

for claim in \
  ISCube-SPEC.implementation \
  ISCube-SPEC.positive-cubes \
  ISCube-SPEC.negative-cubes \
  ISCube-SPEC.positive-noncubes \
  ISCube-SPEC.negative-noncubes
do
  run kprove spec.k \
    --definition verification-audit-kompiled \
    --spec-module ISCube-SPEC \
    --claims "$claim" \
    --output pretty \
    --warnings none
done

exit "$overall"
