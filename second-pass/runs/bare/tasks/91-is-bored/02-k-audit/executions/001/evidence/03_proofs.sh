#!/usr/bin/env bash
set -u

work=/tmp/audit-work/reconstruction
status=0

printf '%s\n' 'The audit-only labels change no claim term, precondition, or postcondition.'
printf '%s\n' 'COMMAND: diff -u spec.k spec-labelled.k'
(cd "$work" && diff -u spec.k spec-labelled.k)
code=$?
printf 'DIFF_EXIT (1 means expected label-only differences): %s\n' "$code"

for number in 1 2 3 4 5 6 7 8; do
  printf 'COMMAND: timeout 120s kprove spec-labelled.k --definition verification-fresh-kompiled --spec-module SPEC --claims SPEC.audit-%s\n' "$number"
  (
    cd "$work" &&
      timeout 120s kprove spec-labelled.k \
        --definition verification-fresh-kompiled \
        --spec-module SPEC \
        --claims "SPEC.audit-$number"
  )
  code=$?
  printf 'CLAIM audit-%s EXIT: %s\n' "$number" "$code"
  (( code == 0 )) || status=1
done

exit "$status"
