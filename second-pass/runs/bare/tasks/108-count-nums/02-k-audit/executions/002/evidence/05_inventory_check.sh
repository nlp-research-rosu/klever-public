#!/usr/bin/env bash
set -u
trap 'status=$?; printf "SCRIPT_EXIT_STATUS=%s\n" "$status"' EXIT
set -x

rg -n '^\s*(syntax|configuration|rule|claim)\b' \
  /candidate/semantic.k \
  /candidate/verification.k \
  /candidate/spec.k

semantic_rules=$(rg -c '^\s*rule\b' /candidate/semantic.k)
verification_rules=$(rg -c '^\s*rule\b' /candidate/verification.k)
spec_claims=$(rg -c '^\s*claim\b' /candidate/spec.k)
printf "SEMANTIC_RULES=%s\n" "$semantic_rules"
printf "VERIFICATION_RULES=%s\n" "$verification_rules"
printf "SPEC_CLAIMS=%s\n" "$spec_claims"
test "$semantic_rules" -eq 39
test "$verification_rules" -eq 11
test "$spec_claims" -eq 7

set +e
rg -n '\[(?:[^]]*priority|[^]]*simplification|[^]]*concrete|[^]]*anywhere|[^]]*opaque)' \
  /candidate/semantic.k \
  /candidate/verification.k \
  /candidate/spec.k
special_status=$?
set -e
printf "NO_PRIORITY_SIMPLIFICATION_CONCRETE_ANYWHERE_OPAQUE_STATUS=%s\n" \
  "$special_status"
test "$special_status" -eq 1

find /candidate -maxdepth 1 -type f -name '*.k' -printf '%f\n' | sort
