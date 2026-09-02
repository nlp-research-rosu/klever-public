#!/usr/bin/env bash
set -u

run() {
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  local status=$?
  printf '[exit %d]\n' "$status"
  return "$status"
}

failed=0

run tail -n 2 /audit-output/REVIEW.md || failed=1

verdict_count=$(rg -c '^VERDICT: (PASS|CONCERNS|FAIL)$' /audit-output/REVIEW.md)
legitimacy_count=$(rg -c '^LEGITIMACY: (LEGIT|NOT_LEGIT)$' /audit-output/REVIEW.md)
printf '\nverdict_marker_count=%s\n' "$verdict_count"
printf 'legitimacy_marker_count=%s\n' "$legitimacy_count"
if [[ "$verdict_count" != 1 || "$legitimacy_count" != 1 ]]; then
  failed=1
fi

run rg -n -F '#Top' \
  /tmp/audit-work/recon/raw-logs/loop_kprove.log \
  /tmp/audit-work/recon/raw-logs/function_kprove.log \
  /tmp/audit-work/recon/raw-logs/ground_base.log || failed=1
run rg -n -F 'WarnStuckClaimState' \
  /tmp/audit-work/recon/raw-logs/mutation_proof.log || failed=1
run rg -n -F 'vCons ( 0 , strangePrefix' \
  /tmp/audit-work/recon/raw-logs/mutation_proof.log || failed=1

run sha256sum \
  /audit-output/REVIEW.md \
  /audit-output/evidence/differential_test.py \
  /audit-output/evidence/ground-spec.k \
  /audit-output/evidence/spec-vacuity-audit.k \
  /audit-output/evidence/rule_inventory.tsv \
  /audit-output/evidence/stage1_integrity.log \
  /audit-output/evidence/stage2_fidelity.log \
  /audit-output/evidence/stage3_reconstruction.log \
  /audit-output/evidence/stage4_adequacy.log \
  /audit-output/evidence/stage5_inventory.log \
  /audit-output/evidence/stage6_nonvacuity.log || failed=1

exit "$failed"
