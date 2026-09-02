#!/usr/bin/env bash
set -u

work=/tmp/audit-work/reconstruction

printf '%s\n' 'COMMAND: test ! -e semantic-haskell-fresh-kompiled'
test ! -e "$work/semantic-haskell-fresh-kompiled"
code=$?
printf 'EXIT: %s\n' "$code"
(( code == 0 )) || exit 1

printf '%s\n' 'COMMAND: timeout 300s kompile semantic.k --backend haskell --syntax-module MPY-SYNTAX --main-module MPY --output-definition semantic-haskell-fresh-kompiled'
(
  cd "$work" &&
    timeout 300s kompile semantic.k \
      --backend haskell \
      --syntax-module MPY-SYNTAX \
      --main-module MPY \
      --output-definition semantic-haskell-fresh-kompiled
)
code=$?
printf 'EXIT: %s\n' "$code"
exit "$code"
