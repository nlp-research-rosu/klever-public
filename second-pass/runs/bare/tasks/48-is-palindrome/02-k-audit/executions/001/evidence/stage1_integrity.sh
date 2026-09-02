#!/usr/bin/env bash
set -uo pipefail

run() {
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@" 2>&1
  local status=$?
  printf '[exit %d]\n' "$status"
  return 0
}

run find -P /candidate -maxdepth 1 -printf '%y\t%s\t%f\t%l\n'
run find -P /reference -maxdepth 1 -printf '%y\t%s\t%f\t%l\n'
run test ! -e /reference/reference-semantics
run test ! -L /reference/reference-semantics
run cmp -s /candidate/prompt.py /reference/prompt.py
run cmp -s /candidate/py2mpy.py /reference/py2mpy.py
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
  /candidate/verification.k \
  /candidate/spec.k \
  /candidate/prove.sh \
  /reference/prompt.py \
  /reference/canonical.py \
  /reference/py2mpy.py
run wc -cl \
  /candidate/run-input.json \
  /candidate/metrics.json \
  /candidate/codex-last.txt \
  /candidate/codex-output.log \
  /candidate/codex-trace/2026/07/22/rollout-2026-07-22T05-00-02-019f8944-9a29-7571-b7ea-8c931ba796a8.jsonl
run python3 -m json.tool /candidate/run-input.json
run python3 -m json.tool /candidate/metrics.json
run sed -n 1,200p /candidate/codex-last.txt
run rg -n \
  'RESULT:|#Top|WarnStuck|kompile|kprove|krun|semantic\\.k|verification\\.k|spec\\.k|solution\\.mpy|solution\\.py' \
  /candidate/codex-output.log
run python3 /audit-output/evidence/inspect_generation_trace.py \
  /candidate/codex-trace/2026/07/22/rollout-2026-07-22T05-00-02-019f8944-9a29-7571-b7ea-8c931ba796a8.jsonl
run kompile --version
run kprove --version
