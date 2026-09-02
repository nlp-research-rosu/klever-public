#!/usr/bin/env bash
set -uo pipefail

echo '$ rg -n "FactorFrom|FactorizeSpec|PrependFactor" /candidate/spec.k'
rg -n 'FactorFrom|FactorizeSpec|PrependFactor' /candidate/spec.k
status=$?
printf '[exit_status=%d expected_nonzero_no_matches=yes]\n' "$status"

echo '$ rg -n "\\[(total|functional|simplification|concrete|owise)|priority|opaque" semantic.k verification.k spec.k'
rg -n '\[(total|functional|simplification|concrete|owise)|priority|opaque' \
  /candidate/semantic.k /candidate/verification.k /candidate/spec.k
status=$?
printf '[exit_status=%d expected_nonzero_no_matches=yes]\n' "$status"

echo '$ rg -n "\\[function\\]" semantic.k verification.k'
rg -n '\[function\]' /candidate/semantic.k /candidate/verification.k
status=$?
printf '[exit_status=%d]\n' "$status"

echo '$ rg -n "^\\s*rule " semantic.k verification.k'
rg -n '^\s*rule ' /candidate/semantic.k /candidate/verification.k
status=$?
printf '[exit_status=%d]\n' "$status"
