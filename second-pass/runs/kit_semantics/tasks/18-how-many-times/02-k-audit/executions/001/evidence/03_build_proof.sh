#!/usr/bin/env bash
set -u

cd /tmp/audit-work/review/candidate-src
printf 'PWD=%s\n' "$PWD"
printf '%s\n' \
  'COMMAND: kompile --backend haskell verification.k --main-module VERIFICATION --syntax-module MPY-SYNTAX --output-definition audit-verification-kompiled'
kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-verification-kompiled
status=$?
printf 'KOMPILE_PROOF_EXIT=%s\n' "$status"
exit "$status"
