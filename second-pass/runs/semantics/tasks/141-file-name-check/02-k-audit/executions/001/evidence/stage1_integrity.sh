#!/usr/bin/env bash
set -uo pipefail

run() {
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  local status=$?
  printf '[exit %d]\n' "$status"
  return 0
}

printf 'Stage 1 integrity audit\n'
printf 'UTC: '
date -u '+%Y-%m-%dT%H:%M:%SZ'

run find /candidate -maxdepth 3 -printf '%y %p -> %l\n'
run find /reference -maxdepth 3 -printf '%y %p -> %l\n'

for artifact in run-input.json metrics.json codex-last.txt codex-output.log; do
  run test -f "/candidate/$artifact"
done

run find /candidate -type l -print
run find /reference -type l -print

run cmp -s /candidate/prompt.py /reference/prompt.py
run diff -u /reference/prompt.py /candidate/prompt.py
run cmp -s /candidate/py2mpy.py /reference/py2mpy.py
run diff -u /reference/py2mpy.py /candidate/py2mpy.py

run diff -ru --no-dereference /reference/reference-semantics /candidate/reference-semantics

run sha256sum \
  /reference/prompt.py /candidate/prompt.py \
  /reference/py2mpy.py /candidate/py2mpy.py \
  /reference/canonical.py /candidate/solution.py /candidate/solution.mpy \
  /candidate/spec.k /candidate/verification.k
