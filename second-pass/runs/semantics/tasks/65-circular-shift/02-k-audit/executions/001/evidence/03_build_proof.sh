#!/usr/bin/env bash
set -u
cd /tmp/audit-work/case || exit 125

printf '$ kompile verification.k --backend haskell --main-module CIRCULAR-SHIFT-VERIFICATION --syntax-module MPY-SYNTAX --output-definition verification-kompiled --warnings none\n'
kompile verification.k \
  --backend haskell \
  --main-module CIRCULAR-SHIFT-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled \
  --warnings none
rc=$?
printf '[exit %d]\n' "$rc"
exit "$rc"
