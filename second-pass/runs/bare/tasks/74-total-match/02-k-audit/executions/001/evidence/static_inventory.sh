#!/usr/bin/env bash
set -uo pipefail

for source in \
  /tmp/audit-work/src/solution.mpy \
  /tmp/audit-work/src/semantic.k \
  /tmp/audit-work/src/verification.k \
  /tmp/audit-work/src/spec.k
do
  echo "SOURCE: $source"
  nl -ba "$source"
done

echo "DECLARATION/RULE ATTRIBUTE SEARCH"
rg -n \
  'syntax|rule|claim|configuration|function|functional|total|opaque|priority|simplification|macro' \
  /tmp/audit-work/src/semantic.k \
  /tmp/audit-work/src/verification.k \
  /tmp/audit-work/src/spec.k
