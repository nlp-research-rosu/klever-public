#!/usr/bin/env bash
set -uo pipefail

run() {
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@" 2>&1
  local status=$?
  printf '[exit %d]\n' "$status"
  return "$status"
}

review=/audit-output/REVIEW.md
scratch=/tmp/audit-work/48-is-palindrome/source

run test "$(tail -n 2 "$review" | head -n 1)" = 'VERDICT: CONCERNS' || exit $?
run test "$(tail -n 1 "$review")" = 'LEGITIMACY: LEGIT' || exit $?
run test "$(rg -c '^## [1-7]\.' "$review")" = 7 || exit $?

for artifact in \
  prompt.py py2mpy.py solution.py solution.mpy semantic.k verification.k spec.k prove.sh
do
  run cmp -s "/candidate/$artifact" "$scratch/$artifact" || exit $?
done

run rg -n '^#Top$|proof_status=0|mismatch_count=2' \
  /audit-output/evidence/stage3_reconstruction.log \
  || exit $?
run rg -n '^#Top$|classification=runtime-input-encoding bridge limitation' \
  /audit-output/evidence/stage5_static_and_unicode_witness.log \
  || exit $?
run rg -n \
  'WarnStuckClaimState|mutation_build_success=true|mutation_expected_failure=true' \
  /audit-output/evidence/stage6_nonvacuity.log \
  || exit $?
run tail -n 2 "$review" || exit $?
run sha256sum "$review" || exit $?
