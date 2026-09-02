#!/usr/bin/env bash
set -u
set -x

sed -n '1,240p' /candidate/run-input.json
sed -n '1,240p' /candidate/metrics.json
sed -n '1,240p' /candidate/codex-last.txt

wc -l -c /candidate/codex-output.log
sed -n '1,70p' /candidate/codex-output.log
rg -n -m 120 \
  'kompile|krun|kprove|#Top|EXIT|RESULT:|WarnStuck|semantic-kompiled|prove\\.sh' \
  /candidate/codex-output.log
tail -70 /candidate/codex-output.log

python3 /audit-output/evidence/summarize_generation_trace.py
