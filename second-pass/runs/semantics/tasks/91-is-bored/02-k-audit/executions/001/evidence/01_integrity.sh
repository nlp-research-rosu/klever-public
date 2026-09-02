#!/usr/bin/env bash
set -u

run() {
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf '[exit %d]\n' "$status"
  return "$status"
}

printf 'Required-generation-artifact presence:\n'
for name in run-input.json metrics.json codex-last.txt codex-output.log; do
  if [[ -e "/candidate/$name" || -L "/candidate/$name" ]]; then
    stat -c '%F %a %n' "/candidate/$name"
  else
    printf 'MISSING /candidate/%s\n' "$name"
  fi
done

printf '\nCandidate top-level entries:\n'
run find /candidate -maxdepth 1 -printf '%f\t%y\t%m\t%l\n'

printf '\nRequired prompt and translator byte comparisons:\n'
run cmp -s /reference/prompt.py /candidate/prompt.py
run cmp -s /reference/py2mpy.py /candidate/py2mpy.py
run sha256sum /reference/prompt.py /candidate/prompt.py
run sha256sum /reference/py2mpy.py /candidate/py2mpy.py

printf '\nSupplied-semantics recursive content comparison:\n'
run diff --no-dereference -r /reference/reference-semantics /candidate/reference-semantics

printf '\nSupplied-semantics type/mode manifests (trusted then candidate):\n'
run find /reference/reference-semantics -printf '%P\t%y\t%m\t%l\n'
run find /candidate/reference-semantics -printf '%P\t%y\t%m\t%l\n'

printf '\nSymlink checks:\n'
run find /candidate/reference-semantics -type l -print
