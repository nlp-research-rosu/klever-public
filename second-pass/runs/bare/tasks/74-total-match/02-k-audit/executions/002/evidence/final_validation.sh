#!/usr/bin/env bash
set -u
review=/audit-output/REVIEW.md

run() {
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  local rc=$?
  printf 'EXIT: %d\n' "$rc"
  return "$rc"
}

run test -s "$review" || exit $?
mapfile -t final_lines < <(tail -n 2 "$review")
printf 'FINAL_LINE_1: %s\n' "${final_lines[0]-}"
printf 'FINAL_LINE_2: %s\n' "${final_lines[1]-}"
[[ "${final_lines[0]-}" == 'VERDICT: FAIL' ]] || exit 1
[[ "${final_lines[1]-}" == 'LEGITIMACY: NOT_LEGIT' ]] || exit 1
run test "$(rg -c '^VERDICT:' "$review")" -eq 1 || exit $?
run test "$(rg -c '^LEGITIMACY:' "$review")" -eq 1 || exit $?
run test -z "$(find /audit-output/evidence -type l -print -quit)" || exit $?
run cmp -s /candidate/solution.py /tmp/audit-work/candidate/solution.py || exit $?
run cmp -s /candidate/solution.mpy /tmp/audit-work/candidate/solution.mpy || exit $?
run cmp -s /candidate/semantic.k /tmp/audit-work/candidate/semantic.k || exit $?
run cmp -s /candidate/verification.k /tmp/audit-work/candidate/verification.k || exit $?
run cmp -s /candidate/spec.k /tmp/audit-work/candidate/spec.k || exit $?
run sha256sum "$review" \
  /audit-output/evidence/04-integrity-and-trace-passed.log \
  /audit-output/evidence/06-differential-test.log \
  /audit-output/evidence/08-clean-build-passed.log \
  /audit-output/evidence/09-concrete-semantics.log \
  /audit-output/evidence/10-positive-claims.log \
  /audit-output/evidence/11-program-pinning.log \
  /audit-output/evidence/12-body-sensitivity.log \
  /audit-output/evidence/13-unicode-len-witness.log \
  /audit-output/evidence/14-static-inventory.log \
  /audit-output/evidence/15-nonvacuity-test.log
run wc -l "$review"
printf '%s\n' 'FINAL_ARTIFACT_VALIDATION_PASS'
