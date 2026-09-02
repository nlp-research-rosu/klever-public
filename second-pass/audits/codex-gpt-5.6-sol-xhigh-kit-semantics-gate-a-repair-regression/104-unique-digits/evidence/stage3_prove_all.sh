#!/usr/bin/env bash
set -uo pipefail

runner=/audit-output/evidence/run_logged.sh
work=/tmp/audit-work/104-unique-digits-audit/candidate-source
connection_definition=/tmp/audit-work/104-unique-digits-audit/connection-fresh-kompiled
verification_definition=/tmp/audit-work/104-unique-digits-audit/verification-fresh-kompiled
audit_definition=/tmp/audit-work/104-unique-digits-audit/audit-fresh-kompiled
overall_status=0

cd "$work" || exit 1

run_claim() {
  local log_name=$1
  local spec_file=$2
  local definition=$3
  local spec_module=$4
  local claim_label=$5
  "$runner" "/audit-output/evidence/$log_name" \
    kprove "$spec_file" \
      --definition "$definition" \
      --spec-module "$spec_module" \
      --claims "$claim_label"
  local claim_status=$?
  (( claim_status == 0 )) || overall_status=1
}

run_claim stage3_claim_connection_digit_loop_general.log \
  connection-spec.k "$connection_definition" CONNECTION-SPEC \
  CONNECTION-SPEC.digit-loop-general
run_claim stage3_claim_connection_digit_loop_positive.log \
  connection-spec.k "$connection_definition" CONNECTION-SPEC \
  CONNECTION-SPEC.digit-loop-positive-connection
run_claim stage3_claim_connection_assign_projection.log \
  connection-spec.k "$connection_definition" CONNECTION-SPEC \
  CONNECTION-SPEC.assign-number-projection

run_claim stage3_claim_spec_digit_loop.log \
  spec.k "$verification_definition" SPEC SPEC.digit-loop
run_claim stage3_claim_spec_outer_loop.log \
  spec.k "$verification_definition" SPEC SPEC.outer-loop
run_claim stage3_claim_spec_unique_digits.log \
  spec.k "$verification_definition" SPEC SPEC.unique-digits

run_claim stage3_claim_audit_bridge_one.log \
  audit-spec.k "$audit_definition" AUDIT-SPEC AUDIT-SPEC.bridge-one-true
run_claim stage3_claim_audit_bridge_two.log \
  audit-spec.k "$audit_definition" AUDIT-SPEC AUDIT-SPEC.bridge-two-false

printf 'ALL_POSITIVE_CLAIMS_STATUS: %d\n' "$overall_status"
exit "$overall_status"
