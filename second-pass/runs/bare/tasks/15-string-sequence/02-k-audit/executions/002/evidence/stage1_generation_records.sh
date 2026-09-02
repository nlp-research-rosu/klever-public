#!/usr/bin/env bash
set -u

printf 'COMMAND: bash /audit-output/evidence/stage1_generation_records.sh\n'
for path in \
  /run.json \
  /task.json \
  /generation-result.json \
  /generation-evidence/invocation.json \
  /generation-evidence/metrics.json \
  /generation-evidence/usage.json \
  /generation-evidence/prompt.txt \
  /generation-evidence/codex-last.txt
do
  printf '\nRECORD: %s\n' "$path"
  sed -n '1,500p' "$path"
done

printf '\nHistorical-only records present but not required by legacy-selected-stage1\n'
for path in \
  /generation-evidence/legacy-metrics.json \
  /generation-evidence/legacy-run-input.json
do
  printf 'RECORD: %s\n' "$path"
  sed -n '1,300p' "$path"
done
if [[ -e /generation-evidence/runtime-metrics.json ]]; then
  printf 'runtime-metrics.json=present\n'
else
  printf 'runtime-metrics.json=absent-as-permitted-for-historical-layout\n'
fi

printf '\nBounded inspection of large plain generation output\n'
wc -lc /generation-evidence/codex-output.log
printf 'OUTPUT_HEAD\n'
sed -n '1,100p' /generation-evidence/codex-output.log
printf 'OUTPUT_PROOF_AND_ARTIFACT_EVENTS\n'
rg -n \
  'kompile|krun|kprove|#Top|WarnStuckClaimState|solution\\.mpy|semantic\\.k|verification\\.k|spec\\.k|RESULT:' \
  /generation-evidence/codex-output.log \
  | sed -n '1,500p'
printf 'OUTPUT_TAIL\n'
tail -n 120 /generation-evidence/codex-output.log

printf '\nStructured trace parsing is recorded separately in generation-trace-summary.log\n'
wc -lc /generation-evidence/codex-trace/2026/07/22/*.jsonl
printf 'SCRIPT_EXIT=0\n'
