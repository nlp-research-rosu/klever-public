#!/usr/bin/env bash
set -uo pipefail

cd /tmp/audit-work/proof || exit 90

printf 'COMMAND: kompile semantic.k --backend llvm --main-module MPY --syntax-module MPY-SYNTAX --output-definition audit-llvm-kompiled\n'
kompile semantic.k \
  --backend llvm \
  --main-module MPY \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-llvm-kompiled
llvm_exit=$?
printf 'LLVM kompile exit=%s\n' "$llvm_exit"
if (( llvm_exit != 0 )); then
  exit "$llvm_exit"
fi

printf 'COMMAND: kompile semantic.k --backend haskell --main-module MPY --syntax-module MPY-SYNTAX --output-definition audit-haskell-kompiled\n'
kompile semantic.k \
  --backend haskell \
  --main-module MPY \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-haskell-kompiled
haskell_exit=$?
printf 'Haskell kompile exit=%s\n' "$haskell_exit"
exit "$haskell_exit"
