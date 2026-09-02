#!/usr/bin/env bash
set -u

run() {
  printf '+'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf 'EXIT_STATUS=%d\n' "$status"
  return "$status"
}

run nl -ba /tmp/audit-work/reconstruction/semantic.k
run nl -ba /tmp/audit-work/reconstruction/solution-program.k
run nl -ba /tmp/audit-work/reconstruction/verification.k
run nl -ba /tmp/audit-work/reconstruction/spec.k
run rg -n \
  '^[[:space:]]*(syntax|configuration|rule|claim)|\\[(function|total|functional|simplification|concrete|priority|owise|anywhere)' \
  /tmp/audit-work/reconstruction/semantic.k \
  /tmp/audit-work/reconstruction/solution-program.k \
  /tmp/audit-work/reconstruction/verification.k \
  /tmp/audit-work/reconstruction/spec.k
run sed -n 1680,1760p /usr/include/kframework/builtin/domains.md
run sed -n 695,750p /usr/include/kframework/builtin/domains.md
run sed -n 2307,2358p /usr/include/kframework/builtin/domains.md
run python3 /audit-output/evidence/04-pinning.py
run python3 /audit-output/evidence/04-string-boundary-probes.py
