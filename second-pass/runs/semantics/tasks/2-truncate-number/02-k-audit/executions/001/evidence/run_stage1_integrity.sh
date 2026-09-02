#!/usr/bin/env bash
set -u

run() {
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf '[exit %d]\n' "$status"
}

printf '[required candidate metadata]\n'
for artifact in run-input.json metrics.json codex-last.txt codex-output.log; do
  if [[ -e "/candidate/$artifact" || -L "/candidate/$artifact" ]]; then
    run stat -c '%F %a %s %n -> %N' "/candidate/$artifact"
  else
    printf 'MISSING /candidate/%s\n' "$artifact"
  fi
done

printf '[structured generation trace candidates]\n'
run find /candidate -maxdepth 2 -type f \
  \( -iname '*trace*' -o -iname '*.jsonl' -o -iname '*events*' \) -print

printf '[candidate and trusted entry types]\n'
run find /candidate /reference -maxdepth 3 -printf '%y %m %p -> %l\n'

printf '[symlink checks]\n'
run find /candidate -type l -print
run find /reference/reference-semantics -type l -print

printf '[trusted-file comparisons]\n'
run cmp -s /candidate/prompt.py /reference/prompt.py
run cmp -s /candidate/py2mpy.py /reference/py2mpy.py

printf '[supplied-semantics recursive comparison]\n'
run diff -r --no-dereference /candidate/reference-semantics /reference/reference-semantics

printf '[trusted and candidate hashes]\n'
run sha256sum \
  /reference/prompt.py /candidate/prompt.py \
  /reference/py2mpy.py /candidate/py2mpy.py \
  /reference/canonical.py \
  /candidate/solution.py /candidate/solution.mpy \
  /candidate/spec.k /candidate/verification.k
run bash -c "find /reference/reference-semantics -type f -print0 | sort -z | xargs -0 sha256sum"
run bash -c "find /candidate/reference-semantics -type f -print0 | sort -z | xargs -0 sha256sum"
