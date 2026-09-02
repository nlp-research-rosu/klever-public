#!/usr/bin/env bash
set -u

work=/tmp/audit-work
evidence=/audit-output/evidence
cd "$work" || exit 90
cp "$evidence/spec-concrete-adequacy.k" spec-concrete-adequacy.k

run_claim() {
  local label="$1"
  local log="$evidence/04-kprove-${label}.log"
  echo "$ kprove spec-concrete-adequacy.k --definition audit-verification-kompiled --spec-module ADEQUACY-CONCRETE-SPEC --claims ADEQUACY-CONCRETE-SPEC.$label" \
    | tee "$log"
  kprove spec-concrete-adequacy.k \
    --definition audit-verification-kompiled \
    --spec-module ADEQUACY-CONCRETE-SPEC \
    --claims "ADEQUACY-CONCRETE-SPEC.$label" \
    2>&1 | tee -a "$log"
  local status=${PIPESTATUS[0]}
  echo "EXIT_STATUS=$status" | tee -a "$log"
  return "$status"
}

run_claim empty
empty_status=$?
run_claim accepted-one
accepted_status=$?
run_claim rejected-two
rejected_status=$?

echo "OBSERVED_STATUS empty=$empty_status accepted-one=$accepted_status rejected-two=$rejected_status"

# This is a diagnostic adequacy probe: expected statuses are encoded so a
# surprising behavior is itself visible as a script failure.
if [[ "$empty_status" -ne 0 || "$accepted_status" -eq 0 || "$rejected_status" -eq 0 ]]; then
  exit 1
fi
exit 0
