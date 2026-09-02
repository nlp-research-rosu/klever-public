#!/usr/bin/env bash
set -uo pipefail

source_spec=/tmp/audit-work/25-factorize-audit/source/audit-factorfrom-witness.k
preserved_spec=/audit-output/evidence/05_factorfrom_witness.k
definition=/tmp/audit-work/25-factorize-audit/verification-fresh-kompiled

echo "$ cmp $source_spec $preserved_spec"
cmp "$source_spec" "$preserved_spec"
status=$?
printf '[exit_status=%d]\n' "$status"
if (( status != 0 )); then
  exit "$status"
fi

echo "$ kprove $source_spec --definition $definition --spec-module AUDIT-FACTORFROM-WITNESS"
kprove "$source_spec" \
  --definition "$definition" \
  --spec-module AUDIT-FACTORFROM-WITNESS
status=$?
printf '[exit_status=%d]\n' "$status"
exit "$status"
