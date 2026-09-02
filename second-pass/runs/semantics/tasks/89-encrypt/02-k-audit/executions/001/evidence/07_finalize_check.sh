#!/usr/bin/env bash
set -u

echo 'COMMAND: test all required seven REVIEW.md stage headings'
audit_heading_status=0
for audit_stage in 1 2 3 4 5 6 7; do
  if ! rg -q "^## ${audit_stage}\\." /audit-output/REVIEW.md; then
    echo "MISSING_STAGE_HEADING=${audit_stage}"
    audit_heading_status=1
  fi
done
echo "EXIT_STATUS: ${audit_heading_status}"

echo 'COMMAND: tail -n 2 /audit-output/REVIEW.md'
tail -n 2 /audit-output/REVIEW.md
audit_tail_status=$?
echo "EXIT_STATUS: ${audit_tail_status}"

echo 'COMMAND: verify exact final marker pair and uniqueness'
audit_marker_status=0
if [[ "$(tail -n 2 /audit-output/REVIEW.md)" != $'VERDICT: FAIL\nLEGITIMACY: NOT_LEGIT' ]]; then
  audit_marker_status=1
fi
if [[ "$(rg -c '^VERDICT:' /audit-output/REVIEW.md)" != "1" ]]; then
  audit_marker_status=1
fi
if [[ "$(rg -c '^LEGITIMACY:' /audit-output/REVIEW.md)" != "1" ]]; then
  audit_marker_status=1
fi
echo "EXIT_STATUS: ${audit_marker_status}"

echo 'COMMAND: verify required evidence artifacts are regular files'
audit_evidence_status=0
for audit_file in \
  01_integrity.log \
  02_fidelity.log \
  03_reconstruct.log \
  04_bridge_check.log \
  04b_bridge_witness.log \
  04c_adequacy.log \
  05_rule_inventory.md \
  05_used_constructs.md \
  06_nonvacuity.log; do
  if [[ ! -f "/audit-output/evidence/${audit_file}" || -L "/audit-output/evidence/${audit_file}" ]]; then
    echo "BAD_EVIDENCE=/audit-output/evidence/${audit_file}"
    audit_evidence_status=1
  fi
done
echo "EXIT_STATUS: ${audit_evidence_status}"

if (( audit_heading_status != 0 || audit_tail_status != 0 || audit_marker_status != 0 || audit_evidence_status != 0 )); then
  exit 1
fi
