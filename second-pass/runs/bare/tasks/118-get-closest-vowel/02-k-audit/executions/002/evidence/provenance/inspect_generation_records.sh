#!/usr/bin/env bash
set -uo pipefail

for path in \
  /run.json \
  /task.json \
  /generation-result.json \
  /generation-evidence/invocation.json \
  /generation-evidence/metrics.json \
  /generation-evidence/usage.json \
  /generation-evidence/codex-last.txt \
  /generation-evidence/prompt.txt
do
  printf 'FILE %s\n' "$path"
  sed -n '1,260p' "$path"
done

printf 'CODEX_OUTPUT_HEAD\n'
sed -n '1,60p' /generation-evidence/codex-output.log
printf 'CODEX_OUTPUT_TAIL\n'
tail -n 80 /generation-evidence/codex-output.log
printf 'CODEX_OUTPUT_KEY_EVENTS_LAST_200\n'
rg -n -i \
  'KPROVE_PASSED|#Top|error|warning|timeout|blocked|partial|semantic\.k|verification\.k|spec\.k' \
  /generation-evidence/codex-output.log | tail -n 200

printf 'TRACE_BOUNDARIES\n'
trace=/generation-evidence/codex-trace/2026/07/22/rollout-2026-07-22T06-47-27-019f89a6-f12e-78d1-90ea-0d9527fcca8d.jsonl
sed -n '1,3p' "$trace"
tail -n 3 "$trace"

printf 'EXIT_STATUS=0\n'
