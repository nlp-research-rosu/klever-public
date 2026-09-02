#!/usr/bin/env bash
set -u
cd /tmp/audit-work/no-abstraction-case || exit 125

printf '$ kompile verification.k --backend haskell --main-module CIRCULAR-SHIFT-VERIFICATION --syntax-module MPY-SYNTAX --output-definition no-abstraction-kompiled --warnings none\n'
kompile verification.k \
  --backend haskell \
  --main-module CIRCULAR-SHIFT-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition no-abstraction-kompiled \
  --warnings none
build_rc=$?
printf '[build exit %d]\n' "$build_rc"
if test "$build_rc" -ne 0; then
  exit "$build_rc"
fi

printf '$ kprove --definition no-abstraction-kompiled --spec-module CIRCULAR-SHIFT-SPEC --claims CIRCULAR-SHIFT-SPEC.normal-shift --depth 300 --warnings none spec.k\n'
kprove \
  --definition no-abstraction-kompiled \
  --spec-module CIRCULAR-SHIFT-SPEC \
  --claims CIRCULAR-SHIFT-SPEC.normal-shift \
  --depth 300 \
  --warnings none \
  spec.k
proof_rc=$?
printf '[proof exit %d]\n' "$proof_rc"
exit "$proof_rc"
