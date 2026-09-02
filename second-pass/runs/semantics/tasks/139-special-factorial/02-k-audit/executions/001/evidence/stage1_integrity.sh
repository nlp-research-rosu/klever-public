#!/usr/bin/env bash
set -u

run() {
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  rc=$?
  printf '[exit %d]\n' "$rc"
  return 0
}

printf 'STAGE 1 INPUT AND PROVENANCE INTEGRITY\n'
run test -d /reference/reference-semantics
run python3 /audit-output/evidence/integrity_compare.py \
  /reference/reference-semantics /candidate/reference-semantics
run cmp /reference/prompt.py /candidate/prompt.py
run cmp /reference/py2mpy.py /candidate/py2mpy.py

for artifact in \
  run-input.json metrics.json codex-last.txt codex-output.log \
  solution.py solution.mpy spec.k verification.k prompt.py py2mpy.py; do
  run test -f "/candidate/$artifact"
done

printf 'Candidate top-level lstat inventory\n'
run find /candidate -maxdepth 1 -mindepth 1 -printf '%y %f -> %l\n'
printf 'Candidate trace-like paths\n'
run find /candidate -maxdepth 3 \
  \( -iname '*trace*' -o -iname '*.jsonl' -o -iname '*trajectory*' \) \
  -printf '%y %p -> %l\n'

printf 'Trusted/candidate SHA-256 values\n'
run sha256sum \
  /reference/prompt.py /candidate/prompt.py \
  /reference/py2mpy.py /candidate/py2mpy.py \
  /candidate/solution.py /candidate/solution.mpy \
  /candidate/spec.k /candidate/verification.k

printf 'Toolchain\n'
run kompile --version
run kprove --version
