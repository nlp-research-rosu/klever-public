#!/usr/bin/env bash
set -u

export PATH="/home/agent/.nix-profile/bin:$PATH"
cd /tmp/audit-work/proof || exit 90

run() {
  printf '\nCOMMAND:'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf 'EXIT_STATUS: %s\n' "$status"
  return "$status"
}

printf '%s\n' "MUTATION: replace the result correctCodes(S,B) with notBool correctCodes(S,B)."
printf '%s\n' "FALSE_WITNESS: S=.IntSeq and B=0 satisfy B >=Int 0; execution returns true, while the mutated destination requires false."
run diff -u spec.k spec-audit-vacuity.k || true

run kprove spec-audit-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-AUDIT-VACUITY \
  --dry-run || exit $?

printf '%s\n' 'COMMAND: kprove spec-audit-vacuity.k --definition verification-kompiled --spec-module SPEC-AUDIT-VACUITY'
set +e
kprove spec-audit-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-AUDIT-VACUITY 2>&1 |
  tee /audit-output/evidence/stage6-vacuity-prover-raw.log
proof_status=${PIPESTATUS[0]}
set -e
printf 'EXIT_STATUS: %s\n' "$proof_status"
if test "$proof_status" -eq 0; then
  printf '%s\n' 'UNEXPECTED: false result mutation proved'
  exit 1
fi
run rg -n 'WarnStuckClaimState|implication check|cannot be rewritten further' \
  /audit-output/evidence/stage6-vacuity-prover-raw.log || exit $?
printf '%s\n' 'SUMMARY: mutation parsed successfully and failed on the expected unmet result implication'
