#!/usr/bin/env bash
set -u

run() {
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  rc=$?
  printf '[exit %d]\n' "$rc"
  return "$rc"
}

printf '%s\n' '$ python3 /tmp/audit-work/reference/py2mpy.py /tmp/audit-work/candidate-src/solution.py > /tmp/audit-work/candidate-src/solution.regenerated.mpy'
python3 /tmp/audit-work/reference/py2mpy.py \
  /tmp/audit-work/candidate-src/solution.py \
  > /tmp/audit-work/candidate-src/solution.regenerated.mpy
rc=$?
printf '[exit %d]\n' "$rc"

run cmp -s \
  /tmp/audit-work/candidate-src/solution.regenerated.mpy \
  /tmp/audit-work/candidate-src/solution.mpy
run sha256sum \
  /tmp/audit-work/candidate-src/solution.regenerated.mpy \
  /tmp/audit-work/candidate-src/solution.mpy
run diff -u \
  /tmp/audit-work/candidate-src/solution.regenerated.mpy \
  /tmp/audit-work/candidate-src/solution.mpy
run nl -ba /tmp/audit-work/reference/prompt.py
run nl -ba /tmp/audit-work/reference/canonical.py
run nl -ba /tmp/audit-work/candidate-src/solution.py
run nl -ba /tmp/audit-work/candidate-src/solution.mpy
