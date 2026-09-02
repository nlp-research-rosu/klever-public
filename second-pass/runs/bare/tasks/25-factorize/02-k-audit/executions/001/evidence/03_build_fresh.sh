#!/usr/bin/env bash
set -uo pipefail

source_dir=/tmp/audit-work/25-factorize-audit/source
semantic_definition=/tmp/audit-work/25-factorize-audit/semantic-fresh-kompiled
verification_definition=/tmp/audit-work/25-factorize-audit/verification-fresh-kompiled

cd "$source_dir" || exit 1

echo "$ find /tmp/audit-work/25-factorize-audit -maxdepth 1 -name '*kompiled' -print"
find /tmp/audit-work/25-factorize-audit -maxdepth 1 -name '*kompiled' -print
printf '[exit_status=%d]\n' "$?"

echo "$ kompile semantic.k --backend haskell --main-module SEMANTIC --syntax-module MPY-SYNTAX --output-definition $semantic_definition"
kompile semantic.k \
  --backend haskell \
  --main-module SEMANTIC \
  --syntax-module MPY-SYNTAX \
  --output-definition "$semantic_definition"
status=$?
printf '[exit_status=%d]\n' "$status"
if (( status != 0 )); then
  exit "$status"
fi

echo "$ kompile verification.k --backend haskell --main-module VERIFICATION --syntax-module MPY-SYNTAX --output-definition $verification_definition"
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition "$verification_definition"
status=$?
printf '[exit_status=%d]\n' "$status"
exit "$status"

