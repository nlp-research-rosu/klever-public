#!/usr/bin/env bash
set -uo pipefail

source_root=/tmp/audit-work/reconstruction

echo 'COMMAND: find candidate source root for K files (compiled directories excluded)'
find "$source_root" -maxdepth 1 -type f -name '*.k' -printf '%f\n' | sort
echo "EXIT_STATUS=$?"

for file in semantic.k verification.k spec.k; do
  echo "FILE=$file"
  sha256sum "$source_root/$file"
  echo 'DECLARATION_STARTS:'
  rg -n '^[[:space:]]*(configuration|syntax|rule|claim)([[:space:]]|$)' \
    "$source_root/$file"
  echo "DECLARATION_SCAN_EXIT_STATUS=$?"
  echo 'ATTRIBUTES_AND_REVIEW_KEYWORDS:'
  rg -n '\[(function|total|functional|macro|simplification|concrete|priority|owise)[^]]*\]|opaque|priority' \
    "$source_root/$file"
  keyword_status=$?
  echo "KEYWORD_SCAN_EXIT_STATUS=$keyword_status (1 means no matching attributes)"
done

echo 'COUNTS:'
printf 'semantic syntax starts='
rg -c '^[[:space:]]*syntax([[:space:]]|$)' "$source_root/semantic.k"
printf 'semantic rule starts='
rg -c '^[[:space:]]*rule([[:space:]]|$)' "$source_root/semantic.k"
printf 'verification syntax starts='
rg -c '^[[:space:]]*syntax([[:space:]]|$)' "$source_root/verification.k"
printf 'verification rule starts='
rg -c '^[[:space:]]*rule([[:space:]]|$)' "$source_root/verification.k"
printf 'spec claim starts='
rg -c '^[[:space:]]*claim([[:space:]]|$)' "$source_root/spec.k"

echo 'RULE_INVENTORY_COMPLETE=YES'
exit 0
