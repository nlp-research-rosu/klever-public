#!/usr/bin/env bash
set -uo pipefail

run() {
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf '[exit %d]\n' "$status"
  return "$status"
}

run python3 /tmp/audit-work/46-fib4-review/py2mpy.py /tmp/audit-work/46-fib4-review/solution.py
run bash -c 'python3 /tmp/audit-work/46-fib4-review/py2mpy.py /tmp/audit-work/46-fib4-review/solution.py > /tmp/audit-work/46-fib4-review/solution.regenerated.mpy'
run cmp -s /tmp/audit-work/46-fib4-review/solution.regenerated.mpy /tmp/audit-work/46-fib4-review/solution.mpy
run sha256sum /tmp/audit-work/46-fib4-review/solution.regenerated.mpy /tmp/audit-work/46-fib4-review/solution.mpy
run diff -u /tmp/audit-work/46-fib4-review/solution.mpy /tmp/audit-work/46-fib4-review/solution.regenerated.mpy
run python3 /audit-output/evidence/differential_fib4.py
