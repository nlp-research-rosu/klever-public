#!/usr/bin/env bash
set -u

source_dir=/tmp/audit-work/106-f/source

echo 'COMMAND: line-numbered source inventory'
for file in semantic.k verification.k spec.k solution.mpy solution.py; do
  echo "FILE: $source_dir/$file"
  nl -ba "$source_dir/$file"
done

echo 'COMMAND: declaration/rule/claim inventory'
rg -n '^\s*(syntax|configuration|rule|claim)' \
  "$source_dir/semantic.k" \
  "$source_dir/verification.k" \
  "$source_dir/spec.k"
status=$?
echo "EXIT_STATUS: $status"

echo 'COMMAND: special-attribute inventory'
rg -n '\[(function|total|functional|simplification|concrete|priority|owise|macro|anywhere|trusted)' \
  "$source_dir/semantic.k" \
  "$source_dir/verification.k" \
  "$source_dir/spec.k"
special_status=$?
echo "RG_EXIT_STATUS: $special_status (0 means matches found; 1 would mean none)"

echo 'COMMAND: opaque-token inventory'
rg -n -i 'opaque|oracle|uninterpreted|fresh' \
  "$source_dir/semantic.k" \
  "$source_dir/verification.k" \
  "$source_dir/spec.k"
opaque_status=$?
echo "RG_EXIT_STATUS: $opaque_status (1 means none found)"

echo 'COMMAND: source rule and claim counts'
printf 'semantic_rules='
rg -c '^\s*rule\b' "$source_dir/semantic.k"
printf 'verification_rules='
rg -c '^\s*rule\b' "$source_dir/verification.k"
printf 'spec_claims='
rg -c '^\s*claim\b' "$source_dir/spec.k"
