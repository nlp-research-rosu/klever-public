#!/usr/bin/env bash
set -u

work=/tmp/audit-work/reconstruction
status=0

printf '%s\n' 'COMMAND: command -v kompile && kompile --version && command -v krun && krun --version && command -v kprove && kprove --version && python3 --version'
command -v kompile
kompile --version
command -v krun
krun --version
command -v kprove
kprove --version
python3 --version
code=$?
printf 'EXIT: %s\n' "$code"
(( code == 0 )) || status=1

printf '%s\n' 'COMMAND: test ! -e semantic-fresh-kompiled && test ! -e verification-fresh-kompiled'
test ! -e "$work/semantic-fresh-kompiled" &&
  test ! -e "$work/verification-fresh-kompiled"
code=$?
printf 'EXIT: %s\n' "$code"
(( code == 0 )) || status=1

printf '%s\n' 'COMMAND: timeout 300s kompile semantic.k --backend llvm --syntax-module MPY-SYNTAX --main-module MPY --output-definition semantic-fresh-kompiled'
(
  cd "$work" &&
    timeout 300s kompile semantic.k \
      --backend llvm \
      --syntax-module MPY-SYNTAX \
      --main-module MPY \
      --output-definition semantic-fresh-kompiled
)
code=$?
printf 'EXIT: %s\n' "$code"
(( code == 0 )) || status=1

printf '%s\n' 'COMMAND: timeout 300s kompile verification.k --backend haskell --syntax-module MPY-SYNTAX --main-module VERIFICATION --output-definition verification-fresh-kompiled'
(
  cd "$work" &&
    timeout 300s kompile verification.k \
      --backend haskell \
      --syntax-module MPY-SYNTAX \
      --main-module VERIFICATION \
      --output-definition verification-fresh-kompiled
)
code=$?
printf 'EXIT: %s\n' "$code"
(( code == 0 )) || status=1

printf '%s\n' 'COMMAND: find fresh definitions -maxdepth 1 -type f -printf "%p %s bytes\n" | sort'
find \
  "$work/semantic-fresh-kompiled" \
  "$work/verification-fresh-kompiled" \
  -maxdepth 1 -type f -printf '%p %s bytes\n' | sort
code=$?
printf 'EXIT: %s\n' "$code"
(( code == 0 )) || status=1

exit "$status"
