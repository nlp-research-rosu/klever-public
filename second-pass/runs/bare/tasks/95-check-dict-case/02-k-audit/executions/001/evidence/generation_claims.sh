#!/usr/bin/env bash
set -u

trace=/candidate/codex-trace/2026/07/22/rollout-2026-07-22T06-13-56-019f8988-436f-7ea3-adee-6619f939ad16.jsonl

echo "===== run-input.json (untrusted claim) ====="
sed -n '1,120p' /candidate/run-input.json
echo "===== metrics.json (untrusted claim) ====="
sed -n '1,120p' /candidate/metrics.json
echo "===== codex-last.txt (untrusted claim) ====="
sed -n '1,120p' /candidate/codex-last.txt
echo "===== bounded codex-output claim excerpts ====="
rg -n -C 2 \
  'CPython smoke tests: passed|krun examples: passed|^#Top$|RESULT: KPROVE_PASSED|ASCII casing|Unicode-aware' \
  /candidate/codex-output.log | tail -120
echo "===== structured-trace terminal events (untrusted claims) ====="
rg -n '"type":"(agent_message|task_complete)"' "$trace"
rg -n \
  'CPython smoke tests: passed\\nkrun examples: passed\\n#Top' \
  "$trace" | tail -5
