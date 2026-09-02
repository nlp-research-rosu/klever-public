#!/usr/bin/env bash
set -u

candidate_root=/candidate
reference_root=/reference
failures=0

printf '%s\n' 'SEMANTICS_MODE: SUPPLIED_SEMANTICS'
if [[ -d "$reference_root/reference-semantics" ]]; then
  printf '%s\n' 'TRUSTED_SEMANTICS_PRESENT: yes'
else
  printf '%s\n' 'TRUSTED_SEMANTICS_PRESENT: no'
  failures=$((failures + 1))
fi

for path in \
  "$candidate_root/solution.py" \
  "$candidate_root/solution.mpy" \
  "$candidate_root/prompt.py" \
  "$candidate_root/py2mpy.py" \
  "$candidate_root/spec.k" \
  "$candidate_root/verification.k" \
  "$candidate_root/reference-semantics"
do
  if [[ -e "$path" ]]; then
    printf 'REQUIRED_ARTIFACT: present %s type=%s\n' "$path" "$(stat -c %F "$path")"
  else
    printf 'REQUIRED_ARTIFACT: MISSING %s\n' "$path"
    failures=$((failures + 1))
  fi
done

for name in run-input.json metrics.json codex-last.txt codex-output.log
do
  if [[ -e "$candidate_root/$name" ]]; then
    printf 'PROVENANCE_ARTIFACT: present %s\n' "$candidate_root/$name"
  else
    printf 'PROVENANCE_ARTIFACT: MISSING %s\n' "$candidate_root/$name"
  fi
done

trace_count=$(find "$candidate_root" -maxdepth 1 -type f \
  \( -iname '*trace*.json' -o -iname '*trace*.jsonl' -o -iname '*trace*.log' \) \
  -print | wc -l)
printf 'STRUCTURED_TRACE_COUNT: %s\n' "$trace_count"

candidate_symlinks=$(find "$candidate_root" -type l -print)
reference_symlinks=$(find "$reference_root/reference-semantics" -type l -print)
printf 'CANDIDATE_SYMLINKS_BEGIN\n%s\nCANDIDATE_SYMLINKS_END\n' "$candidate_symlinks"
printf 'TRUSTED_SEMANTICS_SYMLINKS_BEGIN\n%s\nTRUSTED_SEMANTICS_SYMLINKS_END\n' "$reference_symlinks"
if [[ -n "$candidate_symlinks" ]]; then
  failures=$((failures + 1))
fi

diff -r --no-dereference \
  "$reference_root/reference-semantics" \
  "$candidate_root/reference-semantics"
semantics_status=$?
printf 'SEMANTICS_RECURSIVE_DIFF_EXIT: %s\n' "$semantics_status"
if (( semantics_status != 0 )); then
  failures=$((failures + 1))
fi

cmp "$reference_root/prompt.py" "$candidate_root/prompt.py"
prompt_status=$?
printf 'PROMPT_BYTE_CMP_EXIT: %s\n' "$prompt_status"
if (( prompt_status != 0 )); then
  failures=$((failures + 1))
fi

cmp "$reference_root/py2mpy.py" "$candidate_root/py2mpy.py"
translator_status=$?
printf 'TRANSLATOR_BYTE_CMP_EXIT: %s\n' "$translator_status"
if (( translator_status != 0 )); then
  failures=$((failures + 1))
fi

sha256sum \
  "$reference_root/prompt.py" \
  "$candidate_root/prompt.py" \
  "$reference_root/py2mpy.py" \
  "$candidate_root/py2mpy.py" \
  "$reference_root/canonical.py" \
  "$candidate_root/solution.py" \
  "$candidate_root/solution.mpy" \
  "$candidate_root/spec.k" \
  "$candidate_root/verification.k"

printf 'INTEGRITY_FAILURE_COUNT: %s\n' "$failures"
exit "$failures"
