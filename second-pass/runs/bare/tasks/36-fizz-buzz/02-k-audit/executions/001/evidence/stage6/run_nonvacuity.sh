#!/usr/bin/env bash
set -u

SOURCE=/tmp/audit-work/source
PROOF_DEF=/tmp/audit-work/reconstruction/verification-haskell

run_shell() {
  local command_text="$1"
  printf 'COMMAND: %s\n' "$command_text"
  bash -o pipefail -c "$command_text"
  local status=$?
  printf 'EXIT_STATUS: %s\n\n' "$status"
  return "$status"
}

run_shell "cp /audit-output/evidence/stage6/spec-vacuity.k '$SOURCE/spec-vacuity.k'"

printf 'SATISFYING FALSE WITNESS\n'
printf '%s\n' \
  'N=79 satisfies the entry claim (which has no requires clause).' \
  'Both trusted canonical.py and submitted solution.py return 3.' \
  'The fresh mutation requires result fizzFrom(0,79)+1 = 4.'
run_shell "python3 /audit-output/evidence/stage3/compare_concrete.py 79"
witness_status=$?

printf 'MUTATION PARSE/BUILD CHECK (NO PROOF EXECUTION)\n'
run_shell "cd '$SOURCE' && kprove spec-vacuity.k --definition '$PROOF_DEF' --spec-module SPEC-VACUITY --trusted SPEC-VACUITY.inner,SPEC-VACUITY.outer --dry-run"
dry_status=$?
if [[ $dry_status -ne 0 ]]; then
  exit 1
fi

printf 'EXPECTED PROOF FAILURE ON THE FALSE RESULT OBLIGATION\n'
command_text="cd '$SOURCE' && timeout 60s kprove spec-vacuity.k --definition '$PROOF_DEF' --spec-module SPEC-VACUITY --trusted SPEC-VACUITY.inner,SPEC-VACUITY.outer"
printf 'COMMAND: %s\n' "$command_text"
proof_output=$(bash -o pipefail -c "$command_text" 2>&1)
proof_status=$?
printf '%s\n' "$proof_output"
printf 'EXIT_STATUS: %s\n' "$proof_status"

if printf '%s\n' "$proof_output" | rg -q 'WarnStuckClaimState'; then
  stuck_status=0
else
  stuck_status=1
fi
if printf '%s\n' "$proof_output" | rg -q 'fizzFrom|\\+Int'; then
  obligation_status=0
else
  obligation_status=1
fi
printf 'EXPECTED_STUCK_RESIDUAL_PRESENT: %s\n' "$((1 - stuck_status))"
printf 'RESULT_OBLIGATION_VISIBLE: %s\n' "$((1 - obligation_status))"
printf 'SUMMARY witness=%s dry=%s proof=%s stuck=%s obligation=%s\n' \
  "$witness_status" "$dry_status" "$proof_status" "$stuck_status" "$obligation_status"

if [[ $witness_status -ne 0 || $proof_status -eq 0 || $proof_status -eq 124 || $stuck_status -ne 0 || $obligation_status -ne 0 ]]; then
  exit 1
fi
exit 0

