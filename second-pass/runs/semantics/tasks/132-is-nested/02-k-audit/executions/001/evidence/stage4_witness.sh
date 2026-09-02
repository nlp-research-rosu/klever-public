#!/usr/bin/env bash
set -u

run() {
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  local command_status=$?
  printf '[exit %d]\n' "$command_status"
  return 0
}

cd /tmp/audit-work/132-is-nested/source || exit 99

run python3 /audit-output/evidence/stage4_witness.py
run timeout 600s kprove \
  --definition verification-kompiled \
  --spec-module IS-NESTED-LOOP-WITNESS-SPEC \
  spec-witness.k
run timeout 600s kprove \
  --definition verification-with-lemma-kompiled \
  --spec-module IS-NESTED-ENTRY-WITNESS-SPEC \
  spec-witness.k
