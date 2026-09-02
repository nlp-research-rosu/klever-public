#!/usr/bin/env bash
set -euo pipefail
trap 'rc=$?; echo "EXIT_STATUS=$rc"' EXIT

source_dir=/tmp/audit-work/11-string-xor/source

echo 'COMMAND: bash /audit-output/evidence/05_inventory.sh'
echo 'FILE: semantic.k'
nl -ba "$source_dir/semantic.k"
echo 'FILE: verification.k'
nl -ba "$source_dir/verification.k"
echo 'FILE: spec.k'
nl -ba "$source_dir/spec.k"
echo 'DECLARATION/RULE INDEX'
rg -n \
  '^[[:space:]]*(imports|syntax|configuration|rule|claim)|\[(function|total|macro|strict|seqstrict|priority|simplification|functional)' \
  "$source_dir/semantic.k" \
  "$source_dir/verification.k" \
  "$source_dir/spec.k"
