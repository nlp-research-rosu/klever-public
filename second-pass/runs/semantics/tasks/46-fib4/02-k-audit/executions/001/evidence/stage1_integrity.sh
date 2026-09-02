#!/usr/bin/env bash
set -u

candidate=/candidate
reference=/reference

run() {
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  local rc=$?
  printf '[exit %d]\n' "$rc"
  return 0
}

printf 'Rendered semantics mode: SUPPLIED_SEMANTICS\n'
run test -d "$reference/reference-semantics"
run find "$candidate" -printf '%y %P -> %l\n'
run find "$reference" -printf '%y %P -> %l\n'

for artifact in run-input.json metrics.json codex-last.txt codex-output.log; do
  run test -f "$candidate/$artifact"
done

printf 'Structured trace candidates:\n'
run find "$candidate" -maxdepth 1 -type f \
  \( -iname '*trace*' -o -iname '*.jsonl' \) -print

run cmp -s "$candidate/prompt.py" "$reference/prompt.py"
run cmp -s "$candidate/py2mpy.py" "$reference/py2mpy.py"
run diff -r --no-dereference "$reference/reference-semantics" \
  "$candidate/reference-semantics"

printf 'Candidate supplied-semantics entry types:\n'
run find "$candidate/reference-semantics" -printf '%y %P -> %l\n'
printf 'Trusted supplied-semantics entry types:\n'
run find "$reference/reference-semantics" -printf '%y %P -> %l\n'

printf 'SHA-256 inventory:\n'
run find "$candidate" -type f -exec sha256sum '{}' +
run find "$reference" -type f -exec sha256sum '{}' +
