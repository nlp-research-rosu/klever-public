#!/usr/bin/env bash
set -u

run() {
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  local rc=$?
  printf '[exit %d]\n' "$rc"
  return 0
}

printf 'Rendered mode: SUPPLIED_SEMANTICS\n'
run test -d /reference/reference-semantics

for name in run-input.json metrics.json codex-last.txt codex-output.log; do
  if test -e "/candidate/$name"; then
    run stat -c '%F|%a|%s|%n' "/candidate/$name"
  else
    printf 'MISSING /candidate/%s\n' "$name"
  fi
done

printf 'Structured-trace candidates:\n'
run find /candidate -maxdepth 2 '(' -iname '*trace*' -o -iname '*.json' -o -iname '*.jsonl' ')' -printf '%y|%p|%l\n'

printf 'All candidate symlinks:\n'
run find /candidate -type l -printf '%p|%l\n'

printf 'Required submitted proof artifacts:\n'
for name in prompt.py py2mpy.py solution.py solution.mpy spec.k verification.k; do
  run stat -c '%F|%a|%s|%n' "/candidate/$name"
done

run cmp -s /reference/prompt.py /candidate/prompt.py
run cmp -s /reference/py2mpy.py /candidate/py2mpy.py
run diff -u /reference/prompt.py /candidate/prompt.py
run diff -u /reference/py2mpy.py /candidate/py2mpy.py
run diff -r --no-dereference /reference/reference-semantics /candidate/reference-semantics

printf 'Trusted/candidate digests:\n'
run sha256sum \
  /reference/prompt.py \
  /candidate/prompt.py \
  /reference/py2mpy.py \
  /candidate/py2mpy.py \
  /reference/canonical.py \
  /candidate/solution.py \
  /candidate/solution.mpy \
  /candidate/spec.k \
  /candidate/verification.k

printf 'Reference semantics manifest:\n'
run find /reference/reference-semantics -printf '%P|%y|%m|%s|%l\n'
printf 'Candidate semantics manifest:\n'
run find /candidate/reference-semantics -printf '%P|%y|%m|%s|%l\n'
