#!/usr/bin/env bash
set -u

overall=0
run() {
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf '[exit %d]\n' "$status"
  if [ "$status" -ne 0 ]; then
    overall=1
  fi
}

run nl -ba /tmp/audit-work/source/semantic.k
run nl -ba /tmp/audit-work/source/verification.k
run nl -ba /tmp/audit-work/source/spec.k
run nl -ba /tmp/audit-work/submitted-solution.mpy
run rg -n \
  '^(requires|module|endmodule|  imports|  syntax|  configuration|  rule|  claim)|\[(function|total|functional|simplification|concrete|priority|symbol)' \
  /tmp/audit-work/source/semantic.k \
  /tmp/audit-work/source/verification.k \
  /tmp/audit-work/source/spec.k
run python3 /audit-output/evidence/check_pinning.py

printf '[script exit %d]\n' "$overall"
exit "$overall"
