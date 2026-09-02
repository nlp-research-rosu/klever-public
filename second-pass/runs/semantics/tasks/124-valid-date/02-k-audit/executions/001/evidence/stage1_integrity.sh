#!/usr/bin/env bash
set -uo pipefail

status=0

for required in run-input.json metrics.json codex-last.txt codex-output.log; do
  if [[ -e "/candidate/${required}" || -L "/candidate/${required}" ]]; then
    printf 'PRESENT required provenance artifact: %s (%s)\n' \
      "${required}" "$(stat -c '%F' "/candidate/${required}")"
  else
    printf 'MISSING required provenance artifact: %s\n' "${required}"
    status=1
  fi
done

printf '\nCandidate top-level entries and types:\n'
find /candidate -maxdepth 1 -mindepth 1 -printf '%y %f -> %l\n' | sort

printf '\nTrusted/candidate hashes:\n'
sha256sum \
  /reference/prompt.py /candidate/prompt.py \
  /reference/py2mpy.py /candidate/py2mpy.py

cmp /reference/prompt.py /candidate/prompt.py
prompt_status=$?
printf 'prompt byte comparison exit: %d\n' "${prompt_status}"
(( prompt_status == 0 )) || status=1

cmp /reference/py2mpy.py /candidate/py2mpy.py
translator_status=$?
printf 'translator byte comparison exit: %d\n' "${translator_status}"
(( translator_status == 0 )) || status=1

printf '\nReference-semantics trees (type, relative path, symlink target):\n'
(
  cd /reference/reference-semantics
  find . -printf 'trusted %y %p -> %l\n' | sort
)
(
  cd /candidate/reference-semantics
  find . -printf 'candidate %y %p -> %l\n' | sort
)

diff -r --no-dereference \
  /reference/reference-semantics \
  /candidate/reference-semantics
semantics_status=$?
printf 'reference-semantics recursive comparison exit: %d\n' "${semantics_status}"
(( semantics_status == 0 )) || status=1

printf '\nOverall integrity-script exit reflects all required provenance artifacts.\n'
exit "${status}"
