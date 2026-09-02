#!/usr/bin/env bash
set -uo pipefail

cd /tmp/audit-work/reconstruction || exit 99

run() {
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  local rc=$?
  printf '[exit %d]\n\n' "$rc"
}

printf 'Fresh-source precheck (no candidate-built definitions copied):\n'
run find . -maxdepth 1 -type d -name '*-kompiled*' -print
run kompile --version
run kprove --version

run kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled-audit

run krun smoke.mpy --definition runtime-kompiled-audit

run kompile verification.k \
  --backend haskell \
  --main-module SUM-TO-N-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled-audit

run kprove spec.k \
  --definition verification-kompiled-audit \
  --spec-module SUM-TO-N-SPEC
