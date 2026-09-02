#!/usr/bin/env bash
set -u

run() {
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf '[exit %d]\n' "$status"
  return 0
}

run test -d /reference/reference-semantics
run find /candidate -printf '%y %p -> %l\n'
run find /reference -printf '%y %p -> %l\n'
run find /candidate/reference-semantics -type l -print
run find /reference/reference-semantics -type l -print
run diff -qr --no-dereference /reference/reference-semantics /candidate/reference-semantics
run cmp -s /reference/prompt.py /candidate/prompt.py
run cmp -s /reference/py2mpy.py /candidate/py2mpy.py
run sha256sum /reference/prompt.py /candidate/prompt.py /reference/py2mpy.py /candidate/py2mpy.py

for path in \
  /candidate/run-input.json \
  /candidate/metrics.json \
  /candidate/codex-last.txt \
  /candidate/codex-output.log
do
  run test -f "$path"
done

run find /candidate -maxdepth 2 -type f -printf '%p\n'
run find /candidate -maxdepth 2 -type d -printf '%p\n'
