#!/usr/bin/env bash
set -u
export PATH="/home/agent/.nix-profile/bin:$PATH"
work=/tmp/audit-work/candidate
definition="$work/verification-audit-kompiled"

run() {
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  local rc=$?
  printf 'EXIT: %d\n' "$rc"
  return "$rc"
}

printf '%s\n' 'SATISFYING WITNESS: LIST1 = .StrVals; LIST2 = pyStr("a") :: .StrVals; totals 0 < 1; actual result is pyList(.StrVals), not pyList(LIST2).'
run kprove "$work/spec-vacuity-audit.k" \
  --definition "$definition" \
  --spec-module SPEC-VACUITY-AUDIT \
  --claims SPEC-VACUITY-AUDIT.false-first-result \
  --dry-run || exit $?
printf '%s\n' 'MUTATION_DRY_RUN_BUILD_PASS'
run kprove "$work/spec-vacuity-audit.k" \
  --definition "$definition" \
  --spec-module SPEC-VACUITY-AUDIT \
  --claims SPEC-VACUITY-AUDIT.false-first-result
proof_rc=$?
if [[ "$proof_rc" -eq 0 ]]; then
  printf '%s\n' 'UNEXPECTED: false result mutation closed'
  exit 1
fi
printf '%s\n' 'EXPECTED_FALSE_POSTCONDITION_FAILURE'
