#!/usr/bin/env bash
set -u

run() {
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf '[exit %d]\n' "$status"
  return "$status"
}

cd /tmp/audit-work/work || exit 2

printf 'The submitted theory has no constructor equality connecting intVals to vCons/.ValSeq.\n'
run kprove representation-gap.k \
  --definition verification-kompiled \
  --spec-module REPRESENTATION-GAP \
  --dry-run
run kprove representation-gap.k \
  --definition verification-kompiled \
  --spec-module REPRESENTATION-GAP \
  --claims REPRESENTATION-GAP.base-connection
run kprove representation-gap.k \
  --definition verification-kompiled \
  --spec-module REPRESENTATION-GAP \
  --claims REPRESENTATION-GAP.step-connection

printf '\nOperational bridge value-sensitivity: mutate yield I to yield I+1.\n'
run kompile verification-bridge-mutated.k \
  --backend haskell \
  --main-module MAX-ELEMENT-VERIFICATION-BRIDGE-MUTATED \
  --syntax-module MPY-SYNTAX \
  --output-definition bridge-mutated-kompiled
run kprove spec-bridge-mutated.k \
  --definition bridge-mutated-kompiled \
  --spec-module SPEC-BRIDGE-MUTATED
