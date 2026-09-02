#!/usr/bin/env bash
set -u

status=0
export PATH="/home/agent/.nix-profile/bin:$PATH"

printf '%s\n' 'COMMAND: kompile reference-semantics/semantics.k --backend llvm --main-module MPY-KRUN --syntax-module MPY-SYNTAX --output-definition runtime-audit-kompiled'
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-audit-kompiled
rc=$?
printf 'EXIT: %d\n\n' "$rc"
(( rc == 0 )) || status=1

printf '%s\n' 'COMMAND: krun reviewer-concrete.mpy --definition runtime-audit-kompiled --output pretty'
krun reviewer-concrete.mpy \
  --definition runtime-audit-kompiled \
  --output pretty
rc=$?
printf 'EXIT: %d\n\n' "$rc"
(( rc == 0 )) || status=1

printf '%s\n' 'COMMAND: kompile verification.k --backend haskell --main-module VERIFICATION --syntax-module VERIFICATION --output-definition verification-audit-kompiled'
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module VERIFICATION \
  --output-definition verification-audit-kompiled
rc=$?
printf 'EXIT: %d\n\n' "$rc"
(( rc == 0 )) || status=1

printf '%s\n' 'COMMAND: kprove spec.k --definition verification-audit-kompiled --spec-module FILTER-BY-PREFIX-SPEC'
kprove spec.k \
  --definition verification-audit-kompiled \
  --spec-module FILTER-BY-PREFIX-SPEC
rc=$?
printf 'EXIT: %d\n\n' "$rc"
(( rc == 0 )) || status=1

printf 'SCRIPT_EXIT: %d\n' "$status"
exit "$status"
