#!/usr/bin/env bash
set -u

scratch=/tmp/audit-work/52-below-threshold
evidence=/audit-output/evidence
failures=0

run_logged() {
  local label="$1"
  local command="$2"
  local log="$evidence/03-${label}.log"
  printf 'COMMAND[%s]: cd %s && %s\n' "$label" "$scratch" "$command"
  script -q -e -c "cd '$scratch' && $command" "$log"
  local status=$?
  printf 'EXIT[%s]=%s LOG=%s\n' "$label" "$status" "$log"
  if [[ "$status" -ne 0 ]]; then
    failures=$((failures + 1))
  fi
}

run_logged translator \
  "python3 trusted/py2mpy.py reviewer-concrete.py > reviewer-concrete.mpy"

if cmp -s <(sed -n '1,10p' "$scratch/reviewer-concrete.mpy") \
          "$scratch/solution.mpy"; then
  printf 'OK reviewer concrete module starts with exact submitted Module term\n'
else
  printf 'NOTE complete translated module contains appended assertions; constructor prefix shown below\n'
  sed -n '1,24p' "$scratch/reviewer-concrete.mpy"
fi

run_logged llvm-kompile \
  "kompile reference-semantics/semantics.k --backend llvm --main-module MPY-KRUN --syntax-module MPY-SYNTAX --output-definition reviewer-runtime-kompiled"
run_logged llvm-krun \
  "krun reviewer-concrete.mpy --definition reviewer-runtime-kompiled --output pretty"

run_logged base-kompile \
  "kompile verification.k --backend haskell --main-module VERIFICATION-BASE --syntax-module VERIFICATION-BASE --output-definition reviewer-verification-base-kompiled"
run_logged loop-proof \
  "kprove spec.k --definition reviewer-verification-base-kompiled --spec-module LOOP-SPEC --output pretty"

if tr -d '\r' < "$evidence/03-loop-proof.log" | rg -x '#Top' >/dev/null; then
  printf 'OK loop-proof printed #Top\n'
else
  printf 'FAIL loop-proof did not print #Top\n'
  failures=$((failures + 1))
fi

run_logged final-kompile \
  "kompile verification.k --backend haskell --main-module VERIFICATION --syntax-module VERIFICATION --output-definition reviewer-verification-kompiled"
run_logged entry-proof \
  "kprove spec.k --definition reviewer-verification-kompiled --spec-module SPEC --output pretty"

if tr -d '\r' < "$evidence/03-entry-proof.log" | rg -x '#Top' >/dev/null; then
  printf 'OK entry-proof printed #Top\n'
else
  printf 'FAIL entry-proof did not print #Top\n'
  failures=$((failures + 1))
fi

printf 'RECONSTRUCTION_FAILURE_COUNT=%s\n' "$failures"
exit "$failures"
