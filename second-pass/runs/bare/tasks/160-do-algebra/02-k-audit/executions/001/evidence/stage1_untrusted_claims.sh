#!/usr/bin/env bash
set -u

trace_path=$(find /candidate/codex-trace -type f -name '*.jsonl' -print -quit)

echo "== run-input.json (untrusted claim) =="
sed -n '1,120p' /candidate/run-input.json
echo "== metrics.json (untrusted claim) =="
sed -n '1,120p' /candidate/metrics.json
echo "== codex-last.txt (untrusted claim) =="
sed -n '1,120p' /candidate/codex-last.txt
echo "== selected codex-output.log lines (bounded) =="
rg -n '#Top|kprove|kompile|mutation|WarnStuck|Process exited|exit code|ERROR' \
  /candidate/codex-output.log |
  awk '{ print substr($0, 1, 700) }' |
  sed -n '1,160p'
echo "== codex-output.log tail =="
tail -40 /candidate/codex-output.log
echo "== structured generation trace endpoints (bounded) =="
sed -n '1p' "$trace_path" | awk '{ print substr($0, 1, 1000) }'
tail -1 "$trace_path" | awk '{ print substr($0, 1, 1000) }'
echo "== selected structured trace lines (bounded) =="
rg -n '#Top|kprove|kompile|mutation|WarnStuck|Process exited|exit code|ERROR' \
  "$trace_path" |
  awk '{ print substr($0, 1, 700) }' |
  sed -n '1,160p'
