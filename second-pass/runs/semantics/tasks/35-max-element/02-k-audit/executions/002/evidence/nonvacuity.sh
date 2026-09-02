#!/usr/bin/env bash
set -u

run() {
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf '[exit %d]\n' "$status"
  return "$status"
}

cd /tmp/audit-work/work || exit 2

printf 'Witness evaluation for false target: input [1,2,3], max=3, mutated target=4.\n'
run python3 -c 'import canonical, solution; x=[1,2,3]; a=canonical.max_element(x); b=solution.max_element(x); print("canonical",a,"candidate",b,"false_target",a+1); assert a == b == 3'

printf '\nDry run must compile the mutation successfully:\n'
run kprove spec-vacuity-audit.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY-AUDIT \
  --dry-run

printf '\nActual mutated proof must fail on the unmet off-by-one result:\n'
run kprove spec-vacuity-audit.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY-AUDIT
