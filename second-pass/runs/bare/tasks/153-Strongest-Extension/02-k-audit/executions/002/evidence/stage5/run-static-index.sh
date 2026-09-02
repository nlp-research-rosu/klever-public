#!/usr/bin/env bash
set -uo pipefail

scratch=/tmp/audit-work/153-strongest-extension

echo '$ sha256sum semantic.k verification.k spec.k'
sha256sum "$scratch/semantic.k" "$scratch/verification.k" "$scratch/spec.k"
echo "exit_status=$?"

echo '$ rg -n syntax|configuration|rule|claim|function|total|macro|priority|simplification'
rg -n \
  'syntax|configuration|^[[:space:]]*rule|^[[:space:]]*claim|function|total|macro|priority|simplification' \
  "$scratch/semantic.k" "$scratch/verification.k" "$scratch/spec.k"
echo "exit_status=$?"

echo '$ counts'
printf 'semantic rules='
rg -c '^[[:space:]]*rule' "$scratch/semantic.k"
printf 'verification rules='
rg -c '^[[:space:]]*rule' "$scratch/verification.k"
printf 'spec claims='
rg -c '^[[:space:]]*claim' "$scratch/spec.k"
