#!/usr/bin/env bash
set -u

scratch=/tmp/audit-work/29-filter-by-prefix/candidate-src
evidence=/audit-output/evidence
status=0
export PATH="/home/agent/.nix-profile/bin:$PATH"

printf '%s\n' 'COMMAND: cp /audit-output/evidence/spec-entry-with-proven-loop.k /tmp/audit-work/29-filter-by-prefix/candidate-src/spec-entry-with-proven-loop.k'
cp "$evidence/spec-entry-with-proven-loop.k" \
  "$scratch/spec-entry-with-proven-loop.k"
rc=$?
printf 'EXIT: %d\n\n' "$rc"
(( rc == 0 )) || status=1

cd "$scratch" || exit 1

printf '%s\n' 'COMMAND: kprove spec-entry-with-proven-loop.k --definition verification-kompiled --spec-module FILTER-BY-PREFIX-ENTRY-WITH-PROVEN-LOOP-SPEC'
kprove spec-entry-with-proven-loop.k \
  --definition verification-kompiled \
  --spec-module FILTER-BY-PREFIX-ENTRY-WITH-PROVEN-LOOP-SPEC
rc=$?
printf 'EXIT: %d\n\n' "$rc"
(( rc == 0 )) || status=1

printf 'SCRIPT_EXIT: %d\n' "$status"
exit "$status"
