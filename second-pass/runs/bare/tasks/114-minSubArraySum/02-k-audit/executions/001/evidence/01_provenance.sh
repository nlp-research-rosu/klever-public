#!/usr/bin/env bash
set -u

run() {
  local cmd="$1"
  printf '$ %s\n' "$cmd"
  bash -o pipefail -c "$cmd"
  local status=$?
  printf '[exit %d]\n' "$status"
  return 0
}

run "find /candidate -maxdepth 10 -printf '%y %p -> %l\n' | LC_ALL=C sort"
run "find /candidate -type l -print"
run "stat -c '%F %N' /candidate/run-input.json /candidate/metrics.json /candidate/codex-last.txt /candidate/codex-output.log /candidate/codex-trace/2026/07/22/rollout-2026-07-22T06-42-25-019f89a2-5723-72d1-9231-c4bd7aff3420.jsonl /candidate/prompt.py /candidate/py2mpy.py /candidate/solution.py /candidate/solution.mpy /candidate/semantic.k /candidate/verification.k /candidate/spec.k /candidate/prove.sh"
run "cmp -s /candidate/prompt.py /reference/prompt.py"
run "sha256sum /candidate/prompt.py /reference/prompt.py"
run "cmp -s /candidate/py2mpy.py /reference/py2mpy.py"
run "sha256sum /candidate/py2mpy.py /reference/py2mpy.py"
run "wc -c -l /candidate/run-input.json /candidate/metrics.json /candidate/codex-last.txt /candidate/codex-output.log /candidate/codex-trace/2026/07/22/rollout-2026-07-22T06-42-25-019f89a2-5723-72d1-9231-c4bd7aff3420.jsonl"
