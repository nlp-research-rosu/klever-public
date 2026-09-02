#!/usr/bin/env bash
set -u

run() {
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  local status=$?
  printf '[exit %d]\n\n' "$status"
  return 0
}

printf 'Stage 1 integrity checks\n'
printf 'UTC: %s\n\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)"

run test -d /reference/reference-semantics
run test -d /candidate/reference-semantics

for path in \
  /candidate/run-input.json \
  /candidate/metrics.json \
  /candidate/codex-last.txt \
  /candidate/codex-output.log \
  /candidate/prompt.py \
  /candidate/py2mpy.py \
  /candidate/solution.py \
  /candidate/solution.mpy \
  /candidate/spec.k \
  /candidate/verification.k
do
  run test -f "$path"
done

run find /candidate -xdev -type l -printf '%p -> %l\n'
run find /candidate -xdev -printf '%y %p\n'
run find /reference/reference-semantics -xdev -type l -printf '%p -> %l\n'

run cmp -s /candidate/prompt.py /reference/prompt.py
run cmp -s /candidate/py2mpy.py /reference/py2mpy.py
run diff -rq --no-dereference /reference/reference-semantics /candidate/reference-semantics

run sha256sum \
  /candidate/prompt.py /reference/prompt.py \
  /candidate/py2mpy.py /reference/py2mpy.py \
  /candidate/solution.py /candidate/solution.mpy \
  /candidate/spec.k /candidate/verification.k
