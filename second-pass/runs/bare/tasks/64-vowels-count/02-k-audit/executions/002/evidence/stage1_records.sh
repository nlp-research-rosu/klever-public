#!/usr/bin/env bash
set -euo pipefail
set -x

sed -n '1,360p' /audit-input.json
sed -n '1,240p' /audit-campaign-lock.json
sed -n '1,320p' /run.json
sed -n '1,240p' /task.json
sed -n '1,280p' /generation-result.json
sed -n '1,320p' /generation-evidence/invocation.json
sed -n '1,240p' /generation-evidence/metrics.json
sed -n '1,280p' /generation-evidence/usage.json
sed -n '1,220p' /generation-evidence/codex-last.txt
sed -n '1,320p' /generation-evidence/prompt.txt
python3 /audit-output/evidence/stage1_integrity.py
python3 /audit-output/evidence/generation_trace_summary.py
rg -n -m 240 'kompile|kprove|krun|#Top|WarnStuckClaimState|RESULT:' \
  /generation-evidence/codex-output.log

