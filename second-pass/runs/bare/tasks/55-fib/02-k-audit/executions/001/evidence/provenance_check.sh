#!/usr/bin/env bash
set -uo pipefail

status=0

printf '%s\n' 'SEMANTICS_MODE: GENERATED_SEMANTICS'
if [[ -e /reference/reference-semantics || -L /reference/reference-semantics ]]; then
  printf '%s\n' 'ERROR: /reference/reference-semantics exists'
  ls -ld /reference/reference-semantics
  status=1
else
  printf '%s\n' 'OK: /reference/reference-semantics is absent'
fi

printf '%s\n' 'CANDIDATE_ARTIFACT_TYPES:'
find /candidate -maxdepth 4 -printf '%y %p -> %l\n' | sort

for pair in \
  '/reference/prompt.py /candidate/prompt.py' \
  '/reference/py2mpy.py /candidate/py2mpy.py'
do
  read -r trusted candidate <<< "$pair"
  printf 'COMPARE_COMMAND: cmp -s %q %q\n' "$trusted" "$candidate"
  cmp -s "$trusted" "$candidate"
  pair_status=$?
  printf 'COMPARE_EXIT_STATUS: %d\n' "$pair_status"
  sha256sum "$trusted" "$candidate"
  if (( pair_status != 0 )); then
    diff -u "$trusted" "$candidate" || true
    status=1
  fi
done

printf 'FINAL_STATUS: %d\n' "$status"
exit "$status"
