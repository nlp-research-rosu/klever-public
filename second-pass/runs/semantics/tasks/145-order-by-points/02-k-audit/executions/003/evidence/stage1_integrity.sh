#!/usr/bin/env bash
set -u

record_status() {
  local status=$1
  printf 'EXIT_STATUS: %s\n' "$status"
}

printf '%s\n' 'COMMAND: python3 /audit-output/evidence/stage1_integrity_check.py'
python3 /audit-output/evidence/stage1_integrity_check.py
record_status "$?"

printf '%s\n' 'COMMAND: diff -r --no-dereference /candidate/reference-semantics /reference/reference-semantics'
diff -r --no-dereference /candidate/reference-semantics /reference/reference-semantics
record_status "$?"

printf '%s\n' 'COMMAND: cmp -s /candidate/prompt.py /reference/prompt.py'
cmp -s /candidate/prompt.py /reference/prompt.py
record_status "$?"

printf '%s\n' 'COMMAND: cmp -s /candidate/py2mpy.py /reference/py2mpy.py'
cmp -s /candidate/py2mpy.py /reference/py2mpy.py
record_status "$?"

printf '%s\n' 'COMMAND: find required mounts -type l'
find /candidate /reference /generation-evidence -type l -print | sort
record_status "$?"
