#!/usr/bin/env bash
set -u

run() {
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  local status=$?
  printf '[exit %d]\n' "$status"
  return 0
}

run stat -c '%n|%F|mode=%a|owner=%U:%G' /reference/reference-semantics
run find /reference -maxdepth 2 -printf '%y|%p|%l\n'
run find /candidate -xdev -printf '%y|%p|%s|%l\n'
run stat -c '%n|%F|mode=%a|size=%s' \
  /candidate/run-input.json \
  /candidate/metrics.json \
  /candidate/codex-last.txt \
  /candidate/codex-output.log \
  /candidate/prompt.py \
  /candidate/py2mpy.py \
  /candidate/solution.py \
  /candidate/solution.mpy \
  /candidate/semantic.k \
  /candidate/verification.k \
  /candidate/spec.k \
  /candidate/prove.sh \
  /candidate/codex-trace/2026/07/22/rollout-2026-07-22T05-05-22-019f8949-7d00-7dc3-95ea-3b4349dee0cf.jsonl
run sha256sum \
  /candidate/run-input.json \
  /candidate/metrics.json \
  /candidate/codex-last.txt \
  /candidate/codex-output.log \
  /candidate/prompt.py \
  /candidate/py2mpy.py \
  /candidate/solution.py \
  /candidate/solution.mpy \
  /candidate/semantic.k \
  /candidate/spec.k \
  /candidate/verification.k \
  /candidate/prove.sh \
  /reference/prompt.py \
  /reference/py2mpy.py \
  /reference/canonical.py
run cmp -s /candidate/prompt.py /reference/prompt.py
run diff -u /reference/prompt.py /candidate/prompt.py
run cmp -s /candidate/py2mpy.py /reference/py2mpy.py
run diff -u /reference/py2mpy.py /candidate/py2mpy.py
run python3 -m json.tool /candidate/run-input.json
run python3 -m json.tool /candidate/metrics.json

printf '\n$ python3 /reference/py2mpy.py /tmp/audit-work/fresh/solution.py > /tmp/audit-work/fresh/regenerated-solution.mpy\n'
python3 /reference/py2mpy.py /tmp/audit-work/fresh/solution.py \
  > /tmp/audit-work/fresh/regenerated-solution.mpy
status=$?
printf '[exit %d]\n' "$status"
run cmp -s \
  /tmp/audit-work/fresh/regenerated-solution.mpy \
  /tmp/audit-work/fresh/solution.mpy
run sha256sum \
  /tmp/audit-work/fresh/regenerated-solution.mpy \
  /tmp/audit-work/fresh/solution.mpy

run kompile --version
run kprove --version
run krun --version
