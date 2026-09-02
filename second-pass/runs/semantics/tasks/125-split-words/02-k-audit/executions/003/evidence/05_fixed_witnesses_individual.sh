#!/usr/bin/env bash
set -u
set -o pipefail

cd /tmp/audit-work/125-split-words

labels=(
  rule-1-false-boolean
  rule-2-true-boolean-discarded
  rule-3-true-boolean-discarded
  rule-4-false-boolean
  rule-5-true-boolean-discarded
)

for label in "${labels[@]}"; do
  echo "$ kprove fixed-false-witnesses.k --definition audit-fixed-kompiled --spec-module FIXED-FALSE-WITNESSES --claims FIXED-FALSE-WITNESSES.$label"
  kprove fixed-false-witnesses.k \
    --definition audit-fixed-kompiled \
    --spec-module FIXED-FALSE-WITNESSES \
    --claims "FIXED-FALSE-WITNESSES.$label"
  echo "${label}_fixed_exit=$?"
done
