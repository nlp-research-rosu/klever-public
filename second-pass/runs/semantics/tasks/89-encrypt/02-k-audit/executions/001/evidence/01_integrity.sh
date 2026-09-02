#!/usr/bin/env bash
set -u

echo 'COMMAND: diff -r --no-dereference /reference/reference-semantics /candidate/reference-semantics'
diff -r --no-dereference /reference/reference-semantics /candidate/reference-semantics
audit_semantics_status=$?
echo "EXIT_STATUS: ${audit_semantics_status}"

echo 'COMMAND: cmp -s /reference/prompt.py /candidate/prompt.py'
cmp -s /reference/prompt.py /candidate/prompt.py
audit_prompt_status=$?
echo "EXIT_STATUS: ${audit_prompt_status}"

echo 'COMMAND: cmp -s /reference/py2mpy.py /candidate/py2mpy.py'
cmp -s /reference/py2mpy.py /candidate/py2mpy.py
audit_translator_status=$?
echo "EXIT_STATUS: ${audit_translator_status}"

echo 'COMMAND: find /candidate -maxdepth 3 -printf ... | sort'
find /candidate -maxdepth 3 -printf '%y %p -> %l\n' | sort
audit_find_status=$?
echo "EXIT_STATUS: ${audit_find_status}"

echo 'COMMAND: test required generation metadata and search for structured trace'
for audit_name in run-input.json metrics.json codex-last.txt codex-output.log; do
  if test -e "/candidate/${audit_name}"; then
    stat -c '%F %n -> %N' "/candidate/${audit_name}"
  else
    echo "MISSING /candidate/${audit_name}"
  fi
done
find /candidate -maxdepth 2 \( -iname '*trace*' -o -iname '*.jsonl' -o -iname '*.json' \) \
  -printf '%y %p -> %l\n' | sort
audit_metadata_status=$?
echo "EXIT_STATUS: ${audit_metadata_status}"

if (( audit_semantics_status != 0 || audit_prompt_status != 0 || audit_translator_status != 0 || audit_find_status != 0 || audit_metadata_status != 0 )); then
  exit 1
fi
