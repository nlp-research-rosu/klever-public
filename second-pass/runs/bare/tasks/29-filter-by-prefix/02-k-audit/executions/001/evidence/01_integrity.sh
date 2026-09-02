#!/usr/bin/env bash
set -u

printf '%s\n' 'COMMAND: find /reference -maxdepth 3 -printf ... | sort'
find /reference -maxdepth 3 -printf '%y %p -> %l\n' | sort
printf 'EXIT: %s\n\n' "$?"

printf '%s\n' 'COMMAND: test ! -e /reference/reference-semantics && test ! -L /reference/reference-semantics'
test ! -e /reference/reference-semantics && test ! -L /reference/reference-semantics
printf 'EXIT: %s\n\n' "$?"

printf '%s\n' 'COMMAND: find /candidate -maxdepth 8 -printf ... | sort'
find /candidate -maxdepth 8 -printf '%y %s %p -> %l\n' | sort
printf 'EXIT: %s\n\n' "$?"

printf '%s\n' 'COMMAND: find /candidate -type l -printf ...'
find /candidate -type l -printf '%p -> %l\n'
printf 'EXIT: %s\n\n' "$?"

printf '%s\n' 'COMMAND: sha256sum trusted and candidate identity inputs'
sha256sum \
  /reference/prompt.py /candidate/prompt.py \
  /reference/py2mpy.py /candidate/py2mpy.py \
  /reference/canonical.py \
  /candidate/solution.py /candidate/solution.mpy \
  /candidate/semantic.k /candidate/verification.k /candidate/spec.k
printf 'EXIT: %s\n\n' "$?"

printf '%s\n' 'COMMAND: cmp -s /reference/prompt.py /candidate/prompt.py'
cmp -s /reference/prompt.py /candidate/prompt.py
printf 'EXIT: %s\n\n' "$?"

printf '%s\n' 'COMMAND: cmp -s /reference/py2mpy.py /candidate/py2mpy.py'
cmp -s /reference/py2mpy.py /candidate/py2mpy.py
printf 'EXIT: %s\n\n' "$?"

printf '%s\n' 'COMMAND: test required candidate artifacts are regular non-symlink files'
status=0
for path in \
  /candidate/run-input.json /candidate/metrics.json \
  /candidate/codex-last.txt /candidate/codex-output.log \
  /candidate/prompt.py /candidate/py2mpy.py \
  /candidate/solution.py /candidate/solution.mpy \
  /candidate/semantic.k /candidate/verification.k \
  /candidate/spec.k /candidate/prove.sh
do
  if test -f "$path" && test ! -L "$path"; then
    printf 'OK regular non-symlink: %s\n' "$path"
  else
    printf 'BAD type or missing: %s\n' "$path"
    status=1
  fi
done
trace_count=$(find /candidate/codex-trace -type f -name '*.jsonl' | wc -l)
printf 'structured trace JSONL count: %s\n' "$trace_count"
if test "$trace_count" -lt 1; then
  status=1
fi
printf 'EXIT: %s\n' "$status"

printf '\n%s\n' 'COMMAND: stat -c permissions for required executable/source artifacts'
stat -c '%A %a %n' \
  /candidate/prove.sh /candidate/solution.py /candidate/solution.mpy \
  /candidate/semantic.k /candidate/verification.k /candidate/spec.k
stat_status=$?
printf 'EXIT: %s\n' "$stat_status"
if test "$stat_status" -ne 0; then
  status=1
fi
exit "$status"
