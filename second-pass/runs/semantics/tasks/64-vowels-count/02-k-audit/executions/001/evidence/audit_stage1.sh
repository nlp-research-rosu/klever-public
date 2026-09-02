#!/usr/bin/env bash
set -u

run() {
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf '[exit %d]\n' "$status"
  return 0
}

run test -d /reference/reference-semantics
run test -f /reference/canonical.py
run test -f /reference/prompt.py
run test -f /reference/py2mpy.py

run find /reference/reference-semantics -printf '%y %P -> %l\n'
run find /candidate/reference-semantics -printf '%y %P -> %l\n'
run diff -r --no-dereference /reference/reference-semantics /candidate/reference-semantics
run cmp -s /reference/prompt.py /candidate/prompt.py
run cmp -s /reference/py2mpy.py /candidate/py2mpy.py
run sha256sum /reference/prompt.py /candidate/prompt.py /reference/py2mpy.py /candidate/py2mpy.py

for artifact in run-input.json metrics.json codex-last.txt codex-output.log; do
  run test -f "/candidate/$artifact"
done

run find /candidate -maxdepth 2 -type f -printf '%P\n'
run find /candidate -type l -printf '%P -> %l\n'
