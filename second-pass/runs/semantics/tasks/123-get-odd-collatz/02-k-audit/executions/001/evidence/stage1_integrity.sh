#!/usr/bin/env bash
set -u

run() {
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  local rc=$?
  printf '[exit %d]\n' "$rc"
  return 0
}

printf 'Stage 1 provenance and supplied-semantics integrity checks\n'
printf 'Audit date (UTC): '
run date -u +%Y-%m-%dT%H:%M:%SZ

printf '\nCandidate top-level manifest (including types and links)\n'
run find /candidate -maxdepth 2 -printf '%P\t%y\t%m\t%s\t%l\n'

printf '\nRequired and claim/evidence artifact presence\n'
for artifact in \
  run-input.json metrics.json codex-last.txt codex-output.log \
  prompt.py py2mpy.py solution.py solution.mpy spec.k verification.k; do
  if [[ -e "/candidate/$artifact" || -L "/candidate/$artifact" ]]; then
    run stat -c '%n|type=%F|mode=%a|size=%s' "/candidate/$artifact"
  else
    printf 'MISSING /candidate/%s\n' "$artifact"
  fi
done

printf '\nStructured-generation-trace filename search\n'
run find /candidate -maxdepth 2 -type f \
  \( -iname '*trace*' -o -iname '*.jsonl' -o -iname '*generation*.json' \) -print

printf '\nCandidate symlink search (any symlink is relevant)\n'
run find /candidate -type l -printf '%p -> %l\n'

printf '\nTrusted/candidate prompt comparison\n'
run sha256sum /reference/prompt.py /candidate/prompt.py
run cmp -s /reference/prompt.py /candidate/prompt.py

printf '\nTrusted/candidate translator comparison\n'
run sha256sum /reference/py2mpy.py /candidate/py2mpy.py
run cmp -s /reference/py2mpy.py /candidate/py2mpy.py

printf '\nTrusted supplied-semantics manifest\n'
run find /reference/reference-semantics -printf '%P\t%y\t%m\t%s\t%l\n'

printf '\nCandidate supplied-semantics manifest\n'
run find /candidate/reference-semantics -printf '%P\t%y\t%m\t%s\t%l\n'

printf '\nSupplied-semantics recursive byte/type comparison\n'
run diff --no-dereference -qr \
  /reference/reference-semantics /candidate/reference-semantics

printf '\nSupplied-semantics file hashes (trusted then candidate)\n'
run bash -c 'find /reference/reference-semantics -type f -print0 | sort -z | xargs -0 sha256sum'
run bash -c 'find /candidate/reference-semantics -type f -print0 | sort -z | xargs -0 sha256sum'
