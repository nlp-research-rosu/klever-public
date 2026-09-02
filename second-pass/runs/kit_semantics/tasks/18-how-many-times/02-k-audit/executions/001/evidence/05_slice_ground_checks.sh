#!/usr/bin/env bash
set -u

cd /tmp/audit-work/review/candidate-src
cp /audit-output/evidence/05_slice_ground_good.k audit-slice-ground-good.k
cp /audit-output/evidence/05_slice_ground_bad.k audit-slice-ground-bad.k

printf '%s\n' \
  'COMMAND: kprove audit-slice-ground-good.k --definition audit-lemma-kompiled --spec-module AUDIT-SLICE-GROUND-GOOD'
kprove audit-slice-ground-good.k \
  --definition audit-lemma-kompiled \
  --spec-module AUDIT-SLICE-GROUND-GOOD
good_status=$?
printf 'GOOD_GROUND_SLICE_EXIT=%s\n' "$good_status"

printf '%s\n' \
  'COMMAND: kprove audit-slice-ground-bad.k --definition audit-lemma-kompiled --spec-module AUDIT-SLICE-GROUND-BAD'
kprove audit-slice-ground-bad.k \
  --definition audit-lemma-kompiled \
  --spec-module AUDIT-SLICE-GROUND-BAD
bad_status=$?
printf 'BAD_GROUND_SLICE_EXIT=%s\n' "$bad_status"

if [ "$good_status" -ne 0 ]; then
  exit 1
fi
if [ "$bad_status" -eq 0 ]; then
  printf 'ERROR: wrong opposite slice result proved\n'
  exit 1
fi
printf 'EXPECTED_BAD_GROUND_REJECTION=1\n'
