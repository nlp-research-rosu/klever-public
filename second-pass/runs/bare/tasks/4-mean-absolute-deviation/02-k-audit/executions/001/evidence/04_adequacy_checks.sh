#!/usr/bin/env bash
set -u

scratch=/tmp/audit-work/reconstruction

run() {
  local description="$1"
  shift
  printf '\nCOMMAND (%s):' "$description"
  printf ' %q' "$@"
  printf '\n'
  "$@"
  local status=$?
  printf 'EXIT STATUS: %d\n' "$status"
  return "$status"
}

printf 'AUDIT STAGE 4: adequacy and real-program pinning\n'

run "copy reviewer-authored ground claims and parsed claim-program AST" \
  cp \
    /audit-output/evidence/04_ground_spec.k \
    /audit-output/evidence/04_claimProgram.mpy \
    "$scratch/"
copy_status=$?

printf '\nCOMMAND (run submitted solution.mpy for pinning comparison): krun solution.mpy --definition verification-kompiled -cARGS=%q\n' \
  'nums(rat(1,1),rat(2,1),rat(3,1),rat(4,1))'
(
  cd "$scratch" &&
  krun solution.mpy \
    --definition verification-kompiled \
    -cARGS='nums(rat(1,1),rat(2,1),rat(3,1),rat(4,1))'
) > /tmp/audit-work/actual-program-run.txt 2>&1
actual_status=$?
sed -n '1,200p' /tmp/audit-work/actual-program-run.txt
printf 'EXIT STATUS: %d\n' "$actual_status"

printf '\nCOMMAND (run parsed AST corresponding to solutionProgram RHS): krun 04_claimProgram.mpy --definition verification-kompiled -cARGS=%q\n' \
  'nums(rat(1,1),rat(2,1),rat(3,1),rat(4,1))'
(
  cd "$scratch" &&
  krun 04_claimProgram.mpy \
    --definition verification-kompiled \
    -cARGS='nums(rat(1,1),rat(2,1),rat(3,1),rat(4,1))'
) > /tmp/audit-work/claim-program-run.txt 2>&1
claim_program_status=$?
sed -n '1,200p' /tmp/audit-work/claim-program-run.txt
printf 'EXIT STATUS: %d\n' "$claim_program_status"

run "submitted file execution equals claim-term execution" \
  cmp -s \
    /tmp/audit-work/actual-program-run.txt \
    /tmp/audit-work/claim-program-run.txt
pinning_status=$?

run "prove two concrete satisfying substitutions with direct result terms" \
  kprove "$scratch/04_ground_spec.k" \
    --definition "$scratch/verification-kompiled" \
    --spec-module GROUND-SPEC
ground_status=$?

run "show exact submitted MPY and verification AST for manual byte-level audit" \
  diff -u \
    <(sed -n '1,200p' "$scratch/solution.mpy") \
    <(sed -n '8,24p' "$scratch/verification.k")
ast_diff_status=$?
printf 'NOTE: the preceding textual diff is expected because verification.k wraps the same constructor tree in a function rule and uses different indentation.\n'

printf '\nSTAGE STATUS SUMMARY\n'
printf 'copy=%d actual_run=%d claim_term_run=%d pinning_cmp=%d ground_claims=%d textual_wrapper_diff=%d\n' \
  "$copy_status" "$actual_status" "$claim_program_status" "$pinning_status" \
  "$ground_status" "$ast_diff_status"

if (( copy_status || actual_status || claim_program_status || pinning_status || ground_status )); then
  exit 1
fi
