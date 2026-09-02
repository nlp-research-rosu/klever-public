#!/usr/bin/env bash
set +e

run() {
  printf '\nCOMMAND:'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf 'EXIT_STATUS: %d\n' "$status"
}

run rg -n 'solution\.mpy|solutionModule|polyBody|findZeroBody' /candidate/spec.k /candidate/verification.k
run rg -n 'validPolynomial|bracketLow|bracketHigh|bisectLow|bisectHigh|approximatesZero|priority' /candidate/spec.k /candidate/verification.k
run rg -n '^\s*claim\b|^\s*rule\b|^\s*syntax\b' /candidate/spec.k /candidate/verification.k
run rg -n '^\s*requires\s+".*solution' /candidate/spec.k /candidate/verification.k
