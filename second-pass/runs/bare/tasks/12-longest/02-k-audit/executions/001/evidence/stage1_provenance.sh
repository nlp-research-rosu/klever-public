#!/usr/bin/env bash
set -euo pipefail

echo '$ stat and hash trusted/candidate inputs'
stat -c '%F %a %s %n' \
  /candidate/run-input.json \
  /candidate/metrics.json \
  /candidate/codex-last.txt \
  /candidate/codex-output.log \
  /candidate/prompt.py \
  /candidate/py2mpy.py \
  /candidate/solution.py \
  /candidate/solution.mpy \
  /candidate/semantic.k \
  /candidate/verification.k \
  /candidate/spec.k \
  /candidate/prove.sh \
  /reference/prompt.py \
  /reference/canonical.py \
  /reference/py2mpy.py
sha256sum \
  /candidate/prompt.py /reference/prompt.py \
  /candidate/py2mpy.py /reference/py2mpy.py

echo '$ compare candidate prompt and translator with trusted files'
cmp /candidate/prompt.py /reference/prompt.py
echo "prompt_cmp_exit=$?"
cmp /candidate/py2mpy.py /reference/py2mpy.py
echo "translator_cmp_exit=$?"

echo '$ enforce GENERATED_SEMANTICS mount boundary'
if [[ -e /reference/reference-semantics || -L /reference/reference-semantics ]]; then
  echo 'ERROR: /reference/reference-semantics exists'
  exit 90
fi
echo 'reference/reference-semantics: absent as required'

echo '$ inventory candidate top level and trace types'
find /candidate -maxdepth 2 -printf '%y %p -> %l\n' | sort
find /candidate/codex-trace -printf '%y %p -> %l\n' | sort

echo '$ read untrusted run metadata'
sed -n '1,220p' /candidate/run-input.json
sed -n '1,220p' /candidate/metrics.json
sed -n '1,220p' /candidate/codex-last.txt

echo '$ bounded untrusted log/trace claims'
rg -n '#Top|RESULT:|WarnStuck|task_complete|final_answer' \
  /candidate/codex-output.log \
  /candidate/codex-trace/2026/07/22/rollout-2026-07-22T04-01-20-019f890e-de6c-7bd2-8b98-1f7c993a736c.jsonl \
  | tail -n 80 | cut -c1-2400

echo 'SCRIPT_EXIT_STATUS=0'
