#!/usr/bin/env bash
set -u

scratch=/tmp/audit-work/29-filter-by-prefix/candidate-src
evidence=/audit-output/evidence
status=0
export PATH="/home/agent/.nix-profile/bin:$PATH"

printf '%s\n' 'COMMAND: cp /audit-output/evidence/spec-loop-only.k /tmp/audit-work/29-filter-by-prefix/candidate-src/spec-loop-only.k'
cp "$evidence/spec-loop-only.k" "$scratch/spec-loop-only.k"
rc=$?
printf 'EXIT: %d\n\n' "$rc"
(( rc == 0 )) || status=1

printf '%s\n' 'COMMAND: cp /audit-output/evidence/spec-entry-only.k /tmp/audit-work/29-filter-by-prefix/candidate-src/spec-entry-only.k'
cp "$evidence/spec-entry-only.k" "$scratch/spec-entry-only.k"
rc=$?
printf 'EXIT: %d\n\n' "$rc"
(( rc == 0 )) || status=1

cd "$scratch" || exit 1

printf '%s\n' 'COMMAND: kprove spec-loop-only.k --definition verification-kompiled --spec-module FILTER-BY-PREFIX-LOOP-ONLY-SPEC'
kprove spec-loop-only.k \
  --definition verification-kompiled \
  --spec-module FILTER-BY-PREFIX-LOOP-ONLY-SPEC
rc=$?
printf 'EXIT: %d\n\n' "$rc"
(( rc == 0 )) || status=1

printf '%s\n' 'COMMAND: kprove spec-entry-only.k --definition verification-kompiled --spec-module FILTER-BY-PREFIX-ENTRY-ONLY-SPEC'
kprove spec-entry-only.k \
  --definition verification-kompiled \
  --spec-module FILTER-BY-PREFIX-ENTRY-ONLY-SPEC
rc=$?
printf 'EXIT: %d\n\n' "$rc"
(( rc == 0 )) || status=1

printf 'SCRIPT_EXIT: %d\n' "$status"
exit "$status"
