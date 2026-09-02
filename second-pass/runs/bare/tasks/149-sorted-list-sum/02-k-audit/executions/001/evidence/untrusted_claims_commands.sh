#!/usr/bin/env bash
set -u
set -o pipefail
trap 'status=$?; printf "SCRIPT_EXIT=%s\n" "$status"' EXIT
set -x

sed -n '1,220p' /candidate/run-input.json
sed -n '1,180p' /candidate/metrics.json
sed -n '1,180p' /candidate/codex-last.txt
wc -l -c \
  /candidate/codex-output.log \
  /candidate/codex-trace/2026/07/22/rollout-2026-07-22T07-40-15-019f89d7-4b4f-7063-88a7-a0437ab8a11e.jsonl
rg -n '#Top|kprove|kompile|krun|differential|spec-vacuity|RESULT:' \
  /candidate/codex-output.log | tail -n 120
trace=/candidate/codex-trace/2026/07/22/rollout-2026-07-22T07-40-15-019f89d7-4b4f-7063-88a7-a0437ab8a11e.jsonl
python3 /audit-output/evidence/summarize_trace.py "$trace"
