#!/usr/bin/env bash
set -u

run() {
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  local rc=$?
  printf '[exit %d]\n\n' "$rc"
  return 0
}

echo "## Required provenance artifact presence"
for name in run-input.json metrics.json codex-last.txt codex-output.log; do
  if [[ -e "/candidate/$name" || -L "/candidate/$name" ]]; then
    run stat -c '%F %s bytes %n -> %N' "/candidate/$name"
  else
    printf 'MISSING /candidate/%s\n\n' "$name"
  fi
done

echo "## Candidate root artifact types"
run find /candidate -maxdepth 1 -mindepth 1 -printf '%y %f -> %l\n'

echo "## Candidate symlink check"
run find /candidate -type l -printf '%p -> %l\n'

echo "## Trusted-mode boundary"
run stat -c '%F %n' /reference/reference-semantics

echo "## Prompt and translator identity"
run cmp -s /reference/prompt.py /candidate/prompt.py
run sha256sum /reference/prompt.py /candidate/prompt.py
run cmp -s /reference/py2mpy.py /candidate/py2mpy.py
run sha256sum /reference/py2mpy.py /candidate/py2mpy.py

echo "## Recursive supplied-semantics identity"
run diff --no-dereference --recursive --brief /reference/reference-semantics /candidate/reference-semantics

echo "## Trusted semantics manifest"
run find /reference/reference-semantics -printf '%y %P -> %l\n'
run bash -c 'find /reference/reference-semantics -type f -print0 | sort -z | xargs -0 sha256sum'

echo "## Candidate semantics manifest"
run find /candidate/reference-semantics -printf '%y %P -> %l\n'
run bash -c 'find /candidate/reference-semantics -type f -print0 | sort -z | xargs -0 sha256sum'
