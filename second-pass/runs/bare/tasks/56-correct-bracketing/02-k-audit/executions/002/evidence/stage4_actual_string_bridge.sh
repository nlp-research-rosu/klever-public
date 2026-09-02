#!/usr/bin/env bash
set -uo pipefail

cd /tmp/audit-work/proof || exit 90

printf 'COMMAND: kompile bridge-definition.k --backend haskell --main-module BRIDGE-DEFINITION --syntax-module MPY-SYNTAX --output-definition bridge-haskell-kompiled\n'
kompile bridge-definition.k \
  --backend haskell \
  --main-module BRIDGE-DEFINITION \
  --syntax-module MPY-SYNTAX \
  --output-definition bridge-haskell-kompiled
build_exit=$?
printf 'bridge definition kompile exit=%s\n' "$build_exit"
if (( build_exit != 0 )); then
  exit 1
fi

printf 'COMMAND: kprove spec-actual-string-attempt.k --definition bridge-haskell-kompiled --spec-module SPEC-ACTUAL-STRING-ATTEMPT --claims SPEC-ACTUAL-STRING-ATTEMPT.actual-string-universal,SPEC-ACTUAL-STRING-ATTEMPT.loop-zero,SPEC-ACTUAL-STRING-ATTEMPT.loop-positive\n'
kprove spec-actual-string-attempt.k \
  --definition bridge-haskell-kompiled \
  --spec-module SPEC-ACTUAL-STRING-ATTEMPT \
  --claims \
  SPEC-ACTUAL-STRING-ATTEMPT.actual-string-universal,SPEC-ACTUAL-STRING-ATTEMPT.loop-zero,SPEC-ACTUAL-STRING-ATTEMPT.loop-positive
proof_exit=$?
printf 'actual-string universal proof exit=%s (nonzero expected: missing bridge)\n' \
  "$proof_exit"
if (( proof_exit == 0 )); then
  exit 1
fi
