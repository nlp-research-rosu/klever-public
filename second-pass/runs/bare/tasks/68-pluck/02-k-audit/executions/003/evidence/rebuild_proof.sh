#!/usr/bin/env bash
set -uo pipefail

scratch=/tmp/audit-work/68-pluck-audit
definition="$scratch/proof-audit-kompiled"

echo '$ test ! -e proof-audit-kompiled'
test ! -e "$definition"
clean_status=$?
echo "clean-start exit=$clean_status"
if (( clean_status != 0 )); then
  exit "$clean_status"
fi

echo '$ kompile --backend haskell verification.k --main-module VERIFICATION --syntax-module MPY-SYNTAX --output-definition proof-audit-kompiled'
kompile \
  --backend haskell \
  "$scratch/verification.k" \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition "$definition"
status=$?
echo "kompile proof exit=$status"
exit "$status"

