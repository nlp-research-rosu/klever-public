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
run test -d /candidate/reference-semantics
run test -f /reference/prompt.py
run test -f /reference/canonical.py
run test -f /reference/py2mpy.py

for artifact in \
  run-input.json metrics.json codex-last.txt codex-output.log \
  prompt.py py2mpy.py solution.py solution.mpy verification.k spec.k
do
  run test -f "/candidate/$artifact"
  run test ! -L "/candidate/$artifact"
done

run cmp -s /candidate/prompt.py /reference/prompt.py
run cmp -s /candidate/py2mpy.py /reference/py2mpy.py
run diff -qr --no-dereference \
  /reference/reference-semantics /candidate/reference-semantics

printf '\nCandidate/reference symlinks (expected: none):\n'
run find /candidate/reference-semantics /reference/reference-semantics \
  -type l -printf '%p -> %l\n'

printf '\nTrusted/candidate hashes:\n'
run sha256sum \
  /reference/prompt.py /candidate/prompt.py \
  /reference/py2mpy.py /candidate/py2mpy.py \
  /reference/canonical.py \
  /candidate/solution.py /candidate/solution.mpy \
  /candidate/verification.k /candidate/spec.k

printf '\nTrusted semantics manifest:\n'
run find /reference/reference-semantics -type f -print0
find /reference/reference-semantics -type f -print0 \
  | sort -z \
  | xargs -0 sha256sum
printf '[manifest exit %d]\n' "$?"

printf '\nCandidate semantics manifest:\n'
run find /candidate/reference-semantics -type f -print0
find /candidate/reference-semantics -type f -print0 \
  | sort -z \
  | xargs -0 sha256sum
printf '[manifest exit %d]\n' "$?"
