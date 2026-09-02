#!/usr/bin/env bash
set -u

work=/tmp/audit-work/reconstruction
evidence=/audit-output/evidence
overall=0

run_logged() {
  label=$1
  shift
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  "$@" 2>&1 | tee "$evidence/$label.log"
  rc=${PIPESTATUS[0]}
  printf '[exit %d]\n' "$rc"
  if [ "$rc" -ne 0 ]; then
    overall=1
  fi
}

prove_logged() {
  label=$1
  shift
  run_logged "$label" "$@"
  rc=$?
  tops=$(grep -cFx '#Top' "$evidence/$label.log" || true)
  printf '[#Top exact-line count %d]\n' "$tops"
  if [ "$tops" -lt 1 ]; then
    overall=1
  fi
  return "$rc"
}

printf 'STAGE 3 CLEAN PROOF RECONSTRUCTION\n'
printf 'Scratch tree contains copied source only; all output definitions below are fresh.\n'

cd "$work" || exit 1
export PATH="/root/.nix-profile/bin:$PATH"

run_logged stage3-tool-versions kompile --version

printf '\n$ python3 py2mpy.py reviewer-smoke.py > reviewer-smoke.mpy\n'
python3 py2mpy.py reviewer-smoke.py > reviewer-smoke.mpy
rc=$?
printf '[exit %d]\n' "$rc"
if [ "$rc" -ne 0 ]; then
  overall=1
fi

run_logged stage3-kompile-runtime \
  kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition fresh-runtime-kompiled
run_logged stage3-krun-smoke \
  krun reviewer-smoke.mpy --definition fresh-runtime-kompiled

run_logged stage3-kompile-connection \
  kompile --backend haskell base-verification.k \
  --main-module VERIFICATION-BASE --syntax-module MPY-SYNTAX \
  --output-definition fresh-connection-kompiled
prove_logged stage3-prove-cmp-int \
  kprove connection-spec.k --definition fresh-connection-kompiled \
  --spec-module CONNECTION-SPEC --claims CONNECTION-SPEC.cmp-int
prove_logged stage3-prove-cmp-bool \
  kprove connection-spec.k --definition fresh-connection-kompiled \
  --spec-module CONNECTION-SPEC --claims CONNECTION-SPEC.cmp-bool
prove_logged stage3-prove-cmp-float \
  kprove connection-spec.k --definition fresh-connection-kompiled \
  --spec-module CONNECTION-SPEC --claims CONNECTION-SPEC.cmp-float
prove_logged stage3-prove-connection-all \
  kprove connection-spec.k --definition fresh-connection-kompiled \
  --spec-module CONNECTION-SPEC

run_logged stage3-kompile-loops \
  kompile --backend haskell verification-loops.k \
  --main-module VERIFICATION-LOOPS --syntax-module MPY-SYNTAX \
  --output-definition fresh-loop-verification-kompiled
prove_logged stage3-prove-loop-empty \
  kprove loop-spec.k --definition fresh-loop-verification-kompiled \
  --spec-module LOOP-SPEC --claims LOOP-SPEC.loop-empty
prove_logged stage3-prove-loop-cons \
  kprove loop-spec.k --definition fresh-loop-verification-kompiled \
  --spec-module LOOP-SPEC --claims LOOP-SPEC.loop-cons
prove_logged stage3-prove-for-empty \
  kprove loop-spec.k --definition fresh-loop-verification-kompiled \
  --spec-module LOOP-SPEC \
  --claims LOOP-SPEC.loop-empty,LOOP-SPEC.loop-cons,LOOP-SPEC.for-empty \
  --trusted LOOP-SPEC.loop-empty,LOOP-SPEC.loop-cons
prove_logged stage3-prove-for-cons \
  kprove loop-spec.k --definition fresh-loop-verification-kompiled \
  --spec-module LOOP-SPEC \
  --claims LOOP-SPEC.loop-empty,LOOP-SPEC.loop-cons,LOOP-SPEC.for-cons \
  --trusted LOOP-SPEC.loop-empty,LOOP-SPEC.loop-cons

run_logged stage3-kompile-verification \
  kompile --backend haskell verification.k \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition fresh-verification-kompiled
prove_logged stage3-prove-entry-empty \
  kprove spec.k --definition fresh-verification-kompiled \
  --spec-module SPEC --claims SPEC.below-threshold-empty
prove_logged stage3-prove-entry-int \
  kprove spec.k --definition fresh-verification-kompiled \
  --spec-module SPEC --claims SPEC.below-threshold-int
prove_logged stage3-prove-entry-bool \
  kprove spec.k --definition fresh-verification-kompiled \
  --spec-module SPEC --claims SPEC.below-threshold-bool
prove_logged stage3-prove-entry-float \
  kprove spec.k --definition fresh-verification-kompiled \
  --spec-module SPEC --claims SPEC.below-threshold-float
prove_logged stage3-prove-entry-all \
  kprove spec.k --definition fresh-verification-kompiled --spec-module SPEC

exit "$overall"
