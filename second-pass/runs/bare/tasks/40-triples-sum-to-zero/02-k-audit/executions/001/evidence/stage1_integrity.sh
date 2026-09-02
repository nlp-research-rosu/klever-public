#!/usr/bin/env bash
set -u

run() {
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  local status=$?
  printf '[exit %d]\n' "$status"
  return "$status"
}

overall=0
run stat -c '%F %a %n' \
  /candidate /reference \
  /reference/canonical.py /reference/prompt.py /reference/py2mpy.py \
  || overall=1

printf '\n$ mode boundary check: test ! -e /reference/reference-semantics && test ! -L /reference/reference-semantics\n'
if [[ ! -e /reference/reference-semantics && ! -L /reference/reference-semantics ]]; then
  printf 'GENERATED_SEMANTICS boundary satisfied: reference-semantics absent\n'
  printf '[exit 0]\n'
else
  printf 'GENERATED_SEMANTICS boundary breached: reference-semantics present\n'
  printf '[exit 1]\n'
  overall=1
fi

run cmp -s /reference/prompt.py /candidate/prompt.py || overall=1
run sha256sum /reference/prompt.py /candidate/prompt.py
run cmp -s /reference/py2mpy.py /candidate/py2mpy.py || overall=1
run sha256sum /reference/py2mpy.py /candidate/py2mpy.py
run find /candidate -type l -printf '%p -> %l\n'
run find /candidate -maxdepth 2 -printf '%y %m %p -> %l\n'
run wc -l -c \
  /candidate/codex-output.log \
  /candidate/codex-trace/2026/07/22/rollout-2026-07-22T04-48-20-019f8939-e4d8-7700-b6aa-22ebe556bb82.jsonl
run sha256sum \
  /candidate/run-input.json /candidate/metrics.json \
  /candidate/codex-last.txt /candidate/codex-output.log \
  /candidate/codex-trace/2026/07/22/rollout-2026-07-22T04-48-20-019f8939-e4d8-7700-b6aa-22ebe556bb82.jsonl

printf '\n[script exit %d]\n' "$overall"
exit "$overall"
