#!/usr/bin/env bash
set -u

run() {
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf '[exit %d]\n' "$status"
  return "$status"
}

printf '[all opaque no-evaluators declarations]\n'
run rg -n '^[[:space:]]*syntax .*no-evaluators' \
  /reference/reference-semantics/semantics \
  /candidate/verification.k

printf '[all local priority attributes]\n'
run rg -n 'priority\([0-9]+\)' \
  /reference/reference-semantics/semantics \
  /candidate/verification.k

printf '[all local simplification attributes; exit 1 means none]\n'
run rg -n '\bsimplification\b' \
  /reference/reference-semantics/semantics \
  /candidate/verification.k

printf '[function/total/functional declaration count]\n'
run bash -c "rg -n '^[[:space:]]*syntax .*\\[(?=[^]]*(function|total|functional))' /reference/reference-semantics/semantics /candidate/verification.k --pcre2 | wc -l"

printf '[inventory disposition counts]\n'
run bash -c "rg -o 'Audit decision: [A-Z_]+' /audit-output/evidence/rule_inventory.md | sort | uniq -c"
