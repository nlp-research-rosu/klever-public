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

printf '## Required artifact types\n'
run find /candidate -maxdepth 1 \
  \( -name run-input.json -o -name metrics.json -o -name codex-last.txt \
     -o -name codex-output.log -o -name prompt.py -o -name py2mpy.py \
     -o -name solution.py -o -name solution.mpy -o -name spec.k \
     -o -name verification.k -o -name prove.sh -o -name PROOF.md \) \
  -printf '%y %f -> %l\n'

printf '## Symlink checks\n'
run find /candidate/reference-semantics -type l -printf '%p -> %l\n'
run find /reference/reference-semantics -type l -printf '%p -> %l\n'

printf '## Trusted identity checks\n'
run sha256sum /reference/prompt.py /reference/py2mpy.py \
  /candidate/prompt.py /candidate/py2mpy.py
run cmp /candidate/prompt.py /reference/prompt.py
run cmp /candidate/py2mpy.py /reference/py2mpy.py
run diff -qr --no-dereference \
  /reference/reference-semantics /candidate/reference-semantics

printf '## Trusted regeneration\n'
printf '%s\n' '$ python3 /tmp/audit-work/reconstruction/py2mpy.py /tmp/audit-work/reconstruction/solution.py > /tmp/audit-work/reconstruction/regenerated-solution.mpy'
python3 /tmp/audit-work/reconstruction/py2mpy.py \
  /tmp/audit-work/reconstruction/solution.py \
  > /tmp/audit-work/reconstruction/regenerated-solution.mpy
printf '[exit %d]\n' "$?"
run cmp /tmp/audit-work/reconstruction/solution.mpy \
  /tmp/audit-work/reconstruction/regenerated-solution.mpy

printf '## Independent Python differential\n'
run python3 /audit-output/evidence/differential_test.py
run cp /tmp/audit-work/reconstruction/differential_inputs.json \
  /audit-output/evidence/inputs/differential_inputs.json
