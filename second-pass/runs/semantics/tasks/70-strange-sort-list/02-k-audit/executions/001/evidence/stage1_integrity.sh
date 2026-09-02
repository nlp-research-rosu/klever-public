#!/usr/bin/env bash
set -u

run() {
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  local status=$?
  printf '[exit %d]\n' "$status"
  return 0
}

printf 'Rendered mode: SUPPLIED_SEMANTICS\n'
run test -d /reference/reference-semantics
run find /reference/reference-semantics -printf '%y %P -> %l\n'
run find /candidate/reference-semantics -printf '%y %P -> %l\n'
run find /candidate -type l -printf '%p -> %l\n'
run diff --no-dereference -r /reference/reference-semantics /candidate/reference-semantics
run cmp /reference/prompt.py /candidate/prompt.py
run cmp /reference/py2mpy.py /candidate/py2mpy.py

for required in \
  run-input.json metrics.json codex-last.txt codex-output.log \
  prompt.py py2mpy.py solution.py solution.mpy spec.k verification.k
do
  run stat -c '%F %s bytes %n' "/candidate/$required"
done

printf '\nStructured trace candidates (top-level names containing trace):\n'
run find /candidate -maxdepth 1 -iname '*trace*' -printf '%f\n'

printf '\nCandidate top-level inventory:\n'
run find /candidate -maxdepth 1 -printf '%y %f -> %l\n'

printf '\nSource hashes:\n'
run sha256sum \
  /reference/prompt.py /candidate/prompt.py \
  /reference/py2mpy.py /candidate/py2mpy.py \
  /reference/canonical.py \
  /candidate/solution.py /candidate/solution.mpy \
  /candidate/spec.k /candidate/verification.k
