#!/usr/bin/env bash
set -u

scratch=/tmp/audit-work/29-filter-by-prefix/candidate-src
evidence=/audit-output/evidence
status=0
export PATH="/home/agent/.nix-profile/bin:$PATH"

printf '%s\n' 'WITNESS: INPUT=.StrList, PREFIX=iCons(97,.IntSeq); candidate and canonical both return [], while the mutation demands [str("a")].'

printf '%s\n' 'COMMAND: cp /audit-output/evidence/spec-vacuity.k /tmp/audit-work/29-filter-by-prefix/candidate-src/spec-vacuity.k'
cp "$evidence/spec-vacuity.k" "$scratch/spec-vacuity.k"
rc=$?
printf 'EXIT: %d\n\n' "$rc"
(( rc == 0 )) || status=1

cd "$scratch" || exit 1

printf '%s\n' 'COMMAND: kprove spec-vacuity.k --definition verification-kompiled --spec-module FILTER-BY-PREFIX-VACUITY-SPEC --dry-run > /tmp/audit-work/29-filter-by-prefix/vacuity.kore'
kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module FILTER-BY-PREFIX-VACUITY-SPEC \
  --dry-run \
  > /tmp/audit-work/29-filter-by-prefix/vacuity.kore
rc=$?
printf 'EXIT: %d\n\n' "$rc"
(( rc == 0 )) || status=1

printf '%s\n' 'COMMAND: kprove spec-vacuity.k --definition verification-kompiled --spec-module FILTER-BY-PREFIX-VACUITY-SPEC'
kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module FILTER-BY-PREFIX-VACUITY-SPEC
rc=$?
printf 'EXIT: %d\n' "$rc"
if (( rc == 0 )); then
  printf '%s\n' 'UNEXPECTED: false mutation proved.'
  status=1
else
  printf '%s\n' 'EXPECTED: false mutation was rejected.'
fi
printf '\n'

printf 'SCRIPT_EXIT: %d\n' "$status"
exit "$status"
