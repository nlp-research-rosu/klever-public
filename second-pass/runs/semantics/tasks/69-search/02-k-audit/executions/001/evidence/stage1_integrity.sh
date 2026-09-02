#!/usr/bin/env bash
set -u

run() {
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf '[exit %d]\n' "$status"
}

run find /candidate -maxdepth 4 -printf '%y %p -> %l\n'
run find /reference -maxdepth 4 -printf '%y %p -> %l\n'

for artifact in run-input.json metrics.json codex-last.txt codex-output.log; do
  run test -f "/candidate/$artifact"
done

printf '\nStructured trace candidates:\n'
run find /candidate -maxdepth 2 -type f '(' -iname '*trace*' -o -iname '*.jsonl' ')'

run cmp -s /candidate/prompt.py /reference/prompt.py
run cmp -s /candidate/py2mpy.py /reference/py2mpy.py
run diff --no-dereference --recursive --brief /reference/reference-semantics /candidate/reference-semantics

printf '\nSHA-256 checksums for candidate/trusted prompt and translator:\n'
run sha256sum /candidate/prompt.py /reference/prompt.py /candidate/py2mpy.py /reference/py2mpy.py

printf '\nSemantics entry inventory with type, size, and SHA-256:\n'
while IFS= read -r trusted; do
  relative=${trusted#/reference/reference-semantics/}
  candidate="/candidate/reference-semantics/$relative"
  printf '%s\t' "$relative"
  stat --printf='trusted=%F,%s\t' "$trusted"
  stat --printf='candidate=%F,%s\t' "$candidate"
  sha256sum "$trusted" "$candidate" | awk '{printf "%s%s", sep, $1; sep=","} END {print ""}'
done < <(find /reference/reference-semantics -type f | sort)
