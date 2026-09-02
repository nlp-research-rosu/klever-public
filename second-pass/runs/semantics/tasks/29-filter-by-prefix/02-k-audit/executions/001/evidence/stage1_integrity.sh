#!/usr/bin/env bash
set -u

candidate=/candidate
reference=/reference

status=0

printf '%s\n' 'COMMAND: find -P /candidate -printf "%y %p -> %l\n" | sort'
find -P "$candidate" -printf '%y %p -> %l\n' | sort
rc=$?
printf 'EXIT: %d\n\n' "$rc"
(( rc == 0 )) || status=1

printf '%s\n' 'COMMAND: find -P /reference -printf "%y %p -> %l\n" | sort'
find -P "$reference" -printf '%y %p -> %l\n' | sort
rc=$?
printf 'EXIT: %d\n\n' "$rc"
(( rc == 0 )) || status=1

printf '%s\n' 'COMMAND: test -d /reference/reference-semantics'
test -d "$reference/reference-semantics"
rc=$?
printf 'EXIT: %d\n\n' "$rc"
(( rc == 0 )) || status=1

for name in run-input.json metrics.json codex-last.txt codex-output.log; do
  printf 'COMMAND: test -f /candidate/%s\n' "$name"
  test -f "$candidate/$name"
  rc=$?
  printf 'EXIT: %d\n\n' "$rc"
  (( rc == 0 )) || status=1
done

for name in prompt.py py2mpy.py; do
  printf 'COMMAND: cmp -s /candidate/%s /reference/%s\n' "$name" "$name"
  cmp -s "$candidate/$name" "$reference/$name"
  rc=$?
  printf 'EXIT: %d\n' "$rc"
  if (( rc != 0 )); then
    diff -u "$reference/$name" "$candidate/$name" || true
    status=1
  fi
  printf '\n'
done

printf '%s\n' 'COMMAND: find /candidate/reference-semantics -type l -print'
find "$candidate/reference-semantics" -type l -print
rc=$?
printf 'EXIT: %d\n\n' "$rc"
(( rc == 0 )) || status=1

printf '%s\n' 'COMMAND: diff -ruN --no-dereference /reference/reference-semantics /candidate/reference-semantics'
diff -ruN --no-dereference "$reference/reference-semantics" "$candidate/reference-semantics"
rc=$?
printf 'EXIT: %d\n\n' "$rc"
(( rc == 0 )) || status=1

printf '%s\n' 'COMMAND: sha256sum candidate and trusted required inputs'
sha256sum \
  "$candidate/prompt.py" "$reference/prompt.py" \
  "$candidate/py2mpy.py" "$reference/py2mpy.py" \
  "$candidate/reference-semantics/semantics.k" \
  "$reference/reference-semantics/semantics.k"
rc=$?
printf 'EXIT: %d\n\n' "$rc"
(( rc == 0 )) || status=1

printf 'SCRIPT_EXIT: %d\n' "$status"
exit "$status"
