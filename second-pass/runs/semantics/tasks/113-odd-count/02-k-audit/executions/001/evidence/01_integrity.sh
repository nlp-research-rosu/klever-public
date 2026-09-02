#!/usr/bin/env bash
set -u

run() {
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf 'EXIT_STATUS=%s\n' "$status"
}

printf 'SEMANTICS_MODE=SUPPLIED_SEMANTICS\n'
printf 'EXPECTED_TRUSTED_SEMANTICS=/reference/reference-semantics\n'
run test -d /reference/reference-semantics

printf '\nREQUIRED_PROVENANCE_ARTIFACTS\n'
for name in run-input.json metrics.json codex-last.txt codex-output.log; do
  if test -e "/candidate/$name"; then
    run stat -c '%F %n' "/candidate/$name"
  else
    printf 'MISSING /candidate/%s\n' "$name"
  fi
done

printf '\nSTRUCTURED_TRACE_CANDIDATES\n'
run find -P /candidate -maxdepth 1 -type f '(' -iname '*trace*' -o -iname '*.jsonl' -o -iname '*.json' ')' -printf '%f\n'

printf '\nSYMLINK_CHECKS\n'
run find -P /candidate -type l -printf '%p -> %l\n'
run find -P /reference/reference-semantics -type l -printf '%p -> %l\n'

printf '\nTRUSTED_ARTIFACT_IDENTITY\n'
run cmp /candidate/prompt.py /reference/prompt.py
run cmp /candidate/py2mpy.py /reference/py2mpy.py
run diff -qr --no-dereference /reference/reference-semantics /candidate/reference-semantics

printf '\nSHA256\n'
run sha256sum /candidate/prompt.py /reference/prompt.py
run sha256sum /candidate/py2mpy.py /reference/py2mpy.py
run find -P /candidate/reference-semantics -type f -print0
run find -P /reference/reference-semantics -type f -print0

printf '\nCOMPLETE_CANDIDATE_INVENTORY\n'
run find -P /candidate -printf '%y %m %s %p -> %l\n'

printf '\nCOMPLETE_REFERENCE_INVENTORY\n'
run find -P /reference -printf '%y %m %s %p -> %l\n'
