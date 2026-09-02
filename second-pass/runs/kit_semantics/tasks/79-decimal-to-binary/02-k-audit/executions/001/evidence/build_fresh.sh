#!/usr/bin/env bash
set -uo pipefail

scratch=/tmp/audit-work/79-audit/source
cd "$scratch" || exit 1

echo '$ kompile --version'
kompile --version
version_status=$?
echo "KOMPILE_VERSION_EXIT_STATUS=$version_status"

echo '$ kprove --version'
kprove --version
kprove_version_status=$?
echo "KPROVE_VERSION_EXIT_STATUS=$kprove_version_status"

echo '$ kompile reference-semantics/semantics.k --backend llvm --main-module MPY-KRUN --syntax-module MPY-SYNTAX --output-definition fresh-runtime-kompiled'
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition fresh-runtime-kompiled
llvm_status=$?
echo "LLVM_KOMPILE_EXIT_STATUS=$llvm_status"

echo '$ kompile verification.k --backend haskell --main-module VERIFICATION --syntax-module MPY-SYNTAX --output-definition fresh-verification-kompiled'
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition fresh-verification-kompiled
haskell_status=$?
echo "HASKELL_KOMPILE_EXIT_STATUS=$haskell_status"

if (( version_status || kprove_version_status || llvm_status || haskell_status )); then
  exit 1
fi
echo 'FRESH_BUILD=PASS'
