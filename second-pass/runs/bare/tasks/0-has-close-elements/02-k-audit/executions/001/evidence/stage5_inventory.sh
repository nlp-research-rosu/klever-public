#!/usr/bin/env bash
set -u

files=(
  /tmp/audit-work/source/semantic.k
  /tmp/audit-work/source/verification.k
  /tmp/audit-work/source/spec.k
)

echo "DECLARATIONS, CONFIGURATION, RULES, AND CLAIMS"
rg -n '^[[:space:]]*(syntax|configuration|rule|claim)' "${files[@]}"

echo
echo "RULE ATTRIBUTES AND SPECIAL DECLARATIONS"
rg -n '\[(function|total|functional|simplification|concrete|owise|priority|trusted|opaque)[^]]*\]|priority|opaque' "${files[@]}" || true

echo
echo "EXPLICIT ABSENCE CHECKS"
for marker in total functional concrete owise priority trusted opaque; do
  count=$(rg -c "\\b${marker}\\b" "${files[@]}" | awk -F: '{ n += $NF } END { print n + 0 }')
  printf '%s=%s\n' "$marker" "$count"
done

echo
echo "IMPORTS AND REQUIRED FILES"
rg -n '^[[:space:]]*(requires|imports)' "${files[@]}"

echo
echo "LOCAL K SOURCE INVENTORY"
find /tmp/audit-work/source -maxdepth 1 -type f \
  \( -name '*.k' -o -name '*.mpy' -o -name '*.py' \) \
  -printf '%f\n' | sort
