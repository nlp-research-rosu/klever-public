#!/usr/bin/env bash
set +e

echo '$ nl -ba /candidate/run-input.json /candidate/metrics.json /candidate/codex-last.txt'
for artifact in \
  /candidate/run-input.json \
  /candidate/metrics.json \
  /candidate/codex-last.txt
do
  echo "===== $artifact ====="
  nl -ba "$artifact"
done
echo "exit=$?"

echo '$ wc -c and sha256sum large untrusted logs/traces'
wc -c \
  /candidate/codex-output.log \
  /candidate/codex-trace/2026/07/22/*.jsonl
sha256sum \
  /candidate/codex-output.log \
  /candidate/codex-trace/2026/07/22/*.jsonl
echo "exit=$?"

echo '$ bounded generation-log claims'
rg -n -m 40 \
  'kprove spec.k|#Top|RESULT:|successfully ran|universal claim|semantic' \
  /candidate/codex-output.log | tail -n 40
echo "exit=$?"

echo '$ structured trace top-level event-type token counts'
sed -n 's/.*"type":"\([^"]*\)".*/\1/p' \
  /candidate/codex-trace/2026/07/22/*.jsonl | sort | uniq -c
echo "exit=$?"

echo '$ bounded structured-trace terminal claims'
rg -n -m 20 'task_complete|KPROVE_PASSED|#Top' \
  /candidate/codex-trace/2026/07/22/*.jsonl | tail -n 20
echo "exit=$?"
