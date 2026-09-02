#!/usr/bin/env bash
set -euo pipefail
set -x

test "$(rg -c '^  rule ' /tmp/audit-work/candidate-src/semantic.k)" -eq 14
test "$(rg -c '^  rule ' /tmp/audit-work/candidate-src/solution-program.k)" -eq 1
test "$(rg -c '^  rule ' /tmp/audit-work/candidate-src/verification.k)" -eq 1

rg -n '^\s*(syntax|configuration|rule|claim|context|alias)' \
  /tmp/audit-work/candidate-src/semantic.k \
  /tmp/audit-work/candidate-src/solution-program.k \
  /tmp/audit-work/candidate-src/verification.k \
  /tmp/audit-work/candidate-src/spec.k

if rg -n '\[(function|total|functional|simplification|macro|anywhere|priority|opaque)' \
  /tmp/audit-work/candidate-src/semantic.k \
  /tmp/audit-work/candidate-src/solution-program.k \
  /tmp/audit-work/candidate-src/verification.k
then
  echo "ERROR: un-inventoried special K attribute found"
  exit 1
else
  echo "no local special K rule/function attributes found"
fi

rg --pcre2 -o '[A-Z][A-Za-z]+(?=\()' \
  /tmp/audit-work/candidate-src/solution.mpy \
  | sort | uniq -c

test "$(rg -c '^  claim$' /tmp/audit-work/candidate-src/spec.k)" -eq 73
echo "static source count checks passed"
