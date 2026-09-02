#!/usr/bin/env bash
set -uo pipefail

scratch=/tmp/audit-work/68-pluck-audit
definition="$scratch/concrete-audit-kompiled"

echo '$ test ! -e concrete-audit-kompiled'
test ! -e "$definition"
clean_status=$?
echo "clean-start exit=$clean_status"
if (( clean_status != 0 )); then
  exit "$clean_status"
fi

echo '$ kompile --backend llvm semantic.k --main-module SEMANTIC --syntax-module MPY-SYNTAX --output-definition concrete-audit-kompiled'
kompile \
  --backend llvm \
  "$scratch/semantic.k" \
  --main-module SEMANTIC \
  --syntax-module MPY-SYNTAX \
  --output-definition "$definition"
status=$?
echo "kompile concrete exit=$status"
exit "$status"

