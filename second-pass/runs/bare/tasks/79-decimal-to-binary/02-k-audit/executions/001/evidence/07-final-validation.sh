#!/usr/bin/env bash
set -u

overall=0
run() {
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf '[exit %d]\n' "$status"
  if [ "$status" -ne 0 ]; then overall=1; fi
}

run cmp /candidate/solution.py /tmp/audit-work/solution.py
run cmp /candidate/solution.mpy /tmp/audit-work/submitted-solution.mpy
run cmp /candidate/semantic.k /tmp/audit-work/source/semantic.k
run cmp /candidate/verification.k /tmp/audit-work/source/verification.k
run cmp /candidate/spec.k /tmp/audit-work/source/spec.k
run cmp /candidate/semantic.k /tmp/audit-work/build-concrete/semantic.k
run cmp /candidate/semantic.k /tmp/audit-work/build-proof/semantic.k
run cmp /candidate/verification.k /tmp/audit-work/build-proof/verification.k
run cmp /candidate/spec.k /tmp/audit-work/build-proof/spec.k
run cmp /reference/canonical.py /tmp/audit-work/canonical.py
run cmp /reference/prompt.py /tmp/audit-work/prompt.py
run cmp /reference/py2mpy.py /tmp/audit-work/py2mpy.py
run test -d /tmp/audit-work/build-concrete/concrete-kompiled
run test -d /tmp/audit-work/build-proof/verification-kompiled
run tail -n 2 /audit-output/REVIEW.md
run rg -n '^## [1-7]\.|^VERDICT:|^LEGITIMACY:' /audit-output/REVIEW.md

for log in /audit-output/evidence/0[1-6]-*.log; do
  run tail -n 2 "$log"
done

printf '[script exit %d]\n' "$overall"
exit "$overall"
