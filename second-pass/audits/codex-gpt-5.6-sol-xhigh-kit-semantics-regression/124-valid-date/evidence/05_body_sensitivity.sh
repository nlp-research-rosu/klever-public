#!/usr/bin/env bash
set -u

record() {
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  local status=$?
  printf 'EXIT_STATUS: %d\n\n' "$status"
  return "$status"
}

overall=0
work=/tmp/audit-work/124-valid-date

record bash -c \
  'sed '\''s/Return(Compare(Name("day"), CmpOp("<=", Int(31))))/Return(Compare(Name("day"), CmpOp("<=", Int(30))))/'\'' /tmp/audit-work/124-valid-date/verification.k > /tmp/audit-work/124-valid-date/verification-body-audit.k' \
  || overall=1
record test \
  "$(rg -c -F 'Return(Compare(Name("day"), CmpOp("<=", Int(30))))' "$work/verification-body-audit.k")" \
  -eq 2 \
  || overall=1
record cp \
  /audit-output/evidence/05_body_sensitivity_spec.k \
  "$work/spec-body-audit.k" \
  || overall=1

record kompile --backend haskell "$work/verification-body-audit.k" \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition "$work/verification-body-audit-kompiled" \
  || overall=1

printf 'COMMAND: kprove %q --definition %q --spec-module AUDIT-BODY-SENSITIVITY\n' \
  "$work/spec-body-audit.k" \
  "$work/verification-body-audit-kompiled"
set +e
kprove "$work/spec-body-audit.k" \
  --definition "$work/verification-body-audit-kompiled" \
  --spec-module AUDIT-BODY-SENSITIVITY \
  2>&1 | tee /audit-output/evidence/05_body_sensitivity_output.log
proof_status=${PIPESTATUS[0]}
set -e
printf 'EXIT_STATUS: %d\n\n' "$proof_status"
if (( proof_status == 0 )); then overall=1; fi

record rg -q WarnStuckClaimState \
  /audit-output/evidence/05_body_sensitivity_output.log \
  || overall=1
record rg -n '<k>|true|false' \
  /audit-output/evidence/05_body_sensitivity_output.log \
  || overall=1

printf 'EXPECTED_NONZERO_PROOF_STATUS: %d\n' "$proof_status"
printf 'OVERALL_STATUS: %d\n' "$overall"
exit "$overall"
