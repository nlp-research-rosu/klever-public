#!/usr/bin/env bash
set -u

echo 'COMMAND: test ! -e /reference/reference-semantics && test ! -L /reference/reference-semantics'
test ! -e /reference/reference-semantics && test ! -L /reference/reference-semantics
status=$?
echo "EXIT_STATUS: $status"

echo 'COMMAND: find /candidate -maxdepth 2 -printf ... | sort'
find /candidate -maxdepth 2 -printf '%y %p -> %l\n' | sort
status=$?
echo "EXIT_STATUS: $status"

echo 'COMMAND: stat required candidate artifacts'
status=0
for name in run-input.json metrics.json codex-last.txt codex-output.log prompt.py py2mpy.py solution.py solution.mpy semantic.k spec.k verification.k prove.sh; do
  if ! stat -c '%F|%a|%s|%n|%N' "/candidate/$name"; then
    status=1
  fi
done
echo "EXIT_STATUS: $status"

trace_path=/candidate/codex-trace/2026/07/22/rollout-2026-07-22T06-31-34-019f8998-69bf-7eb3-ab26-2035b23baca9.jsonl
echo "COMMAND: stat structured generation trace $trace_path"
stat -c '%F|%a|%s|%n|%N' "$trace_path"
status=$?
echo "EXIT_STATUS: $status"

echo 'COMMAND: sha256sum provenance and trusted inputs'
sha256sum \
  /candidate/run-input.json \
  /candidate/metrics.json \
  /candidate/codex-last.txt \
  /candidate/codex-output.log \
  "$trace_path" \
  /candidate/prompt.py \
  /reference/prompt.py \
  /candidate/py2mpy.py \
  /reference/py2mpy.py \
  /reference/canonical.py
status=$?
echo "EXIT_STATUS: $status"

echo 'COMMAND: cmp candidate prompt/translator against trusted mounts'
cmp /candidate/prompt.py /reference/prompt.py
prompt_status=$?
cmp /candidate/py2mpy.py /reference/py2mpy.py
translator_status=$?
echo "PROMPT_CMP_EXIT_STATUS: $prompt_status"
echo "TRANSLATOR_CMP_EXIT_STATUS: $translator_status"

echo 'COMMAND: display untrusted run-input.json, metrics.json, codex-last.txt'
sed -n '1,240p' /candidate/run-input.json
sed -n '1,240p' /candidate/metrics.json
sed -n '1,240p' /candidate/codex-last.txt
status=$?
echo "EXIT_STATUS: $status"

echo 'COMMAND: bounded untrusted log claim scan'
rg -n -i 'kprove|kompile|krun|#Top|WarnStuck|\\[Error\\]|RESULT:' /candidate/codex-output.log | tail -n 160
status=$?
echo "EXIT_STATUS: $status"

echo 'COMMAND: structured trace record count and terminal claim scan'
wc -l "$trace_path"
rg -n '"type":"task_complete"|RESULT:|#Top|WarnStuck|\\[Error\\]' "$trace_path" | tail -n 80
status=$?
echo "EXIT_STATUS: $status"
