#!/usr/bin/env bash
set -euo pipefail
set -x

cd /tmp/audit-work/64-vowels-count
rg -n '^\s*(module|endmodule|imports|syntax|configuration|rule|claim)' \
  semantic.k verification.k spec.k
rg -n '\[(function|total|functional|simplification|concrete|macro|strict|seqstrict|priority)' \
  semantic.k verification.k spec.k
if rg -n '\[(priority|simplification|concrete|functional)\b|opaque' \
  semantic.k verification.k spec.k; then
  printf 'unexpected_special_declaration=true\n'
  exit 1
else
  printf 'priority_simplification_concrete_functional_opaque_absent=true\n'
fi
sha256sum semantic.k verification.k spec.k \
  /audit-output/evidence/rule-inventory.md

