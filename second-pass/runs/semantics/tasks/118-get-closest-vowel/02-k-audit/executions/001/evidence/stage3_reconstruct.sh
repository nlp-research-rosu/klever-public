#!/usr/bin/env bash
set -u

cd /tmp/audit-work/run-118 || exit 70
cp /audit-output/evidence/independent-positive-claims.k ./independent-positive-claims.k
overall=0
counter=0

run_bounded() {
  counter=$((counter + 1))
  out="/tmp/audit-work/run-118/.audit-command-${counter}.log"
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  "$@" >"$out" 2>&1
  rc=$?
  lines=$(wc -l <"$out")
  printf '[output lines %d]\n' "$lines"
  if (( lines <= 240 )); then
    sed -n '1,240p' "$out"
  else
    sed -n '1,160p' "$out"
    printf '[... %d lines omitted ...]\n' "$((lines - 240))"
    tail -n 80 "$out"
  fi
  printf '[exit %d]\n' "$rc"
  if (( rc != 0 )); then
    overall=1
  fi
}

echo '== Toolchain =='
run_bounded kompile --version
run_bounded kprove --version

echo '== Fresh concrete definition from supplied source semantics =='
run_bounded kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-runtime-kompiled
run_bounded krun concrete-tests.mpy --definition audit-runtime-kompiled

echo '== Fresh proof definition from source =='
run_bounded kompile verification.k \
  --backend haskell \
  --main-module HUMAN-EVAL-118-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-proof-kompiled

echo '== Independently run every positive target claim =='
run_bounded kprove independent-positive-claims.k \
  --definition audit-proof-kompiled \
  --spec-module AUDIT-CLAIM-EMPTY
run_bounded kprove independent-positive-claims.k \
  --definition audit-proof-kompiled \
  --spec-module AUDIT-CLAIM-ONE
run_bounded kprove independent-positive-claims.k \
  --definition audit-proof-kompiled \
  --spec-module AUDIT-CLAIM-TWO
run_bounded kprove independent-positive-claims.k \
  --definition audit-proof-kompiled \
  --spec-module AUDIT-CLAIM-THREE-PLUS

exit "$overall"
