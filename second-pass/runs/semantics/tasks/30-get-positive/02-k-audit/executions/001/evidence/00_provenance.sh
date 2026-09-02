#!/usr/bin/env bash
set -u

run() {
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  local status=$?
  printf '[exit %d]\n' "$status"
}

run sha256sum \
  /reference/prompt.py /candidate/prompt.py \
  /reference/py2mpy.py /candidate/py2mpy.py
run cmp /reference/prompt.py /candidate/prompt.py
run cmp /reference/py2mpy.py /candidate/py2mpy.py
run diff -ruN --no-dereference \
  /reference/reference-semantics /candidate/reference-semantics
run find /candidate/reference-semantics -printf '%y %P -> %l\n'
run find /reference/reference-semantics -printf '%y %P -> %l\n'
run stat -c '%F %n -> %N' \
  /candidate/prompt.py \
  /candidate/py2mpy.py \
  /candidate/solution.py \
  /candidate/solution.mpy \
  /candidate/spec.k \
  /candidate/verification.k \
  /candidate/reference-semantics
run find /candidate -maxdepth 4 -type l -printf '%p -> %l\n'

for artifact in \
  run-input.json metrics.json codex-last.txt codex-output.log
do
  printf '\n$ test -e /candidate/%s\n' "$artifact"
  if test -e "/candidate/$artifact"; then
    stat -c '%F %n' "/candidate/$artifact"
    printf '[exit 0]\n'
  else
    printf 'MISSING /candidate/%s\n' "$artifact"
    printf '[exit 1]\n'
  fi
done

run find /candidate -maxdepth 2 -type f \
  \( -iname '*trace*' -o -iname '*.jsonl' \) -print
