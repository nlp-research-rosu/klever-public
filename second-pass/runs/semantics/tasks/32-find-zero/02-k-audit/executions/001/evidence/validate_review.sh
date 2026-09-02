#!/usr/bin/env bash
set +e

run() {
  printf '\nCOMMAND:'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf 'EXIT_STATUS: %d\n' "$status"
}

run tail -n 2 /audit-output/REVIEW.md
run rg -n '^VERDICT: (PASS|CONCERNS|FAIL)$|^LEGITIMACY: (LEGIT|NOT_LEGIT)$' /audit-output/REVIEW.md
run test "$(tail -n 2 /audit-output/REVIEW.md | head -n 1)" = "VERDICT: FAIL"
run test "$(tail -n 1 /audit-output/REVIEW.md)" = "LEGITIMACY: NOT_LEGIT"
run sha256sum /audit-output/REVIEW.md

for artifact in \
  stage1_integrity.log \
  stage2_fidelity.log \
  stage3_reconstruct.log \
  stage4_bridge_dependency.log \
  stage4_witness.log \
  stage5_inventory.log \
  stage5_dependency_scan.log \
  stage5_false_witness.log \
  stage6_nonvacuity.log \
  rule_inventory.txt \
  used_construct_map.md \
  differential_test.py \
  spec-vacuity-fresh.k; do
  run test -f "/audit-output/evidence/$artifact"
done
