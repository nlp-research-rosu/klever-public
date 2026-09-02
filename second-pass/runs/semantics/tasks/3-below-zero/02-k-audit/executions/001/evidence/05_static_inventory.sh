#!/usr/bin/env bash
set -u

log=/audit-output/evidence/05_static_inventory.log
exec > >(tee "$log") 2>&1

run() {
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf '[exit %d]\n' "$status"
  if test "$status" -ne 0; then
    exit "$status"
  fi
}

run python3 /audit-output/evidence/rule_inventory.py
run wc -l -c /audit-output/evidence/05_rule_inventory.md
run sha256sum \
  /reference/reference-semantics/semantics.k \
  /candidate/reference-semantics/semantics.k \
  /candidate/verification.k \
  /candidate/spec.k
run rg -n 'syntax.*no-evaluators|syntax.*functional|\[simplification' \
  /reference/reference-semantics/semantics.k \
  /reference/reference-semantics/semantics \
  /candidate/verification.k
run rg -n 'priority\(' /candidate/verification.k
