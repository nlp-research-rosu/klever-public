#!/usr/bin/env bash
set +e

run() {
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  rc=$?
  printf 'EXIT_STATUS=%d\n' "$rc"
}

printf 'STAGE 1 INPUT AND PROVENANCE INTEGRITY\n'
run cmp /candidate/prompt.py /reference/prompt.py
run cmp /candidate/py2mpy.py /reference/py2mpy.py
run diff -r --no-dereference /reference/reference-semantics /candidate/reference-semantics
run find /reference/reference-semantics -printf '%y %P -> %l\n'
run find /candidate/reference-semantics -printf '%y %P -> %l\n'
run sha256sum /reference/prompt.py /candidate/prompt.py /reference/py2mpy.py /candidate/py2mpy.py

for artifact in \
  /candidate/run-input.json \
  /candidate/metrics.json \
  /candidate/codex-last.txt \
  /candidate/codex-output.log \
  /candidate/PROOF.md
do
  printf '$ test -e %q || test -L %q\n' "$artifact" "$artifact"
  if test -e "$artifact" || test -L "$artifact"; then
    stat -c '%F %n' "$artifact"
    printf 'EXIT_STATUS=0\n'
  else
    printf 'MISSING %s\n' "$artifact"
    printf 'EXIT_STATUS=1\n'
  fi
done

printf '$ find /candidate -maxdepth 2 -type l -printf %%p\\ -\\>\\ %%l\\\\n\n'
find /candidate -maxdepth 2 -type l -printf '%p -> %l\n'
printf 'EXIT_STATUS=%d\n' "$?"
