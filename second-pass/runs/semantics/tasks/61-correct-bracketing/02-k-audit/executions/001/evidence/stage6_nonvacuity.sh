#!/usr/bin/env bash
set +e

scratch_spec=/tmp/audit-work/candidate-src/spec-vacuity.k
evidence_spec=/audit-output/evidence/spec-vacuity.k
definition=/tmp/audit-work/build/verification-kompiled
log_dir=/audit-output/evidence

cp "$evidence_spec" "$scratch_spec"

run_logged() {
  logfile=$1
  shift
  (
    printf '$'
    printf ' %q' "$@"
    printf '\n'
    "$@"
    rc=$?
    printf 'EXIT_STATUS=%d\n' "$rc"
    exit "$rc"
  ) 2>&1 | tee "$logfile"
  return "${PIPESTATUS[0]}"
}

cd /tmp/audit-work/candidate-src || exit 125

run_logged "$log_dir/stage6-mutation-dry-run.log" \
  kprove spec-vacuity.k \
    --definition "$definition" \
    --spec-module SPEC-VACUITY \
    --claims false-result \
    --dry-run
dry_rc=$?

run_logged "$log_dir/stage6-mutation-proof.log" \
  kprove spec-vacuity.k \
    --definition "$definition" \
    --spec-module SPEC-VACUITY \
    --claims false-result
proof_rc=$?

printf 'ground_false_witness=S=.IntSeq,B=0; actual=true; mutated_destination=false\n'
printf 'dry_run_rc=%d\n' "$dry_rc"
printf 'proof_rc=%d\n' "$proof_rc"

# The audit succeeds iff the mutation parses/builds and the proof is rejected.
if (( dry_rc == 0 && proof_rc != 0 )); then
  exit 0
fi
exit 1
