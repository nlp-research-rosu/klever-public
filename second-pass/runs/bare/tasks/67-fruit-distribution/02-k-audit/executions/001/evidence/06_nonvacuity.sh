#!/usr/bin/env bash
set -u

audit_failures=0

run_expect_zero() {
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf 'EXIT_STATUS: %d\n' "$status"
  if (( status != 0 )); then audit_failures=$((audit_failures + 1)); fi
}

printf 'MUTATION WITNESS: A=5 O=6 N=19; precondition=true; actual=8; mutated_expected=9\n'
run_expect_zero python3 -c \
  'from importlib.util import module_from_spec,spec_from_file_location; p="/tmp/audit-work/fresh/solution.py"; s=spec_from_file_location("mutation_candidate",p); m=module_from_spec(s); s.loader.exec_module(m); actual=m.fruit_distribution("5 apples and 6 oranges",19); print(f"actual={actual} mutated_expected=9 false={actual != 9}"); raise SystemExit(0 if actual != 9 else 1)'

run_expect_zero kprove spec-vacuity-audit.k \
  --definition audit-verification-kompiled \
  --spec-module SPEC-VACUITY-AUDIT \
  --dry-run

printf 'COMMAND: kprove spec-vacuity-audit.k --definition audit-verification-kompiled --spec-module SPEC-VACUITY-AUDIT\n'
mutation_output=$(kprove spec-vacuity-audit.k \
  --definition audit-verification-kompiled \
  --spec-module SPEC-VACUITY-AUDIT 2>&1)
mutation_status=$?
printf '%s\n' "$mutation_output"
printf 'EXIT_STATUS: %d\n' "$mutation_status"
if (( mutation_status == 0 )); then
  printf 'EXPECTED_NONZERO_NOT_OBSERVED\n'
  audit_failures=$((audit_failures + 1))
fi
if [[ "$mutation_output" == *"WarnStuckClaimState"* ]] \
   && [[ "$mutation_output" == *"implication check between the conditions has failed"* ]]; then
  printf 'EXPECTED_UNMET_OBLIGATION_CONFIRMED\n'
else
  printf 'EXPECTED_UNMET_OBLIGATION_NOT_CONFIRMED\n'
  audit_failures=$((audit_failures + 1))
fi

printf 'AUDIT_FAILURE_COUNT: %d\n' "$audit_failures"
exit "$audit_failures"
