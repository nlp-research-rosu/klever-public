#!/usr/bin/env bash
set -u

cd /tmp/audit-work/candidate || exit 90

printf '%s\n' 'COMMAND: test ! -e /tmp/audit-work/concrete-kompiled'
test ! -e /tmp/audit-work/concrete-kompiled
status=$?
printf 'EXIT: %s\n\n' "$status"
if test "$status" -ne 0; then
  exit "$status"
fi

printf '%s\n' 'COMMAND: kompile --backend llvm semantic.k --main-module MPY --syntax-module MPY-SYNTAX --output-definition /tmp/audit-work/concrete-kompiled'
kompile --backend llvm semantic.k \
  --main-module MPY \
  --syntax-module MPY-SYNTAX \
  --output-definition /tmp/audit-work/concrete-kompiled
status=$?
printf 'EXIT: %s\n\n' "$status"
if test "$status" -ne 0; then
  exit "$status"
fi

printf '%s\n' 'COMMAND: test ! -e /tmp/audit-work/proof-kompiled'
test ! -e /tmp/audit-work/proof-kompiled
status=$?
printf 'EXIT: %s\n\n' "$status"
if test "$status" -ne 0; then
  exit "$status"
fi

printf '%s\n' 'COMMAND: kompile --backend haskell semantic.k --main-module SEMANTIC --syntax-module VERIFICATION --output-definition /tmp/audit-work/proof-kompiled'
kompile --backend haskell semantic.k \
  --main-module SEMANTIC \
  --syntax-module VERIFICATION \
  --output-definition /tmp/audit-work/proof-kompiled
status=$?
printf 'EXIT: %s\n' "$status"
exit "$status"
