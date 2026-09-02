#!/usr/bin/env bash
set -uo pipefail

for path in \
  /candidate/run-input.json \
  /candidate/metrics.json \
  /candidate/codex-last.txt
do
  echo "BEGIN $path"
  sed -n '1,240p' "$path"
  echo "END $path"
done

echo "CODEX_OUTPUT_METADATA"
wc -lc /candidate/codex-output.log
sha256sum /candidate/codex-output.log

echo "CODEX_OUTPUT_HEAD"
sed -n '1,20p' /candidate/codex-output.log | cut -c1-500

echo "CODEX_OUTPUT_RELEVANT_TAIL"
rg -n -i \
  '#Top|WarnStuckClaimState|EXPECTED_FAILURE|kprove|sortKeyVS|oracle|mutation|RESULT:' \
  /candidate/codex-output.log \
  | tail -n 160 \
  | cut -c1-1000

echo "CODEX_OUTPUT_TAIL"
tail -n 30 /candidate/codex-output.log | cut -c1-1000
