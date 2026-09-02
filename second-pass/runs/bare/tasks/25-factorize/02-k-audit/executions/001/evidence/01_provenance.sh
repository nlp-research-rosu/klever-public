#!/usr/bin/env bash
set -uo pipefail

run() {
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  local status=$?
  printf '[exit_status=%d]\n' "$status"
}

echo "AUDITOR PROVENANCE CHECK"
run date -u '+%Y-%m-%dT%H:%M:%SZ'
run kompile --version
run kprove --version
run find -P /candidate -maxdepth 8 -printf '%y %s %p\n'
run find -P /reference -maxdepth 4 -printf '%y %s %p\n'
run sha256sum \
  /reference/prompt.py /candidate/prompt.py \
  /reference/py2mpy.py /candidate/py2mpy.py \
  /reference/canonical.py \
  /candidate/solution.py /candidate/solution.mpy \
  /candidate/semantic.k /candidate/verification.k /candidate/spec.k \
  /candidate/run-input.json /candidate/metrics.json \
  /candidate/codex-last.txt /candidate/codex-output.log \
  /candidate/codex-trace/2026/07/22/rollout-2026-07-22T04-26-36-019f8925-fce7-7f52-b753-b35e7b37f1fe.jsonl
run cmp /reference/prompt.py /candidate/prompt.py
run cmp /reference/py2mpy.py /candidate/py2mpy.py
run test ! -e /reference/reference-semantics
run python3 -m json.tool /candidate/run-input.json
run python3 -m json.tool /candidate/metrics.json
run wc -l -c /candidate/codex-output.log \
  /candidate/codex-trace/2026/07/22/rollout-2026-07-22T04-26-36-019f8925-fce7-7f52-b753-b35e7b37f1fe.jsonl

echo '$ sed -n 1,$p /candidate/codex-output.log >/dev/null'
sed -n '1,$p' /candidate/codex-output.log >/dev/null
printf '[exit_status=%d]\n' "$?"

echo '$ python3 -c "parse every JSONL record" TRACE >/dev/null'
python3 -c 'import json, pathlib, sys; [json.loads(line) for line in pathlib.Path(sys.argv[1]).open()]' \
  /candidate/codex-trace/2026/07/22/rollout-2026-07-22T04-26-36-019f8925-fce7-7f52-b753-b35e7b37f1fe.jsonl >/dev/null
printf '[exit_status=%d]\n' "$?"

echo "UNTRUSTED GENERATION CLAIM EXCERPT"
run rg -n --no-heading \
  'WarnTrivialClaim|WarnStuckClaimState|#Top|All 26 positive claims|broad ground proof partition' \
  /candidate/codex-output.log /candidate/NOTES.md /candidate/codex-last.txt
