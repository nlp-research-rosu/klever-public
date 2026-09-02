#!/usr/bin/env bash
set -u

printf '%s\n' '$ sed -n 1,240p /candidate/run-input.json'
sed -n '1,240p' /candidate/run-input.json
printf '[exit %d]\n' "$?"

printf '%s\n' '$ sed -n 1,240p /candidate/metrics.json'
sed -n '1,240p' /candidate/metrics.json
printf '[exit %d]\n' "$?"

printf '%s\n' '$ sed -n 1,240p /candidate/codex-last.txt'
sed -n '1,240p' /candidate/codex-last.txt
printf '[exit %d]\n' "$?"

printf '%s\n' \
  '$ rg -n -m 220 "#Top|WarnStuckClaimState|\[Error\]|RESULT:|kompile|kprove|krun" /candidate/codex-output.log'
rg -n -m 220 \
  '#Top|WarnStuckClaimState|\[Error\]|RESULT:|kompile|kprove|krun' \
  /candidate/codex-output.log
printf '[exit %d]\n' "$?"
