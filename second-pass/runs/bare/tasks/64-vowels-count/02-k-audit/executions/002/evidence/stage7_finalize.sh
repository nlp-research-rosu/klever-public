#!/usr/bin/env bash
set -euo pipefail
set -x

cd /audit-output
test "$(tail -n 2 REVIEW.md)" = $'VERDICT: CONCERNS\nLEGITIMACY: LEGIT'
test "$(rg -c '^VERDICT:' REVIEW.md)" = 1
test "$(rg -c '^LEGITIMACY:' REVIEW.md)" = 1

for required_evidence in \
  evidence/stage1_records.log \
  evidence/stage2_fidelity.log \
  evidence/stage3_rebuild.log \
  evidence/stage4_pinning.log \
  evidence/rule-inventory.md \
  evidence/stage5_static_inventory.log \
  evidence/stage6_nonvacuity.log \
  evidence/false-post-kprove.raw.log
do
  test -s "$required_evidence"
done

rg -n 'COMMAND_EXIT_CODE="0"' \
  evidence/stage1_records.log \
  evidence/stage2_fidelity.log \
  evidence/stage3_rebuild.log \
  evidence/stage4_pinning.log \
  evidence/stage5_static_inventory.log \
  evidence/stage6_nonvacuity.log

sha256sum REVIEW.md \
  evidence/rule-inventory.md \
  evidence/spec-false-postcondition.k \
  evidence/semantic-body-mutant.k \
  evidence/differential_test.py

find evidence -maxdepth 1 -type f -printf '%f %s bytes\n' | sort

