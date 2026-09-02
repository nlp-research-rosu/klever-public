#!/usr/bin/env bash
set -u

run() {
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf '[exit %d]\n' "$status"
  return 0
}

run python3 /audit-output/evidence/05_encoding_witness.py
run kprove /tmp/audit-work/proof-162/spec-nonascii-witness.k \
  --definition /tmp/audit-work/proof-162/verification-kompiled \
  --spec-module SPEC-NONASCII-WITNESS
