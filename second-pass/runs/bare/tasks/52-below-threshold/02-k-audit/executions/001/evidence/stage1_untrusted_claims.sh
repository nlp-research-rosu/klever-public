#!/usr/bin/env bash
set -u

for path in \
  /candidate/run-input.json \
  /candidate/metrics.json \
  /candidate/codex-last.txt; do
  echo "===== $path ====="
  nl -ba "$path"
done

path=/candidate/codex-output.log
echo "===== $path metadata ====="
wc -l -c "$path"
sha256sum "$path"
echo "===== first 120 lines ====="
sed -n '1,120p' "$path"
echo "===== proof/build/result claim lines ====="
rg -n -C 2 \
  'kompile|kprove|krun|#Top|WarnStuckClaimState|EXIT|RESULT:|KPROVE_PASSED|proof|vacu' \
  "$path" || true
echo "===== last 180 lines ====="
tail -n 180 "$path"
