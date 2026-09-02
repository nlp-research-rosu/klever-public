#!/usr/bin/env bash
set -u
cd /tmp/audit-work/body-mut-case || exit 125

printf '$ kompile verification.k --backend haskell --main-module CIRCULAR-SHIFT-VERIFICATION --syntax-module MPY-SYNTAX --output-definition body-mut-kompiled --warnings none\n'
kompile verification.k \
  --backend haskell \
  --main-module CIRCULAR-SHIFT-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition body-mut-kompiled \
  --warnings none
build_rc=$?
printf '[build exit %d]\n' "$build_rc"
if test "$build_rc" -ne 0; then
  exit 90
fi

printf '$ kprove --definition body-mut-kompiled --spec-module CIRCULAR-SHIFT-SPEC --claims CIRCULAR-SHIFT-SPEC.normal-shift --depth 300 --warnings none spec.k\n'
kprove \
  --definition body-mut-kompiled \
  --spec-module CIRCULAR-SHIFT-SPEC \
  --claims CIRCULAR-SHIFT-SPEC.normal-shift \
  --depth 300 \
  --warnings none \
  spec.k
proof_rc=$?
printf '[proof exit %d]\n' "$proof_rc"

if test "$proof_rc" -eq 0; then
  printf 'UNEXPECTED: the material body mutation still proved.\n'
  exit 91
fi
printf 'EXPECTED FAILURE: swapped suffix/prefix result obligation is not met by the unchanged program.\n'
exit 0
