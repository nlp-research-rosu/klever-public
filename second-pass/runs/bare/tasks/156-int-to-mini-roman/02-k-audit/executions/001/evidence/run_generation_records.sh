#!/usr/bin/env bash
set -u

for file in \
  /run.json \
  /task.json \
  /generation-result.json \
  /generation-evidence/invocation.json \
  /generation-evidence/metrics.json \
  /generation-evidence/runtime-metrics.json \
  /generation-evidence/usage.json \
  /generation-evidence/prompt.txt \
  /generation-evidence/codex-last.txt
do
  echo "===== $file"
  sed -n '1,300p' "$file"
  echo "READ_EXIT_STATUS=$?"
done

echo '===== codex-output metadata'
wc -c -l /generation-evidence/codex-output.log
sha256sum /generation-evidence/codex-output.log

echo '===== codex-output bounded head'
sed -n '1,100p' /generation-evidence/codex-output.log

echo '===== codex-output bounded tail'
tail -n 140 /generation-evidence/codex-output.log

echo '===== codex-output proof/action index'
rg -n \
  'RESULT:|#Top|kprove|kompile|krun solution|independent Python cross-check|byte-for-byte identical|universal claim|Warning|Error' \
  /generation-evidence/codex-output.log | tail -n 240

echo "EXIT_STATUS=$?"
