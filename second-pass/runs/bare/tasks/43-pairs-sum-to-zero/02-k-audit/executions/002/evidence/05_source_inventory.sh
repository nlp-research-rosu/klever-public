#!/usr/bin/env bash
set -euo pipefail

source_dir=/tmp/audit-work/43-pairs-sum-to-zero/candidate
echo 'COMMAND: nl -ba semantic.k verification.k spec.k; rg syntax/configuration/rule/claim/attributes'
for file in semantic.k verification.k spec.k
do
  echo "FILE: $file"
  nl -ba "$source_dir/$file"
done
echo 'DECLARATION_AND_RULE_INDEX:'
rg -n \
  '^[[:space:]]*(syntax|configuration|rule|claim)|\[(function|total|functional|simplification|priority|owise|symbol)' \
  "$source_dir/semantic.k" \
  "$source_dir/verification.k" \
  "$source_dir/spec.k"
echo 'EXIT_STATUS: 0'
