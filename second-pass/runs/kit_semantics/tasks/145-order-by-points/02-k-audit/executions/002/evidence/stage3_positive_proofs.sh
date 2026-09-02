#!/usr/bin/env bash
set -uo pipefail

scratch=/tmp/audit-work/145-order-by-points-002
evidence=/audit-output/evidence
definition=audit-verification-kompiled
overall=0

run_proof() {
  label=$1
  claims=$2
  log="$evidence/stage3_positive_${label}.log"
  if [ -n "$claims" ]; then
    echo "$ timeout --signal=TERM 300s kprove spec.k --definition $definition --spec-module SPEC --claims $claims"
    timeout --signal=TERM 300s \
      kprove spec.k \
      --definition "$definition" \
      --spec-module SPEC \
      --claims "$claims" \
      2>&1 | tee "$log"
  else
    echo "$ timeout --signal=TERM 300s kprove spec.k --definition $definition --spec-module SPEC"
    timeout --signal=TERM 300s \
      kprove spec.k \
      --definition "$definition" \
      --spec-module SPEC \
      2>&1 | tee "$log"
  fi
  command_status=${PIPESTATUS[0]}
  echo "EXIT ($label): $command_status"
  if [ "$command_status" -ne 0 ] || ! rg -q '^#Top$' "$log"; then
    overall=1
  fi
}

echo "$ cd $scratch"
cd "$scratch" || exit 1
echo "EXIT: 0"
test -d "$definition" || exit 1

run_proof loop SPEC.digit-sum-loop
run_proof function_with_loop \
  SPEC.digit-sum-loop,SPEC.digit-sum-function
run_proof order SPEC.order-by-points
run_proof all ""

echo "STAGE3 POSITIVE PROOFS EXIT: $overall"
exit "$overall"
