#!/usr/bin/env bash
set -uo pipefail

candidate=/candidate
reference=/reference

printf '%s\n' 'SEMANTICS_MODE: SUPPLIED_SEMANTICS'
if [[ -d "$reference/reference-semantics" ]]; then
  printf '%s\n' 'TRUSTED_SEMANTICS_PRESENT: yes'
else
  printf '%s\n' 'TRUSTED_SEMANTICS_PRESENT: no'
fi

printf '%s\n' 'CANDIDATE_TOP_LEVEL_BEGIN'
find "$candidate" -maxdepth 1 -mindepth 1 -printf '%y %f -> %l\n' | sort
printf '%s\n' 'CANDIDATE_TOP_LEVEL_END'

for artifact in \
  run-input.json metrics.json codex-last.txt codex-output.log \
  prompt.py py2mpy.py solution.py solution.mpy spec.k verification.k \
  reference-semantics
do
  path="$candidate/$artifact"
  if [[ -e "$path" || -L "$path" ]]; then
    file_type=$(stat -c '%F' "$path")
    printf 'ARTIFACT %-24s PRESENT type=%s\n' "$artifact" "$file_type"
  else
    printf 'ARTIFACT %-24s MISSING\n' "$artifact"
  fi
done

printf '%s\n' 'CANDIDATE_SYMLINKS_BEGIN'
find "$candidate" -type l -printf '%p -> %l\n' | sort
printf '%s\n' 'CANDIDATE_SYMLINKS_END'

for pair in \
  "$candidate/prompt.py:$reference/prompt.py:prompt.py" \
  "$candidate/py2mpy.py:$reference/py2mpy.py:py2mpy.py"
do
  candidate_path=${pair%%:*}
  remainder=${pair#*:}
  reference_path=${remainder%%:*}
  label=${remainder##*:}
  if cmp -s "$candidate_path" "$reference_path"; then
    printf 'BYTE_COMPARE %s: IDENTICAL\n' "$label"
  else
    cmp_status=$?
    printf 'BYTE_COMPARE %s: DIFFERENT_OR_MISSING cmp_status=%d\n' "$label" "$cmp_status"
  fi
done

printf '%s\n' 'SEMANTICS_TREE_DIFF_BEGIN'
diff -r --no-dereference "$reference/reference-semantics" "$candidate/reference-semantics"
diff_status=$?
printf 'SEMANTICS_TREE_DIFF_STATUS: %d\n' "$diff_status"
printf '%s\n' 'SEMANTICS_TREE_DIFF_END'

printf '%s\n' 'SEMANTICS_MANIFEST_BEGIN'
find "$candidate/reference-semantics" -printf '%y %P -> %l\n' | sort
printf '%s\n' 'SEMANTICS_MANIFEST_END'

if [[ "$diff_status" -ne 0 ]]; then
  exit 1
fi
