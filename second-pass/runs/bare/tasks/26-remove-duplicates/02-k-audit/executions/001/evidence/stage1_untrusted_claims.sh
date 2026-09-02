#!/usr/bin/env bash
set -u

trace=/candidate/codex-trace/2026/07/22/rollout-2026-07-22T04-26-37-019f8926-01ea-7c62-b9eb-477c716491b7.jsonl

printf '%s\n' '--- run-input.json (untrusted claim) ---'
sed -n '1,120p' /candidate/run-input.json

printf '%s\n' '--- metrics.json (untrusted claim) ---'
sed -n '1,120p' /candidate/metrics.json

printf '%s\n' '--- codex-last.txt (untrusted claim) ---'
sed -n '1,120p' /candidate/codex-last.txt

printf '%s\n' '--- artifact line counts ---'
wc -l -c \
  /candidate/codex-output.log \
  "$trace"

printf '%s\n' '--- bounded proof-related generation-log claims ---'
rg -n \
  'kprove|kompile|krun|#Top|WarnStuckClaimState|RESULT:|prove\.sh' \
  /candidate/codex-output.log \
  | tail -n 120 \
  | cut -c1-500

printf '%s\n' '--- bounded trace endpoints ---'
head -n 2 "$trace" | cut -c1-500
tail -n 3 "$trace" | cut -c1-500

printf '%s\n' '--- bounded proof-related structured-trace claims ---'
rg -n \
  'kprove|#Top|WarnStuckClaimState|RESULT: KPROVE_PASSED' \
  "$trace" \
  | tail -n 80 \
  | cut -c1-500
