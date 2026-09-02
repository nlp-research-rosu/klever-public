#!/usr/bin/env bash
set -u

overall=0
run() {
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf '[exit %d]\n' "$status"
  if (( status != 0 )); then overall=1; fi
}

printf 'Parser/build gate for fresh mutation:\n'
run /usr/bin/kprove \
  fresh-vacuity-spec.k \
  --definition verification-kompiled \
  --spec-module SEARCH-FRESH-VACUITY-SPEC \
  --dry-run

printf '\nFresh false-result proof (nonzero expected):\n'
printf '$ /usr/bin/kprove fresh-vacuity-spec.k --definition verification-kompiled --spec-module SEARCH-FRESH-VACUITY-SPEC\n'
/usr/bin/kprove \
  fresh-vacuity-spec.k \
  --definition verification-kompiled \
  --spec-module SEARCH-FRESH-VACUITY-SPEC \
  2>&1 | tee /audit-output/evidence/stage6_mutation_failure.log
status=${PIPESTATUS[0]}
printf '[exit %d; nonzero expected]\n' "$status"
if (( status == 0 )); then
  printf 'ERROR: false result mutation unexpectedly proved\n'
  overall=1
fi
if ! rg -q 'WarnStuckClaimState|implication check.*failed|cannot be rewritten further' \
     /audit-output/evidence/stage6_mutation_failure.log; then
  printf 'ERROR: meaningful unmet-obligation diagnostic absent\n'
  overall=1
fi

exit "$overall"
