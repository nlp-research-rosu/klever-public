#!/usr/bin/env bash
set -euo pipefail

printf '%s\n' 'COMMAND: wc -c required legacy-selected-stage1 records'
wc -c \
  /run.json \
  /task.json \
  /generation-result.json \
  /generation-evidence/invocation.json \
  /generation-evidence/metrics.json \
  /generation-evidence/usage.json \
  /generation-evidence/codex-last.txt \
  /generation-evidence/codex-output.log \
  /generation-evidence/prompt.txt \
  /generation-evidence/codex-trace/2026/07/22/rollout-2026-07-22T05-11-27-019f894f-0f4b-7912-adc3-c85b88e6a8cd.jsonl

printf '%s\n' 'COMMAND: read compact required JSON/text records'
sed -n '1,260p' /generation-evidence/invocation.json
sed -n '1,260p' /generation-evidence/metrics.json
sed -n '1,260p' /generation-evidence/usage.json
sed -n '1,260p' /generation-evidence/codex-last.txt
sed -n '1,320p' /generation-evidence/prompt.txt

printf '%s\n' 'COMMAND: parse every structured trace JSONL record'
python3 /audit-output/evidence/01_generation_record_summary.py

printf '%s\n' 'COMMAND: bounded salient scan of codex-output.log'
rg -n -i 'kompile|krun|kprove|#Top|WarnStuckClaimState|RESULT:' \
  /generation-evidence/codex-output.log | sed -n '1,220p'

printf 'EXIT_STATUS=0\n'
