#!/usr/bin/env bash
set -u
cd /tmp/audit-work/source

printf '%s\n' 'FALSE WITNESS: input [1, 11] has digit points [1, 2], so both Python implementations return [1, 11]; [11, 1] violates the contract.'

printf '%s\n' 'COMMAND: kompile opposite-interpretation.k --backend haskell --main-module OPPOSITE-INTERPRETATION --syntax-module MPY-SYNTAX --output-definition opposite-kompiled'
kompile \
  opposite-interpretation.k \
  --backend haskell \
  --main-module OPPOSITE-INTERPRETATION \
  --syntax-module MPY-SYNTAX \
  --output-definition opposite-kompiled
printf 'BUILD_EXIT_STATUS: %s\n' "$?"

printf '%s\n' 'COMMAND: kprove spec-opposite.k --definition opposite-kompiled --spec-module REVIEWER-SPEC-OPPOSITE --claims wrong_reverse_result'
kprove \
  spec-opposite.k \
  --definition opposite-kompiled \
  --spec-module REVIEWER-SPEC-OPPOSITE \
  --claims wrong_reverse_result
printf 'PROOF_EXIT_STATUS: %s\n' "$?"
