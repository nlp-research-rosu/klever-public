#!/usr/bin/env bash
set -uo pipefail

overall=0

printf 'COMMAND: find /candidate -maxdepth 2 -printf <type/path/link> | sort\n'
find /candidate -maxdepth 2 -printf '%y %p -> %l\n' | sort
status=$?
printf 'EXIT_STATUS: %d\n\n' "$status"
(( status == 0 )) || overall=1

printf 'COMMAND: find /candidate -type l -printf <path/link> | sort\n'
find /candidate -type l -printf '%p -> %l\n' | sort
status=$?
printf 'EXIT_STATUS: %d\n\n' "$status"
(( status == 0 )) || overall=1

printf 'COMMAND: test ! -e /reference/reference-semantics && test ! -L /reference/reference-semantics\n'
test ! -e /reference/reference-semantics && test ! -L /reference/reference-semantics
status=$?
printf 'EXIT_STATUS: %d\n\n' "$status"
(( status == 0 )) || overall=1

printf 'COMMAND: cmp -s /candidate/prompt.py /reference/prompt.py\n'
cmp -s /candidate/prompt.py /reference/prompt.py
status=$?
printf 'EXIT_STATUS: %d\n\n' "$status"
(( status == 0 )) || overall=1

printf 'COMMAND: cmp -s /candidate/py2mpy.py /reference/py2mpy.py\n'
cmp -s /candidate/py2mpy.py /reference/py2mpy.py
status=$?
printf 'EXIT_STATUS: %d\n\n' "$status"
(( status == 0 )) || overall=1

printf 'COMMAND: sha256sum <candidate/trusted metadata and provenance files>\n'
sha256sum \
  /candidate/prompt.py /reference/prompt.py \
  /candidate/py2mpy.py /reference/py2mpy.py \
  /candidate/run-input.json /candidate/metrics.json \
  /candidate/codex-last.txt /candidate/codex-output.log \
  /candidate/codex-trace/2026/07/22/rollout-2026-07-22T05-14-42-019f8952-09f1-7763-a225-2b722207253e.jsonl
status=$?
printf 'EXIT_STATUS: %d\n\n' "$status"
(( status == 0 )) || overall=1

printf 'COMMAND: required source artifact regular-file checks\n'
for path in \
  /candidate/run-input.json /candidate/metrics.json \
  /candidate/codex-last.txt /candidate/codex-output.log \
  /candidate/prompt.py /candidate/py2mpy.py \
  /candidate/solution.py /candidate/solution.mpy \
  /candidate/semantic.k /candidate/verification.k \
  /candidate/spec.k /candidate/prove.sh
do
  if [[ -f "$path" && ! -L "$path" ]]; then
    printf 'OK regular non-symlink: %s\n' "$path"
  else
    printf 'FAIL required regular non-symlink: %s\n' "$path"
    overall=1
  fi
done
printf 'EXIT_STATUS: %d\n' "$overall"
exit "$overall"
