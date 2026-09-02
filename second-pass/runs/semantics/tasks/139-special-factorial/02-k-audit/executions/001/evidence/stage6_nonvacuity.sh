#!/usr/bin/env bash
set -u

task_dir=/tmp/audit-work/139-special-factorial
evidence_dir=/audit-output/evidence
mutation="$task_dir/spec-audit-vacuity.k"

run_log() {
  label=$1
  shift
  log="$evidence_dir/stage6_${label}.log"
  (
    printf '$'
    printf ' %q' "$@"
    printf '\n'
    timeout 600 "$@"
    rc=$?
    printf '[exit %d]\n' "$rc"
    exit "$rc"
  ) > "$log" 2>&1
  rc=$?
  printf '%s exit=%d log=%s\n' "$label" "$rc" "$log"
  return "$rc"
}

printf 'STAGE 6 FRESH NON-VACUITY MUTATION\n'
printf 'witness N=4: actual=288 mutated_required=289 precondition_4_gt_0=true\n'
printf '$ cp %q %q\n' \
  "$evidence_dir/spec-audit-vacuity.k" "$mutation"
cp "$evidence_dir/spec-audit-vacuity.k" "$mutation"
copy_rc=$?
printf '[exit %d]\n' "$copy_rc"

run_log mutation_build \
  kprove "$mutation" \
  --definition "$task_dir/verification-kompiled" \
  --spec-module SPEC-AUDIT-VACUITY \
  --dry-run \
  --output pretty
build_rc=$?

run_log mutation_proof \
  kprove "$mutation" \
  --definition "$task_dir/verification-kompiled" \
  --spec-module SPEC-AUDIT-VACUITY \
  --output pretty
proof_rc=$?

printf '$ rg -n %q %q\n' \
  'WarnStuckClaimState|implication check|cannot be rewritten further|#Equals|specialFactorial' \
  "$evidence_dir/stage6_mutation_proof.log"
rg -n \
  'WarnStuckClaimState|implication check|cannot be rewritten further|#Equals|specialFactorial' \
  "$evidence_dir/stage6_mutation_proof.log"
diagnostic_rc=$?
printf '[exit %d]\n' "$diagnostic_rc"

printf 'summary copy=%d build=%d proof=%d diagnostic=%d\n' \
  "$copy_rc" "$build_rc" "$proof_rc" "$diagnostic_rc"

if (( copy_rc != 0 || build_rc != 0 || proof_rc == 0 || diagnostic_rc != 0 )); then
  exit 1
fi
