#!/usr/bin/env bash
set -u
cd /tmp/audit-work/source

printf '%s\n' 'WITNESS: input [1] satisfies the entry precondition; both Python implementations return [1], not [].'

printf '%s\n' 'COMMAND: kprove spec-vacuity.k --definition verification-kompiled --spec-module REVIEWER-SPEC-VACUITY --claims false_empty_for_singleton --dry-run'
kprove \
  spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module REVIEWER-SPEC-VACUITY \
  --claims false_empty_for_singleton \
  --dry-run
printf 'DRY_RUN_EXIT_STATUS: %s\n' "$?"

printf '%s\n' 'COMMAND: kprove spec-vacuity.k --definition verification-kompiled --spec-module REVIEWER-SPEC-VACUITY --claims false_empty_for_singleton'
kprove \
  spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module REVIEWER-SPEC-VACUITY \
  --claims false_empty_for_singleton
printf 'PROOF_EXIT_STATUS: %s\n' "$?"
