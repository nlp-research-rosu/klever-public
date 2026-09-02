#!/usr/bin/env bash
set -u

candidate=/candidate
reference=/reference

printf '%s\n' '== Required provenance artifacts =='
for name in run-input.json metrics.json codex-last.txt codex-output.log; do
  if [[ -e "$candidate/$name" || -L "$candidate/$name" ]]; then
    printf 'PRESENT type=%s path=%s\n' "$(stat -c '%F' "$candidate/$name")" "$candidate/$name"
  else
    printf 'MISSING path=%s\n' "$candidate/$name"
  fi
done

printf '%s\n' '== Structured generation trace candidates =='
find "$candidate" -maxdepth 1 \( -iname '*trace*' -o -iname '*trajectory*' \) -printf '%y %p -> %l\n' | sort

printf '%s\n' '== Candidate symlinks =='
find "$candidate" -type l -printf '%p -> %l\n' | sort

printf '%s\n' '== Trusted semantics mount =='
if [[ -d "$reference/reference-semantics" && ! -L "$reference/reference-semantics" ]]; then
  printf 'PRESENT_DIRECTORY %s\n' "$reference/reference-semantics"
else
  printf 'MODE_CONTRADICTION type=%s path=%s\n' \
    "$(stat -c '%F' "$reference/reference-semantics" 2>/dev/null || printf MISSING)" \
    "$reference/reference-semantics"
fi

printf '%s\n' '== prompt.py comparison =='
cmp "$candidate/prompt.py" "$reference/prompt.py"
prompt_status=$?
printf 'CMP_EXIT_STATUS: %d\n' "$prompt_status"
sha256sum "$candidate/prompt.py" "$reference/prompt.py"

printf '%s\n' '== py2mpy.py comparison =='
cmp "$candidate/py2mpy.py" "$reference/py2mpy.py"
translator_status=$?
printf 'CMP_EXIT_STATUS: %d\n' "$translator_status"
sha256sum "$candidate/py2mpy.py" "$reference/py2mpy.py"

printf '%s\n' '== reference-semantics recursive comparison =='
diff -ruN --no-dereference \
  "$reference/reference-semantics" \
  "$candidate/reference-semantics"
semantics_status=$?
printf 'DIFF_EXIT_STATUS: %d\n' "$semantics_status"

printf '%s\n' '== reference-semantics entry types and hashes =='
find "$candidate/reference-semantics" -printf '%y %P -> %l\n' | sort
find "$candidate/reference-semantics" -type f -print0 | sort -z | xargs -0 sha256sum

exit 0
