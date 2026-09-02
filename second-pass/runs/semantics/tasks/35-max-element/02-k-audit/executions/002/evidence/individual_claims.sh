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
printf 'Corrected claim filtering: declarations now use claim [name]: syntax.\n'

run kprove spec-labeled.k \
  --definition verification-kompiled \
  --spec-module MAX-ELEMENT-SPEC-LABELED \
  --claims MAX-ELEMENT-SPEC-LABELED.fold

run kprove spec-labeled.k \
  --definition verification-kompiled \
  --spec-module MAX-ELEMENT-SPEC-LABELED \
  --claims MAX-ELEMENT-SPEC-LABELED.example-one

run kprove spec-labeled.k \
  --definition verification-kompiled \
  --spec-module MAX-ELEMENT-SPEC-LABELED \
  --claims MAX-ELEMENT-SPEC-LABELED.example-two

printf '\nThe universal target uses the fold claim as its circularity/lemma;\n'
printf 'select both exact claims together.\n'
run kprove spec-labeled.k \
  --definition verification-kompiled \
  --spec-module MAX-ELEMENT-SPEC-LABELED \
  --claims MAX-ELEMENT-SPEC-LABELED.fold,MAX-ELEMENT-SPEC-LABELED.universal
