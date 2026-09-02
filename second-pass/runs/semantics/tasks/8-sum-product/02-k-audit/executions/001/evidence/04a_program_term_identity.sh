#!/usr/bin/env bash
set -u

WORK=/tmp/audit-work/reconstruction
cd "$WORK" || exit 99

run() {
  printf '\nCOMMAND:'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  rc=$?
  printf 'EXIT_STATUS: %d\n' "$rc"
  return 0
}

run cp /audit-output/evidence/sum-product-macro.mpy "$WORK/sum-product-macro.mpy"

printf 'COMMAND: kast solution.mpy --definition verification-kompiled --module SUM-PRODUCT-VERIFICATION --sort Module --expand-macros --output kore > actual-solution-term.kore\n'
kast solution.mpy --definition verification-kompiled \
  --module SUM-PRODUCT-VERIFICATION --sort Module --expand-macros --output kore \
  > actual-solution-term.kore
rc=$?
printf 'EXIT_STATUS: %d\n' "$rc"

printf 'COMMAND: kast sum-product-macro.mpy --definition verification-kompiled --module SUM-PRODUCT-VERIFICATION --sort Module --expand-macros --output kore > proof-macro-term.kore\n'
kast sum-product-macro.mpy --definition verification-kompiled \
  --module SUM-PRODUCT-VERIFICATION --sort Module --expand-macros --output kore \
  > proof-macro-term.kore
rc=$?
printf 'EXIT_STATUS: %d\n' "$rc"

run cmp actual-solution-term.kore proof-macro-term.kore
run sha256sum actual-solution-term.kore proof-macro-term.kore
