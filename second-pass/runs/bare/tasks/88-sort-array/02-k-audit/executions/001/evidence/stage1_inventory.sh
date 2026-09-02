#!/usr/bin/env bash
set -u
set -x

test ! -e /reference/reference-semantics
test ! -L /reference/reference-semantics

find /candidate -printf '%y %m %s %p -> %l\n' | LC_ALL=C sort
find /candidate -type l -printf 'SYMLINK %p -> %l\n' | LC_ALL=C sort
find /reference -printf '%y %m %s %p -> %l\n' | LC_ALL=C sort
find /reference -type l -printf 'SYMLINK %p -> %l\n' | LC_ALL=C sort

sha256sum \
  /candidate/prompt.py /reference/prompt.py \
  /candidate/py2mpy.py /reference/py2mpy.py

cmp /candidate/prompt.py /reference/prompt.py
prompt_cmp_status=$?
printf 'PROMPT_CMP_STATUS=%d\n' "$prompt_cmp_status"

cmp /candidate/py2mpy.py /reference/py2mpy.py
translator_cmp_status=$?
printf 'TRANSLATOR_CMP_STATUS=%d\n' "$translator_cmp_status"

for required in \
  run-input.json metrics.json codex-last.txt codex-output.log \
  prompt.py py2mpy.py solution.py solution.mpy semantic.k \
  verification.k spec.k
do
  if [[ -f "/candidate/$required" && ! -L "/candidate/$required" ]]; then
    printf 'REQUIRED_OK=%s\n' "$required"
  else
    printf 'REQUIRED_BAD=%s\n' "$required"
  fi
done

python3 -m json.tool /candidate/run-input.json
run_input_status=$?
printf 'RUN_INPUT_JSON_STATUS=%d\n' "$run_input_status"

python3 -m json.tool /candidate/metrics.json
metrics_status=$?
printf 'METRICS_JSON_STATUS=%d\n' "$metrics_status"

find /candidate/codex-trace -type f -maxdepth 3 -printf '%p\n' | LC_ALL=C sort
