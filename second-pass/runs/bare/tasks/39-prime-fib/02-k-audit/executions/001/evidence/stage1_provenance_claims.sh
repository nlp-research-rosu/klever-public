#!/usr/bin/env bash
set -u
set -o pipefail
set -x

sed -n '1,240p' /candidate/run-input.json
sed -n '1,240p' /candidate/metrics.json
sed -n '1,240p' /candidate/codex-last.txt

printf '\nBOUNDED_GENERATION_LOG_CLAIMS\n'
rg -n \
  'Both positive kprove|Both `kprove`|#Top|RESULT: KPROVE|completed with exit code 0|all eleven claims' \
  /candidate/codex-output.log | tail -n 120

trace=$(find -P /candidate/codex-trace -type f -name '*.jsonl' -print -quit)
printf '\nSTRUCTURED_TRACE=%s\n' "$trace"
sha256sum "$trace"
printf 'TRACE_EVENT_TYPE_COUNTS\n'
rg -o '"type":"[^"]+"' "$trace" | sort | uniq -c | head -n 80
printf 'TRACE_COMPLETION_CLAIMS\n'
rg -n '"type":"task_complete"|RESULT: KPROVE_PASSED' "$trace" | tail -n 8

printf 'SCRIPT_EXIT=0\n'
