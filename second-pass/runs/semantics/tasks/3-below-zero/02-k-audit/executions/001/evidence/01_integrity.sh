#!/usr/bin/env bash
set -u

log=/audit-output/evidence/01_integrity.log
exec > >(tee "$log") 2>&1

run() {
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf '[exit %d]\n' "$status"
  return 0
}

printf 'AUDIT STAGE 1: INPUT AND PROVENANCE INTEGRITY\n'
run find /candidate -maxdepth 3 -printf '%y %p -> %l\n'
run find /reference -maxdepth 3 -printf '%y %p -> %l\n'
run cmp --silent /candidate/prompt.py /reference/prompt.py
run cmp --silent /candidate/py2mpy.py /reference/py2mpy.py
run python3 /audit-output/evidence/compare_trees.py \
  /candidate/reference-semantics /reference/reference-semantics
run sha256sum \
  /candidate/prompt.py /reference/prompt.py \
  /candidate/py2mpy.py /reference/py2mpy.py \
  /candidate/solution.py /candidate/solution.mpy \
  /candidate/spec.k /candidate/verification.k

for required in run-input.json metrics.json codex-last.txt codex-output.log; do
  path=/candidate/$required
  if test -L "$path"; then
    printf 'INTEGRITY_FAILURE symlinked required claim artifact: %s\n' "$path"
  elif test ! -e "$path"; then
    printf 'INTEGRITY_FAILURE missing required claim artifact: %s\n' "$path"
  elif test ! -f "$path"; then
    printf 'INTEGRITY_FAILURE mistyped required claim artifact: %s\n' "$path"
  else
    printf '\n--- UNTRUSTED CLAIM ARTIFACT %s ---\n' "$path"
    sed -n '1,240p' "$path"
  fi
done

printf '\nStructured trace candidates (if any):\n'
run find /candidate -maxdepth 2 -type f \
  '(' -iname '*trace*' -o -iname '*.jsonl' -o -iname '*generation*.json' ')'
