#!/usr/bin/env bash
set -u

run() {
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  rc=$?
  printf '[exit %d]\n' "$rc"
  return 0
}

printf 'Rendered mode: SUPPLIED_SEMANTICS\n'
run test -d /reference/reference-semantics
run find /reference -maxdepth 4 -printf '%y %p -> %l\n'
run find /candidate -maxdepth 4 -printf '%y %p -> %l\n'

for required in \
  /candidate/run-input.json \
  /candidate/metrics.json \
  /candidate/codex-last.txt \
  /candidate/codex-output.log \
  /candidate/prompt.py \
  /candidate/py2mpy.py \
  /candidate/solution.py \
  /candidate/solution.mpy \
  /candidate/spec.k \
  /candidate/verification.k \
  /candidate/reference-semantics
do
  run test -e "$required"
done

run find /candidate -type l -print
run find /reference/reference-semantics -type l -print
run diff -r --no-dereference /reference/reference-semantics /candidate/reference-semantics
run cmp /reference/prompt.py /candidate/prompt.py
run cmp /reference/py2mpy.py /candidate/py2mpy.py
run sha256sum \
  /reference/prompt.py \
  /candidate/prompt.py \
  /reference/py2mpy.py \
  /candidate/py2mpy.py \
  /reference/canonical.py \
  /candidate/solution.py \
  /candidate/solution.mpy \
  /candidate/spec.k \
  /candidate/verification.k

printf '\nPossible structured generation traces:\n'
run find /candidate -maxdepth 2 -type f \
  '(' -iname '*trace*' -o -iname '*.jsonl' -o -iname '*generation*' ')'
