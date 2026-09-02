#!/usr/bin/env bash
set -uo pipefail
set -x

cd /tmp/audit-work/64-vowels-count
cp /audit-output/evidence/spec-false-postcondition.k audit-spec-false-postcondition.k
python3 /audit-output/evidence/false_postcondition_witness.py
witness_status=$?
printf 'FALSE_WITNESS_EXIT_STATUS=%d\n' "$witness_status"

kprove audit-spec-false-postcondition.k \
  --definition audit-verification-kompiled \
  --spec-module SPEC-FALSE-POSTCONDITION \
  --dry-run \
  > false-post-dry-run.raw.log 2>&1
dry_run_status=$?
printf 'FALSE_SPEC_DRY_RUN_EXIT_STATUS=%d\n' "$dry_run_status"
sed -n '1,160p' false-post-dry-run.raw.log
cp false-post-dry-run.raw.log /audit-output/evidence/false-post-dry-run.raw.log

timeout 60 kprove audit-spec-false-postcondition.k \
  --definition audit-verification-kompiled \
  --spec-module SPEC-FALSE-POSTCONDITION \
  --output pretty \
  > false-post-kprove.raw.log 2>&1
false_proof_status=$?
printf 'FALSE_SPEC_PROOF_EXIT_STATUS=%d\n' "$false_proof_status"
sed -n '1,280p' false-post-kprove.raw.log
cp false-post-kprove.raw.log /audit-output/evidence/false-post-kprove.raw.log
rg -q 'WarnStuckClaimState' false-post-kprove.raw.log
stuck_status=$?
printf 'FALSE_SPEC_STUCK_RESIDUAL_PRESENT=%d\n' "$stuck_status"
rg -n 'intVal \( 2 \)|intVal \( 3 \)|cannot be rewritten further' \
  false-post-kprove.raw.log
value_residual_status=$?
printf 'FALSE_SPEC_VALUE_RESIDUAL_PRESENT=%d\n' "$value_residual_status"

if (( witness_status != 0 )); then exit "$witness_status"; fi
if (( dry_run_status != 0 )); then exit "$dry_run_status"; fi
if (( false_proof_status == 0 )); then exit 94; fi
if (( false_proof_status == 124 )); then exit 95; fi
if (( stuck_status != 0 )); then exit 96; fi
if (( value_residual_status != 0 )); then exit 97; fi

