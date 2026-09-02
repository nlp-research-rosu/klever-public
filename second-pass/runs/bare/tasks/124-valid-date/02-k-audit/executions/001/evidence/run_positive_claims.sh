#!/usr/bin/env bash
set -u

definition=/tmp/audit-work/verification-audit-kompiled
claim_dir=/audit-output/evidence/positive_claims
failures=0
count=0

for claim_file in "$claim_dir"/claim-[0-9][0-9][0-9].k; do
  count=$((count + 1))
  ordinal=${claim_file##*/claim-}
  ordinal=${ordinal%.k}
  module="AUDIT-CLAIM-$ordinal"
  run_log="$claim_dir/run-$ordinal.log"
  {
    printf 'WORKDIR: %s\n' "$PWD"
    printf 'COMMAND: kprove %q --definition %q --spec-module %q --smt-timeout 5000\n' \
      "$claim_file" "$definition" "$module"
  } >"$run_log"
  kprove "$claim_file" \
    --definition "$definition" \
    --spec-module "$module" \
    --smt-timeout 5000 >>"$run_log" 2>&1
  status=$?
  printf 'EXIT_STATUS: %d\n' "$status" >>"$run_log"
  if [[ $status -ne 0 ]] || ! rg -q '^#Top$' "$run_log"; then
    failures=$((failures + 1))
    printf 'claim %s: FAIL (exit=%d, top=%s)\n' \
      "$ordinal" "$status" "$(rg -q '^#Top$' "$run_log" && printf yes || printf no)"
  else
    printf 'claim %s: PASS (exit=0, #Top)\n' "$ordinal"
  fi
done

printf 'claims_run=%d failures=%d\n' "$count" "$failures"
[[ $failures -eq 0 ]]
