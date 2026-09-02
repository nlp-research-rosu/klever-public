#!/usr/bin/env bash
set -u

run() {
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  local rc=$?
  printf '[exit %d]\n' "$rc"
  return 0
}

cd /tmp/audit-work/candidate || exit 99

run nl -ba semantic.k
run nl -ba verification.k
run nl -ba spec.k
run rg -n \
  '^[[:space:]]*(syntax|configuration|rule|claim)|\\[(function|total|functional|simplification|simplifier|priority|owise|anywhere|macro|alias)' \
  semantic.k verification.k spec.k
run rg -n \
  '\\[(total|functional|simplification|simplifier|priority|owise|anywhere|macro|alias)' \
  semantic.k verification.k spec.k
run rg -n 'opaque|fresh|\\?[A-Za-z_]' semantic.k verification.k spec.k
run rg -o '^[[:space:]]*rule' semantic.k
run rg -o '^[[:space:]]*rule' verification.k
run rg -o '^[[:space:]]*claim' spec.k
