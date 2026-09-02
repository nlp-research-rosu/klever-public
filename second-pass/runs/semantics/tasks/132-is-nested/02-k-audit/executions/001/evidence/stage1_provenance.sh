#!/usr/bin/env bash
set -u

run() {
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  local command_status=$?
  printf '[exit %d]\n' "$command_status"
  return 0
}

run find /candidate -printf '%y %p -> %l\n'
run find /reference -printf '%y %p -> %l\n'
run cmp -s /reference/prompt.py /candidate/prompt.py
run cmp -s /reference/py2mpy.py /candidate/py2mpy.py
run python3 /audit-output/evidence/tree_integrity.py \
  /reference/reference-semantics /candidate/reference-semantics

for artifact in run-input.json metrics.json codex-last.txt codex-output.log; do
  if [[ -e "/candidate/$artifact" ]]; then
    run stat -c '%F %s bytes %n' "/candidate/$artifact"
    run sed -n '1,240p' "/candidate/$artifact"
  else
    printf 'MISSING /candidate/%s\n' "$artifact"
  fi
done

run find /candidate -maxdepth 2 \
  \( -iname '*trace*' -o -iname '*.jsonl' -o -iname '*generation*' \) \
  -printf '%y %p -> %l\n'
