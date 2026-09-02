#!/usr/bin/env bash
set +e

run() {
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf '[exit %d]\n' "$status"
  return 0
}

printf '%s\n' 'Stage 1: input and provenance integrity'
run find /candidate -maxdepth 4 -printf '%y %p -> %l\n'
run find /reference -maxdepth 4 -printf '%y %p -> %l\n'

for artifact in run-input.json metrics.json codex-last.txt codex-output.log; do
  run test -f "/candidate/$artifact"
done

printf '\nStructured-trace-like candidate entries (if any):\n'
run find /candidate -maxdepth 2 -type f '(' -iname '*trace*' -o -iname '*.jsonl' -o -iname '*events*' ')'

printf '\nTrusted source identity checks:\n'
run cmp -s /candidate/prompt.py /reference/prompt.py
run cmp -s /candidate/py2mpy.py /reference/py2mpy.py
run sha256sum /candidate/prompt.py /reference/prompt.py /candidate/py2mpy.py /reference/py2mpy.py

printf '\nCandidate semantics entry types, relative paths, and symlink targets:\n'
run bash -c "cd /candidate/reference-semantics && find . -printf '%y %P -> %l\\n' | LC_ALL=C sort"
printf '\nTrusted semantics entry types, relative paths, and symlink targets:\n'
run bash -c "cd /reference/reference-semantics && find . -printf '%y %P -> %l\\n' | LC_ALL=C sort"

printf '\nRecursive semantics comparison (no symlink dereference):\n'
run diff -ruN --no-dereference /reference/reference-semantics /candidate/reference-semantics
run bash -c "test -z \"\$(find /candidate/reference-semantics -type l -print -quit)\""

printf '\nK/Python tool versions:\n'
run command -v kompile
run command -v kprove
run command -v krun
run kompile --version
run kprove --version
run python3 --version
