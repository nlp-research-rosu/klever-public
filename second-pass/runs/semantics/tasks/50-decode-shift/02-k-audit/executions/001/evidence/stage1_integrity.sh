#!/usr/bin/env bash
set -u

run_check() {
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  check_status=$?
  printf 'EXIT_STATUS: %d\n\n' "$check_status"
}

run_check test -d /reference/reference-semantics
run_check find /reference/reference-semantics -printf '%y %P -> %l\n'
run_check find /candidate/reference-semantics -printf '%y %P -> %l\n'
run_check diff --no-dereference --recursive --brief /reference/reference-semantics /candidate/reference-semantics
run_check cmp --silent /reference/prompt.py /candidate/prompt.py
run_check cmp --silent /reference/py2mpy.py /candidate/py2mpy.py
run_check sha256sum /reference/prompt.py /candidate/prompt.py /reference/py2mpy.py /candidate/py2mpy.py

for artifact in \
  run-input.json \
  metrics.json \
  codex-last.txt \
  codex-output.log \
  generation-trace.json \
  trace.json \
  solution.py \
  solution.mpy \
  spec.k \
  verification.k \
  prompt.py \
  py2mpy.py \
  reference-semantics
do
  run_check stat --format='%F | %n' "/candidate/$artifact"
done

run_check find /candidate -type l -printf '%p -> %l\n'
