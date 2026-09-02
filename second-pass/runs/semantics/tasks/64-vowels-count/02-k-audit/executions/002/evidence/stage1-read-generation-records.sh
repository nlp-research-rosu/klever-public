#!/usr/bin/env bash
set -u

printf 'DECLARED LEGACY-SELECTED-STAGE1 RECORDS (FULL SMALL RECORDS)\n'
for path in \
  /run.json \
  /task.json \
  /generation-result.json \
  /generation-evidence/invocation.json \
  /generation-evidence/metrics.json \
  /generation-evidence/usage.json \
  /generation-evidence/codex-last.txt \
  /generation-evidence/prompt.txt
do
  printf '\nFILE %s\n' "$path"
  sed -n '1,1000p' "$path"
done

printf '\nLARGE GENERATION LOG READABILITY AND BOUNDED INSPECTION\n'
wc -lc \
  /generation-evidence/codex-output.log \
  /generation-evidence/codex-trace/2026/07/23/*.jsonl
nul_count=$(LC_ALL=C tr -cd '\000' < /generation-evidence/codex-output.log | wc -c)
printf 'codex_output_nul_bytes=%d\n' "$nul_count"

printf '\nCODEX OUTPUT FIRST 40 LINES\n'
sed -n '1,40p' /generation-evidence/codex-output.log
printf '\nCODEX OUTPUT LAST 180 LINES\n'
tail -n 180 /generation-evidence/codex-output.log
printf '\nCODEX OUTPUT PROOF-RELATED MATCHES (LAST 300)\n'
rg -n -C 2 \
  'KPROVE|#Top|kprove|kompile|verification\.k|spec\.k|WarnStuck|ERROR|FAIL|PASS' \
  /generation-evidence/codex-output.log | tail -n 300
