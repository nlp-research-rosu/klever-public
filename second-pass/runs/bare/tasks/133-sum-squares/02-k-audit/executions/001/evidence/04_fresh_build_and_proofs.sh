#!/usr/bin/env bash
set -u

log=/audit-output/evidence/04_fresh_build_and_proofs.log
exec > >(tee "$log") 2>&1
scratch=/tmp/audit-work/133-sum-squares
capture="$scratch/.audit-command-output.log"

run_bounded() {
  printf '\nCOMMAND:'
  printf ' %q' "$@"
  printf '\n'
  "$@" >"$capture" 2>&1
  status=$?
  lines=$(wc -l <"$capture")
  bytes=$(wc -c <"$capture")
  printf 'OUTPUT_LINES: %d OUTPUT_BYTES: %d\n' "$lines" "$bytes"
  if (( lines <= 240 )); then
    sed -n '1,240p' "$capture"
  else
    sed -n '1,180p' "$capture"
    printf '[... bounded log omitted %d middle lines ...]\n' "$((lines - 240))"
    tail -60 "$capture"
  fi
  printf 'EXIT_STATUS: %d\n' "$status"
  return 0
}

printf 'COMMAND: cd %q\n' "$scratch"
cd "$scratch"
printf 'EXIT_STATUS: %d\n' "$?"

run_bounded test ! -e audit-semantic-kompiled
run_bounded test ! -e audit-verification-kompiled
run_bounded kompile semantic.k \
  --backend llvm \
  --syntax-module MPY-SYNTAX \
  --main-module MPY \
  --output-definition audit-semantic-kompiled
run_bounded kompile verification.k \
  --backend haskell \
  --syntax-module MPY-SYNTAX \
  --main-module VERIFICATION \
  --output-definition audit-verification-kompiled

run_bounded kprove spec-claim-1.k \
  --definition audit-verification-kompiled \
  --spec-module SPEC-CLAIM-1
run_bounded kprove spec-claim-2.k \
  --definition audit-verification-kompiled \
  --spec-module SPEC-CLAIM-2
run_bounded kprove spec-claim-3.k \
  --definition audit-verification-kompiled \
  --spec-module SPEC-CLAIM-3
run_bounded kprove spec-claim-4.k \
  --definition audit-verification-kompiled \
  --spec-module SPEC-CLAIM-4
run_bounded kprove spec-claim-5.k \
  --definition audit-verification-kompiled \
  --spec-module SPEC-CLAIM-5
run_bounded kprove spec.k \
  --definition audit-verification-kompiled \
  --spec-module SPEC
