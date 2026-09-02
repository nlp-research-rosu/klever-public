#!/usr/bin/env bash
set -euo pipefail

generation_log=/generation-evidence/codex-output.log
trace_file=/generation-evidence/codex-trace/2026/07/25/rollout-2026-07-25T00-56-45-019f97d8-f1f4-7550-990f-b8d53c13dc66.jsonl

wc -l -c "$generation_log" "$trace_file"

for pattern in \
  '^#Top$' \
  'RESULT:' \
  'VALIDATED' \
  'WarnStuckClaimState' \
  'EXPECTED FAILURE' \
  'UNEXPECTED SUCCESS' \
  'timed out|timeout|OOM|oom_killed' \
  '\\[Error\\]| failed in | exited with code '
do
  printf 'PATTERN %s COUNT ' "$pattern"
  rg -i -c "$pattern" "$generation_log" || true
done

printf '%s\n' 'GENERATION_LOG_FIRST_30_LINES'
sed -n '1,30p' "$generation_log"
printf '%s\n' 'GENERATION_LOG_RELEVANT_TAIL'
rg -n \
  '(^#Top$|RESULT:|VALIDATED|WarnStuckClaimState|EXPECTED FAILURE|UNEXPECTED SUCCESS|\\[Error\\]| exited [0-9])' \
  "$generation_log" | tail -n 160
printf '%s\n' 'GENERATION_LOG_LAST_60_LINES'
tail -n 60 "$generation_log"
