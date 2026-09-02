#!/usr/bin/env bash
set -uo pipefail

cd /tmp/audit-work/candidate || exit 99
overall=0
proof_output=/tmp/audit-work/stage6-vacuity-proof.out

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

run cp /audit-output/evidence/spec-vacuity-audit.k \
  /tmp/audit-work/candidate/spec-vacuity-audit.k

run kprove spec-vacuity-audit.k \
  --definition verification-audit-kompiled \
  --spec-module ISCUBE-SPEC-VACUITY-AUDIT \
  --dry-run \
  --warnings all

printf '%s\n' 'SATISFYING_WITNESS: N=1, input=1; candidate Python returns True, mutated destination requires false.'
run python3 -c \
  'import solution; print("iscube(1)=", solution.iscube(1))'

printf '%s\n' 'COMMAND (expected unmet result obligation): kprove spec-vacuity-audit.k --definition verification-audit-kompiled --spec-module ISCUBE-SPEC-VACUITY-AUDIT --output pretty --warnings all'
kprove spec-vacuity-audit.k \
  --definition verification-audit-kompiled \
  --spec-module ISCUBE-SPEC-VACUITY-AUDIT \
  --output pretty \
  --warnings all 2>&1 | tee "$proof_output"
status=${PIPESTATUS[0]}
printf 'EXIT_STATUS: %s\n' "$status"
if (( status == 0 )); then
  overall=1
fi

if rg -q 'WarnStuckClaimState' "$proof_output"; then
  printf '%s\n' 'CHECK[WarnStuckClaimState]=present'
else
  printf '%s\n' 'CHECK[WarnStuckClaimState]=missing'
  overall=1
fi

if rg -q 'implication check between the conditions has failed|cannot be rewritten further' "$proof_output"; then
  printf '%s\n' 'CHECK[unmet_obligation_diagnostic]=present'
else
  printf '%s\n' 'CHECK[unmet_obligation_diagnostic]=missing'
  overall=1
fi

exit "$overall"
