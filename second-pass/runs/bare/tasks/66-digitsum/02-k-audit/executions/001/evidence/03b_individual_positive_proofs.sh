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

cd /tmp/audit-work/reconstruction || exit 125
run cp /audit-output/evidence/spec-labeled.k spec-labeled.k

# First prove the invariant claim by itself.
run timeout 180s kprove spec-labeled.k \
  --definition audit-proof-haskell-kompiled \
  --spec-module SPEC-LABELED \
  --claims SPEC-LABELED.loop

# Then prove only the entry target while admitting the already-proved loop
# invariant as its explicit supporting lemma.
run timeout 180s kprove spec-labeled.k \
  --definition audit-proof-haskell-kompiled \
  --spec-module SPEC-LABELED \
  --claims SPEC-LABELED.entry,SPEC-LABELED.loop \
  --trusted SPEC-LABELED.loop
