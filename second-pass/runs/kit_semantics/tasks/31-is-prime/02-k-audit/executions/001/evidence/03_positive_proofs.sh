#!/usr/bin/env bash
set -u

scratch=/tmp/audit-work/prime31
definition="$scratch/reviewer-verification-kompiled"
evidence=/audit-output/evidence

cd "$scratch" || exit 2

echo '$ kprove spec.k --definition reviewer-verification-kompiled --spec-module SPEC'
kprove spec.k \
  --definition "$definition" \
  --spec-module SPEC \
  > "$evidence/03_positive_all.log" 2>&1
all_status=$?
echo "EXIT: $all_status"

echo '$ kprove spec.k --definition reviewer-verification-kompiled --spec-module SPEC --claims SPEC.prime-loop'
kprove spec.k \
  --definition "$definition" \
  --spec-module SPEC \
  --claims SPEC.prime-loop \
  > "$evidence/03_positive_prime_loop.log" 2>&1
loop_status=$?
echo "EXIT: $loop_status"

if [[ $all_status -ne 0 || $loop_status -ne 0 ]]; then
  echo 'RESULT=FAIL'
  exit 1
fi
if [[ "$(head -n 1 "$evidence/03_positive_all.log")" != '#Top' ]]; then
  echo 'RESULT=MISSING_TOP_ALL'
  exit 2
fi
if [[ "$(head -n 1 "$evidence/03_positive_prime_loop.log")" != '#Top' ]]; then
  echo 'RESULT=MISSING_TOP_LOOP'
  exit 3
fi
echo 'RESULT=PASS'
