#!/usr/bin/env bash
set -uo pipefail

for file in \
  /run.json \
  /task.json \
  /generation-result.json \
  /generation-evidence/invocation.json \
  /generation-evidence/metrics.json \
  /generation-evidence/usage.json
do
  echo "===== $file ====="
  sed -n '1,360p' "$file"
done

trace_file=$(find /generation-evidence/codex-trace -type f -name '*.jsonl' -print -quit)
echo "===== TRACE STRUCTURE ====="
wc -l "$trace_file"
sed -n '1,3p' "$trace_file"

echo "===== TRACE EVENT TYPES ====="
rg -o '"type":"[^"]+"' "$trace_file" | sort | uniq -c

echo "===== TRACE COMMAND/ARTIFACT INDEX ====="
rg -n \
  'exec_command|apply_patch|update_plan|kprove|kompile|krun|solution\.py|verification\.k|spec\.k|prove\.sh|#Top|WarnStuckClaimState' \
  "$trace_file"

echo "===== CODEX LOG COMMAND/RESULT INDEX ====="
rg -n \
  '^exec$|^ succeeded|^ failed|kprove|kompile|krun|#Top|WarnStuckClaimState|RESULT:' \
  /generation-evidence/codex-output.log
