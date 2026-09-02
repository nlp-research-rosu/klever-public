#!/usr/bin/env bash
set -uo pipefail

trace=$(find /candidate/codex-trace -type f -name '*.jsonl' | sort | head -n 1)

printf 'RUN_INPUT\n'
python3 -m json.tool --sort-keys /candidate/run-input.json
printf 'METRICS\n'
python3 -m json.tool --sort-keys /candidate/metrics.json
printf 'CODEX_LAST\n'
sed -n '1,80p' /candidate/codex-last.txt
printf 'TRACE_VALIDATION_AND_TYPE_COUNTS\n'
python3 /audit-output/evidence/summarize_trace.py "$trace"
printf 'CODEX_OUTPUT_RELEVANT_FINAL_CLAIMS\n'
rg -n '#Top|exhaustive Python cross-check|RESULT: KPROVE_PASSED|full reproducibility script' \
  /candidate/codex-output.log | tail -n 40
