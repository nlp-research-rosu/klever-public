#!/usr/bin/env bash
set +e
set -x

cd /tmp/audit-work/source || exit 90

test ! -e /tmp/audit-work/concrete-kompiled
printf 'fresh concrete output path check exit: %s\n' "$?"
test ! -e /tmp/audit-work/proof-kompiled
printf 'fresh proof output path check exit: %s\n' "$?"

kompile semantic.k \
  --backend llvm \
  --main-module MPY-COMPILED \
  --syntax-module MPY-SYNTAX \
  --output-definition /tmp/audit-work/concrete-kompiled
llvm_build_exit=$?
printf 'fresh LLVM build exit: %s\n' "$llvm_build_exit"

kompile semantic.k \
  --backend haskell \
  --main-module MPY-COMPILED \
  --syntax-module MPY-SYNTAX \
  --output-definition /tmp/audit-work/proof-kompiled
haskell_build_exit=$?
printf 'fresh Haskell build exit: %s\n' "$haskell_build_exit"

if [ "$llvm_build_exit" -ne 0 ] || [ "$haskell_build_exit" -ne 0 ]; then
  exit 1
fi
exit 0
