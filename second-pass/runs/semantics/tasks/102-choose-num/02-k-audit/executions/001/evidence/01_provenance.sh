#!/usr/bin/env bash
set +e

run() {
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf '[exit %d]\n' "$status"
}

printf 'Stage 1 provenance and supplied-semantics integrity\n'
run ls -la /candidate

for artifact in run-input.json metrics.json codex-last.txt codex-output.log; do
  run stat "/candidate/$artifact"
done

printf '\nStructured-trace name search (absence is allowed when no trace is present):\n'
run find /candidate -maxdepth 2 -type f \( -iname '*trace*' -o -iname '*generation*.json' -o -iname '*.jsonl' \) -print

run cmp -s /candidate/prompt.py /reference/prompt.py
run sha256sum /candidate/prompt.py /reference/prompt.py
run cmp -s /candidate/py2mpy.py /reference/py2mpy.py
run sha256sum /candidate/py2mpy.py /reference/py2mpy.py

printf '\nCandidate supplied-semantics entry types:\n'
run find /candidate/reference-semantics -printf '%y %P -> %l\n'
printf '\nTrusted supplied-semantics entry types:\n'
run find /reference/reference-semantics -printf '%y %P -> %l\n'
run find /candidate/reference-semantics -type l -print
run diff --no-dereference -r /candidate/reference-semantics /reference/reference-semantics
