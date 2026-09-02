#!/usr/bin/env bash
set -u
cd /tmp/audit-work/program-mut-case || exit 125

printf '$ kompile verification.k --backend haskell --main-module CIRCULAR-SHIFT-VERIFICATION --syntax-module MPY-SYNTAX --output-definition program-mut-kompiled --warnings none\n'
kompile verification.k \
  --backend haskell \
  --main-module CIRCULAR-SHIFT-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition program-mut-kompiled \
  --warnings none
build_rc=$?
printf '[build exit %d]\n' "$build_rc"
if test "$build_rc" -ne 0; then
  exit 90
fi

printf '$ kprove --definition program-mut-kompiled --spec-module CIRCULAR-SHIFT-SPEC --claims CIRCULAR-SHIFT-SPEC.normal-shift --depth 300 --warnings none spec.k\n'
kprove \
  --definition program-mut-kompiled \
  --spec-module CIRCULAR-SHIFT-SPEC \
  --claims CIRCULAR-SHIFT-SPEC.normal-shift \
  --depth 300 \
  --warnings none \
  spec.k
proof_rc=$?
printf '[proof exit %d]\n' "$proof_rc"

if test "$proof_rc" -eq 0; then
  printf 'UNEXPECTED: the swapped program body still proved.\n'
  exit 91
fi
printf 'EXPECTED FAILURE: swapped program execution does not meet the unchanged result function.\n'
exit 0
