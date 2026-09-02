#!/usr/bin/env bash
set -u

candidate=/candidate
reference=/reference

printf '%s\n' 'Candidate top-level inventory:'
find "$candidate" -mindepth 1 -maxdepth 1 -printf '%y %f -> %l\n' | sort

printf '%s\n' 'Required untrusted generation records:'
for artifact in run-input.json metrics.json codex-last.txt codex-output.log; do
  if [[ -e "$candidate/$artifact" || -L "$candidate/$artifact" ]]; then
    stat --printf='%F %n\n' "$candidate/$artifact"
  else
    printf 'MISSING %s\n' "$candidate/$artifact"
  fi
done

printf '%s\n' 'Potential structured trace records:'
find "$candidate" -maxdepth 1 \
  \( -iname '*trace*' -o -iname '*generation*.json' -o -iname '*events*.jsonl' \) \
  -printf '%y %p -> %l\n' | sort

printf '%s\n' 'Candidate prompt comparison:'
cmp --silent "$reference/prompt.py" "$candidate/prompt.py"
printf 'prompt.py cmp exit: %d\n' "$?"
sha256sum "$reference/prompt.py" "$candidate/prompt.py"

printf '%s\n' 'Candidate translator comparison:'
cmp --silent "$reference/py2mpy.py" "$candidate/py2mpy.py"
printf 'py2mpy.py cmp exit: %d\n' "$?"
sha256sum "$reference/py2mpy.py" "$candidate/py2mpy.py"

printf '%s\n' 'Supplied semantics recursive comparison:'
diff -r --no-dereference \
  "$reference/reference-semantics" \
  "$candidate/reference-semantics"
printf 'semantics diff exit: %d\n' "$?"

printf '%s\n' 'Supplied semantics non-directory/non-regular entries:'
find "$candidate/reference-semantics" \
  ! -type d ! -type f -printf '%y %p -> %l\n' | sort

printf '%s\n' 'Supplied semantics entry inventory:'
find "$candidate/reference-semantics" -printf '%y %P -> %l\n' | sort
