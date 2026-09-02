#!/usr/bin/env bash
set -euo pipefail

trace=$(find /candidate/codex-trace -type f -name '*.jsonl' -print -quit)

printf 'run-input.json\n'
sed -n '1,120p' /candidate/run-input.json
printf 'metrics.json\n'
sed -n '1,120p' /candidate/metrics.json
printf 'codex-last.txt\n'
sed -n '1,120p' /candidate/codex-last.txt

printf 'provenance sizes and hashes\n'
wc -lc /candidate/codex-output.log "$trace"
sha256sum /candidate/codex-output.log "$trace"

python3 /audit-output/evidence/trace_summary.py

printf 'codex-output selected terminal claims\n'
rg -n '^(VALIDATED|RESULT:)|Actual proof result:|mismatches=0|EXPECTED_FAILURE|Both positive proof commands print' /candidate/codex-output.log | tail -n 80
