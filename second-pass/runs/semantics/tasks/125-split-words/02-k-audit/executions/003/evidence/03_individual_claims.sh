#!/usr/bin/env bash
set -u
set -o pipefail

cd /tmp/audit-work/125-split-words

for label in whitespace comma odd-lowercase-count; do
  echo "$ kprove spec.k --definition audit-verification-kompiled --spec-module SPEC --claims SPEC.$label"
  kprove spec.k \
    --definition audit-verification-kompiled \
    --spec-module SPEC \
    --claims "SPEC.$label"
  echo "SPEC.${label}_kprove_exit=$?"
done
