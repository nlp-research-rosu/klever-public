#!/usr/bin/env bash
set -uo pipefail

cd /tmp/audit-work/fresh

run_claim() {
  local audit_definition="$1"
  local audit_module="$2"
  local audit_label="$3"
  local audit_log="/audit-output/evidence/claim-${audit_module}-${audit_label}.log"
  printf 'COMMAND=kprove spec.k --definition %s --spec-module %s --claims %s.%s --output pretty -Wno unused-symbol -Wno unused-var\n' \
    "$audit_definition" "$audit_module" "$audit_module" "$audit_label" | tee "$audit_log"
  kprove spec.k \
    --definition "$audit_definition" \
    --spec-module "$audit_module" \
    --claims "${audit_module}.${audit_label}" \
    --output pretty \
    -Wno unused-symbol -Wno unused-var 2>&1 | tee -a "$audit_log"
  local audit_status=${PIPESTATUS[0]}
  printf 'EXIT_STATUS=%d\n' "$audit_status" | tee -a "$audit_log"
  return "$audit_status"
}

audit_failures=0
run_claim verification-haskell-kompiled COUNT-LOOP-SPEC count-empty || audit_failures=$((audit_failures + 1))
run_claim verification-haskell-kompiled COUNT-LOOP-SPEC count-existing-raises-step || audit_failures=$((audit_failures + 1))
run_claim verification-haskell-kompiled COUNT-LOOP-SPEC count-fresh-step || audit_failures=$((audit_failures + 1))
run_claim verification-haskell-kompiled COUNT-LOOP-SPEC count-existing-keeps-step || audit_failures=$((audit_failures + 1))
run_claim verification-haskell-kompiled COUNT-LOOP-SPEC count-fresh-keeps-step || audit_failures=$((audit_failures + 1))

run_claim verification-haskell-kompiled SELECT-LOOP-SPEC select-empty || audit_failures=$((audit_failures + 1))
run_claim verification-haskell-kompiled SELECT-LOOP-SPEC select-equal-step || audit_failures=$((audit_failures + 1))
run_claim verification-haskell-kompiled SELECT-LOOP-SPEC select-unequal-step || audit_failures=$((audit_failures + 1))

run_claim verification-haskell-kompiled EXAMPLES-SPEC example-all-once || audit_failures=$((audit_failures + 1))
run_claim verification-haskell-kompiled EXAMPLES-SPEC example-tied-two || audit_failures=$((audit_failures + 1))
run_claim verification-haskell-kompiled EXAMPLES-SPEC example-filter-one || audit_failures=$((audit_failures + 1))
run_claim verification-haskell-kompiled EXAMPLES-SPEC example-single-winner || audit_failures=$((audit_failures + 1))
run_claim verification-haskell-kompiled EXAMPLES-SPEC example-empty || audit_failures=$((audit_failures + 1))

run_claim lemmas-haskell-kompiled MAIN-CORRECTNESS-SPEC all-token-lists || audit_failures=$((audit_failures + 1))
run_claim lemmas-haskell-kompiled MAIN-CORRECTNESS-SPEC all-space-separated-strings || audit_failures=$((audit_failures + 1))

printf 'TOTAL_CLAIMS=15\n'
printf 'FAILED_CLAIMS=%d\n' "$audit_failures"
test "$audit_failures" -eq 0
