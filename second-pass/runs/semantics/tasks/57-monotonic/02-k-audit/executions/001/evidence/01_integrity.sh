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

printf 'Rendered mode: SUPPLIED_SEMANTICS\n'
run test -d /reference/reference-semantics
run test -e /reference/reference-semantics
run find /reference/reference-semantics -printf '%y %P\n'
run find /candidate/reference-semantics -printf '%y %P\n'
run find /candidate/reference-semantics -type l -printf '%P -> %l\n'
run diff --no-dereference --recursive --brief /reference/reference-semantics /candidate/reference-semantics

for pair in \
  /reference/prompt.py:/candidate/prompt.py \
  /reference/py2mpy.py:/candidate/py2mpy.py
do
  trusted=${pair%%:*}
  submitted=${pair#*:}
  run cmp --silent "$trusted" "$submitted"
  run sha256sum "$trusted" "$submitted"
done

for artifact in \
  run-input.json \
  metrics.json \
  codex-last.txt \
  codex-output.log
do
  run test -f "/candidate/$artifact"
done

printf '\nCandidate top-level inventory:\n'
run find /candidate -maxdepth 1 -printf '%y %f\n'
