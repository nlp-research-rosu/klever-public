#!/usr/bin/env bash
set -u -o pipefail

SCRATCH=/tmp/audit-work/141-file-name-check
cd "$SCRATCH" || exit 1

run() {
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf '[exit %d]\n' "$status"
  return "$status"
}

run python3 /audit-output/evidence/04-compare-constructors.py || exit $?

run kprove \
  pinning-spec.k \
  --definition audit-verification-kompiled \
  --spec-module PINNING-SPEC \
  --warnings all || exit $?

run kprove \
  ground-validation-spec.k \
  --definition audit-verification-kompiled \
  --spec-module GROUND-VALIDATION-SPEC \
  --warnings all || exit $?

printf '\n$ diff -u verification.k verification-body-mutated.k\n'
diff -u verification.k verification-body-mutated.k
diff_status=$?
printf '[exit %d; expected difference]\n' "$diff_status"

run kompile \
  --backend haskell \
  verification-body-mutated.k \
  --main-module VERIFICATION-BODY-MUTATED \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-body-mutated-kompiled \
  --warnings none || exit $?

run kprove \
  spec-body-mutated.k \
  --definition audit-body-mutated-kompiled \
  --spec-module SPEC-BODY-MUTATED \
  --warnings all
mutation_status=$?
if [ "$mutation_status" -eq 0 ]; then
  printf 'BODY MUTATION UNEXPECTEDLY PROVED\n'
  exit 1
fi
printf 'BODY MUTATION REJECTED AS EXPECTED\n'
exit 0
