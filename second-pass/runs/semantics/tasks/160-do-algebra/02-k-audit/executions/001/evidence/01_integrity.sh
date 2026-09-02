#!/usr/bin/env bash
set -u

LOG=/audit-output/evidence/01_integrity.log
: > "$LOG"

run() {
  printf 'COMMAND: ' >> "$LOG"
  printf '%q ' "$@" >> "$LOG"
  printf '\n' >> "$LOG"
  "$@" >> "$LOG" 2>&1
  status=$?
  printf 'EXIT: %d\n\n' "$status" >> "$LOG"
  return 0
}

run pwd
run kompile --version
run kprove --version
run find /candidate /reference -printf '%y %p -> %l\n'

for artifact in \
  /candidate/run-input.json \
  /candidate/metrics.json \
  /candidate/codex-last.txt \
  /candidate/codex-output.log \
  /candidate/generation-trace.json \
  /candidate/prompt.py \
  /candidate/py2mpy.py \
  /candidate/solution.py \
  /candidate/solution.mpy \
  /candidate/spec.k \
  /candidate/verification.k \
  /candidate/reference-semantics \
  /reference/canonical.py \
  /reference/prompt.py \
  /reference/py2mpy.py \
  /reference/reference-semantics
do
  run stat -c '%F %a %s %n' "$artifact"
done

run diff -u /reference/prompt.py /candidate/prompt.py
run diff -u /reference/py2mpy.py /candidate/py2mpy.py
run diff -ru --no-dereference /reference/reference-semantics /candidate/reference-semantics
run find /candidate/reference-semantics -type l -printf '%p -> %l\n'
run sha256sum \
  /reference/prompt.py /candidate/prompt.py \
  /reference/py2mpy.py /candidate/py2mpy.py \
  /reference/canonical.py \
  /candidate/solution.py /candidate/solution.mpy \
  /candidate/spec.k /candidate/verification.k
