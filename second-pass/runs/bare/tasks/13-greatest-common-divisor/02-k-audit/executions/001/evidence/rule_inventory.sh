#!/usr/bin/env bash
set -u

for path in \
  /tmp/audit-work/source/semantic.k \
  /tmp/audit-work/source/gcd-spec.k \
  /tmp/audit-work/source/verification.k \
  /tmp/audit-work/source/loop-verification.k \
  /tmp/audit-work/source/loop-spec.k \
  /tmp/audit-work/source/spec.k
do
  printf 'FILE %s\n' "$path"
  nl -ba "$path"
done

printf '%s\n' 'DECLARATION_AND_RULE_INDEX'
rg -n \
  '^\s*(syntax|configuration|rule|claim)|\[(function|total|functional|simplification|concrete|priority|owise|anywhere)' \
  /tmp/audit-work/source/semantic.k \
  /tmp/audit-work/source/gcd-spec.k \
  /tmp/audit-work/source/verification.k \
  /tmp/audit-work/source/loop-verification.k \
  /tmp/audit-work/source/loop-spec.k \
  /tmp/audit-work/source/spec.k
