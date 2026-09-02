#!/usr/bin/env bash
set -u
set -o pipefail
PS4='+ command: '
set -x

python3 /audit-output/evidence/02_generation_trace_summary.py
printf 'trace_summary_exit=%s\n' "$?"

wc -lc \
  /generation-evidence/codex-output.log \
  /generation-evidence/codex-trace/2026/07/25/rollout-2026-07-25T02-26-36-019f982b-3454-72a0-9280-99e7bcf6de86.jsonl
printf 'size_check_exit=%s\n' "$?"

sed -n '1,80p' /generation-evidence/codex-output.log
printf 'codex_output_head_exit=%s\n' "$?"
tail -n 120 /generation-evidence/codex-output.log
printf 'codex_output_tail_exit=%s\n' "$?"

sed -n '1,260p' /run.json
sed -n '1,220p' /task.json
sed -n '1,240p' /generation-result.json
sed -n '1,260p' /generation-evidence/invocation.json
sed -n '1,180p' /generation-evidence/metrics.json
sed -n '1,180p' /generation-evidence/runtime-metrics.json
sed -n '1,220p' /generation-evidence/usage.json
sed -n '1,220p' /generation-evidence/codex-last.txt
sed -n '1,260p' /generation-evidence/prompt.txt
printf 'generation_records_read_exit=%s\n' "$?"
