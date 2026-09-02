#!/usr/bin/env bash
set -u

LOG=/audit-output/evidence/01_integrity.log
exec >"$LOG" 2>&1

run() {
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  local rc=$?
  printf '[exit %d]\n' "$rc"
  return 0
}

run find /reference -maxdepth 3 -printf '%y %p -> %l\n'
run find /candidate -maxdepth 4 -printf '%y %p -> %l\n'
run test -d /reference/reference-semantics
run test ! -L /reference/reference-semantics
run test -d /candidate/reference-semantics
run test ! -L /candidate/reference-semantics
run diff -qr --no-dereference /reference/reference-semantics /candidate/reference-semantics
run cmp -s /reference/prompt.py /candidate/prompt.py
run cmp -s /reference/py2mpy.py /candidate/py2mpy.py
run sha256sum /reference/prompt.py /candidate/prompt.py /reference/py2mpy.py /candidate/py2mpy.py

for path in \
  /candidate/run-input.json \
  /candidate/metrics.json \
  /candidate/codex-last.txt \
  /candidate/codex-output.log; do
  run test -f "$path"
done

printf '\nStructured trace candidates (regular files only):\n'
find /candidate -maxdepth 2 -type f \
  \( -iname '*trace*' -o -iname '*trajectory*' -o -iname '*generation*' \) \
  -printf '%p\n' | sort

printf '\nCandidate and trusted file digests:\n'
find /candidate/reference-semantics -type f -print0 |
  sort -z |
  xargs -0 sha256sum
find /reference/reference-semantics -type f -print0 |
  sort -z |
  xargs -0 sha256sum
