#!/usr/bin/env bash
set -u

work=/tmp/audit-work/92-any-int
src="$work/src"
log=/audit-output/evidence/03_reconstruct.log
failures=0
exec > >(tee "$log") 2>&1

run() {
  printf '\nCOMMAND:'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf 'EXIT_STATUS: %d\n' "$status"
  if [ "$status" -ne 0 ]; then
    failures=$((failures + 1))
  fi
  return 0
}

capture() {
  output=$1
  shift
  printf '\nCOMMAND:'
  printf ' %q' "$@"
  printf ' > %q\n' "$output"
  "$@" >"$output"
  status=$?
  printf 'EXIT_STATUS: %d\n' "$status"
  if [ "$status" -ne 0 ]; then
    failures=$((failures + 1))
  fi
  return 0
}

printf 'AUDIT_STAGE: 3 clean reconstruction\n'
run kompile --version
run kprove --version
run rm -rf -- "$work/concrete-kompiled" "$work/proof-kompiled"
run kompile "$src/verification.k" \
  --backend llvm \
  --main-module ANY-INT-VERIFICATION \
  --syntax-module ANY-INT-VERIFICATION \
  --output-definition "$work/concrete-kompiled"
run kompile "$src/verification.k" \
  --backend haskell \
  --main-module ANY-INT-VERIFICATION \
  --syntax-module ANY-INT-VERIFICATION \
  --output-definition "$work/proof-kompiled"

capture "$work/generated/submitted-program.kore" \
  kast -d "$work/proof-kompiled" \
  -m ANY-INT-VERIFICATION -s Program \
  --expand-macros -o kore "$src/solution.mpy"
capture "$work/generated/wrapper-program.kore" \
  kast -d "$work/proof-kompiled" \
  -m ANY-INT-VERIFICATION -s Program \
  --expand-macros -o kore -e solutionProgram
run cmp -s "$work/generated/submitted-program.kore" "$work/generated/wrapper-program.kore"
run sha256sum "$work/generated/submitted-program.kore" "$work/generated/wrapper-program.kore"

run python3 /audit-output/evidence/03_k_concrete_compare.py

run kprove "$src/spec.k" \
  --definition "$work/proof-kompiled" \
  --spec-module ANY-INT-SPEC

for label in int-first int-second int-third int-none nonint-first nonint-second nonint-third; do
  run kprove "$src/spec-individual.k" \
    --definition "$work/proof-kompiled" \
    --spec-module ANY-INT-SPEC-INDIVIDUAL \
    --claims "ANY-INT-SPEC-INDIVIDUAL.$label"
done

printf '\nESSENTIAL_FAILURES: %d\n' "$failures"
if [ "$failures" -ne 0 ]; then
  exit 1
fi
