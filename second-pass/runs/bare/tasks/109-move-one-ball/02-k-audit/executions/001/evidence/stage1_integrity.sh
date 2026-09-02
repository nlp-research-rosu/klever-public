#!/usr/bin/env bash
set -uo pipefail

log=/audit-output/evidence/stage1_integrity.log
exec > >(tee "$log") 2>&1

run() {
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf 'EXIT_STATUS: %d\n' "$status"
  return 0
}

run stat -c '%F %s %n' \
  /candidate/run-input.json \
  /candidate/metrics.json \
  /candidate/codex-last.txt \
  /candidate/codex-output.log \
  /candidate/prompt.py \
  /candidate/py2mpy.py \
  /candidate/solution.py \
  /candidate/solution.mpy \
  /candidate/mpy-syntax.k \
  /candidate/semantic.k \
  /candidate/verification.k \
  /candidate/spec.k \
  /candidate/prove.sh \
  /reference/prompt.py \
  /reference/py2mpy.py \
  /reference/canonical.py

run find /candidate -type l -print
run find /reference -type l -print
run cmp -s /candidate/prompt.py /reference/prompt.py
run cmp -s /candidate/py2mpy.py /reference/py2mpy.py
run sha256sum \
  /candidate/run-input.json \
  /candidate/metrics.json \
  /candidate/codex-last.txt \
  /candidate/codex-output.log \
  /candidate/codex-trace/2026/07/22/rollout-2026-07-22T06-34-43-019f899b-497c-79f0-a88b-47cd648deece.jsonl \
  /candidate/prompt.py \
  /candidate/py2mpy.py \
  /candidate/solution.py \
  /candidate/solution.mpy \
  /candidate/mpy-syntax.k \
  /candidate/semantic.k \
  /candidate/verification.k \
  /candidate/spec.k \
  /candidate/prove.sh \
  /reference/prompt.py \
  /reference/py2mpy.py \
  /reference/canonical.py

if [[ -e /reference/reference-semantics || -L /reference/reference-semantics ]]; then
  printf 'BOUNDARY_ERROR: /reference/reference-semantics exists\n'
  run stat -c '%F %n' /reference/reference-semantics
else
  printf 'BOUNDARY_OK: /reference/reference-semantics is absent\n'
fi

run python3 -m json.tool /candidate/run-input.json
run python3 -m json.tool /candidate/metrics.json

