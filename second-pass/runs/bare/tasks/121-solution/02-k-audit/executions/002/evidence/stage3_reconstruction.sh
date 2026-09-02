#!/usr/bin/env bash
set -u

work=/tmp/audit-work/121-solution-audit/candidate
status=0

run() {
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  rc=$?
  printf '[exit %d]\n' "$rc"
  if [ "$rc" -ne 0 ]; then
    status=1
  fi
}

run command -v kompile
run kompile --version
run kprove --version
run test ! -e "$work/semantic-audit-kompiled"
run test ! -e "$work/verification-audit-kompiled"
run kompile "$work/semantic.k" \
  --main-module MPY \
  --syntax-module MPY-SYNTAX \
  --backend llvm \
  --output-definition "$work/semantic-audit-kompiled"
run python3 /audit-output/evidence/semantics_differential.py
run kompile "$work/verification.k" \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --backend haskell \
  --output-definition "$work/verification-audit-kompiled"

for label in \
  SPEC.example-one \
  SPEC.example-two \
  SPEC.example-three \
  SPEC.all-integer-lists
do
  run kprove "$work/spec.k" \
    --definition "$work/verification-audit-kompiled" \
    --spec-module SPEC \
    --claims "$label" \
    --smt-timeout 1000
done

run kprove "$work/spec.k" \
  --definition "$work/verification-audit-kompiled" \
  --spec-module SPEC \
  --smt-timeout 1000

exit "$status"
