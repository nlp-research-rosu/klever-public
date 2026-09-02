#!/usr/bin/env bash
set -uo pipefail

printf '%s\n' '--- /candidate/run-input.json ---'
sed -n '1,240p' /candidate/run-input.json
printf '%s\n' '--- /candidate/metrics.json ---'
sed -n '1,240p' /candidate/metrics.json
printf '%s\n' '--- /candidate/codex-last.txt ---'
sed -n '1,240p' /candidate/codex-last.txt
printf '%s\n' '--- /candidate/codex-output.log size ---'
wc -lc /candidate/codex-output.log
printf '%s\n' '--- bounded outcome-bearing lines from codex-output.log ---'
rg -n \
  'KOMPILE_EXIT=|KPROVE_EXIT=|PROVE_SH_EXIT=|^#Top$|WarnStuckClaimState|Expected failure:|RESULT: KPROVE' \
  /candidate/codex-output.log | tail -n 160
