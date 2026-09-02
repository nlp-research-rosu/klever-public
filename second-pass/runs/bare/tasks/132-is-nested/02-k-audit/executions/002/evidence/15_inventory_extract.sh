#!/usr/bin/env bash
set -euo pipefail

printf '%s\n' 'LOCAL_K_FILES'
find /candidate -maxdepth 1 -type f -name '*.k' -printf '%f\n' | sort
printf '%s\n' 'DECLARATIONS_RULES_CLAIMS'
rg -n '^\s*(syntax|configuration|rule|claim|imports|requires)' \
  /candidate/semantic.k /candidate/verification.k /candidate/spec.k
printf '%s\n' 'SPECIAL_ATTRIBUTES'
rg -n '\[(function|total|functional|simplification|priority|owise|macro|anywhere|hook|preserves-definedness)' \
  /candidate/semantic.k /candidate/verification.k /candidate/spec.k || true
printf '%s\n' 'OPAQUE_OR_PRIORITY_TOKENS'
rg -n '\b(opaque|priority|simplification|owise|anywhere)\b' \
  /candidate/semantic.k /candidate/verification.k /candidate/spec.k || true
