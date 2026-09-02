#!/usr/bin/env bash
set -u

status=0

printf '%s\n' 'COMMAND: test ! -e /reference/reference-semantics && test ! -L /reference/reference-semantics'
test ! -e /reference/reference-semantics && test ! -L /reference/reference-semantics
code=$?
printf 'EXIT: %s\n' "$code"
(( code == 0 )) || status=1

printf '%s\n' 'COMMAND: find /reference -maxdepth 2 -printf "%y %p -> %l\n" | sort'
find /reference -maxdepth 2 -printf '%y %p -> %l\n' | sort
code=$?
printf 'EXIT: %s\n' "$code"
(( code == 0 )) || status=1

printf '%s\n' 'COMMAND: find /candidate -maxdepth 2 -printf "%y %p -> %l\n" | sort'
find /candidate -maxdepth 2 -printf '%y %p -> %l\n' | sort
code=$?
printf 'EXIT: %s\n' "$code"
(( code == 0 )) || status=1

printf '%s\n' 'COMMAND: find /candidate -type l -printf "%p -> %l\n"'
find /candidate -type l -printf '%p -> %l\n'
code=$?
printf 'EXIT: %s\n' "$code"
(( code == 0 )) || status=1

required=(
  run-input.json metrics.json codex-last.txt codex-output.log
  prompt.py py2mpy.py solution.py solution.mpy semantic.k
  verification.k spec.k prove.sh
)
for name in "${required[@]}"; do
  printf 'COMMAND: test -f /candidate/%s && test ! -L /candidate/%s\n' "$name" "$name"
  test -f "/candidate/$name" && test ! -L "/candidate/$name"
  code=$?
  printf 'EXIT: %s\n' "$code"
  (( code == 0 )) || status=1
done

printf '%s\n' 'COMMAND: find /candidate/codex-trace -type f -name "*.jsonl" -printf "%p\n" | sort'
find /candidate/codex-trace -type f -name '*.jsonl' -printf '%p\n' | sort
code=$?
printf 'EXIT: %s\n' "$code"
(( code == 0 )) || status=1

printf '%s\n' 'COMMAND: sha256sum trusted and candidate prompt/translator'
sha256sum \
  /reference/prompt.py /candidate/prompt.py \
  /reference/py2mpy.py /candidate/py2mpy.py
code=$?
printf 'EXIT: %s\n' "$code"
(( code == 0 )) || status=1

printf '%s\n' 'COMMAND: cmp /candidate/prompt.py /reference/prompt.py'
cmp /candidate/prompt.py /reference/prompt.py
code=$?
printf 'EXIT: %s\n' "$code"
(( code == 0 )) || status=1

printf '%s\n' 'COMMAND: cmp /candidate/py2mpy.py /reference/py2mpy.py'
cmp /candidate/py2mpy.py /reference/py2mpy.py
code=$?
printf 'EXIT: %s\n' "$code"
(( code == 0 )) || status=1

printf '%s\n' 'COMMAND: python3 -m json.tool /candidate/run-input.json'
python3 -m json.tool /candidate/run-input.json
code=$?
printf 'EXIT: %s\n' "$code"
(( code == 0 )) || status=1

printf '%s\n' 'COMMAND: python3 -m json.tool /candidate/metrics.json'
python3 -m json.tool /candidate/metrics.json
code=$?
printf 'EXIT: %s\n' "$code"
(( code == 0 )) || status=1

printf '%s\n' 'COMMAND: sed -n "1,80p" /candidate/codex-last.txt'
sed -n '1,80p' /candidate/codex-last.txt
code=$?
printf 'EXIT: %s\n' "$code"
(( code == 0 )) || status=1

printf '%s\n' 'COMMAND: rg -n "python differential cases:|#Top|RESULT: KPROVE|backend terminated" /candidate/codex-output.log'
rg -n 'python differential cases:|#Top|RESULT: KPROVE|backend terminated' \
  /candidate/codex-output.log | head -n 80
code=${PIPESTATUS[0]}
printf 'RG_EXIT: %s\n' "$code"

printf '%s\n' 'COMMAND: python3 /audit-output/evidence/trace_summary.py'
python3 /audit-output/evidence/trace_summary.py
code=$?
printf 'EXIT: %s\n' "$code"
(( code == 0 )) || status=1

exit "$status"
