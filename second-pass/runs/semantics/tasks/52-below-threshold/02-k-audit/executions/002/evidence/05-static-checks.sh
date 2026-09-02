#!/usr/bin/env bash
set -u

failures=0
scratch=/tmp/audit-work/52-below-threshold

printf 'Exact local sources:\n'
nl -ba "$scratch/verification.k"
nl -ba "$scratch/spec.k"

/audit-output/evidence/summary_compare.py
status=$?
printf 'summary_compare.py exit=%s\n' "$status"
if [[ "$status" -ne 0 ]]; then
  failures=$((failures + 1))
fi

printf 'Opaque/symbol declarations in complete inventory:\n'
rg -n '\bsymbol\b|no-evaluators' \
  "$scratch/reference-semantics/semantics"/*.k \
  "$scratch/verification.k" || true

printf 'Simplification/functional declarations in complete source (expected none):\n'
rg -n '\bsimplification\b|\bfunctional\b' \
  "$scratch/reference-semantics/semantics.k" \
  "$scratch/reference-semantics/semantics"/*.k \
  "$scratch/verification.k" \
  "$scratch/spec.k" || true

printf 'STATIC_CHECK_FAILURE_COUNT=%s\n' "$failures"
exit "$failures"
