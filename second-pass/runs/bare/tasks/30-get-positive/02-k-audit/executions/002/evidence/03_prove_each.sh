#!/usr/bin/env bash
set -u

work=/tmp/audit-work/30-get-positive/candidate-src
cd "$work" || exit 90

overall=0
for claim in \
  VERIFICATION-LABELED.helper-positive-head \
  VERIFICATION-LABELED.helper-nonpositive-head \
  VERIFICATION-LABELED.helper-empty \
  SPEC-LABELED.universal \
  SPEC-LABELED.example-one \
  SPEC-LABELED.example-two \
  SPEC-LABELED.empty \
  SPEC-LABELED.all-nonpositive
do
  printf 'PROVE claim=%s\n' "$claim"
  kprove spec-labeled.k \
    --definition proof-kompiled \
    --spec-module SPEC-LABELED \
    --claims "$claim"
  status=$?
  printf 'STATUS claim=%s exit=%s\n' "$claim" "$status"
  if [ "$status" -ne 0 ]; then
    overall=1
  fi
done
exit "$overall"
