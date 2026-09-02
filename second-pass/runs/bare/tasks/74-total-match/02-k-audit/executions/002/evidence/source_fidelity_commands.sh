#!/usr/bin/env bash
set -u

run() {
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  local rc=$?
  printf 'EXIT: %d\n' "$rc"
  return 0
}

run mkdir -p /tmp/audit-work/candidate /tmp/audit-work/reference
run cp /candidate/solution.py /candidate/solution.mpy /candidate/semantic.k \
  /candidate/verification.k /candidate/spec.k /candidate/prove.sh \
  /tmp/audit-work/candidate/
run cp /reference/canonical.py /reference/prompt.py /reference/py2mpy.py \
  /tmp/audit-work/reference/
run nl -ba /reference/prompt.py
run nl -ba /reference/canonical.py
run nl -ba /candidate/solution.py
run nl -ba /candidate/solution.mpy
run nl -ba /candidate/semantic.k
run nl -ba /candidate/verification.k
run nl -ba /candidate/spec.k
run nl -ba /candidate/prove.sh
printf '%s\n' 'COMMAND: python3 /tmp/audit-work/reference/py2mpy.py /tmp/audit-work/candidate/solution.py > /tmp/audit-work/candidate/regenerated.mpy'
python3 /tmp/audit-work/reference/py2mpy.py \
  /tmp/audit-work/candidate/solution.py \
  > /tmp/audit-work/candidate/regenerated.mpy
printf 'EXIT: %d\n' "$?"
run cmp -s /tmp/audit-work/candidate/regenerated.mpy \
  /tmp/audit-work/candidate/solution.mpy
run sha256sum /tmp/audit-work/candidate/regenerated.mpy \
  /tmp/audit-work/candidate/solution.mpy
