#!/usr/bin/env bash
set -euo pipefail
trap 'status=$?; printf "[audit] exit_status=%s\n" "$status"' EXIT
set -x

src=/tmp/audit-work/130-tri/candidate

nl -ba "$src/solution.mpy"
nl -ba "$src/semantic.k"
nl -ba "$src/verification.k"
nl -ba "$src/spec.k"

rg -n \
  '^\s*(configuration|syntax|rule|claim)\b|\[(function|total|functional|macro|simplification|concrete|priority)\b' \
  "$src/semantic.k" "$src/verification.k" "$src/spec.k"

if rg -n '\[(total|functional|simplification|concrete|priority)\b|owise|opaque' \
  "$src/semantic.k" "$src/verification.k" "$src/spec.k"
then
  printf 'special_soundness_attributes_present=true\n'
else
  printf 'special_soundness_attributes_present=false\n'
fi
