#!/usr/bin/env bash
set -euo pipefail

fresh=/tmp/audit-work/42-incr-list-audit/fresh-build-003
definition="$fresh/audit-verification-kompiled"
evidence=/audit-output/evidence
false_spec="$fresh/stage6_false_spec.k"
body_spec="$fresh/stage6_body_mutant_spec.k"

cp "$evidence/stage6_false_spec.k" "$false_spec"
cp "$evidence/stage6_body_mutant_spec.k" "$body_spec"

run_expect_zero() {
  local log_path=$1
  shift
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  set +e
  "$@" 2>&1 | tee "$log_path"
  local status=${PIPESTATUS[0]}
  set -e
  echo "EXIT_STATUS=$status"
  [[ "$status" -eq 0 ]]
}

run_expect_proof_failure() {
  local log_path=$1
  shift
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  set +e
  "$@" 2>&1 | tee "$log_path"
  local status=${PIPESTATUS[0]}
  set -e
  echo "EXIT_STATUS=$status"
  [[ "$status" -ne 0 ]]
  grep -q 'WarnStuckClaimState' "$log_path"
  grep -q 'configuration cannot be' "$log_path"
  grep -q 'rewritten further' "$log_path"
}

(
  cd "$fresh"
  run_expect_zero "$evidence/stage6_false_dry_run.log" \
    kprove stage6_false_spec.k \
      --definition "$definition" \
      --spec-module AUDIT-FALSE-SPEC \
      --dry-run

  run_expect_proof_failure "$evidence/stage6_false_kprove.log" \
    kprove stage6_false_spec.k \
      --definition "$definition" \
      --spec-module AUDIT-FALSE-SPEC

  run_expect_zero "$evidence/stage6_body_mutant_dry_run.log" \
    kprove stage6_body_mutant_spec.k \
      --definition "$definition" \
      --spec-module AUDIT-BODY-MUTANT-SPEC \
      --dry-run

  run_expect_proof_failure "$evidence/stage6_body_mutant_kprove.log" \
    kprove stage6_body_mutant_spec.k \
      --definition "$definition" \
      --spec-module AUDIT-BODY-MUTANT-SPEC
)

grep -q 'vCons ( 1 , .ValSeq )' "$evidence/stage6_false_kprove.log"
grep -q 'vCons ( 2 , .ValSeq )' "$evidence/stage6_body_mutant_kprove.log"

echo "STAGE6_MUTATIONS_REJECTED_AS_EXPECTED"
