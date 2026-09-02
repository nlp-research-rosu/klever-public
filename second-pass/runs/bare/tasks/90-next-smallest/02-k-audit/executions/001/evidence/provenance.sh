#!/usr/bin/env bash
set -uo pipefail

run() {
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  local status=$?
  printf '[exit %d]\n' "$status"
  return "$status"
}

printf 'Rendered mode: GENERATED_SEMANTICS\n'
if [[ -e /reference/reference-semantics || -L /reference/reference-semantics ]]; then
  printf 'INTEGRITY FAILURE: /reference/reference-semantics exists\n'
  run stat -c '%F %n -> %N' /reference/reference-semantics
else
  printf 'Boundary check: /reference/reference-semantics is absent\n'
fi

run stat -c '%F %a %U:%G %s %n -> %N' \
  /candidate/run-input.json \
  /candidate/metrics.json \
  /candidate/codex-last.txt \
  /candidate/codex-output.log \
  /candidate/codex-trace/2026/07/22/rollout-2026-07-22T06-03-01-019f897e-45c8-7f62-bf6d-98da4a9c7e73.jsonl \
  /candidate/prompt.py \
  /candidate/py2mpy.py \
  /candidate/solution.py \
  /candidate/solution.mpy \
  /candidate/semantic.k \
  /candidate/verification.k \
  /candidate/spec.k \
  /candidate/prove.sh

run cmp /candidate/prompt.py /reference/prompt.py
run cmp /candidate/py2mpy.py /reference/py2mpy.py
run sha256sum \
  /reference/prompt.py /candidate/prompt.py \
  /reference/py2mpy.py /candidate/py2mpy.py \
  /reference/canonical.py \
  /candidate/solution.py /candidate/solution.mpy \
  /candidate/semantic.k /candidate/verification.k /candidate/spec.k

run python3 -m json.tool /candidate/run-input.json
run python3 -m json.tool /candidate/metrics.json
run wc -l -c \
  /candidate/codex-output.log \
  /candidate/codex-trace/2026/07/22/rollout-2026-07-22T06-03-01-019f897e-45c8-7f62-bf6d-98da4a9c7e73.jsonl

run find /candidate -xdev -type l -print
run find /candidate -xdev -maxdepth 1 -printf '%y %f\n'
