#!/usr/bin/env bash
set -u

run() {
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  local rc=$?
  printf '[exit %d]\n' "$rc"
  return 0
}

run kompile --version
run kprove --version
run cmp -s /candidate/solution.py /tmp/audit-work/case/solution.py
run cmp -s /candidate/solution.mpy /tmp/audit-work/case/solution.mpy
run cmp -s /candidate/spec.k /tmp/audit-work/case/spec.k
run cmp -s /candidate/verification.k /tmp/audit-work/case/verification.k
run diff -r --no-dereference /candidate/reference-semantics /tmp/audit-work/case/reference-semantics

printf 'Proof/non-vacuity signals:\n'
run grep -aE '#Top|\\[exit [01]\\]|\\[build exit [01]\\]|\\[proof exit [01]\\]|WarnStuckClaimState|EXPECTED FAILURE' \
  /audit-output/evidence/03_prove_normal.log \
  /audit-output/evidence/03_prove_oversize.log \
  /audit-output/evidence/05_program_body_sensitivity.log \
  /audit-output/evidence/06_nonvacuity.log

printf 'Reviewer evidence manifest:\n'
run find /audit-output/evidence -maxdepth 1 -type f -printf '%f|%s\n'
