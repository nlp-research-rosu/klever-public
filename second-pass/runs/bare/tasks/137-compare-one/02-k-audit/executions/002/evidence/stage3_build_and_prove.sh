#!/usr/bin/env bash
set -uo pipefail

work=/tmp/audit-work/137-compare-one-audit

run_checked() {
  description=$1
  shift
  printf 'COMMAND: %s\n' "$description"
  "$@"
  status=$?
  printf 'EXIT: %s\n' "$status"
  (( status == 0 )) || exit "$status"
}

printf '%s\n' 'TOOLCHAIN'
command -v kup || printf '%s\n' 'kup: unavailable (independent K binaries are installed)'
run_checked 'kompile --version' kompile --version
run_checked 'kprove --version' kprove --version
run_checked 'krun --version' krun --version

if [[ -e "$work/concrete-kompiled" || -e "$work/proof-kompiled" ]]; then
  printf '%s\n' 'FAIL: fresh output definitions already exist'
  exit 1
fi

run_checked \
  'kompile semantic.k --backend llvm --main-module MPY --syntax-module MPY-SYNTAX --output-definition concrete-kompiled' \
  kompile "$work/semantic.k" \
    --backend llvm \
    --main-module MPY \
    --syntax-module MPY-SYNTAX \
    --output-definition "$work/concrete-kompiled"

run_checked \
  'kompile verification.k --backend haskell --main-module VERIFICATION --syntax-module MPY-SYNTAX --output-definition proof-kompiled' \
  kompile "$work/verification.k" \
    --backend haskell \
    --main-module VERIFICATION \
    --syntax-module MPY-SYNTAX \
    --output-definition "$work/proof-kompiled"

printf '%s\n' 'COMMAND: kast solution.mpy --output kore > solution-term.kore'
kast "$work/solution.mpy" \
  --definition "$work/proof-kompiled" \
  --module MPY-SYNTAX \
  --sort Pgm \
  --expand-macros \
  --output kore \
  > "$work/solution-term.kore"
status=$?
printf 'EXIT: %s\n' "$status"
(( status == 0 )) || exit "$status"

printf '%s\n' 'COMMAND: kast -e theSolution --output kore > proof-term.kore'
kast -e theSolution \
  --definition "$work/proof-kompiled" \
  --module VERIFICATION \
  --sort Pgm \
  --expand-macros \
  --output kore \
  > "$work/proof-term.kore"
status=$?
printf 'EXIT: %s\n' "$status"
(( status == 0 )) || exit "$status"

run_checked \
  'cmp solution-term.kore proof-term.kore' \
  cmp "$work/solution-term.kore" "$work/proof-term.kore"
sha256sum "$work/solution-term.kore" "$work/proof-term.kore"

run_checked \
  'kprove spec.k --definition proof-kompiled --spec-module SPEC --output pretty' \
  kprove "$work/spec.k" \
    --definition "$work/proof-kompiled" \
    --spec-module SPEC \
    --output pretty

printf '%s\n' 'STAGE3_BUILD_AND_FULL_PROOF_OK'
